/**
 * Autocomplete for external reference systems based on Tom Select
 * Documentation: https://tom-select.js.org/
 *
 * Usage:
 *   initReferenceAutocomplete(systemId, {
 *     minLength: 3,   // minimum characters before searching (default 1)
 *     delay: 400,     // debounce in ms (default 300)
 *     search: query => promise resolving to [{id, label, info, detail}]
 *   });
 *
 * - id: identifier which is stored in the input field (required)
 * - label: main text shown in the dropdown
 * - info: additional short information shown next to the label
 * - detail: additional information shown in the second line
 */
function initReferenceAutocomplete(systemId, options) {
  const input = document.querySelector(
    `input[data-reference-system="${systemId}"]`);
  if (!input || input.tomselect) return null;

  const minLength = options.minLength || 1;
  let requestCounter = 0;

  function normalize(items) {
    if (!Array.isArray(items)) return [];
    return items
      .filter(item => item && item.id !== undefined && item.id !== null
        && String(item.id).trim() !== '')
      .map(item => ({
        id: String(item.id).trim(),
        label: item.label ? String(item.label) : String(item.id),
        info: item.info ? String(item.info) : '',
        detail: item.detail ? String(item.detail) : ''
      }));
  }

  return new TomSelect(input, {
    valueField: 'id',
    labelField: 'id',
    searchField: ['label', 'info', 'detail', 'id'],
    maxItems: 1,
    maxOptions: null,
    create: value => ({id: value.trim(), label: value.trim()}),
    createOnBlur: true,
    persist: false,
    addPrecedence: false,
    hideSelected: true,
    highlight: false,
    refreshThrottle: 0,
    loadThrottle: options.delay || 300,
    plugins: ['restore_on_backspace'],
    shouldLoad: query => query.length >= minLength,
    score: () => () => 1,
    onType: function (query) {
      this.wrapper.classList.toggle('is-typing', query.length > 0);
      requestCounter++;
      this.clearOptions();
      this.refreshOptions(false);
    },
    onChange: function () {
      this.wrapper.classList.remove('is-typing');
    },
    onBlur: function () {
      this.wrapper.classList.remove('is-typing');
    },
    load: function (query, callback) {
      if (query !== this.inputValue()) return callback([]);
      const requestId = ++requestCounter;
      Promise.resolve(options.search(query)).then(
        items => {
          callback(requestId === requestCounter ? normalize(items) : []);
        },
        () => callback([])
      );
    },
    render: {
      option: (item, escape) => `
        <div>
          <strong>${escape(item.label)}</strong>
          ${item.info ? `<span class="text-muted"> - ${escape(item.info)}</span>` : ''}
          <small class="d-block text-muted">
            ${escape(item.id)}${item.detail ? ` - ${escape(item.detail)}` : ''}
          </small>
        </div>`,
      item: (item, escape) => `<div>${escape(item.id)}</div>`,
      option_create: (data, escape) => `
        <div class="create">
          <i class="fas fa-plus"></i> <strong>${escape(data.input)}</strong>
        </div>`
    }
  });
}
