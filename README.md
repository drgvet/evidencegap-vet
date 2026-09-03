# evidencegap.vet

The site's text lives in `content/`. Those are plain text files. Edit them,
commit, and the site rebuilds itself.

---

## Changing the wording of an appraisal

Open the file for the page you want:

| Page | File |
|---|---|
| Rapamycin appraisal | `content/review-rapamycin.txt` |
| Steroids commentary | `content/review-steroids-chf.txt` |
| Pimobendan re-analysis | `content/review-pimobendan-b2.txt` |

Edit the sentences. Save. That is the whole job — you never touch HTML.

## What the marks in those files mean

Almost everything is an ordinary paragraph. Blank lines separate paragraphs.
The few marks are:

```
== 3. Issues with the evidence     a numbered section
=== 3.1 The endpoint               a subsection
== references                      a section with a special meaning
                                   (references, declarations, abstract,
                                    summary, cite as)

:Findings                          a run-in label in the abstract
Evidence :: one trial in 43 cats   a row in the summary block

[1]        a citation, becomes a superscript link to reference 1
[1,2]      two citations
*word*     italic          **word**   bold
---        an em dash      --         an en dash
"quotes"   become curly automatically
| a | b |  a table row
- item     a bullet
> text     a small note, set below the body text
```

Numbers keep their units on one line by themselves, so writing `7.41 mm` or
`p = 0.013` gives the right typography without you doing anything.

## The top of each file

The lines before the first blank line are the page's details:

```
title: Rapamycin (sirolimus) for subclinical hypertrophic cardiomyopathy in cats
id: EG-2026-004
domain: Feline cardiology
first_published: 14 August 2026
last_revised: 27 August 2026
certainty: Very low
endpoint: Surrogate only
```

Anything you add here that the template does not recognise appears as an extra
row in the sidebar, so you can invent your own without editing code.

## Correcting an entry on the gap map

The 24 map entries are still in `legacy/p_gapmap.py`, in a list near the top.
Each is a block like this, and the wording is safe to edit in place:

```python
dict(t="Rapamycin (sirolimus) in subclinical hypertrophic cardiomyopathy",
     conf="verylow", dirn="unclear",
     basis="1 randomised trial, 43 cats, surrogate endpoint only",
     verdict="RAPACAT is a dose-finding study ...")
```

`conf` is one of `high`, `moderate`, `low`, `verylow`, `none`.

## Building it

```
python3 build.py
```

Plain Python 3, no packages to install. The finished site lands in `_site/`.
Open `_site/index.html` in a browser to check it before committing.

## How it publishes

Cloudflare Pages watches the `main` branch. Every push runs `python3 build.py`
and serves `_site/`. Nothing else to do.

## What is where

```
content/          the text you edit
content/figures/  charts, kept as their own files
lib/              the templates and the text parser
legacy/           pages whose text has not been moved to content/ yet
assets/site.css   the stylesheet
build.py          the build
_site/            output, not committed
```

## Adding a new appraisal

1. Copy an existing file in `content/` to a new name.
2. Replace the details at the top and the text.
3. Add one line to `APPRAISALS` in `build.py` with the new name, a browser
   title and a one-sentence description.
4. Add the entry to `legacy/p_reviews2.py` so it appears on the appraisals
   page, and to `legacy/p_gapmap.py` if it belongs on the map.

## A note on corrections

Every edit becomes a dated commit, so the record of what changed and when is
kept automatically. For a site whose argument is that other people's evidence
does not hold up, that history is worth having.
