// Init map
map = L.map('map', {maxZoom: 18, fullscreenControl: true});

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
    polygonLayer = new L.GeoJSON(gisPolygonAll, {
        onEachFeature: setPopup,
        style: {color: '#9A9A9A'}
    });
    controls.Polygons = polygonLayer;
}

if (gisPointSelected != '') {
    gisPoints = L.geoJson(gisPointSelected, {onEachFeature: setPopup}).addTo(map);
    gisPoints.on('click', setObjectId);
}

if (gisPolygonSelected != '') {
    gisPolygons = L.geoJson(gisPolygonSelected, {onEachFeature: setPopup}).addTo(map);
    gisPolygons.on('click', setObjectId);
}

if (window.location.href.indexOf('update') >= 0) {
    $('#gis_points').val(JSON.stringify(gisPointSelected));
    $('#gis_polygons').val(JSON.stringify(gisPolygonSelected));
}


// Set zoom level depending on getbounds of selected points/polygons
if (gisPointSelected != '' && gisPolygonSelected != '') {
    map.fitBounds(L.featureGroup([gisPoints, gisPolygons]).getBounds(), {maxZoom: 12});
} else if (gisPointSelected != '') {
    map.fitBounds(gisPoints.getBounds(), {maxZoom: 12});
} else if (gisPolygonSelected != '') {
    map.fitBounds(gisPolygons.getBounds(), {maxZoom: 12});
} else if (gisPointAll != '') {
    map.fitBounds(pointLayer.getBounds(), {maxZoom: 12});
} else {
    map.setView([30, 340], 2);
}

L.control.layers(baseMaps, controls).addTo(map);
baseMaps.Landscape.addTo(map);

// Geoname search control init and add to map
geoSearchControl = L.control.geonames({
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
    } else if (!selected) {
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
