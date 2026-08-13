# Elasticsearch — From Basics to Expert

## Core Concepts
- **Elasticsearch**: A distributed, RESTful search and analytics engine built on Apache Lucene — great for full-text search, logging analytics, and real-time data exploration.
- **Document**: The basic unit of information stored in Elasticsearch — a JSON object with fields.
- **Index**: A collection of documents that share similar characteristics; analogous to a "database" table in relational DBs.
- **Type**: A categorization within an index (deprecated in 6.x, removed in 7.x; indices now have one mapping).
- **Shard**: A single Lucene index; an index is split into primary and replica shards for distribution and redundancy.
- **Primary shard**: The authoritative copy of data; each document lives on exactly one primary shard.
- **Replica shard**: A copy of a primary shard; provides failover and increases read throughput.
- **Node**: A single server in the cluster that stores data and participates in indexing/search.
- **Cluster**: A collection of nodes that together hold data and provide search/indexing across all nodes.
- **Mapping**: The schema definition — how fields are indexed and stored (types, analyzers, etc.).
- **Inverted index**: The core data structure; maps every term to the documents containing it, enabling fast full-text search.

## Cluster Architecture
- **Node roles**: master-eligible (voting), data, ingest, machine learning, and coordinating-only nodes.
- **Master-eligible node**: Handles cluster-wide operations (index creation, shard allocation, node membership).
- **Data node**: Stores data and executes data-related queries (search, aggregations, indexing).
- **Coordinating node**: Routes requests to the right shards and aggregates results; any node can act as coordinator.
- **Ingest node**: Runs ingest pipelines for document preprocessing (enrichment, parsing, transformation) before indexing.
- **Zen Discovery (7.x) / Cluster formation (8.x)**: How nodes find each other and elect a master (based on quorum).
- **Quorum**: `(master_eligible_nodes / 2) + 1` — minimum number of votes needed to elect a master and avoid split-brain.
- **Split-brain**: When two nodes both think they are master; prevented by the quorum requirement and `discovery.zen.minimum_master_nodes`.
- **Cluster state**: The global metadata (indices, mappings, settings, shard routing) replicated to master-eligible nodes.
- **Shard allocation**: The process of assigning shards to nodes; controlled by allocation awareness, filters, and rerouting.
- **Node discovery**: `discovery.seed_hosts` (7.x+) replaced `discovery.zen.ping.unicast.hosts`.
- **Cluster health**: `green` (all shards assigned), `yellow` (primary shards assigned, replicas not), `red` (some primary shards unassigned).

## Indexing & Documents
- **Indexing a document**: `PUT /index/_doc/1` creates/updates; `POST /index/_doc` auto-generates an ID.
- **_id**: Unique identifier for a document; used for routing to a shard.
- **Routing**: `routing` parameter (or field) determines which shard a document goes to; default is hash of `_id`.
- **Bulk API**: `POST /_bulk` — batch multiple index/update/delete operations in one request for high throughput.
- **Refresh interval**: Controls how often indexed documents become searchable (default 1s; `?refresh=false` for bulk).
- **Near-real-time (NRT)**: Documents are searchable ~1s after indexing due to periodic refresh, not immediately.
- **Flush**: Syncing in-memory segments to disk (every 30s or when translog is full by default).
- **Translog**: Append-only write-ahead log that ensures durability; replayed on recovery.
- **Update**: `POST /index/_update/1` — partial update; internally does get, modify, re-index (version conflicts possible).
- **Delete**: `DELETE /index/_doc/1` — marks document as deleted (not physically removed until segment merge).
- **Versioning**: Optimistic concurrency via `_version` or `if_seq_no`/`if_primary_term` for conflict detection.
- **Refresh vs flush**: Refresh makes data searchable (memory→segment); flush persists segments and clears translog to disk.
- **Update by query**: `POST /index/_update_by_query` — updates documents matching a query (e.g., pipeline changes).
- **Reindex**: `POST /_reindex` — copy documents between indices (used for mapping changes, migrations).

## Mapping & Analysis
- **Explicit mapping**: Define `properties` for each field upfront to control types and analyzers.
- **Dynamic mapping**: Elasticsearch infers field types from the first document (can be surprising; disable in prod if needed).
- **Field types**: `text`, `keyword`, `integer`, `long`, `float`, `double`, `boolean`, `date`, `ip`, `geo_point`, `nested`, `object`.
- **text vs keyword**: `text` is analyzed (full-text search, not aggregatable); `keyword` is exact-match (sortable, aggregatable).
- **Multi-fields**: `"city": { "type": "text", "fields": { "keyword": { "type": "keyword" } } }` — search one way, aggregate another.
- **Analyzer pipeline**: Character filters → tokenizer → token filters; produces the terms in the inverted index.
- **Standard analyzer**: Splits on word boundaries, lowercases, removes most punctuation (default).
- **Custom analyzers**: Combine char filters, tokenizers, and token filters (e.g., ngram for autocomplete, edge_ngram, synonym).
- **Stemming**: Reduces words to root form (e.g., "running" → "run") via token filters like `porter_stem` or `kstem`.
- **Stop words**: Common words removed during analysis to save space and improve relevance (often disabled for phrase search).
- **Normalizers**: Apply to keyword fields for case-insensitive sorting/aggregations (`lowercase`, `asciifolding`).
- **Index-time vs search-time analysis**: The same analyzer is applied at index and search time unless overridden.
- **`ignore_above`**: Limits keyword field length; longer values are not indexed (prevents huge fields).
- **`coerce`**: Automatically converts types (e.g., string "5" to integer 5) — on by default, disable for strictness.
- **`enabled: false`**: Field is stored but not indexed/searched (useful for large blobs you only need to return).
- **`index: false`**: Field is not indexed but can still be stored and returned (e.g., URLs you don't search).

## Query DSL & Search
- **match query**: Full-text search on analyzed fields (e.g., `{ "match": { "message": "hello world" } }`).
- **term query**: Exact match on keyword/numeric fields (do not use on text fields).
- **terms query**: Matches any of a list of exact values (e.g., status IN ['active', 'pending']).
- **range query**: `{ "range": { "age": { "gte": 18, "lt": 30 } } }` — supports gte/gt/lte/lt, dates, numerics.
- **bool query**: Combines `must` (AND), `should` (OR/boost), `must_not` (NOT), `filter` (non-scoring).
- **filter context**: Non-scoring, cacheable — use for filtering (e.g., date ranges, status) to improve performance.
- **query vs filter context**: Query affects relevance scoring; filter is boolean match (yes/no) and is cached.
- **wildcard query**: `{ "wildcard": { "name": "jo*" } }` — slow on text fields; prefer ngram/suffix solutions.
- **prefix query**: Looks for terms starting with a prefix (fast on keyword fields).
- **fuzzy query**: Matches terms within an edit distance (typo tolerance).
- **regexp query**: Allows regex patterns (slow, use sparingly).
- **match_phrase query**: Matches exact phrase with optional `slop` for word-order tolerance.
- **match_phrase_prefix**: Phrase match with prefix on the last term (for search-as-you-type).
- **nested query**: Queries inside `nested` objects (must use `nested` query, not plain match).
- **exists query**: Finds documents where a field exists (`{ "exists": { "field": "user" } }`).
- **multi_match**: Search multiple fields with a single query (types: best_fields, most_fields, cross_fields, phrase).
- **function_score**: Custom scoring — boost by recency, popularity, field values, random, etc.
- **boosting query**: Decreases relevance of documents matching a negative clause.

## Aggregations
- **Metric aggregations**: `avg`, `sum`, `min`, `max`, `cardinality` (unique count), `value_count`, `percentiles`, `stats`.
- **Bucket aggregations**: `terms` (group by field), `date_histogram` (time buckets), `range`, `histogram`, `filter`, `nested`.
- **Pipeline aggregations**: Compute from other aggregations (e.g., `avg_bucket`, `cumulative_sum`, `derivative`, `moving_avg`).
- **`terms` aggregation**: Group by field; use on `keyword` (not `text`); set `size` for top-N; watch `doc_count_error_upper_bound`.
- **`date_histogram`**: Time-series bucketing with `calendar_interval` (e.g., `1d`) or `fixed_interval` (e.g., `90m`).
- **Nested aggregations**: Buckets within buckets (e.g., terms → date_histogram → percentiles).
- **`cardinality` precision**: Approximate count with `precision_threshold` (default 3000) and memory trade-off.
- **Percentiles**: Approximate (TDigest algorithm); useful for latency SLOs (p50, p95, p99).
- **Pipeline aggregations need `buckets_path`**: Reference the path to the parent aggregation's output.
- **`significant_terms`**: Finds statistically interesting/unusual terms in a subset vs the whole corpus.
- **Composite aggregation**: Paginated/sliced buckets for many unique values (avoids `terms` size limits).
- **Aggregation on `nested`**: Must use `nested` aggregation wrapping the sub-aggregation.

## Relevance & Scoring
- **TF-IDF**: Term Frequency × Inverse Document Frequency — measures how important a term is to a document in a corpus.
- **BM25**: Default similarity in ES 5+; replaces TF-IDF; handles term saturation and field length normalization.
- **Scoring formula**: Sum of term scores across matching clauses; `_score` is a float (highest = most relevant).
- **Boosting**: `boost` on queries or fields to weight importance (e.g., title > body).
- **`should` + `minimum_should_match`**: Control how many should clauses must match (for OR semantics).
- **`minimum_should_match` on match**: e.g., `"75%"` — require 75% of terms to match (great for typo tolerance).
- **`_explain` API**: `GET /index/_explain` — understand why a doc got a particular score (debugging relevance).
- **Synonyms**: `synonym` token filter to treat related terms as equal (e.g., "car" = "automobile").
- **Stopword removal**: Improves precision but can hurt phrase search; use `stop` filter carefully.
- **Index-time vs query-time boosting**: Query-time boosting is more flexible; index-time boosts affect all queries on the field.
- **Constant score**: Wrap a query in `constant_score` to ignore scoring (useful with filters).
- **`rescore`**: Second-pass scoring to refine top-N results (e.g., rescore top 50 with a slow but accurate query).

## Operations & Production
- **Backup**: Snapshot and restore API — take snapshots to a repository (S3, GCS, Azure, shared FS).
- **Snapshot lifecycle management (SLM)**: Automate scheduled snapshots with retention policies.
- **Monitoring**: `_cat/health` (cluster status), `_cat/nodes` (node stats), `_cat/indices`, `_cluster/health`.
- **Node stats**: `_nodes/stats` — CPU, memory, disk, JVM, thread pools, indexing/search throughput.
- **Important metrics**: Heap usage (keep < 75% JVM), CPU, disk space, search/index latency, rejected requests.
- **JVM heap sizing**: Set `-Xms` = `-Xmx` (default 1GB; recommend up to 50% of RAM, max ~30GB for compressed oops).
- **`fielddata`**: In-memory data structure for aggregations/sorting on text fields (avoid; use keyword).
- **`circuit_breaker`**: Prevents OOM from excessive memory use (parent circuit breaker ~95% of heap).
- **`index.refresh_interval`**: Tune upward for bulk ingestion (e.g., `30s` or `-1` for no refresh) to improve indexing throughput.
- **Bulk sizing**: ~5–15 MB per bulk request is a good starting point; tune based on hardware.
- **Replica configuration**: More replicas = more read throughput and redundancy; each replica adds disk and network overhead.
- **Shard sizing rule of thumb**: Keep shards between 10–50 GB; ~20–40 shards per GB of heap.
- **Too many shards**: "this action would add [X] total shards" — the `cluster.max_shards_per_node` limit (default 1000).
- **Rollover**: `POST /<index>-write/_rollover` — automatically create a new index when conditions met (size, docs, age).
- **Index lifecycle management (ILM)**: Automate hot → warm → cold → frozen → delete phases with rollover and snapshots.
- **Index templates**: Define settings/mappings for indices matching a pattern (e.g., `logs-*`).
- **Component templates**: Reusable building blocks for index templates (mappings, settings, aliases).
- **Aliases**: Named pointers to one or more indices; `index:false` on aliases for write routing; zero-downtime reindexing.
- **Cluster routing allocation**: `cluster.routing.allocation.enable` (all/primaries/none) to control shard movement during maintenance.
- **Rolling restart**: Stop node, upgrade, restart one at a time; use `_cluster/settings` to disable shard allocation during restart.
- **Full cluster restart**: Stop all nodes, upgrade, start master-eligible first, then data nodes.
- **Out-of-memory (OOM)**: Occurs when heap is exhausted; kill offending queries, reduce `size`, use `max_result_window` (default 10000).
- **`max_result_window`**: Prevents deep pagination (default 10000); use `search_after` or PIT for deep scrolling.
- **`search_after`**: Efficient deep pagination using a sort key from the last result (no offset).
- **Point-in-time (PIT)**: `POST /index/_pit` — consistent view for subsequent `search_after` searches.
- **`scroll` API**: Old-style deep pagination (deprecated in favor of PIT/search_after); maintain an open context.
- **Thread pools**: `search`, `index`, `write`, `bulk`; watch for `rejected` count (queue saturation → add nodes or tune).
- **Field dropping `_source`**: Disable `_source` to save disk (but you lose original doc retrieval; use `store: true` selectively).
- **`_source`**: Stores the original JSON document; returned by default on search hits.
- **`stored fields` vs `_source`**: `store: true` stores a field separately; `_source` is the whole doc.
- **`_update_by_query` with conflicts**: Use `conflicts=proceed` to skip version conflicts during large updates.
- **`delete_by_query`**: Delete docs matching a query (e.g., data retention); use `conflicts=proceed` for large deletes.
- **Disk-based shard allocation**: ES won't allocate shards to nodes below the `low` watermark (85% disk used by default).
- **Watermarks**: `cluster.routing.allocation.disk.watermark.low` (85%), `high` (90%), `flood_stage` (95% — read-only blocker).
- **Read-only index block**: When `flood_stage` is hit, indices go read-only — free space and explicitly unblock them.
- **Security**: TLS for transport/client, authentication (built-in, LDAP, SAML, OIDC), role-based access control (RBAC).
- **Audit logging**: Enable `xpack.security.audit.enabled` for compliance.

## Common Pitfalls & Troubleshooting
- **`ElasticsearchException: all shards failed`**: Usually a query error, mapping mismatch, or unassigned shard — check `_cat/shards`.
- **Yellow cluster**: Replicas not allocated (missing replica nodes or disk watermark) — data is safe if primaries are okay.
- **Red cluster**: Primary shards unassigned — data at risk; check `_cat/shards` and `cluster.routing.allocation` logs.
- **`circuit_breaking_exception`**: Query tried to use too much memory; reduce `size`, add filters, or use larger nodes.
- **Slow queries**: Use `_search` with `profile: true` to see which query clause is slow; check for `script` and `wildcard`.
- **High JVM heap**: Reduce query size, add replicas (spread load), or scale out data nodes.
- **`too_many_clauses`**: `max_clause_count` (default 1024) exceeded — simplify query or raise limit (with caution).
- **Unassigned shard reasons**: Node left, disk full, allocation decider (`_cat/shards?v&h=index,shard,state,unassigned.reason`).
- **`FORCE_MERGE`**: `POST /index/_forcemerge?max_num_segments=1` to reduce segment count after big deletes (improves search).
- **Segment count**: Too many small segments degrade search; merges happen automatically but can be tuned.
- **`_cluster/reroute?retry_failed=true`**: Retry failed shard allocations after transient issues.
- **`index.mapping.total_fields.limit`**: Default 1000 fields — raise if schema is wide (or rethink mapping).
- **`index.blocks.read_only_allow_delete`**: Set to `false` to recover from flood_stage.
- **`no handler found for uri`**: Wrong endpoint, wrong HTTP method, or wrong index name.
- **`mapper_parsing_exception`**: Field type mismatch — check mapping and document values.
- **`document_missing_exception`**: Update/delete on a nonexistent doc without version — check `_id` and routing.
- **`rejected_execution_exception`**: Thread pool queue full — reduce bulk size, add nodes, or increase queue (temporarily).

## Ecosystem & Integration
- **Kibana**: Visualization, dashboards, Discover, Dev Tools console, and management UI for Elasticsearch.
- **Logstash**: Server-side data processing pipeline (inputs → filters → outputs) for ingestion/transformation.
- **Beats**: Lightweight shippers (Filebeat for logs, Metricbeat for metrics, Heartbeat for uptime, Winlogbeat).
- **Elastic Agent / Fleet**: Modern agent-based data collection with centralized policy management.
- **The ELK/Elastic Stack**: Elasticsearch + Logstash + Kibana (+ Beats) for log analytics and observability.
- **Ingest pipelines**: `_ingest/pipeline` — process documents before indexing (grok, dissect, set, rename, date parsing).
- **Painless script**: Default scripting language for `script` queries, `script_fields`, and ingest processors.
- **Grok**: Pattern-based regex for parsing unstructured logs (e.g., Apache logs, syslog). Use `grok debugger` in Kibana.
- **`_search/template`**: Store reusable search templates with Mustache placeholders.
- **`_msearch`**: Multi-search API — batch multiple searches in one request.
- **`_count`**: Fast count of matching documents (no results returned).
- **`_field_caps`**: Get the types/capabilities of fields across indices (useful for cross-index searches).
- **`_cat` APIs**: Quick human-readable stats (`_cat/indices`, `_cat/shards`, `_cat/nodes`, `_cat/health`).
- **Cross-cluster search (CCS)**: Query across multiple clusters from a single "remote" cluster.
- **Cross-cluster replication (CCR)**: Replicate indices between clusters for DR or geo-distribution.
- **Data streams**: Append-only time-series indices (logs, metrics) with automatic rollover and ILM integration.
- **Index aliases for zero-downtime**: Reindex to a new index, switch alias, delete old — no downtime.
- **Security integration**: TLS everywhere, API keys, RBAC roles per team, field-level security (FLS), document-level security (DLS).
- **Machine Learning**: Built-in anomaly detection (rare/outlier detectors) and data frame analytics.
- **Vector search / kNN**: `knn` search and dense vectors for semantic/recommendation use cases (with `dense_vector` field).
- **Semantic search**: `text_embedding` + `dense_vector` + `knn` for RAG and AI-powered search (ELSER, model deployments).