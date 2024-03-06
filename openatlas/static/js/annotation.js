map = L.map('annotate', {
  crs: L.CRS.Simple
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
      tileSize: 128
    }
  ).addTo(map);

  const bounds = [
    [0, 0],
    [page.width, page.height]
  ];
  map.fitBounds(bounds);
  // Iterate through annotations and add them to the map
  $.getJSON(page.otherContent[0]['@id'], function (annoData) {
    const scaleFactor = baseLayer.x / baseLayer._imageSizes[map.getZoom()].x;
    $.each(annoData.resources, function (i, value) {
      // Extract coordinates from the SVG tag
      const pathCoordinates = new DOMParser().parseFromString(value.on.selector.item.value, "image/svg+xml")
        .querySelector('path').getAttribute('d').match(/(\d+\.\d+|\d+)/g);
      const coordinates = [];
      // Divide coordinates into pairs an unproject them to fit it on the image
      for (let j = 0; j < pathCoordinates.length; j += 2) {
        let lat = parseInt(pathCoordinates[j]) / scaleFactor;
        let lng = parseInt(pathCoordinates[j + 1]) / scaleFactor;
        coordinates.push(map.unproject([lat, lng], map.getZoom()));
      }
      L.polygon(coordinates).bindPopup(constructPopupText(value.resource)).addTo(map);
    });
  });
});
function constructPopupText(resource) {
  let content = '';
  resource.forEach(function(item) {
    if (item["@type"] === "dctypes:Dataset") {
      content += '<p>' + item.chars + '</p>';
    } else if (item["@type"] === "dctypes:Text") {
      content += '<p>' + item.chars + '</p>';
    }
  });
  return content;
}

map.addLayer(drawnItems);

let drawnGeometries = []; // Array to store drawn geometries

let drawControl = new L.Control.Draw({
  draw: {
    polyline: false,
    circle: false,
    circlemarker: false,
    marker: false,
    polygon: true
  },
  edit: {
    featureGroup: drawnItems
  }
});
map.addControl(drawControl);

map.on('draw:created', function (event) {
  clearDrawnGeometries();
  drawnItems.addLayer(event.layer);
  drawnGeometries.push(event.layer);
  updateCoordinatesInput(event);
});

map.on('draw:edited', function (event) {
  updateCoordinatesInput(event);
});

function updateCoordinatesInput(event) {
  const mapinstance = event.target;
  const scaleFactor = baseLayer.x / baseLayer._imageSizes[mapinstance.getZoom()].x;
  if (drawnItems.getLayers().length > 0) {
    let coordinates = drawnItems.getLayers()[0].getLatLngs()[0].map(latlng => {
      // Convert each LatLng to pixel coordinates
      const point = mapinstance.project(latlng, mapinstance.getZoom());
      return [
        Math.trunc(point.x * scaleFactor),
        Math.trunc(point.y * scaleFactor)
      ];
    });
    $('#coordinate').val(coordinates);
  } else {
    $('#coordinate').val('');
  }
}

function clearDrawnGeometries() {
  drawnItems.clearLayers();
  drawnGeometries = [];
}

map.on('draw:deleted', function (event) {
  clearDrawnGeometries();
  updateCoordinatesInput();
});


