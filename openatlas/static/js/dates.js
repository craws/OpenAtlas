document.addEventListener('DOMContentLoaded', () => {
  const dateSwitcher = document.getElementById('date-switcher');
  const dateSwitchElements = document.querySelectorAll('.date-switch');
  const beginYearFrom = document.getElementById('begin_year_from');
  const beginYearTo = document.getElementById('begin_year_to');
  const endYearFrom = document.getElementById('end_year_from');
  const endYearTo = document.getElementById('end_year_to');

  /* ==========================================================================
   * 1. Calendar and Leap Year Calculation Helpers
   * Pure mathematical helper functions for astronomical/historical years (incl. BC)
   * and month lengths.
   * ========================================================================== */

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

  /* ==========================================================================
   * 2. DOM Input/Output Helpers for Date Boundaries
   * Functions for reading raw values from and writing raw values to the
   * advanced date and time input fields (from / to).
   * ========================================================================== */

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

  function readBoundaryRaw(mode, bound) {
    return {
      Y: getInputValue(`${mode}_year_${bound}`),
      M: getInputValue(`${mode}_month_${bound}`),
      D: getInputValue(`${mode}_day_${bound}`),
      h: getInputValue(`${mode}_hour_${bound}`),
      m: getInputValue(`${mode}_minute_${bound}`),
      s: getInputValue(`${mode}_second_${bound}`)
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

  /* ==========================================================================
   * 3. Validation, Check, and Normalization Functions
   * Validates raw date/time inputs (value ranges, required parts, leap days),
   * fills in default boundary values, formats ISO strings, and computes a
   * numeric sort value for chronological comparison.
   * ========================================================================== */

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

  /* ==========================================================================
   * 4. Semantic Analysis and Model Transformation
   * Analyzes a begin/end boundary pair to determine its semantic mode
   * (empty, invalid, after, before, exact, between) and expands simple date
   * inputs into full from/to boundary pairs.
   * ========================================================================== */

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

  /* ==========================================================================
   * 5. UI Synchronization, Tab Switching, and User Feedback
   * Updates preview labels, synchronizes Simple View with Advanced View, and
   * controls visibility of the date section and view modes.
   * ========================================================================== */

  function updateDateFeedback() {
    if (!beginYearFrom) return;
    ['begin', 'end'].forEach((mode) => {
      const sem = analyzePairSemantics(mode);
      const isInvalid = sem.mode === 'invalid';
      document.querySelectorAll(`[data-feedback-pair="${mode}"]`).forEach((el) => {
        el.textContent = sem.label;
        el.classList.toggle('text-danger', isInvalid);
        el.classList.toggle('fw-semibold', isInvalid);
        el.classList.toggle('text-muted', !isInvalid);
      });
    });
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

  /* ==========================================================================
   * 6. Initialization and Event Binding
   * Determines initial open/closed and Simple/Advanced state on page load and
   * registers event listeners for tabs, inputs, comments, and validation errors.
   * ========================================================================== */

  if (beginYearFrom) {
    const hasDateValue =
      beginYearFrom.value !== '' ||
      (beginYearTo && beginYearTo.value !== '') ||
      (endYearFrom && endYearFrom.value !== '') ||
      (endYearTo && endYearTo.value !== '');
    const hasDateError = document.querySelector('.date-switch .error') !== null;
    isDateSectionOpen = hasDateValue || hasDateError;

    const bSemInit = analyzePairSemantics('begin');
    const eSemInit = analyzePairSemantics('end');
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

    /* ========================================================================
     * 7. Form Validation Integration
     * Automatically expands the date section and switches to Advanced View
     * when form validation marks a date field as invalid on submission.
     * ======================================================================== */

    document.querySelectorAll('form').forEach((form) => {
      form.addEventListener('submit', () => {
        queueMicrotask(() => {
          if (form.querySelector('.date-switch input.error, .date-switch label.error:not([style*="display: none"])')) {
            isDateSectionOpen = true;
            isAdvancedDateView = true;
            if (dateSwitcher) {
              dateSwitcher.textContent = translate.hide;
            }
            renderDateVisibility();
          }
        });
      }, true);
    });
  }
});
