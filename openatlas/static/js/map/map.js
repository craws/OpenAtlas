// Init map variable using the #map div with options
var map = L.map('map', {
    fullscreenControl: true,
    drawControl: true
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
        selectedShape = feature.properties.id;
        editLayer = e.layer;
        editMarker = e.marker;
        shapeName = feature.properties.name;
        count = feature.properties.count;
        shapeType = feature.properties.shapeType;
        shapeDescription = feature.properties.description;
        objectName = feature.properties.title;
        helpText = translate['map_info_shape'];
        headingText = 'Shape';
        if (shapeType == "area") {
            helpText = translate['map_info_area'];
            headingText = 'Area';
        }
        if (geometryType == "Point") {
            helpText = translate['map_info_point'];
            headingText = 'Point';
        }
    }
}

function preventPopup(event) {
    if (editOn === 1) {
        map.closePopup();
    }
}

/**
 * Function to display a marker's popup on the map
 * @param feature - Markers object.
 * @param layer - Map layer to bind.
 * @param mode - 'display' for view only or 'update' for editing.
 */
function setPopup(feature, layer, mode='display') {
    var popupHTML = `
        <div id="popup">
            <strong>` + feature.properties.title + `</strong>
            <br />`+ feature.properties.siteType + `
            <br /><strong>` + feature.properties.name + `</strong>
            <div style="max-height:140px; overflow-y: auto;">` + feature.properties.description + `</div>` +
            feature.properties.shapeType;
    if (mode == 'update') {
        // While editing map content
        popupHTML += `
            <div id="buttonBar" style="white-space:nowrap;">
                <button id="editButton" onclick="editShape()"/>` + translate['edit'] + `</button>
                <button id="deleteButton" onclick="deleteShape()"/>` + translate['delete'] + `</button>
            </div>`;
    } else {
        // While only displaying map content
        popupHTML += '<p><a href="/place/view/' + feature.properties.objectId + '">' + translate['details'] + '</a></p>';
    }
    popupHTML += '</div>'
    layer.bindPopup(popupHTML);
}
