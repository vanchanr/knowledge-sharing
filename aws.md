# AWS — From Basics to Expert

## Core Concepts & Global Infrastructure
- **Regions**: Geographic locations (us-east-1, eu-west-1, ap-south-1) with 2+ isolated Availability Zones each; choose based on latency, compliance, and cost.
- **Availability Zones (AZs)**: Isolated data centers within a region with independent power, cooling, and network; use multiple AZs for high availability.
- **Edge locations**: PoPs for CloudFront CDN caching and Route 53 latency-based routing; not AZs.
- **Account & root user**: The email-based root user has unrestricted access — enable MFA and use IAM Users/Roles for daily work.
- **IAM (Identity and Access Management)**: Manages users, groups, roles, and policies to control access (who can do what on which resource).
- **Policies**: JSON documents with `Effect`, `Action`, `Resource`, `Condition`; IAM policy evaluation is "explicit deny wins".
- **IAM Roles**: Identity with permissions assumed by users, services, EC2s, or Lambdas (not tied to a person) — use roles over long-term keys.
- **IAM Best practices**: Least privilege, root MFA, no hardcoded keys, use roles/key rotation, enable CloudTrail for audit.
- **Shared Responsibility Model**: AWS secures the cloud (hardware, network, hypervisor); you secure what's in the cloud (data, IAM, configs).
- **Well-Architected Framework**: Six pillars — Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability.
- **Service quotas (limits)**: Per-region defaults (e.g., 5 EIPs, 200 security groups/EC2, 1152 vCPUs) — request increases via Support.
- **CloudTrail**: Audits all API activity in the account (who did what, when) — enable in all regions for security/compliance.
- **CloudWatch**: Monitoring service for logs (`/aws/...`), metrics (CPU, memory via agent), alarms, dashboards, and events.

## Compute: EC2 & Auto Scaling
- **EC2 (Elastic Compute Cloud)**: Virtual servers with instance types (compute, memory, storage, GPU optimized).
- **Instance families**: t (burstable), m (general purpose), c (compute), r (memory), i/d (storage), g/p (GPU).
- **Burstable instances (t2/t3)**: Use CPU credits; can burst above baseline then throttle — avoid for sustained load.
- **Amazon Machine Image (AMI)**: The template for launching instances (OS, apps, config) — customize with golden AMIs for consistency.
- **Instance store vs EBS**: Instance store is ephemeral (fast, data lost on stop); EBS is durable block storage (survives stop/terminate).
- **EBS volume**: Network-attached block storage; types — gp3/gp2 (SSD general), io1/io2 (provisioned IOPS), st1/sc1 (HDD throughput/cold).
- **EBS snapshots**: Incremental backups (first is full, then deltas); can be copied across regions for DR.
- **Security groups (SGs)**: Instance-level stateful firewall (allow rules only) — default deny inbound, allow all outbound.
- **SG vs NACL**: SG is stateful, at instance level, allow-only; NACL is stateless, at subnet level, allow+deny rules.
- **Key pairs**: SSH public/private keys for Linux access; Windows uses encrypted administrator password.
- **User data**: Script run at first boot — use for bootstrapping (install software, configure).
- **Metadata service**: `169.254.169.254/latest/meta-data` — instance metadata (IMDSv2 token-based recommended); used to fetch IAM role creds.
- **Elastic IP (EIP)**: Static public IPv4 (limited to 5/region unless increased); prefer ALB/NAT over EIP where possible.
- **EC2 pricing models**: On-Demand, Reserved (1/3yr discount), Savings Plans, Spot (up to 90% off, can be interrupted), Dedicated Hosts.
- **Spot instances**: Interruptible capacity for batch/fault-tolerant workloads; use for cost savings with 2-min warning.
- **Auto Scaling Group (ASG)**: Maintains desired instance count, scales based on CloudWatch alarms or schedules, replaces unhealthy.
- **Launch template**: Defines what ASG instances use (AMI, instance type, SG, user data) — versioned, preferred over launch config.
- **Placement groups**: Cluster (low latency, same rack), Spread (isolated across hardware), Partition (fault domains for HDFS/Cassandra).
- **Lifecycle hooks**: Pause instances during scale-in/out for custom actions (drain connections, backups) before termination.
- **Load balancer + ASG**: Standard high-availability pattern — LB in front, ASG behind, health checks route only to healthy instances.

## Load Balancing & DNS
- **Elastic Load Balancing (ELB)**: Managed load balancing — three types: ALB, NLB, GWLB.
- **Application Load Balancer (ALB)**: Layer 7 (HTTP/S) — path/host-based routing, WebSocket, gRPC, Lambda targets, sticky sessions.
- **Network Load Balancer (NLB)**: Layer 4 (TCP/UDP/TLS) — extreme performance, static IPs, preserves client source IP.
- **Target groups**: Logical grouping of targets (instances, IPs, Lambda) that the LB routes to; health checks per target group.
- **Health checks**: HTTP/HTTPS/TCP probes against `/health` endpoints — used by LB and ASG to remove unhealthy targets.
- **Cross-zone load balancing**: Distributes traffic evenly across healthy targets in all AZs (enabled by default on ALB/NLB).
- **Sticky sessions (session affinity)**: Cookie-based (ALB) or source-IP-based (NLB) to pin a client to the same target.
- **Route 53**: AWS DNS service — record types (A, AAAA, CNAME, MX, TXT, SRV), domain registration, and health checks.
- **Route 53 routing policies**: Simple, Weighted, Latency-based, Geolocation, Geoproximity, Failover, Multi-value.
- **Route 53 failover**: Uses health checks to route traffic away from unhealthy endpoints (active-passive or active-active).
- **CNAME vs Alias**: Alias (Route 53) works at zone apex and routes to AWS resources (ELB, CF, S3) — no extra charge, no CNAME limitations.
- **TTL**: Time-to-live on DNS records — lower for failover speed, higher for lower DNS cost/load on resolvers.

## Networking & VPC
- **VPC (Virtual Private Cloud)**: Isolated virtual network; every region has a default VPC, but create custom ones with planned CIDRs.
- **Subnets**: Ranges within the VPC CIDR — public (has route to IGW) vs private (no direct internet route).
- **Internet Gateway (IGW)**: Horizontally scaled, redundant component allowing internet access from VPC (attached to VPC, not subnet).
- **NAT Gateway**: Managed service enabling outbound internet from private subnets (e.g., for updates) — ~$0.045/hr + data.
- **NAT vs IGW**: NAT allows one-way (outbound) internet from private subnets; IGW allows both directions for public subnets.
- **Route tables**: Define where traffic goes per subnet (e.g., 0.0.0.0/0 → IGW, 0.0.0.0/0 → NAT for private).
- **NACL (Network ACL)**: Stateless subnet-level firewall with ordered rules (allow/deny) — both inbound and outbound must allow return traffic.
- **VPC Peering**: Direct private connection between two VPCs (no transitive routing; no overlapping CIDRs).
- **Transit Gateway (TGW)**: Hub-and-spoke networking connecting many VPCs, VPNs, and Direct Connect — simplifies complex topologies.
- **VPC Endpoints**: Private connection to AWS services (S3, DynamoDB) without internet — Gateway (S3/DDB) or Interface (ENI) type.
- **VPN (Site-to-Site)**: Encrypted IPsec tunnel between on-prem and VPC over the internet.
- **Direct Connect**: Dedicated physical network connection to AWS (low latency, consistent bandwidth, for hybrid).
- **AWS PrivateLink**: Expose a service in your VPC to other VPCs/accounts privately via endpoint services.
- **ENI (Elastic Network Interface)**: Virtual network card attached to an instance — can attach multiple for network appliances.
- **IP addressing**: IPv4 (public/private) and IPv6 (dual-stack); each ENI gets a private IP from the subnet's range.
- **Elastic IP vs public IP**: Public IP changes on stop/start; EIP is static (extra cost when not attached).
- **VPC Flow Logs**: Capture IP traffic metadata (allowed/denied) — send to CloudWatch Logs/S3 for security and debugging.

## Storage: S3, EFS, EBS
- **S3 (Simple Storage Service)**: Object storage — 99.999999999% (11 nines) durability, virtually unlimited scale.
- **S3 buckets**: Global namespace (bucket names unique) but stored in a region; key = full object path.
- **Storage classes**: Standard (hot), Intelligent-Tiering (auto), S3-IA (infrequent), OneZone-IA, Glacier (archive), Glacier Deep Archive.
- **Lifecycle rules**: Automate transition to cheaper classes and expiration/deletion (e.g., after 30d → IA, 90d → Glacier, 365d → delete).
- **Versioning**: Keeps all versions of an object (protection against deletes/overwrites) — combine with lifecycle to expire old.
- **S3 encryption**: SSE-S3 (default), SSE-KMS (with key rotation/audit), SSE-C (customer keys), client-side encryption.
- **Bucket policies vs IAM**: Bucket policies (resource-based) vs IAM policies (identity-based); both are evaluated for access.
- **Access Control**: Block public access by default; use policies + ACLs (legacy) — prefer policies and IAM roles.
- **Presigned URLs**: Time-limited URLs granting temporary access to a specific object (for downloads/uploads).
- **S3 Transfer Acceleration**: Uses CloudFront edge locations to speed up uploads over long distances.
- **Multipart upload**: Upload large objects in parts (parallel, resumable) — for objects > 100MB, needed > 5GB.
- **S3 Select**: Query data inside objects (CSV/JSON/Parquet) directly with SQL — reduces transfer costs.
- **S3 events**: `s3:ObjectCreated:*`, `s3:ObjectRemoved:*` — trigger Lambda, SQS, SNS for automation.
- **Static website hosting**: Serve static sites directly from S3 (custom domain via Route 53 + CloudFront).
- **EBS**: Block storage for EC2 (mentioned above) — the building block for databases/file systems on EC2.
- **EFS (Elastic File System)**: Fully managed NFS file storage — shared across multiple EC2s/AZs; pay per use.
- **EFS vs EBS**: EBS is per-AZ block storage for one instance; EFS is region-wide shared file system for many.
- **S3 vs EFS vs EBS**: S3 = object/API for data lakes/backups; EFS = shared file system; EBS = block device for DBs.

## Database Services
- **RDS (Relational Database Service)**: Managed MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora.
- **RDS Multi-AZ**: Synchronous standby replica in another AZ — automatic failover for high availability.
- **RDS Read replicas**: Asynchronous copies for read scaling (up to 5 direct + chain) — reduce read load off primary.
- **RDS backups**: Automated backups (full daily + transaction logs, PITR to 5 min) and manual snapshots.
- **Aurora**: AWS's MySQL/PostgreSQL-compatible DB — 5x MySQL/3x Postgres throughput, 6 replicas, auto-scaling storage.
- **Aurora Serverless**: Auto-scaling capacity for intermittent/unpredictable workloads (pay per second).
- **DynamoDB**: Managed NoSQL key-value/document DB — single-digit millisecond latency, fully serverless.
- **DynamoDB capacity modes**: On-Demand (pay per request) vs Provisioned (RCU/WCU with auto-scaling).
- **DynamoDB partitions/keys**: Partition key (hash) for routing; sort key for range queries; design key for even distribution.
- **DynamoDB GSI/LSI**: Global secondary index (any key, eventual consistency) vs Local secondary index (same partition key).
- **DynamoDB DAX**: In-memory caching layer for DynamoDB (10x reads, microsecond latency) — for hot reads.
- **ElastiCache**: Managed Redis/Memcached — for caching, sessions, pub/sub, real-time data.
- **ElastiCache Redis**: Rich features (persistence, replication, clusters, streams, Lua) vs Memcached (simple, multithreaded).
- **Redshift**: Petabyte-scale columnar data warehouse (SQL) — for OLAP/BI analytics; Spectrum for S3 querying.
- **Neptune**: Managed graph database (for social/traversal workloads).
- **DocumentDB**: MongoDB-compatible document DB (for document workloads wanting MongoDB API).
- **DMS (Database Migration Service)**: Migrate DBs with minimal downtime (homogeneous or heterogeneous).

## Serverless
- **Lambda**: FaaS — run code without provisioning servers; scales automatically; pay per invocation/duration.
- **Lambda triggers**: API Gateway, S3 events, SQS/SNS, DynamoDB Streams, EventBridge, CloudWatch — event-driven.
- **Lambda limits**: Timeout 15 min, memory 128MB–10GB, package 50MB zip/250MB unzipped, 1000 concurrent executions (default).
- **Lambda cold starts**: Latency on first invocation (provisioned concurrency reduces it, at cost).
- **API Gateway**: Fully managed API frontend — REST, HTTP, WebSocket APIs; auth, throttling, caching, mocking.
- **API Gateway auth**: IAM, Cognito, Lambda authorizers (custom JWT/token validation).
- **Step Functions**: Serverless workflow orchestration — state machines for multi-step, long-running, retryable processes.
- **EventBridge**: Serverless event bus — route events between AWS services and custom apps (scheduled rules too).
- **SQS (Simple Queue Service)**: Managed message queue — decoupling; standard (at-least-once) vs FIFO (exactly-once).
- **SQS visibility timeout**: Message hidden from consumers while processing; DLQ for failed messages.
- **SNS (Simple Notification Service)**: Pub/sub messaging — push to subscribers (Lambda, HTTP, SQS, Email, SMS).
- **SNS vs SQS**: SNS = push fan-out to many; SQS = pull queue for one consumer group.
- **DynamoDB Streams**: Ordered change feed (insert/update/delete) → Lambda for real-time processing.
- **Kinesis**: Real-time data streaming — Data Streams (producer/consumer), Firehose (deliver to S3/Redshift), Analytics.

## Containers & Kubernetes
- **ECS (Elastic Container Service)**: AWS managed container orchestration — simpler than EKS, integrates with Fargate.
- **ECS Launch types**: EC2 (you manage nodes) vs Fargate (serverless containers — no node management).
- **ECS patterns**: Task definitions (CPU/mem/image), services (long-running with LB), scheduled/reproducible tasks.
- **EKS (Elastic Kubernetes Service)**: Managed Kubernetes control plane — run K8s without managing masters.
- **EKS components**: Managed control plane, worker node groups (managed or self-managed), Fargate profiles for serverless pods.
- **Amazon ECR**: Container registry — store/pull Docker images securely (with lifecycle policies for cleanup).
- **EKS vs ECS**: EKS = standard K8s (portable, ecosystem); ECS = AWS-native simpler for AWS-centric workloads.
- **App Runner / Lightsail for Containers**: Simpler paths for containerized web apps with less control.

## Security & Identity
- **IAM** (covered above): Users, groups, roles, policies, MFA, access keys, SSO federation.
- **AWS Organizations**: Manage multiple accounts — SCPs (service control policies) apply guardrails across accounts.
- **AWS SSO / IAM Identity Center**: Centralized access for users across accounts and apps (SAML/SWF).
- **KMS (Key Management Service)**: Managed keys for encryption (CMK) — key rotation, policies, and envelope encryption.
- **Secrets Manager**: Store/rotate secrets (DB credentials, API keys) — integrates with RDS, Lambda, ECS.
- **Secrets Manager vs SSM Parameter Store**: Secrets Manager = auto-rotation + integration; Parameter Store = cheaper plain/key-value config.
- **ACM (Certificate Manager)**: Free SSL/TLS certificates for your domains (integrated with ALB, CloudFront, API Gateway).
- **WAF (Web Application Firewall)**: Layer 7 filtering — SQLi/XSS rules, rate limiting, IP/geo blocks, managed rules.
- **Shield**: DDoS protection — Standard (free) vs Advanced (24/7, cost protection) on CloudFront/ALB/ELB.
- **GuardDuty**: Threat detection (anomalous API calls, crypto mining, unusual login) — continuous, ML-based.
- **Security Hub**: Centralized security findings + posture (compliance checks across services).
- **CloudTrail** (covered): API audit log — mandatory for incident response/forensics.
- **AWS Config**: Continuous resource config assessment/compliance (e.g., SG open to world, EBS unencrypted).
- **SSM (Systems Manager)**: Operations — Run Command, Session Manager (shell without SSH), Parameter Store, Patch Manager.
- **Session Manager**: Secure shell access to EC2 via IAM (no open SSH port, full audit logging).

## Monitoring, Observability & Cost
- **CloudWatch Metrics**: Default metrics (CPU, NetworkIn/Out) — custom metrics cost money; enable detailed monitoring.
- **CloudWatch Alarms**: Trigger on metric thresholds (e.g., CPU > 70% for 5 min) → SNS → actions (ASG scale, notify).
- **CloudWatch Logs**: Central log storage — log groups/streams, filters, metric filters, subscription to Lambda/Kinesis.
- **CloudWatch Logs Insights**: SQL-like query language for interactive log analysis.
- **X-Ray**: Distributed tracing across services (Lambda, API GW, ECS) — trace requests, find bottlenecks/errors.
- **SNS + CloudWatch**: Standard alarm/notification pipeline — metric change → alarm → SNS → email/Slack/Lambda.
- **Cost Management**: Cost Explorer (analysis), Budgets (alerts), Consolidated billing, tags for cost allocation.
- **Cost optimization**: Right-size instances, use Spot/Reserved/Savings Plans, lifecycle S3, serverless where possible, shut down non-prod.
- **Trusted Advisor**: Automated checks (cost, security, performance, fault tolerance) — Core free vs full in Business+.
- **AWS Pricing**: On-demand is baseline; Savings Plans (compute) and reserved offer 40-60% discounts.

## Architectural Patterns
- **High availability**: Deploy across ≥2 AZs; ELB + ASG for stateless web; Multi-AZ RDS/Aurora for stateful.
- **Disaster recovery (DR) strategies**: Backup & restore (RPO hours), Pilot light (RPO minutes), Warm standby, Multi-site active-active.
- **Data backup strategy**: EBS snapshots / RDS backups scheduled + off-region replication + tested restores.
- **Stateless app + external state**: Keep app stateless; store sessions/data in ElastiCache/S3/DynamoDB — scale horizontally freely.
- **Event-driven architecture**: S3 events + SQS/SNS + Lambda + DynamoDB — decoupled, scalable, pay-per-use.
- **Serverless web app**: CloudFront → S3 (SPA) + API Gateway → Lambda → DynamoDB/RDS + Cognito auth.
- **Three-tier architecture**: Web tier (ALB/EC2) → App tier (ASG) → DB tier (RDS) — classic, scalable, maintainable.
- **Microservices on AWS**: ECS/EKS + API GW + service discovery (Cloud Map) + observability (X-Ray/Metrics).
- **Caching patterns**: ElastiCache for hot DB reads, CloudFront for static assets, DynamoDB DAX for item reads.
- **Blue/green & canary**: Route 53/ALB weight shifting or AppConfig for gradual rollouts with easy rollback.
- **Well-Architected review**: Regularly review against the 6 pillars — catch security & cost drift early.

## Common Pitfalls & Cost Traps
- **Forgetting to stop instances**: Non-prod instances left running at On-Demand cost — use scheduling (Instance Scheduler).
- **Public SG (0.0.0.0/0) on 22/3306**: Exposed services get hacked/mined fast — restrict SG source IPs.
- **Hardcoded keys in code/repos**: Audit with tools (git-secrets, detectors); use IAM roles + Secrets Manager.
- **No CloudTrail/Config**: No audit trail for security incidents — enable across all accounts now.
- **EIPs and NAT gateways left running**: Each EIP+NAT costs money even when unused — release/remove.
- **No lifecycle rules on S3**: Storage costs balloon with old/1-AZ data — set lifecycle transitions.
- **Single-AZ deployment**: No HA — DB and app in same AZ = single point of failure — spread across AZs.
- **No backup tests**: "We have snapshots" is not enough — test restore procedures regularly.
- **Oversized instances**: Check CPU utilization trends — modernize to right-sized/correct families (c vs m vs r).
- **Ignoring budgets/alerts**: Set cost budgets + alarms so unexpected spend is caught immediately.