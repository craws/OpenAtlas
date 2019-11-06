
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

    // DataTables - sort for checkbox columns
    $.fn.dataTable.ext.order['dom-checkbox'] = function(settings, col) {
        return this.api().column(col, {order:'index'}).nodes().map( function (td, i) {
            return $('input', td).prop('checked') ? '1' : '0';
        });
    };

    // DataTables - sort for CIDOC model
    $.fn.dataTable.ext.order['cidoc-model'] = function(settings, col) {
        return this.api().column(col, {order:'index'}).nodes().map( function (td, i) {
            const d = td.firstChild.innerText
                .replace('OA', '100')
                .replace(/[\D]*/,'');
            return parseInt(d, 10);
        });
    };

    // DataTables - ignore special characters for search
    (function(){
        function removeAccents ( data ) {
            if ( data.normalize ) {
                // Use I18n API if available to split characters and accents, then remove
                // the accents wholesale. Note that we use the original data as well as
                // the new to allow for searching of either form.
                return data +' '+ data
                    .normalize('NFD')
                    .replace(/[\u0300-\u036f]/g, '');
            }
            return data;
        }
        var searchType = jQuery.fn.DataTable.ext.type.search;
        searchType.string = function ( data ) {
            return ! data ?
                '' :
                typeof data === 'string' ?
                    removeAccents( data ) :
                    data;
        };
        searchType.html = function ( data ) {
            return ! data ?
                '' :
                typeof data === 'string' ?
                    removeAccents( data.replace( /<.*?>/g, '' ) ) :
                    data;
        };
    }());

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

    /* Show and hide function for value type input fields */
    $("#value-type-switcher").click(function () {
        $(".value-type-switch").toggleClass('display-none');
        $(this).text(function(i, text){
            return text === show ? hide : show;
        })
    })

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

function createOverlay(name, title=false, multiple=false, type='table', value_type=false) {
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
                    selectFromTreeMulti(name, value_type);
                }
                if (multiple && type=='table') {
                    selectFromTableMulti(name);
                }
                $('#' + name + '-overlay').css('display', 'none');
            }
        });
        $('#' + name + '-table').trigger('applyWidgets');
        $('#' + name + '-search').focus(); /* set search focus for tree select */
        $('#' + name + '_table_filter > label > input').focus(); /* focus for multi table select */
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

function selectFromTreeMulti(name, value_type=false) {
    var checkedNames = '';
    var ids = $('#' + name + '-tree').jstree('get_selected');
    ids.forEach(function (item, index, array) {
        var node = $('#' + name + '-tree').jstree().get_node(item);
        if (value_type) {
            $('#' + name + '-button').after('<span> ' + node['text'] + '</span>');
            $('#' + name + '-button').after(
                $('<input>').attr({
                    type: 'text',
                    id: node.id ,
                    name: node.id,
                    value: '20',
                    class: 'value_input'
            }));
            $('#' + name + '-button').after($('<br>'));
        } else {
            checkedNames += node['text'] + "<br>";
        }
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
    $('#' + name + '_table').DataTable().rows().nodes().to$().find('input[type="checkbox"]').each(
        function() {
            if ($(this).is(':checked')) {
                checkedNames += $(this).val() + '<br>';
                ids.push($(this).attr('id'));
            }
        });
    $('#' + name + '-selection').html(checkedNames);
    $('#' + name).val(ids.length > 0 ? '[' + ids+ ']' : '').trigger('change');
}

function clearSelect(name) {
    $('#' + name).attr('value', '');
    $('#' + name + '-button').val('');
    $('#' + name + '-tree').jstree('deselect_all');
    $('#' + name + '-clear').hide();
}

function openParentTab() {
    locationHash = location.hash.substring(1);
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
