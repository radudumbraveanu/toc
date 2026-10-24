---
type: Technology
title: Jenesis
description: A Java build tool that reads your module-info.java instead of a pom.xml, with companion tools to run modules and package jars.
resource: https://jenesis.build/
tags: [java, build-tool, maven, modules]
generated: { by: claude/sonnet-5.5, at: 2026-10-24T09:00:00Z }
sources:
  - { resource: https://jenesis.build/, id: home, title: "Jenesis home, no license found" }
  - { resource: https://jenesis.build/tool/, id: tool, title: "Jenesis build tool, no license found" }
  - { resource: https://jenesis.build/jpx/, id: jpx, title: "Jenesis jpx, no license found" }
  - { resource: https://jenesis.build/modules/, id: modules, title: "Jenesis Module Index, no license found" }
---

Jenesis is a Java build tool. Your build is plain Java code, and your `module-info.java` tells it what to compile and which dependencies to fetch, so there is no `pom.xml` to maintain.[^home]

It ships with companions: `jpx` runs a published module with one command, a launcher builds modular executable jars, and a module index maps module names to Maven Central artifacts.[^home]

# When it is useful

- You start a new Java project that should be fully modular, and want to skip writing POMs.
- You want to run a published tool or Maven artifact with one command, without a project (`jpx`).
- You want an executable jar that keeps Java modules instead of one merged fat jar.
- You need reproducible builds with pinned, verified dependencies, SBOMs and vulnerability scans, identical on laptop and CI.

**Where it beats the alternatives**

- Versus Maven: the build comes from `module-info.java` and project layout, with little or no build config. Maven dependencies still work through a `requires` line, and your artifacts stay usable from Maven.
- Versus fat jars: the Launcher keeps modularity.
- Versus installing a build tool: it ships as source inside your repo, so it needs only a JDK.

# Example

Declare a dependency by **module name** in `module-info.java`. No `pom.xml`:

```java
module com.example.app {
    requires com.fasterxml.jackson.databind;   // jar found via the Module Index
}
```

Install the tool, then build, test and package using only the JDK:[^tool]

```bash
curl -fsSL https://get.jenesis.build | bash
java build/jenesis/Make.java
```

Run any published module with `jpx`:[^jpx]

```bash
jpx <module-name> <arguments>
```

The module index resolves a module name to its jar by URL:[^modules]

```bash
curl -L -O https://repo.jenesis.build/module/<module-name>/<module-name>.jar
```

Source and license are not published on the site, so check before depending on it.

More: [jenesis.build](https://jenesis.build/)

[^home]: Jenesis home page. No license found; facts only, rephrased.
[^tool]: Jenesis build tool page. No license found; only the exact command syntax is reused.
[^jpx]: Jenesis jpx page. No license found; only the command shape is reused.
[^modules]: Jenesis Module Index page. No license found; only the URL pattern is reused.
