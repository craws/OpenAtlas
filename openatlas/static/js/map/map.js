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

var controls = {}
if (gisPointAll) {
    var pointLayer = new L.GeoJSON(gisPointAll, {
        onEachFeature: setPopup,
        pointToLayer: function(feature, latlng) {
            return L.marker(latlng, {icon: grayMarker});
        }
    });
    controls.Points = pointLayer;
}

if (gisPolygonAll) {
    var polygonLayer = new L.GeoJSON(gisPolygonAll, {onEachFeature: setPopup});
    controls.Polygons = polygonLayer;
}

if (gisPointSelected != '') {
    // View for a single place, set geoJson layer for all points
    var gisPoints = L.geoJson(gisPointSelected, {onEachFeature: setPopup}).addTo(map);
    gisPoints.on('click', setObjectId);
    setTimeout(function () {
        map.fitBounds(gisPoints.getBounds(), {maxZoom: 12});
    }, 1);
}

if (gisPolygonSelected != '') {
    var gisPoints = L.geoJson(gisPointSelected, {onEachFeature: setPopup}).addTo(map);
    gisPoints.on('click', setObjectId);
    var gisSites = L.geoJson(gisPolygonSelected, {onEachFeature: setPopup}).addTo(map);
    gisSites.on('click', setObjectId);
    var gisExtend = L.featureGroup([gisPoints, gisSites]);
    setTimeout(function () {
        map.fitBounds(gisExtend.getBounds(), {maxZoom: 12});
    }, 1);
}

if (window.location.href.indexOf('update') >= 0) {
    $('#gis_points').val(JSON.stringify(gisPointSelected));
    $('#gis_polygons').val(JSON.stringify(gisPolygonSelected));
}

// Add markers to the map
map.addLayer(pointLayer);
map.fitBounds(pointLayer.getBounds(), {maxZoom: 12});
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
    layer = e.layer;
    editLayer = e.layer;
    feature = layer.feature;
    console.log(feature);
    console.log(feature.properties.geometryType);
    editMarker = e.marker;
    //if (shapeType == 'point') {
    //    position = (e.latlng);
    //}
}

function buildPopup(feature, action='view', selected=False) {
    console.log(action);
    popupHtml = `
        <div id="popup">
            <strong>` + feature.properties.objectName + `</strong>
            <br /><strong>` + feature.properties.geometryName + `</strong>
            <div style="max-height:140px;overflow-y:auto">` + feature.properties.geometryDescription + `</div>
            <i>` + feature.properties.geometryType + `</i>`
    if (action == 'edit') {
        popupHtml += '<p><i>' + translate['map_info_reedit'] + '</i></p>';
    }
    // Add detail link if not selected
    if (!selected) {
        popupHtml += '<p><a href="/place/view/' + feature.properties.objectId + '">' + translate['details'] + '</a></p>';
    }
    // Add edit and delete button if selected and in update mode
    if (action == 'edit') {
        popupHtml += `
            <div id="buttonBar" style="white-space:nowrap;">
                <p>
                    <button id="editButton" onclick="editGeometry()"/>` + translate['edit'] + `</button>
                    <button id="deleteButton" onclick="deleteGeometry()"/>` + translate['delete'] + `</button>
                </p>
            </div>`;
    }
    popupHtml += '</div>';
    return popupHtml;
}


/**
 * Function to display a marker's popup on the map
 * @param feature - Markers object.
 * @param layer - Map layer to bind.
 */
function setPopup(feature, layer, mode) {
    selected = false;
    // Check if this feature is selected
    if (gisPointSelected) {
        for (pointSelected in gisPointSelected) {
            if (gisPointSelected[pointSelected].properties.objectId == feature.properties.objectId) {
                selected = true;
            }
        }
    }
    layer.bindPopup(buildPopup(feature, 'view', selected));
}
