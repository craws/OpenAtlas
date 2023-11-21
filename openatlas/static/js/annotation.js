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


let drawnItems = new L.FeatureGroup();
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

// Function to update the #coordinate input field with the latest coordinates
function updateCoordinatesInput() {
    if (drawnItems.getLayers().length > 0) {
        const precision = 2; // Specify the number of decimal places

        let coordinates = drawnItems.getLayers()[0].getLatLngs()[0].map(x => [
            x.lng.toFixed(precision),
            x.lat.toFixed(precision)
        ]);

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

// To remove the last drawn geometry
function removeLastDrawnGeometry() {
    const lastGeometry = drawnGeometries.pop();
    if (lastGeometry) {
        drawnItems.removeLayer(lastGeometry);
    }
}

// Event handler for when a geometry is deleted
map.on('draw:deleted', function (event) {
    // Clear drawn geometries and update the input field with the remaining coordinates
    clearDrawnGeometries();
    updateCoordinatesInput();
});

// Function to transform coordinates from 'x,y,x,y,...' to Leaflet LatLng array
function transformCoordinates(coordinates) {
    const latLngArray = coordinates.split(',').map((coord, index) => {
        return index % 2 === 0 ? parseFloat(coord) : parseFloat(coord);
    });

    return latLngArray.reduce((result, value, index, array) => {
        if (index % 2 === 0) {
            result.push([array[index + 1], value]); // Swap the order of latitude and longitude
        }
        return result;
    }, []);
}

// Iterate through annotations and add them to the map
annotations.forEach(annotation => {
    const coordinates = transformCoordinates(annotation.coordinates);
    const geometry = L.polygon(coordinates, {
        color: 'blue', // You can customize the style here
        fillOpacity: 0.5
    }).addTo(map);

    // Add popup with annotation text
    geometry.bindPopup(annotation.annotation);
});
