"""Build static academic pages from local data, using Python's standard library."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parent
UPDATED = 'September 2026'
# Version every internal page and asset together, so cached old HTML cannot
# reappear when navigating from an updated page.
_VERSION_INPUTS = [Path(__file__), ROOT/'assets/css/academic.css', ROOT/'assets/js/publications.js', ROOT/'images/favicon.png', ROOT/'images/jiaheng-liu-cutout.png', *sorted((ROOT/'data').glob('*.json'))]
SITE_VERSION = hashlib.sha256(b''.join(p.read_bytes() for p in _VERSION_INPUTS)).hexdigest()[:12]
SCHOLAR = 'https://scholar.google.com/citations?user=yFI_RjUAAAAJ&hl=en'
LAB = 'https://www.nju-link.com/'
NAV = [('index.html', 'About'), ('pub.html', 'Publications'), ('group.html', 'Members'), ('service.html', 'Services'), ('award.html', 'Honors')]

def e(value): return escape(str(value), quote=True)

def page(filename, title, content):
    nav = ''.join(f'<a href="{f}"' + (' aria-current="page"' if f == filename else '') + f'>{name}</a>' for f,name in NAV)
    script = f'<script src="assets/js/publications.js?v={SITE_VERSION}" defer></script>' if filename == 'pub.html' else ''
    heading = '' if filename == 'index.html' else f'<h1 class="page-title">{e(title)}</h1>'
    document = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Jiaheng Liu (刘佳恒), Assistant Professor at Nanjing University. Research in foundation models, code intelligence, reinforcement learning, agents, and evaluation.">
  <meta name="theme-color" content="#660066">
  <title>{e(title)} | Jiaheng Liu · Nanjing University</title>
  <link rel="icon" href="images/favicon.png?v={SITE_VERSION}" type="image/png" sizes="128x128">
  <link rel="stylesheet" href="assets/css/academic.css?v={SITE_VERSION}">
  {script}
</head>
<body class="page-{filename.removesuffix('.html')}">
<a class="skip-link" href="#main">Skip to content</a>
<div class="site">
  <header class="site-header">
    <a class="lab-brand" href="index.html" aria-label="Jiaheng Liu homepage">
      <img src="images/link-lab-web.png" width="2233" height="3072" alt="LINK Lab logo">
      <span>Jiaheng Liu<small>NANJING UNIVERSITY · LINK LAB</small></span>
    </a>
    <nav class="menu" aria-label="Main navigation">{nav}</nav>
  </header>
  <main id="main">
    {heading}
    {content}
    <footer><span>Jiaheng Liu · Nanjing University</span><span>Updated {UPDATED}</span></footer>
  </main>
</div>
</body>
</html>
'''
    document = re.sub(r'href="((?:index|pub|group|service|award|email)\.html)(#[^"]*)?"', lambda m: f'href="{m[1]}?v={SITE_VERSION}{m[2] or ""}"', document)
    document = '\n'.join(line.rstrip() for line in document.splitlines()) + '\n'
    (ROOT/filename).write_text(document, encoding='utf-8')

def homepage():
    news = json.loads((ROOT/'data/news.json').read_text())
    def news_list(rows):
        return '<ul class="news">' + ''.join(f'<li><time datetime="{e(r["date"])}">{e(r["label"])}</time><span>{e(r["text"])}</span></li>' for r in rows) + '</ul>'
    page('index.html', "Jiaheng Liu’s Homepage", f'''
    <section class="profile" aria-label="Profile">
      <img class="portrait" src="images/jiaheng-liu-cutout.png?v={SITE_VERSION}" width="161" height="239" alt="Portrait of Jiaheng Liu">
      <div class="profile-details">
        <h1 class="profile-name">Jiaheng Liu <span lang="zh-CN">刘佳恒</span></h1>
        <p class="position">Assistant Professor · Ph.D. Supervisor</p>
        <p><a href="https://is.nju.edu.cn/ljh/main.htm">School of Intelligence Science and Technology</a><br>Nanjing University (Suzhou Campus)</p>
        <p><a href="{LAB}">NJU LINK Lab</a></p>
        <p><strong>Email:</strong> <a href="mailto:liujiaheng@nju.edu.cn">liujiaheng@nju.edu.cn</a></p>
        <div class="contact-links"><a href="{SCHOLAR}">Google Scholar</a><a href="https://github.com/liujiaheng">GitHub</a><a href="https://www.zhihu.com/people/liu-jia-heng-12">Zhihu</a></div>
      </div>
    </section>
    <aside class="recruitment"><p><strong>Join us!</strong> I am looking for motivated Ph.D. and master’s students, as well as research interns, to work on foundation models, agents, and their evaluation. Please <a href="mailto:liujiaheng@nju.edu.cn">email me</a> if you are interested.</p></aside>
    <section aria-labelledby="biography"><h2 id="biography">Biography</h2>
      <p>I am an Assistant Professor at <a href="https://www.nju.edu.cn/en/">Nanjing University</a>, where I am a member of the <a href="{LAB}">Large-scale Intelligence and Knowledge (LINK) Lab</a>. I am also a co-founder of <a href="https://github.com/multimodal-art-projection">Multimodal Art Projection (M-A-P)</a>, an open-source research community working on text, audio, and visual intelligence.</p>
      <p>My research spans <strong>foundation models, code intelligence, reinforcement learning, agents, and evaluation</strong>. I aim to build capable and reliable models that can reason, use tools, and complete complex tasks. My work connects open model development with post-training, realistic benchmarks, and applications in education and scientific research.</p>
      <p>Previously, I was a Research Scientist at Alibaba (2023–2025), through the <strong>Alibaba Star</strong> program. I received my Ph.D. (2023) and B.Eng. (2019) in Software Engineering from Beihang University, advised during my Ph.D. by <a href="https://scse.buaa.edu.cn/info/1078/2655.htm">Prof. Ke Xu</a> and <a href="https://scholar.google.com/citations?user=7Hdu5k4AAAAJ">Prof. Dong Xu</a>. I also interned at SenseTime, Baidu, and Shanghai AI Laboratory.</p>
      <p>I received an <a href="award.html">ACL 2024 Outstanding Paper Award</a>. I contribute to open-source models and training frameworks, including MAP-Neo, OpenCoder, YuE, ROLL, and Flow-GRPO.</p>
      <p>I serve as an <strong>Area Chair for ICLR, KDD, and ACL ARR</strong> and organize workshops at ICLR and AACL. See my <a href="service.html">professional services</a> for details.</p>
    </section>
    <section aria-labelledby="research"><h2 id="research">Research Interests</h2>
      <ul>
        <li><strong>Foundation models:</strong> open pretraining, code and multimodal models, long-context modeling, and efficient inference.</li>
        <li><strong>Post-training and reinforcement learning:</strong> alignment, reasoning, reward modeling, and optimization for multimodal generation.</li>
        <li><strong>Agents and code intelligence:</strong> software engineering, tool use, deep research, and long-horizon task execution.</li>
        <li><strong>Evaluation:</strong> knowledge, factuality, safety, multimodal understanding, and realistic agent capabilities.</li>
      </ul>
      <p>See my <a href="pub.html">publications</a> for recent work.</p>
    </section>
    <section aria-labelledby="news"><h2 id="news">News</h2>{news_list(news[:6])}
      <details class="older-news"><summary>Earlier news</summary>{news_list(news[6:])}</details>
    </section>
    <section aria-labelledby="experience"><h2 id="experience">Experience &amp; Education</h2>
      <dl class="timeline">
        <dt>2025–present</dt><dd><strong>Nanjing University</strong><span class="detail">Assistant Professor, School of Intelligence Science and Technology</span></dd>
        <dt>2023–2025</dt><dd><strong>Alibaba</strong><span class="detail">Research Scientist · Alibaba Star</span></dd>
        <dt>2019–2023</dt><dd><strong>Beihang University</strong><span class="detail">Ph.D. in Software Engineering</span></dd>
        <dt>2015–2019</dt><dd><strong>Beihang University</strong><span class="detail">B.Eng. in Software Engineering</span></dd>
      </dl>
    </section>''')

def author_key(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

def format_authors(names, corresponding_authors=(), equal_contributors=()):
    corresponding_keys = {author_key(name) for name in corresponding_authors}
    equal_keys = {author_key(name) for name in equal_contributors}
    output=[]
    for name in names:
        clean_name=name.strip().rstrip('*#')
        value=e(clean_name)
        if '*' in name or author_key(clean_name) in equal_keys:
            value+='<sup title="Equal contribution" aria-label="Equal contribution">*</sup>'
        if '#' in name or author_key(clean_name) in corresponding_keys:
            value+='<sup class="corresponding-author" title="Corresponding author" aria-label="Corresponding author">#</sup>'
        if author_key(clean_name)=='jiahengliu': value=f'<strong>{value}</strong>'
        output.append(value)
    return ', '.join(output)

def paper(p):
    title=e(p['title']); authors=p['authors']; url=p.get('url','')
    title_html=f'<a class="paper-title" href="{e(url)}">{title}</a>' if url else f'<span class="paper-title">{title}</span>'
    corresponding=p.get('corresponding_authors',[])
    equal=p.get('equal_contributors',[])
    author_html=format_authors(authors, corresponding, equal)
    if len(authors)>12:
        own=next((i for i,a in enumerate(authors) if 'Jiaheng Liu' in a),None)
        corresponding_keys={author_key(name) for name in corresponding}
        corresponding_indices=[i for i,a in enumerate(authors) if '#' in a or author_key(a) in corresponding_keys]
        indices=sorted(set([0,1,2,len(authors)-1] + ([own] if own is not None else []) + corresponding_indices))
        short=[]; prev=-1
        for i in indices:
            if i>prev+1: short.append('…')
            short.append(format_authors([authors[i]], corresponding, equal)); prev=i
        author_html=f'<details class="paper-authors"><summary>{", ".join(short)}</summary><div class="full-authors">{author_html}</div></details>'
    else: author_html=f'<p class="paper-authors">{author_html}</p>'
    link=f'<a href="{e(url)}">[{e(p.get("link_label","Paper"))}]</a>' if url else f'<a href="https://scholar.google.com/scholar?q={quote(chr(34)+p["title"]+chr(34))}">[Scholar search]</a>'
    if p.get('hide_paper_link'): link=''
    extra=''.join(f'<a href="{e(v)}">[{e(k)}]</a>' for k,v in p.get('links',{}).items())
    award=f'<span class="paper-award">{e(p["award"])}</span>' if p.get('award') else ''
    return f'<li class="publication {p["status"]}" data-year="{p["year"]}" data-status="{p["status"]}" id="{e(p["id"])}">{title_html}{author_html}<div class="paper-meta"><span class="venue">{e(p["venue"])}</span>{award}{link}{extra}</div></li>'

def publications():
    papers=json.loads((ROOT/'data/publications.json').read_text())
    years=sorted({p['year'] for p in papers},reverse=True)
    options=''.join(f'<option value="{y}">{y}</option>' for y in years)
    years_nav=''.join(f'<a href="#year-{y}">{y}</a>' for y in years)
    sections=''
    for year in years:
        rows=[p for p in papers if p['year']==year]
        rows.sort(key=lambda p:(p['status']=='preprint',-p.get('sort_order',0),p['title'].lower()))
        sections+=f'<section class="pub-year" id="year-{year}" aria-labelledby="heading-{year}"><h2 id="heading-{year}">{year}</h2><ul class="pub-list">'+''.join(paper(p) for p in rows)+'</ul></section>'
    page('pub.html','Publications',f'''
    <div class="publication-intro"><p>My research covers foundation models, code intelligence, reinforcement learning, agents, evaluation, and computer vision. See also <a href="{SCHOLAR}">Google Scholar</a>.</p>
    <p class="subtle">Papers are grouped by publication or conference year; preprints appear after peer-reviewed papers within each year. <sup>*</sup> Equal contribution; <sup>#</sup> Corresponding author. Authorship marks follow the paper or author-confirmed information.</p></div>
    <form class="pub-controls" id="publication-filters" role="search" aria-label="Search publications">
      <label for="pub-search">Search publications<input type="search" id="pub-search" placeholder="Title, author, or venue…" autocomplete="off"></label>
      <label for="pub-status">Publication type<select id="pub-status"><option value="">All types</option><option value="published">Peer-reviewed</option><option value="preprint">Preprints</option></select></label>
      <label for="pub-year">Year<select id="pub-year"><option value="">All years</option>{options}</select></label>
    </form>
    <div class="filter-status"><span id="result-count" role="status" aria-live="polite">{len(papers)} publications</span><button class="reset-filter" id="reset-filter" type="button" hidden>Clear filters</button></div>
    <nav class="year-nav" aria-label="Publication years">{years_nav}</nav>
    <p class="no-results" id="no-results" hidden>No matching publications. Try another keyword or clear the filters.</p>
    {sections}''')

def members():
    data=json.loads((ROOT/'data/members.json').read_text())
    content=f'<div class="members-intro"><p>I am a member of the <a href="{LAB}">Large-scale Intelligence and Knowledge (LINK) Lab</a> at Nanjing University. Our students work on foundation models, reinforcement learning, agents, code intelligence, and evaluation.</p><p>Interested in joining us? Please contact <a href="mailto:liujiaheng@nju.edu.cn">liujiaheng@nju.edu.cn</a>.</p></div>'
    def member_list(rows):
        result='<ul class="members">'
        for m in rows:
            link=f'<a class="member-link" href="{e(m["url"])}">Profile ↗</a>' if m.get('url') else ''
            upcoming=m.get('status')=='upcoming'
            year=f'{m["since"]} · Upcoming' if upcoming else f'{m["since"]}–present'
            result+=f'<li class="member{" upcoming" if upcoming else ""}"><span class="member-name">{e(m["name"])}</span><span class="member-cn" lang="zh-CN">{e(m["chinese_name"])}</span><span class="member-year">{year}</span>{link}</li>'
        return result+'</ul>'
    for degree,heading in [('PhD','Ph.D. Students'),('Master','Master’s Students')]:
        rows=[r for r in data if r['degree']==degree and r.get('status')!='upcoming']
        content+=f'<section><h2>{heading}</h2>'+member_list(rows)+'</section>'
    incoming=[r for r in data if r.get('status')=='upcoming']
    if incoming:
        content+='<section class="incoming-students"><h2>Incoming Students <span class="section-note">2027 · Upcoming</span></h2>'
        for degree,heading in [('PhD','Ph.D. Students'),('Master','Master’s Students')]:
            rows=[r for r in incoming if r['degree']==degree]
            if rows:content+=f'<h3>{heading}</h3>'+member_list(rows)
        content+='</section>'
    page('group.html','Members',content)

def services():
    page('service.html','Professional Services','''
    <section><h2>Conference &amp; Workshop Organization</h2><ul class="service-list">
      <li><strong>Area Chair</strong>, ICLR, KDD, and ACL Rolling Review (ARR).</li>
      <li><strong>Local Chair</strong>, EMNLP 2025.</li>
      <li><strong>Workshop Organizer</strong>, Open Science for Foundation Models, ICLR 2025.</li>
      <li><strong>Workshop Organizer</strong>, Latent &amp; Implicit Thinking – Going Beyond CoT Reasoning, ICLR 2026.</li>
      <li><strong>Workshop Organizer</strong>, From Reasoning to Agency: Learning, Acting, and Adapting with Foundation Models, AACL-IJCNLP 2026.</li>
    </ul></section>
    <section><h2>Peer Review</h2><ul class="service-list">
      <li><strong>Conferences:</strong> CVPR, ICCV, ECCV, NeurIPS, ACL ARR, ICLR, and ICML.</li>
      <li><strong>Journals:</strong> International Journal of Computer Vision (IJCV), ACM Computing Surveys (CSUR), IEEE Transactions on Neural Networks and Learning Systems (TNNLS), IEEE Transactions on Image Processing (TIP), and IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI).</li>
    </ul></section>
    <section><h2>Open-source Community</h2><p>I am a co-founder of <a href="https://github.com/multimodal-art-projection">Multimodal Art Projection (M-A-P)</a>, a research community advancing open models, datasets, and reproducible training. Our work spans language, audio, vision, code intelligence, and evaluation.</p></section>''')

def awards():
    page('award.html','Honors & Awards','''
    <ul class="award-list">
      <li><strong>2026 · Second Prize, Science and Technology Progress Award</strong><span class="award-detail" lang="zh-CN">中国指挥与控制学会科学技术进步二等奖</span></li>
      <li><strong>2025 · Gusu Young Scholar</strong>, Nanjing University (<span lang="zh-CN">南京大学姑苏青年学者</span>).</li>
      <li><strong>2024 · ACL Outstanding Paper Award</strong>, for <em>Emulated Disalignment: Safety Alignment for Large Language Models May Backfire!</em></li>
      <li><strong>2023 · Alibaba Star</strong>, Alibaba’s graduate talent program.</li>
      <li><strong>2022 · National Scholarship</strong> for Graduate Students; Huawei Scholarship; Guorui Scholarship.</li>
      <li><strong>2019 · Second Place</strong>, ICCV Lightweight Face Recognition Challenge.</li>
    </ul>''')

if __name__=='__main__':
    homepage(); publications(); members(); services(); awards()
    page('email.html','Contact','<p>Please reach me at <a href="mailto:liujiaheng@nju.edu.cn">liujiaheng@nju.edu.cn</a>.</p>')
    print('Built Homepage, Publications, Members, Services, Awards, and Contact.')
