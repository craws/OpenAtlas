var postGisGeoJSON;
var selectedshape;
var editlayer;
var editmarker;
var drawnstuff = L.featureGroup();
var layer;
var shapesyntax;
var type;
var drawlayer;
var editon = 0;
var togglebtn = 0;
var shapename;
var shapetype;
var shapedescription;
var geometrytype;
var marker;
var markerimg; // temporary marker for coordinate capture
var capture = false; // var to store whether control is active or not
var coordcapture = false;
var headingtext;
var objectName = '';
var lastclicked;
var position;
var geoJsonArray = [];

var polygonbtn = L.easyButton(
    'topright',
    'fa-pencil-square-o',
    function () {
        shapetype = "shape";
        helptext = translate['map_info_shape'];
        headingtext = 'Shape';
        drawpolygon();
    },
    translate['map_info_shape']
    );

var areabutton = L.easyButton(
    'topright',
    'fa-circle-o-notch',
    function () {
        shapetype = "area";
        helptext = translate['map_info_area'];
        headingtext = 'Area';
        drawpolygon();
    },
    translate['map_info_area']
    );

var pointbutton = L.easyButton(
    'topright',
    'fa-map-marker',
    function () {
        helptext = translate['map_info_point'];
        headingtext = 'Point';
        shapetype = "centerpoint";
        capture = true;
        coordcapture = true;
        drawmarker();
    },
    translate['map_info_point']
);

function check_coordinates_input() {
    if ($('#easting').val() && $('#northing').val()) {
        $("#markersavebtn").prop('disabled', false);
    } else {
        $("#markersavebtn").prop('disabled', true);
    }
}

var datainput = L.control();
datainput.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'shapeinput');
    div.innerHTML += "\
        <div id='insertform' style='display:block'>\
            <form id='shapeform' onmouseover='interoff()' onmouseout='interon()'>\
                <i id='headingtext'>  </i>\
                <i id='closebtn' title='" + translate['map_info_close'] + "' onclick='closemyformx()' class='fa'>X</i>\
                <i id='editclosebtn' title='" + translate['map_info_close'] + "' onclick='editclosemyform()' class='fa'>X</i>\
                <i id='markerclosebtn' title='" + translate['map_info_close'] + "' onclick='closemymarkerformx()' class='fa'>X</i>\
                <br/>\
                <p id='p1'>Hello World!</p>\
                <div style='display: none'>\
                    <label>Parent:</label>\
                    <span><input type='text' id='shapeparent' value='NULL'/></span>\n\
                </div>\
                <div id='namefield' style='display: block'>\
                <span><input type='text' id='shapename' placeholder='enter name if desired'/></span> </div>\
                <span><textarea rows='3' cols='70' id='shapedescription' placeholder='" + translate['map_info_description'] + "'/></textarea></span>\
                <span><input type='text' id='shapetype' value='NULL'/></span>\
                <span><label id='eastinglabel' style='display: none'> Easting: </label><input type='text' oninput='check_coordinates_input()' id='easting' placeholder='decimal degrees' /></span>\
                <span><label id='northinglabel' style='display: none'> Northing:</label><input type='text' oninput='check_coordinates_input()' id='northing' placeholder='decimal degrees' /></span>\
                <div style='display: none'>\
                    <label> Coordinates: </label>\
                    <span><textarea rows='4' cols='50' id='shapecoords'/></textarea></span>\
                    <label> Geometrytype: </label>\
                    <span><input type='text' id='geometrytype'/></span>\n\
                </div>\
            </form>\
            <input type='button' title='Reset values and shape' id='resetbtn' disabled value='" + translate['map_clear'] + "' onclick='resetmyform()'/>\
            <input type='button' title='Save shape' id='savebtn' disabled value='" + translate['save'] + "' onclick='savetodb()'/>\
            <input type='button' title='Save edits' id='editsavebtn' disabled value='" + translate['save'] + "' onclick='editsavetodb()'/>\
            <input type='button' title='Save marker' id='markersavebtn' disabled value='" + translate['save'] + "' onclick='saveMarker()'/>\
         </div>";
    return div;
    document.getElementById("headingtext").innerHTML = headingtext;
};

var mylayer;
var myoldlayer;
var editIcon = L.icon({iconUrl: "/static/vendor/leaflet/images/marker-icon_edit.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
var editedIcon = L.icon({iconUrl: "/static/vendor/leaflet/images/marker-icon_edited.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});
var newIcon = L.icon({iconUrl: "/static/vendor/leaflet/images/marker-icon_new.png", iconAnchor: [12, 41], popupAnchor: [0, -34]});

function editshape() {
    togglebtns();
    if (editon === 0) {
        map.addControl(datainput);
        document.getElementById("p1").innerHTML = helptext;
        document.getElementById("headingtext").innerHTML = headingtext;
        document.getElementById("shapecoords").value = 'empty';
        document.getElementById('savebtn').style.display = 'none';
        document.getElementById('resetbtn').style.display = 'none';
        document.getElementById('closebtn').style.display = 'none';
        document.getElementById('editclosebtn').style.display = 'block';
        document.getElementById('editsavebtn').style.display = 'block';
        document.getElementById('markersavebtn').style.display = 'none';
        document.getElementById('shapename').value = shapename;
        document.getElementById('shapetype').value = shapetype;
        document.getElementById('shapedescription').value = shapedescription;
        $("#shapeform").on("input", function () {
            document.getElementById('editsavebtn').disabled = false;
        });
        map.closePopup();
        editon = 1;
        if (geometrytype === 'Polygon') {
            mylayer = L.polygon(editlayer.getLatLngs()).addTo(map);
            mylayer.bindPopup(
                '<div id="popup"><strong>' + objectName + '</strong><br/>' +
                '<div id="popup"><strong>' + shapename + '</strong><br/>' +
                '<i>' + shapetype + '</i><br/><br/>' +
                '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '</div>'
                );
            map.removeLayer(editlayer);
            if (typeof (myoldlayer) == 'object') {
                map.removeLayer(myoldlayer);
            }
            myoldlayer = L.polygon(editlayer.getLatLngs());
            myoldlayer.bindPopup(
                '<div id="popup"><strong>' + objectName + '</strong><br/>' +
                '<div id="popup"><strong>' + shapename + '</strong><br/>' +
                '<i>' + shapetype + '</i><br/><br/>' +
                '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '</div>' +
                '<button onclick="editshape()"/>' + translate['edit'] + '</button> <button onclick="deleteshape()"/>' + translate['delete'] + '</button></div>'
                );
            map.removeLayer(editlayer);
        }

        if (geometrytype === 'Point') {
            mylayer = L.marker((editlayer.getLatLng()), {draggable: true, icon: editIcon}).addTo(map);
            mylayer.bindPopup(
                '<div id="popup"><strong>' + objectName + '</strong><br/>' +
                '<div id="popup"><strong>' + shapename + '</strong><br/>' +
                '<i>' + shapetype + '</i><br/><br/>' +
                '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '</div>'
                );
            if (typeof (myoldlayer) == 'object') {
                map.removeLayer(myoldlayer);
            }
            myoldlayer = L.marker(editlayer.getLatLng());
            myoldlayer.bindPopup(
                '<div id="popup"><strong>' + objectName + '</strong><br/>' +
                '<div id="popup"><strong>' + shapename + '</strong><br/>' +
                '<i>' + shapetype + '</i> <br/> <br/>' +
                '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '<br/></div>' +
                '<button onclick="editshape()"/>' + translate['edit'] + '</button> <button onclick="deleteshape()"/>' + translate['delete'] + '</button></div>'
                );
            map.removeLayer(editlayer);
            document.getElementById('savebtn').style.display = 'none';
            document.getElementById('resetbtn').style.display = 'none';
            document.getElementById('closebtn').style.display = 'none';
            document.getElementById('editclosebtn').style.display = 'block';
            document.getElementById('editsavebtn').style.display = 'none';
            document.getElementById('markerclosebtn').style.display = 'none';
            document.getElementById('markersavebtn').style.display = 'none';
            document.getElementById('editsavebtn').style.display = 'block';
            document.getElementById('easting').style.display = 'block';
            document.getElementById('northing').style.display = 'block';
            document.getElementById('eastinglabel').style.display = 'block';
            document.getElementById('northinglabel').style.display = 'block';
            document.getElementById('northing').value = position.lat;
            document.getElementById('easting').value = position.lng;
            var wgs84 = mylayer.getLatLng();
            mylayer.on('dragend', function (event) {
                var marker = event.target;
                position = marker.getLatLng();
                document.getElementById('northing').value = position.lat;
                document.getElementById('easting').value = position.lng;
                document.getElementById('editsavebtn').disabled = false;
            });
        }
        mylayer.options.editing || (mylayer.options.editing = {});
        mylayer.editing.enable();
        document.getElementById('geometrytype').value = geometrytype;
        mylayer.on('edit', function () {
            var latLngs = mylayer.getLatLngs();
            var latLngs; // to store coordinates of vertices
            var newvector = []; // array to store coordinates as numbers
            geoJsonArray = [];
            var type = geometrytype.toLowerCase();
            document.getElementById('editsavebtn').disabled = false;
            if (type != 'marker') {  // if other type than point then store array of coordinates as variable
                latLngs = mylayer.getLatLngs();
                for (i = 0; i < (latLngs.length); i++) {
                    newvector.push(' ' + latLngs[i].lng + ' ' + latLngs[i].lat);
                    geoJsonArray.push('[' + latLngs[i].lng + ',' + latLngs[i].lat + ']');
                }
                if (type === 'polygon') {
                    // if polygon add first xy again as last xy to close polygon
                    newvector.push(' ' + latLngs[0].lng + ' ' + latLngs[0].lat);
                    shapesyntax = '(' + newvector + ')';
                    geoJsonArray.push('[' + latLngs[0].lng + ',' + latLngs[0].lat + ']');
                    returndata();

                }
                if (type === 'linestring') {
                    shapesyntax = newvector;
                    returndata();
                }
            }
            if (type === 'point') {
                latLngs = mylayer.getLatLng();
                newvector = (' ' + latLngs.lng + ' ' + latLngs.lat);
                shapesyntax = 'ST_GeomFromText(\'POINT(' + newvector + ')\',4326);'
                document.getElementById('northing').value = latLngs.lat;
                document.getElementById('easting').value = latLngs.lng;
            }
        });
    }
}

// what happens, after stuff is drawn
map.on('draw:created', function (e) {
    document.getElementById('savebtn').disabled = false;
    document.getElementById('resetbtn').disabled = false;
    drawnstuff.addLayer(e.layer); // add new geometry to layer
    type = e.layerType; // whatever geometry
    layer = e.layer;
    var latLngs; // to store coordinates of vertices
    var newvector = []; // array to store coordinates as numbers
    geoJsonArray = [];
    if (type != 'marker') {  // if other type than point then store array of coordinates as variable
        latLngs = layer.getLatLngs();
        for (i = 0; i < (latLngs.length); i++) {
            newvector.push(' ' + latLngs[i].lng + ' ' + latLngs[i].lat);
            geoJsonArray.push('[' + latLngs[i].lng + ',' + latLngs[i].lat + ']');
        }
        if (type === 'polygon') {
            // if polygon add first xy again as last xy to close polygon
            newvector.push(' ' + latLngs[0].lng + ' ' + latLngs[0].lat);
            geoJsonArray.push('[' + latLngs[0].lng + ',' + latLngs[0].lat + ']');
            shapesyntax = '(' + newvector + ')';
            returndata();
        }
        if (type === 'polyline') {
            shapesyntax = newvector;
            returndata();
        }
    }
    if (type === 'marker') {
        latLngs = layer.getLatLng();
        newvector = (' ' + latLngs.lng + ' ' + latLngs.lat);
        shapesyntax = 'ST_GeomFromText(\'POINT(' + newvector + ')\',4326);'
    }
});

function drawpolygon() {
    drawlayer = new L.Draw.Polygon(map);
    geometrytype = "polygon";
    capture = false;
    startdrawing();
}

function drawpolyline() {
    drawlayer = new L.Draw.Polyline(map);
    geometrytype = "linestring";
    startdrawing();
}

function startdrawing() {
    map.addControl(datainput);
    resetmyform();
    map.addLayer(drawnstuff);
    drawlayer.enable();
    togglebtns();
    $("#shapeform").on("input", function () {
        document.getElementById('resetbtn').disabled = false;
    });
}

function returndata() {
    document.getElementById("shapecoords").value = shapesyntax;
}

function editsavetodb() {
    document.getElementById('editsavebtn').style.display = 'none';
    var uid = selectedshape;
    var shapename = $('#shapename').val();
    var shapetype = $('#shapetype').val();
    var shapedescription = $('#shapedescription').val();
    var shapecoords = $('#shapecoords').val();
    var geometrytype = $('#geometrytype').val();
    var dataString = 'shapename=' + shapename + '&shapetype=' + shapetype + '&shapedescription=' + shapedescription + '&shapecoords=' + shapecoords + '&geometrytype=' + geometrytype + '&uid=' + uid;
    if (geometrytype == 'Polygon') {
        var myeditedlayer = L.polygon(mylayer.getLatLngs()).addTo(map);
        myeditedlayer.setStyle({fillColor: '#686868'});
        myeditedlayer.setStyle({color: '#686868'});
    }
    if (geometrytype == 'Point') {
        var myeditedlayer = L.marker((mylayer.getLatLng()), {icon: editedIcon}).addTo(map);
    }
    myeditedlayer.bindPopup(
        '<div id="popup"><strong>' + objectName + '</strong> (edited)<br/>' +
        '<div id="popup"><strong>' + shapename + '</strong> <br/>' +
        '<i>' + shapetype + '</i> <br/> <br/>' +
        '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '<br/><br/><br/> </div>' +
        '<i> (' + translate['map_info_reedit'] + ')</i>'
        );
    map.removeLayer(mylayer);
    // here we need the id of the shape/point not "selectedshape" which seems to be the id of the place
    // Now selectedshape is the ID of the shape of the object and no longer of the object
    // loop through array of existing
    if (geometrytype == 'Point') {
        var points = JSON.parse($('#gis_points').val());
        $.each(points, function (key, value) {
            var id = (JSON.stringify(value.properties.id));
            var index = ((JSON.stringify(key)));
            if (id == selectedshape) {
                points.splice(index, 1);
                return false;
            }
        });

        $('#gis_points').val(JSON.stringify(points)); // write array back to form field
        var point = '{"type":"Feature","geometry":{"type":"Point","coordinates":[' + $('#easting').val() + ',' + $('#northing').val() + ']},"properties":';
        point += '{"name": "' + $('#shapename').val().replace(/\"/g,'\\"') + '","description": "' + $('#shapedescription').val().replace(/\"/g,'\\"') + '","marker-color": "#fc4353","siteType":"To do","shapeType": "centerpoint"}}';
        var points = JSON.parse($('#gis_points').val());
        points.push(JSON.parse(point));
        $('#gis_points').val(JSON.stringify(points));
    }

    // here we need the id of the shape/point not "selectedshape" which seems to be the id of the place
    // Now selectedshape is the ID of the shape of the object and no longer of the object
    // loop through array of existing
    if (geometrytype == 'Polygon') {
        var polygons = JSON.parse($('#gis_polygons').val());
        $.each(polygons, function (key, value) {
            var id = (JSON.stringify(value.properties.id));
            var index = ((JSON.stringify(key)));
            if (id == selectedshape) {
                polygons.splice(index, 1);
                return false;
            }
        });
        $('#gis_polygons').val(JSON.stringify(polygons));
        var polygon = '{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[' + geoJsonArray.join(',') + ']]},"properties":';
        polygon += '{"name": "' + $('#shapename').val().replace(/\"/g,'\\"') + '","description": "' + $('#shapedescription').val().replace(/\"/g,'\\"') + '", "shapeType": "' + shapetype + '"}}';
        var polygons = JSON.parse($('#gis_polygons').val());
        polygons.push(JSON.parse(polygon));
        $('#gis_polygons').val(JSON.stringify(polygons));
    }
    editclosemyformsave();
}

function deleteshape() {
    if (editon === 0) {
        var dataString = 'uid=' + selectedshape + '&geometrytype=' + geometrytype;
        if (typeof (editlayer) == 'object') {
            map.removeLayer(editlayer);
        }
        if (typeof (editmarker) == 'object') {
            map.removeLayer(editmarker);
            var dataString = 'uid=' + selectedshape + '&geometrytype=' + geometrytype;
        }
        if (geometrytype == 'Point') {
            var points = JSON.parse($('#gis_points').val());
            $.each(points, function (key, value) {
                var id = (JSON.stringify(value.properties.id));
                var index = ((JSON.stringify(key)));
                if (id == selectedshape) {
                    points.splice(index, 1);
                    return false;
                }
            });
            $('#gis_points').val(JSON.stringify(points)); // write array back to form field
        }
        if (geometrytype == 'Polygon') {
            var polygons = JSON.parse($('#gis_polygons').val());
            $.each(polygons, function (key, value) {
                var id = (JSON.stringify(value.properties.id));
                var index = ((JSON.stringify(key)));
                if (id == selectedshape) {
                    polygons.splice(index, 1);
                    return false;
                }
            });
            $('#gis_polygons').val(JSON.stringify(polygons)); // write array back to form field
        }
    }
}

function resetDrawLayer() {
    drawnstuff.removeLayer(layer);
}

function resetmyform() {
    document.getElementById('savebtn').style.display = 'block';
    map.closePopup();
    document.getElementById("shapeform").reset();
    document.getElementById("geometrytype").value = geometrytype;
    if (capture = false) {
        drawlayer.enable();
    }
    document.getElementById('savebtn').disabled = true;
    document.getElementById('resetbtn').disabled = true;
    document.getElementById("shapetype").value = shapetype;
    document.getElementById("p1").innerHTML = helptext;
    document.getElementById("headingtext").innerHTML = headingtext;
}

function closemyform() {
    datainput.removeFrom(map);
    togglebtns();
    drawlayer.disable();
    var coordcapture = false;
    interon();
}

function closemyformx() {
    datainput.removeFrom(map);
    drawnstuff.removeLayer(layer);
    togglebtns();
    drawlayer.disable();
    var coordcapture = false;
    interon();
}

function closemymarkerformx() {
    datainput.removeFrom(map);
    if (marker) {
        map.removeLayer(marker);
    }
    togglebtns();
    coordcapture = false;
    capture = false;
    interon();
}

function closemymarkerform() {
    datainput.removeFrom(map);
    map.removeLayer(marker);
    togglebtns();
    coordcapture = false;
    capture = false;
    interon();
}

function editclosemyform() {
    editon = 0;
    datainput.removeFrom(map);
    map.removeLayer(mylayer);
    myoldlayer.addTo(map);
    togglebtns();
    var coordcapture = false;
    interon();
}

function editclosemyformsave() {
    editon = 0;
    datainput.removeFrom(map);
    map.removeLayer(mylayer);
    togglebtns();
    var coordcapture = false;
    interon();
}

map.on('click', function (e) {
    if (capture) {
        document.getElementById('markersavebtn').disabled = false;
        document.getElementById('geometrytype').value = 'point';
        if (typeof (marker) !== 'object') {
            marker = new L.marker(e.latlng, {draggable: true, icon: newIcon});
            marker.addTo(map);
            var wgs84 = (marker.getLatLng());
            document.getElementById('northing').value = wgs84.lat;
            document.getElementById('easting').value = wgs84.lng;
        } else {
            marker.setLatLng(e.latlng);
            marker.on('dragend', function (event) {
                var marker = event.target;
                position = marker.getLatLng();
                document.getElementById('northing').value = position.lat;
                document.getElementById('easting').value = position.lng;
            });
        }
        var wgs84 = marker.getLatLng();
        marker.on('dragend', function (event) {
            var marker = event.target;
            position = marker.getLatLng();
            document.getElementById('northing').value = position.lat;
            document.getElementById('easting').value = position.lng;
        });
        document.getElementById('northing').value = wgs84.lat;
        document.getElementById('easting').value = wgs84.lng;
    }
});

function drawmarker() {
    $('#map').css('cursor', 'crosshair');
    map.addControl(datainput);
    togglebtns();
    resetmyform();
    document.getElementById("p1").innerHTML = helptext;
    document.getElementById("headingtext").innerHTML = headingtext;
    document.getElementById('savebtn').style.display = 'none';
    document.getElementById('resetbtn').style.display = 'none';
    document.getElementById('closebtn').style.display = 'none';
    document.getElementById('markerclosebtn').style.display = 'block';
    document.getElementById('markersavebtn').style.display = 'block';
    document.getElementById('easting').style.display = 'block';
    document.getElementById('northing').style.display = 'block';
    document.getElementById('eastinglabel').style.display = 'block';
    document.getElementById('northinglabel').style.display = 'block';
}

function saveMarker() {
    capture = false;
    document.getElementById('savebtn').style.display = 'none';
    var point = '{"type":"Feature","geometry":{"type":"Point","coordinates":[' + $('#easting').val() + ',' + $('#northing').val() + ']},"properties":';
    point += '{"name": "' + $('#shapename').val().replace(/\"/g,'\\"') + '","description": "' + $('#shapedescription').val().replace(/\"/g,'\\"') + '", "shapeType": "centerpoint"}}';
    var points = JSON.parse($('#gis_points').val());
    points.push(JSON.parse(point));
    $('#gis_points').val(JSON.stringify(points));
    var newmarker = L.marker(([$('#northing').val(), $('#easting').val()]), {icon: newIcon}).addTo(map);
    newmarker.bindPopup(
        '<div id="popup"><strong>' + objectName + '</strong></br>' +
        '<div id="popup"><strong>' + $('#shapename').val() + '</strong></br>' +
        '<i> centerpoint </i></br></br>' +
        '<div style="max-height:140px; overflow-y: auto">' + $('#shapedescription').val() + '</br></br></br></div>' +
        '<i>' + translate['map_info_reedit'] + '</i>'
        );
    closemymarkerform();
}

function savetodb() {
    document.getElementById('savebtn').style.display = 'none';
    var shapename = $('#shapename').val();
    var shapetype = $('#shapetype').val();
    var shapedescription = $('#shapedescription').val();
    var shapecoords = $('#shapecoords').val();
    var geometrytype = $('#geometrytype').val();
    var dataString = '&shapename=' + shapename + '&shapetype=' + shapetype + '&shapedescription=' + shapedescription + '&shapecoords=' + shapecoords + '&geometrytype=' + geometrytype;
    $('#gisData').val($('#gisData').val() + dataString);
    var polygon = '{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[' + geoJsonArray.join(',') + ']]},"properties":';
    polygon += '{"name": "' + $('#shapename').val().replace(/\"/g,'\\"') + '","description": "' + $('#shapedescription').val().replace(/\"/g,'\\"') + '", "shapeType": "' + shapetype + '"}}';
    var polygons = JSON.parse($('#gis_polygons').val());
    polygons.push(JSON.parse(polygon));
    $('#gis_polygons').val(JSON.stringify(polygons));
    layer.bindPopup('<div id="popup"><strong>' + objectName + '</strong><br/>' +
        '<div id="popup"><strong>' + shapename + '</strong> <br/>' +
        '<i>' + shapetype + '</i> <br/> <br/>' +
        '<div style="max-height:140px; overflow-y: auto">' + shapedescription + '<br/><br/><br/> </div>' +
        '<i>' + translate['map_info_reedit'] + '</i>');
    layer.addTo(map);
    closemyform();
}
