const variables = {}

/* Handle Accessibility Inputs */
function onActivateKeyInput(event) {
  if (
    event.key !== "Enter" &&
    event.key !== " "
  ) {
    return false;
  }
  event.stopPropagation();
  event.preventDefault();
  return true;
}

function validateSubmitHandler (form) {
  if (form.dataset.dateInvalid === 'true') {
    return;
  }
  if (typeof this.submitButton !== 'undefined') {
      if (this.submitButton.id === "insert_and_continue") $('#continue_').val('yes');
      if (this.submitButton.id === "insert_continue_sub") $('#continue_').val('sub');
      if (this.submitButton.id === "insert_continue_human_remains") $('#continue_').val('human_remains');
    $('button[type="submit"]').prop("disabled", true).text(translate.inProgress);
    form.submit();
  }
}

/* Show and hide function for value type input fields. Has to be outside of $(document).ready() */
function switch_value_type(id, el) {
  if (el.hasAttribute('show')) {
    el.removeAttribute('show');
    $(`.value-type-field.sub-of-${id}`).each(function () {
      this.classList.add('d-none');
    });
    $(`.value-type-field.sub-of-${id} .value-type-switcher`).each(function () {
      this.removeAttribute('show');
    });
  } else {
    $(`.value-type-field.direct-sub-of-${id}`).each(function () {
      this.classList.remove('d-none');
    });
    el.setAttribute('show', '');
  }
  el.setAttribute("aria-pressed", el.hasAttribute('show'));
}

$(document).ready(function () {

  /* Write selected DataTables checkboxes to hidden input */
  $('#checkbox-form').submit((a) => {
    ids = [];
    $('#checkbox-form .dataTable').DataTable().rows().nodes().to$().find('input[type="checkbox"]').each(
      function () {
        if ($(this).is(':checked')) {
          ids.push($(this).attr('value'));
        }
      });
    $('#checkbox_values').val(ids.length > 0 ? '[' + ids + ']' : '');
  });

  /* Needed for ajax bookmark functionality */
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", bookmark_csrf_token);
      }
    }
  });

  /* Show and hide function for reference systems */
  $("#reference-system-switcher").click(function () {
    $(".reference-system-switch").toggleClass('d-none');
    $(this).text(function (i, text) {
      return $.trim(text) === translate.show ? translate.hide : translate.show;
    })
  });

  /* Hide value type fields with class* wildcard selector */
  $('[class*="value-type-switch"]').addClass('display-none');

  $('#show_passwords').show()
  .change(function () {
    $('#password')[0].type = this.checked ? 'text' : 'password';
    $('#password2')[0].type = this.checked ? 'text' : 'password';
    if (document.getElementById('password_old')) {
      $('#password_old')[0].type = this.checked ? 'text' : 'password';
    }
  });

  /* Below section sets up validation for various forms */
  let v = $.validator;
  v.setDefaults({
    ignore: ".date-switch input, .year, .month, .day, .hour, .minute, .second",
  });

  v.addClassRules({
    integer: {digits: true},
    signed_integer: {signedInteger: true},
    email: {email: true},
    "value-type": {number: true}
  });

  v.addMethod('notEqual', function (value, element, param) {
    return this.optional(element) || value != $(param).val();
  }, 'This has to be different');

  v.addMethod('fileSize', function (value, element, param) {
    return this.optional(element) || element.files[0].size <= param;
  }, 'This file it too large, allowed are ' + maxFileSize + ' MB');

  v.addMethod("signedInteger", function (value, element) {
    return /^-?\d+$/i.test(value);
  }, 'Please enter a valid integer.');

  $("#password-form").validate({
    rules: {
      password: {minlength: minimumPasswordLength, notEqual: "#password_old"},
      password2: {equalTo: "#password"},
    }
  });

  $('#user-form').validate({
    rules: {
      password: {minlength: minimumPasswordLength},
      password2: {equalTo: '#password'}
    },
    submitHandler: validateSubmitHandler,
  });

  $('#file-form').validate({
    rules: {
      file: {fileSize: maxFileSize * 1024 * 1024}
    },
  });

  $("form").on('click', '#generate-password', function () {
    charset = '123456789abcdefghjklmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ';
    random_password = '';
    for (var i = 0; i < minimumPasswordLength; i++) {
      index = Math.floor(Math.random() * (charset.length));
      random_password += charset[index];
    }
    $("#password").val(random_password);
    $("#password2").val(random_password);
  })

  // Adding a generic submit handler to form validation
  .each(function () {
    $(this).validate({
      errorClass: "error",
      submitHandler: validateSubmitHandler,
    });
  });

  // Add required to reference precision if reference is set
  ['keyup', 'change'].forEach((listener) => {
    $("[id^=reference_system_id]").on(listener, function () {
      const select = $(`#reference_system_precision_${this.id.split('_').pop()}`);
      if (!this.value?.length)
        select.removeClass('required');
      else
        select.addClass('required');
    });
  })

  $("div[id*='-modal']").on('shown.bs.modal', function () {
    $("input[id*='-tree-search']").focus();
    $("input[type='search']").focus();
  });

  $('.extend-icon').click((a) => {
    if (a.currentTarget.id === 'extend-form-icon') {
      $('#extend-form-icon').hide();
      $('#extend-map-icon').show();
      $('.col-xl-4').toggleClass("col-xl-4").toggleClass("col-xl-10");
      $('.col-xl-8').toggleClass("col-xl-8").toggleClass("col-xl-2");
      return;
    }
    $('#extend-form-icon').show();
    $('#extend-map-icon').hide();
    $('.col-xl-10').toggleClass("col-xl-10").toggleClass("col-xl-4");
    $('.col-xl-2').toggleClass("col-xl-2").toggleClass("col-xl-8");
  });

  $(".modal").on('shown.bs.modal', function () {
    $(`#${this.id} input`)?.get(0)?.focus()
  });

  initDuplicateNameCheck();

});

function initDuplicateNameCheck() {
  const inputs = document.querySelectorAll('input[data-duplicate-check-class]');
  if (!inputs.length) return;

  const instances = [];

  inputs.forEach((input) => {
    if (input.dataset.duplicateCheckBound) return;
    input.dataset.duplicateCheckBound = 'true';

    const container = input.parentElement;
    if (!container) return;

    const host = input.closest('.modal') || document.body;
    const bubble = document.createElement('div');
    bubble.className = 'duplicate-check-bubble';
    bubble.setAttribute('role', 'status');
    bubble.setAttribute('aria-live', 'polite');
    bubble.hidden = true;
    host.appendChild(bubble);

    const entityClass = input.dataset.duplicateCheckClass;
    const excludeId = input.dataset.excludeId || '';
    const MIN_SIDE_WIDTH = 260;
    const MAX_SIDE_WIDTH = 380;
    const MAX_BELOW_WIDTH = 420;
    const GAP = 10;
    const VIEWPORT_MARGIN = 12;

    let debounceTimer = null;
    let abortController = null;
    let requestCounter = 0;
    let lastQuery = '';
    let hasResults = false;
    let dismissedQuery = null;

    const positionBubble = () => {
      if (bubble.hidden) return;
      const rect = input.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) {
        bubble.hidden = true;
        return;
      }

      const spaceRight = window.innerWidth - rect.right - GAP - VIEWPORT_MARGIN;
      if (spaceRight >= MIN_SIDE_WIDTH) {
        bubble.classList.add('duplicate-check-bubble--right');
        bubble.classList.remove('duplicate-check-bubble--below-end');
        const width = Math.min(MAX_SIDE_WIDTH, spaceRight);
        bubble.style.width = `${width}px`;

        const left = rect.right + GAP;
        const bubbleHeight = bubble.offsetHeight || 0;
        let top = rect.top - 4;
        if (top + bubbleHeight > window.innerHeight - VIEWPORT_MARGIN) {
          top = Math.max(VIEWPORT_MARGIN, window.innerHeight - bubbleHeight - VIEWPORT_MARGIN);
        }
        top = Math.max(VIEWPORT_MARGIN, top);

        const inputCenterY = rect.top + rect.height / 2;
        const arrowTop = Math.max(
          14,
          Math.min(Math.max(14, bubbleHeight - 14), inputCenterY - top)
        );
        bubble.style.setProperty('--duplicate-arrow-top', `${arrowTop}px`);
        bubble.style.left = `${left}px`;
        bubble.style.top = `${top}px`;
      } else {
        bubble.classList.add('duplicate-check-bubble--below-end');
        bubble.classList.remove('duplicate-check-bubble--right');
        const width = Math.min(MAX_BELOW_WIDTH, window.innerWidth - VIEWPORT_MARGIN * 2);
        bubble.style.width = `${width}px`;
        const left = Math.max(
          VIEWPORT_MARGIN,
          Math.min(window.innerWidth - width - VIEWPORT_MARGIN, rect.right - width)
        );
        const top = rect.bottom + 8;
        bubble.style.left = `${left}px`;
        bubble.style.top = `${top}px`;
      }
    };

    const resetState = () => {
      clearTimeout(debounceTimer);
      if (abortController) {
        abortController.abort();
        abortController = null;
      }
      requestCounter++;
      lastQuery = '';
      hasResults = false;
      dismissedQuery = null;
      bubble.hidden = true;
      bubble.innerHTML = '';
    };

    const fetchDuplicateHtml = async (query, offset = 0) => {
      if (abortController) {
        abortController.abort();
      }
      abortController = new AbortController();
      const currentCounter = ++requestCounter;
      const params = new URLSearchParams({
        search: query,
        class_: entityClass,
        offset: String(offset),
        ...(excludeId ? { exclude_id: String(excludeId) } : {})
      });
      const response = await fetch(`/ajax/duplicate_check?${params.toString()}`, {
        credentials: 'same-origin',
        signal: abortController.signal
      });
      if (!response.ok) return null;
      const html = await response.text();
      if (currentCounter !== requestCounter || input.value.trim() !== query) {
        return null;
      }
      return html;
    };

    bubble.addEventListener('click', async (event) => {
      if (event.target.closest('.duplicate-check-close')) {
        event.stopPropagation();
        bubble.hidden = true;
        dismissedQuery = lastQuery;
        return;
      }

      const loadMoreBtn = event.target.closest('.duplicate-check-load-more');
      if (!loadMoreBtn || loadMoreBtn.disabled) return;
      event.preventDefault();
      event.stopPropagation();
      const originalText = loadMoreBtn.textContent;
      loadMoreBtn.disabled = true;
      loadMoreBtn.textContent = `${translate.inProgress}…`;
      try {
        const html = await fetchDuplicateHtml(
          lastQuery,
          loadMoreBtn.dataset.offset || '0'
        );
        if (html === null) return;
        loadMoreBtn.closest('.duplicate-check-footer')?.remove();
        if (html.trim()) {
          bubble
            .querySelector('.duplicate-check-list')
            ?.insertAdjacentHTML('beforeend', html);
        }
        positionBubble();
      } catch (err) {
        if (err.name !== 'AbortError') {
          loadMoreBtn.disabled = false;
          loadMoreBtn.textContent = originalText;
        }
      }
    });

    input.addEventListener('input', () => {
      const query = input.value.trim();
      if (query.length < 2) {
        resetState();
        return;
      }
      if (query !== dismissedQuery) {
        dismissedQuery = null;
      }
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(async () => {
        try {
          const html = await fetchDuplicateHtml(query, 0);
          if (html === null) return;
          lastQuery = query;
          if (!html.trim()) {
            hasResults = false;
            bubble.hidden = true;
            bubble.innerHTML = '';
            return;
          }
          hasResults = true;
          bubble.innerHTML = html;
          if (dismissedQuery !== query) {
            bubble.hidden = false;
            positionBubble();
          }
        } catch (err) {
          if (err.name !== 'AbortError') {
            bubble.hidden = true;
          }
        }
      }, 300);
    });

    input.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !bubble.hidden) {
        event.stopPropagation();
        bubble.hidden = true;
        dismissedQuery = lastQuery;
      }
    });

    input.addEventListener('focus', () => {
      if (input.value.trim() === lastQuery && hasResults && dismissedQuery !== lastQuery) {
        bubble.hidden = false;
        positionBubble();
      }
    });

    instances.push({ input, container, bubble, positionBubble });
  });

  if (instances.length) {
    document.addEventListener('mousedown', (event) => {
      instances.forEach(({ input, container, bubble }) => {
        if (
          !bubble.hidden
          && event.target !== input
          && !container.contains(event.target)
          && !bubble.contains(event.target)
        ) {
          bubble.hidden = true;
        }
      });
    });

    const repositionAll = (event) => {
      if (event?.target?.classList?.contains('duplicate-check-list')) return;
      instances.forEach(({ bubble, positionBubble }) => {
        if (!bubble.hidden) {
          positionBubble();
        }
      });
    };

    window.addEventListener('resize', repositionAll, { passive: true });
    window.addEventListener('scroll', repositionAll, true);

    $(document).on('hidden.bs.modal', '.modal', function () {
      this.querySelectorAll('.duplicate-check-bubble').forEach((bubble) => {
        bubble.hidden = true;
      });
    });
  }
}

const closableBadge = (name, onclick = '') => `
  <div onclick="event.stopPropagation()" class="badge col-auto bg-gray">
    <div class="d-flex align-items-center">
      <span class="text-black">${name}</span>
      <button
      onclick="${onclick}"
      type="button"
      class="btn-close p-0 ms-1"
      aria-label="Close"
      ></button>
    </div>
  </div>`
