(() => {
  const catalog = document.querySelector('.eval-catalog');
  if (!catalog) return;
  const cards = [...catalog.querySelectorAll('.eval-card')];
  const search = document.getElementById('eval-search');
  const category = document.getElementById('eval-category');
  const status = document.getElementById('eval-status');
  const role = document.getElementById('eval-role');
  const count = document.getElementById('eval-count');
  const clear = document.getElementById('eval-clear');
  const empty = document.getElementById('eval-empty');
  const load = document.getElementById('eval-load');
  const more = document.getElementById('eval-more');
  const pageSize = Number(catalog.dataset.pageSize);
  let limit = pageSize;
  const normalize = text => text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[²³]/g, c => c === '²' ? '2' : '3').replace(/[‐‑–—]/g, '-');
  const searchable = cards.map(card => normalize(card.dataset.search));
  const fields = {q: search, category, status, role};
  const initial = new URLSearchParams(location.search);
  for (const [key, field] of Object.entries(fields)) {
    if (!field || !initial.has(key)) continue;
    const value = initial.get(key);
    if (field.tagName === 'INPUT' || [...field.options].some(o => o.value === value)) field.value = value;
  }
  function syncURL() {
    const url = new URL(location.href);
    for (const [key, field] of Object.entries(fields)) {
      if (field?.value.trim()) url.searchParams.set(key, field.value.trim());
      else url.searchParams.delete(key);
    }
    history.replaceState(null, '', url);
  }
  function apply(updateURL = false) {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    const matches = cards.filter((card, index) =>
      words.every(word => searchable[index].includes(word)) &&
      (!category?.value || card.dataset.category === category.value) &&
      (!status.value || card.dataset.status === status.value) &&
      (!role.value || card.dataset.corresponding === 'true')
    );
    const visible = new Set(matches.slice(0, limit));
    cards.forEach(card => { card.hidden = !visible.has(card); });
    const shown = Math.min(limit, matches.length);
    count.textContent = shown < matches.length ? `Showing ${shown} of ${matches.length} works` : `${matches.length} ${matches.length === 1 ? 'work' : 'works'}`;
    empty.hidden = matches.length !== 0;
    load.hidden = shown >= matches.length;
    more.textContent = `Show more (${matches.length - shown} remaining)`;
    clear.hidden = ![search, category, status, role].some(field => field?.value);
    if (updateURL) syncURL();
  }
  function changed() { limit = pageSize; apply(true); }
  search.addEventListener('input', changed);
  [category, status, role].filter(Boolean).forEach(field => field.addEventListener('change', changed));
  catalog.querySelector('form').addEventListener('submit', event => { event.preventDefault(); changed(); });
  clear.addEventListener('click', () => { Object.values(fields).filter(Boolean).forEach(field => {field.value = '';}); changed(); search.focus(); });
  more.addEventListener('click', () => {
    const firstHidden = cards.find(card => card.hidden &&
      (!category?.value || card.dataset.category === category.value) &&
      (!status.value || card.dataset.status === status.value) &&
      (!role.value || card.dataset.corresponding === 'true') &&
      normalize(search.value.trim()).split(/\s+/).filter(Boolean).every(word => normalize(card.dataset.search).includes(word)));
    limit += pageSize; apply();
    if (firstHidden) { firstHidden.tabIndex = -1; firstHidden.focus({preventScroll:true}); }
  });
  const categoryMenu = document.querySelector('.eval-category-menu');
  if (categoryMenu && matchMedia('(max-width: 800px)').matches) categoryMenu.open = false;
  apply();
})();
