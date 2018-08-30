var shapeType; // centerpoint, shape or area
var geometryType; // point or polygon
var captureCoordinates = false; // boolean if clicks on map should be captured as coordinates
var marker = false; // temporary marker for point coordinate
var geoJsonArray = []; // polygon coordinates storage
var objectName = ''; // name of the entry at update of an existing entry
var drawnPolygon = L.featureGroup();
var newIcon = L.icon({iconUrl: '/static/images/map/marker-icon_new.png', iconAnchor: [12, 41], popupAnchor: [0, -34]});

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
polygonButton.intendedFunction = function() {drawPolygon('shape');}
map.addControl(polygonButton);

var areaButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-circle-o-notch',
    title: translate['map_info_area']
})
areaButton.intendedFunction = function() {drawPolygon('area');}
map.addControl(areaButton);

var pointButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-map-marker',
    title: translate['map_info_point']
})
pointButton.intendedFunction = function () {drawMarker();}
map.addControl(pointButton);

/* Input form */
var inputForm = L.control();
inputForm.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'shapeInput');
    div.innerHTML += `
        <div id="insertForm" style="display:block">
            <form id="shapeForm" onmouseover="interactionOff()" onmouseout="interactionOn()">
                <input type="hidden" id="shapeParent" value="NULL" />
                <input type="hidden" id="shapeCoordinates" />
                <span id="inputFormTitle"></span>
                <span id="closeButton" title="` + translate["map_info_close"] + `" onclick="closeForm('` + shapeType + `')" class="fa">X</span>
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
    if (captureCoordinates && shapeType == 'centerpoint') {
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
            var wgs84 = (marker.getLatLng());
            $('#northing').val(wgs84.lat);
            $('#easting').val(wgs84.lng);
        }
        var wgs84 = marker.getLatLng();
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
    $('#saveButton').prop('disabled', false);
    $('#resetButton').prop('disabled', false);
    drawnPolygon.addLayer(e.layer);
    geometryType = e.layerType;
    layer = e.layer;
    var coordinates;
    var vector = []; // Array to store coordinates as numbers
    geoJsonArray = [];
    if (geometryType == 'point') {
        coordinates = layer.getLatLng();
        vector = (' ' + coordinates.lng + ' ' + coordinates.lat);
        shapeSyntax = 'ST_GeomFromText(\'POINT(' + vector + ')\',4326);'
    } else {  // if other not point store array of coordinates as variable
        coordinates = layer.getLatLngs()[0];
        for (i = 0; i < (coordinates.length); i++) {
            vector.push(' ' + coordinates[i].lng + ' ' + coordinates[i].lat);
            geoJsonArray.push('[' + coordinates[i].lng + ',' + coordinates[i].lat + ']');
        }
        // If polygon add first xy again as last xy to close polygon
        vector.push(' ' + coordinates[0].lng + ' ' + coordinates[0].lat);
        geoJsonArray.push('[' + coordinates[0].lng + ',' + coordinates[0].lat + ']');
        $('#shapeCoordinates').val('(' + vector + ')');
    }
});

function closeForm() {
    inputForm.remove(map);
    $('.leaflet-right .leaflet-bar').show();
    interactionOn();
    $('#map').css('cursor', '');
    if (shapeType != 'centerpoint') {
        drawnPolygon.removeLayer(layer);
        drawLayer.disable();
    }
    if (marker) {
        map.removeLayer(marker);
    }
    captureCoordinates = false; // Important that this is the last statement
}

function drawMarker() {
    shapeType = 'centerpoint';
    geometryType = 'point'
    $('#map').css('cursor', 'crosshair');
    map.addControl(inputForm);
    $('#inputFormTitle').text('Point');
    $('#inputFormInfo').text(translate['map_info_point']);
    $('.leaflet-right .leaflet-bar').hide();
    $('#resetButton').hide();
    $('#coordinatesDiv').show();
}

function drawPolygon(selectedType) {
    shapeType = selectedType;
    geometryType = 'polygon';
    captureCoordinates = false;
    drawLayer = new L.Draw.Polygon(map);
    $('.leaflet-right .leaflet-bar').hide();
    map.addControl(inputForm);
    map.addLayer(drawnPolygon);
    drawLayer.enable();
    $('#inputFormTitle').text(shapeType=='area' ? 'Area' : 'Shape');
    $('#inputFormInfo').text(translate['map_info_' + shapeType]);
    $('#shapeForm').on('input', function () {
        $('#resetButton').prop('disabled', false);
    });
    $('#coordinatesDiv').hide();
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
    var name = $('#shapeName').val().replace(/\"/g,'\\"');
    var description = $('#shapeDescription').val().replace(/\"/g,'\\"');
    popupHtml = `
        <div id="popup">
            <strong>` + objectName + `</strong>
            <br />` + shapeType + `
            <br /><strong>` + name + `</strong>
            <div style="max-height:140px;overflow-y:auto">` + description + `</div>
            <i>` + translate['map_info_reedit'] + `</i>
        </div>`;
    if (shapeType == 'centerpoint') {
        var point = '{"type": "Feature","geometry": {"type": "Point","coordinates": [' + $('#easting').val() + ',' + $('#northing').val() + ']},"properties":';
        point += '{"name": "' + name + '","description": "' + description + '", "shapeType": "centerpoint"}}';
        var points = JSON.parse($('#gis_points').val());
        points.push(JSON.parse(point));
        $('#gis_points').val(JSON.stringify(points));
        var newMarker = L.marker(([$('#northing').val(), $('#easting').val()]), {icon: newIcon}).addTo(map);
        newMarker.bindPopup(popupHtml);
        marker = false;  // unset the marker
    } else {
        var coordinates = $('#shapeCoordinates').val();
        var dataString = '&shapename=' + name + '&shapetype=' + shapeType + '&shapedescription=' + description + '&shapeCoordinates=' + coordinates + '&geometryType=' + geometryType;
        $('#gisData').val($('#gisData').val() + dataString);
        var polygon = '{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[' + geoJsonArray.join(',') + ']]},"properties":';
        polygon += '{"name": "' + name + '","description": "' + description + '", "shapeType": "' + shapeType + '"}}';
        var polygons = JSON.parse($('#gis_polygons').val());
        polygons.push(JSON.parse(polygon));
        $('#gis_polygons').val(JSON.stringify(polygons));
        layer.bindPopup(popupHtml);
        layer.addTo(map);
    }
    closeForm();
}
