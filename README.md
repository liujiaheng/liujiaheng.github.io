# Jiaheng Liu’s academic homepage

Static academic website for Jiaheng Liu, Nanjing University.

## Update the site

Edit `data/publications.json`, `data/members.json`, or `data/news.json`, then run:

```sh
python3 build_site.py
```

The builder generates six pages. Biography, services, and honors are maintained in `build_site.py`; presentation is in `assets/css/academic.css`.

Internal page links, styles, and scripts share a content version to prevent stale pages during navigation. The campus photograph appears only in the homepage profile header, without blur and with a light overlay behind the text. Original image assets are preserved; display variants use lightweight web encodings.

Publication author marks: `#` indicates a confirmed corresponding author and `*` equal contribution. Long author lists can be expanded; verified corresponding authors remain visible in the collapsed list. Accepted papers and preprints are distinguished and can be filtered. EMNLP main-conference papers use the venue label “EMNLP 2026”; Findings retain their separate venue label.

Student status is `current` or `upcoming`. Historical news with no verified acceptance month shows the year only.

GitHub Pages serves these static files directly; `.nojekyll` disables Jekyll processing. Existing historical project pages and their license notices are retained.
