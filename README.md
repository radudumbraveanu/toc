# toc

**toc** stands for **table of contents**.

A collection of short descriptions and small examples of technologies the author found interesting. Most of them have no immediate use, but an occasion to use them may appear in the future, and this is the place to remember they exist.

## The toc method

First get the big picture, then learn the details only when a real need appears.

Knowing that X exists and what problem it solves is often enough. The deep dive can wait until the problem shows up. Each card is a hook to hang the details on later.

The idea comes from Barbara Oakley (*A Mind for Numbers*, *Learning How to Learn*): before reading a chapter, do a "picture walk" through its headings, pictures and summary. The overview gives your brain hooks, and the details stick to them when you finally read them.

It works in two phases:

1. **Scan**: note that X exists, what it is and **when it is useful**. No details.
2. **Return**: when a problem shows up, come back to the card, follow its link and only then study X in depth.

Phase 2 is why every card must be findable by the **problem it solves**, not only by the name of the technology.

## The idea

Think of toc as a feed of **"Did you know technology X exists?"** cards.

The reaction it aims for: *"I didn't know X existed, but it looks interesting."*

Each entry is micro content:

- short and self-contained, understandable at first read
- dated, because the day it was published matters
- one technology per card: what it is, why it is interesting, **when it is useful** (the most important part), a tiny example

There is no deep dive here. If an entry makes you curious, follow its link to the official docs.

## Who it is for

First, the author: this is an external memory, and the selection is personal. Second, anyone who enjoys finding out that something exists.

## How it is built

- Entries are Markdown files, stored as an OKF bundle (see [AGENTS.md](AGENTS.md)).
- The site is generated with [MkDocs](https://www.mkdocs.org/) and published on GitHub Pages.
- The site is rendered as a feed, newest cards first.

## License

Copyright (c) 2026 Radu Dumbrăveanu <radu.dumbraveanu@gmail.com>

- **Content** (the cards in `docs/`, this README): [CC BY 4.0](LICENSE-CONTENT). Copy, modify, reuse; just credit the author.
- **Code and configuration** (`hooks/`, `mkdocs.yml`, workflows): [MIT](LICENSE).

Short examples or quotes taken from third-party documentation stay under their original license and are cited in the card.
