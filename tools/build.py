"""Builds the URI3AN Lab site from content/*.json into static HTML pages at the repository root.

Usage: python tools/build.py
Edit content/*.json (news, members, publications, ...) and run this again.
"""
import json
import re
from collections import OrderedDict
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
site = json.loads((C / "site.json").read_text(encoding="utf-8"))
pubs = json.loads((C / "publications.json").read_text(encoding="utf-8"))
research = json.loads((C / "research.json").read_text(encoding="utf-8"))
teaching = json.loads((C / "teaching.json").read_text(encoding="utf-8"))
LAB = site["lab"]

NAV = [("index.html", "Home"), ("members.html", "Members"), ("professor.html", "Professor"),
       ("publications.html", "Publications"), ("research.html", "Research"), ("teaching.html", "Teaching")]


def e(s):
    return escape(s or "", quote=True)


def page(fname, title, body, desc=None):
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{f}"{cur if f == fname else ""}><i>{i:02d}</i>{n}</a>' for i, (f, n) in enumerate(NAV, 1))
    full = f"{title} | {LAB['short']}" if fname != "index.html" else f"{LAB['short']} · {LAB['ko']}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc or LAB['name'] + ' (' + LAB['ko'] + '), ' + LAB['dept'] + '. ' + LAB['tagline'])}">
<meta property="og:title" content="{e(full)}">
<meta property="og:image" content="assets/img/logo.png">
<link rel="icon" href="assets/img/logo-simple.png">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<aside class="side">
  <a class="brand" href="index.html"><img src="assets/img/logo.png" alt="URI3AN Lab logo" width="564" height="188"></a>
  <p class="side-name">{e(LAB['ko'])}<small>Ewha Womans University</small></p>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <div class="side-contact"><a href="mailto:{e(LAB['email'])}">{e(LAB['email'])}</a><span>{e(LAB['phone'])}</span></div>
</aside>
<div class="main-col">
<main>
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div><b>{e(LAB['name'])} ({e(LAB['short'])})</b><span>{e(LAB['dept'])}</span></div>
    <div><span>{e(LAB['office'])}</span><span><a href="mailto:{e(LAB['email'])}">{e(LAB['email'])}</a> · {e(LAB['phone'])}</span></div>
  </div>
</footer>
</div>
</body>
</html>
"""


def title_block(h1, p=""):
    return f'<section class="band"><div class="wrap page-title"><h1>{e(h1)}</h1>{"<p>" + e(p) + "</p>" if p else ""}</div></section>'


def home():
    items = []
    for n in site["news"]:
        txt = e(n["text"])
        if n.get("link"):
            txt += f' <a href="{e(n["link"])}">Related article</a>'
        pics = "".join(f'<img src="assets/img/news/{i}.webp" alt="{e(n["date"])} {e(n["text"])}" loading="lazy">' for i in n["imgs"])
        pics = '<div class="pics">' + pics + '</div>' if pics else ""
        items.append(f'<li><time>{e(n["date"])}</time><div><p>{txt}</p>{pics}</div></li>')
    body = f"""<section class="band"><div class="wrap hero">
  <div>
    <p class="eyebrow">Ewha Womans University · Architectural &amp; Urban Systems Engineering</p>
    <h1>URBAN Informatics and Intelligent Infrastructure Lab</h1>
    <p class="ko">(URI3AN) {e(LAB['ko'])}</p>
    <p class="tag">{e(LAB['tagline'])}</p>
    <div class="contact">
      <span><b>Email</b> <a href="mailto:{e(LAB['email'])}">{e(LAB['email'])}</a></span>
      <span><b>Office</b> {e(LAB['office'])}</span>
      <span><b>Phone</b> {e(LAB['phone'])}</span>
    </div>
  </div>
  <figure><img src="assets/img/concept.webp" alt="Lab concept: urban systems, people's safety, health and wellness, and intelligent infrastructures" width="606" height="712"></figure>
</div></section>
<section class="sec"><div class="wrap"><h2>News</h2><ul class="news">{''.join(items)}</ul></div></section>"""
    return page("index.html", "Home", body)


def members():
    cards = []
    for m in site["members"]:
        note = f'<p class="note">{e(m["note"])}</p>' if m.get("note") else ""
        cards.append(f'<li class="person"><img src="assets/img/members/{m["img"]}.webp" alt="{e(m["name"])}" loading="lazy" width="480" height="600"><div>'
                     f'<h3>{e(m["ko"] or m["name"])}<span>{e(m["name"]) if m["ko"] else ""}</span></h3>'
                     f'<p class="role">{e(m["role"])} ({e(m["since"])} ~ )</p><p>Research interest: {e(m["interest"])}</p>{note}</div></li>')
    al = []
    for grp in ("PhD", "MSc", "Postdoc"):
        label = "Doctoral Dissertation" if grp == "PhD" else "Master&#39;s Thesis"
        rows = "".join(f'<li><div><b>{e(a["name"])}</b><span class="yr">{e(a["years"])}</span></div><div>'
                       + (f'<span class="pos">{e(a["position"])}</span>' if a.get("position") else "")
                       + (f'<span class="th">{label}: {e(a["thesis"])}</span>' if a.get("thesis") else "")
                       + '</div></li>' for a in site["alumni"][grp])
        al.append(f'<h3 style="margin:24px 0 8px;font-size:1rem">{grp}</h3><ul class="alumni">{rows}</ul>')
    ug = "".join(f'<li>{e(a["name"])}<span>{e(a["years"])}</span></li>' for a in site["alumni"]["Undergraduate"])
    al.append(f'<h3 style="margin:24px 0 8px;font-size:1rem">Undergraduate Students</h3><ul class="chips">{ug}</ul>')
    body = (title_block("Members") + f'<section class="wrap" style="padding-block:40px 56px"><ul class="people">{"".join(cards)}</ul></section>'
            + f'<section class="sec"><div class="wrap"><h2>Alumni</h2>{"".join(al)}</div></section>')
    return page("members.html", "Members", body)


def dl(rows):
    return '<ul class="dl">' + "".join(f"<li><span>{e(a)}</span><span>{e(b)}</span></li>" for a, b in rows) + "</ul>"


def professor():
    p = site["professor"]
    body = title_block("Professor") + f"""<section class="wrap prof" style="padding-block:40px">
  <img src="assets/img/members/sungjoo-hwang.webp" alt="{e(p['name'])}" width="413" height="513">
  <div><h2>{e(p['name'])} <span style="font-weight:500;color:var(--muted);font-size:1.1rem">{e(p['ko'])}</span></h2>
  <p class="sub">{e(p['title'])}<br>{e(p['dept'])}</p>
  <p class="sub"><a href="mailto:{e(LAB['email'])}">{e(LAB['email'])}</a> · {e(LAB['phone'])}</p>
  <h3 style="margin:24px 0 10px;font-size:1rem">Research Interest</h3><ul class="bullets">{''.join(f'<li>{e(x)}</li>' for x in p['interests'])}</ul></div>
</section>
<section class="sec"><div class="wrap"><h2>Education</h2>{dl(p['education'])}</div></section>
<section class="sec"><div class="wrap"><h2>Academic &amp; Professional Experience</h2>{dl(p['experience'])}</div></section>
<section class="sec"><div class="wrap"><h2>Awards &amp; Honors</h2>{dl(p['awards'])}</div></section>
<section class="sec"><div class="wrap"><h2>Activities</h2>{dl(p['activities'])}</div></section>"""
    return page("professor.html", "Professor", body)


def mark(t):
    t = e(t)
    t = re.sub(r"\bHwang, S\.", '<span class="me">Hwang, S.</span>', t)
    t = t.replace("황성주", '<span class="me">황성주</span>')
    for k, lab in (("(Under Review)", "Under Review"), ("(Corresponding Author)", "Corresponding")):
        t = t.replace(e(k), f'<span class="badge">{lab}</span>')
    return t


def publications():
    secs = [("journal", "Journal Papers"), ("conference", "Conference Papers"), ("book", "Books and Book Chapters"),
            ("patent", "Patents"), ("software", "Software")]
    toc = "".join(f'<a href="#{k}">{n}<span>{len(pubs[k])}</span></a>' for k, n in secs)
    out = []
    for k, n in secs:
        by = OrderedDict()
        for x in pubs[k]:
            by.setdefault(x["year"], []).append(x)
        yrs = "".join(f'<div class="year"><h3>{y}</h3><ul class="pubs">'
                      + "".join(f'<li>{mark(x["text"])}' + (f' <a href="{e(x["link"])}">DOI</a>' if x["link"] else "") + "</li>" for x in xs)
                      + "</ul></div>" for y, xs in by.items())
        out.append(f'<section class="sec" id="{k}"><div class="wrap"><h2>{n}<small>{len(pubs[k])}</small></h2>{yrs}</div></section>')
    body = (f'<section class="band"><div class="wrap page-title"><h1>Publications</h1><p>Bold marks Prof. Sungjoo Hwang. '
            f'Corresponding-author and under-review papers are tagged.</p><nav class="toc" aria-label="Sections">{toc}</nav></div></section>' + "".join(out))
    return page("publications.html", "Publications", body)


def research_page():
    def proj(p):
        img = f'<img src="assets/img/research/{p["img"]}.webp" alt="{e(p["title"])}" loading="lazy">' if p["img"] else ""
        meta = "".join(f"<span><b>{lab}</b> {e(p[k])}</span>" for k, lab in (("sponsor", "Sponsor"), ("partner", "Partner"), ("role", "Role")) if p[k])
        return (f'<article class="project{"" if img else " noimg"}"><div><p class="yrs">{e(p["years"])}</p><h3>{e(p["title"])}</h3>'
                f'<p class="ko">{e(p["ko"])}</p><div class="meta">{meta}</div></div>{img}</article>')
    on = "".join(proj(p) for p in research if p["status"] == "ongoing")
    past = "".join(proj(p) for p in research if p["status"] == "past")
    body = (title_block("Research", LAB["tagline"])
            + f'<section class="sec"><div class="wrap"><h2>Ongoing Research Projects</h2><div class="projects">{on}</div></div></section>'
            + f'<section class="sec"><div class="wrap"><h2>Past Research Projects</h2><div class="projects">{past}</div></div></section>')
    return page("research.html", "Research", body)


def teaching_page():
    rows = "".join(f'<li><code>{e(c["code"])}</code><div><h3>{e(c["title"])}<span>{e(c["ko"])}</span></h3><p>{e(c["desc"])}'
                   + (f' ({e(c["note"])})' if c["note"] else "") + f'</p></div><span class="yrs">{e(c["years"])}</span></li>' for c in teaching)
    body = title_block("Teaching") + f'<section class="wrap" style="padding-block:40px 56px"><ul class="courses">{rows}</ul></section>'
    return page("teaching.html", "Teaching", body)


for fname, fn in (("index.html", home), ("members.html", members), ("professor.html", professor),
                  ("publications.html", publications), ("research.html", research_page), ("teaching.html", teaching_page)):
    (ROOT / fname).write_text(fn(), encoding="utf-8")
    print("wrote", fname)
