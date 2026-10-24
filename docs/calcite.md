---
type: Technology
title: Apache Calcite
description: A Java framework with a SQL parser, validator, cost-based optimizer and JDBC driver, for running SQL over data that does not live in a SQL database.
resource: https://calcite.apache.org/
tags: [java, sql, query-engine, federated-query, sql-over-files]
generated: { by: claude/sonnet-5.5, at: 2026-10-24T09:30:00Z }
sources:
  - { resource: https://calcite.apache.org/, id: home, title: "Calcite home page, Apache License v2" }
  - { resource: https://calcite.apache.org/docs/tutorial.html, id: tutorial, title: "Calcite tutorial, Apache License v2" }
---

Calcite is the SQL brain without the storage. It parses SQL, turns it into relational algebra, optimizes it, and hands the work to whatever data source you plug in.[^home]

You write only the connector. Calcite gives you SQL, planning rules and a JDBC driver on top of it.

# When it is useful

- You have CSV or JSON files, an API or in-memory objects and want to query them with plain SQL.
- You are building your own database, query engine or data product and do not want to write a SQL parser and planner.
- You need one query that joins data from several systems.
- You need to parse, validate or rewrite SQL in code, for example for linting, lineage or access rules.

**Where it beats the alternatives**

- Versus writing your own parser and planner: both exist, with a rule-based, cost-based optimizer you can extend.
- Versus loading everything into H2 or SQLite first: it queries data where it is and can push filters and joins down to the source.
- No edge when you only need to query local files from a script. DuckDB is simpler there. Calcite is a library, not a database.

# Example

Describe a folder of CSV files as a schema in `model.json`:[^tutorial]

```json5
{
  version: '1.0',
  defaultSchema: 'SALES',
  schemas: [{
    name: 'SALES',
    type: 'custom',
    factory: 'org.apache.calcite.adapter.csv.CsvSchemaFactory',
    operand: { directory: 'data' }
  }]
}
```

Query it through JDBC:

```java
Connection c = DriverManager.getConnection("jdbc:calcite:model=model.json");
ResultSet rs = c.createStatement().executeQuery("select * from emps");
```

Each `.csv` file in `data/` becomes a table. The CSV adapter is the tutorial's sample module, so you write your own adapter for other sources.

More: [calcite.apache.org](https://calcite.apache.org/)

[^home]: Calcite home page. Facts only, rephrased.
[^tutorial]: Calcite tutorial. Model structure and connect string adapted, with a different directory name and a short query. Docs are under Apache License v2.
