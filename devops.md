# DevOps & Site Reliability Engineering — From Basics to Expert

## Core DevOps & SRE Principles
- **DevOps Culture (CALMS Framework)**:
  - **Culture**: Shared ownership, break down silos between development and operations.
  - **Automation**: Automate testing, provisioning, builds, and remediation.
  - **Lean**: Small batch sizes, limit Work-In-Progress (WIP), eliminate waste.
  - **Measurement**: Measure everything (deployment frequency, lead time, MTTR, change failure rate).
  - **Sharing**: Blameless postmortems, transparency, continuous learning.
- **DORA Metrics (State of DevOps Benchmarks)**:
  1. **Deployment Frequency**: How often code deploys to production (Elite: multiple per day).
  2. **Lead Time for Changes**: Time from commit to production (Elite: < 1 hour).
  3. **Time to Restore Service (MTTR)**: Time to recover from an incident (Elite: < 1 hour).
  4. **Change Failure Rate**: Percentage of deployments causing production failure (Elite: 0–15%).
- **SRE Reliability Framework**:
  - **SLI (Service Level Indicator)**: The quantifiable metric observed (e.g., HTTP successful response percentage $\frac{\text{HTTP } 2xx/3xx}{\text{Total Requests}}$).
  - **SLO (Service Level Objective)**: Target reliability agreed upon internally (e.g., 99.9% of requests succeed over 30 days).
  - **SLA (Service Level Agreement)**: Legally binding contractual guarantee with customers, with financial penalties for breach (e.g., 99.5%).
  - **Error Budget**: Allowed unreliability ($100\% - \text{SLO} = 0.1\%$). When budget is exhausted, freeze feature releases and focus exclusively on reliability.
  - **Toil Reduction**: Automate repetitive, non-creative operational work so engineers spend $>50\%$ of time on engineering projects.

## Infrastructure as Code (IaC)
- **Declarative vs Imperative**:
  - *Declarative (Terraform, CloudFormation, Kubernetes)*: Define *what* desired state you want; the engine determines execution steps.
  - *Imperative (Ansible, Bash, Python)*: Define *how* to achieve state step-by-step.
- **Terraform Best Practices**:
  - **Remote State**: Store `.tfstate` in Amazon S3 or Google Cloud Storage with versioning and encryption.
  - **State Locking**: Use DynamoDB table locking to prevent concurrent state corruption during `terraform apply`.
  - **Modules**: Reusable, parameterized infrastructure templates (e.g., standard VPC module, EKS cluster module).
  - **Drift Detection**: Regularly run `terraform plan` in scheduled CI pipelines to catch manual console out-of-band changes.

## Observability: The Three Pillars

### 1. Metrics (Aggregations over Time)
- Low cost, real-time alert generation, numeric telemetry.
- **The Four Golden Signals (Google SRE)**:
  - **Latency**: Time to service a request (distinguish between success latency and error latency).
  - **Traffic**: Demand on the system (e.g., HTTP requests per second, I/O bandwidth).
  - **Errors**: Rate of failed requests (explicit $5xx$, semantic errors, timeout violations).
  - **Saturation**: How full the service is (CPU %, memory %, database connection pool utilization).
- **Stack**: **Prometheus** (pull-based metric collection via scrape endpoints, PromQL engine) + **Alertmanager** + **Grafana** (dashboards).

### 2. Logs (Contextual Event Records)
- Structured logging (JSON format) containing timestamp, severity, service name, request ID, user ID, message, and stack trace.
- **Stack**: **Elasticsearch / OpenSearch** (indexing and full-text search) + **Fluentbit** / **Logstash** (lightweight log collectors) + **Kibana** (visualization) or **Grafana Loki** (index-by-label, low memory cost).

### 3. Distributed Tracing (Request Journeys)
- Tracks the end-to-end lifecycle of a request as it crosses multiple microservices, queues, and databases.
- **Trace & Spans**: A **Trace** represents the overall transaction; each individual service hop or database query is a **Span** with start/end time and tags.
- **Context Propagation**: Standardized headers (W3C `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`) passed downstream over HTTP and message brokers.
- **Stack**: **OpenTelemetry (OTel)** vendor-neutral instrumentation SDK + **Jaeger** or **Tempo** backends.

## Service Mesh & Traffic Management
- **The Sidecar Proxy Pattern**:
  - Injects a lightweight proxy (e.g., **Envoy**) alongside every application container inside Kubernetes pods.
  - Decouples networking logic from application business code.
- **Key Capabilities**:
  - **Mutual TLS (mTLS)**: Automatic, transparent end-to-end encryption and identity verification between all services without modifying application code.
  - **Traffic Control**: Dynamic canary splitting, request retries, timeout injection, fault injection (chaos engineering).
  - **Telemetry**: Zero-code HTTP metrics, access logs, and distributed trace generation for all service communication.
  - **Implementations**: **Istio**, **Linkerd**, **Consul Connect**.

## Web Infrastructure & Proxies
- **Forward Proxy**: Sits in front of clients; handles egress security, filtering, and caching.
- **Reverse Proxy**: Sits in front of backend servers; handles ingress routing, load balancing, SSL termination, and static asset serving (NGINX, Tomcat, Envoy).
- **Web Servers**:
  - **NGINX**: Asynchronous, event-driven, non-blocking architecture; ultra-high concurrency for static assets and reverse proxying.
  - **Tomcat**: Multi-threaded servlet container executing Java servlets, JSPs, and Spring Boot applications.
