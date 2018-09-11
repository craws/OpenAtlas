var shapeType; // point, shape or area
var geometryType; // point or polygon
var captureCoordinates = false; // boolean if clicks on map should be captured as coordinates
var marker = false; // temporary marker for point coordinate
var geoJsonArray = []; // polygon coordinates storage
var objectName = ''; // name of the entry at update of an existing entry
var drawnPolygon = L.featureGroup();
var newIcon = L.icon({iconUrl: '/static/images/map/marker-icon_new.png', iconAnchor: [12, 41], popupAnchor: [0, -34]});
var layer;

/* Controls with EasyButton */
L.Control.EasyButtons = L.Control.extend({
    onAdd: function () {
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        this.link = L.DomUtil.create('a', 'leaflet-bar-part', container);
        this._addImage()
        this.link.href = '#';
        L.DomEvent.on(this.link, 'click', this._click, this);
        this.link.title = this.options.title;
        return container;
    },
    _click: function (e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);
        this.intendedFunction();
    },
    _addImage: function () {
        var extraClasses = this.options.intentedIcon.lastIndexOf('fa', 0) === 0 ? ' fa fa-lg' : ' glyphicon';
        L.DomUtil.create('i', this.options.intentedIcon + extraClasses, this.link);
    }
});

var polygonButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-pencil-square-o',
    title: translate['map_info_shape']
})
polygonButton.intendedFunction = function() {drawGeometry('shape');}
map.addControl(polygonButton);

var areaButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-circle-o-notch',
    title: translate['map_info_area']
})
areaButton.intendedFunction = function() {drawGeometry('area');}
map.addControl(areaButton);

var pointButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-map-marker',
    title: translate['map_info_point']
})
pointButton.intendedFunction = function () {drawGeometry('point');}
map.addControl(pointButton);

/* Input form */
var inputForm = L.control();
inputForm.onAdd = function (map) {
    div = L.DomUtil.create('div', 'shapeInput');
    div.innerHTML += `
        <div id="insertForm" style="display:block">
            <form id="shapeForm" onmouseover="interactionOff()" onmouseout="interactionOn()">
                <input type="hidden" id="shapeParent" value="NULL" />
                <input type="hidden" id="shapeCoordinates" />
                <span id="inputFormTitle"></span>
                <span id="closeButton" title="` + translate["map_info_close"] + `" onclick="closeForm()" class="fa">X</span>
                <p id="inputFormInfo"></p>
                <div id="nameField" style="display: block">
                    <input type="text" id="shapeName" placeholder="Enter a name if desired" />
                </div>
                <textarea rows="3" cols="70" id="shapeDescription" placeholder="` + translate["map_info_description"] + `"/></textarea>
                <div id="coordinatesDiv">
                    <div style="display:block;clear:both;">
                        <label for='easting'>Easting</label>
                        <input type="text" style="margin-top:0.5em;" oninput="check_coordinates_input()" id="easting" placeholder="decimal degrees" />
                    </div>
                    <div style="display:block;clear:both;">
                        <label for='northing'>Northing</label>
                        <input type="text" style="margin-top:0.5em;" oninput="check_coordinates_input()" id="northing" placeholder="decimal degrees" />
                    </div>
                </div>
                <input type="button" title="Reset values and shape" id="resetButton" disabled value="` + translate["map_clear"] + `" onclick="resetForm()" />
                <input type="button" title="` + translate["save"] + `" id="saveButton" disabled value="` + translate["save"] + `" onclick="saveForm()" />
            </form>
         </div>`;
    return div;
};

map.on('click', function(e) {
    if (captureCoordinates && shapeType == 'point') {
        $('#saveButton').prop('disabled', false);
        if (marker) {  // marker already exists so move it
            marker.setLatLng(e.latlng);
            marker.on('dragend', function (event) {
                var marker = event.target;
                position = marker.getLatLng();
                $('#northing').val(position.lat);
                $('#easting').val(position.lng);
            });
        } else {  // no marker exists so create it
            marker = new L.marker(e.latlng, {draggable: true, icon: newIcon});
            marker.addTo(map);
            wgs84 = (marker.getLatLng());
            $('#northing').val(wgs84.lat);
            $('#easting').val(wgs84.lng);
        }
        wgs84 = marker.getLatLng();
        marker.on('dragend', function (event) {
            var marker = event.target;
            position = marker.getLatLng();
            $('#northing').val(position.lat);
            $('#easting').val(position.lng);
        });
        $('#northing').val(wgs84.lat);
        $('#easting').val(wgs84.lng);
    }
});

map.on('draw:created', function (e) {
    drawnPolygon.addLayer(e.layer);
    layer = e.layer;
    if (geometryType == 'point') {
        coordinates = layer.getLatLng();
        shapeSyntax = 'ST_GeomFromText(\'POINT(' + (' ' + coordinates.lng + ' ' + coordinates.lat) + ')\',4326);'
    } else {  // It's a polygon
        vector = []; // Array to store coordinates as numbers
        geoJsonArray = [];
        coordinates = layer.getLatLngs()[0];
        for (i = 0; i < (coordinates.length); i++) {
            vector.push(' ' + coordinates[i].lng + ' ' + coordinates[i].lat);
            geoJsonArray.push('[' + coordinates[i].lng + ',' + coordinates[i].lat + ']');
        }
        // Add first xy again as last xy to close polygon
        vector.push(' ' + coordinates[0].lng + ' ' + coordinates[0].lat);
        geoJsonArray.push('[' + coordinates[0].lng + ',' + coordinates[0].lat + ']');
        $('#shapeCoordinates').val('(' + vector + ')');
    }
    $('#saveButton').prop('disabled', false);
    $('#resetButton').prop('disabled', false);
});

function closeForm(withoutSave = true) {
    inputForm.remove(map);
    $('.leaflet-right .leaflet-bar').show();
    interactionOn();
    $('#map').css('cursor', '');
    if (shapeType != 'point' && withoutSave) {
        drawnPolygon.removeLayer(layer);
        drawLayer.disable();
    }
    if (marker) {
        map.removeLayer(marker);
    }
    captureCoordinates = false; // Important that this is the last statement
}

function drawGeometry(selectedType) {
    shapeType = selectedType;
    map.addControl(inputForm);
    if (shapeType == 'point') {
        geometryType = 'point';
        $('#resetButton').hide();
        $('#coordinatesDiv').show();
    } else {
        geometryType = 'polygon';
        captureCoordinates = false;
        drawLayer = new L.Draw.Polygon(map);
        map.addLayer(drawnPolygon);
        drawLayer.enable();
        $('#coordinatesDiv').hide();
    }
    $('#inputFormTitle').text(shapeType.substr(0,1).toUpperCase() + shapeType.substr(1));
    $('#inputFormInfo').text(translate['map_info_' + shapeType]);
    $('.leaflet-right .leaflet-bar').hide();
}

function interactionOn() {
    // Enable interaction with map e.g. if cursor leaves form
    captureCoordinates = true;
    map.dragging.enable();
    map.touchZoom.enable();
    map.doubleClickZoom.enable();
    map.scrollWheelZoom.enable();
    map.boxZoom.enable();
    map.keyboard.enable();
    if (map.tap) {
        map.tap.enable();
    }
    $('#map').css( 'cursor', 'crosshair');
}

function interactionOff() {
    // Disable interaction with map e.g. if cursor is over a form
    captureCoordinates = false;
    map.dragging.disable();
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    map.scrollWheelZoom.disable();
    map.boxZoom.disable();
    map.keyboard.disable();
    if (map.tap) {
        map.tap.disable();
    }
}

function resetForm() {
    captureCoordinates = false;
    map.closePopup();
    drawnPolygon.removeLayer(layer);
    drawLayer.enable();
    $('#saveButton').prop('disabled', true);
    $('#resetButton').prop('disabled', true);
}

function saveForm() {
    name = $('#shapeName').val().replace(/\"/g,'\\"');
    description = $('#shapeDescription').val().replace(/\"/g,'\\"');
    popupHtml = `
        <div id="popup">
            <strong>` + objectName + `</strong>
            <br /><strong>` + name + `</strong> ` + shapeType + `
            <div style="max-height:140px;overflow-y:auto">` + description + `</div>
            <p><i>` + translate['map_info_reedit'] + `</i></p>
        </div>`;
    if (shapeType == 'point') {
        point =
            `{"type": "Feature","geometry":` +
            `{"type": "Point","coordinates": [` + $('#easting').val() + `,` + $('#northing').val() + `]},` +
            `"properties":{"name": "` + name + `","description": "` + description + `", "shapeType": "centerpoint"}}`;
        points = JSON.parse($('#gis_points').val());
        points.push(JSON.parse(point));
        $('#gis_points').val(JSON.stringify(points));
        var newMarker = L.marker(([$('#northing').val(), $('#easting').val()]), {icon: newIcon}).addTo(map);
        newMarker.bindPopup(popupHtml);
        marker = false;  // unset the marker
    } else {
        coordinates = $('#shapeCoordinates').val();
        polygon =
            `{"type":"Feature","geometry":` +
            `{"type":"Polygon","coordinates":[[` + geoJsonArray.join(',') + `]]},"properties":` +
            `{"name": "` + name + `","description": "` + description + `", "shapeType": "` + shapeType + `"}}`;
        polygons = JSON.parse($('#gis_polygons').val());
        polygons.push(JSON.parse(polygon));
        $('#gis_polygons').val(JSON.stringify(polygons));
        layer.bindPopup(popupHtml);
        layer.addTo(map);
    }
    closeForm(false);
}

function deleteGeometry() {
    // Remove layer of geometry, remove geometry from form field value
    if (typeof(editLayer) == 'object') { map.removeLayer(editLayer); }
    if (typeof(editMarker) == 'object') { map.removeLayer(editMarker); }
    console.log(geometryType);
    if (geometryType == 'Point') {
        points = JSON.parse($('#gis_points').val());
        $.each(points, function (key, value) {
            if (value.properties.id == selectedGeometryId) {
                points.splice(key, 1);
                return false;
            }
        });
        $('#gis_points').val(JSON.stringify(points));
    }
    if (geometryType == 'Polygon') {
        polygons = JSON.parse($('#gis_polygons').val());
        $.each(polygons, function (key, value) {
            if (value.properties.id == selectedGeometryId) {
                polygons.splice(key, 1);
                return false;
            }
        });
        $('#gis_polygons').val(JSON.stringify(polygons)); // write array back to form field
    }
}

function editGeometry(selectedType, geometryType) {
    /*  Work in progress.
        This former code looks like the whole layer with form, popup, ... is deleted and
        reconstructed. Maybe there is a more efficient way to do that. */

    editIcon = L.icon({iconUrl: "/static/images/map/marker-icon_edit.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
    editedIcon = L.icon({iconUrl: "/static/images/map/marker-icon_edited.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
    newIcon = L.icon({iconUrl: "/static/images/map/images/marker-icon_new.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});

    map.addControl(inputForm);
    $('#inputFormTitle').text(shapeType.substr(0,1).toUpperCase() + shapeType.substr(1));
    $('#inputFormInfo').text(translate['map_info_' + shapeType]);
    $('#shapeName').val(shapeName);
    $('#shapeDescription').val(shapeDescription);
    $('.leaflet-right .leaflet-bar').hide();
    map.closePopup();

    if (geometryType === 'Point') {
        $('#resetButton').hide();
        newLayer = L.marker((editLayer.getLatLng()), {draggable: true, icon: editIcon}).addTo(map);
        wgs84 = newLayer.getLatLng();
        $('#northing').val(wgs84.lat);
        $('#easting').val(wgs84.lng);
        newLayer.bindPopup(
            '<div id="popup"><strong>' + objectName + '</strong><br/>' +
            '<div id="popup"><strong>' + shapeName + '</strong><br/>' +
            '<i>' + shapeType + '</i><br/><br/>' +
            '<div style="max-height:140px; overflow-y: auto">' + shapeDescription + '</div>'
        );
        newLayer.on('dragend', function (event) {
            newMarker = event.target;
            position = newMarker.getLatLng();
            $('#northing').val(position.lat);
            $('#easting').val(position.lng);
            $('#saveButton').prop('disabled', false);
        });
    }

    //$("#shapeform").on("input", function () {
    //    document.getElementById('editsavebtn').disabled = false;
    //});
    /*
    if (geometryType === 'Polygon') {
        newLayer = L.polygon(editLayer.getLatLngs()).addTo(map);
        newLayer.bindPopup(
            '<div id="popup"><strong>' + objectName + '</strong><br/>' +
            '<div id="popup"><strong>' + shapename + '</strong><br/>' +
            '<i>' + shapetype + '</i><br/><br/>' +
            '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '</div>'
            );
        map.removeLayer(editLayer);
        if (typeof (originLayer) == 'object') {
            map.removeLayer(originLayer);
        }
        originLayer = L.polygon(editLayer.getLatLngs());
        originLayer.bindPopup(
            '<div id="popup"><strong>' + objectName + '</strong><br/>' +
            '<div id="popup"><strong>' + shapename + '</strong><br/>' +
            '<i>' + shapetype + '</i><br/><br/>' +
            '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '</div>' +
            '<button onclick="editshape()"/>' + translate['edit'] + '</button> <button onclick="deleteshape()"/>' + translate['delete'] + '</button></div>'
            );
        map.removeLayer(editLayer);
    }


    newLayer.options.editing || (newlayer.options.editing = {});
    newLayer.editing.enable();
    document.getElementById('geometryType').value = geometryType;
    newLayer.on('edit', function () {
        var latLngs = newLayer.getLatLngs();
        var latLngs; // to store coordinates of vertices
        var newvector = []; // array to store coordinates as numbers
        geoJsonArray = [];
        var type = geometryType.toLowerCase();
        document.getElementById('editsavebtn').disabled = false;
        if (type != 'marker') {  // if other type than point then store array of coordinates as variable
            latLngs = mylayer.getLatLngs();
            for (i = 0; i < (latLngs.length); i++) {
                newvector.push(' ' + latLngs[i].lng + ' ' + latLngs[i].lat);
                geoJsonArray.push('[' + latLngs[i].lng + ',' + latLngs[i].lat + ']');
            }
            if (type === 'polygon') {
                // if polygon add first xy again as last xy to close polygon
                newvector.push(' ' + latLngs[0].lng + ' ' + latLngs[0].lat);
                shapesyntax = '(' + newvector + ')';
                geoJsonArray.push('[' + latLngs[0].lng + ',' + latLngs[0].lat + ']');
                returndata();

            }
            if (type === 'linestring') {
                shapesyntax = newvector;
                returndata();
            }
        }
        if (type === 'point') {
            latLngs = newLayer.getLatLng();
            newvector = (' ' + latLngs.lng + ' ' + latLngs.lat);
            shapesyntax = 'ST_GeomFromText(\'POINT(' + newvector + ')\',4326);'
            document.getElementById('northing').value = latLngs.lat;
            document.getElementById('easting').value = latLngs.lng;
        }
    });*/
}
