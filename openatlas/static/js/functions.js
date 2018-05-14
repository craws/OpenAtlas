
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

$(document).ready(function() {

    /* jQuery UI tabs init */
    $("#tabs").tabs({
        activate: function(event, ui) {
            window.location.hash = ui.newPanel.attr('id');
        }
    });

    /* Show and hide function for date input fields */
    $("#date-switcher").click(function () {
        $(".date-switch").toggleClass('display-none');
        $(this).text(function(i, text){
            return text === show ? hide : show;
        })
    });

    /* When selecting a file for upload: if name is empty, fill with filename without extension */
    $('#file').on("change", function() {
        if ($('#name').val() == '') {
            var filename = $('#file')[0].files.length ? $('#file')[0].files[0].name : '';
            $('#name').val(filename.replace(/\.[^/.]+$/, ""));
        }
    });

    /* Show more/less function for texts */
    var showChar = 800;
    var ellipsesText = "...";
    $('.more').each(function() {
        var content = $(this).html();
        if (content.length > showChar) {
            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);
            var html = c + '<span class="more-ellipses">' + ellipsesText + '</span>'
            html += '<span class="more-content"><span>' + h + '</span>'
            html += '<a href="" class="more-link">' + moreText + '</a></span>';
            $(this).html(html);
        }
    });
    $(".more-link").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moreText);
        } else {
            $(this).addClass("less");
            $(this).html(lessText);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });
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

function createOverlay(name, title=false, multiple=false, type='table') {
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
            title: ucString(title).replace('_', ' '),
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
    $('#' + name + '-button').val(text.replace(/&apos;/g, "'"));
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
    if (ids.length > 0) {
        $("#" + name).val('[' + ids + ']');
    } else {
        $("#" + name).val('');
    }
    $("#" + name).trigger('change');
}

function selectFromTable(element, table, id) {
    $("#" + table).attr('value', id);
    $("#" + table + "-button").val(element.innerText);
    $("#" + table + "-button").focus(); /* to refresh/fill button and remove validation errors */
    $("#" + table + "-clear").show();
    $(".ui-dialog-titlebar-close").trigger('click');
}

function selectFromTableMulti(name) {
    var checkedNames = '';
    var ids = [];
    $("#" + name + "-table .multi-table-select").each(function () {
        if ($(this).is(':checked')) {
            checkedNames += $(this).val() + "<br />";
            ids.push($(this).attr('id'));
        }
    });
    if (ids.length > 0) {
        $("#" + name).val('[' + ids + ']');
    } else {
        $("#" + name).val('');
    }
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
