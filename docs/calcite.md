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
  - { resource: https://calcite.apache.org/docs/model.html, id: model, title: "Calcite JSON/YAML models, Apache License v2" }
  - { resource: https://github.com/apache/calcite/blob/main/core/src/test/java/org/apache/calcite/test/MultiJdbcSchemaJoinTest.java, id: multijdbc, title: "MultiJdbcSchemaJoinTest, Apache License v2" }
  - { resource: https://jobs.picnic.app/en/blogs/enabling-rapid-business-use-case-iteration-with-apache-calcite, id: picnic, title: "Picnic engineering blog, facts only" }
  - { resource: https://www.besthub.dev/articles/design-and-practice-of-360-s-multi-data-source-unified-sql-query-engine-c6867d31eb6c, id: quicksql, title: "360 QuickSQL article, facts only" }
---

Calcite is the SQL brain without the storage. It parses SQL, turns it into relational algebra, optimizes it, and hands the work to whatever data source you plug in.[^home]

You write only the connector. Calcite gives you SQL, planning rules and a JDBC driver on top of it.

# When it is useful

- You have CSV or JSON files, an API or in-memory objects and want to query them with plain SQL.
- You are building your own database, query engine or data product and do not want to write a SQL parser and planner.
- You have several microservices, each with its own database, and need a read-only report or internal tool that joins data across them without building a new API for every question.
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

# Example: join across two microservice databases

Two JDBC schemas in `model.json`,[^model] one query:

```json5
{
  version: '1.0',
  schemas: [
    { name: 'ORDERS', type: 'jdbc', jdbcUrl: 'jdbc:postgresql://orders-db/orders' },
    { name: 'USERS',  type: 'jdbc', jdbcUrl: 'jdbc:postgresql://users-db/users' }
  ]
}
```

```sql
SELECT u.email, COUNT(*) AS orders
FROM ORDERS.orders o JOIN USERS.users u ON o.user_id = u.id
GROUP BY u.email
```

Calcite pushes each side's filters to its database and does the join itself, in memory.[^tutorial] Good for reports and internal tools, not for the hot path. Reading another service's database directly also bypasses that service's API.

**Used in practice**

- [Picnic](https://jobs.picnic.app/en/blogs/enabling-rapid-business-use-case-iteration-with-apache-calcite) runs this in production over a microservice architecture. They wrap service APIs as Calcite tables instead of connecting to the databases, and analysts join them in SQL. Query planning became a latency problem, so they cache and share plans.[^picnic]
- [360's QuickSQL](https://www.besthub.dev/articles/design-and-practice-of-360-s-multi-data-source-unified-sql-query-engine-c6867d31eb6c) uses Calcite as a SQL facade over MySQL, Hive and Elasticsearch with cross-source joins. A data platform, not microservices, but the same mechanism.[^quicksql]
- The multi-JDBC join is an official feature: the [tutorial](https://calcite.apache.org/docs/tutorial.html#jdbc-adapter) says Calcite pushes what it can to each JDBC source and handles the rest itself, and [`MultiJdbcSchemaJoinTest`](https://github.com/apache/calcite/blob/main/core/src/test/java/org/apache/calcite/test/MultiJdbcSchemaJoinTest.java) covers exactly that case.[^multijdbc]

More: [calcite.apache.org](https://calcite.apache.org/)

[^home]: Calcite home page. Facts only, rephrased.
[^tutorial]: Calcite tutorial. Model structure and connect string adapted, with a different directory name and a short query; pushdown behavior of the JDBC adapter rephrased. Docs are under Apache License v2.
[^model]: Calcite model reference, `type: 'jdbc'` schema shape. Example written for this card. Apache License v2.
[^multijdbc]: Calcite test suite, cited as evidence only; nothing copied.
[^picnic]: Picnic engineering blog, facts summarized; nothing copied.
[^quicksql]: 360 QuickSQL article, facts summarized; nothing copied.
