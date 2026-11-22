#!/usr/bin/env python3
"""Generate perfected CI/CD and DevOps Observability architecture diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_cicd():
    d = DiagramBuilder()
    d.add_header(
        "Modern CI/CD & GitOps Continuous Delivery Architecture",
        "Automated Pull Request Validation, Immutable OCI Artifact Signing, and GitOps Pull Reconciliation",
        x=40, y=25, w=1220, h=65
    )

    # 1. Left Container: CI Pipeline (x=40..630, w=590)
    d.add_container(40, 110, 590, 500, label="Continuous Integration (CI Engine: GitHub Actions / GitLab CI)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # Row 1 (CI Flow): Developer -> Verification -> Build & Push
    d.add_box(60, 155, 130, 70, "Developer PR", "Feature branch commit\nWebhook triggers CI", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(190, 190, 230, 190, label="Triggers CI", stroke="#1971c2", label_offset_y=-16, font_size=11)

    d.add_box(230, 155, 175, 70, "Automated Verification", [
        "• Lint & Spotless format",
        "• Compile & Unit tests",
        "• Security SAST & Trivy"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(405, 190, 445, 190, label="Pass", stroke="#2b8a3e", label_offset_y=-16, font_size=11)

    d.add_box(445, 155, 165, 70, "Docker Buildx & ECR", "Builds multi-arch image;\nSigns digest via Cosign", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Row 2 (Details): OCI Immutable Artifacts
    d.add_box(60, 255, 550, 80, "Immutable OCI Container Artifacts (Amazon ECR / Harbor Registry)", [
        "• Tagged with immutable git commit SHA and cryptographically verified sha256 digest.",
        "• Signed software bill of materials (SBOM) and SLSA Level 3 provenance attestations.",
        "• Zero Mutable Tags: Deploying mutable ':latest' or ':dev' tags is strictly prohibited."
    ], bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Row 3 (Invariants): CI Architecture Invariants
    d.add_box(60, 360, 550, 175, "Continuous Integration (CI) Architectural Invariants", [
        "• Shift-Left Security: Block PR merge immediately if SAST, secrets, or CVE scans fail.",
        "• Ephemeral Runners: Every workflow executes in isolated, single-use container runners.",
        "• Reproducibility: Strict dependency lockfiles (pom.xml, yarn.lock, go.sum) enforce builds.",
        "• Speed Optimization: Heavy layer caching via GitHub Actions cache or registry caches.",
        "• Blast Radius Containment: CI runners never have direct write credentials to production K8s."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 2. Right Container: GitOps CD (x=710..1260, w=550)
    d.add_container(710, 110, 550, 500, label="GitOps Continuous Deployment (CD: ArgoCD / Flux)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    # Row 1 (CD Entry): GitOps Manifest Repo
    d.add_box(730, 155, 510, 70, "GitOps Config Repository (Single Source of Truth)", "Declarative Kubernetes manifests (Helm / Kustomize) version-controlled in Git.\nCI bot automatically commits new image digest sha256:7b9... on PR merge", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    # Arrow connecting CI Buildx to GitOps Repo (horizontal between containers, gap = 120px)
    d.add_arrow(610, 190, 730, 190, label="Commit Digest", stroke="#9c36b5", label_offset_y=-16, label_bg="#ffffff", font_size=11)

    # Arrow from GitOps Repo down to ArgoCD
    d.add_arrow(985, 225, 985, 255, label="Poll Git State (In-Cluster Pull)", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # Row 2 (Operator): ArgoCD
    d.add_box(730, 255, 510, 60, "ArgoCD / Flux In-Cluster Operator", "Continuously reconciles Desired State (Git) vs Live State (K8s cluster);\nDetects and automatically heals out-of-band configuration drift", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Arrow from ArgoCD down to Production Cluster
    d.add_arrow(985, 315, 985, 345, label="Applies Desired State (Canary Rollout)", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # Row 3 (Cluster): Production Kubernetes
    d.add_box(730, 345, 510, 65, "Production Kubernetes Cluster (Worker Nodes)", "Executes zero-downtime rolling update / Canary traffic shifting;\nNode Kubelets pull cryptographically verified image digest from ECR", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Row 4 (Invariants): GitOps CD Invariants
    d.add_box(730, 430, 510, 160, "GitOps CD Architectural Invariants", [
        "• Pull Model: Operator inside cluster pulls configs; NO inbound firewall holes required.",
        "• Anti-Drift: Manual edits via 'kubectl' are auto-reverted to Git desired state.",
        "• Instant Rollback: 'git revert <commit>' instantly restores known healthy cluster state.",
        "• Immutable Audit Trail: Every infrastructure modification is tracked via Git commit log."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Master Invariant Banner
    d.add_box(40, 630, 1220, 50, "Core Delivery Invariant: Git is the single source of truth; CI tests & packages code, GitOps pulls & reconciles production.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("cicd-pipeline-gitops-flow.png")

def generate_devops():
    d = DiagramBuilder()
    d.add_header(
        "The Three Pillars of Site Reliability Observability",
        "Metrics (Numeric Telemetry), Logs (Structured Events), and Distributed Traces (Call Graphs)",
        x=40, y=25, w=1220, h=65
    )

    # 3 Pillars side-by-side: each w=380, gaps=40
    # Pillar 1: Metrics (x=40..420, w=380)
    d.add_container(40, 110, 380, 430, label="1. Metrics (Aggregated Telemetry)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    d.add_box(60, 155, 340, 65, "Numeric Time-Series Data", "Key-value pairs + timestamp:\nhttp_requests_total{code='500'} 42", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(60, 230, 340, 115, "Four Golden Signals", [
        "• Latency: Time taken to serve a request",
        "• Traffic: Demand placed on system (RPS)",
        "• Errors: Rate of requests that fail",
        "• Saturation: Resource usage (CPU, RAM)"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(60, 355, 340, 65, "Tooling & Protocols", "Prometheus (Pull scraper), VictoriaMetrics,\nOpenTelemetry metrics, Grafana Dashboards", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)

    d.add_box(60, 430, 340, 95, "Primary Superpower & Trade-Off", [
        "• Strengths: Low storage cost; fast alerting.",
        "• Limits: Needs contextual logs for root-cause."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Pillar 2: Logs (x=460..840, w=380)
    d.add_container(460, 110, 380, 430, label="2. Logs (Contextual Event Records)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    d.add_box(480, 155, 340, 65, "Structured JSON Events", "Timestamp, log level, message & metadata:\n{\"time\":\"...\",\"lvl\":\"ERR\",\"err\":\"Timeout\"}", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(480, 230, 340, 115, "Log Structuring Standards", [
        "• Structured JSON: Machine-parsable fields",
        "• Context: Inject user_id, order_id, tenant",
        "• Correlation: trace_id & span_id included",
        "• Levels: DEBUG, INFO, WARN, ERROR, FATAL"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    d.add_box(480, 355, 340, 65, "Tooling & Protocols", "Grafana Loki (Label indexing), FluentBit,\nElasticsearch / Logstash, AWS CloudWatch", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)

    d.add_box(480, 430, 340, 95, "Primary Superpower & Trade-Off", [
        "• Strengths: Rich context for post-mortems.",
        "• Limits: High storage cost at massive volume."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Pillar 3: Distributed Traces (x=880..1260, w=380)
    d.add_container(880, 110, 380, 430, label="3. Distributed Traces (Request Journeys)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")

    d.add_box(900, 155, 340, 65, "Call Graph Spans (DAG)", "End-to-end request path across services\nwith per-operation duration & hierarchy", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(900, 230, 340, 115, "Context Propagation (W3C)", [
        "• Traceparent: Encodes version, trace_id",
        "• TraceID: Unique 128-bit global transaction ID",
        "• SpanID: Unique 64-bit per-operation ID",
        "• ParentSpanID: Establishes causal hierarchy"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(900, 355, 340, 65, "Tooling & Protocols", "OpenTelemetry (OTel SDK), Jaeger Tracing,\nGrafana Tempo, AWS X-Ray, Zipkin", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)

    d.add_box(900, 430, 340, 95, "Primary Superpower & Trade-Off", [
        "• Strengths: Pinpoints latency bottlenecks.",
        "• Limits: Tracing overhead requires sampling."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Bottom Unified Correlation Workflow Container (x=40..1260, w=1220, h=115)
    d.add_container(40, 560, 1220, 115, label="Unified Observability Correlation Workflow (OpenTelemetry Standard)", stroke="#495057", badge_bg="#f1f3f5", badge_stroke="#495057", label_color="#212529")

    # 4 Steps of correlation: each w=265, gap=30
    d.add_box(60, 605, 265, 55, "1. Metric Alert Fires", "Prometheus alerts: P99 latency > 2s", bg="#ffc9c9", stroke="#e03131", text_color="#c92a2a", font_size=11)
    d.add_arrow(325, 632, 365, 632, stroke="#495057")

    d.add_box(365, 605, 265, 55, "2. Jump to Exemplar Trace", "Grafana maps spike to TraceID", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(630, 632, 670, 632, stroke="#495057")

    d.add_box(670, 605, 265, 55, "3. Inspect Span Waterfall", "Tempo isolates 1.8s slow SQL span", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_arrow(935, 632, 975, 632, stroke="#495057")

    d.add_box(975, 605, 265, 55, "4. View Correlated Logs", "Loki filters logs matching TraceID", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.render("devops-observability-pillars.png")

if __name__ == "__main__":
    generate_cicd()
    generate_devops()
