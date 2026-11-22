# Distributed Systems — From Basics to Expert

## Core Foundations: Scalability & Resiliency

### Scalability
- **Horizontal Scaling (Scale-Out)**: Adding more commodity nodes/instances to distribute workload across a cluster. Provides near-limitless expansion and high availability.
- **Vertical Scaling (Scale-Up)**: Adding more CPU, RAM, or storage to a single server. Limited by hardware boundaries, cost ceilings, and creates a single point of failure (SPOF).
- **Elasticity**: Dynamically matching resource provisioning with fluctuating real-time load (handling 1 user up to 100M users smoothly during traffic spikes).

### Resiliency & Fault Tolerance
- **Designing for Failure**: Distributed systems span thousands of machines, switches, and disks; failures are inevitable rather than exceptional.
- **Planning Across Layers**:
  - **Infrastructure & Network**: Multi-AZ deployments, redundant network backbones, dynamic failovers.
  - **Data Storage**: Quorum-based writes, geo-replication, snapshot backups.
  - **Application**: Graceful degradation, idempotent retries, timeouts, and fallback mechanisms.
- **Key Resiliency Patterns**:
  - **Automation**: Automated provisioning, rolling health checks, automated canary deployments, and self-healing node replacement.
  - **Loose Coupling**: Event-driven communication (message queues/streams) preventing cascading failures across services.
  - **Data-Driven Observability**: Distributed metrics, APM tracing, and health endpoints driving autoscaling and traffic shedding decisions.

## Fundamental Theorems & Tradeoffs

### The CAP Theorem (Brewer's Theorem)
In an asynchronous network subject to partitions, a distributed system can guarantee at most **two out of three** properties:
- **Consistency ($C$)**: Every read receives the most recent write or an error (linearizability).
- **Availability ($A$)**: Every non-failing node returns a non-error response for every request (without guarantee it contains the latest write).
- **Partition Tolerance ($P$)**: The system continues to operate despite arbitrary message loss or network partitions.
- *Reality*: Network partitions are physical realities of networks; thus, you must choose between **CP** (e.g., ZooKeeper, Google Spanner, HBase) or **AP** (e.g., Cassandra, DynamoDB, CouchDB) during a network split.

### The PACELC Theorem
Extends CAP by evaluating tradeoffs when the network is running normally:
- If there is a **Partition ($P$)**, how does the system trade off **Availability ($A$)** and **Consistency ($C$)**?
- **Else ($E$)**, how does the system trade off **Latency ($L$)** and **Consistency ($C$)**?
- *Examples*:
  - **PC/EC** (e.g., BigTable, Spanner): Chooses consistency both during partitions and normal operations (higher latency).
  - **PA/EL** (e.g., Dynamo, Cassandra): Chooses availability during partitions and low latency during normal operations (eventual consistency).

## Consensus Protocols
- **The Consensus Problem**: Getting a cluster of independent distributed nodes to agree on a single value or state machine sequence, even when some nodes fail or experience network delays.
- **Raft Consensus Protocol**:
  - Designed for understandability and decomposed into distinct subproblems:
  - **Leader Election**: Nodes are in one of three states (`Follower`, `Candidate`, `Leader`). Randomized election timeouts prevent split-vote deadlocks.
  - **Log Replication**: The Leader accepts commands from clients, appends them to its log, and sends `AppendEntries` RPCs to followers. A log entry is committed once replicated across a majority of nodes ($N/2 + 1$).
  - **Safety Invariant**: If a leader commits an entry, that entry will be present in the logs of all future leaders (guaranteed by requiring candidates to have up-to-date logs to win elections).
- **Paxos Protocol**: Classic consensus protocol. Uses two phases: Phase 1 (Prepare / Promise) and Phase 2 (Accept / Accepted). High theoretical rigor, but notoriously complex to implement.
- **Byzantine Fault Tolerance (BFT)**: Consensus in adversarial networks where nodes can not only fail, but intentionally lie or act maliciously (used in blockchain protocols like PBFT, Tendermint, PoW/PoS).

## Replication & Consistency Models
- **Replication Topologies**:
  - **Single-Leader (Primary-Replica)**: All writes go to the primary leader; reads can be served by replicas. Simple, but write scalability is bounded by the leader node.
  - **Multi-Leader**: Writes processed at multiple data centers/nodes. Requires conflict resolution strategies (Last-Write-Wins, CRDTs, Operational Transformation).
  - **Leaderless (Dynamo-style)**: Clients write directly to multiple replicas using quorum parameters:
    - $N$ = Replication factor, $W$ = Write quorum, $R$ = Read quorum.
    - If $W + R > N$, a read quorum overlaps with a write quorum, guaranteeing at least one node returns the latest value.
- **Consistency Spectrum**:
  - **Strict / Linearizable Consistency**: All operations appear to take effect atomically at a single instant in global real time.
  - **Sequential Consistency**: Operations take effect in some sequential order consistent with each individual node's program order.
  - **Causal Consistency**: Causally related operations are seen by every node in the same order; concurrent operations may be seen in different orders.
  - **Eventual Consistency**: Given no new updates, all replicas eventually converge to the identical value (weakest guarantee).
  - **Monotonic Reads & Read-Your-Writes**: Client-centric consistency preventing users from seeing time move backwards.

## Distributed Transactions & Data Integrity
- **Two-Phase Commit (2PC)**:
  - **Phase 1 (Prepare)**: Coordinator asks all participants if they can commit. Participants acquire locks and vote `YES` or `NO`.
  - **Phase 2 (Commit/Abort)**: If all vote `YES`, coordinator broadcasts `COMMIT`; otherwise broadcasts `ABORT`.
  - *Pitfall*: Blocking protocol. If the coordinator crashes after Phase 1, participants remain locked indefinitely.
- **Three-Phase Commit (3PC)**: Adds a non-blocking `PreCommit` phase with timeouts, but remains vulnerable to network partitions.
- **The Saga Pattern**:
  - Breaks a distributed transaction into a sequence of local transactions across microservices.
  - Each step updates local storage and publishes an event/message triggering the next step.
  - **Compensating Transactions**: If a intermediate step fails, explicit undo actions are executed in reverse order.
  - **Coordination**:
    - **Choreography**: Services listen to domain events and decide when to act (decentralized, good for simple flows).
    - **Orchestration**: A dedicated orchestrator service manages the transaction state machine and directs participants (centralized, easier to trace).
- **Transactional Outbox Pattern**:
  - Solves dual-write problems (saving to database and publishing to message queue atomically).
  - Write business data and an outgoing event message to an `OUTBOX` table in the *same local database transaction*.
  - A separate CDC (Change Data Capture like Debezium) process reads the outbox table and reliably publishes messages to Kafka.

## Time, Ordering & Distributed Clocks
- **Physical Clocks & Clock Drift**:
  - Quartz crystals in servers drift based on temperature. NTP (Network Time Protocol) synchronizes time over networks but introduces non-deterministic jitter ($\pm 10$ to $100$ ms). Never rely on physical wall-clock timestamps for strict ordering.
- **Logical Clocks**:
  - **Lamport Timestamps**: Simple scalar integer incremented on local events and sent with messages. Guarantees partial ordering: if $A \to B$, then $L(A) < L(B)$. Cannot detect concurrency ($L(A) < L(B)$ does not imply $A \to B$).
  - **Vector Clocks**: Vector of logical counters (one per node). Enables detecting causal relationships vs concurrent conflicting updates.
- **TrueTime (Google Spanner)**:
  - Uses synchronized atomic clocks and GPS receivers across data centers to bound clock uncertainty ($\epsilon \approx 1-7$ ms).
  - Wait-out-the-uncertainty guarantees external consistency (linearizability) globally.

## Fault Isolation & Stability Patterns
- **Circuit Breaker Pattern**: Wraps external calls. Transitions through `CLOSED` (normal), `OPEN` (fail-fast without calling failing dependency), and `HALF-OPEN` (probe trial requests).
- **Bulkheads**: Isolates resources (thread pools, memory, connections) into distinct pools so a failure in one tenant or dependency does not exhaust resources for the rest of the application.
- **Rate Limiting & Shedding**: Protects backend services from traffic surges using Token Bucket, Leaky Bucket, or Sliding Window algorithms.
- **Retry with Exponential Backoff & Full Jitter**:
  $$\text{Sleep} = \text{random}(0, \, \min(M, \, B \times 2^{\text{attempt}}))$$
  Prevents the **Thundering Herd** problem where synchronized retries overwhelm recovering backends.
