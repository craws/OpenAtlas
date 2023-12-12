map = L.map('annotate', {
    crs: L.CRS.Simple,
    zoom: 0,
});

let baseLayer;
let drawnItems = new L.FeatureGroup();

$.getJSON(iiif_manifest, function (data) {
    const page = data.sequences[0].canvases[0];
    baseLayer = L.tileLayer.iiif(
        page.images[0].resource.service['@id'] + '/info.json',
        {
            continuousWorld: false,
            fitBounds: true,  // Set fitBounds to true for automatic fitting
            setMaxBounds: true,
            tileSize: 256
        }
    ).addTo(map);

    // Get the bounds of the image and fit the map to those bounds
    const bounds = [
        [0, 0],  // Assuming the image starts from the top-left corner
        [page.width, page.height]  // Adjust if the coordinates are different
    ];
    map.fitBounds(bounds);
    // Iterate through annotations and add them to the map
    $.getJSON(page.otherContent[0]['@id'], function(annoData) {
        $.each(annoData.resources, function(i, value) {
            const b = /xywh=(.*)/.exec(value.on.selector.value)[1].split(',');
            const minPoint = L.point(parseInt(b[0]), parseInt(b[1]));
            const maxPoint = L.point(parseInt(b[0]) + parseInt(b[2]), parseInt(b[1]) + parseInt(b[3]));
            const min = map.unproject(minPoint, 5);
            const max = map.unproject(maxPoint, 5);
            L.rectangle(L.latLngBounds(min, max)).bindPopup(value.resource[0].chars).addTo(map);
        });
    });
});

map.addLayer(drawnItems);

let drawnGeometries = []; // Array to store drawn geometries

let drawControl = new L.Control.Draw({
    draw: {
        polyline: false,
        circle: false,
        circlemarker: false,
        marker: false,
        polygon: {
            allowIntersection: false
        }
    },
    edit: {
        featureGroup: drawnItems
    }
});
map.addControl(drawControl);

map.on('draw:created', function (event) {
    // Clear drawn geometries and add the new one
    clearDrawnGeometries();
    drawnItems.addLayer(event.layer);
    drawnGeometries.push(event.layer);

    // Update the input field with the coordinates
    updateCoordinatesInput();
});

// Event handler for when a geometry is edited
map.on('draw:edited', function (event) {
    // Update the input field with the coordinates after editing
    updateCoordinatesInput();
});

// Function to update the #coordinate input field with the latest pixel coordinates
function updateCoordinatesInput() {
    if (drawnItems.getLayers().length > 0) {
        let coordinates = drawnItems.getLayers()[0].getLatLngs()[0].map(latlng => {
            // Convert each LatLng to pixel coordinates
            const point = map.project(latlng, 5);
            return [
                point.x,
                point.y
            ];
        });
        console.log("converted" ,coordinates, "bounds", map.getPixelOrigin());
        $('#coordinate').val(coordinates);
    } else {
        $('#coordinate').val('');
    }
}


// To remove all drawn geometries
function clearDrawnGeometries() {
    drawnItems.clearLayers();
    drawnGeometries = [];
}



// Event handler for when a geometry is deleted
map.on('draw:deleted', function (event) {
    // Clear drawn geometries and update the input field with the remaining coordinates
    clearDrawnGeometries();
    updateCoordinatesInput();
});


