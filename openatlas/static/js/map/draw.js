var marker; // temporary marker for coordinate capture
var capture = false; // var to store whether control is active or not
var coordinateCapture;
var coordinateCaptureImage;
var objectName = '';
var drawnPolygone = L.featureGroup();
var newIcon = L.icon({iconUrl: "/static/images/map/marker-icon_new.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});


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

var polygonButton = new L.Control.EasyButtons;
polygonButton.options.position = 'topright';
polygonButton.options.intentedIcon = 'fa-pencil-square-o';
polygonButton.options.title = translate['map_info_shape'];
polygonButton.intendedFunction =
    function () {
        shapeType = "shape";
        helpText = translate['map_info_shape'];
        headingText = 'Shape';
        drawPolygon();
    }
map.addControl(polygonButton);

var areaButton = new L.Control.EasyButtons;
areaButton.options.position = 'topright';
areaButton.options.intentedIcon = 'fa-circle-o-notch';
areaButton.options.title = translate['map_info_area'];
areaButton.intendedFunction =
    function () {
        shapeType = "area";
        helpText = translate['map_info_area'];
        headingText = 'Area';
        drawPolygon();
    }
map.addControl(areaButton);

var pointButton = new L.Control.EasyButtons;
pointButton.options.position = 'topright';
pointButton.options.intentedIcon = 'fa-map-marker';
pointButton.options.title = translate['map_info_point'];
pointButton.intendedFunction =
    function () {
        shapeType = "centerpoint";
        helpText = translate['map_info_point'];
        headingText = 'Point';
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
                <input type="hidden" id="shapeType" value="NULL" />
                <input type="hidden" id="shapeCoordinates" />
                <input type="hidden" id="geometryType" />
                <span id="headingText"></span>
                <span id="closeButton" title="` + translate["map_info_close"] + `" onclick="closeMyFormX()" class="fa">X</span>
                <span id="editCloseButton" title="` + translate["map_info_close"] + `" onclick="editCloseMyForm()" class="fa">X</span>
                <span id="markerCloseButton" title="` + translate["map_info_close"] + `" onclick="closeMarkerFormX()" class="fa">X</span>
                <p id="p1"></p>
                <div id="nameField" style="display: block">
                    <input type="text" id="shapeName" placeholder="Enter a name if desired" />
                </div>
                <textarea rows="3" cols="70" id="shapeDescription" placeholder="` + translate["map_info_description"] + `"/></textarea>
                <div style="display:block;clear:both;">
                    <label for='easting'>Easting</label>
                    <input type="text" style="margin-top:0.5em;" oninput="check_coordinates_input()" id="easting" placeholder="decimal degrees" />
                </div>
                <div style="display:block;clear:both;">
                    <label for='northing'>Northing</label>
                    <input type="text" style="margin-top:0.5em;" oninput="check_coordinates_input()" id="northing" placeholder="decimal degrees" />
                </div>
            </form>
            <input type="button" title="Reset values and shape" id="resetButton" disabled value="` + translate["map_clear"] + `" onclick="resetMyForm()"/>
            <input type="button" title="Save shape" id="saveButton" disabled value="` + translate["save"] + `" onclick="saveToDb()"/>
            <input type="button" title="Save edits" id="editSaveButton" disabled value="` + translate["save"] + `" onclick="editSaveToDb()"/>
            <input type="button" title="Save marker" id="markerSaveButton" disabled value="` + translate["save"] + `" onclick="saveMarker()"/>
         </div>`;
    return div;
};

function drawMarker() {
    $('#map').css('cursor', 'crosshair');
    map.addControl(inputForm);
    $('.leaflet-right .leaflet-bar').hide();
    // resetMyForm();
    document.getElementById("p1").innerHTML = helpText;
    document.getElementById("headingText").innerHTML = headingText;
    document.getElementById('saveButton').style.display = 'none';
    document.getElementById('resetButton').style.display = 'none';
    document.getElementById('closeButton').style.display = 'none';
    document.getElementById('markerCloseButton').style.display = 'block';
    document.getElementById('markerSaveButton').style.display = 'block';
    document.getElementById('easting').style.display = 'block';
    document.getElementById('northing').style.display = 'block';
}

function drawPolygon() {
    drawLayer = new L.Draw.Polygon(map);
    $('.leaflet-right .leaflet-bar').hide();
    geometryType = "polygon";
    capture = false;
    map.addControl(inputForm);
    // resetMyForm();
    map.addLayer(drawnPolygone);
    drawLayer.enable();
    $("#shapeForm").on("input", function () {
        document.getElementById('resetButton').disabled = false;
    });
}

function closeMarkerFormX() {
    inputForm.remove(map);
    if (marker) {
        map.removeLayer(marker);
    }
    $('.leaflet-right .leaflet-bar').show();
    coordinateCapture = false;
    capture = false;
    interactionOn();
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
    $('#map').css('cursor', '');
    if (coordinateCapture) {
        document.getElementById('map').style.cursor = 'crosshair';
        capture = true;
    }
    if (coordinateCaptureImage) {
        document.getElementById('map').style.cursor = 'crosshair';
    }
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

map.on('click', function(e) {
    if (capture) {
        document.getElementById('markerSaveButton').disabled = false;
        document.getElementById('geometryType').value = 'point';
        if (typeof(marker) !== 'object') {
            marker = new L.marker(e.latlng, {draggable: true, icon: newIcon});
            marker.addTo(map);
            var wgs84 = (marker.getLatLng());
            document.getElementById('northing').value = wgs84.lat;
            document.getElementById('easting').value = wgs84.lng;
        } else {
            marker.setLatLng(e.latlng);
            marker.on('dragend', function (event) {
                var marker = event.target;
                position = marker.getLatLng();
                document.getElementById('northing').value = position.lat;
                document.getElementById('easting').value = position.lng;
            });
        }
        var wgs84 = marker.getLatLng();
        marker.on('dragend', function (event) {
            var marker = event.target;
            position = marker.getLatLng();
            document.getElementById('northing').value = position.lat;
            document.getElementById('easting').value = position.lng;
        });
        document.getElementById('northing').value = wgs84.lat;
        document.getElementById('easting').value = wgs84.lng;
    }
});

function saveMarker() {
    capture = false;
    document.getElementById('saveButton').style.display = 'none';
    var point = '{"type": "Feature","geometry": {"type": "Point","coordinates": [' + $('#easting').val() + ',' + $('#northing').val() + ']},"properties":';
    point += '{"name": "' + $('#shapeName').val().replace(/\"/g,'\\"') + '","description": "' + $('#shapeDescription').val().replace(/\"/g,'\\"') + '", "shapeType": "centerpoint"}}';
    var points = JSON.parse($('#gis_points').val());
    points.push(JSON.parse(point));
    $('#gis_points').val(JSON.stringify(points));
    var newMarker = L.marker(([$('#northing').val(), $('#easting').val()]), {icon: newIcon}).addTo(map);
    newMarker.bindPopup(`
        <div id="popup"><strong>` + objectName + `</strong></div></br />
        <div id="popup"><strong>` + $('#shapeName').val() + `</strong></div></br />
        <i>Centerpoint</i><br /><br />
        <div style="max-height:140px;overflow-y:auto">` + $('#shapeDescription').val() + `<br /><br /><br /></div>
        <i>` + translate['map_info_reedit'] + `</i>`
    );
    closeMarkerForm();
}

function closeMarkerForm() {
    inputForm.remove(map);
    $('.leaflet-right .leaflet-bar').show();
    map.removeLayer(marker);
    coordinateCapture = false;
    capture = false;
    interactionOn();
}



