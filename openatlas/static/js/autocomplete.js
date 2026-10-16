/**
 * Autocomplete for external reference systems based on autoComplete.js
 * Documentation: https://tarekraafat.github.io/autoComplete.js/
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
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function initReferenceAutocomplete(systemId, options) {
  const input = document.querySelector(
    `input[data-reference-system="${systemId}"]`);
  if (!input || input.autocomplete_instance) return null;

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

  const autocomplete = new autoComplete({
    selector: () => input,
    placeHolder: input.placeholder || '',
    threshold: minLength,
    debounce: options.delay || 300,
    wrapper: false,
    searchEngine: () => true,
    data: {
      src: async (query) => {
        const currentCounter = ++requestCounter;
        if (query !== input.value.trim()) {
          return [];
        }
        try {
          const items = await Promise.resolve(options.search(query));
          if (currentCounter !== requestCounter || query !== input.value.trim()) {
            return [];
          }
          return normalize(items);
        } catch (err) {
          return [];
        }
      },
      cache: false
    },
    resultsList: {
      tag: 'ul',
      class: 'autoComplete_list',
      maxResults: options.maxResults || 50
    },
    resultItem: {
      tag: 'li',
      class: 'autoComplete_result',
      element: (item, data) => {
        const record = data.value;
        item.innerHTML = `
          <div class="autocomplete-label">
            <strong>${escapeHtml(record.label)}</strong>
            ${record.info ? `<span class="text-muted"> - ${escapeHtml(record.info)}</span>` : ''}
          </div>
          <small class="d-block text-muted">
            ${escapeHtml(record.id)}${record.detail ? ` - ${escapeHtml(record.detail)}` : ''}
          </small>`;
      }
    },
    events: {
      input: {
        selection: (event) => {
          const selection = event.detail.selection.value;
          input.value = selection.id;
          requestCounter++;
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      }
    }
  });

  input.autocomplete_instance = autocomplete;
  return autocomplete;
}
