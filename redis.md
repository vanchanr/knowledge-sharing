# Redis — From Basics to Expert

## Core Concepts
- **Redis**: In-memory data structure store — used as cache, message broker, database, and for real-time data — single-threaded event loop, sub-millisecond latency.
- **Keys**: Binary-safe strings (up to 512MB) — name them with conventions like `user:123:profile`, `session:abc123` for organization.
- **Key expiration**: `EXPIRE`/`SETEX`/`TTL` — auto-delete after TTL; essential for caching and session data.
- **Data structures**: Strings, Lists, Sets, Sorted Sets, Hashes, Bitmaps, HyperLogLog, Geospatial, Streams.
- **Single-threaded model**: All commands execute serially on one thread — atomic per command, no context switching, but never run blocking operations (KEYS, huge SCAN).
- **Why so fast**: In-memory data + event loop (epoll) + simple data structures + optimized C code — vs disk-based DBs.
- **Persistence**: Two options — RDB snapshots and AOF (Append-Only File); understand the durability trade-offs.
- **Replication**: Master → replica async replication for read scaling and HA (replicas can be promoted).
- **Clustering**: Redis Cluster — data sharded across nodes (16384 hash slots) with automatic failover.
- **Redis vs Memcached**: Redis = rich data structures, persistence, replication, Lua scripts; Memcached = simpler, multithreaded, pure cache (eviction only).
- **Redis vs traditional cache**: Distributed cache shared across app instances; not a primary DB (except RedisJSON/RedisGears use cases).

## Data Structures
- **Strings**: Simple key-value — use for counters (`INCR`), cached values, session tokens, binary-safe.
- **`INCR`/`DECR`**: Atomic counters — perfect for rate limiting, stock counts, visit counts (no race conditions).
- **`SET NX EX`**: Set if not exists + expiry — the basis of distributed locks and deduplication.
- **`GETSET`**: Atomically set a new value and return the old — useful for resetting counters (e.g., rate limits per window).
- **`MGET`/`MSET`**: Batch get/set — reduces round-trips; use pipelines for many keys.
- **Lists**: Linked list of strings — `LPUSH`/`RPUSH`, `LPOP`/`RPOP`, `LRANGE` — perfect for queues, recent items, timelines.
- **List as queue**: `LPUSH` + `BRPOP` (blocking) — a simple reliable work queue (with `BRPOPLPUSH` for safe processing).
- **Sets**: Unordered unique strings — `SADD`, `SINTER`, `SUNION`, `SDIFF` — for tags, follows, deduplication, membership.
- **Set operations**: `SISMEMBER` (fast membership test), `SCARD` (size), `SRANDMEMBER` (random sampling).
- **Sorted Sets (ZSETs)**: Unique members with a score — `ZADD`, `ZRANGE`, `ZRANGEBYSCORE` — the most powerful structure: leaderboards, rankings, rate limiting.
- **ZSET use cases**: Leaderboards, top-N queries, scheduled jobs (score = timestamp), sliding window rate limiting.
- **`ZINCRBY`**: Atomic increment/decrement of a member's score — live-updating leaderboards.
- **Hashes**: Maps of field-value pairs — `HSET`, `HGETALL`, `HINCRBY` — ideal for objects (users, products, session data).
- **Hash vs string for objects**: Hashes reduce memory and allow partial updates (better than serializing whole objects to strings).
- **Bitmaps**: String bits as flags — `SETBIT`, `GETBIT`, `BITCOUNT` — for tracking user actions (e.g., daily active users) with tiny memory.
- **HyperLogLog**: Probabilistic unique counter — `PFADD`, `PFCOUNT` — ~0.81% error, ~12KB constant memory for billions of unique items.
- **Geospatial**: `GEOADD`, `GEOSEARCH` — store coordinates, find points within radius (location-based features).
- **Streams**: Append-only log data structure — `XADD`, `XREAD`, `XREADGROUP`, consumer groups — for event streaming, processing, fan-out.
- **Streams vs Pub/Sub**: Streams persist messages and support consumer groups/replay; Pub/Sub is fire-and-forget (no persistence, no replay).
- **`TYPE` command**: Check the data structure type of a key — right tool for the job.

## Caching
- **Cache-aside (lazy loading)**: Check Redis → miss → load from DB → write back to Redis with TTL — the most common pattern.
- **Write-through**: Write to Redis and DB simultaneously — cache always current; extra write latency.
- **Write-behind**: Write to Redis, async flush to DB — high throughput, eventual consistency, risk of data loss.
- **TTL strategy**: Set sensible TTLs (seconds–hours); add jitter (± 10%) to prevent mass expiry stampedes.
- **Cache stampede (thundering herd)**: Many concurrent misses on expiry overload the DB — use `SETNX` single-flight lock or read-through with lock.
- **Eviction policies (`maxmemory-policy`)**: `noeviction`, `allkeys-lru`, `allkeys-lfu`, `volatile-lru`, `volatile-ttl`, `volatile-random`, `allkeys-random`.
- **LRU vs LFU**: LRU (recently used) vs LFU (frequency-based) — LFU better for skewed access patterns.
- **Eviction policy trade-offs**: `volatile-*` only evicts keys with TTL (keep cached data, drop session-free keys); `allkeys-*` can evict anything.
- **Hot key problem**: A single key getting huge traffic — mitigate with sharding (key suffix), replication, or local caches.
- **Cache consistency**: Invalidate on writes (delete vs update); accept small inconsistency windows — TTL is the safety net.

## Pub/Sub & Messaging
- **Pub/Sub**: Publisher sends messages to channels; subscribers receive — fire-and-forget, no persistence.
- **Channels**: `SUBSCRIBE channel`, `PUBLISH channel message` — any number of subscribers receive; patterns via `PSUBSCRIBE`.
- **Pub/Sub use cases**: Real-time notifications, chat, live updates, system alerts, websocket fan-out.
- **Pub/Sub limitations**: No persistence, no replay, no acknowledgment, no consumer groups — messages are lost if no subscriber.
- **Streams (with consumer groups)**: Durable messaging with acks (`XACK`), pending entries (`XPENDING`), and replay — for reliable processing.
- **Consumer groups**: Distribute stream entries among consumers; track delivery status for at-least-once processing.
- **`XREADGROUP`**: Consumer reads from group; messages go to the group's pending list until acknowledged.
- **Dead-letter handling**: Reclaim stuck messages with `XAUTOCLAIM` after `XCLAIM` timeout — expire retries after N attempts.
- **Streams vs Kafka**: Kafka = distributed multi-consumer partitions, long retention; Redis Streams = in-memory/disk single-node (unless cluster), simpler for many cases.

## Persistence & Durability
- **RDB snapshots**: Point-in-time binary dump — small, fast load; loses data since last save (default 60s/10000 writes).
- **AOF (Append-Only File)**: Logs every write command — fsync policies: `always` (fsync every write, slow), `everysec` (default), `no` (OS flush).
- **AOF rewrite**: `BGREWRITEAOF` compacts the log (same logical state, smaller file) — triggered automatically by config.
- **Durability comparison**: RDB = fast, coarse granularity; AOF = finer granularity, slower; combine both for production (AOF primary, RDB for load).
- **`SAVE` vs `BGSAVE`**: Blocking save (rarely use) vs fork+save in background — never block the event loop.
- **Forks**: `BGSAVE`/`BGREWRITEAOF` fork the process — copy-on-write memory, so plan memory headroom (avoid swapping).
- **Persistence trade-off**: Enable persistence for critical data; disabled (`save ""` + `appendonly no`) for pure-cache-only instances.

## High Availability
- **Replication**: Master-replica — `replicaof <ip> <port>`; async replication; replicas serve reads (`READONLY`).
- **Promotion/failover**: Replica promoted to master on failure — automatic via Sentinel or Cluster.
- **Replication lag**: Replicas lag behind master (async) — reads from replicas can be stale; watch `master_repl_offset`.
- **Sentinel**: Redis Sentinel monitors masters/replicas — automatic failover, service discovery for clients.
- **Sentinel quorum**: `sentinel monitor mymaster 127.0.0.1 6379 2` — needs quorum of sentinels to trigger failover (avoid split-brain).
- **Redis Cluster**: Sharded setup with 16384 hash slots across master nodes; each master has replicas.
- **Cluster hash slots**: Key → CRC16(key) % 16384 → node; clients redirect with `MOVED`/`ASK` errors.
- **Cluster guarantees**: Failover automatic, but during failover window (up to ~5s) commands may fail (not split-brain safe).
- **Cluster limitations**: Multi-key operations only if keys share a hash slot (`{user:123}` hash tags); no multi-slot transactions.
- **Hash tags**: `user:{123}:orders` — force keys into the same slot for atomic multi-key ops.

## Performance & Operations
- **Pipelines**: Batch multiple commands in one round-trip (`redis-cli --pipe`, client-multi pipelines) — massive throughput gains.
- **Transactions (MULTI/EXEC)**: Queue commands atomically — all or nothing, but no rollback on runtime errors; `WATCH` for optimistic CAS.
- **`WATCH`**: Conditional execution — watch key(s), run checks, `EXEC` fails if watched keys changed (optimistic locking).
- **Lua scripting (`EVAL`)**: Atomic server-side scripts — combine read/check/write in one atomic step (beat MULTI for conditional logic).
- **Lua best practices**: Keep scripts short, avoid `KEYS` (use `ARGV`), idempotent if possible (restart risk).
- **`KEYS` vs `SCAN`**: `KEYS pattern` blocks the server (never in prod); `SCAN` is cursor-based and non-blocking.
- **`SCAN` guarantees**: Returns all elements eventually (can duplicate); use `MATCH` pattern and `COUNT` hint.
- **Big keys**: Keys > 10MB (or huge lists/sets) — cause memory spikes, slow commands, cluster imbalance; use `redis-cli --bigkeys`.
- **Hot keys**: Keys accessed disproportionately — detect with `redis-cli --hotkeys` (LFU) or MONITOR sampling.
- **`DEBUG`/`MONITOR`**: `MONITOR` streams all commands (high overhead — use sparingly for debugging).
- **Memory**: `INFO memory`, `MEMORY USAGE key`, `MEMORY STATS` — watch `used_memory` vs `maxmemory`, fragmentation (`mem_fragmentation_ratio`).
- **`maxmemory`**: Set a cap; choose eviction policy (see above) or Redis goes OOM/swap.
- **Swap is death**: If Redis swaps to disk, latency tanks — monitor `vm.swappiness` (set to 0/1) and `used_memory` vs RAM.
- **`CONFIG GET/SET`**: Runtime config (`CONFIG SET maxmemory 2gb`) — note which settings require restart (e.g., maxmemory-policy is dynamic, aof is not all).
- **`lastsave` & persistence health**: Check `INFO persistence` for last RDB/AOF write success/failure.
- **`INFO replication`**: Master/replica offsets, link status — watch for `master_link_down_since_seconds` (replication broken).
- **`CLIENT LIST`/`CLIENT KILL`**: Manage client connections; watch for too many connections (leaks) or blocking clients.
- **`REDIS_MAXMEMORY`/`ulimit`**: Raise file descriptor limits for many connections to Redis.

## Data Structures / Memory Optimization
- **Intset / ziplist (listpack)**: Small collections are stored in compact encodings — memory efficient; `object encoding key` to inspect.
- **`OBJECT ENCODING`**: Check encoding (int, embstr, raw, hashtable, listpack) — small ints/strings are memory optimized.
- **Memory efficiency tips**: Use Hashes for small objects, shorten keys, avoid big strings, use integers when possible, set `maxmemory-policy`.
- **`debug object`**: No, use `MEMORY USAGE <key>` to estimate memory for a specific key.
- **`redis-cli --stat`**: Real-time server stats — quick health check.
- **`redis-benchmark`**: Load/stress testing tool — measure ops/sec, latency percentiles.

## Use Cases & Patterns
- **Session storage**: Store user sessions as hashes/strings with TTL — distributed apps share sessions without sticky sessions.
- **Rate limiting**: `INCR` + `EXPIRE` (fixed window), `ZADD`/`ZCOUNT` (sliding window), token bucket via Lua.
- **Leaderboards**: ZSETs — `ZADD` scores, `ZREVRANGE` top-N, `ZINCRBY` live updates.
- **Distributed locks**: `SET key uuid NX PX 30000` + Lua for release (compare value then DEL) — not a full Redlock, but often sufficient.
- **Redlock**: Distributed lock across 5+ independent masters — controversial (use with care, or use ZooKeeper/etcd).
- **Caching layer in front of DB**: Read-heavy workloads — cache hot queries/objects to offload DB.
- **Message queue**: Lists (`LPUSH`/`BRPOP`) or Streams for reliable async processing.
- **Real-time analytics**: `INCR` counters, HyperLogLog uniques, Streams ingest, sorted sets for time buckets.
- **Job scheduler / delayed queue**: ZSET with score = timestamp; worker does `ZRANGEBYSCORE ... 0 now` then processes.
- **Feature flags**: Strings with TTL or simple keys — instant toggles at runtime.
- **Distributed rate limiter**: Sliding window per user/IP via ZSET or Lua — enforce API quotas.
- **Global ID generation**: `INCR` for sequential IDs (not scalable across cluster, but fine for single-instance/MLU).

## Security & Best Practices
- **No default configuration**: Set a strong password (`requirepass`) or use ACLs; never expose on public internet without auth.
- **ACLs (Access Control Lists)**: Per-user permissions — `ACL SETUSER app on >password ~cache:* +get +set +expire`.
- **ACL categories**: `+@read`, `+@write`, `+@admin`, `+@all` — restrict commands per app/service.
- **`RENAME` dangerous commands**: Disable/rename `FLUSHALL`, `FLUSHDB`, `KEYS`, `CONFIG`, `DEBUG`, `SHUTDOWN` (via `rename-command`).
- **TLS**: Enable `tls-port` and `tls-cert-file` — encrypt traffic between apps and Redis (no plaintext passwords).
- **Network isolation**: Put Redis in private network/VPC segment; use security groups/firewalls (SG allow only app hosts).
- **Never run as root**: Run redis as a dedicated user; set `dir` permissions to the data directory only.
- **Protected mode**: `protected-mode yes` — only localhost connections allowed unless a password is set (safe default).
- **Disable dangerous commands**: `enable-protected-configs`, or rename commands in redis.conf for production.
- **Sentinel/Cluster passwords**: Configure `sentinel auth-pass` and cluster `requirepass` consistently.
- **Avoid storing sensitive plaintext**: Redis is not encrypted at rest (unless DEK with encryption layer) — don't put secrets/PII in Redis without additional encryption.
- **Backup plan**: Periodic `BGSAVE`/`AOF` archive to S3/object storage; restore-test regularly (persistence + snapshot lifecycle).

## Common Pitfalls & Troubleshooting
- **`OOM command not allowed when used memory > 'maxmemory'`**: Redis hit maxmemory + noeviction — increase memory, change eviction policy, or free keys.
- **`READONLY You can't write against a read only replica`**: Writing to a replica — connect to master (or promote).
- **`MOVED`/`ASK` (cluster)**: Client library must follow redirects — use a cluster-aware client (redis-py-cluster, Lettuce).
- **`ERR no such key`**: Obvious but common — with `MGET`/`HGETALL`, check the key naming scheme.
- **`BUSYKEY`/`WRONGTYPE`**: Wrong data structure used on a key — `TYPE` key to inspect, fix app logic.
- **`MISCONF Redis is configured to save RDB snapshots, but it's currently unable to persist on disk`**: Disk full/permission — fix disk or set `save ""` for cache-only.
- **Latency spikes**: Watch for swapping, fork during BGSAVE, `KEYS` commands, big keys, and network saturation.
- **`Redis is running in protected mode`**: Can't connect externally without password — set `requirepass` or bind correctly.
- **Aborted connections / connection resets**: Check `tcp-keepalive`, `timeout` config, ulimit/`maxclients`.
- **`WRONGPASS invalid username-password pair`**: Wrong auth/ACL credentials — debug with `AUTH` tests (careful in logs).
- **`Redis Cluster requires a config file`**: Cluster nodes need proper `cluster-enabled yes` + config file.
- **`Can't handle RDB format version`**: Old/new version mismatch — verify Redis versions are compatible (or migrate RDB).
- **`Redis 7 vs 6 changes`**: ACL is default (default user `default`), `listpack` replaces ziplist, `XAUTOCLAIM`, `function` (Lua library) vs `EVAL`.
- **`DEBUG SLEEP`/`DEBUG` commands**: Never run in prod — blocks the event loop.
- **`MASTERDOWN Link with MASTER is down and replica-serve-stale-data is set to 'no'`**: Replica is not serving stale reads during failover — config choice.

## Redis Distributed & Ecosystem
- **Redis Cluster**: 16384 slots, `CLUSTER SLOTS`, add nodes (`CLUSTER MEET`), reshard (`redis-cli --cluster reshard`).
- **Cluster failover**: `CLUSTER FAILOVER` — manual graceful promotion of a replica (for maintenances).
- **Redis Sentinel vs Cluster**: Sentinel = HA for single-master setups; Cluster = sharding + HA for large-scale.
- **Redis on Kubernetes**: Operator pattern (Spotahome, kube-redis) for provisioning/config/failover automation.
- **Cache frameworks**: Spring Cache (Redis), Django Redis cache, sidekiq/Resque (background jobs on Redis).
- **Redis client libraries**: jedis/lettuce (Java), redis-py (Python), node-redis/ioredis (Node), go-redis (Go).
- **Redis Modules**: RediSearch (full-text), RedisJSON (JSON), RedisTimeSeries (time series), RedisBloom (probabilistic).
- **RediSearch**: Secondary index with full-text queries on Redis — can be a lightweight Elasticsearch alternative.
- **RedisJSON**: Native JSON type with `JSON.GET`, `JSON.SET`, path queries — avoids serialization overhead.
- **Redis Functions**: Server-side scripting library (Lua) managed via `FUNCTION LOAD` — more structured than EVAL scripts.
- **Observability**: `INFO`, `LATENCY` (Redis latency doctor), `SLOWLOG` (slow commands), RedisInsight (GUI).
- **`SLOWLOG GET`**: Shows slow commands (default > 10ms) — identify `KEYS`, big `LRANGE`, expensive scripts.
- **`LATENCY DOCTOR`**: Self-diagnostic latency report — check for Redis/Linux kernel latencies.