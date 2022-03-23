let drawnItems = L.featureGroup();
let editedShapes = {};
let currentEditLayer = undefined;
let currentDrawLayer = undefined;
let deleteIdList = [];
let drawLayerIsArea = false;
map.addLayer(drawnItems);
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
        L.DomUtil.create('i', this.options.intentedIcon, this.link);
    }
});

pointButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-map-marker-alt fa',
    title: translate['map_info_centerpoint']
})
pointButton.intendedFunction = () => drawGeometry('point');
map.addControl(pointButton);

polylineButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-project-diagram fa',
    title: translate['map_info_linestring']
})
polylineButton.intendedFunction = () => drawGeometry('polyline');
map.addControl(polylineButton);

polygonButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-vector-square fa',
    title: translate['map_info_shape']
})
polygonButton.intendedFunction = () => drawGeometry('shape');
map.addControl(polygonButton);

areaButton = new L.Control.EasyButtons({
    position: 'topright',
    intentedIcon: 'fa-draw-polygon fa',
    title: translate['map_info_area']
})
areaButton.intendedFunction = () => drawGeometry('area');
map.addControl(areaButton);

let mapInputForm = L.control();
mapInputForm.onAdd = () => {
    let div = L.DomUtil.create('div');
    div.innerHTML = `
    <div class="mapFormDiv" onmouseover="interactionOff()" onmouseout="interactionOn()">
            <span id="closeButton" title="${translate["map_info_close"]}" onclick="closeForm()" class="fad">X</span>
            <span id="inputFormTitle"></span>
            <p id="inputFormInfo"></p>
            <input type="text" id="nameField" placeholder="Enter a name if desired">
            <textarea rows="3" cols="70" id="descriptionField" placeholder="${translate["map_info_description"]}"/></textarea>
            <div id="coordinatesDiv">
            <div class="markerInput">
                <label for='easting'>Easting</label>
                <input type="text" oninput="check_coordinates_input_marker()" id="easting" placeholder="decimal degrees">
            </div>
            <div class="markerInput">
                <label for='northing'>Northing</label>
                <input type="text" oninput="check_coordinates_input_marker()" id="northing" placeholder="decimal degrees">
            </div>
            <div class="polygonInput">
                <label for='polyInput'>Points</label>
                <input type="text" oninput="check_coordinates_input_polygon()" id="polyInput"  placeholder="[[lon1,lat1],[lon2,lat2],...]">
            </div>
        </div>
        </div>
    `;
    return div;
}

map.on(L.Draw.Event.CREATED, function (e) {
    const name = $('#nameField')?.val();
    const description = $('#descriptionField')?.val();
    let geometry = [];
    let shapeType = "";
    currentEditLayer = e.layer;
    switch (e.layerType.toLowerCase()) {
        case 'marker':
            geometry = { type: 'Point', coordinates: [currentEditLayer.getLatLng().lng, currentEditLayer.getLatLng().lat] };
            shapeType = 'centerpoint';
            $('#easting').val(currentEditLayer.getLatLng().lng)
            $('#northing').val(currentEditLayer.getLatLng().lat)
            $("#coordinatesDiv input").removeClass('error');
            break;
        case 'polyline':
            geometry = { type: 'Linestring', coordinates: currentEditLayer.getLatLngs().map(x => [x.lng, x.lat]) };
            shapeType = 'polyline';
            $('#polyInput').val(JSON.stringify(geometry.coordinates));
            break;
        case 'polygon':
            geometry = { type: 'Polygon', coordinates: [currentEditLayer.getLatLngs()[0].map(x => [x.lng, x.lat])] };
            // Add first xy again as last xy to close polygon
            geometry.coordinates = [[...geometry.coordinates[0], geometry.coordinates[0][0]]]
            $('#polyInput').val(JSON.stringify(geometry.coordinates[0]));


            shapeType = drawLayerIsArea ? 'area' : 'shape';
            break;

    }
    currentEditLayer.feature = {
        type: "Feature",
        geometry: geometry,
        properties: { name: name, description: description, id: Date.now() * -1, shapeType: shapeType }
    }
    currentEditLayer.bindPopup(buildPopup(currentEditLayer.feature, 'view', true));
    currentDrawLayer = undefined;
    drawnItems.addLayer(currentEditLayer);
});

function editGeometry(featureId) {
    saveCurrentEditLayer();
    let tempLayer = Object.values(selectedLayer._layers).find(x => x.feature.properties.id === featureId) ||
        Object.values(drawnItems._layers).find(x => x?.feature?.properties?.id === featureId);

    openForm(tempLayer.feature.properties.shapeType, tempLayer.feature);

    switch (tempLayer.feature.properties.shapeType.toLowerCase()) {
        case "centerpoint": case "point":
            currentEditLayer = L.marker(tempLayer.getLatLng(), { draggable: true, icon: editIcon }).addTo(map);
            $('#easting').val(tempLayer.getLatLng().lng)
            $('#northing').val(tempLayer.getLatLng().lat)

            break;
        case "polyline": case "linestring":
            currentEditLayer = L.polyline(tempLayer.getLatLngs()).addTo(map);
            currentEditLayer.options.editing || (currentEditLayer.options.editing = {});
            $('#polyInput').val(JSON.stringify(tempLayer.feature.geometry.coordinates));
            break;
        default:
            currentEditLayer = L.polygon(tempLayer.getLatLngs()).addTo(map);
            $('#polyInput').val(JSON.stringify(tempLayer.feature.geometry.coordinates[0]));

    }
    $("#coordinatesDiv input").removeClass('error');
    currentEditLayer.options.editing || (currentEditLayer.options.editing = {});
    currentEditLayer.editing.enable();
    currentEditLayer.feature = tempLayer.feature;
    map.closePopup();
    currentEditLayer.bindPopup(buildPopup(tempLayer.feature, 'view', true));
    drawnItems.removeLayer(tempLayer);
    selectedLayer.removeLayer(tempLayer);
}

function deleteGeometry(featureId) {
    closeForm();
    saveCurrentEditLayer();
    let tempLayer = Object.values(selectedLayer._layers).find(x => x.feature.properties.id === featureId) ||
        Object.values(drawnItems._layers).find(x => x?.feature?.properties?.id === featureId);
    tempLayer.remove();
    deleteIdList.push(featureId);
}

function drawGeometry(shapeType) {
    openForm(shapeType);
    drawLayerIsArea = false;
    switch (shapeType.toLowerCase()) {
        case 'point':
            currentDrawLayer = new L.Draw.Marker(map);
            break;
        case 'polyline':
            currentDrawLayer = new L.Draw.Polyline(map);
            break;
        case 'area':
            drawLayerIsArea = true;
            currentDrawLayer = new L.Draw.Polygon(map, { allowIntersection: false, test: 'hoi' });
            break;
        case 'shape':
            currentDrawLayer = new L.Draw.Polygon(map, { allowIntersection: false, test: 'hoi' });
            break;
    }
    currentDrawLayer.enable();
}
function openForm(shapeType, feature = undefined) {
    if (shapeType === 'polyline') shapeType = 'linestring'
    if (shapeType === 'point') shapeType = 'centerpoint'

    map.addControl(mapInputForm);
    $('.leaflet-right .leaflet-bar').hide();

    if (shapeType == 'centerpoint') { $('.markerInput').show(); $('.polygonInput').hide(); }
    else { $('.markerInput').hide(); $('.polygonInput').show(); }

    $('#inputFormTitle').text(shapeType);
    $('#inputFormInfo').text(translate[`map_info_${shapeType}`]);
    $('#nameField').val(feature?.properties?.name || '');
    $('#descriptionField').val(feature?.properties?.description || '');


}
function closeForm(withoutSave = true) {
    interactionOn();
    currentDrawLayer?.disable();
    saveCurrentEditLayer();

    mapInputForm.remove(map);
    $('.leaflet-right .leaflet-bar').show();
}

function saveCurrentEditLayer() {
    const name = $('#nameField').val();
    const description = $('#descriptionField').val();
    let geometry = [];
    let shapeType = "";
    if (currentEditLayer) {
        switch (currentEditLayer?.feature?.properties?.shapeType.toLowerCase()) {
            case 'marker': case 'point': case 'centerpoint':
                geometry = { type: 'Point', coordinates: [currentEditLayer.getLatLng().lng, currentEditLayer.getLatLng().lat] };
                shapeType = "centerpoint";
                break;
            case 'polyline': case 'linestring':
                geometry = { type: 'Linestring', coordinates: currentEditLayer.getLatLngs().map(x => [x.lng, x.lat]) };
                shapeType = "polyline";
                break;
            case 'polygon': case 'area': case 'shape':
                geometry = { type: 'Polygon', coordinates: [currentEditLayer.getLatLngs()[0].map(x => [x.lng, x.lat])] };
                // Add first xy again as last xy to close polygon
                geometry.coordinates = [[...geometry.coordinates[0], geometry.coordinates[0][0]]]

                shapeType = currentEditLayer?.feature?.properties?.shapeType;
                break;

        }
        currentEditLayer.feature = {
            ...currentEditLayer.feature,
            geometry: geometry,
            properties: { ...currentEditLayer.feature.properties, name: name, description: description, shapeType: shapeType },

        }
        currentEditLayer.editing.disable();
        currentEditLayer.bindPopup(buildPopup(currentEditLayer.feature, 'view', true));

        drawnItems.addLayer(currentEditLayer);
        currentEditLayer = undefined;
    }

}

function updateHiddenInputFields() {
    saveCurrentEditLayer();
    const drawnItemsFeatures = Object.values(drawnItems?._layers).map(x => x.feature);
    const drawnItemsFeaturesIds = drawnItemsFeatures.map(x => x.properties.id);
    const removeIdList = [...drawnItemsFeaturesIds, ...deleteIdList];
    const allGisElements = [...gisSelected.filter(x => !removeIdList.includes(x.properties.id)),
    ...drawnItemsFeatures.filter(x => !deleteIdList.includes(x.properties.id))];

    $('#gis_points').val(JSON.stringify(allGisElements.filter(x => x.geometry.type.toLowerCase() === 'point')));
    $('#gis_lines').val(JSON.stringify(allGisElements.filter(x => x.geometry.type.toLowerCase() === 'linestring')));
    $('#gis_polygons').val(JSON.stringify(allGisElements.filter(x => x.geometry.type.toLowerCase() === 'polygon')));
}

function importGeonamesID(geo, popup) {
    $('.GeoNames').val(geo.geonameId);
    popup._close();
}

function importNewPoint(geo, popup) {
    saveCurrentEditLayer();
    popup._close();
    point =
    {
        type: "Feature",
        geometry: { type: "Point", coordinates: [geo.lng, geo.lat] },
        properties: { name: geo.name, description: `${geo.name} (${geo.geonameId}), imported from GeoNames`, shapeType: "centerpoint" }
    };
    openForm("centerpoint", point);
    currentEditLayer = L.marker([geo.lat, geo.lng], { draggable: true, icon: editIcon }).addTo(map);
    currentEditLayer.editing.enable();
    currentEditLayer.feature = point;
    currentEditLayer.bindPopup(buildPopup(point, 'view', true));
}

function importAll(geo, popup) {
    importGeonamesID(geo, popup);
    importNewPoint(geo, popup);
}
$(document).ready(function () {
    $('#save,#insert_and_continue,#insert_continue_sub').on('click', function () { // I think this should be click event because you're not submitting your page you're just clearing it based on "CLEAR"
        updateHiddenInputFields();
    });
});

function check_coordinates_input_marker() {
    var floatRegex = /^-?\d+(?:[.,]\d*?)?$/;
    let lng = $('#easting').val().replace(",", ".")
    let lat = $('#northing').val().replace(",", ".")

    if (!floatRegex.test(lng)) $("#easting").addClass('error');
    else $("#easting").removeClass('error');
    if (!floatRegex.test(lat)) $("#northing").addClass('error');
    else $("#northing").removeClass('error');
    if (!floatRegex.test(lng) || !floatRegex.test(lat)) return false;
    currentEditLayer.feature.geometry.coordinates = [parseFloat(lng), parseFloat(lat)]
    var newLatLng = new L.LatLng(parseFloat(lat), parseFloat(lng));
    currentEditLayer.setLatLng(newLatLng);
    if (!map.getBounds().contains(newLatLng)) map.panTo(newLatLng);
    return floatRegex.test(lng) && floatRegex.test(lat);
}

function check_coordinates_input_polygon() {
    var floatRegex = /^-?\d+(?:[.,]\d*?)?$/;
    currentEditLayer.editing.disable();

    const validateInput = (input) => {
        let points = [];
        try {
            points = JSON.parse(input)
        } catch { return false }

        if (!Array.isArray(points)) return false;
        if (points.some(x => !Array.isArray(x) || x.length !== 2)) return false;
        if (points.some(x => x.some(y => !floatRegex.test(y)))) return false;
        return true
    }
    if (!validateInput($('#polyInput').val())) {
        $('#polyInput').addClass('error');
        return false;
    }
    $('#polyInput').removeClass('error');
    const points = JSON.parse($('#polyInput').val());

    const latLngs = points.map(x => new L.LatLng(x[1], x[0]));
    currentEditLayer.setLatLngs(latLngs);
}

map.on('draw:editvertex', function () {
    const newCoordinates = currentEditLayer.feature.geometry.type === 'Polygon' ?
        currentEditLayer.getLatLngs()[0].map(x => [x.lng, x.lat]) :
        currentEditLayer.getLatLngs().map(x => [x.lng, x.lat]);
    $('#polyInput').val(JSON.stringify(newCoordinates))
    $("#coordinatesDiv input").removeClass('error');

});
map.on('draw:editmove', function () {
    $('#easting').val(currentEditLayer.getLatLng().lng)
    $('#northing').val(currentEditLayer.getLatLng().lat)
    $("#coordinatesDiv input").removeClass('error');
});

map.on('keyup', (event) => {
    if (event.originalEvent.key === 'Escape' )
        closeForm();
});
function interactionOn() {
    // Enable interaction with map e.g. if cursor leaves form
    if(currentDrawLayer?.type === 'marker')
        currentDrawLayer.enable();
    captureCoordinates = true;
    map.dragging.enable();
    map.touchZoom.enable();
    map.doubleClickZoom.enable();
    map.scrollWheelZoom.enable();
    map.boxZoom.enable();
    map.keyboard.enable();
    if (map.tap) {
        map.tap.enable();
    }
}

function interactionOff() {
    if(currentDrawLayer?.type === 'marker')
        currentDrawLayer.disable();
    // Disable interaction with map e.g. if cursor is over a form
    captureCoordinates = false;
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
