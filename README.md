# toc

**toc** stands for **table of contents**.

A collection of short descriptions and small examples of technologies the author found interesting. Most of them have no immediate use, but an occasion to use them may appear in the future, and this is the place to remember they exist.

## The idea

Think of ToC as a feed of **"Did you know technology X exists?"** cards.

The reaction it aims for: *"I didn't know X existed, but it looks interesting."*

Each entry is micro content:

- short and self-contained, understandable at first read
- dated, because the day it was published matters
- one technology per card: what it is, why it is interesting, a tiny example

There is no deep dive here. If an entry makes you curious, follow its link to the official docs.

## How it is built

- Entries are Markdown files, stored as an OKF bundle (see [AGENTS.md](AGENTS.md)).
- The site is generated with [MkDocs](https://www.mkdocs.org/) and published on GitHub Pages.
- The site is rendered as a feed, newest cards first.
