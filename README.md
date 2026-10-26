# Jiaheng Liu’s academic homepage

Static academic website for Jiaheng Liu, Nanjing University.

## Update the site

Edit `data/publications.json`, `data/members.json`, `data/member_highlights.json`, or `data/news.json`, then run:

```sh
python3 build_site.py
```

The builder generates the main academic pages and the Evaluation overview with nine category pages. Biography, services, and honors are maintained in `build_site.py`; student profiles are rendered by `members_site.py`. Shared presentation is in `assets/css/academic.css`, with Members-specific styles in `assets/css/members.css`.

Internal page links, styles, and scripts share a content version to prevent stale pages during navigation. The homepage uses the original portrait at its natural aspect ratio on a plain background. Original image assets are preserved; display variants use lightweight web encodings.

Publication author marks: `#` indicates a confirmed corresponding author and `*` equal contribution. Long author lists can be expanded; verified corresponding authors remain visible in the collapsed list. Accepted papers and preprints are distinguished and can be filtered. EMNLP main-conference papers use the venue label “EMNLP 2026”; Findings retain their separate venue label.

Student status is `current` or `upcoming`. Historical news with no verified acceptance month shows the year only.

Student internships, selected research, authorship roles, and separate research-intern outcomes are maintained in `data/member_highlights.json`. Dates are `YYYY.MM`; `present` indicates an ongoing internship at the stated update date. Missing information is omitted. The three overview statistics are computed from the current/incoming roster: students with internships; students with first/co-first authored accepted papers; and distinct accepted papers with such authorship. Preprints and the separate research-intern cohort do not contribute to the latter two counts. Offers are explicitly labeled as offers, not enrollment destinations.

GitHub Pages serves these static files directly; `.nojekyll` disables Jekyll processing. Existing historical project pages and their license notices are retained.
