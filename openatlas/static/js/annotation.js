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
    console.log([page.width, page.height])
    // Get the bounds of the image and fit the map to those bounds
    const bounds = [
        [0, 0],  // Assuming the image starts from the top-left corner
        [page.width, page.height]  // Adjust if the coordinates are different
    ];
    map.fitBounds(bounds);
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
            const point = map.latLngToContainerPoint(latlng);
            return [
                point.x,
                point.y
            ];
        });
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
        color: 'blue',
        fillOpacity: 0.2
    }).addTo(map);

    // Extract the first 30 characters from the annotation text
    const truncatedText = annotation.annotation.substring(0, 30);

    // Add popup with truncated annotation text below the geometry
    geometry.bindPopup(`<p>${truncatedText}</p>`, {closeOnClick: false}).openPopup();
});
