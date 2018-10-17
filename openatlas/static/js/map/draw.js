// Todo: try to remove most of these global variables
var objectName; // Name of the entry at update of an existing entry

// Variables for a selected geometry
var geometryName;
var geometryDescription;
var geometryType; // centerpoint, shape or area

var captureCoordinates = false; // Boolean if clicks on map should be captured as coordinates
var marker = false; // Temporary marker for point coordinate
var geoJsonArray = []; // Polygon coordinates storage
var drawnPolygon = L.featureGroup();
var layer;
var newLayer = false;
var editedLayer = false;

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
pointButton.intendedFunction = function () {drawGeometry('centerpoint');}
map.addControl(pointButton);

/* Input form */
var inputForm = L.control();
inputForm.onAdd = function (map) {
    div = L.DomUtil.create('div', 'mapFormDiv');
    div.innerHTML = `
        <form id="geometryForm" onmouseover="interactionOff()" onmouseout="interactionOn()">
            <input type="hidden" id="geometryParent" value="NULL" />
            <input type="hidden" id="geometryCoordinates" />
            <span id="inputFormTitle"></span>
            <span id="closeButton" title="` + translate["map_info_close"] + `" onclick="closeForm()" class="fa">X</span>
            <p id="inputFormInfo"></p>
            <div id="nameField" style="display: block">
                <input type="text" id="geometryName" placeholder="Enter a name if desired" />
            </div>
            <textarea rows="3" cols="70" id="geometryDescription" placeholder="` + translate["map_info_description"] + `"/></textarea>
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
            <div style="clear:both;"></div>
            <input type="button" id="saveButton" disabled value="` + translate["save"] + `" onclick="saveForm()" />
        </form>`;
    return div;
};

map.on('click', function(e) {
    if (captureCoordinates && geometryType == 'centerpoint') {
        $('#saveButton').prop('disabled', false);
        console.log(marker)
        if (marker) {  // Marker already exists so move it
            console.log('here');
            console.log(marker);
            marker.setLatLng(e.latlng);
            marker.on('dragend', function (event) {
                var marker = event.target;
                position = marker.getLatLng();
                $('#northing').val(position.lat);
                $('#easting').val(position.lng);
            });
        } else {  // No marker exists so create it
            var marker = new L.marker(e.latlng, {draggable: true, icon: newIcon});
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
    } else if (captureCoordinates) {
        $('#saveButton').prop('disabled', false);
    }
});

map.on('draw:created', function (e) {
    drawnPolygon.addLayer(e.layer);
    layer = e.layer;
    if (geometryType == 'centerpoint') {
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
        $('#geometryCoordinates').val('(' + vector + ')');
    }
    $('#saveButton').prop('disabled', false);
});

function closeForm(withoutSave = true) {
    inputForm.remove(map);
    $('.leaflet-right .leaflet-bar').show();
    interactionOn();
    $('#map').css('cursor', '');
    if (geometryType != 'centerpoint' && withoutSave) {
        drawnPolygon.removeLayer(layer);
        drawLayer.disable();
    }
    if (marker) {
        map.removeLayer(marker);
    }
    captureCoordinates = false; // Important that this is the last statement
}

function drawGeometry(selectedType) {
    geometryType = selectedType;
    map.addControl(inputForm);
    if (selectedType == 'centerpoint') {
        $('#coordinatesDiv').show();
    } else {
        captureCoordinates = false;
        drawLayer = new L.Draw.Polygon(map);
        map.addLayer(drawnPolygon);
        drawLayer.enable();
        $('#coordinatesDiv').hide();
    }
    $('#inputFormTitle').text(selectedType.substr(0,1).toUpperCase() + selectedType.substr(1));
    $('#inputFormInfo').text(translate['map_info_' + selectedType]);
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

function saveForm() {
    geometryName = $('#geometryName').val().replace(/\"/g,'\\"');
    geometryDescription = $('#geometryDescription').val().replace(/\"/g,'\\"');
    if (typeof newLayer == 'object') {
        saveEditedGeometry();
        newLayer.remove(map);
        newLayer = false;
    } else {
        saveNewGeometry();
    }
}

function saveEditedGeometry() {
    geometryCoordinates = $('#geometryCoordinates').val();
    if (feature.properties.geometryType == 'centerpoint') {
        // Remove former point
        points = JSON.parse($('#gis_points').val());
        $.each(points, function (key, value) {
            if (value.properties.id == feature.properties.id) {
                points.splice(key, 1);
                return false;
            }
        });
        // Add new point
        point =
            `{"type": "Feature", "geometry":` +
            `{"type": "Point", "coordinates": [` + $('#easting').val() + `,` + $('#northing').val() + `]},` +
            `"properties":{"geometryName": "` + geometryName + `", "geometryDescription": "` + geometryDescription + `", "geometryType": "centerpoint"}}`;
        points.push(JSON.parse(point));
        $('#gis_points').val(JSON.stringify(points));
        editedLayer = L.marker(newLayer.getLatLng(), {icon: editedIcon}).addTo(map);
        editedLayer.bindPopup(buildPopup(JSON.parse(point), 'edited'));
    }
    closeForm(false);

    /*if (geometrytype == 'Polygon') {
        var myeditedlayer = L.polygon(mylayer.getLatLngs()).addTo(map);
        myeditedlayer.setStyle({fillColor: '#686868'});
        myeditedlayer.setStyle({color: '#686868'});
    }*/
    /*if (geometrytype == 'Polygon') {
        var polygons = JSON.parse($('#gis_polygons').val());
        $.each(polygons, function (key, value) {
            var id = (JSON.stringify(value.properties.id));
            var index = ((JSON.stringify(key)));
            if (id == selectedshape) {
                old_coordinates = value['geometry']['coordinates'];
                polygons.splice(index, 1);
                return false;
            }
        });
        $('#gis_polygons').val(JSON.stringify(polygons));
        coordinates = '[[' + geoJsonArray.join(',') + ']]'
        if (geoJsonArray.length < 1) {
            coordinates = JSON.stringify(old_coordinates);
        }
        var polygon = '{"type":"Feature","geometry":{"type":"Polygon","coordinates":' + coordinates + '},"properties":';
        polygon += '{"name": "' + $('#geometryName').val().replace(/\"/g,'\\"') + '","description": "' + $('#geometryDescription').val().replace(/\"/g,'\\"') + '", "geometryType": "' + geometryType + '"}}';
        var polygons = JSON.parse($('#gis_polygons').val());
        polygons.push(JSON.parse(polygon));
        $('#gis_polygons').val(JSON.stringify(polygons));
    }*/
}

function saveNewGeometry() {
    if (geometryType == 'centerpoint') {
        point =
            `{"type": "Feature", "geometry":` +
            `{"type": "Point", "coordinates": [` + $('#easting').val() + `,` + $('#northing').val() + `]},` +
            `"properties":{"geometryName": "` + geometryName + `", "geometryDescription": "` + geometryDescription + `", "geometryType": "centerpoint"}}`;
        points = JSON.parse($('#gis_points').val());
        points.push(JSON.parse(point));
        $('#gis_points').val(JSON.stringify(points));
        newMarker = L.marker(([$('#northing').val(), $('#easting').val()]), {icon: editedIcon}).addTo(map);
        newMarker.bindPopup(buildPopup(JSON.parse(point), 'edited'));
        marker = false;  // unset the marker
    } else {
        coordinates = $('#geometryCoordinates').val();
        polygon =
            `{"type": "Feature", "geometry":` +
            `{"type": "Polygon", "coordinates":[[` + geoJsonArray.join(',') + `]]},
            "properties":{"geometryName": "` + geometryName + `", "geometryDescription": "` + geometryDescription + `", "geometryType": "` + geometryType + `"}}`;
        polygons = JSON.parse($('#gis_polygons').val());
        polygons.push(JSON.parse(polygon));
        $('#gis_polygons').val(JSON.stringify(polygons));
        layer.bindPopup(buildPopup(JSON.parse(polygon), 'edited'));
        layer.addTo(map);
    }
    closeForm(false);
}

function deleteGeometry() {
    // Remove layer of geometry, remove geometry from form field value
    if (typeof(editLayer) == 'object') { map.removeLayer(editLayer); }
    if (typeof(editMarker) == 'object') { map.removeLayer(editMarker); }
    if (feature.properties.geometryType == 'centerpoint') {
        points = JSON.parse($('#gis_points').val());
        $.each(points, function (key, value) {
            if (value.properties.id == feature.properties.id) {
                points.splice(key, 1);
                return false;
            }
        });
        $('#gis_points').val(JSON.stringify(points));
    } else {
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

function editGeometry() {
    map.closePopup();
    map.addControl(inputForm);
    $('#inputFormTitle').text(feature.properties.geometryType.substr(0,1).toUpperCase() + feature.properties.geometryType.substr(1));
    $('#inputFormInfo').text(translate['map_info_' + feature.properties.geometryType]);
    $('#geometryName').val(feature.properties.geometryName);
    $('#geometryDescription').val(feature.properties.geometryDescription);
    $('.leaflet-right .leaflet-bar').hide();
    if (feature.properties.geometryType == 'centerpoint') {
        newLayer = L.marker(editLayer.getLatLng(), {draggable: true, icon: editIcon}).addTo(map);
        wgs84 = newLayer.getLatLng();
        $('#northing').val(wgs84.lat);
        $('#easting').val(wgs84.lng);
        newLayer.bindPopup(feature, 'edit');
        newLayer.on('dragend', function (event) {
            newMarker = event.target;
            position = newMarker.getLatLng();
            $('#northing').val(position.lat);
            $('#easting').val(position.lng);
            $('#saveButton').prop('disabled', false);
        });
        layer.remove(marker);
    } else {
        $('#coordinatesDiv').hide();
        newLayer = L.polygon(editLayer.getLatLngs()).addTo(map);

        // Workaround for Leaflet draw bug: https://github.com/Leaflet/Leaflet.draw/issues/804
        newLayer.options.editing || (newLayer.options.editing = {});

        newLayer.editing.enable();
        newLayer.bindPopup(feature, 'edit');
        newLayer.on('edit', function () {
            $('#saveButton').prop('disabled', false);

            /*var latLngs = mylayer.getLatLngs();
            var latLngs; // to store coordinates of vertices
            var newvector = []; // array to store coordinates as numbers
            geoJsonArray = [];
            var type = geometrytype.toLowerCase();
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
                latLngs = mylayer.getLatLng();
                newvector = (' ' + latLngs.lng + ' ' + latLngs.lat);
                shapesyntax = 'ST_GeomFromText(\'POINT(' + newvector + ')\',4326);'
                document.getElementById('northing').value = latLngs.lat;
                document.getElementById('easting').value = latLngs.lng;
            };*/
        })
        map.removeLayer(editLayer);
    }

}
