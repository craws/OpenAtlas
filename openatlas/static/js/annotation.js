map = L.map('annotate', {
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
let drawControl = new L.Control.Draw({
    draw: {
        polyline: false,
        circle: false,
        circlemarker: false,
        marker: false
    }
});
map.addControl(drawControl);


var jsonData = jsonData || [];
// Event Handling for Drawn Items
map.on(L.Draw.Event.CREATED, function (e) {
    let layer = e.layer;

    // Open a popup for the user to enter a description
    layer.bindPopup("Enter description: <input type='text' id='popup-description' /><br/><button onclick='saveDescription()'>Save</button>", {
        maxWidth: 300
    }).openPopup();

    // Add the drawn layer to the drawnItems FeatureGroup
    drawnItems.addLayer(layer);
});

function saveDescription() {
    let description = document.getElementById('popup-description').value;
    let latlngs = drawnItems.getLayers()[drawnItems.getLayers().length - 1].getLatLngs()[0].map(x => [x.lng, x.lat]);

    // Update the existing data object
    jsonData.push({
        description: description,
        coordinates: latlngs
    });

    $('#annotation').val(JSON.stringify(jsonData));
    // Log the JSON data for demonstration purposes
    console.log("JSON Data:", JSON.stringify(jsonData, null, 2));
    // Clear drawn items from the map
    drawnItems.clearLayers();

    // Close the popup
    map.closePopup();
}

