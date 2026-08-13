# DynamoDB — From Basics to Expert

### connection timeout issues in DynamoDB:
- possible reasons:
  - Network congestion
  - Hardware or software issues
  - Communication problems between devices
- resolution:
  - Update SDK HTTP timeout settings
  - Configure retries with exponential backoff + jitter
  - Connection pooling + warm connections with test/dummy requests

---

## Core Concepts
- **DynamoDB**: AWS's fully managed NoSQL key-value/document database — single-digit millisecond latency at any scale, serverless, highly available across 3 AZs.
- **Table**: A collection of items — unlike SQL, tables have a flexible schema (item-level attributes).
- **Item**: A single record in a table — composed of attributes (JSON-like); up to 400KB per item.
- **Attributes**: Fields of an item — can be of type String, Number, Binary, Boolean, Null, String/Number/Binary Sets, or nested documents (List, Map).
- **Partition key (PK)**: The hash key — determines which partition an item is stored on via hash function.
- **Sort key (SK)**: Optional range key — secondary ordering within a partition; enables range queries.
- **Composite key**: PK + SK together form the primary key — allows flexible item collections (e.g., PK = user_id, SK = entity_type#id).
- **Primary key options**: Single-column PK (hash only — GetItem by exact key) or composite PK+SK (hash + range — query ranges).

## Capacity & Pricing
- **Capacity modes**: On-Demand (pay per request, automatic scaling) vs Provisioned (RCU/WCU units you specify).
- **RCU (Read Capacity Unit)**: 1 RCU = 1 strongly-consistent read/sec up to 4KB, or 2 eventually-consistent reads/sec up to 4KB.
- **WCU (Write Capacity Unit)**: 1 WCU = 1 write/sec up to 1KB.
- **Calculate capacity**: Item size affects RCU/WCU cost — e.g., an 8KB item read = 2 RCU (strong) or 1 RCU (eventual).
- **On-Demand mode**: No capacity planning; pay per request — good for unpredictable/spiky traffic, but costs more per request than provisioned.
- **Provisioned mode + Auto Scaling**: Set base capacity with target utilization — Auto Scaling adjusts for the lowest cost at steady load.
- **Burst capacity**: DynamoDB retains spare capacity for short bursts above provisioned limits — then throttles.
- **Throttling (ProvisionedThroughputExceededException)**: Exceeding capacity → requests throttled; retry with exponential backoff or increase capacity.
- **Adaptive capacity**: DynamoDB automatically redistributes (hot partitions) capacity to skewed partitions — improves on hot keys.

## Data Access (CRUD)
- **GetItem**: Fetch one item by primary key — fast, point lookup; specify `ConsistentRead: true` for strong consistency.
- **PutItem**: Insert or fully replace an item by key (upsert) — atomic.
- **UpdateItem**: Modify specific attributes atomically — supports `SET`, `ADD`, `REMOVE`, `DELETE` and conditional updates.
- **DeleteItem**: Delete an item by key — optionally conditional.
- **BatchGetItem**: Fetch up to 100 items in a single request (across tables) — reduces round-trips.
- **BatchWriteItem**: Up to 25 put/delete (up to 16MB) in one request — cannot update (must Get+Update).
- **Query**: Retrieve all items with a given partition key — filter/sort by sort key (range, begins_with, BETWEEN, ==).
- **Scan**: Read every item in a table/index — expensive, use sparingly (last resort); always filter in application.
- **Scan vs Query**: Query by PK is efficient; Scan reads everything then filters (O(N)) — avoid scans on large tables in production paths.
- **Pagination**: DynamoDB returns up to 1MB per request — use `ExclusiveStartKey`/`LastEvaluatedKey` (or v3 `startKey`) to page.
- **Conditional writes**: `ConditionExpression` — only perform if condition true (e.g., `attribute_not_exists(id)`, `version = :v`) — atomic optimistic locking.
- **Atomic counters**: `ADD` in UpdateItem for atomic increments without read-modify-write races.
- **ReturnValues**: Return old/new item (`ALL_OLD`, `ALL_NEW`, `UPDATED_OLD`, `UPDATED_NEW`) with update.

## Consistency & Transactions
- **Eventual consistency (default)**: Reads may briefly see stale data (~<1s) — faster and cheaper (½ the RCU).
- **Strongly consistent reads**: Latest committed data guaranteed — set `ConsistentRead: true` (2x RCU cost).
- **When to use strong reads**: When correctness matters immediately post-write (balance checks, auth, order confirmation).
- **Transactions**: `TransactWriteItems` / `TransactGetItems` — ACID across up to 100 items (25 actions for txn writes), tables, or global tables within one region.
- **Transaction semantics**: All-or-nothing — with idempotency: if a txn request is retried with same client token, it won't double-apply.
- **ClientRequestToken**: Prevents duplicate processing of the same transaction — important with retries.
- **Transaction cost**: Costs 2x the standard RCU/WCU — measure before widespread use.
- **Transactional use cases**: Financial transfers, inventory consistency, multi-record updates that must be atomic.
- **Optimistic locking**: Use a `version` attribute + conditional expression (`version = :expected`) — on conflict, re-read and retry.

## Secondary Indexes
- **GSI (Global Secondary Index)**: Alternate partition/sort keys on the whole table — supports any attribute as PK; eventual consistency (newer supports strong via transaction + GSI update).
- **LSI (Local Secondary Index)**: Alternate sort key on the same partition key — always strongly consistent; must be created at table creation (immutable).
- **GSI vs LSI**: GSI = different PK, eventual, create anytime, separate capacity; LSI = same PK diff SK, strong, table-creation-time only.
- **GSI counts toward table limits**: You can have up to 20 GSIs and 20 LSIs (default) per table.
- **GSI capacity**: GSIs can have their own provisioned capacity or share the table's — hot GSI can throttle queries even if table is fine.
- **Denormalization with GSIs**: Model access patterns with dedicated GSIs (e.g., query by email, by status+date) instead of scans.
- **Projection types**: ALL (copy all attrs), KEYS_ONLY, INCLUDE (specific attrs) — choose to control GSI storage cost.
- **Index key considerations**: GSI partition/sort keys should spread data evenly — avoid one "hot" key getting most writes.

## Partitioning & Hot Keys
- **Partition internals**: DynamoDB stores items across partitions (~10GB each) — partition count based on data size and capacity.
- **Hash-based routing**: PK hashed → partition; even key distribution = even partition load.
- **Hot partition**: A single key receiving the majority of reads/writes — causes throttling on that partition despite table headroom.
- **Mitigate hot keys**: Distribute key space (suffix with random/numeric ranges), cache hot data, use adaptive capacity.
- **Design for even distribution**: Avoid monotonically increasing keys as PK alone (e.g., timestamps, auto-increment IDs) — use composite keys with a high-cardinality PK.
- **Time-series design**: Use partition key = high-cardinality dimension (e.g., device_id), sort key = timestamp — natural time-ordering per partition.
- **Single-item scaling**: No single item can exceed 400KB; queries to one partition can't exceed 3000 RCU / 1000 WCU.

## Best Practices for Modeling
- **Single-table design**: Store multiple entity types in one table using composite keys (PK/SK) — reduces cost, enables powerful queries, supports adjacency lists.
- **Single-table example**: PK = `USER#<id>`, SK = the entity type+id (`PROFILE`, `ORDER#<id>`, `ORDER#<id>#ITEM#<id>`) — one table serves many access patterns.
- **Adjacency lists**: Store one-to-many/many-to-many relationships with two items or composite keys pointing both ways.
- **Sparse index pattern**: A GSI on an attribute that only exists on some items — effectively filters queries with a cheap index.
- **Global secondary index on "type"**: `itemType` as GSI PK enables entity-scoped scans by type.
- **Sort key design patterns**: `status#date`, `date` reversed (`2026-08-13T...` desc and ranges), `category#id` for prefix queries.
- **One-to-many**: PK = parent ID, SK = child ID — Query gets all children efficiently.
- **Many-to-many**: Two items per relationship (A→B, B→A) with same composite key trick.
- **Access pattern-first design**: List all queries your app needs, then design keys/GSIs to serve them — never "model entities like SQL".
- **Avoid**: Over-normalization, per-entity tables, by using items as SQL rows will quickly become costly and slow.

## DynamoDB Streams & Triggers
- **Streams**: Ordered, durable change feed of items (insert/update/delete) with before/after images — enables event-driven architecture.
- **Stream records**: 24-hour retention; supports `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, `NEW_AND_OLD_IMAGES`.
- **Trigger Lambda**: Streams → Lambda — process changes in near-real time (denormalize, aggregate, fan-out, audit).
- **Streams ordering**: Records per partition key are ordered; shard-based — Lambda processes up to 10 batches per shard concurrently.
- **Streams vs DynamoDB Kinesis**: Streams are simpler per-table; Kinesis supports cross-table/other sources.
- **Exactly-once-ish with idempotency**: Stream processing is at-least-once — make Lambda idempotent (use item version/event ID).
- **Export to S3**: On-demand/managed streaming export of table data to S3 (Parquet/Json) for analytics — no read capacity consumed.

## Global Tables & Replication
- **Global Tables**: Multi-Region, multi-active replication — data written in any region is replicated to others (eventual consistency).
- **Conflict resolution**: Last-writer-wins (based on item timestamp) between regional versions of an item.
- **Use cases**: Disaster recovery (DR), low-latency reads/writes in multiple geographies, active-active workloads.
- **Replication latency**: Usually <1 second but not hard-guaranteed — design for eventual consistency across regions.
- **Global table capacity**: Writes in one region are replicated with additional WCU cost in other regions.
- **Streams with global tables**: Each region has its own stream — process local changes or fan out.

## Integration & Ecosystem
- **DAX (DynamoDB Accelerator)**: In-memory cache (microsecond reads) — for hot read-heavy workloads; eventual consistency by default.
- **DAX vs ElastiCache**: DAX is purpose-built for DynamoDB API compatibility; ElastiCache is a general cache you manage.
- **DynamoDB with API Gateway + Lambda**: Serverless REST/graphQL backend — Lambda reads/writes DynamoDB directly.
- **Stored as JSON**: Use DocumentClient (v2) / DynamoDBClient (v3) services — marshaling data to/from JSON types.
- **IAM for DynamoDB**: Fine-grained access — conditional IAM policies per table/attribute (attribute-level access control).
- **Envelope encryption**: DynamoDB supports encryption at rest with AWS KMS (SSE), including customer-managed keys.
- **Backups**: On-demand backups and continuous PITR (point-in-time recovery) — restore to any second in last 35 days.
- **S3 export/import**: Export table to S3 (JSON/Parquet, no RCU) and import from S3 to create/append a table.
- **AWS Backup**: Centralized backup policy integration with DynamoDB for retention/compliance.
- **CloudWatch metrics**: `ConsumedReadCapacityUnits`, `ThrottledRequests`, `SystemErrors`, `UserErrors` — monitor throttling.
- **CloudTrail**: Audit API calls (who created/updated/deleted tables).

## Common Pitfalls & Troubleshooting
- **`ProvisionedThroughputExceededException`**: Throttled — implement exponential backoff + jitter, increase capacity, or fix hot keys.
- **Hot partition due to uneven keys**: Redesign partition key for even distribution; add cardinals/counter suffixes; use adaptive capacity aware patterns.
- **Scanning huge tables**: Extremely slow + cost — rethink with a Query or a GSI, or pre-aggregate.
- **Item size > 400KB**: Can't store larger items — split into multiple items/attributes (e.g., blob links to S3).
- **"LastEvaluatedKey" not continuing**: Missed pagination in Scan/Query — always loop with the returned key.
- **Eventually-consistent reads returning stale data**: Accepted trade-off — use `ConsistentRead: true` where needed (2x cost).
- **Transactions throttled even at low table load**: Transactions + retries — increase capacity, use client tokens, minimize txn scope.
- **Cross-region replication delays**: Global Tables are eventually consistent — don't read-your-writes across regions.
- **GSI throttling with table healthy**: GSIs have separate capacity — provision capacity on the GSI too.
- **Indexing everything (over-indexing)**: Each GSI costs storage + capacity — only create indices for real access patterns.
- **A field that must never change used as PK**: Changing a partition key = delete + re-insert (cannot update PK) — design for immutable keys.
- **`ResourceNotFoundException` on restore**: Ensure the table region/name is correct post-restore; update app config to point to restored table.

## Advanced Patterns
- **Time-series with TTL**: Use `TimeToLive` attribute (epoch seconds) — auto-delete old items at no cost (ideal for logs, sessions, metrics).
- **TTL caveats**: Expired items are removed asynchronously (may take up to ~48h for full deletion); TTL deletions aren't charged as WCU.
- **Materialized aggregates**: Store precomputed counters/totals in a separate "aggregate" item, updated in the same transaction as source data.
- **Event-driven fan-out**: Streams + SNS/SQS/Lambda to trigger downstream processes (emails, analytics, search index sync).
- **Item collections with composite keys**: Prefix + shared PK grouping — e.g., query all orders AND their items for a user with one Query.
- **DynamoDB as a queue (approximate)**: Candidate messages with status SK; "claim" via conditional update — hacky; prefer SQS for true queues.
- **Write-heavy ingest**: BatchWrite + on-demand or high provisioned capacity + retries; avoid per-item writes in a loop when possible.
- **`ConditionExpression` on `attribute_exists`/`attribute_not_exists`**: Essential for idempotency and singleton guarantees (e.g., one reservation per seat).
- **`ReturnValuesOnConditionCheckFailure`**: Returns rejected item on conditional failure — avoids a second GetItem.
- **Multi-action workflows**: Combine multiple items in a single `TransactWriteItems` for all-or-nothing domain operations.