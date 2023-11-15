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
    layer.bindPopup("Enter description: <input type='text' id='popup-description' />", {
        maxWidth: 300
    }).openPopup();

    // Add the drawn layer to the drawnItems FeatureGroup
    drawnItems.addLayer(layer);

    // Listen for the popupclose event to save description and coordinates
    layer.on('popupclose', function () {
        saveDescription(layer);
    });
});

// Function to save the entered description and coordinates
function saveDescription(layer) {
    let description = document.getElementById('popup-description').value;

    // Get the coordinates of the drawn shape
    let latlngs = layer.getLatLngs()[0].map(x => [x.lng, x.lat]);

    // Create a JSON object with description and coordinates
    let data = {
        description: description,
        coordinates: latlngs
    };

    // Store the JSON object in a variable or array
    // (You can extend this logic to save it to a database or elsewhere)

    jsonData.push(data);
    $('#annotation').val(JSON.stringify(data));

    // Log the JSON data for demonstration purposes
    console.log("JSON Data:", jsonData);
}