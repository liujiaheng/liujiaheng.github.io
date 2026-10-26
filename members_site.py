"""Render student research, industry experience, and research-intern outcomes."""
import json
from html import escape


def build_members(root, page, lab):
    e = lambda value: escape(str(value), quote=True)
    people = json.loads((root / 'data/members.json').read_text())
    data = json.loads((root / 'data/member_highlights.json').read_text())
    works, highlights = data['works'], data['students']
    roles = {'first': 'First author', 'co-first': 'Co-first author', 'coauthor': 'Co-author'}
    leadership = {'first', 'co-first'}

    def accepted_lead_work(person):
        return {item['work'] for item in person.get('works', []) + person.get('additional_works', [])
                if item['role'] in leadership and works[item['work']]['status'] == 'published'}

    student_rows = [highlights.get(p['name'], {}) for p in people]
    internship_count = sum(bool(p.get('internships')) for p in student_rows)
    author_count = sum(bool(accepted_lead_work(p)) for p in student_rows)
    paper_count = len(set().union(*(accepted_lead_work(p) for p in student_rows)))

    def research_item(item):
        w = works[item['work']]
        url = w.get('url') or f'pub.html#{w["paper_id"]}'
        venue = 'Preprint' if w['status'] == 'preprint' else w['venue']
        venue = venue.replace(' (Datasets and Benchmarks)', ' · Datasets & Benchmarks')
        venue = venue.replace('Findings of EMNLP', 'EMNLP').replace('Findings of ACL', 'ACL') + (' · Findings' if 'Findings of ' in venue else '')
        return (f'<li><a class="research-title" href="{e(url)}" title="{e(w["title"])}">{e(w["name"])}</a>'
                f'<span class="research-meta"><span class="author-role {e(item["role"])}">{roles[item["role"]]}</span>'
                f'<span>{e(venue)}</span></span></li>')

    def experience(person):
        jobs = person.get('internships', [])
        if not jobs:
            return ''
        organizations = list(dict.fromkeys(j['organization'] for j in jobs))
        result = '<div class="member-experience"><h4>Research internships</h4><p>' + ' · '.join(e(x) for x in organizations) + '</p>'
        dated_jobs = [j for j in jobs if j.get('start')]
        if dated_jobs:
            result += '<details class="experience-dates"><summary>Internship timeline</summary><ul>'
            for job in dated_jobs:
                result += f'<li><span>{e(job["organization"])}</span><time>{e(job["start"])}–{e(job["end"])}</time></li>'
            result += '</ul></details>'
        return result + '</div>'

    def card(person, intern=False):
        h = person if intern else highlights.get(person['name'], {})
        cls = 'member-card' + (' incoming' if person.get('status') == 'upcoming' else '')
        header = f'<h3>{e(person["name"])} <span lang="zh-CN">{e(person["chinese_name"])}</span></h3>'
        if intern:
            subtitle = person['education']
        else:
            degree = 'Ph.D.' if person['degree'] == 'PhD' else 'Master’s'
            subtitle = f'{degree} · {person["since"]}' + (' intake · Incoming' if person.get('status') == 'upcoming' else '–present')
        profile = f'<a class="member-profile" href="{e(person["url"])}">Profile ↗</a>' if person.get('url') else ''
        result = f'<li class="{cls}"><div class="member-card-header">{header}{profile}</div><p class="member-subtitle">{e(subtitle)}</p>'
        if intern and person.get('research_since'):
            result += f'<p class="research-period">Research with our group since {e(person["research_since"])}</p>'
        if h.get('offers'):
            result += f'<p class="student-outcome"><strong>{e(h.get("offer_label", "Ph.D. offers"))}</strong><span>' + ' · '.join(e(x) for x in h['offers']) + '</span></p>'
        result += experience(h)
        if h.get('works'):
            result += '<div class="member-research"><h4>Selected research</h4><ul class="student-work">' + ''.join(research_item(w) for w in h['works']) + '</ul></div>'
        if h.get('additional_works') or h.get('other_work'):
            result += '<details class="more-research"><summary>More research</summary><ul class="student-work">'
            result += ''.join(research_item(w) for w in h.get('additional_works', []))
            for w in h.get('other_work', []):
                result += f'<li><span class="research-title">{e(w["name"])}</span><span class="research-meta"><span class="author-role {e(w["role"])}">{roles[w["role"]]}</span><span>Research project</span></span></li>'
            result += '</ul></details>'
        return result + '</li>'

    def cohort(rows, heading, section_id, note=''):
        label = f'<span class="section-note">{e(note)}</span>' if note else ''
        return f'<section class="student-cohort" id="{section_id}"><h2>{heading}{label}</h2><ul class="member-cards">' + ''.join(card(p) for p in rows) + '</ul></section>'

    content = f'''<div class="members-intro"><p>I am a member of the <a href="{lab}">Large-scale Intelligence and Knowledge (LINK) Lab</a> at Nanjing University. Our students work on foundation models, reinforcement learning, agents, code intelligence, and evaluation.</p></div>
    <section class="student-highlights" aria-label="Student research and industry highlights">
      <p class="highlights-eyebrow">Student research &amp; industry experience</p>
      <div class="student-stats">
        <div><strong>{internship_count}</strong><span>students with industry internships</span></div>
        <div><strong>{author_count}</strong><span>students with first / co-first authored papers</span></div>
        <div><strong>{paper_count}</strong><span>distinct accepted / published papers as first / co-first authors</span></div>
      </div>
      <p class="stats-scope">As of October 26, 2026 · Based on the {len(people)} current and incoming students listed below, including the 2027 intake. Papers are counted once across students; preprints and the separate research-intern cohort are excluded from the paper and authorship totals.</p>
      <div class="industry-line"><span>Internship destinations</span><p>Alibaba · Kuaishou / Kling · ByteDance · StepFun · Insta360</p></div>
    </section>
    <nav class="people-nav" aria-label="Member groups"><a href="#phd-students">Ph.D. students</a><a href="#masters-students">Master’s students</a><a href="#incoming-students">Incoming students</a><a href="#research-interns">Research interns &amp; outcomes</a></nav>'''
    for degree, title, sid in [('PhD', 'Ph.D. Students', 'phd-students'), ('Master', 'Master’s Students', 'masters-students')]:
        content += cohort([p for p in people if p['degree'] == degree and p['status'] == 'current'], title, sid)
    content += '<section class="student-cohort" id="incoming-students"><h2>Incoming Students <span class="section-note">2027 intake</span></h2><p class="cohort-note">Students joining our graduate programs in 2027, with research and internship experience already underway.</p>'
    for degree, title in [('PhD', 'Ph.D. Students'), ('Master', 'Master’s Students')]:
        rows = [p for p in people if p['degree'] == degree and p['status'] == 'upcoming']
        content += f'<h3 class="cohort-subheading">{title}</h3><ul class="member-cards">' + ''.join(card(p) for p in rows) + '</ul>'
    content += '</section><section class="student-cohort" id="research-interns"><h2>Research Interns &amp; Outcomes</h2><p class="cohort-note">Undergraduate research, industry experience, and the next steps in our students’ academic journeys. Offers below indicate admissions received.</p><ul class="member-cards">'
    content += ''.join(card(p, intern=True) for p in data['research_interns'])
    content += '</ul></section><aside class="recruitment"><p><strong>Join us!</strong> We welcome motivated students and research interns interested in foundation models, agents, and evaluation. Contact <a href="mailto:liujiaheng@nju.edu.cn">liujiaheng@nju.edu.cn</a>.</p></aside>'
    page('group.html', 'Members', content)
