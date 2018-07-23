// Derived from Leaflet.Geonames https://github.com/consbio/Leaflet.Geonames

L.Control.Sitesearch = L.Control.extend({
    _active: false,
    options: {
        className: 'fa fa-search', //class for icon
        workingClass: 'fa-spin', //class for search underway
        position: 'topleft',
    },
    onAdd: function () {
        this._container = L.DomUtil.create('div', 'leaflet-sitesearch-search leaflet-bar');
        this._container.title = 'Search by site name';
        var link = this._link = L.DomUtil.create('a', this.options.className, this._container);
        link.href = '#';
        var form = L.DomUtil.create('form', '', this._container);
        var input = this._input = L.DomUtil.create('input', '', form);
        input.id = 'search';
        input.type = 'text';
        input.placeholder = 'Enter a site name';
        L.DomEvent
            .on(this._container, 'dblclick', L.DomEvent.stop)
            .on(this._container, 'click', L.DomEvent.stop)
            .on(link, 'click', function () {
                this._active = !this._active;
                if (this._active) {
                    L.DomUtil.addClass(this._container, 'active');
                    input.i
                    input.focus();
                } else {
                    this._close();
                }
            }, this);
        return this._container;
    },
    _close: function () {
        L.DomUtil.removeClass(this._container, 'active');
        this._active = false;
    },
});

L.control.Sitesearch = function (options) {
    return new L.Control.Sitesearch(options);
};

$(document).ready(function () {  //disable/enable dragging when cursor is in/out of input field
    interonoff('#search');
});

$(function () { //autocomplete jquery ui with site data
    $("#search").keypress(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
        }
    });
    $("#search").autocomplete({
        source: jsonSearch,
        select: function (event, ui) {
            $("#search").val(ui.item.label);
            xylatlon = ([ui.item.lat, ui.item.lon]);
            var y = (ui.item.lon);
            var x = (ui.item.lat);
            var searchuid = (ui.item.uid);
            openSite(searchuid, x, y);
            map.panBy(new L.Point(0, -150));
            $(this).val('');
            return false;
        }
    }).data("ui-autocomplete")._renderItem = function (ul, item) {
        return $("<li></li>")
            .data("ui-autocomplete-item", item)
            .append("<a><strong>" + item.label + "</strong> / " + item.type + "<br></a>")
            .appendTo(ul);
    };
});

function openSite(id, x, y) {  //open Popup after site is selected
    map.setView([y, x], 15);
    sitesmarkers.eachLayer(function (marker) {
        if (marker.feature.properties.id === id) {
            marker.openPopup();
        }
    });
}
