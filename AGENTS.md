# AGENTS.md

Instructions for AI agents working in this repository. Read [README.md](README.md) first for the project idea.

## Why the cards look the way they do

The author follows the **toc method**: first know that X exists and when it is useful, learn the details only when a real problem appears. The future reader of a card is the author, with a concrete problem in front of them, asking "what did I note that solves this?". So:

- **"When it is useful" is the core of the card.** Write each bullet as a recognizable trigger (a situation or symptom: "you have X and need Y", "instead of Y when Z"), not as a feature list.
- The card must be findable by the **problem it solves**, not only by the technology name. Tags and bullets should reflect problems, not only the stack.
- Details belong in the linked docs, not in the card.

## Adding a technology: `Add <URL>`

The author adds entries with this command:

```
Add <URL> [extra info]
```

- `<URL>`: page about the technology (official site, repo, docs).
- `[extra info]` (optional): anything the author wants to add (context, why it caught their eye, points to stress). Treat it as input for the card; do not drop or contradict it.

When you receive `Add <URL> [extra info]`:

1. Fetch the URL and understand what the technology is. Do not guess from the name.
2. Extract the **technology name** (official spelling).
3. **Check the bundle for duplicates.** Search `docs/` for the name, the resource URL and close variants (same tool under another name, a fork, a rename). If a card already exists, tell the author and ask whether to update it or stop. Do not create a second card for the same technology. If a card for a closely related technology exists, mention it; the author decides.
4. Draft a **"When it is useful"** bullet list: concrete situations or problems where the author might reach for it later. This is the most important part of the card, since the author may not need the technology now. Phrase each bullet as a trigger the author would recognize when the problem appears.
 - Add a sub-list **"Where it beats the alternatives"**: the cases where this technology is clearly better than the usual alternatives (what it does that others do not, or do worse). If it has no real edge, say so honestly; do not invent one.
5. Draft **1-2 short examples** (code, command or config). Verify them against the docs; do not invent APIs.
6. **Show the draft for review, visually** (see below). Do not write the `.md` file yet.
7. Only after the author approves (apply requested changes first), generate the concept document in the bundle, following the format below. Set `generated.at` to the current time and `generated.by` to yourself.
8. Check the writing rules and the checklist at the end of this file.

The choice of what to add is the author's, and it is subjective. Do not filter or second-guess it; your job is duplicates, quality of the card and the licensing rules below.

## Third-party material: hard rules

The cards are published under CC BY 4.0 (see [LICENSE-CONTENT](LICENSE-CONTENT)) and the author is responsible for every word on the site. These rules are **not optional**. If you cannot satisfy them, leave the material out and tell the author.

1. **Write the card in your own words.** Never paste prose from the source site, README or docs. Rephrase from understanding. A verbatim sentence from the source is a bug, even if it is short.
2. **Prefer your own examples.** Write the smallest example that shows the point, and verify it against the docs. Copy an example from the source only when writing your own would be wrong or misleading (for example, an exact config key or command syntax).
3. **Check the license before copying anything**, code or text. Look for a `LICENSE` file, a license line in the README, a footer on the docs site, or a terms page. Then:
 - Permissive license (MIT, Apache-2.0, BSD, CC BY, CC0, public domain, or an explicit "examples may be freely used" statement): a short snippet is fine, with attribution (rule 4).
 - Copyleft (GPL, CC BY-SA, ...): keep the copied part minimal and attribute; prefer rewriting.
 - No license found, "all rights reserved", proprietary docs, paywalled or login-only content, blog posts, Stack Overflow answers, books: **do not copy**. Rewrite from scratch or omit.
 - If unsure, treat it as "no license found".
4. **Cite every source.** List each page you took facts, quotes or snippets from in the `sources` frontmatter (`{ resource, id?, title? }`). In the body, put a footnote matching the `id` next to copied snippets and non-obvious claims. The `resource` field alone is not a citation for copied material.
5. **Record the license of anything copied.** Add a short note next to the snippet or in `sources` (`title: "Official docs, Apache-2.0"`), so the author can see at a glance what was taken and under which terms.
6. **No images, logos or screenshots** from third-party sites. Cards are text and code only.
7. **Never present copied material as the author's.** If a quote is needed, mark it as a quote (`>`) and name the source.

In the visual review (see below), state explicitly which parts, if any, are copied, from where and under which license, so the author approves that too.

### Visual review

- Render the draft as a **single card, as it will look on the site**: name, one-sentence description, "When it is useful" bullets (with the "Where it beats the alternatives" sub-list), examples, link, date. Use the Artifact tool (private HTML page) so the author sees it rendered, not as raw Markdown.
- Keep it faithful to the final result: same content, same order. What the author approves is what gets generated.
- If the author asks for changes, update the same artifact (same file path), do not create a new one.

### Generated Markdown

The `.md` file must read well as a **visual card** on the site: short sentences, bullets, a code block, no walls of text. Prefer visual structure (headings, lists, code fences, a small table or diagram when it explains faster than words) over prose.

A `SessionStart` hook (`.claude/hooks/session-start.sh`) reminds the author of this command at the start of each session.


## Storage format

The short description of each technology is saved in an **OKF bundle** (Google's format for storing data that LLMs can process).

Spec (v0.2): <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>. Re-read it when in doubt; it wins over this summary.

- The bundle root is `docs/`. All concept files live there, flat (no subfolders for now).
- One technology = one concept document = one `.md` file. The Concept ID is the file path without `.md`.
- Every concept file is UTF-8 Markdown with YAML frontmatter (`---`) followed by the body.
- Do not invent fields outside the spec. Extra keys are allowed by OKF, but keep them to a minimum.

### Frontmatter

| Key | Status | Use in this repo |
|---|---|---|
| `type` | **required**, non-empty | Always `Technology` |
| `title` | recommended | Technology name |
| `description` | recommended | One sentence: what it is |
| `resource` | recommended | Official site or repo URL |
| `tags` | recommended | Short lowercase list. Mix stack tags with **problem tags** so the card is findable by need, e.g. `[database, rust, embedded, zero-config]` |
| `generated` | optional | `{ by: <actor>, at: <ISO 8601 UTC> }`. `at` is the **publication date** used to order the feed |
| `verified` | optional | List of `{ by, at }`. Use `human:<id>` only when a human actually confirmed it |
| `sources` | optional | List of `{ resource, id?, title? }`; cite claims with footnotes matching `id` |
| `status` | optional | `draft`, `stable` (default) or `deprecated` |
| `stale_after` | optional | ISO 8601 UTC instant after which the card is stale |

Actors: `<producer>/<version>` for agents (e.g. `claude/sonnet-5.5`), `human:<id>` for people, `process:<id>` for automation.

Example:

```markdown
---
type: Technology
title: Example Tech
description: One plain sentence saying what it is.
resource: https://example.com
tags: [example]
generated: { by: claude/sonnet-5.5, at: 2026-10-24T09:00:00Z }
---

Why it is interesting, in two or three lines.

# When it is useful

- Concrete situation 1
- Concrete situation 2

**Where it beats the alternatives**

- Concrete edge over the usual alternative

# Example

(tiny code block)
```

### Body

- Standard Markdown. Prefer structure (headings, lists, code fences) over prose.
- No required sections; conventional headings are `# Examples` and `# Schema`.
- Links: standard Markdown, bundle-relative paths starting with `/` preferred.

### Reserved files

- `index.md` and `log.md` are reserved at any level. Never use them for a concept.
- `index.md` has no frontmatter, except the bundle-root one may carry `okf_version: "0.2"`.
- `log.md` has date-grouped entries under `YYYY-MM-DD` headings, newest first.

### Conformance

A bundle is valid if every non-reserved `.md` has parseable YAML frontmatter with a non-empty `type`, and reserved files follow their structure. Missing optional fields, unknown keys and broken links must not break it.

## Publishing target

The Markdown files will be turned into a **GitHub Pages site with MkDocs**. Keep this in mind for every change:

- Entries must be plain Markdown that MkDocs renders well.
- Every entry needs a **publication date**, stored in `generated.at`. The date is part of the content.
- The site is a **feed of cards** (micro content, "Did you know X exists?"), newest first. Each entry is one card, not a page in a documentation tree.
- Do not rely on cross-page navigation or detail pages. There may be no other pages: the intro/feed page is the only one.
- Exception: `hooks/feed.py` also writes `/share/<slug>/` for each card at build time (Open Graph tags, a generated 1200x630 `og.png`, instant redirect to `/#<title-slug>`). They exist only so a link pasted into LinkedIn and similar sites shows a preview of that card. They are not part of the feed and are not linked from it. Share links to post: `https://radudumbraveanu.github.io/toc/share/<slug>/`, where `<slug>` is the card file name without `.md`.

## Writing rules for entries

Narration must be **very clear and understandable from the first read**. The reader sees only the card.

- Open with what the technology is, in one plain sentence.
- Then why it is interesting (the "I didn't know this existed" hook).
- Then **when it is useful**: 2-4 short bullets with concrete situations ("use it when you need X", "instead of Y when Z"), with a sub-list of 1-3 bullets on where it beats the alternatives. Each bullet is a trigger the author would recognize later, not a feature.
- Then a tiny example, if it helps.
- Link to the official site/docs for anyone who wants more.
- Be succinct. No filler, no jargon without explanation, no assumed prior knowledge.
- Self-contained: never depend on another entry to be understood.
- English only.

## Checklist before finishing

- [ ] No existing card for the same technology in `docs/`
- [ ] Frontmatter has `type`; `title`, `description`, `resource`, `tags` filled (tags include at least one problem tag)
- [ ] Date present and correct (`generated.at`)
- [ ] First sentence explains what the technology is
- [ ] Says when the technology is useful (concrete situations) and where it beats the alternatives (or honestly says it has no clear edge)
- [ ] Understandable with no other context
- [ ] Example (if any) is short and correct
- [ ] No verbatim prose from the source; any copied snippet has a checked permissive license and is cited in `sources` with a footnote
- [ ] Entry stored in the OKF bundle
- [ ] Renders correctly in MkDocs
