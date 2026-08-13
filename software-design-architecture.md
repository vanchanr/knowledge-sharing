# Software Design & Architecture — From Basics to Expert

## Architecture Fundamentals
- **Software architecture**: The high-level structure of a system — the significant design decisions, components, their relationships, and the principles guiding evolution.
- **Architecture vs Design**: Architecture is the macro (system structure, components, tech choices, non-functional requirements); design is the micro (class-level, algorithm, pattern detail within components).
- **Non-functional requirements (NFRs)**: Scalability, availability, reliability, maintainability, performance, security, cost — often matter more than features for architecture success.
- **Quality attributes**: The measurable properties (latency, throughput, fault tolerance, modifiability, testability) that architecture must satisfy.
- **The 4+1 View Model**: Logical (class diagrams), Process (concurrency), Development (module organization), Physical (deployment), + Scenarios (use cases).
- **C4 Model**: Context → Containers → Components → Code — 4 levels of zoom for visualizing software architecture.
- **Monolithic architecture**: Single deployable unit — simple to start, but becomes hard to scale/maintain as the team/codebase grows.
- **Microservices architecture**: Many small, independently deployable services, each owning a business capability, communicating via APIs.
- **Modular monolith**: One deployment unit but clean, well-bounded internal modules — a pragmatic middle ground (start here, split later if needed).
- **Service-oriented architecture (SOA)**: An older enterprise style based on coarse-grained reusable services (often via ESB) — predecessor to microservices.

## SOLID Principles
- **Single Responsibility Principle (SRP)**: A class/module should have exactly one reason to change — one responsibility (the backbone of maintainable code).
- **Open/Closed Principle (OCP)**: Software entities should be open for extension but closed for modification — add behavior via polymorphism/strategy, not edits.
- **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types without altering correctness — don't break the contract.
- **Interface Segregation Principle (ISP)**: Clients should not depend on interfaces they don't use — split fat interfaces into smaller specific ones.
- **Dependency Inversion Principle (DIP)**: High-level modules should not depend on low-level modules; both should depend on abstractions — invert the dependency direction.

## Design Principles & Patterns (GoF)
- **Design patterns**: Reusable, proven solutions to recurring design problems — categorized as Creational, Structural, and Behavioral.
- **Creational patterns** (object creation): Singleton, Factory Method, Abstract Factory, Builder, Prototype.
- **Singleton**: Ensures one instance globally — used carefully (hides dependencies, complicates tests); prefer DI-controlled singletons.
- **Factory Method**: Define an interface for creating objects; subclasses decide which class to instantiate.
- **Abstract Factory**: Create families of related objects without specifying concrete classes.
- **Builder**: Construct complex objects step-by-step — good for objects with many optional parameters (e.g., request builders).
- **Structural patterns** (composition): Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight.
- **Adapter**: Convert one interface to another so incompatible classes work together.
- **Decorator**: Add behavior to objects dynamically by wrapping them (e.g., logging, caching, retrying) without changing their interface.
- **Facade**: Provide a simplified unified interface to a complex subsystem.
- **Proxy**: A stand-in that controls access to the real object (lazy loading, access control, remote proxy, caching).
- **Composite**: Treat individual objects and compositions of objects uniformly (tree structures like file systems).
- **Behavioral patterns** (interaction): Strategy, Observer, Command, Template Method, State, Chain of Responsibility, Iterator, Mediator, Memento.
- **Strategy**: Encapsulate interchangeable algorithms behind an interface — swap at runtime (e.g., different payment methods, sort algorithms).
- **Observer**: One-to-many dependency — when the subject changes, all observers are notified (event systems, pub/sub).
- **Command**: Encapsulate a request as an object — enables undo, queuing, and transactional behavior.
- **Template Method**: Define the skeleton of an algorithm, letting subclasses override specific steps.
- **State**: Allow an object to change behavior when its internal state changes (e.g., order status, workflow).
- **Chain of Responsibility**: Pass a request along a chain of handlers until one handles it (middleware pipelines).

## Architectural Patterns
- **Layered (N-tier) architecture**: Presentation → Application → Domain → Infrastructure — classic separation but can leak dependencies.
- **Hexagonal architecture (Ports & Adapters)**: Core domain in the middle; adapters (DB, HTTP, messaging) plug in via ports — isolate the business logic.
- **Onion architecture**: Variant of hexagonal — dependencies point inward toward the domain model; infrastructure on the outside.
- **Clean architecture**: Uncle Bob's version — concentric circles with the enterprise/use-case/domain core; dependency rule points inward.
- **Dependency Rule (Clean Arch)**: Source code dependencies only point inward; outer layers (UI, DB, frameworks) depend on inner (use cases, entities).
- **Domain-Driven Design (DDD)**: Approach focusing on the business domain and its language (ubiquitous language) to model software.
- **Bounded context**: A boundary where a domain model applies consistently — different contexts have their own models/terms for the same concept.
- **Entities vs Value Objects (DDD)**: Entities have identity and continuity; value objects are immutable and defined by their attributes.
- **Aggregates (DDD)**: Clusters of related entities/value objects treated as one unit — changes go through the aggregate root.
- **Repositories**: Provide collection-like access to aggregates — abstract the persistence mechanism (part of infrastructure).
- **Application services**: Orchestrate use cases/transactions — coordinate domain objects, don't contain business rules.
- **Event sourcing**: Persist all domain events as the source of truth instead of current state; rebuild state by replaying events.
- **CQRS (Command Query Responsibility Segregation)**: Separate write (commands) models from read (queries) models — enables independent scaling/optimization.
- **Event-driven architecture (EDA)**: Systems communicate via events (async, decoupled) — producers don't know consumers.
- **Message-driven vs event-driven**: Message-driven = command/request-response with a known destination; event-driven = state-change notification broadcast to subscribers.
- **Outbox pattern**: Write domain changes and an "outbox" event in the same DB transaction; a relay publishes to the message broker — guarantees at-least-once delivery.
- **Saga pattern**: Distributed transaction across services via a sequence of local transactions with compensating actions on failure.
- **Choreography vs orchestration (Sagas)**: Choreography = each service reacts to events (decoupled, hard to trace); orchestration = central coordinator (explicit, single point).
- **Strangler fig pattern**: Incrementally replace a legacy monolith with new services piece by piece until the old is "strangled".

## Concurrency & Asynchronous Patterns
- **Thread safety**: Object/function safe to use from multiple threads — via immutability, locks, or confinement.
- **Locks**: Mutex (mutual exclusion), read-write lock (many readers / one writer), reentrant lock (same thread can re-acquire).
- **Deadlock**: Two+ threads wait forever holding locks each other needs — avoid via lock ordering, timeouts, or single global lock.
- **Race condition**: Behavior depends on the timing/interleaving of threads — guard shared state or use atomic operations.
- **Atomic operations**: Lock-free primitives (CAS — compare-and-swap) used in concurrent data structures.
- **Volatile keyword**: Ensures visibility of writes across threads (not atomicity) — use atomic classes for increments.
- **Thread pool**: Reuse a fixed set of threads to avoid creation overhead — tune size to CPU-bound vs I/O-bound work.
- **CPU-bound vs I/O-bound**: CPU-bound = compute heavy (threads ≈ cores); I/O-bound = waiting on I/O (more threads or async/event-loop).
- **Async/await**: Non-blocking concurrency model — yields the thread during I/O, improving scalability with fewer threads.
- **Event loop**: Single-threaded async model (Node.js, Netty) — never block the loop with sync/blocking calls.
- **Actor model**: Concurrency via isolated actors communicating by messages (Akka, Erlang) — no shared state, high resilience.
- **Semaphore**: Controls access to a limited number of resources (e.g., connection pools).
- **Producer-consumer pattern**: Producers add to a queue, consumers process — decouple and buffer work (bounded queue with blocking).
- **Circuit breaker**: Wrap calls to flaky dependencies — after N failures, trip open and fail fast, then half-open to retry.
- **Bulkhead pattern**: Isolate failures — separate pools/queues per dependency so one failing service doesn't exhaust all resources.
- **Retry with backoff**: Retry transient failures with exponential + jittered delays; avoid retry storms.
- **Timeouts everywhere**: Always set connection/read/write timeouts on HTTP, DB, and external calls to avoid thread exhaustion.

## Caching & Performance Patterns
- **Cache-aside (lazy loading)**: Read: check cache → miss → load from DB → write cache. Write: update DB, invalidate/delete cache.
- **Write-through cache**: Write to cache and DB together — cache always consistent, but write latency higher and DB redundant for rarely-read data.
- **Write-back (write-behind)**: Write to cache first, asynchronously flush to DB — high write throughput, risk of data loss on crash.
- **Cache invalidation**: The hard problem — TTL, versioning, or explicit invalidation on writes (delete vs update).
- **Cache stampede (thundering herd)**: Many requests miss simultaneously and hammer the DB — use single-flight/coalescing and jittered TTLs.
- **TTL (Time-to-live)**: Expire cache entries; add random jitter to avoid synchronized mass expiry.
- **Cache consistency**: Trade-off between staleness and performance — choose TTL short enough for acceptable staleness.
- **Content-based caching**: HTTP caching (ETag, Cache-Control, Last-Modified) at CDN/edge for static and dynamic content.
- **Read-through vs write-through**: Read-through = cache loads from DB on miss; write-through = cache writes to DB on write.
- **Local vs distributed cache**: Local (in-process, fastest, per-node) vs distributed (Redis/Memcached, shared across nodes, consistency).

## Database Design & Performance
- **Normalization (1NF–3NF)**: Eliminate redundancy — 1NF atomic values, 2NF remove partial dependencies, 3NF remove transitive dependencies.
- **Denormalization**: Intentionally add redundancy (duplicated columns, precomputed aggregates) for read performance.
- **Indexing**: B-tree for range/lookup on columns; covering indexes to avoid table lookups; composite key order matters (leftmost prefix).
- **Index trade-offs**: Each index slows writes (extra maintenance) — index what you actually query, not everything.
- **Query optimization**: Use `EXPLAIN` — check for full table scans, index usage, sort/hash operations; rewrite bad queries.
- **N+1 query problem**: Loading a list then one query per item — fix with JOIN, eager loading, or batching.
- **Connection pooling**: Reuse DB connections (expensive to create) — size pool ~ cores×2 + slow I/O factor; watch for exhaustion.
- **Transactions**: ACID guarantees — use short transactions; never hold transactions across network/remote calls.
- **Isolation levels**: Read uncommitted, read committed (default in PG/Oracle), repeatable read (MySQL default), serializable — trade consistency vs concurrency.
- **Pessimistic vs optimistic locking**: Pessimistic = lock rows on read; optimistic = version/check at write (higher concurrency, retry on conflict).
- **Partitioning**: Split a table by key (range, hash, list) — improves manageability and query pruning.
- **Sharding**: Distribute data across multiple DB instances/nodes (horizontal scaling) — adds complexity for joins/transactions.

## Distributed Systems Concepts
- **CAP theorem**: In a partition, choose Consistency or Availability (CP vs AP) — you can't have all three simultaneously.
- **Consistency models**: Strong (linearizable), eventual (converges over time), causal, read-your-writes — choose per data need.
- **ACID vs BASE**: ACID = strong consistency for relational; BASE (Basically Available, Soft state, Eventually consistent) for NoSQL/distributed.
- **Leader election**: One node coordinates writes (Raft, Paxos, ZooKeeper, etcd) — failover when leader dies.
- **Consensus algorithms**: Raft/Paxos — allow distributed nodes to agree on a value safely despite failures.
- **Quorum**: Read/write quorums (e.g., W+R > N) to ensure latest data is read — trade consistency vs availability.
- **Replication**: Primary-secondary (async/sync) or multi-primary; determines read scaling, failover, and consistency.
- **Gossip protocol**: Nodes exchange state with peers to reach cluster-wide awareness (Cassandra, Redis cluster) — no central registry.
- **Idempotency**: Operations safe to repeat without side effects — use idempotency keys so retries don't double-apply.
- **At-least-once vs exactly-once**: Messaging semantics — at-least-once + idempotent consumers is the practical norm.
- **Timeouts & retries in distributed systems**: Always add timeouts; use circuit breakers, exponential backoff, and jitter.
- **Distributed tracing**: Trace a request across services (trace ID, spans) — with OpenTelemetry/Jaeger for debugging latency.
- **Distributed locking**: Redis (Redlock), ZooKeeper, or DB advisory locks — avoid if simpler alternatives exist.

## Testing & Quality
- **Test pyramid**: Many unit tests, fewer integration tests, few end-to-end tests — fast feedback and reliability.
- **Unit tests**: Test a single unit in isolation (mocked dependencies) — fast, catch regressions early.
- **Integration tests**: Test units together (real DB, real HTTP to internal services) — catch contract/interface issues.
- **Contract testing**: Verify a service's API matches the consumer's expectation without full e2e (consumer-driven).
- **Test doubles**: Stub (fixed response), mock (verify interactions), spy, fake (working in-memory implementation).
- **Test-Driven Development (TDD)**: Write failing test → implement → refactor — short cycles ensuring testability.
- **Mutation testing**: Introduce small bugs and check if tests catch them — measures test effectiveness.
- **Coverage**: Line/branch coverage — 100% isn't the goal; meaningful assertions on critical logic matter more.
- **Property-based testing**: Generate random inputs and assert invariants (QuickCheck/Hypothesis) — find edge cases manually missed.
- **Static analysis & linters**: Catch bugs/style issues without running code (SonarQube, ESLint, SpotBugs).

## Pragmatic & Engineering Practices
- **YAGNI**: You Aren't Gonna Need It — don't build speculative features; keep the design minimal for current requirements.
- **DRY**: Don't Repeat Yourself — avoid duplication; but a little duplication is better than a wrong premature abstraction.
- **KISS**: Keep It Simple, Stupid — simplicity beats cleverness; simplest solution that meets requirements.
- **Convention over configuration**: Use sensible defaults to reduce decision burden (major frameworks follow this).
- **Composition over inheritance**: Prefer composing small objects over deep inheritance hierarchies (more flexible, less brittle).
- **Fail fast vs fail safe**: Fail fast surfaces bugs early; fail safe degrades gracefully — choose per context.
- **Graceful degradation**: When a dependency fails, degrade functionality (cached data, defaults) rather than crashing the whole app.
- **Backward compatibility**: Never break existing API consumers — version APIs, add fields not remove, deprecate before deleting.
- **Feature flags**: Toggle features at runtime — safe rolling out, kill switches, and A/B testing.
- **Technical debt**: Recognize short-term compromises; track and refactor them deliberately (never "later" indefinitely).
- **Boy Scout rule**: Leave the code better than you found it — incremental improvements keep debt manageable.
- **Code review**: Structured review for correctness, design, security, and readability — catch bugs antes de merge.
- **Documentation**: Code documents "how"; docs/README/ADR document "why" — decisions, constraints, and context.

## Common Anti-patterns to Avoid
- **God object**: A class that knows/does too much — violates SRP; refactor into smaller focused classes.
- **Golden hammer**: Forcing a familiar tool/pattern everywhere (e.g., microservices for a tiny app).
- **Premature optimization**: Optimizing before measuring — profile first, then optimize the real bottleneck.
- **Spaghetti code**: Unstructured tangled control flow — refactor into small, named, single-purpose pieces.
- **Stovepipe (silo) architecture**: Systems that can't share data/integrate — favor standardized interfaces.
- **Reinventing the wheel**: Hand-rolling mature solutions (DBs, queues, auth) instead of using proven libraries/services.
- **DTOs leaking everywhere**: Exposing internal entities as API contracts — separate internal model from external DTOs.
- **Inappropriate intimacy**: Classes knowing too much about each other's internals — hide internals, communicate via interfaces.
- **Copy-paste programming**: Duplicated logic — extract to shared tested helpers (with care for DRY misuse).