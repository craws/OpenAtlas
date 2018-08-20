/* EasyButton */

L.Control.EasyButtons = L.Control.extend({
    onAdd: function () {
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        this.link = L.DomUtil.create('a', 'leaflet-bar-part', container);
        this._addImage()
        this.link.href = '#';
        L.DomEvent.on(this.link, 'click', this._click, this);
        this.link.title = this.options.title;
        return container;
    },
    _click: function (e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);
        this.intendedFunction();
    },
    _addImage: function () {
        var extraClasses = this.options.intentedIcon.lastIndexOf('fa', 0) === 0 ? ' fa fa-lg' : ' glyphicon';
        L.DomUtil.create('i', this.options.intentedIcon + extraClasses, this.link);
    }
});

var polygonButton = new L.Control.EasyButtons;
polygonButton.options.position = 'topright';
polygonButton.options.intentedIcon = 'fa-pencil-square-o';
polygonButton.options.title = translate['map_info_shape'];
polygonButton.intendedFunction =
    function () {
        shapeType = "shape";
        helpText = translate['map_info_shape'];
        headingText = 'Shape';
        // drawPolygon();
    }
map.addControl(polygonButton);

var areaButton = new L.Control.EasyButtons;
areaButton.options.position = 'topright';
areaButton.options.intentedIcon = 'fa-circle-o-notch';
areaButton.options.title = translate['map_info_area'];
areaButton.intendedFunction =
    function () {
        shapeType = "area";
        helpText = translate['map_info_area'];
        headingText = 'Area';
        // drawPolygon();
    }
map.addControl(areaButton);


var pointButton = new L.Control.EasyButtons;
pointButton.options.position = 'topright';
pointButton.options.intentedIcon = 'fa-map-marker';
pointButton.options.title = translate['map_info_point'];
pointButton.intendedFunction =
    function () {
        shapeType = "centerpoint";
        helpText = translate['map_info_point'];
        headingText = 'Point';
        capture = true;
        coordinatesCapture = true;
        // drawMarker();
    }
map.addControl(pointButton);



