tinymce.init({
  menubar: false,
  relative_urls: false,
  mode: 'specific_textareas',
  editor_selector: 'tinymce',
  resize: 'both',
  toolbar_items_size: 'small',
  plugins: 'link code textcolor colorpicker',
  toolbar: 'bold italic underline strikethrough alignleft aligncenter alignright alignjustify ' +
      ' undo redo link unlink fontselect fontsizeselect forecolor code',
});

$(document).ready(function () {

  $('[data-bs-toggle="popover"]').popover(); // Popovers init

  /* DataTables - sort for checkbox columns */
  $.fn.dataTable.ext.order['dom-checkbox'] = function (settings, col) {
    return this.api().column(col, {order: 'index'}).nodes().map(function (td, i) {
      return $('input', td).prop('checked') ? '1' : '0';
    });
  };

  /* DataTables - sort for CIDOC model */
  $.fn.dataTable.ext.order["cidoc-model"] = function (settings, col) {
    return this.api()
      .column(col, { order: "index" })
      .nodes()
      .map((td) =>
        parseInt(
          td?.firstChild?.innerText
            ?.replace("OA", "100")
            ?.replace(/[\D]*/, "") || "0",
          10
        )
      );
  };

  /* DataTables - ignore special characters for search */
  var searchType = jQuery.fn.DataTable.ext.type.search;
  searchType.string = function (data) {
    return !data ?
        '' :
        typeof data === 'string' ?
            removeAccents(data) :
            data;
  };
  searchType.html = function (data) {
    return !data ?
        '' :
        typeof data === 'string' ?
            removeAccents(data.replace(/<.*?>/g, '')) :
            data;
  };

  /* When selecting a file for upload: if name is empty, fill with filename without extension */
  $('#file').on("change", function () {
    if ($('#name').val() == '') {
      var filename = $('#file')[0].files.length ? $('#file')[0].files[0].name : '';
      $('#name').val(filename.replace(/\.[^/.]+$/, ""));
    }
  });

  /* Show more/less function for texts */
  var showChar = 800;
  var ellipsesText = "...";
  $('.more').each(function () {
    var content = $(this).html();
    if (this.scrollHeight - 1 > this.clientHeight) {
      more = '<a href="" class="more-link">' + moreText + '</a></span>';
      $(more).insertAfter(this);
    }
  });
  $(".more-link").click(function () {
    if ($(this).hasClass("less")) {
      $(this).removeClass("less");
      $(this).html(moreText);
      $(this).prev().css('line-clamp', "10");
    } else {
      $(this).addClass("less");
      $(this).html(lessText);
      $(this).prev().css('line-clamp', "1000");
    }
    return false;
  });

  /* Bootstrap tabs navigation */
  let url = location.href.replace(/\/$/, "");
  if (location.hash) {
    const hashes = url.split("#")[1].split("_");
    $(`a[href="#${hashes[0]}"]`).tab('show');
    $(`#${hashes[1]}`).collapse('show');
    url = location.href.replace(/\/#/, "#");
    history.replaceState(null, null, url);
    setTimeout(() => {
      $(window).scrollTop(0);
    }, 400);
  } else {
    $(`a[href="#menu-tab-standard"]`).tab('show');
  }

  $('a[data-bs-toggle="tab"]').on("click", function () {
    let newUrl;
    const hash = $(this).attr("href");
    newUrl = url.split("#")[0] + hash;
    history.replaceState(null, null, newUrl);
  });

  /**
   * Wikidata autocomplete
   * Documentation: https://bootstrap-autocomplete.readthedocs.io/en/latest/
   * Bootstrap version needs to be manually set d/t
   */
  $('.Wikidata').autoComplete({
    bootstrapVersion: '4',
    resolver: 'custom',
    formatResult: function (item) {
        return {
            value: item.id,
            text: `${item.id} - ${item.label} - ${item.description}`
        };
    },
    events: {
        search: function (qry, callback) {
            $.ajax(
                `https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&format=json&origin=*&search=${qry}`,
            ).done(function (res) {
                callback(res.search)
            });
        }
    }
  }).on('autocomplete.select', function(evt,item) {
      $('.Wikidata').val(item.id);
  });
});

$.jstree.defaults.core.themes.dots = false;

/**
 * Sets default text size to a multiple of 0.2em via body stylesheet
 * @param {number}multiplier
 */
function resizeText(multiplier) {
  if (document.body.style.fontSize === '') {
    document.body.style.fontSize = '1.0em';
  }
  document.body.style.fontSize =
      parseFloat(document.body.style.fontSize) + (multiplier * 0.2) + 'em';
}

/**
 * Sets first character of passed string to an uppercase
 * @param {string}string
 * @returns {string}
 */
function ucString(string) {
  if (!string || typeof string !== 'string') {
    return '';
  }
  return string.charAt(0).toUpperCase() + string.slice(1);
}

/**
 * Makes an ajax request to bookmark a passed entity
 * @param {number}entityId
 */
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

async function ajaxAddEntity(data) {
  const newEntityId = await $.ajax({
    type: 'post',
    url: '/ajax/add_entity',
    data: data,
  });
  return newEntityId;
}

function getTable(id,filterIds = []){
  return $.ajax({
    type: 'post',
    url: `/ajax/get_entity_table/${id}`,
    data: {filterIds:JSON.stringify(filterIds)},
  });
}

async function ajaxAddType(data, fieldId, typeId, multiple=false) {
  const newTypeId = await $.ajax({
    type: 'post',
    url: '/ajax/addtype',
    data: data,
  });
  const typeTree = await getTypeTree(typeId);

  const selectNode = () => {
    selectFromTree(typeId, newTypeId, data.name);
  };
  const selectNodeMultiple = () => {
    $(`#${typeId}-tree`).jstree('select_node', newTypeId);
    $(`#${typeId}-tree`).unbind('refresh.jstree');
  };
  refreshCallback = multiple ? selectNodeMultiple : selectNode

  updateTree(`${fieldId}`, JSON.parse(typeTree.replaceAll("'", "\"")), refreshCallback);
  updateTree(`${fieldId}-dynamic`, JSON.parse(typeTree.replaceAll("'", "\"")));
  $('.modal').modal('hide');
  return newTypeId;
}

function getTypeTree(rootId){
  return $.ajax({type: 'get', url: `/ajax/get_type_tree/${rootId}`});
}
function updateTree(id, d, refreshCallback) {
  $(`#${id}-tree`).jstree(true).settings.core.data = d;
  $(`#${id}-tree`).jstree(true).refresh();
  if (refreshCallback) $(`#${id}-tree`).on('refresh.jstree', refreshCallback);
}
function fillTreeSelect(id,d,minimum_jstree_search){
    $(`#${id}-tree`).jstree({
      "plugins": ["search"],
      "core": {"check_callback": true, "data": d},
      "search": {
          "case_insensitive": true,
          "show_only_matches": true,
          "show_only_matches_children": true
      },
  });

  $(`#${id}-tree`).on("select_node.jstree", function (e, data) {
      selectFromTree(`${id}`, data.node.id, data.node.text);
  });
  $(`#${id}-tree-search`).keyup(function () {
      if (this.value.length >= minimum_jstree_search) {
          $(`#${id}-tree`).jstree("search", $(this).val());
      } else if (this.value.length == 0) {
          $(`#${id}-tree`).jstree("search", $(this).val());
          $(`#${id}-tree`).jstree(true).show_all();
      }
  });
}

function selectFromTree(name, id, text) {
  $('#' + name).val(id)
  $('#' + name + '-button').val(text.replace(/&apos;/g, "'"));
  $('#' + name + '-modal').modal('hide');
  $('#' + name + '-clear').show();
}

function selectFromTreeMulti(name, value_type = false) {
  var checkedNames = '';
  var ids = $('#' + name + '-tree').jstree('get_selected');
  ids.forEach(function (item, index, array) {
    var type_ = $('#' + name + '-tree').jstree().get_node(item);
    if (value_type) {
      $('#' + name + '-button').after('<span> ' + type_['text'] + '</span>');
      $('#' + name + '-button').after(
          $('<input>').attr({
            type: 'text',
            id: type_.id,
            name: type_.id,
            value: '20',
            class: 'value_input'
          }));
      $('#' + name + '-button').after($('<br>'));
    } else {
      checkedNames += type_['text'] + "<br>";
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

function selectFromTable(element, table, id,label= undefined) {
  $("#" + table).attr('value', id);
  $("#" + table + "-button").val(label || element?.innerText );
  $("#" + table + "-button").focus(); /* to refresh/fill button and remove validation errors */
  $("#" + table + "-clear").show();
  $('#' + table + '-modal').modal('hide');
}

function selectFromTableMulti(name) {
  var checkedNames = '';
  var ids = [];
  $('#' + name + '_table').DataTable().rows().nodes().to$().find('input[type="checkbox"]').each(
      function () {
        if ($(this).is(':checked')) {
          checkedNames += $(this).val() + '<br>';
          ids.push($(this).attr('id'));
        }
      });
  $('#' + name + '-selection').html(checkedNames);
  $('#' + name).val(ids.length > 0 ? '[' + ids + ']' : '').trigger('change');
}

function clearSelect(name) {
  $('#' + name).attr('value', '');
  $('#' + name + '-button').val('');
  $('#' + name + '-tree').jstree('deselect_all');
  $('#' + name + '-clear').hide();
}

function overflow() {
  setTimeout(() => {
    $('td').bind('mouseenter', function () {
      var $this = $(this);
      if (this.offsetWidth < this.scrollWidth) {
        $this.attr('title', $this.text());
      }
    });
  }, 0);
}

function removeAccents(data) {
  if (data.normalize) {
    // Use I18n API if available to split characters and accents, then remove
    // the accents wholesale. Note that we use the original data as well as
    // the new to allow for searching of either form.
    return data + ' ' + data
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');
  }
  return data;
}
