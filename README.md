# Knowledge Sharing & Engineering Reference

A curated, production-grade knowledge base and technical reference covering software architecture, distributed systems, backend engineering, cloud infrastructure, databases, and DevOps.

All technical guides are enriched with professional, hand-drawn-style architectural diagrams (rendered via Excalidraw) with clear visual flows and zero-crossing layouts to make complex concepts intuitive.

Designed for senior software engineers, backend architects, and interview preparation.

---

## 📚 Table of Contents

### 1. System Design & Software Architecture
- [Software Design & Architecture](software-design-architecture.md) — Architectural patterns (Monolith, Modular Monolith, Microservices), SOLID principles, GoF patterns, C4 model, DDD, and NFRs.
- [System Design](system-design.md) — End-to-end system design methodology, scalability patterns, rate limiting, consistent hashing, caching strategies, and real-world architectures.
- [Distributed Systems](distributed-systems.md) — CAP & PACELC theorems, consensus protocols (Raft, Paxos), distributed transactions (2PC, Saga), replication, and fault tolerance.
- [Software Architecture & Leadership](software-architect.md) — Engineering leadership, Architecture Decision Records (ADRs), trade-off analysis, tech debt management, and agile delivery.
- [API Design](api-design.md) — RESTful best practices, gRPC vs GraphQL, HTTP/1.1 to HTTP/3, idempotency, rate limiting, and API security.

### 2. Programming Languages & Frameworks
- [Java](java.md) — Core Java, Generics, Collections Framework, Concurrency & Multithreading, JVM Memory & GC, Streams, and Modern Java (Java 8–21+).
- [Spring Boot](spring-boot.md) — IoC & DI, Autoconfiguration internals, Actuators, Spring MVC, Spring Data JPA/Hibernate, Spring Security (OAuth2/JWT), and Spring Cloud.

### 3. Databases, Caching & Storage
- [Databases](databases.md) — Relational internals, normalization, B-Trees & indexes, query planning, ACID guarantees, transaction isolation, and NoSQL models.
- [SQL](sql.md) — Complex joins, window functions, CTEs, aggregation techniques, query tuning, and common interview patterns.
- [MySQL](mysql.md) — MySQL administration, performance diagnostics, server configurations, and setup workflows.
- [Redis](redis.md) — In-memory data structures, single-threaded event loop, eviction algorithms, persistence (RDB/AOF), replication, and Redis Cluster.
- [DynamoDB](dynamodb.md) — Partition keys, sort keys, GSIs & LSIs, single-table design, DynamoDB Streams, and consistency models.
- [Elasticsearch](elasticsearch.md) — Distributed search architecture, inverted indexes, Lucene internals, sharding, mappings, aggregations, and cluster sizing.
- [Storage Systems](storage.md) — Storage hierarchy, Block vs File vs Object storage, durability metrics (11 9s), replication topologies, and lifecycle management.

### 4. Cloud, Infrastructure & DevOps
- [AWS](aws.md) — Core AWS services (EC2, S3, IAM, VPC, Lambda, ECS, RDS), Well-Architected Framework, multi-region high availability, and cost optimization.
- [Docker](docker.md) — Container virtualization, namespaces & cgroups, multi-stage builds, layer caching, security hardening, and Docker Compose.
- [Kubernetes](kubernetes/kubernetes.md) — Architecture (Control Plane vs Worker), Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, PV/PVC, HPA, and Kind setups.
- [DevOps & SRE](devops.md) — Infrastructure as Code (Terraform), Observability (Prometheus, Grafana, OpenTelemetry, Datadog), Service Mesh (Istio/Envoy), and SRE principles.
- [CI/CD Pipelines](ci-cd.md) — CI/CD automation, pipeline stages, testing pyramid, artifact registries, GitOps with ArgoCD, and zero-downtime deployment strategies.
- [Linux](linux.md) — Linux kernel vs user space, Virtual File System (VFS), process management, signals, memory diagnostics, and networking utilities.
- [Computer Networks](networks.md) — OSI vs TCP/IP models, TCP 3-way handshake & flow control, UDP, HTTP/1.1 vs HTTP/2 vs HTTP/3, HTTPS/TLS handshake, DNS, Proxies, and CDNs.
- [Git & GitHub](git-github.md) — Advanced Git branching workflows, cherry-picking, interactive rebasing, merge vs rebase, git hooks, and release tags.

### 5. Emerging Tech & Career
- [Generative AI & LLMs](gen-ai.md) — Transformer architecture, attention mechanisms, fine-tuning (LoRA, QLoRA), RAG pipelines, vector databases, prompt engineering, and LLM agent frameworks.
- [Apache Kafka](kafka.md) — Event streaming, topic partitioning, consumer groups, offsets, retention, Kafka Streams, and Kafka Connect.
- [Engineering Roles & Industry Career Maps](Eng-roles/) — Comprehensive career rubrics, levels, and engineering expectations across Spotify, Instagram, and YouTube.
- [Backend Resume Optimization](resume-optimization-backend.txt) — ATS keyword strategies, metric-driven impact framing, and resume optimization for senior backend roles.

---

## 🚀 Live Site
This repository powers the live technical notes at **[blog.vanchanr.tech](https://blog.vanchanr.tech)**.
