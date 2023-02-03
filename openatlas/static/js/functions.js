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

  processUcFirst()

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
    setFilesOfDropField([...$('#file')[0].files])
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
      more = '<a href="" class="more-link">' + translate.moreText + '</a></span>';
      $(more).insertAfter(this);
    }
  });
  $(".more-link").click(function () {
    if ($(this).hasClass("less")) {
      $(this).removeClass("less");
      $(this).html(translate.moreText);
      $(this).prev().css('line-clamp', "10");
    } else {
      $(this).addClass("less");
      $(this).html(translate.lessText);
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

$.extend(true, $.fn.dataTable.defaults, {
     "initComplete": processUcFirst
});

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

async function refillTable(id, filterIds = []) {
  const tableContent = await $.ajax({
    type: 'post',
    url: `/ajax/get_entity_table/${id}`,
    data: {filterIds: JSON.stringify(filterIds)},
  });
  $(`#${id}-modal .modal-body-table`)
    .empty()
    .append($(`${tableContent}`));
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
  $('#' + name + '-clear-field').show();
}

function selectFromTreeMulti(name, value_type = false) {
  let checkedNames = [];
  const ids = $('#' + name + '-tree').jstree('get_selected');
  ids.forEach(function (item, index, array) {
    const type_ = $('#' + name + '-tree').jstree().get_node(item);
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
      checkedNames.push(type_);
    }
  });
  $("#" + name + "-selection")
      .html(checkedNames.map(x => closableBadge(x['text'],`deselectNode('${ name }', ${x['id']})`)));
  if (ids.length > 0) {
    $("#" + name).val('[' + ids + ']');
  } else {
    $("#" + name).val('');
  }
  $("#" + name).trigger('change');
}
function deselectNode(fieldId,nodeId){
 $(`#${fieldId}-tree`).jstree('deselect_node', nodeId); 
 selectFromTreeMulti(fieldId)
}
function selectFromTable(element, table, id,label= undefined) {
  $("#" + table).attr('value', id);
  $("#" + table + "-button").val(label || element?.innerText );
  $("#" + table + "-button").focus(); /* to refresh/fill button and remove validation errors */
  $("#" + table + "-clear-field").show();
  $('#' + table + '-modal').modal('hide');
}
function deselectFromTable(tableName, nodeId) {
  $(`#${tableName}_table`)?.find(`#${nodeId}[type="checkbox"]`)?.prop( "checked", false )
  selectFromTableMulti(tableName)
}
function selectFromTableMulti(name) {
  let checkedNames = [];
  let ids = [];
  $('#' + name + '_table').DataTable().rows().nodes().to$().find('input[type="checkbox"]').each(
    function () {
      if ($(this).is(':checked')) {
        checkedNames.push({name:$(this).val(),id:$(this).attr('id')});
        ids.push($(this).attr('id'));
      }
    });
  $('#' + name + '-selection')
      .html(checkedNames.map(x => closableBadge(x.name,`deselectFromTable('${name}',${x.id})`)));
  $('#' + name).val(ids.length > 0 ? '[' + ids + ']' : '').trigger('change');
}

function clearSelect(name) {
  $('#' + name).attr('value', '');
  $('#' + name + '-button').val('');
  $('#' + name + '-tree').jstree('deselect_all');
  $('#' + name + '-clear-field').hide();
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

function setFilesOfDropField(files) {
  const dropContainer = document.getElementById('drag-n-drop')
  dropContainer.children[0].style.display = "none";
  dropContainer.children[1].innerHTML = '';
  files?.forEach((file, index) => {
    const fileDiv = document.createElement('div');
    fileDiv.classList.add('drag-drop-item');
    fileDiv.innerHTML = `
                            <div class="card" data-bs-toggle="tooltip" data-bs-placement="top" title="${file.name}">
                                <div class="card-body">
                                <i class="card-icon fa fa-file"></i>
                                <i onclick="removeFile(${index})" class="close-icon fa fa-times"></i>
                                ${file.name}
                            </div>`
    dropContainer.children[1].appendChild(fileDiv)
  })
}

function removeFile(index) {
  const fileInput = document.getElementById('file')
  const filesList = [...fileInput.files];
  filesList.splice(index, 1);
  setFile(fileInput, filesList)
  setFilesOfDropField(filesList)
  if(filesList.length === 0){
    document.getElementById('drag-n-drop').children[0].style.display = "";
  }

}

function setFile(fileInput, fileList) {
  const newFiles = new DataTransfer();
  fileList.forEach(x => newFiles.items.add(x));
  fileInput.files = newFiles.files;
}

function addDragNDropListeners(dropContainer) {
  dropContainer.addEventListener("dragenter", function (e) {
    dropContainer.classList.add('highlight')

    e.preventDefault();
    e.stopPropagation();
  });
  dropContainer.addEventListener("dragover", function (e) {
    dropContainer.classList.add('highlight')

    e.preventDefault();
    e.stopPropagation();
  });
  dropContainer.addEventListener("dragleave", function (e) {
    dropContainer.classList.remove('highlight')

    e.preventDefault();
    e.stopPropagation();
  });

  dropContainer.addEventListener("drop", function (e) {
    const allowedTypes = ["gif", "jpeg", "jpg", "pdf", "png", "txt", "zip"]
    const allowedFiles = [...e.dataTransfer.files].filter(x => allowedTypes.includes(x.name.split(('.')).at(-1)))
    if (allowedFiles.length > 0) {
      const fileInput = document.getElementById('file')
      setFile(fileInput, [...fileInput.files, ...allowedFiles]);
      setFilesOfDropField([...fileInput.files])

      if ($('#name').val() == '') {
        const filename = allowedFiles[0].name;
        $('#name').val(filename.replace(/\.[^/.]+$/, ""));
      }
    }
    dropContainer.classList.remove('highlight')
    e.preventDefault();
    e.stopPropagation();
  });
}

// removable list field

function addListElement(id){
      const list = document.getElementById(id);
      const lastIndex = list.lastChild?.getElementsByTagName('input')?.item(0)?.id;
      const lastId = parseInt(lastIndex.split('-').pop(),10)

      const newField = document.createElement('li')
      newField.innerHTML = `
                            <div class="d-flex">
                                <input id="${id}-${lastId + 1}"  name="${id}-${lastId + 1}" class="form-control form-control-sm" type="text"/>
                                <button onclick="removeListField('${id}-${lastId + 1}')" type="button" class="${style.button.secondary} ms-1"><icon class="fa fa-minus"></icon></button>
                            </div>`
      list.appendChild(newField)
}

function removeListField(id){
  console.log(id)
        const el = document.getElementById(id);
        el.parentElement?.closest('li')?.remove();
}

function capitalizeFirstLetter(text){
  return text?.charAt(0)?.toUpperCase() + text?.slice(1);
}

function processUcFirst(){
  if (navigator.userAgent.indexOf("Firefox") != -1) {
    $(".uc-first").each(function (i, obj) {
      if (obj!=NaN && !!obj?.firstChild && obj?.firstChild?.nodeType === 3 && obj?.firstChild?.data)
        obj.firstChild.data = capitalizeFirstLetter(obj.firstChild.data)
    });
    document.body.style.display = '';
  }
}
