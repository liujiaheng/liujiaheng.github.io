"""Render a capability-based catalog from audited publication records."""
from pathlib import Path
from html import escape as e
from urllib.parse import urlparse
import json
import re

ROOT = Path(__file__).resolve().parent

def build_evaluation(page, format_authors):
    data = json.loads((ROOT / 'data/evaluation.json').read_text())
    papers = {p['id']: p for p in json.loads((ROOT / 'data/publications.json').read_text())}
    categories = data['categories']
    category_by_id = {c['id']: c for c in categories}
    entries = data['entries']
    assert len({r['paper_id'] for r in entries}) == len(entries)
    for row in entries:
        assert row['paper_id'] in papers and row['category'] in category_by_id
        assert row['kind'] in ('benchmark', 'companion', 'method')
    counts = {c['id']: sum(r['category'] == c['id'] for r in entries) for c in categories}
    def path(category):
        return f'evaluation-{category}.html'
    def anchor(row):
        return 'eval-' + row['paper_id'].removeprefix('paper-')
    def corresponding(paper):
        return any(re.sub('[^a-z]', '', a.lower()) == 'jiahengliu' for a in paper.get('corresponding_authors', []))
    def order(row):
        p = papers[row['paper_id']]
        return (-p['year'], p['status'] == 'preprint', -p.get('sort_order', 0), row['name'].lower())
    def card(row, overview=False):
        p = papers[row['paper_id']]
        c = category_by_id[row['category']]
        role = corresponding(p)
        kind_labels = {'benchmark': 'Benchmark', 'companion': 'Companion dataset', 'method': 'Evaluation method'}
        status = 'Preprint' if p['status'] == 'preprint' else 'Accepted / published'
        venue = p['venue']
        if 'EMNLP 2026' in venue:
            venue += ' · Accepted'
        link_items = []
        seen = set()
        url = p.get('url', '')
        if 'openreview.net' in url:
            url = 'https://arxiv.org/abs/' + p['arxiv_ids'][0] if p.get('arxiv_ids') else ''
        if url and not p.get('hide_paper_link'):
            label = 'Code' if urlparse(url).netloc == 'github.com' else 'Paper'
            link_items.append((label, url))
            seen.add(url)
        for label, url in {**p.get('links', {}), **row.get('links', {})}.items():
            if url not in seen and 'openreview.net' not in url:
                link_items.append((label, url)); seen.add(url)
        links = ''.join(f'<a href="{e(url, quote=True)}">{e(label)} <span aria-hidden="true">↗</span></a>' for label, url in link_items)
        links += f'<a href="pub.html#{e(p["id"])}">Publication details</a>'
        tags = ''.join(f'<span>{e(t)}</span>' for t in row['tags'])
        authors = format_authors(p['authors'], p.get('corresponding_authors', []), p.get('equal_contributors', []))
        name = f'<a href="{path(row["category"])}#{anchor(row)}">{e(row["name"])}</a>' if overview else e(row['name'])
        topic = f'<a class="eval-topic" href="{path(row["category"])}">{e(c["name"])}</a>' if overview else f'<span class="eval-topic">{e(row["section"])}</span>'
        kind = f'<span class="eval-kind">{kind_labels[row["kind"]]}</span>' if row['kind'] != 'benchmark' else ''
        role_html = '<span class="eval-role">Corresponding author</span>' if role else ''
        search = ' '.join([row['name'], p['title'], row['summary'], c['name'], row['section'], *row['tags'], p['venue'], *p['authors']])
        return f'''<article class="eval-card" id="{anchor(row)}" data-category="{row['category']}" data-status="{p['status']}" data-corresponding="{str(role).lower()}" data-search="{e(search, quote=True)}">
          <div class="eval-card-top">{topic}{kind}</div>
          <h3>{name}</h3>
          <p class="eval-summary">{e(row['summary'])}</p>
          <div class="eval-tags" aria-label="Topics">{tags}</div>
          <div class="eval-meta"><span class="eval-venue{' is-preprint' if p['status'] == 'preprint' else ''}">{e(venue)}</span>{role_html}</div>
          <details class="eval-paper"><summary>Paper &amp; authors</summary><p class="eval-paper-title">{e(p['title'])}</p><p class="eval-authors">{authors}</p><p class="subtle"><sup>*</sup> Equal contribution; <sup>#</sup> Corresponding author.</p></details>
          <div class="eval-links">{links}</div>
        </article>'''
    def filters(overview=False):
        options = ''.join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in categories)
        category = f'<label for="eval-category">Research area<select id="eval-category"><option value="">All areas</option>{options}</select></label>' if overview else ''
        return f'''<form class="eval-controls" role="search" aria-label="Filter evaluation research">
          <label class="eval-search-field" for="eval-search">Search the collection<input id="eval-search" type="search" placeholder="Benchmark, capability, paper, or author…" autocomplete="off"></label>
          {category}
          <label for="eval-status">Publication status<select id="eval-status"><option value="">All statuses</option><option value="published">Accepted / published</option><option value="preprint">Preprints</option></select></label>
          <label for="eval-role">Authorship<select id="eval-role"><option value="">All contributions</option><option value="corresponding">Corresponding author</option></select></label>
        </form>'''
    def result_area(rows, overview=False):
        cards = ''.join(card(row, overview) for row in sorted(rows, key=order))
        return f'''<section class="eval-catalog" aria-labelledby="catalog-heading" data-page-size="{12 if overview else 1000}">
          <div class="eval-catalog-heading"><h2 id="catalog-heading">{'Explore all work' if overview else 'Benchmarks &amp; related work'}</h2><span class="eval-result-count" id="eval-count" role="status" aria-live="polite">{len(rows)} works</span></div>
          {filters(overview)}
          <div class="eval-filter-feedback"><p class="subtle" id="eval-filter-hint">Search by name or capability, or narrow by publication status and authorship.</p><button class="eval-clear" type="button" id="eval-clear" hidden>Clear filters</button></div>
          <div class="eval-grid{' eval-grid-overview' if overview else ''}">{cards}</div>
          <div class="eval-empty" id="eval-empty" hidden><h3>No matching work</h3><p>Try a broader keyword or clear the filters.</p></div>
          <div class="eval-load" id="eval-load" hidden><button type="button" id="eval-more">Show more</button></div>
        </section>'''
    num_methods = sum(r['kind'] == 'method' for r in entries)
    tiles = ''
    for i, c in enumerate(categories, 1):
        examples = ' · '.join(c['examples'])
        tiles += f'''<a class="eval-category-card" href="{path(c['id'])}"><div class="eval-category-top"><span class="eval-index">{i:02d}</span><span>{counts[c['id']]} works <span aria-hidden="true">↗</span></span></div><h3>{e(c['name'])}</h3><p>{e(c['tagline'])}</p><div class="eval-examples">{e(examples)}</div></a>'''
    intro = f'''<section class="eval-hero"><p class="eval-eyebrow">Benchmarks &amp; evaluation research</p><h1>Evaluation</h1><p class="eval-lede">How do we know what a model can really do?</p><p class="eval-intro">Benchmarks, datasets, and evaluation methods from my work with collaborators — spanning coding agents, knowledge work, reasoning, and multimodal intelligence.</p><dl class="eval-stats"><div><dt>Benchmarks &amp; datasets</dt><dd>{len(entries)-num_methods}</dd></div><div><dt>Research areas</dt><dd>{len(categories)}</dd></div></dl></section>
      <section aria-labelledby="areas-heading"><h2 id="areas-heading">Browse by capability</h2><div class="eval-category-grid">{tiles}</div></section>'''
    note = '<p class="eval-scope">This collection includes co-authored benchmarks, companion evaluation datasets, and evaluation methods. Each work has one primary category; topic tags capture related capabilities. Corresponding-author labels refer to Jiaheng Liu.</p>'
    page('evaluation.html', 'Evaluation', intro + result_area(entries, True) + note)
    for c in categories:
        rows = [r for r in entries if r['category'] == c['id']]
        menu = f'<a href="evaluation.html">All evaluation research <span>{len(entries)}</span></a>'
        menu += ''.join(f'<a href="{path(k["id"])}"' + (' aria-current="page"' if k['id'] == c['id'] else '') + f'>{e(k["name"])}<span>{counts[k["id"]]}</span></a>' for k in categories)
        hero = f'''<section class="eval-hero eval-category-hero"><a class="eval-back" href="evaluation.html">← Evaluation overview</a><p class="eval-eyebrow">{len(rows)} research contributions</p><h1>{e(c['name'])}</h1><p class="eval-intro">{e(c['description'])}</p></section>'''
        side = f'<aside class="eval-sidebar"><details class="eval-category-menu" open><summary>Browse research areas</summary><nav aria-label="Evaluation categories">{menu}</nav></details></aside>'
        page(path(c['id']), c['name'] + ' | Evaluation', hero + '<div class="eval-layout">' + side + result_area(rows) + '</div>' + note)
