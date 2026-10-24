"""Render every card in docs/ (except reserved files) as one feed on the index page, newest first."""
import hashlib
import html
import re
from pathlib import Path

import yaml
from markdown.extensions.toc import slugify
from PIL import Image, ImageDraw, ImageFont

RESERVED = {"index.md", "log.md"}
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def _parse(path):
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    meta = yaml.safe_load(m.group(1)) if m else {}
    return meta or {}, text[m.end():] if m else text


def _prefix_footnotes(body, slug):
    """Make footnote ids unique per card, since all cards share one page."""
    return re.sub(r"\[\^([^\]]+)\]", lambda m: f"[^{slug}-{m.group(1)}]", body)


def _demote(body):
    """Turn card headings (# ...) into ###, leaving code fences untouched."""
    out, fenced = [], False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("# "):
            line = "##" + line
        out.append(line)
    return "\n".join(out)


def _load_cards(docs):
    cards = []
    for path in docs.glob("*.md"):
        if path.name in RESERVED:
            continue
        meta, body = _parse(path)
        if meta.get("type") != "Technology":
            continue
        cards.append((str(meta.get("generated", {}).get("at", "")), meta, _prefix_footnotes(body, path.stem), path.stem))
    cards.sort(key=lambda c: c[0], reverse=True)
    return cards


def _wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def _share_image(path, meta):
    """1200x630 preview image: title, description, tags."""
    w, h, pad = 1200, 630, 72
    img = Image.new("RGB", (w, h), "#eef1f4")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 14], fill="#b3402a")
    title_f, body_f, small_f = (ImageFont.load_default(size=s) for s in (84, 36, 30))
    d.text((pad, 70), str(meta.get("title", "")), font=title_f, fill="#1c242c")
    desc = _wrap(d, str(meta.get("description", "")), body_f, w - 2 * pad)[:4]
    for i, line in enumerate(desc):
        d.text((pad, 200 + i * 52), line, font=body_f, fill="#5b6874")
    d.text((pad, h - 120), "  ".join(f"#{t}" for t in meta.get("tags", [])[:5]), font=small_f, fill="#b3402a")
    d.text((pad, h - 70), "toc: know it exists, dig in when you need it", font=small_f, fill="#5b6874")
    img.save(path, optimize=True)


SHARE_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<meta name="robots" content="noindex">
<meta name="description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace({target_js});</script>
</head><body><p><a href="{target}">{title}</a></p></body></html>
"""


def on_post_build(config):
    """Write /share/<slug>/ pages for link previews; each redirects to the card in the feed."""
    site, base = Path(config["site_dir"]), config["site_url"].rstrip("/") + "/"
    for at, meta, _, stem in _load_cards(Path(config["docs_dir"])):
        out = site / "share" / stem
        out.mkdir(parents=True, exist_ok=True)
        _share_image(out / "og.png", meta)
        version = hashlib.md5((out / "og.png").read_bytes()).hexdigest()[:8]
        target = f"{base}#{slugify(str(meta.get('title')), '-')}"
        page = SHARE_PAGE.format(
            title=html.escape(f"{meta.get('title')} | toc"),
            desc=html.escape(str(meta.get("description", ""))),
            image=f"{base}share/{stem}/og.png?v={version}",
            url=f"{base}share/{stem}/",
            target=html.escape(target),
            target_js='"' + target + '"',
        )
        (out / "index.html").write_text(page, encoding="utf-8")


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != "index.md":
        return markdown
    cards = [c[:3] for c in _load_cards(Path(config["docs_dir"]))]

    intro = [l for l in markdown.splitlines() if not l.startswith("- [")]
    parts = ["\n".join(intro).strip()]
    for at, meta, body in cards:
        tags = " ".join(f"`{t}`" for t in meta.get("tags", []))
        head = f"## {meta.get('title')}\n\n*{at[:10]}* {tags}"
        parts.append(f"{head}\n\n{_demote(body).strip()}")
    return "\n\n---\n\n".join(parts) + "\n"
