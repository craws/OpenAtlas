/**
 * @file 
 * OpenAtlas' map init and options
 *
 * Asil Çetin
 */

// Init map variable using the #map div with options
var map = L.map('map', {
    fullscreenControl: true
});

// Define base map layers
var baseMaps = {
    OpenStreetMap: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
    GoogleSatellite: L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {subdomains: ['mt0', 'mt1', 'mt2', 'mt3'], attribution: '&copy; Google Maps '}),
};

// Default base map init
baseMaps.OpenStreetMap.addTo(map);

// Add map layers control
L.control.layers(baseMaps).addTo(map);

// Define and add geo json layer for markers
var geoJsonLayer = new L.GeoJSON(gisPointAll, {onEachFeature: setPopup});
geoJsonLayer.addTo(map);
map.fitBounds(geoJsonLayer.getBounds(), {maxZoom: 12});

// Geoname search control init and add to map
var geoSearchControl = L.control.geonames({
    username: geoNamesUsername, // Geonames account username.  Must be provided
    zoomLevel: 12, // Max zoom level to zoom to for location.  If null, will use the map's max zoom level.
    maxresults: 8, // Maximum number of results to display per search
    className: 'fa fa-globe', // class for icon
    workingClass: 'fa-spin', // class for search underway
});
map.addControl(geoSearchControl);

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
 * Function to display a marker's popop on the map
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