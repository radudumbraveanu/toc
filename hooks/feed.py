"""Render every card in docs/ (except reserved files) as one feed on the index page, newest first."""
import re
from pathlib import Path

import yaml

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


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != "index.md":
        return markdown
    docs = Path(config["docs_dir"])
    cards = []
    for path in docs.glob("*.md"):
        if path.name in RESERVED:
            continue
        meta, body = _parse(path)
        if meta.get("type") != "Technology":
            continue
        cards.append((str(meta.get("generated", {}).get("at", "")), meta, _prefix_footnotes(body, path.stem)))
    cards.sort(key=lambda c: c[0], reverse=True)

    intro = [l for l in markdown.splitlines() if not l.startswith("- [")]
    parts = ["\n".join(intro).strip()]
    for at, meta, body in cards:
        tags = " ".join(f"`{t}`" for t in meta.get("tags", []))
        head = f"## {meta.get('title')}\n\n*{at[:10]}* {tags}"
        parts.append(f"{head}\n\n{_demote(body).strip()}")
    return "\n\n---\n\n".join(parts) + "\n"
