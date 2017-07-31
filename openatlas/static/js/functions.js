
tinymce.init({
    menubar: false,
    relative_urls : false,
    mode: "specific_textareas",
    editor_selector: "tinymce",
    resize: "both",
    toolbar_items_size : 'small',
    plugins: "link code textcolor colorpicker",
    toolbar: "bold italic underline strikethrough alignleft aligncenter alignright alignjustify undo redo link " +
        "unlink fontselect fontsizeselect forecolor code",
});

$.tablesorter.addParser({
    id: 'class_code',
    is: function (string) {return false;},
    format: function (string) {return string.replace(/E/,'');},
    type: 'numeric'
});

$.tablesorter.addParser({
    id: 'property_code',
    is: function (string) {return false;},
    format: function(string) {return string.replace(/P/,'');},
    type: 'numeric'
});

function resizeText(multiplier) {
    if (document.body.style.fontSize === "") {
        document.body.style.fontSize = "1.0em";
    }
    document.body.style.fontSize = parseFloat(document.body.style.fontSize) + (multiplier * 0.2) + "em";
}

function ucString(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function selectFromTable(element, table, id) {
    $("#" + table).attr('value', id);
    $("#" + table + "-button").val(element.innerHTML);
    $("#" + table + "-button").focus(); /* to refresh/fill button and remove validation errors */
    $("#" + table + "-clear").show();
    $(".ui-dialog-titlebar-close").trigger('click');
}

function createOverlay(name, multiple = false, type = 'table') {
    $('#' + name + '-overlay').click(function () {
        $('#' + name + '-dialog').dialog('close');
    });
    $('#' + name + '-button').click(function () {
        $('#' + name + '-overlay').height($(window).height());
        $('#' + name + '-overlay').width($(window).width());
        $('#' + name + '-overlay').fadeTo(1, 0.6);
        $('#' + name + '-dialog').dialog({
            position: {my: 'center top', at: 'center top+80', of: window},
            closeText: 'X',
            title: ucString(name),
            closeOnEscape: true,
            width: 'auto',
            height: 'auto',
            close: function () {
                if (multiple && type=='tree') {
                    selectFromTreeMulti(name);
                }
                if (multiple && type=='table') {
                    selectFromTableMulti(name);
                }
                $('#' + name + '-overlay').css('display', 'none');
            }
        });
        $('#' + name + '-table').trigger('applyWidgets');
        $('#' + name + '-search').focus();
    });
}

function ajaxBookmark(entityId) {
    $.ajax({
        type: 'POST',
        url: '/ajax/bookmark',
        data: 'entity_id=' + entityId,
        success: function (label) {
            $('#bookmark' + entityId).html(label);
        }
    });
}
