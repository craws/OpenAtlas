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

  /* Show and hide function for date input fields */
  const dateSwitcher = $("#date-switcher");
  const dateSwitch = $(".date-switch");
  const beginYearFrom = $('#begin_year_from');
  const beginYearTo = $('#begin_year_to');
  const endYearFrom = $('#end_year_from');
  const endYearTo = $('#end_year_to');

  function isLeapYear(yearInt) {
    const astroYear = yearInt > 0 ? yearInt : yearInt + 1;
    if (astroYear % 400 === 0) return true;
    if (astroYear % 100 === 0) return false;
    return astroYear % 4 === 0;
  }

  function getLastDayOfMonth(yearInt, monthInt) {
    const daysInMonths = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (monthInt < 1 || monthInt > 12) return 31;
    if (monthInt === 2 && isLeapYear(yearInt)) return 29;
    return daysInMonths[monthInt];
  }

  function readBoundaryRaw(mode, bound) {
    return {
      Y: ($(`#${mode}_year_${bound}`).val() || '').trim(),
      M: ($(`#${mode}_month_${bound}`).val() || '').trim(),
      D: ($(`#${mode}_day_${bound}`).val() || '').trim(),
      h: ($(`#${mode}_hour_${bound}`).val() || '').trim(),
      m: ($(`#${mode}_minute_${bound}`).val() || '').trim(),
      s: ($(`#${mode}_second_${bound}`).val() || '').trim()
    };
  }

  function writeBoundaryRaw(mode, bound, raw) {
    $(`#${mode}_year_${bound}`).val(raw.Y || '');
    $(`#${mode}_month_${bound}`).val(raw.M || '');
    $(`#${mode}_day_${bound}`).val(raw.D || '');
    if ($(`#${mode}_hour_${bound}`).length) {
      $(`#${mode}_hour_${bound}`).val(raw.h || '');
      $(`#${mode}_minute_${bound}`).val(raw.m || '');
      $(`#${mode}_second_${bound}`).val(raw.s || '');
    }
  }

  function resolveBoundary(raw, isToDate = false) {
    const yStr = (raw.Y || '').trim();
    const mStr = (raw.M || '').trim();
    const dStr = (raw.D || '').trim();
    const hStr = (raw.h || '').trim();
    const minStr = (raw.m || '').trim();
    const sStr = (raw.s || '').trim();

    if (!yStr && !mStr && !dStr && !hStr && !minStr && !sStr) {
      return { empty: true, valid: true, hasCustomTime: false };
    }
    if (!yStr) {
      return { empty: false, valid: false };
    }

    const yearNum = Number(yStr);
    if (!/^-?\d+$/.test(yStr) || !Number.isInteger(yearNum) || yearNum === 0 || yearNum < -4713 || yearNum > 9999) {
      return { empty: false, valid: false };
    }

    let monthNum = isToDate ? 12 : 1;
    if (mStr !== '') {
      monthNum = Number(mStr);
      if (!/^\d+$/.test(mStr) || monthNum < 1 || monthNum > 12) {
        return { empty: false, valid: false };
      }
    }

    const maxDay = getLastDayOfMonth(yearNum, monthNum);
    let dayNum = isToDate ? maxDay : 1;
    if (dStr !== '') {
      if (mStr === '') {
        return { empty: false, valid: false };
      }
      dayNum = Number(dStr);
      if (!/^\d+$/.test(dStr) || dayNum < 1 || dayNum > maxDay) {
        return { empty: false, valid: false };
      }
    }

    let hourNum = isToDate ? 23 : 0;
    let minNum = isToDate ? 59 : 0;
    let secNum = isToDate ? 59 : 0;
    let hasCustomTime = false;

    if (hStr !== '' || minStr !== '' || sStr !== '') {
      if ((sStr !== '' && minStr === '') || (minStr !== '' && hStr === '')) {
        return { empty: false, valid: false };
      }
      hourNum = hStr !== '' ? Number(hStr) : 0;
      minNum = minStr !== '' ? Number(minStr) : 0;
      secNum = sStr !== '' ? Number(sStr) : 0;
      if (
        (hStr !== '' && !/^\d+$/.test(hStr)) ||
        (minStr !== '' && !/^\d+$/.test(minStr)) ||
        (sStr !== '' && !/^\d+$/.test(sStr)) ||
        hourNum < 0 || hourNum > 23 ||
        minNum < 0 || minNum > 59 ||
        secNum < 0 || secNum > 59
      ) {
        return { empty: false, valid: false };
      }
      if (isToDate) {
        hasCustomTime = !(hourNum === 23 && minNum === 59 && secNum === 59);
      } else {
        hasCustomTime = !(hourNum === 0 && minNum === 0 && secNum === 0);
      }
    }

    const isBC = yearNum < 0;
    const absYear = Math.abs(yearNum);
    const padY = String(absYear).padStart(4, '0');
    const padM = String(monthNum).padStart(2, '0');
    const padD = String(dayNum).padStart(2, '0');
    const padH = String(hourNum).padStart(2, '0');
    const padMin = String(minNum).padStart(2, '0');
    const padS = String(secNum).padStart(2, '0');
    const bcSuffix = isBC ? ' BC' : '';

    const astroYear = isBC ? yearNum + 1 : yearNum;
    const sortValue =
      (astroYear * 10000000000) +
      (monthNum * 100000000) +
      (dayNum * 1000000) +
      (hourNum * 10000) +
      (minNum * 100) +
      secNum;

    return {
      empty: false,
      valid: true,
      yearNum,
      monthNum,
      dayNum,
      hasCustomTime,
      isoShort: `${padY}-${padM}-${padD}${bcSuffix}`,
      timeStr: `${padH}:${padMin}:${padS}`,
      sortValue
    };
  }

  function analyzePairSemantics(mode) {
    const fromRaw = readBoundaryRaw(mode, 'from');
    const toRaw = readBoundaryRaw(mode, 'to');
    const rFrom = resolveBoundary(fromRaw, false);
    const rTo = resolveBoundary(toRaw, true);

    if (rFrom.empty && rTo.empty) {
      return {
        mode: 'empty',
        isStandard: true,
        simpleY: '',
        simpleM: '',
        simpleD: '',
        label: translate.date_no_date || 'No date set'
      };
    }
    if (!rFrom.valid || !rTo.valid) {
      return {
        mode: 'invalid',
        isStandard: false,
        simpleY: '',
        simpleM: '',
        simpleD: '',
        label: translate.date_invalid || 'Invalid date input'
      };
    }
    if (!rFrom.empty && rTo.empty) {
      const boundStr = rFrom.hasCustomTime ? `${rFrom.isoShort} ${rFrom.timeStr}` : rFrom.isoShort;
      return {
        mode: 'after',
        isStandard: false,
        simpleY: '',
        simpleM: '',
        simpleD: '',
        label: `${translate.date_earliest_bound || 'Earliest bound'} (${translate.date_from || 'from'} ${boundStr} ${translate.date_onwards || 'onwards'})`
      };
    }
    if (rFrom.empty && !rTo.empty) {
      const boundStr = rTo.hasCustomTime ? `${rTo.isoShort} ${rTo.timeStr}` : rTo.isoShort;
      return {
        mode: 'before',
        isStandard: false,
        simpleY: '',
        simpleM: '',
        simpleD: '',
        label: `${translate.date_latest_bound || 'Latest bound'} (${translate.date_up_to || 'up to'} ${boundStr})`
      };
    }

    if (rFrom.sortValue > rTo.sortValue) {
      return {
        mode: 'invalid',
        isStandard: false,
        simpleY: '',
        simpleM: '',
        simpleD: '',
        label: translate.date_invalid || 'Invalid date input'
      };
    }

    if (!rFrom.hasCustomTime && !rTo.hasCustomTime) {
      if (rFrom.yearNum === rTo.yearNum && rFrom.monthNum === rTo.monthNum && rFrom.dayNum === rTo.dayNum) {
        return {
          mode: 'exact',
          isStandard: true,
          simpleY: String(rFrom.yearNum),
          simpleM: String(rFrom.monthNum),
          simpleD: String(rFrom.dayNum),
          label: `${translate.date_exact || 'Exact date'}: ${rFrom.isoShort} (00:00:00 – 23:59:59)`
        };
      }
      if (rFrom.yearNum === rTo.yearNum) {
        if (rFrom.monthNum === 1 && rFrom.dayNum === 1 && rTo.monthNum === 12 && rTo.dayNum === 31) {
          return {
            mode: 'exact',
            isStandard: true,
            simpleY: String(rFrom.yearNum),
            simpleM: '',
            simpleD: '',
            label: `${translate.date_full_year || 'Full year'}: ${rFrom.isoShort} ${translate.date_to || 'to'} ${rTo.isoShort}`
          };
        }
        const lastDay = getLastDayOfMonth(rFrom.yearNum, rFrom.monthNum);
        if (rFrom.monthNum === rTo.monthNum && rFrom.dayNum === 1 && rTo.dayNum === lastDay) {
          return {
            mode: 'exact',
            isStandard: true,
            simpleY: String(rFrom.yearNum),
            simpleM: String(rFrom.monthNum),
            simpleD: '',
            label: `${translate.date_full_month || 'Full month'}: ${rFrom.isoShort} ${translate.date_to || 'to'} ${rTo.isoShort}`
          };
        }
      }
    }

    const fromStr = rFrom.hasCustomTime ? `${rFrom.isoShort} ${rFrom.timeStr}` : rFrom.isoShort;
    const toStr = rTo.hasCustomTime ? `${rTo.isoShort} ${rTo.timeStr}` : rTo.isoShort;
    return {
      mode: 'between',
      isStandard: false,
      simpleY: '',
      simpleM: '',
      simpleD: '',
      label: `${translate.date_timespan || 'Timespan'}: ${translate.date_between || 'between'} ${fromStr} ${translate.date_and || 'and'} ${toStr}`
    };
  }

  function expandSimpleToPair(simpleObj) {
    const yStr = (simpleObj.Y || '').trim();
    const mStr = (simpleObj.M || '').trim();
    const dStr = (simpleObj.D || '').trim();
    const emptyRaw = () => ({ Y: '', M: '', D: '', h: '', m: '', s: '' });

    if (!yStr && !mStr && !dStr) {
      return { from: emptyRaw(), to: emptyRaw() };
    }

    const yearNum = Number(yStr);
    const validYear = /^-?\d+$/.test(yStr) && Number.isInteger(yearNum) && yearNum !== 0;

    if (yStr && mStr && dStr) {
      return {
        from: { Y: yStr, M: mStr, D: dStr, h: '', m: '', s: '' },
        to: { Y: yStr, M: mStr, D: dStr, h: '', m: '', s: '' }
      };
    }
    if (yStr && mStr && !dStr) {
      const monthNum = Number(mStr);
      const lastDay = (validYear && monthNum >= 1 && monthNum <= 12)
        ? String(getLastDayOfMonth(yearNum, monthNum))
        : '31';
      return {
        from: { Y: yStr, M: mStr, D: '1', h: '', m: '', s: '' },
        to: { Y: yStr, M: mStr, D: lastDay, h: '', m: '', s: '' }
      };
    }
    if (yStr && !mStr && !dStr) {
      return {
        from: { Y: yStr, M: '1', D: '1', h: '', m: '', s: '' },
        to: { Y: yStr, M: '12', D: '31', h: '', m: '', s: '' }
      };
    }
    return {
      from: { Y: yStr, M: mStr, D: dStr, h: '', m: '', s: '' },
      to: { Y: yStr, M: mStr, D: dStr, h: '', m: '', s: '' }
    };
  }

  function updateDateFeedback() {
    if (!beginYearFrom.length) return;
    ['begin', 'end'].forEach((mode) => {
      const sem = analyzePairSemantics(mode);
      $(`[data-feedback-pair="${mode}"]`).each(function () {
        $(this).text(sem.label);
        $(this).toggleClass('text-danger fw-semibold', sem.mode === 'invalid');
        $(this).toggleClass('text-muted', sem.mode !== 'invalid');
      });
    });
  }

  function syncSimpleViewFromAdvanced() {
    if (!beginYearFrom.length) return;
    ['begin', 'end'].forEach((mode) => {
      const sem = analyzePairSemantics(mode);
      const inputs = $(`input[data-simple="${mode}"]`);
      const msgBox = $(`#simple-${mode}-disabled-msg`);
      if (sem.isStandard) {
        inputs.prop('disabled', false);
        $(`#simple_${mode}_year`).val(sem.simpleY);
        $(`#simple_${mode}_month`).val(sem.simpleM);
        $(`#simple_${mode}_day`).val(sem.simpleD);
        msgBox.addClass('d-none').removeClass('d-flex');
      } else {
        inputs.val('').prop('disabled', true);
        msgBox.find('.simple-disabled-text').text(
          `${translate.date_complex_disabled || 'Complex date set in Advanced View'}: ${sem.label}`
        );
        msgBox.removeClass('d-none').addClass('d-flex');
      }
      const commentVal = $(`#${mode}_comment`).val() || '';
      $(`input[data-simple-comment="${mode}_comment"]`).val(commentVal);
    });
  }

  let isDateSectionOpen = false;
  let isAdvancedDateView = false;

  function renderDateVisibility() {
    if (!beginYearFrom.length) return;
    if (!isDateSectionOpen) {
      dateSwitch.addClass('d-none');
      dateSwitcher.attr("aria-pressed", false);
      return;
    }
    dateSwitcher.attr("aria-pressed", true);
    $('.date-tab-row').removeClass('d-none');
    $('.date-mode-simple').toggleClass('d-none', isAdvancedDateView);
    $('.date-mode-advanced').toggleClass('d-none', !isAdvancedDateView);
    $('#date-tab-simple').toggleClass('active fw-bold', !isAdvancedDateView);
    $('#date-tab-advanced').toggleClass('active fw-bold', isAdvancedDateView);
  }

  function toggleDateFieldVisible(el) {
    isDateSectionOpen = !isDateSectionOpen;
    renderDateVisibility();
    $(el).text(function (i, text) {
      return $.trim(text) === translate.show ? translate.hide : translate.show;
    });
  }

  if (beginYearFrom.length) {
    const hasDateValue =
      beginYearFrom.val() !== '' ||
      beginYearTo.val() !== '' ||
      endYearFrom.val() !== '' ||
      endYearTo.val() !== '';
    const hasDateError = $('.date-switch .error').length > 0;
    isDateSectionOpen = hasDateValue || hasDateError;

    const bSemInit = analyzePairSemantics('begin');
    const eSemInit = analyzePairSemantics('end');
    isAdvancedDateView = !(bSemInit.isStandard && eSemInit.isStandard) || hasDateError;

    syncSimpleViewFromAdvanced();
    updateDateFeedback();
    renderDateVisibility();

    dateSwitcher.click(function () {
      toggleDateFieldVisible(this);
    });
    dateSwitcher.on('keydown', function (event) {
      if (!onActivateKeyInput(event)) return;
      toggleDateFieldVisible(this);
    });

    $('.date-mode-btn').on('click', function () {
      const targetAdv = $(this).attr('data-adv') === 'true';
      if (!targetAdv) {
        syncSimpleViewFromAdvanced();
      }
      isAdvancedDateView = targetAdv;
      renderDateVisibility();
      updateDateFeedback();
    });

    $('input[data-simple]').on('input', function () {
      const mode = $(this).attr('data-simple');
      const simpleObj = {
        Y: $(`#simple_${mode}_year`).val() || '',
        M: $(`#simple_${mode}_month`).val() || '',
        D: $(`#simple_${mode}_day`).val() || ''
      };
      const expanded = expandSimpleToPair(simpleObj);
      writeBoundaryRaw(mode, 'from', expanded.from);
      writeBoundaryRaw(mode, 'to', expanded.to);
      updateDateFeedback();
    });

    $('.date-mode-advanced input').on('input', function () {
      updateDateFeedback();
    });

    $('input[data-simple-comment]').on('input', function () {
      const targetId = $(this).attr('data-simple-comment');
      $(`#${targetId}`).val($(this).val());
    });

    $('#begin_comment, #end_comment').on('input', function () {
      const id = $(this).attr('id');
      $(`input[data-simple-comment="${id}"]`).val($(this).val());
    });
  }

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
  // Enable validation for hidden fields
  let v = $.validator;
  v.setDefaults({
    ignore: [],
  });

  v.addClassRules({
    year: {number: true, min: -4713, max: 9999},
    month: {digits: true, min: 1, max: 12},
    day: {digits: true, min: 1, max: 31},
    hour: {digits: true, min: 0, max: 23},
    minute: {digits: true, min: 0, max: 59},
    second: {digits: true, min: 0, max: 59},
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
      errorClass: "d-block error",
      invalidHandler: function (event, validator) {
        if (validator.errorList.some((err) => $(err.element).closest('.date-switch').length > 0)) {
          isDateSectionOpen = true;
          isAdvancedDateView = true;
          dateSwitcher.text(translate.hide);
          renderDateVisibility();
        }
      },
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

});

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
