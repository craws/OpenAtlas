L.Control.Geonames = L.Control.extend({
    _active: false,
    _resultsList: null,
    _marker: null,
    _hasResults: false,
    options: {
        username: '', //Geonames account username.  Must be provided
        maxresults: 5, //Maximum number of results to display per search
        zoomLevel: null, //Max zoom level to zoom to for location.  If null, will use the map's max zoom level.
        className: 'fa fa-crosshairs', //class for icon
        workingClass: 'fa-spin', //class for search underway
        featureClasses: ['A', 'H', 'L', 'P', 'R', 'T', 'U', 'V'], //feature classes to search against.  See: http://www.geonames.org/export/codes.html
        baseQuery: 'isNameRequired=true', //The core query sent to GeoNames, later combined with other parameters above
        position: 'topleft',
    },
    onAdd: function () {
        this._container = L.DomUtil.create('div', 'leaflet-geonames-search leaflet-bar');
        this._container.title = 'Search by location name';
        var link = this._link = L.DomUtil.create('a', this.options.className, this._container);
        link.href = '#';
        var form = L.DomUtil.create('form', '', this._container);
        L.DomEvent.addListener(form, 'submit', this._search, this);
        var input = this._input = L.DomUtil.create('input', '', form);
        input.type = 'text';
        input.placeholder = 'Enter a location name';
        input.id = 'geosearch';
        this._resultsList = L.DomUtil.create('ul', '', this._container);
        L.DomEvent
            .on(this._container, 'dblclick', L.DomEvent.stop)
            .on(this._container, 'click', L.DomEvent.stop)
            .on(link, 'click', function () {
                this._active = !this._active;
                if (this._active) {
                    L.DomUtil.addClass(this._container, 'active');
                    input.focus();
                    if (this._hasResults) {
                        L.DomUtil.addClass(this._resultsList, 'hasResults');
                    }
                } else {
                    this._close();
                }
            }, this);

        return this._container;
    },
    _close: function () {
        L.DomUtil.removeClass(this._container, 'active');
        L.DomUtil.removeClass(this._resultsList, 'hasResults');
        L.DomUtil.removeClass(this._resultsList, 'noResults');
        this._active = false;
        if (this._marker != null) {
            this._map.removeLayer(this._marker);
            this._marker = null;
        }
    },
    _search: function (event) {
        L.DomEvent.preventDefault(event);
        L.DomUtil.addClass(this._link, this.options.workingClass);
        L.DomUtil.removeClass(this._resultsList, 'noResults');
        //clear results
        this._hasResults = false;
        this._resultsList.innerHTML = '';
        var url = 'https://secure.geonames.org/searchJSON?q=' + encodeURIComponent(this._input.value)
            + '&maxRows=' + this.options.maxresults
            + '&username=' + this.options.username
            + '&style=LONG';
        if (this.options.featureClasses && this.options.featureClasses.length) {
            url += '&' + this.options.featureClasses.map(function (fc) {
                return 'featureClass=' + fc
            }).join('&');
        }
        if (this.options.baseQuery) {
            url += '&' + this.options.baseQuery;
        }
        var origScope = this;
        var callbackName = 'geonamesSearchCallback';
        this._jsonp(url,
            function (response) {
                document.body.removeChild(document.getElementById('getJsonP'));
                delete window[callbackName];
                origScope._processResponse(response);
            },
            callbackName
        );
    },
    _jsonp: function (url, callback, callbackName) {
        callbackName = callbackName || 'jsonpCallback';
        window[callbackName] = callback;
        url += '&callback=' + callbackName;
        var script = document.createElement('script');
        script.id = 'getJsonP';
        script.src = url;
        script.async = true;
        document.body.appendChild(script);
    },
    _processResponse: function (response) {
        L.DomUtil.removeClass(this._link, this.options.workingClass);
        if (response.geonames.length > 0) {
            L.DomUtil.addClass(this._resultsList, 'hasResults');
            this._hasResults = true;
            var li;
            response.geonames.forEach(function (geoname) {
                li = L.DomUtil.create('li', '', this._resultsList);
                li.innerHTML = this._getName(geoname);
                L.DomEvent.addListener(li, 'click', function () {
                    var lat = parseFloat(geoname.lat);
                    var lon = parseFloat(geoname.lng);
                    if (this._marker != null) {
                        this._map.removeLayer(this._marker);
                        this._marker = null;
                    }
                    this._marker = L.userMarker([lat, lon], {pulsing: true, accuracy: 100}).addTo(this._map).bindPopup(
                        '<div style="max-width:200px">' + this._getName(geoname) + '</div>');
                    this._map.setView([lat, lon], this.options.zoomLevel || this._map.getMaxZoom(), false);
                    //this._map.panBy(new L.Point(-100, 0));
                    //this._marker.openPopup();
                }, this);
            }, this);
        } else {
            L.DomUtil.addClass(this._resultsList, 'noResults');
            li = L.DomUtil.create('li', '', this._resultsList);
            li.innerText = 'No results found';
        }
    },
    _getName: function (geoname) {
        var name = geoname.name;
        var extraName;
        ['adminName1', 'countryName'].forEach(function (d) {
            extraName = geoname[d];
            if (extraName && extraName != '' && extraName != geoname.name) {
                name += ', ' + extraName;
            }
        }, this);
        return name;
    }
});

L.control.geonames = function (options) {
    return new L.Control.Geonames(options);
};

$(document).ready(function () {  //disable/enable dragging when cursor is in/out of input field
    interonoff('#geosearch');
});
