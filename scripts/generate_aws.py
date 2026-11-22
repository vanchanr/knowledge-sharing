#!/usr/bin/env python3
"""Generate perfected AWS Multi-AZ VPC Architecture diagram."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_aws():
    d = DiagramBuilder()
    d.add_header(
        "AWS Multi-AZ High-Availability VPC Production Architecture",
        "Multi-Tier Network Isolation: Internet Gateway, Public Subnets (ALB/NAT), Private App Subnets & Multi-AZ RDS",
        x=40, y=20, w=1220, h=65
    )

    # External Client Layer (y=95..140)
    d.add_box(460, 95, 340, 42, "Internet Clients (HTTPS :443)", "External requests routed via Amazon Route 53 DNS", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(630, 137, 630, 175, label="HTTPS :443", stroke="#1971c2", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Master VPC Container (x=40..1260, w=1220, h=555)
    d.add_container(40, 175, 1220, 535, label="AWS Region: us-east-1 | Virtual Private Cloud (VPC CIDR: 10.0.0.0/16)", stroke="#e67700", badge_bg="#fff9db", badge_stroke="#e67700", label_color="#d9480f", badge_w=580)

    # Internet Gateway inside VPC top (x=460..800, w=340, h=42)
    d.add_box(460, 205, 340, 42, "Internet Gateway (IGW: Attached to VPC)", "VPC edge router for 0.0.0.0/0 internet traffic", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Availability Zone A (Left: x=60..600, w=540)
    d.add_container(60, 260, 540, 435, label="AZ-A (us-east-1a)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=170)

    # AZ-A: Tier 1 - Public Subnet A (x=80..580, w=500)
    d.add_box(80, 310, 220, 65, "NAT Gateway A (Elastic IP)", "Public Subnet (10.0.1.0/24)\nOutbound IPv4 NAT for AZ-A", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_box(320, 310, 260, 65, "ALB Ingress Node A (Public IP)", "Public Subnet (10.0.1.0/24)\nSSL termination & load balancing", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # AZ-A: Tier 2 - Private App Subnet A
    d.add_box(80, 415, 500, 65, "Application Workloads (EKS Pods / EC2 Auto-Scaling Group)", "Private App Subnet (10.0.10.0/24) | No Public IPs\nInbound from ALB SG (:8080) | Outbound updates via NAT-GW-A", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # AZ-A: Tier 3 - Isolated DB Subnet A
    d.add_box(80, 520, 500, 65, "Amazon RDS PostgreSQL (Primary Writer)", "Isolated DB Subnet (10.0.20.0/24) | No Internet Route\nActive primary instance | Port 5432 from App Security Group only", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    # AZ-A Invariant Box
    d.add_box(80, 615, 500, 65, "AZ-A Route & Security Controls", [
        "• Defense in Depth: Security Groups (stateful) + Network ACLs (stateless).",
        "• Blast Radius: AZ-A hardware degradation leaves AZ-B fully operational."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Availability Zone B (Right: x=700..1240, w=540)
    # Gap between AZ-A and AZ-B = 100px (600 to 700)
    d.add_container(700, 260, 540, 435, label="AZ-B (us-east-1b)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=170, badge_align="right")

    # AZ-B: Tier 1 - Public Subnet B (x=720..1220, w=500)
    d.add_box(720, 310, 260, 65, "ALB Ingress Node B (Public IP)", "Public Subnet (10.0.2.0/24)\nSSL termination & load balancing", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(1000, 310, 220, 65, "NAT Gateway B (Elastic IP)", "Public Subnet (10.0.2.0/24)\nOutbound IPv4 NAT for AZ-B", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # AZ-B: Tier 2 - Private App Subnet B
    d.add_box(720, 415, 500, 65, "Application Workloads (EKS Pods / EC2 Auto-Scaling Group)", "Private App Subnet (10.0.11.0/24) | No Public IPs\nInbound from ALB SG (:8080) | Outbound updates via NAT-GW-B", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # AZ-B: Tier 3 - Isolated DB Subnet B
    d.add_box(720, 520, 500, 65, "Amazon RDS PostgreSQL (Standby Replica)", "Isolated DB Subnet (10.0.21.0/24) | No Internet Route\nSynchronous hot-standby copy | Automatic DNS failover in < 60s", bg="#e5dbff", stroke="#7950f2", text_color="#7950f2", font_size=11)

    # AZ-B Invariant Box
    d.add_box(720, 615, 500, 65, "AZ-B Route & Security Controls", [
        "• Multi-AZ NAT: Independent NAT Gateway per AZ prevents single points of failure.",
        "• Complete DB Isolation: DB subnets have NO route to Internet or NAT."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Connecting Arrows:
    # 1. IGW -> ALB Nodes (entering AZ-A at x=450 and AZ-B at x=850, completely outside AZ badges which end at x=230 and x=870)
    d.add_arrow(490, 247, 450, 310, label="Inbound SSL", stroke="#1971c2", label_offset_y=-14, label_bg="#ffffff", font_size=11)
    d.add_arrow(770, 247, 850, 310, label="Inbound SSL", stroke="#1971c2", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # 2. ALB Nodes -> App Workloads (straight down)
    d.add_arrow(450, 375, 450, 415, label="Target Group :8080", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)
    d.add_arrow(850, 375, 850, 415, label="Target Group :8080", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # 3. App Workloads -> RDS Primary (straight down in AZ-A)
    d.add_arrow(330, 480, 330, 520, label="Read/Write SQL :5432", stroke="#9c36b5", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # 4. Outbound Egress: App Workloads -> NAT Gateway (straight up)
    d.add_arrow(190, 415, 190, 375, label="Outbound Egress", stroke="#f59f00", label_offset_y=-10, label_bg="#ffffff", font_size=11)
    d.add_arrow(1110, 415, 1110, 375, label="Outbound Egress", stroke="#f59f00", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # 5. RDS Synchronous Replication (straight horizontal between AZ-A and AZ-B, gap = 140px: 580 to 720)
    d.add_arrow(580, 552, 720, 552, label="Sync EBS Mirror", stroke="#9c36b5", label_offset_y=-14, label_bg="#ffffff", font_size=11)

    # Master Invariant Banner
    d.add_box(40, 725, 1220, 50, "Security Invariant: Zero public IPs on database or app tiers; NAT Gateways isolate outbound egress; Security Groups enforce least-privilege.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("aws-ha-vpc-architecture.png")

if __name__ == "__main__":
    generate_aws()
