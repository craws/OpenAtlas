// Init map variable using the #map div with options
var map = L.map('map', {
    fullscreenControl: true
});

var grayMarker = L.icon({iconUrl: '/static/images/map/marker-icon-gray.png'});

// Define base layers
var baseMaps = {
    Landscape: L.tileLayer('https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=' + thunderforestKey, {attribution: '&copy; <a href="http://www.thunderforest.com">Thunderforest Landscape '}),
    OpenStreetMap: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
    GoogleSatellite: L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {subdomains: ['mt0', 'mt1', 'mt2', 'mt3'], attribution: '&copy; Google Maps '}),
};


if (gisPointSelected == "") {
    // Define and add geo JSON layer for markers for all places index
    var pointLayer = new L.GeoJSON(gisPointAll, {
        onEachFeature: setPopup,
        pointToLayer: function(feature, latlng) {
            return L.marker(latlng, {icon: grayMarker});
        }
    });
} else {
    // View for a single place entity
    // Set geo json layer for all points
    var pointLayer = new L.GeoJSON(gisPointAll, {
        onEachFeature: setPopup,
        pointToLayer: function(feature, latlng) {
            return L.marker(latlng, {icon: grayMarker});
        }
    });
    // If it's not a polygon
    if (gisPolygonSelected == "") {
        var gisPoints = L.geoJson(gisPointSelected, {onEachFeature: setPopup}).addTo(map);
        gisPoints.on('click', setObjectId);
        setTimeout(function () {
            map.fitBounds(gisPoints.getBounds(), {maxZoom: 12});
        }, 1);
    } else {
        // If it's a polygon
        var gisPoints = L.geoJson(gisPointSelected, {onEachFeature: setPopup}).addTo(map);
        gisPoints.on('click', setObjectId);
        var gisSites = L.geoJson(gisPolygonSelected, {onEachFeature: setPopup}).addTo(map);
        gisSites.on('click', setObjectId);
        var gisExtend = L.featureGroup([gisPoints, gisSites]);
        setTimeout(function () {
            map.fitBounds(gisExtend.getBounds(), {maxZoom: 12});
        }, 1);
    }
}

// Add markers to the map
map.addLayer(pointLayer);
map.fitBounds(pointLayer.getBounds(), {maxZoom: 12});

var controls = {
    Sites: pointLayer,
}

L.control.layers(baseMaps, controls).addTo(map);
baseMaps.Landscape.addTo(map);

// Geoname search control init and add to map
var geoSearchControl = L.control.geonames({
    username: geoNamesUsername, // Geonames account username.  Must be provided
    zoomLevel: 12, // Max zoom level to zoom to for location.  If null, will use the map's max zoom level.
    maxresults: 8, // Maximum number of results to display per search
    className: 'fa fa-globe', // class for icon
    workingClass: 'fa-spin', // class for search underway
});
map.addControl(geoSearchControl);

function setObjectId(e) {
    preventPopup();
    if (editOn === 0) {
        var layer = e.layer;
        var feature = layer.feature;
        var objectId = feature.properties.objectId;
        geometryType = feature.geometry.type;
        if (geometryType == 'Point') {
            position = (e.latlng);
        }
        selectedshape = feature.properties.id;
        editlayer = e.layer;
        editmarker = e.marker;
        shapename = feature.properties.name;
        count = feature.properties.count;
        shapetype = feature.properties.shapeType;
        shapedescription = feature.properties.description;
        objectName = feature.properties.title;
        helptext = translate['map_info_shape'];
        headingtext = 'Shape';
        if (shapetype == "area") {
            helptext = translate['map_info_area'];
            headingtext = 'Area';
        }
        if (geometryType == "Point") {
            helptext = translate['map_info_point'];
            headingtext = 'Point';
        }
    }
}

function preventPopup(event) {
    if (editOn === 1) {
        map.closePopup();
    }
}

/**
 * Interactions with the map
 */

// Init variables
var coordCapture;
var coordCaptureImg;


/**
 * Custom map functions
 */

/**
 * Function to display a marker's popup on the map
 * @param feature - Markers object.
 * @param layer - Map layer to bind.
 * @param mode - 'display' for view only or 'update' for editing.
 */
function setPopup(feature, layer, mode='display') {
    // Base popup HTML content
    var popupHTML =
        '<div id="popup"><strong>' + feature.properties.title + '</strong><br/>' +
        '<div id="popup"><i>' + feature.properties.siteType + '</i><br/>' +
        '<div id="popup"><strong>' + feature.properties.name + '</strong><br/>' +
        '<div style="max-height:140px; overflow-y: auto;">' + feature.properties.description + '<br/></div>' +
        '<i>' + feature.properties.shapeType + '</i><br/><br/>';
    // While editing map content
    if (mode == 'update') {
        popupHTML +=
          '<div id="btnBar" style="white-space:nowrap;">' +
          '<button id="editBtn" onclick="editshape()"/>' + translate['edit'] + '</button> <button id="delBtn" onclick="deleteshape()"/>' + translate['delete'] + '</button></div>' +
          '</div>';
    } else {
        // While only displaying map content
        popupHTML +=
          '<a href="/place/view/' + feature.properties.objectId + '">' + translate['details'] + '</a>';
    }
    // Bind to layer
    layer.bindPopup(popupHTML);
}

/*
/**
 * Function to set interactions off
 */
function interactionOff() {
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

/**
 * Function to set interactions on
 */
function interactionOn() {
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
    if (coordCapture) {
        document.getElementById('map').style.cursor = 'crosshair';
        capture = true;
    }
    if (coordCaptureImg) {
        document.getElementById('map').style.cursor = 'crosshair';
    }
}

/**
 * Function to toggle interactions between on and off
 * @param element - Interaction element.
 */
function interactionToggle(element) { // disable map dragging when cursor is e.g. in search input field.
    $(element).hover(function () {
        interactionOn();
    }, function () {
        interactionOff();
    });
}
