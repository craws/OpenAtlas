var map = L.map('annotate', {
    center: [0, 0],
    crs: L.CRS.Simple,
    zoom: 1,
    tileSize: 128
});

let baseLayer;
$.getJSON(iiif_manifest, function (data) {
    const page = data.sequences[0].canvases[0];
    baseLayer = L.tileLayer.iiif(
        page.images[0].resource.service['@id'] + '/info.json',
        {
            tileSize: 128
        }
    ).addTo(map);
});

// Initialise the FeatureGroup to store editable layers
let drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw({
    draw: {
        polyline: false,
        circle: false,
        circlemarker: false
    },
    edit: {
        featureGroup: drawnItems
    }
});

map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (e) {
    var type = e.layerType
    var layer = e.layer;

    // Do whatever else you need to. (save to db, add to map etc)

    drawnItems.addLayer(layer);
});


var popup = L.popup([0, 1], {content: '<p>Hello world!<br />This is a nice popup.</p>'}).openOn(map);
