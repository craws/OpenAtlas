document.addEventListener('DOMContentLoaded', () => {
  const dateSwitcher = document.getElementById('date-switcher');
  const dateSwitchElements = document.querySelectorAll('.date-switch');
  const beginYearFrom = document.getElementById('begin_year_from');

  /* =======================================================================
   * 1. Calendar and Leap Year Calculation Helpers
   * ======================================================================= */

  function isLeapYear(yearInt) {
    const year = yearInt > 0 ? yearInt : yearInt + 1;
    if (year % 400 === 0) return true;
    if (year % 100 === 0) return false;
    return year % 4 === 0;
  }

  function getLastDayOfMonth(yearInt, monthInt) {
    const daysInMonths = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (monthInt < 1 || monthInt > 12) return 31;
    if (monthInt === 2 && isLeapYear(yearInt)) return 29;
    return daysInMonths[monthInt];
  }

  /* =======================================================================
   * 2. DOM Input/Output Helpers for Date Boundaries
   * ======================================================================= */

  function getInputValue(id) {
    const el = document.getElementById(id);
    return el ? (el.value || '').trim() : '';
  }

  function setInputValue(id, value) {
    const el = document.getElementById(id);
    if (el) {
      el.value = value || '';
    }
  }

  function isBadNumberInput(id) {
    const el = document.getElementById(id);
    return Boolean(el && el.validity && el.validity.badInput);
  }

  function blockInvalidNumberChars(input) {
    const allowMinus = input.classList.contains('year');
    input.addEventListener('keydown', (event) => {
      if (event.ctrlKey || event.metaKey || event.altKey) return;
      if (['e', 'E', '+', '.', ','].includes(event.key) || (!allowMinus && event.key === '-')) {
        event.preventDefault();
      }
    });
    input.addEventListener('paste', (event) => {
      const text = (event.clipboardData || window.clipboardData)?.getData('text') || '';
      const regex = allowMinus ? /^-?\d*$/ : /^\d*$/;
      if (!regex.test(text.trim())) {
        event.preventDefault();
      }
    });
  }

  function readBoundaryRaw(mode, bound) {
    const badParts = ['Y', 'M', 'D', 'h', 'm', 's'].filter((part) =>
      isBadNumberInput(`${mode}_${PART_TO_FIELD[part]}_${bound}`)
    );
    if (!isAdvancedDateView) {
      ['Y', 'M', 'D'].forEach((part) => {
        const simpleId = `simple_${mode}_${PART_TO_FIELD[part]}`;
        const simpleEl = document.getElementById(simpleId);
        if (simpleEl && !simpleEl.disabled && isBadNumberInput(simpleId) && !badParts.includes(part)) {
          badParts.push(part);
        }
      });
    }
    return {
      Y: getInputValue(`${mode}_year_${bound}`),
      M: getInputValue(`${mode}_month_${bound}`),
      D: getInputValue(`${mode}_day_${bound}`),
      h: getInputValue(`${mode}_hour_${bound}`),
      m: getInputValue(`${mode}_minute_${bound}`),
      s: getInputValue(`${mode}_second_${bound}`),
      badParts
    };
  }

  function writeBoundaryRaw(mode, bound, raw) {
    setInputValue(`${mode}_year_${bound}`, raw.Y);
    setInputValue(`${mode}_month_${bound}`, raw.M);
    setInputValue(`${mode}_day_${bound}`, raw.D);
    setInputValue(`${mode}_hour_${bound}`, raw.h);
    setInputValue(`${mode}_minute_${bound}`, raw.m);
    setInputValue(`${mode}_second_${bound}`, raw.s);
  }

  /* =======================================================================
   * 3. Validation, Check, and Normalization Functions
   * ======================================================================= */

  const PART_TO_FIELD = {
    Y: 'year',
    M: 'month',
    D: 'day',
    h: 'hour',
    m: 'minute',
    s: 'second'
  };

  function resolveBoundary(raw, isToDate = false) {
    const yStr = (raw.Y || '').trim();
    const mStr = (raw.M || '').trim();
    const dStr = (raw.D || '').trim();
    const hStr = (raw.h || '').trim();
    const minStr = (raw.m || '').trim();
    const sStr = (raw.s || '').trim();
    const badParts = Array.isArray(raw.badParts) ? raw.badParts : [];

    if (!yStr && !mStr && !dStr && !hStr && !minStr && !sStr && badParts.length === 0) {
      return { empty: true, valid: true, invalidParts: [], hasCustomTime: false };
    }

    const invalidParts = [...badParts];
    let yearValid = false;
    let yearNum = 0;
    if (!yStr) {
      if (!invalidParts.includes('Y')) invalidParts.push('Y');
    } else {
      yearNum = Number(yStr);
      if (!/^-?\d+$/.test(yStr) || !Number.isInteger(yearNum) || yearNum === 0 || yearNum < -4713 || yearNum > 9999) {
        if (!invalidParts.includes('Y')) invalidParts.push('Y');
      } else {
        yearValid = true;
      }
    }

    let monthValid = !invalidParts.includes('M');
    let monthNum = isToDate ? 12 : 1;
    if (mStr !== '') {
      monthNum = Number(mStr);
      if (!/^\d+$/.test(mStr) || monthNum < 1 || monthNum > 12) {
        if (!invalidParts.includes('M')) invalidParts.push('M');
        monthValid = false;
      }
    }

    const maxDay = (yearValid && monthValid) ? getLastDayOfMonth(yearNum, monthNum) : 31;
    let dayNum = isToDate ? maxDay : 1;
    if (dStr !== '' || invalidParts.includes('D')) {
      if (mStr === '' && !invalidParts.includes('M')) {
        invalidParts.push('M');
      }
      if (dStr !== '') {
        dayNum = Number(dStr);
        if (!/^\d+$/.test(dStr) || dayNum < 1 || dayNum > maxDay) {
          if (!invalidParts.includes('D')) invalidParts.push('D');
        }
      }
    }

    let hourNum = isToDate ? 23 : 0;
    let minNum = isToDate ? 59 : 0;
    let secNum = isToDate ? 59 : 0;
    let hasCustomTime = false;

    if (
      hStr !== '' || minStr !== '' || sStr !== '' ||
      invalidParts.includes('h') || invalidParts.includes('m') || invalidParts.includes('s')
    ) {
      if ((minStr !== '' || invalidParts.includes('m')) && hStr === '' && !invalidParts.includes('h')) {
        invalidParts.push('h');
      }
      if ((sStr !== '' || invalidParts.includes('s')) && minStr === '' && !invalidParts.includes('m')) {
        invalidParts.push('m');
      }
      if (hStr !== '') {
        hourNum = Number(hStr);
        if (!/^\d+$/.test(hStr) || hourNum < 0 || hourNum > 23) {
          if (!invalidParts.includes('h')) invalidParts.push('h');
        }
      }
      if (minStr !== '') {
        minNum = Number(minStr);
        if (!/^\d+$/.test(minStr) || minNum < 0 || minNum > 59) {
          if (!invalidParts.includes('m')) invalidParts.push('m');
        }
      }
      if (sStr !== '') {
        secNum = Number(sStr);
        if (!/^\d+$/.test(sStr) || secNum < 0 || secNum > 59) {
          if (!invalidParts.includes('s')) invalidParts.push('s');
        }
      }
      if (isToDate) {
        hasCustomTime = !(hourNum === 23 && minNum === 59 && secNum === 59);
      } else {
        hasCustomTime = !(hourNum === 0 && minNum === 0 && secNum === 0);
      }
    }

    if (invalidParts.length > 0) {
      return {
        empty: false,
        valid: false,
        invalidParts,
        error: translate.date_invalid || 'Not a valid date'
      };
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

    const sortValue =
      (yearNum * 10000000000) +
      (monthNum * 100000000) +
      (dayNum * 1000000) +
      (hourNum * 10000) +
      (minNum * 100) +
      secNum;

    return {
      empty: false,
      valid: true,
      invalidParts: [],
      yearNum,
      monthNum,
      dayNum,
      hasCustomTime,
      isoShort: `${padY}-${padM}-${padD}${bcSuffix}`,
      timeStr: `${padH}:${padMin}:${padS}`,
      sortValue
    };
  }

  /* =======================================================================
   * 4. Analyzes a begin/end and expands simple date
    * ====================================================================== */

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
        rFrom,
        rTo,
        invalidFields: [],
        label: translate.date_no_date || 'No date set'
      };
    }
    if (!rFrom.valid || !rTo.valid) {
      const invalidFields = [];
      if (!rFrom.valid) {
        rFrom.invalidParts.forEach((part) => {
          const fieldName = PART_TO_FIELD[part];
          invalidFields.push(`${mode}_${fieldName}_from`);
          if (part === 'Y' || part === 'M' || part === 'D') {
            invalidFields.push(`simple_${mode}_${fieldName}`);
          }
        });
      }
      if (!rTo.valid) {
        rTo.invalidParts.forEach((part) => {
          const fieldName = PART_TO_FIELD[part];
          invalidFields.push(`${mode}_${fieldName}_to`);
          if (part === 'Y' || part === 'M' || part === 'D') {
            invalidFields.push(`simple_${mode}_${fieldName}`);
          }
        });
      }
      return {
        mode: 'invalid',
        isStandard: false,
        simpleY: '',
        simpleM: '',
        simpleD: '',
        rFrom,
        rTo,
        invalidFields,
        label: translate.date_invalid || 'Not a valid date'
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
        rFrom,
        rTo,
        invalidFields: [],
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
        rFrom,
        rTo,
        invalidFields: [],
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
        rFrom,
        rTo,
        invalidFields: [`${mode}_year_from`, `${mode}_year_to`],
        label: translate.date_first_after_second || 'First date cannot be after second.'
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
          rFrom,
          rTo,
          invalidFields: [],
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
            rFrom,
            rTo,
            invalidFields: [],
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
            rFrom,
            rTo,
            invalidFields: [],
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
      rFrom,
      rTo,
      invalidFields: [],
      label: `${translate.date_timespan || 'Timespan'}: ${translate.date_between || 'between'} ${fromStr} ${translate.date_and || 'and'} ${toStr}`
    };
  }

  function analyzeAllDates() {
    const begin = analyzePairSemantics('begin');
    const end = analyzePairSemantics('end');

    if (begin.mode !== 'invalid' && end.mode !== 'invalid') {
      const beginFrom = !begin.rFrom.empty ? begin.rFrom.sortValue : null;
      const beginTo = !begin.rTo.empty ? begin.rTo.sortValue : null;
      const endFrom = !end.rFrom.empty ? end.rFrom.sortValue : null;
      const endTo = !end.rTo.empty ? end.rTo.sortValue : null;
      const beginVal = beginFrom !== null ? beginFrom : beginTo;
      const endVal = endTo !== null ? endTo : endFrom;

      if (
        (beginFrom !== null && endFrom !== null && beginFrom > endFrom) ||
        (beginTo !== null && endTo !== null && beginTo > endTo) ||
        (beginVal !== null && endVal !== null && beginVal > endVal)
      ) {
        begin.mode = 'invalid';
        begin.label = translate.date_begin_after_end || 'Begin dates cannot start after end dates.';
        const targetYearField = beginFrom !== null ? 'begin_year_from' : 'begin_year_to';
        begin.invalidFields = [targetYearField, 'simple_begin_year'];
      }
    }

    return { begin, end };
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
        from: { Y: yStr, M: mStr, D: dStr, h: '00', m: '00', s: '00' },
        to: { Y: yStr, M: mStr, D: dStr, h: '23', m: '59', s: '59' }
      };
    }
    if (yStr && mStr && !dStr) {
      const monthNum = Number(mStr);
      const lastDay = (validYear && monthNum >= 1 && monthNum <= 12)
        ? String(getLastDayOfMonth(yearNum, monthNum))
        : '31';
      return {
        from: { Y: yStr, M: mStr, D: '1', h: '00', m: '00', s: '00' },
        to: { Y: yStr, M: mStr, D: lastDay, h: '23', m: '59', s: '59' }
      };
    }
    if (yStr && !mStr && !dStr) {
      return {
        from: { Y: yStr, M: '1', D: '1', h: '00', m: '00', s: '00' },
        to: { Y: yStr, M: '12', D: '31', h: '23', m: '59', s: '59' }
      };
    }
    return {
      from: { Y: yStr, M: mStr, D: dStr, h: '00', m: '00', s: '00' },
      to: { Y: yStr, M: mStr, D: dStr, h: '23', m: '59', s: '59' }
    };
  }

  /* =======================================================================
   * 5. UI Elements
   * ======================================================================= */

  function updateDateFeedback() {
    if (!beginYearFrom) return;
    const analysis = analyzeAllDates();

    document.querySelectorAll('.date-switch input.error').forEach((input) => {
      input.classList.remove('error');
    });

    let hasAnyError = false;
    ['begin', 'end'].forEach((mode) => {
      const sem = analysis[mode];
      const isInvalid = sem.mode === 'invalid';
      if (isInvalid) {
        hasAnyError = true;
        sem.invalidFields.forEach((fieldId) => {
          const el = document.getElementById(fieldId);
          if (el && !el.disabled) {
            el.classList.add('error');
          }
        });
      }
      document.querySelectorAll(`[data-feedback-pair="${mode}"]`).forEach((el) => {
        el.textContent = sem.label;
        el.classList.toggle('text-danger', isInvalid);
        el.classList.toggle('fw-semibold', isInvalid);
        el.classList.toggle('text-muted', !isInvalid);
      });
    });

    const form = beginYearFrom.closest('form');
    if (form) {
      form.dataset.dateInvalid = hasAnyError ? 'true' : 'false';
    }
  }

  function syncSimpleViewFromAdvanced() {
    if (!beginYearFrom) return;
    ['begin', 'end'].forEach((mode) => {
      const sem = analyzePairSemantics(mode);
      const inputs = document.querySelectorAll(`input[data-simple="${mode}"]`);
      const msgBox = document.getElementById(`simple-${mode}-disabled-msg`);
      if (sem.isStandard) {
        inputs.forEach((input) => {
          input.disabled = false;
        });
        setInputValue(`simple_${mode}_year`, sem.simpleY);
        setInputValue(`simple_${mode}_month`, sem.simpleM);
        setInputValue(`simple_${mode}_day`, sem.simpleD);
        if (msgBox) {
          msgBox.classList.add('d-none');
          msgBox.classList.remove('d-flex');
        }
      } else {
        inputs.forEach((input) => {
          input.value = '';
          input.disabled = true;
        });
        if (msgBox) {
          const msgText = msgBox.querySelector('.simple-disabled-text');
          if (msgText) {
            msgText.textContent =
              `${translate.date_complex_disabled || 'Complex date set in Advanced View'}: ${sem.label}`;
          }
          msgBox.classList.remove('d-none');
          msgBox.classList.add('d-flex');
        }
      }
      const commentVal = getInputValue(`${mode}_comment`);
      document.querySelectorAll(`input[data-simple-comment="${mode}_comment"]`).forEach((input) => {
        input.value = commentVal;
      });
    });
  }

  let isDateSectionOpen = false;
  let isAdvancedDateView = false;

  function renderDateVisibility() {
    if (!beginYearFrom) return;
    if (!isDateSectionOpen) {
      dateSwitchElements.forEach((el) => el.classList.add('d-none'));
      if (dateSwitcher) {
        dateSwitcher.setAttribute('aria-pressed', 'false');
      }
      return;
    }
    if (dateSwitcher) {
      dateSwitcher.setAttribute('aria-pressed', 'true');
    }
    document.querySelectorAll('.date-tab-row').forEach((el) => el.classList.remove('d-none'));
    document.querySelectorAll('.date-mode-simple').forEach((el) => {
      el.classList.toggle('d-none', isAdvancedDateView);
    });
    document.querySelectorAll('.date-mode-advanced').forEach((el) => {
      el.classList.toggle('d-none', !isAdvancedDateView);
    });

    const tabSimple = document.getElementById('date-tab-simple');
    if (tabSimple) {
      tabSimple.classList.toggle('active', !isAdvancedDateView);
      tabSimple.classList.toggle('fw-bold', !isAdvancedDateView);
    }
    const tabAdvanced = document.getElementById('date-tab-advanced');
    if (tabAdvanced) {
      tabAdvanced.classList.toggle('active', isAdvancedDateView);
      tabAdvanced.classList.toggle('fw-bold', isAdvancedDateView);
    }
  }

  function toggleDateFieldVisible(el) {
    isDateSectionOpen = !isDateSectionOpen;
    renderDateVisibility();
    if (el) {
      el.textContent = (el.textContent || '').trim() === translate.show ? translate.hide : translate.show;
    }
  }

  /* =======================================================================
   * 6. Initialization and Event Binding
   * ======================================================================= */

  if (beginYearFrom) {
    const bSemInit = analyzePairSemantics('begin');
    const eSemInit = analyzePairSemantics('end');
    const hasDateError = document.querySelector('.date-switch .error') !== null;
    isDateSectionOpen = bSemInit.mode !== 'empty' || eSemInit.mode !== 'empty' || hasDateError;
    isAdvancedDateView = !(bSemInit.isStandard && eSemInit.isStandard) || hasDateError;

    syncSimpleViewFromAdvanced();
    updateDateFeedback();
    renderDateVisibility();

    if (dateSwitcher) {
      dateSwitcher.addEventListener('click', function () {
        toggleDateFieldVisible(this);
      });
      dateSwitcher.addEventListener('keydown', function (event) {
        if (!onActivateKeyInput(event)) return;
        toggleDateFieldVisible(this);
      });
    }

    document.querySelectorAll('.date-mode-btn').forEach((btn) => {
      btn.addEventListener('click', function () {
        const targetAdv = this.getAttribute('data-adv') === 'true';
        if (!targetAdv) {
          syncSimpleViewFromAdvanced();
        }
        isAdvancedDateView = targetAdv;
        renderDateVisibility();
        updateDateFeedback();
      });
    });

    document.querySelectorAll('input[data-simple]').forEach((input) => {
      blockInvalidNumberChars(input);
      input.addEventListener('input', function () {
        const mode = this.getAttribute('data-simple');
        const simpleObj = {
          Y: getInputValue(`simple_${mode}_year`),
          M: getInputValue(`simple_${mode}_month`),
          D: getInputValue(`simple_${mode}_day`)
        };
        const expanded = expandSimpleToPair(simpleObj);
        writeBoundaryRaw(mode, 'from', expanded.from);
        writeBoundaryRaw(mode, 'to', expanded.to);
        updateDateFeedback();
      });
    });

    document.querySelectorAll('.date-mode-advanced input').forEach((input) => {
      if (input.type === 'number') {
        blockInvalidNumberChars(input);
      }
      input.addEventListener('input', () => {
        updateDateFeedback();
      });
    });

    document.querySelectorAll('input[data-simple-comment]').forEach((input) => {
      input.addEventListener('input', function () {
        const targetId = this.getAttribute('data-simple-comment');
        setInputValue(targetId, this.value);
      });
    });

    ['begin_comment', 'end_comment'].forEach((id) => {
      const commentInput = document.getElementById(id);
      if (commentInput) {
        commentInput.addEventListener('input', function () {
          document.querySelectorAll(`input[data-simple-comment="${id}"]`).forEach((simpleComment) => {
            simpleComment.value = this.value;
          });
        });
      }
    });

    /* =====================================================================
     * 7. Form Validation
     * ===================================================================== */

    document.querySelectorAll('form').forEach((form) => {
      form.addEventListener('submit', (event) => {
        updateDateFeedback();
        if (form.dataset.dateInvalid === 'true') {
          event.preventDefault();
          isDateSectionOpen = true;
          const bSem = analyzePairSemantics('begin');
          const eSem = analyzePairSemantics('end');
          const simpleBeginDisabled = document.getElementById('simple_begin_year')?.disabled;
          const simpleEndDisabled = document.getElementById('simple_end_year')?.disabled;
          if ((bSem.mode === 'invalid' && simpleBeginDisabled) || (eSem.mode === 'invalid' && simpleEndDisabled)) {
            isAdvancedDateView = true;
          }
          if (dateSwitcher) {
            dateSwitcher.textContent = translate.hide;
          }
          renderDateVisibility();
        }
      }, true);
    });
  }

  /* =======================================================================
   * 8. Search Form Date Validation
   * ======================================================================= */

  const searchBeginYear = document.getElementById('begin_year');
  const searchEndYear = document.getElementById('end_year');
  const searchFeedback = document.getElementById('search-date-feedback');

  if (searchBeginYear && searchEndYear) {
    const searchFieldIds = [
      'begin_year', 'begin_month', 'begin_day',
      'end_year', 'end_month', 'end_day'
    ];

    function updateSearchDateFeedback() {
      const rFrom = resolveBoundary({
        Y: getInputValue('begin_year'),
        M: getInputValue('begin_month'),
        D: getInputValue('begin_day'),
        badParts: ['Y', 'M', 'D'].filter((part) => isBadNumberInput(`begin_${PART_TO_FIELD[part]}`))
      }, false);
      const rTo = resolveBoundary({
        Y: getInputValue('end_year'),
        M: getInputValue('end_month'),
        D: getInputValue('end_day'),
        badParts: ['Y', 'M', 'D'].filter((part) => isBadNumberInput(`end_${PART_TO_FIELD[part]}`))
      }, true);

      searchFieldIds.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('error');
      });

      const invalidFields = [];
      let errorLabel = '';

      if (!rFrom.valid || !rTo.valid) {
        if (!rFrom.valid) {
          rFrom.invalidParts.forEach((part) => {
            invalidFields.push(`begin_${PART_TO_FIELD[part]}`);
          });
        }
        if (!rTo.valid) {
          rTo.invalidParts.forEach((part) => {
            invalidFields.push(`end_${PART_TO_FIELD[part]}`);
          });
        }
        errorLabel = translate.date_invalid || 'Not a valid date';
      } else if (!rFrom.empty && !rTo.empty && rFrom.sortValue > rTo.sortValue) {
        invalidFields.push('begin_year', 'end_year');
        errorLabel = translate.date_begin_after_end || 'Begin dates cannot start after end dates.';
      }

      const hasError = invalidFields.length > 0;
      invalidFields.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.classList.add('error');
      });

      if (searchFeedback) {
        searchFeedback.textContent = errorLabel;
        searchFeedback.classList.toggle('d-none', !hasError);
        searchFeedback.classList.toggle('text-danger', hasError);
        searchFeedback.classList.toggle('fw-semibold', hasError);
      }

      const form = searchBeginYear.closest('form');
      if (form) {
        form.dataset.dateInvalid = hasError ? 'true' : 'false';
      }
    }

    searchFieldIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        blockInvalidNumberChars(el);
        el.addEventListener('input', updateSearchDateFeedback);
      }
    });

    const searchForm = searchBeginYear.closest('form');
    if (searchForm) {
      searchForm.addEventListener('submit', (event) => {
        updateSearchDateFeedback();
        if (searchForm.dataset.dateInvalid === 'true') {
          event.preventDefault();
        }
      }, true);
    }
  }
});
