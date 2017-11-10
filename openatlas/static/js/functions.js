
tinymce.init({
    menubar: false,
    relative_urls : false,
    mode: 'specific_textareas',
    editor_selector: 'tinymce',
    resize: 'both',
    toolbar_items_size : 'small',
    plugins: 'link code textcolor colorpicker',
    toolbar: 'bold italic underline strikethrough alignleft aligncenter alignright alignjustify ' +
        ' undo redo link unlink fontselect fontsizeselect forecolor code',
});

$.jstree.defaults.core.themes.dots = false;

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
    if (document.body.style.fontSize === '') {
        document.body.style.fontSize = '1.0em';
    }
    document.body.style.fontSize =
        parseFloat(document.body.style.fontSize) + (multiplier * 0.2) + 'em';
}

function ucString(string) {
    if (!string) {
        return '';
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function createOverlay(name, title, multiple = false, type = 'table') {
    if (!title) {
        title = name;
    }
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
            title: ucString(title),
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

function selectFromTree(name, id, text) {
    $('#' + name).val(id)
    $('#' + name + '-button').val(text);
    $('#' + name + '-dialog').dialog('close');
    $('#' + name + '-clear').show();
}

function selectFromTreeMulti(name) {
    var checkedNames = '';
    var ids = $('#' + name + '-tree').jstree('get_selected');
    ids.forEach(function (item, index, array) {
        var node = $('#' + name + '-tree').jstree().get_node(item);
        checkedNames += node['text'] + "<br />";
    });
    $("#" + name + "-selection").html(checkedNames);
    /* Todo: js required validation with trigger on multi fields not working anymore (have '[]') */
    /* e.g. event */
    $("#" + name).val('[' + ids + ']').trigger('change');
}

function selectFromTable(element, table, id) {
    $("#" + table).attr('value', id);
    $("#" + table + "-button").val(element.innerHTML);
    $("#" + table + "-button").focus(); /* to refresh/fill button and remove validation errors */
    $("#" + table + "-clear").show();
    $(".ui-dialog-titlebar-close").trigger('click');
}

function selectFromTableMulti(name) {
    var checkedNames = '';
    var ids = [];
    $(".multi-table-select").each(function () {
        if ($(this).is(':checked')) {
            checkedNames += $(this).val() + "<br />";
            ids.push($(this).attr('id'));
        }
    });
    $("#" + name).val('[' + ids + ']');
    $("#" + name + "-selection").html(checkedNames);
}

function clearSelect(name) {
    $('#' + name).attr('value', '');
    $('#' + name + '-button').val('');
    $('#' + name + '-tree').jstree('deselect_all');
    $('#' + name + '-clear').hide();
}

function openParentTab() {
    locationHash = location.hash.substring(1);
    console.log(locationHash);
    if (locationHash) {
        var hash = $('#' + locationHash);
        if (hash.length) {
            if (hash.closest(".tab-content").length) {
                var tabNumber = hash.closest(".tab-content").index();
                $("#tabs-menu").tabs({active: tabNumber - 1});
            }
        }
    }
}
