---
type: Technology
title: Jenesis
description: A Java build tool where you write plain Java instead of a pom.xml, and module-info.java drives the whole build.
resource: https://jenesis.build/
tags: [java, build-tool, maven, modules]
generated: { by: claude/sonnet-5.5, at: 2026-10-24T09:00:00Z }
---

Jenesis is a Java build tool where you write plain Java instead of a `pom.xml`, and `module-info.java` drives the whole build.

It comes with a small family of tools: `jpx` (like `npx`, for Java), a launcher for modular executable jars, and a module index for Maven Central.

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
    requires com.fasterxml.jackson.databind;   // resolved via the Module Index
}
```

Then build, test and package with only the JDK:

```bash
curl -fsSL https://get.jenesis.build | bash   # install, needs a JDK
java build/jenesis/Make.java                  # compile, test, package
jpx org.junit.platform.console --version      # run a published module
```

Look up which jar a module name maps to (the build tool does this for you):

```bash
curl -L -O https://repo.jenesis.build/module/com.fasterxml.jackson.databind/com.fasterxml.jackson.databind.jar
```

Source and license are not published on the site, so check before depending on it.

More: [jenesis.build](https://jenesis.build/)
