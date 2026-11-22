# CI/CD & Delivery Pipelines — From Basics to Expert

## Core Foundations: CI vs CD
- **Continuous Integration (CI)**:
  - Developers commit and merge code frequently to a shared main branch (trunk-based development or short-lived feature branches).
  - Every push triggers an automated build and test pipeline to validate changes, detect regressions, and provide immediate feedback within minutes.
- **Continuous Delivery (CD)**:
  - Extends CI by automatically building, testing, packaging, and deploying code to staging/pre-production environments.
  - The software is always in a releasable state, but deployment to production requires manual human approval or a trigger.
- **Continuous Deployment (CD)**:
  - Fully automated from commit to production. Every passing change in the pipeline is deployed directly to end users without manual gatekeeping.

## Anatomy of a Production CI/CD Pipeline
```
[ Commit ] ➔ [ Lint & Format ] ➔ [ Compile & Build ] ➔ [ Unit Tests ]
     ➔ [ SAST & Security Scan ] ➔ [ Containerize & Sign ] ➔ [ Push Registry ]
          ➔ [ Deploy Staging ] ➔ [ Integration/E2E Tests ] ➔ [ Canary / Prod Deploy ]
```

1. **Source & Trigger**: GitHub / GitLab Webhook on pull requests or main branch merges.
2. **Linting & Code Quality**: Enforces formatting standards (`Spotless`, `Checkstyle`, `ESLint`) and static analysis (`SonarQube`) checking for code smells and test coverage thresholds.
3. **Compile & Unit Test**: Fast, hermetic unit tests (`JUnit 5`, `pytest`). Must finish in under 3–5 minutes.
4. **Security & Vulnerability Scanning**:
   - **SAST (Static Application Security Testing)**: Scans source code for security flaws (e.g., Semgrep, CodeQL).
   - **SCA (Software Composition Analysis)**: Checks third-party libraries for known CVEs (e.g., Snyk, Dependabot).
   - **Container Vulnerability Scanning**: Scans base OS layers and packages (e.g., Trivy, Clair).
5. **Artifact Packaging & Provenance**:
   - Docker image build using multi-stage builds.
   - Tagging with Git commit SHA and semantic version (avoid mutable `:latest` tags in production).
   - Image signing via **Cosign** (Sigstore) and generating **SBOM (Software Bill of Materials)**.
6. **Push to Registry**: Secure storage in Amazon ECR, Google Artifact Registry, or Harbor.

## Zero-Downtime Deployment Strategies

### 1. Rolling Deployment
- Incrementally updates instances/pods with the new version until all are updated.
- *Pros*: Resource-efficient; no extra infrastructure needed.
- *Cons*: During rollout, both old and new versions run concurrently (requires backwards-compatible APIs and database migrations); rollback takes time.

### 2. Blue-Green Deployment
- Maintains two identical production environments: **Blue** (active traffic) and **Green** (idle/new version).
- Deploy new release to Green, run smoke tests, then switch the router/load balancer instantly to point traffic to Green.
- *Pros*: Zero downtime, instantaneous rollback (switch router back to Blue if errors spike).
- *Cons*: Doubles infrastructure resource costs during deployment.

### 3. Canary Deployment
- Releases the new version to a small subset of servers or users (e.g., 2%–5%) while the remaining 95% stay on the stable version.
- Automated metric verification evaluates error rates, latency (P99), and CPU load. If metrics remain healthy, traffic incrementally scales: $5\% \to 25\% \to 50\% \to 100\%$.
- *Pros*: Limits blast radius; detects real-world production defects safely.
- *Cons*: Requires sophisticated routing (e.g., Envoy, Istio, Flagger, Argo Rollouts) and advanced observability.

### 4. Dark Launch / Shadowing
- Duplicates real production HTTP traffic at the load balancer and asynchronously sends a shadow copy to the new version without returning the shadow response to the client.
- *Pros*: Validates performance and scale under true production traffic with zero user risk.

## GitOps & Declarative Delivery
- **Core Principles**:
  - Entire infrastructure and application state declared declaratively in Git.
  - Git is the single source of truth and single audit log.
  - Automated software agents continuously reconcile live cluster state with Git state.
- **Pull-Based (GitOps) vs Push-Based CI/CD**:
  - *Push-Based*: CI runner has direct write/admin credentials to Kubernetes cluster and executes `kubectl apply` (security risk if CI runner is compromised).
  - *Pull-Based*: An in-cluster controller (e.g., **ArgoCD**, **Flux**) polls Git and pulls changes inward. Cluster credentials never leave the cluster perimeter.

## The Testing Pyramid
- **Unit Tests (70%)**: Fast, isolated, test single classes/functions with mocks. Run on every commit.
- **Integration Tests (20%)**: Test interactions between components (e.g., Spring Boot + PostgreSQL via `Testcontainers`). Run before packaging.
- **End-to-End / Contract Tests (10%)**: Test full business journeys through APIs and UI (`Playwright`, `Pact` for consumer-driven contracts). Run against staging.
