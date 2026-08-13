# Storage — From Basics to Expert

## Core Concepts
- **Object storage**
- **File storage**
- **Block storage**

---

## Storage Fundamentals
- **Storage hierarchy**: Registers → Cache (L1/L2/L3) → RAM → SSD → HDD → Tape — each level trades speed, cost, and capacity.
- **Latency vs throughput**: Latency = time to first byte (ms); throughput = data per second (MB/s) — different workloads need different optimizations.
- **Durability**: Resistance to data loss (RAID, replication, erasure coding) — measured in nines (S3 = 11 nines).
- **Availability**: Uptime of data access (SLA) — e.g., 99.99% = ~52 min downtime/year.
- **Data lifecycle**: Hot (frequent access) → Warm (infrequent) → Cold (archive) → Deleted — governed by policies.
- **RPO (Recovery Point Objective)**: Maximum acceptable data loss (how far back you can restore).
- **RTO (Recovery Time Objective)**: Maximum acceptable downtime to restore service after failure.

## Block Storage
- **Block storage**: Raw storage divided into fixed-size blocks, addressed by block number — attached to a single server (EBS, SAN, local disks).
- **Block devices**: Presented to the OS as a disk (e.g., `/dev/sda`) — the OS/file system manages the blocks.
- **Use cases**: OS disks, databases, VMs, anything needing low-latency random I/O and a file system.
- **Low latency & low overhead**: Direct block access, no API layer — best for random read/write workloads (DBs, transactional systems).
- **No shared access**: A block volume is typically attached to one server at a time (except cluster-aware file systems).
- **RAID levels**: RAID 0 (striping, performance), RAID 1 (mirroring, redundancy), RAID 5 (distributed parity), RAID 10 (stripe+mirror).
- **RAID vs replication**: RAID protects against disk failure on one host; replication/erasure coding protects across hosts.

## File Storage
- **File storage**: A hierarchical file system with directories/files — presented as a share mounted on clients (NFS, SMB, EFS).
- **Use cases**: Shared drives, user home dirs, media/content, CI artifacts, legacy apps needing a filesystem path.
- **Protocols**: NFS (Linux/Unix), SMB/CIFS (Windows), POSIX file semantics (open/read/write/close).
- **File lock & semantics**: Multiple clients read/write the same file — distributed locking and cache coherence are hard.
- **Network file systems**: NFS on NAS devices; EFS (AWS), Azure Files, Cloud Filestore (GCP).
- **Performance**: File systems have higher overhead than raw block — directory traversal, metadata operations.
- **When to choose**: When apps expect a mountable filesystem path, or multiple servers need shared mutable files.

## Object Storage
- **Object storage**: Stores data as objects (data + metadata + unique ID) in a flat namespace (buckets/keys) — accessed via HTTP APIs (S3, GCS, Swift).
- **Use cases**: Static assets, backups, media/archives, data lakes, big data analytics, user uploads — the backbone of cloud storage.
- **Key features**: Unlimited scalability, high durability (replication/erasure coding), REST API access, metadata & tags.
- **Consistency**: Strong read-after-write consistency (S3 since 2020); designed for WORM (write once, read many) — not for updating parts of files.
- **Not a file system**: No POSIX semantics (no append, no in-place update) — but S3-compatible foundations and FUSE drivers exist (s3fs).
- **Storage classes / tiers**: Hot, infrequent, archive (Glacier/Deep Archive) — cost tiers based on access frequency/retrieval time.
- **Versioning**: Keep multiple versions of objects — protection against accidental deletes/overwrites.
- **Encryption**: Server-side (SSE keys) managed object encryption; client-side encryption for extra control.
- **Lifecycle policies**: Automatically transition objects between tiers and expire/delete them after set durations.

## Databases & Storage Engines
- **Storage engine**: How a DB physically stores rows/pages on disk (InnoDB, MyRocks, WiredTiger, PostgreSQL heap).
- **Row vs columnar storage**: Row-oriented = OLTP (fast point lookups); columnar = OLAP (fast aggregates/compression).
- **LSM-tree**: Log-structured merge — append-only writes + in-memory memtable + sorted SSTable compaction (used by Cassandra, RocksDB, HBase).
- **B-tree vs LSM**: B-tree = in-place (better reads, worse writes); LSM = append-only (better writes, compaction cost, worse reads).
- **WAL (Write-Ahead Log)**: Every mutation is appended to a log first — guarantees durability and enables crash recovery.
- **Buffer pool / page cache**: In-memory cache of DB pages — hit ratio is a key performance metric.
- **Compression**: Columnar & dictionary compression (Parquet, ZSTD) reduce storage and I/O for analytics.

## Distributed Storage
- **Replication**: Multiple copies of data across nodes/regions — for durability, availability, and read scaling.
- **Erasure coding**: Split data into fragments with parity (e.g., 6+3) — better space efficiency than full replication (S3, Ceph).
- **Sharding**: Horizontally partition data across nodes by key/range/hash — scale write capacity, adds complexity.
- **Consensus (Raft/Paxos)**: Nodes agree on state — used for metadata, leader election, and replicated logs.
- **Split-brain**: Two nodes accept writes independently → divergence — prevented by quorum and fencing.
- **CAP theorem**: In a partition, choose consistency or availability — storage systems are designed CP or AP.
- **Structured vs unstructured**: Unstructured = blobs/objects (S3); structured = rows (SQL) — different consistency and access models.
- **Metadata services**: Where "which object is on which node" is tracked (HDFS NameNode, S3 metadata) — a common single point of concern.
- **Locality of reference**: Keep related data near each other (same node/region) to reduce network I/O.

## Cloud Storage Services
- **AWS S3**: Object storage — 11 nines durability, classes, versioning, lifecycle, presigned URLs, static hosting, Transfer Acceleration.
- **EBS (AWS)**: Block storage for EC2 — gp3 (general), io2 (provisioned IOPS), snapshots, cross-region copy.
- **EFS (AWS)**: Managed NFS file storage — shared across EC2/AZs, elastic capacity.
- **Google GCS**: Object storage with classes (Standard, Nearline, Coldline, Archive), object lifecycle, optional strong consistency.
- **Azure Blob**: Object storage — hot/cool/archive tiers; Azure Files = managed SMB file shares.
- **CDN + origin storage**: CloudFront/S3, Cloudflare R2 — global edge caching reduces latency & origin load.

## Storage Performance & Reliability
- **I/O patterns**: Random vs sequential, read vs write heavy, small vs large blocks — choose storage accordingly.
- **Measuring performance**: IOPS (operations/sec), throughput (MB/s), latency (ms) — the three key metrics.
- **SSD vs HDD**: SSD = low latency, high IOPS, costlier; HDD = cheap capacity, good sequential throughput, higher latency.
- **NVMe vs SATA/SAS**: NVMe = PCIe bus, much lower latency & higher parallelism — standard for modern SSDs.
- **Caching**: Hot data in fast tiers (RAM/SSD) ahead of slow storage (L1/L2 cache, page cache, cache-aside).
- **Write-ahead & fsync**: fsync flushes to durable storage — frequent fsync = durable but slow (DB trade-off with `synchronous_commit`).
- **Dedup & compression**: File/system-level dedup (ZFS) and compression (LZ4, ZSTD, gzip) reduce storage footprint.
- **Backup vs replication**: Backups = point-in-time copies for restore; replication = live copies for HA — both needed.
- **Backup types**: Full, incremental (changes since last), differential (changes since last full), and continuous (WAL/log).
- **Consistency of backups**: Snapshot consistency (crash-consistent vs app-consistent) — coordinate app + storage snapshots (e.g., DB + EBS).
- **Test restores**: Regularly verify backups actually restore (RTO measured) — untested backups are worthless.
- **Monitoring**: Disk space, IOPS, latency, throughput, error rates, and capacity trends — alert on thresholds.

## Capacity Planning & Optimization
- **Understand growth**: Track data growth rate to forecast storage needs — plan for 60-70% utilization.
- **Retention policies**: Define how long data is kept (compliance + cost) — automate deletion/archival.
- **Tier data intentionally**: Move cold data to cheaper tiers — but account for retrieval latency and costs.
- **Monitor cost**: Storage classes, retrieval fees, cross-region replication, egress — all factor into total cost.
- **Right-size and right-type**: Choose the correct storage type for each workload (block for DB, object for blobs, file for shares).

## Common Pitfalls & Mistakes
- **Using object storage like a file system**: Attempting in-place updates/appends on S3 — object storage is immutable (re-upload on change).
- **Ignoring durability of single node**: A single disk/instance is one failure away from data loss — always replicate/backup.
- **No versioning on object storage**: Accidental overwrite/deletion is permanent without versioning (S3).
- **Backups on the same system as data**: A single host/cloud region failure takes both — replicate backups off-site/off-region.
- **Measuring only capacity**: A disk at 10% capacity can still hit IOPS/latency limits — monitor performance too.
- **Not planning for RPO/RTO**: Requirement ambiguity → restore failures and long downtime when incidents occur.
- **Hot data on cold tier**: Retrieval latency/costs explode — ensure frequently-accessed data is on hot tiers.
- **Single point of failure in metadata**: Distributed storage systems often have a metadata cache/leader — design/patch carefully (e.g., HDFS NameNode).