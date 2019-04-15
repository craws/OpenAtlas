// Init map
map = L.map('map', {maxZoom: 18, fullscreenControl: true});

L.control.scale().addTo(map);

// Icons
newIcon = L.icon({iconUrl: '/static/images/map/marker-icon_new.png', iconAnchor: [12, 41], popupAnchor: [0, -34]});
editIcon = L.icon({iconUrl: "/static/images/map/marker-icon_edit.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
editedIcon = L.icon({iconUrl: "/static/images/map/marker-icon_edited.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
grayMarker = L.icon({iconUrl: '/static/images/map/marker-icon-gray.png', iconAnchor: [12, 41], popupAnchor: [0, -34]});

// Define base layers
baseMaps = {
    Landscape: L.tileLayer('https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=' + thunderforestKey, {attribution: '&copy; <a href="http://www.thunderforest.com">Thunderforest Landscape '}),
    OpenStreetMap: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
    GoogleSatellite: L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {subdomains: ['mt0', 'mt1', 'mt2', 'mt3'], attribution: '&copy; Google Maps '}),
};

cluster = L.markerClusterGroup({
    showCoverageOnHover: false,
    maxClusterRadius: maxClusterRadius,
    disableClusteringAtZoom: disableClusteringAtZoom
});

controls = {}
if (gisPointAll) {
    pointLayer = new L.GeoJSON(gisPointAll, {
        onEachFeature: setPopup,
        pointToLayer: function(feature, latlng) {
            if (window.location.pathname == '/place') {
                return L.marker(latlng);
            }
            return L.marker(latlng, {icon: grayMarker});
        }
    });
}

if (useCluster) {
    cluster.addLayer(pointLayer);
    map.addLayer(cluster);
    controls.Points = cluster;
} else {
    map.addLayer(pointLayer);
    controls.Points = pointLayer;
}

if (gisPolygonAll) {
    polygonLayer = new L.GeoJSON(gisPolygonAll, {onEachFeature: setPopup, style: {color: '#9A9A9A'}});
    controls.Polygons = polygonLayer;
}

if (gisLinestringAll) {
    linestringLayer = new L.GeoJSON(gisLinestringAll, {onEachFeature: setPopup, style: {color: '#9A9A9A'}});
    controls.Linestrings = linestringLayer;
}

if (gisPointSelected != '') {
    gisPoints = L.geoJson(gisPointSelected, {onEachFeature: setPopup}).addTo(map);
    gisPoints.on('click', setObjectId);
}

if (gisPolygonSelected != '') {
    gisPolygons = L.geoJson(gisPolygonSelected, {onEachFeature: setPopup}).addTo(map);
    gisPolygons.on('click', setObjectId);
}

if (gisLinestringSelected != '') {
    gisLinestrings = L.geoJson(gisLinestringSelected, {onEachFeature: setPopup}).addTo(map);
    gisLinestrings.on('click', setObjectId);
}

// Workaround overlay maps for Stefan until #978 is implemented
if (overlayHack) {
    controls.Stara = L.imageOverlay('/display/112757.png', [[49.99800, 14.99246], [49.99747, 14.99328]]);
    controls.Thunau = L.imageOverlay('/display/112760.png', [[48.58709, 15.64294], [48.58653, 15.64356]]);
    map.options.maxZoom = 30;
}

if (window.location.href.indexOf('update') >= 0) {
    $('#gis_points').val(JSON.stringify(gisPointSelected));
    $('#gis_polygons').val(JSON.stringify(gisPolygonSelected));
    $('#gis_linestrings').val(JSON.stringify(gisLinestringSelected));
}

// Set zoom level depending on getbounds of selected points/polygons
let allSelected = [];
if (gisLinestringSelected != '') allSelected.push(gisLinestrings);
if (gisPolygonSelected != '') allSelected.push(gisPolygons);
if (gisPointSelected != '') allSelected.push(gisPoints);
if (allSelected.length > 0) map.fitBounds(L.featureGroup(allSelected).getBounds(), {maxZoom: 12});
else if(gisPointAll) map.fitBounds(pointLayer.getBounds(), {maxZoom: 12});
else map.setView([30, 340], 2);

L.control.layers(baseMaps, controls).addTo(map);
baseMaps.Landscape.addTo(map);

// Geoname search control init and add to map
geoSearchControl = L.control.geonames({
    username: geoNamesUsername, // Geonames account username.  Must be provided
    zoomLevel: 12, // Max zoom level to zoom to for location.  If null, will use the map's max zoom level.
    maxresults: 8, // Maximum number of results to display per search
    className: 'fa-globe-europe fas', // class for icon
    //workingClass: 'fa-globe-europe fas', // class for search underway
});
map.addControl(geoSearchControl);

function setObjectId(e) {
    layer = e.layer;
    editLayer = e.layer;
    feature = layer.feature;
    editMarker = e.marker;
}

function buildPopup(feature, action='view', selected=false) {
    popupHtml = '<div id="popup">'
    if (feature.properties.objectName) {
        popupHtml += '<strong>' + feature.properties.objectName + '</strong><br />';
        if (feature.properties.objectType) {
            popupHtml += '<i>' + feature.properties.objectType + '</i><br />'
        }
    }
    popupHtml += `
        <strong>` + feature.properties.name + `</strong>
        <div style="max-height:140px;overflow-y:auto">` + feature.properties.description + `</div>`
    if (action == 'edited') {
        popupHtml += '<p><i>' + translate['map_info_reedit'] + '</i></p>';
    } else if (!selected || window.location.href.indexOf('place') < 1) {
        popupHtml += '<p><a href="/place/view/' + feature.properties.objectId + '">' + translate['details'] + '</a></p>';
    } else if (window.location.href.indexOf('update') >= 0) {
        popupHtml += `
            <div id="buttonBar" style="white-space:nowrap;">
                <p>
                    <button id="editButton" onclick="editGeometry('` + feature.properties.geometryType + `')">` + translate['edit'] + `</button>
                    <button id="deleteButton" onclick="deleteGeometry()">` + translate['delete'] + `</button>
                </p>
            </div>`;
    }
    return popupHtml + '</div>';
}

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
    if (gisPolygonSelected) {
        for (polygonSelected in gisPolygonSelected) {
            if (gisPolygonSelected[polygonSelected].properties.objectId == feature.properties.objectId) {
                selected = true;
            }
        }
    }
    layer.bindPopup(buildPopup(feature, 'view', selected));
}
