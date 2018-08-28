var marker; // temporary marker for coordinate capture
var capture = false; // var to store whether control is active or not
var coordinateCapture;
var coordinateCaptureImage;
var objectName = '';
var drawnPolygon = L.featureGroup();
var newIcon = L.icon({iconUrl: '/static/images/map/marker-icon_new.png', iconAnchor: [12, 41], popupAnchor: [0, -34]});
var shapeType;  // centerpoint, shape or area
var geoJsonArray = [];  // used to store shape coordinates

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
polygonButton.intendedFunction =
    function () {
        shapeType = 'shape';
        drawPolygon();
    }
map.addControl(polygonButton);

var areaButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-circle-o-notch',
    title: translate['map_info_area']
})
areaButton.intendedFunction =
    function () {
        shapeType = 'area';
        inputFormInfo = translate['map_info_area'];
        drawPolygon();
    }
map.addControl(areaButton);

var pointButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-map-marker',
    title: translate['map_info_point']
})
pointButton.intendedFunction =
    function () {
        shapeType = 'centerpoint';
        capture = true;
        coordinatesCapture = true;
        drawMarker();
    }
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
                <input type="hidden" id="geometryType" />
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
            </form>
            <input type="button" title="Reset values and shape" id="resetButton" disabled value="` + translate["map_clear"] + `" onclick="resetForm()" />
            <input type="button" title="` + translate["save"] + `" id="saveButton" disabled value="` + translate["save"] + `" onclick="saveForm()" />
         </div>`;
    return div;
};

map.on('click', function(e) {
    if (capture) {
        $('#saveButton').prop('disabled', false);
        $('#geometryType').val('point');
        if (typeof(marker) !== 'object') {
            marker = new L.marker(e.latlng, {draggable: true, icon: newIcon});
            marker.addTo(map);
            var wgs84 = (marker.getLatLng());
            $('#northing').val(wgs84.lat);
            $('#easting').val(wgs84.lng);
        } else {
            marker.setLatLng(e.latlng);
            marker.on('dragend', function (event) {
                var marker = event.target;
                position = marker.getLatLng();
                $('#northing').val(position.lat);
                $('#easting').val(position.lng);
            });
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
    if (geometryType === 'marker') {
        coordinates = layer.getLatLng();
        vector = (' ' + coordinates.lng + ' ' + coordinates.lat);
        shapeSyntax = 'ST_GeomFromText(\'POINT(' + vector + ')\',4326);'
    } else {  // if other not point store array of coordinates as variable
        coordinates = layer.getLatLngs();
        for (i = 0; i < (coordinates.length); i++) {
            vector.push(' ' + coordinates[i].lng + ' ' + coordinates[i].lat);
            geoJsonArray.push('[' + coordinates[i].lng + ',' + coordinates[i].lat + ']');
        }
        if (geometryType === 'polygon') {
            alert(coordinates);
            // If polygon add first xy again as last xy to close polygon
            vector.push(' ' + coordinates[0].lng + ' ' + coordinates[0].lat);
            geoJsonArray.push('[' + coordinates[0].lng + ',' + coordinates[0].lat + ']');
            $('#shapeCoordinates').val('(' + vector + ')');
            alert(geoJsonArray);
        }
    }
});

function closeForm() {
    inputForm.remove(map);
    $('.leaflet-right .leaflet-bar').show();
    interactionOn();
    capture = false;
    coordinateCapture = false;
    $('#map').css('cursor', '');
    if (shapeType != 'centerpoint') {
        drawnPolygon.removeLayer(layer);
        drawLayer.disable();
    }
    if (marker) {
        map.removeLayer(marker);
    }
}


function drawMarker() {
    $('#map').css('cursor', 'crosshair');
    map.addControl(inputForm);
    $('#inputFormTitle').text('Point');
    $('#inputFormInfo').text(translate['map_info_point']);
    $('.leaflet-right .leaflet-bar').hide();
    $('#resetButton').hide();
    $('#coordinatesDiv').show();
}


function drawPolygon() {
    drawLayer = new L.Draw.Polygon(map);
    $('.leaflet-right .leaflet-bar').hide();
    geometryType = 'polygon';
    capture = false;
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
    capture = true;
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
    capture = false;
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
    var popup = `
            <div id="popup"><strong>` + objectName + `</strong></div></br />
            <div id="popup"><strong>` + name + `</strong></div></br />
            <i>Centerpoint</i><br /><br />
            <div style="max-height:140px;overflow-y:auto">` + description + `<br /><br /><br /></div>
            <i>` + translate['map_info_reedit'] + `</i>`
    if (shapeType == 'centerpoint') {
        var point = '{"type": "Feature","geometry": {"type": "Point","coordinates": [' + $('#easting').val() + ',' + $('#northing').val() + ']},"properties":';
        point += '{"name": "' + name + '","description": "' + description + '", "shapeType": "centerpoint"}}';
        var points = JSON.parse($('#gis_points').val());
        points.push(JSON.parse(point));
        $('#gis_points').val(JSON.stringify(points));
        var newMarker = L.marker(([$('#northing').val(), $('#easting').val()]), {icon: newIcon}).addTo(map);
        newMarker.bindPopup(popup);
    } else {
        var coordinates = $('#shapeCoordinates').val();
        var geometryType = $('#geometryType').val();
        var dataString = '&shapename=' + name + '&shapetype=' + shapeType + '&shapedescription=' + description + '&shapeCoordinates=' + coordinates + '&geometryType=' + geometryType;
        $('#gisData').val($('#gisData').val() + dataString);
        var polygon = '{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[' + geoJsonArray.join(',') + ']]},"properties":';
        polygon += '{"name": "' + name + '","description": "' + description + '", "shapeType": "' + shapeType + '"}}';
        var polygons = JSON.parse($('#gis_polygons').val());
        polygons.push(JSON.parse(polygon));
        $('#gis_polygons').val(JSON.stringify(polygons));
        layer.bindPopup(popup);
        layer.addTo(map);
    }
    closeForm();
}
