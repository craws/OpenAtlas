var map = L.map('map');

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var geoJsonLayer = new L.GeoJSON(gisPointAll, {onEachFeature: setPopup});
geoJsonLayer.addTo(map);

map.fitBounds(geoJsonLayer.getBounds(), {maxZoom: 12});

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