// Init map
map = L.map('map', {maxZoom: mapMaxZoom, fullscreenControl: true});
L.control.scale().addTo(map);

// Icons
newIcon = L.icon({iconUrl: '/static/images/map/marker-icon_new.png', iconAnchor: [12, 41], popupAnchor: [0, -34]});
editIcon = L.icon({iconUrl: "/static/images/map/marker-icon_edit.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
editedIcon = L.icon({iconUrl: "/static/images/map/marker-icon_edited.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
grayMarker = L.icon({iconUrl: '/static/images/map/marker-icon-gray.png', iconAnchor: [12, 41], popupAnchor: [0, -34]});

// Define base layers
baseMaps = {
    Landscape: L.tileLayer('https://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=' + thunderforestKey, {attribution: '&copy; <a href="http://www.thunderforest.com">Thunderforest Landscape'}),
    OpenStreetMap: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
    GoogleSatellite: L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {subdomains: ['mt0', 'mt1', 'mt2', 'mt3'], attribution: '&copy; Google Maps'}),
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

if (gisLineAll) {
    linestringLayer = new L.GeoJSON(gisLineAll, {onEachFeature: setPopup, style: {color: '#9A9A9A'}});
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

if (gisLineSelected != '') {
    gisLines = L.geoJson(gisLineSelected, {onEachFeature: setPopup}).addTo(map);
    gisLines.on('click', setObjectId);
}

// Overlay maps
for (i=0; i < overlays.length; i++) {
    overlay = L.imageOverlay('/display/' + overlays[i].image, overlays[i].boundingBox)
    controls[overlays[i].name] = overlay;
    overlay.addTo(map)
}

if (window.location.href.indexOf('update') >= 0) {
    $('#gis_points').val(JSON.stringify(gisPointSelected));
    $('#gis_polygons').val(JSON.stringify(gisPolygonSelected));
    $('#gis_lines').val(JSON.stringify(gisLineSelected));
}

// Set zoom level depending on getBounds of selected points/polygons
let allSelected = [];
if (gisLineSelected != '') allSelected.push(gisLines);
if (gisPolygonSelected != '') allSelected.push(gisPolygons);
if (gisPointSelected != '') allSelected.push(gisPoints);
if (allSelected.length > 0) map.fitBounds(L.featureGroup(allSelected).getBounds(), {maxZoom: 12});
else if(gisPointAll.length > 0) map.fitBounds(pointLayer.getBounds(), {maxZoom: 12});
else map.setView([30, 0], 2);

L.control.layers(baseMaps, controls).addTo(map);
baseMaps.Landscape.addTo(map);

var geoSearchControl = L.control.geonames({
    // position: 'topcenter', // In addition to standard 4 corner Leaflet control layout, this will position and size from top center.
    position: 'topleft',
    geonamesSearch: 'https://secure.geonames.org/searchJSON', // Override this if using a proxy to get connection to geonames.
    geonamesPostalCodesSearch: 'https://secure.geonames.org/postalCodeSearchJSON', // Override this if using a proxy to get connection to geonames.
    username: geoNamesUsername, // Geonames account username.  Must be provided.
    maxresults: 8, // Maximum number of results to display per search.
    zoomLevel: 12, // Max zoom level to zoom to for location. If null, will use the map's max zoom level.
    className: 'leaflet-geonames-icon', // Class for icon.
    workingClass: 'leaflet-geonames-icon-working', // Class for search underway.
    featureClasses: ['A', 'H', 'L', 'P', 'R', 'T', 'U', 'V', 'S'], // Feature classes to search against.  See: http://www.geonames.org/export/codes.html.
    baseQuery: 'isNameRequired=true', // The core query sent to GeoNames, later combined with other parameters above.
    showMarker: false, // Show a marker at the location the selected location.
    showPopup: true, // Show a tooltip at the selected location.
    adminCodes: {}, // Filter results by the specified admin codes mentioned in `ADMIN_CODES`. Each code can be a string or a function returning a string. `country` can be a comma-separated list of countries.
    bbox: {}, // An object in form of {east:..., west:..., north:..., south:...}, specifying the bounding box to limit the results to.
    lang: 'en', // Locale of results.
    alwaysOpen: false, // If true, search field is always visible.
    enablePostalCodes: true, // If true, use postalCodesRegex to test user provided string for a postal code.  If matches, then search against postal codes API instead.
    postalCodesRegex: POSTALCODE_REGEX_US, // Regex used for testing user provided string for a postal code.  If this test fails, the default geonames API is used instead.
    title: translate['map_geonames_title'], // Search input title value.
    placeholder: translate['map_geonames_placeholder'] // Search input placeholder text.
});

geoSearchControl.on('select', function(e){
    if (geoNamesModule) {
        var popup = `<div>
                  <a href='https://www.geonames.org/${e.geoname.geonameId}' target='_blank'>${e.geoname.name}</a><br>
                  <div id="buttonBar" style="white-space:nowrap;">
                    <p>
                        <button id="ImportGeonamesID">Import ID</button>
                        <button id="ImportCoordinates">Import Coordinates</button><br><br>
                        <button id="ImportAll">Import ID and Coordinates</button>
                    </p>
                </div>
            </div>`;
        e.target._map.on('opengeopopup', p => {
            p.popup.setContent(popup);
            p.popup.update();
            $('#ImportCoordinates').click(() => importNewPoint(e.geoname, p.popup));
            $('#ImportGeonamesID').click(() => importGeonamesID(e.geoname, p.popup));
            $('#ImportAll').click(() => importAll(e.geoname, p.popup));
        });
    }
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
        popupHtml += '<strong>' + feature.properties.objectName + '</strong><br>';
        if (feature.properties.objectType) {
            popupHtml += '<i>' + feature.properties.objectType + '</i><br>'
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
                    <button id="editButton" onclick="editGeometry()">` + translate['edit'] + `</button>
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
    if (gisLineSelected) {
        for (lineSelected in gisLineSelected) {
            if (gisLineSelected[lineSelected].properties.objectId == feature.properties.objectId) {
                selected = true;
            }
        }
    }
    layer.bindPopup(buildPopup(feature, 'view', selected));
}
