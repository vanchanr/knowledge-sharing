# Databases — From Basics to Expert

## Relational Databases
- **PostgreSQL**
- **Normalization**
- **DB migrations**
- **SQL**
- **DB indexes**
- **Query performance analysis**

## NoSQL
- **Key Value**
- **Document**
- **Wide Column**
- **Graph**
- **Timeseries**

## ORMs
- **ACID**
- **Transactions**
- **N+1 problem**

---

## Core Concepts
- **Database**: An organized collection of data for efficient storage, retrieval, update, and management.
- **DBMS vs RDBMS**: DBMS = general data store; RDBMS = relational model with tables, rows, and relationships (MySQL, PostgreSQL, Oracle, SQL Server).
- **Schema**: The logical structure of a database — tables, columns, types, constraints, relationships.
- **Table**: A collection of rows (records) and columns (attributes) with a defined schema.
- **Primary key**: Uniquely identifies each row; must be unique and non-null; often auto-increment (SERIAL/IDENTITY) or UUID.
- **Foreign key**: References the primary key of another table — enforces referential integrity (no orphan rows).
- **Composite key**: A primary key made of multiple columns — used when no single column is unique.
- **Entity-Relationship (ER) model**: Conceptual design with entities, attributes, and relationships (1:1, 1:N, N:M).
- **Constraints**: NOT NULL, UNIQUE, CHECK, DEFAULT, PRIMARY KEY, FOREIGN KEY — enforce data integrity at the DB level.

## Normalization & Schema Design
- **1NF (First Normal Form)**: Atomic values only — no repeating groups or arrays in a column.
- **2NF (Second Normal Form)**: 1NF + no partial dependency — every non-key column depends on the whole composite key.
- **3NF (Third Normal Form)**: 2NF + no transitive dependency — non-key columns don't depend on other non-key columns.
- **BCNF (Boyce-Codd Normal Form)**: Stricter than 3NF — every determinant must be a candidate key.
- **Denormalization**: Deliberately adding redundancy (duplicated data, precomputed columns) for read performance in read-heavy systems.
- **Surrogate vs natural keys**: Surrogate (autoincrement/UUID, no business meaning) vs natural (SSN, email) — surrogate preferred for stability.
- **Star schema**: Central fact table linked to dimension tables — classic data warehouse design for analytics (OLAP).
- **Snowflake schema**: Star schema with normalized (further split) dimension tables — less redundancy, more joins.
- **Database migrations**: Version-controlled schema changes (Flyway, Liquibase, Alembic) — apply incrementally, reversible, tested.
- **Migration best practices**: Never edit an applied migration; each migration is one logical change; test on staging first.
- **Index-friendly schema**: Queries drive schema design — model for how data is read, not just how it's written.

## SQL Mastery
- **SELECT**: Query data — `SELECT *` is a red flag; always list columns explicitly.
- **WHERE**: Filter rows — use indexed columns, avoid wrapping columns in functions (breaks index usage).
- **JOIN types**: INNER (only matches), LEFT (all left + matches), RIGHT, FULL OUTER — understand row semantics.
- **JOIN vs subquery**: JOINs are usually faster; subqueries useful for aggregation and "IN" patterns; correlated subqueries can be slow.
- **GROUP BY**: Aggregate rows — every non-aggregated column in SELECT must appear in GROUP BY.
- **HAVING vs WHERE**: HAVING filters after aggregation (groups); WHERE filters rows before aggregation — HAVING is slower, use WHERE first.
- **ORDER BY**: Sort results — use indexes for common sorts; `NULLS FIRST/LAST` (PG).
- **LIMIT/OFFSET vs keyset pagination**: OFFSET scans skipped rows (O(N)); keyset (`WHERE id > last_id ORDER BY id LIMIT 20`) is faster for big tables.
- **Aggregates**: COUNT, SUM, AVG, MIN, MAX — COUNT(*) vs COUNT(col) matters (nulls).
- **DISTINCT vs GROUP BY**: Both deduplicate — GROUP BY allows aggregates; DISTINCT on high-cardinality can be slow.
- **Window functions**: Compute values across rows relative to the current row — ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, SUM(...) OVER (PARTITION BY ...).
- **Window function examples**: Running totals, moving averages, top-N per group, row comparison (LAG), deduplication (ROW_NUMBER = 1).
- **Subqueries**: `WHERE x IN (SELECT ...)`, `EXISTS` — EXISTS is often faster than IN for large sets (stops at first hit).
- **CTEs (Common Table Expressions)**: `WITH cte AS (...) SELECT ...` — readability, recursion (`WITH RECURSIVE`), and temporary results.
- **CASE WHEN**: Conditional logic in SQL — pivoting, conditional aggregation.
- **COALESCE/NULLIF**: COALESCE = first non-null; NULLIF(a, b) = NULL if equal (avoid divide-by-zero).
- **String functions**: CONCAT, SUBSTRING, LENGTH, UPPER/LOWER, TRIM, REPLACE, SPLIT_PART.
- **Date/time functions**: NOW(), CURRENT_DATE, DATE_TRUNC (PG), INTERVAL math, EXTRACT — beware timezone handling.
- **EXPLAIN/EXPLAIN ANALYZE**: Read the query plan — seq scan vs index scan vs bitmap scan, join types, row estimates.
- **Transaction control**: BEGIN, COMMIT, ROLLBACK, SAVEPOINT — atomic units of work.
- **UPSERT**: `INSERT ... ON CONFLICT DO UPDATE` (PG) / `ON DUPLICATE KEY UPDATE` (MySQL) — insert or update atomically.
- **Locks in SQL**: `SELECT ... FOR UPDATE` (row-level lock for pessimistic concurrency), table locks, advisory locks.
- **SET operations**: UNION (dedup), UNION ALL (faster, no dedup), INTERSECT, EXCEPT.

## Indexing Deep Dive
- **B-tree index (default)**: Balanced tree — good for equality and range queries (>, <, BETWEEN, prefix match).
- **Composite (multi-column) index**: Order matters — leftmost prefix rule; `(a, b, c)` serves WHERE a / a+b / a+b+c.
- **Covering index**: Index includes all columns needed by the query — avoids table heap lookup (index-only scan).
- **Unique index**: Enforces uniqueness (auto-created for PK/UNIQUE constraints).
- **Partial index**: Index on a subset of rows (`WHERE status = 'active'`) — smaller, faster for filtered queries (PG).
- **Expression/functional index**: Index on `LOWER(email)`, `(created_at::date)` — enables function-based lookups.
- **Bitmap index**: For low-cardinality columns (e.g., gender, status) — used by some engines (Oracle, PG bitmap scans).
- **Hash index**: Equality-only, very fast — rarely needed on modern B-trees (better range support).
- **Inverted index (GIN/trigram)**: For full-text search, JSONB, arrays — `@@`, `ILIKE '%x%'` via pg_trgm.
- **Index scan vs seq scan**: DB uses index when selectivity is high; full scan can be faster for small tables or fetching most rows.
- **Index on FK columns**: Prevents locks and speeds up JOIN/ON DELETE CASCADE operations.
- **Index maintenance**: Writes cost more (each index updated per write) — index what you query, not everything.
- **Index bloat**: Dead tuples in indexes after updates/deletes — VACUUM/REBUILD (PG) to reclaim space.
- **`ANALYZE`/statistics**: Up-to-date planner statistics are critical for good query plans.
- **Index visibility**: `pg_stat_activity`, `pg_stat_user_indexes` (PG) — check unused indexes to drop.

## Transactions & Concurrency
- **ACID**: Atomicity (all-or-nothing), Consistency (valid state), Isolation (concurrent ops don't interfere), Durability (committed survives crash).
- **Atomicity**: Via undo logs (MySQL), MVCC (PG), or rollback segments — all statements in a transaction commit or roll back together.
- **Isolation levels**: Read Uncommitted (dirty reads), Read Committed (default PG/Oracle, no dirty reads), Repeatable Read (default MySQL), Serializable (full).
- **Dirty read**: Reading uncommitted data — prevented by Read Committed and above.
- **Non-repeatable read**: Same query returns different rows in one transaction (another txn committed) — prevented by Repeatable Read.
- **Phantom read**: New rows appear in repeated range queries — prevented by Serializable (or PG Repeatable Read with SSI).
- **MVCC (Multi-Version Concurrency Control)**: Readers don't block writers — each transaction sees a snapshot via versioned rows (PG, MySQL InnoDB).
- **Pessimistic locking**: Lock rows upfront (`SELECT ... FOR UPDATE`) — simpler, lower concurrency.
- **Optimistic locking**: Version/timestamp column — update fails if version changed; retry the transaction (higher concurrency).
- **Deadlocks**: Two txns hold locks each other needs — DB detects and rolls back one; retry on error 40P01 (PG) / 1213 (MySQL).
- **Lock granularity**: Row, page, table, gap, next-key locks — InnoDB uses next-key (row + gap) to prevent phantoms.
- **Gap locks**: Lock the space between index entries (InnoDB) — prevent inserts in range; can cause deadlocks with SELECT FOR UPDATE.
- **Transaction best practices**: Keep txns short, do I/O outside, no network calls inside, retry deadlocks, set timeouts (`lock_timeout`, `statement_timeout`).

## NoSQL Overview
- **Why NoSQL**: Horizontal scale-out, flexible schema, high write throughput, specialized data models — at the cost of consistency/complexity.
- **Key-Value stores**: Redis, DynamoDB, Memcached — simple get/set by key, ultra-low latency; cache, sessions, counters.
- **Document stores**: MongoDB, CouchDB, DynamoDB — JSON documents, flexible schema, embedded sub-documents; content, catalogs, profiles.
- **Wide-column stores**: Cassandra, HBase, ScyllaDB — column families, sparse data, massive scale; time-series, IoT, event logs.
- **Graph databases**: Neo4j, Neptune, ArangoDB — nodes/edges; social networks, recommendation, fraud detection.
- **Time-series DBs**: InfluxDB, TimescaleDB, Prometheus — optimized for timestamped metrics; monitoring, IoT.
- **Multi-model**: Some DBs support several models (DynamoDB key-value+document, CosmosDB multi-model).
- **Columnar stores**: Redshift, ClickHouse, Snowflake — column-oriented storage for OLAP analytics (compression, scan efficiency).

## Relational vs NoSQL Trade-offs
- **When to use SQL**: Strong consistency needs, complex joins/transactions, OLTP with relational data, reporting.
- **When to use NoSQL**: Massive scale-out, flexible/evolving schema, high write throughput, simple access patterns.
- **ACID vs BASE**: SQL gives ACID (strong consistency); NoSQL often BASE — Basically Available, Soft state, Eventually Consistent.
- **Consistency models**: Strong, eventual, causal, read-your-writes — pick per workload.
- **CAP theorem**: In partition, pick Consistency or Availability — SQL (CP-ish), most K/V (AP, eventually consistent).
- **Single-machine vs distributed**: Most SQL scales up (bigger box); NoSQL designed for scale-out (sharding built-in).
- **The polyglot persistence pattern**: Use multiple DBs for different workloads (SQL for orders, Redis for cache, Elasticsearch for search).

## Query Performance Analysis
- **EXPLAIN**: Show query plan — table access method (seq/idx), join (nested loop/hash/merge), sort/hash ops, estimated rows.
- **EXPLAIN ANALYZE**: Actually execute and report real times/rows — compare estimates vs actual (stats freshness).
- **Common red flags**: Seq scan on big tables, nested loops with huge inner scans, high "rows removed by filter", temp files.
- **Hash join**: Small build + large probe — usually efficient; happens when no join index.
- **Nested loop join**: For each outer row, probe inner — good with indexes and small outer sets.
- **Merge join**: Requires sorted inputs — rare; uses index order; then merge.
- **`pg_stat_statements` / `performance_schema`**: Find the most expensive repeated queries in production.
- **Slow query log**: Enable thresholds (e.g., `log_min_duration_statement` = 100ms) to capture offenders.
- **Index usage stats**: `pg_stat_user_indexes` (idx_scan > 0?), `sys.dm_db_index_usage_stats` (SQL Server).
- **Buffer cache hit ratio**: High % means reads come from memory — low ratio = scale memory or redesign queries.
- **Query rewrite patterns**: Avoid `SELECT *`, avoid functions on indexed cols in WHERE, use EXISTS over IN, pre-aggregate.

## ORMs (Object-Relational Mappers)
- **ORM purpose**: Map objects/classes to relational tables — reduce boilerplate, gain type safety (Hibernate, ActiveRecord, SQLAlchemy, Prisma).
- **The N+1 problem**: Loading a list of entities then one query per child — fix: eager loading (JOIN/IN), batches, or lazy-load carefully.
- **Lazy vs eager loading**: Lazy = load on first access (N+1 risk); eager = pre-load with JOIN/IN — choose per use case.
- **Session/unit of work**: ORM tracks changes and flushes at transaction commit (dirty checking) — batch DB writes.
- **Identity map**: ORM caches entities by ID in the session — same ID returns same object (but stale data risk).
- **Migrations via ORM**: Generate schema migrations from models (Alembic, Flyway, Prisma migrate) — review generated SQL!
- **ORM pitfalls**: Over-fetching, cartesian explosion (too many JOINs), magic SQL hiding, N+1, lazy-load in serialization (LazyInitializationException).
- **ORM vs raw SQL**: ORM for CRUD and common paths; raw SQL for complex analytics, bulk ops, or query tuning.
- **Criteria/query builder middleware**: Type-safe query composition between ORM and raw SQL.
- **Connection management**: ORM pools and binds sessions to requests — watch for leaks and long-lived sessions.
- **Batch inserts**: ORM bulk operations dramatically faster (single statement vs per-row) — know your ORM's bulk API.
- **Optimistic locking via ORM**: @Version column everywhere — retries on `OptimisticLockException`.

## Database Operations & Reliability
- **Backups**: Full (periodic) + incremental/WAL (continuous) — RPO is the backup frequency; RTO is restore time.
- **Point-in-time recovery (PITR)**: Full backup + WAL/log replay — restore to any minute (RDS, Barman, pgBackRest).
- **Restore testing**: Backups are worthless until you've tested a restore — do it quarterly.
- **High availability (HA)**: Primary/standby (sync replication for zero data loss in PG/MySQL); automatic failover (Patroni, RDS Multi-AZ, Orchestrator).
- **Read replicas**: Async copies for read scaling — stale reads possible; master handles writes.
- **Failover considerations**: Connection strings (VIP/DNS), uncommitted transactions, replica promotion lag.
- **Connection pooling**: PgBouncer (transaction pooling), HikariCP (app-side) — avoid connection exhaustion at scale.
- **Schema change strategies**: Expand-contract (add column nullable → backfill → set NOT NULL), pt-online-schema-change, gh-ost for zero-downtime.
- **Zero-downtime migration**: Duplicate table → dual-write → switch reads → drop old (green-blue for DB).
- **Capacity planning**: Watch disk, connections, CPU, memory, IOPS trends; plan 60-70% thresholds.
- **Monitoring**: Query latency (p95/p99), slow queries, lock waits, replication lag, free disk, connection count.

## Common Pitfalls & Troubleshooting
- **`SELECT *` on huge tables**: Transfers and materializes everything — list columns.
- **Missing index on FK**: JOINs and deletes crawl — add indexes on all FK columns.
- **Implicit type conversion**: `WHERE varchar_col = 123` — prevents index use; always match types.
- **`OR` across columns**: Prevents index usage — use UNION ALL or rethink.
- **Leading wildcard `LIKE '%xyz'`**: Cannot use B-tree index — pg_trgm (GIN) or full-text search.
- **`OFFSET` on huge pages**: O(N) scan — keyset/seek pagination.
- **Too many indexes**: Each slows writes and bloats disk — drop unused (check usage stats).
- **No deadlock retry**: Production deadlocks are normal — implement retry (with jitter).
- **Lock contention**: One long txn blocks many — keep transactions short, inspect `pg_locks`/`information_schema.innodb_trx`.
- **Replication lag causing reads**: Route critical reads to primary, or accept staleness (bounded).
- **Unbounded tables**: Old data slows everything — partition by date, archive/delete old rows.
- **VACUUM never runs (PG)**: Bloat and transaction-ID wraparound — autovacuum tuning is production-critical on PG.