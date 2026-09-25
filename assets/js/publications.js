(() => {
  const form = document.querySelector('#publication-filters');
  if (!form) return;
  const query = form.querySelector('#pub-search');
  const status = form.querySelector('#pub-status');
  const year = form.querySelector('#pub-year');
  const items = Array.from(document.querySelectorAll('.publication'));
  const sections = Array.from(document.querySelectorAll('.pub-year'));
  const count = document.querySelector('#result-count');
  const reset = document.querySelector('#reset-filter');
  const empty = document.querySelector('#no-results');
  const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const texts = new Map(items.map(item => [item, normalize(item.textContent)]));
  function filter() {
    const terms = normalize(query.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    items.forEach(item => {
      const matched = terms.every(term => texts.get(item).includes(term)) &&
        (!status.value || item.dataset.status === status.value) &&
        (!year.value || item.dataset.year === year.value);
      item.hidden = !matched;
      if (matched) visible++;
    });
    sections.forEach(section => {
      section.hidden = !section.querySelector('.publication:not([hidden])');
      const link = document.querySelector(`.year-nav a[href="#${section.id}"]`);
      if (link) link.hidden = section.hidden;
    });
    count.textContent = `${visible} of ${items.length} publications`;
    empty.hidden = visible > 0;
    reset.hidden = !query.value && !status.value && !year.value;
  }
  form.addEventListener('submit', event => event.preventDefault());
  query.addEventListener('input', filter);
  status.addEventListener('change', filter);
  year.addEventListener('change', filter);
  reset.addEventListener('click', () => { form.reset(); filter(); query.focus(); });
  filter();
})();
