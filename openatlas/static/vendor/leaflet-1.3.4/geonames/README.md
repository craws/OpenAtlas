# Leaflet.Geonames

A [GeoNames](http://www.geonames.org/) powered geocoding search control for Leaflet.

It allows you to enter a placename, display a list of search results using GeoNames,
and select a placename to zoom to.

Location markers remain on the map until the search field is cleared.
Click on icon to open / close unless `alwaysOpen` is set to true (in which case clicking on the icon does nothing).

\*Tested with Leaflet 1.1.0

## Install

From NPM:

```
npm install leaflet-geonames
```

## Usage

Include the CSS:

```
<link rel="stylesheet" href="L.Control.Geonames.css" />
```

This control uses [Google Material Icons](https://design.google.com/icons) by default.

Include the JavaScript:

```
<script src="L.Control.Geonames.min.js"></script>
```

Example usage:

```
var control = L.control.geonames({
    //position: 'topcenter',  // in addition to standard 4 corner Leaflet control layout, this will position and size from top center
    geonamesURL: '//api.geonames.org/searchJSON',  // override this if using a proxy to get connection to geonames
    username: '',  // Geonames account username.  Must be provided
    zoomLevel: null,  // Max zoom level to zoom to for location.  If null, will use the map's max zoom level.
    maxresults: 5,  // Maximum number of results to display per search
    className: 'leaflet-geonames-icon', //class for icon
    workingClass: 'leaflet-geonames-icon-working', //class for search underway
    featureClasses: ['A', 'H', 'L', 'P', 'R', 'T', 'U', 'V'],  // feature classes to search against.  See: http://www.geonames.org/export/codes.html
    baseQuery: 'isNameRequired=true',  // The core query sent to GeoNames, later combined with other parameters above
    position: 'topleft',
    showMarker: true, //Show a marker at the location the selected location
    showPopup: true, //Show a tooltip at the selected location
    adminCodes: { // filter results by a country and state.  Values can be strings or return by a function.
        country: 'us',
        adminCode1: function() {return 'wa'}
    },
    lang: 'en', // language for results
    bbox: {east:-121, west: -123, north: 46, south: 45}, // bounding box filter for results (e.g., map extent).  Values can be an object with east, west, north, south, or a function that returns that object.
    alwaysOpen: false,  //if true, search field is always visible
    enablePostalCodes: false, // if true, use postalCodesRegex to test user provided string for a postal code.  If matches, then search against postal codes API instead.
    postalCodesRegex: POSTALCODE_REGEX_US // regex used for testing user provided string for a postal code.  If this test fails, the default geonames API is used instead.
});
map.addControl(control);
```

For mobile responsive view, use `position: 'topcenter'` and `alwaysOpen: true` options.
See [mobile example](http://consbio.github.io/Leaflet.Geonames/examples/mobileview.html)
using a mobile device or emulator.

## Events

### Search Event

This control fires a `search` event with the value of search parameters:

`control.on('search', function(e){console.log(e.params)});`

results in
`{q: "oregon", lang: "en"}`

### Select Event

This control fires a `select` event when an option was selected from list,
with the full response JSON from geonames:

`control.on('select', function(e){console.log(e.geoname)});`

results in
`{adminCode1: "OR", lng: "-120.50139", geonameId: 5744337, ...}`

## Demos:

* [Basic](/examples/basic.html)
* [Admin Codes](/examples/adminCodes.html)
* [Bounding Box](/examples/bbox.html)
* [Locale](/examples/locale.html)
* [Events](/examples/events.html)
* [Mobile View](/examples/mobileview.html)
* [Postal Codes](/examples/postCodes.html)

## Changes

See [changelog](CHANGES.md)

## Credits:

Developed with support from the [South Atlantic Landscape Conservation Cooperative](http://www.southatlanticlcc.org/), and maintained with support from [Peninsular Florida LCC](http://peninsularfloridalcc.org/).

Some ideas derived from [L.GeoSearch](https://github.com/smeijer/L.GeoSearch).

## Contributors:

* [Brendan Ward](https://github.com/brendan-ward)
* [Kaveh Karimi-Asli](https://github.com/ka7eh)
* [Nik Molnar](https://github.com/nikmolnar)
* [Mike Moran](https://github.com/mikemoraned)
* [Natasha Anisimova](https://github.com/anisimon)
