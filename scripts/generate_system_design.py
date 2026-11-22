#!/usr/bin/env python3
"""Generate perfected System Design diagrams with zero defects."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_system_architecture():
    d = DiagramBuilder()
    d.add_header(
        "End-to-End Scalable System Architecture",
        "High-Availability Layered Multi-Tier Production Topology",
        x=40, y=25, w=1140, h=65
    )

    # 1. Clients Tier (w=150, x=40..190)
    d.add_container(40, 110, 160, 330, label="Client Tier", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_align="left")
    d.add_box(55, 155, 130, 48, "Web Browser", "React / Vue SPA", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(55, 220, 130, 48, "Mobile App", "iOS / Android Native", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(55, 285, 130, 48, "External Clients", "3rd-Party Webhooks", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")

    # Arrow: Clients -> Edge (gap = 80px)
    d.add_arrow(200, 242, 280, 242, stroke="#1971c2")
    d.add_text(215, 222, "HTTPS", stroke="#1971c2", font_size=11, align="left", w=60)

    # 2. Edge Layer (w=165, x=280..445)
    d.add_container(280, 110, 165, 330, label="Edge & Routing", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_align="left")
    d.add_box(295, 165, 135, 55, "Route 53 / DNS", "Anycast Geo-DNS", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(295, 245, 135, 55, "CDN Edge Cache", "CloudFront / Cloudflare", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e")

    # Arrow: Edge -> Gateway (gap = 75px)
    d.add_arrow(445, 242, 520, 242, stroke="#2b8a3e")
    d.add_text(465, 222, "TLS", stroke="#2b8a3e", font_size=11, align="left", w=50)

    # 3. API Gateway / Load Balancer (w=150, x=520..670)
    d.add_box(520, 205, 150, 75, "API Gateway", ["L7 Reverse Proxy", "Auth & Rate Limit"], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")

    # Arrow: Gateway -> App Cluster (gap = 85px)
    d.add_arrow(670, 242, 755, 242, stroke="#f59f00")
    d.add_text(685, 222, "LB Route", stroke="#f59f00", font_size=11, align="left", w=65)

    # 4. Stateless App Cluster (w=170, x=755..925)
    d.add_container(755, 110, 170, 330, label="App Cluster", stroke="#f59f00", badge_bg="#fff3bf", badge_stroke="#f59f00", label_color="#d9480f", badge_align="left")
    d.add_box(770, 155, 140, 48, "App Service 1", "Stateless Worker", bg="#ffffff", stroke="#f59f00", text_color="#d9480f")
    d.add_box(770, 220, 140, 48, "App Service 2", "Autoscaling Group", bg="#ffffff", stroke="#f59f00", text_color="#d9480f")
    d.add_box(770, 285, 140, 48, "App Service 3", "Container / Pod", bg="#ffffff", stroke="#f59f00", text_color="#d9480f")

    # Arrows: App Cluster -> Storage Tier (gap = 65px)
    d.add_arrow(925, 170, 990, 170, stroke="#e03131")
    d.add_text(935, 152, "Cache", stroke="#e03131", font_size=11, align="left", w=50)

    d.add_arrow(925, 225, 990, 225, stroke="#9c36b5")
    d.add_text(935, 207, "Write", stroke="#9c36b5", font_size=11, align="left", w=50)

    d.add_arrow(925, 280, 990, 280, stroke="#9c36b5")
    d.add_text(935, 262, "Read", stroke="#9c36b5", font_size=11, align="left", w=50)

    # 5. Data & Storage Tier (w=190, x=990..1180)
    d.add_container(990, 110, 190, 330, label="Data & Storage", stroke="#c92a2a", badge_bg="#ffe3e3", badge_stroke="#c92a2a", label_color="#c92a2a", badge_align="left")
    d.add_box(1005, 148, 160, 45, "Redis Cluster", "Cache & Session", bg="#ffffff", stroke="#e03131", text_color="#c92a2a")
    d.add_box(1005, 203, 160, 45, "Primary DB", "ACID Master (Writes)", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5")
    d.add_box(1005, 258, 160, 45, "Read Replicas", "Scale-Out Reads", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5")
    d.add_box(1005, 313, 160, 45, "Object Store (S3)", "Blobs & Backups", bg="#ffffff", stroke="#1098ad", text_color="#0c8599")

    # DB Replication Arrow
    d.add_arrow(1085, 248, 1085, 258, stroke="#9c36b5", stroke_style="dashed")

    # 6. Bottom Async Streaming & Worker Tier (Full width x=40..1180)
    d.add_container(40, 480, 1140, 140, label="Asynchronous Event Streaming & Worker Pipeline", stroke="#0ca678", badge_bg="#e6fcf5", badge_stroke="#0ca678", label_color="#0ca678", badge_align="left")

    # Bottom layout:
    # Right: Kafka directly under App Cluster (x=750..930)
    d.add_box(750, 520, 185, 65, "Kafka Message Bus", ["Durable Event Partitions", "Commit Log on Disk"], bg="#ffffff", stroke="#0ca678", text_color="#0ca678")

    # Center: Async Workers (x=430..630)
    d.add_box(430, 520, 200, 65, "Async Worker Pool", ["Celery / K8s Job Runners", "Idempotent Retry & DLQ"], bg="#ffffff", stroke="#0ca678", text_color="#0ca678")

    # Left: Search & Storage (x=100..310)
    d.add_box(100, 520, 210, 65, "Elasticsearch & S3", ["Full-Text Lucene Indexes", "Analytical Parquet Lake"], bg="#ffffff", stroke="#0ca678", text_color="#0ca678")

    # Vertical drop from App Cluster down to Kafka: straight clean line!
    d.add_arrow(842, 440, 842, 520, stroke="#0ca678")
    d.add_text(852, 452, "Publish Events", stroke="#0ca678", font_size=11, align="left", w=110)

    # Kafka -> Async Worker Pool (gap from 750 to 630 = 120px!)
    d.add_arrow(750, 552, 630, 552, stroke="#0ca678")
    d.add_text(638, 530, "Consume Events", stroke="#0ca678", font_size=11, align="left", w=110)

    # Async Worker Pool -> Elasticsearch (gap from 430 to 310 = 120px!)
    d.add_arrow(430, 552, 310, 552, stroke="#0ca678")
    d.add_text(320, 530, "Sync & Index", stroke="#0ca678", font_size=11, align="left", w=105)

    # Bottom takeaway bar
    d.add_box(40, 638, 1140, 45, "Architectural Invariant: Decouple Synchronous Request Paths from Asynchronous Event Pipelines", [
        "Synchronous user transactions execute within 50ms via Memory Cache & DB; long-running computations are offloaded to Kafka."
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#495057", font_size=12)

    d.render("system-design-architecture.png")


def generate_consistent_hashing():
    d = DiagramBuilder()
    d.add_header(
        "Consistent Hashing Ring Topology with Virtual Nodes",
        "O(1) Distributed Partitioning, Minimal Key Remapping, and Non-Disruptive Node Scaling",
        x=40, y=25, w=1140, h=65
    )

    # Master Ring Container (badge on right leaves top-left completely open)
    d.add_container(40, 110, 1140, 480, label="Consistent Hash Ring: Modulo Range [0, 2^32 - 1]", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_align="right")

    # 6 Nodes on circular ring perimeter:
    # Top Center: Node A1
    d.add_box(485, 175, 170, 55, "Node A1", "Server A (Primary)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")

    # Top Right: Node B1
    d.add_box(790, 250, 165, 55, "Node B1", "Server B (Primary)", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Bottom Right: Node C1
    d.add_box(790, 410, 165, 55, "Node C1", "Server C (Primary)", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")

    # Bottom Center: Node A2 (Virtual Node)
    d.add_box(485, 490, 170, 55, "Node A2", "Virtual Node (Server A)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")

    # Bottom Left: Node B2 (Virtual Node)
    d.add_box(185, 410, 165, 55, "Node B2", "Virtual Node (Server B)", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Top Left: Node C2 (Virtual Node)
    d.add_box(185, 250, 165, 55, "Node C2", "Virtual Node (Server C)", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")

    # Clockwise Perimeter Arrows connecting the 6 nodes cleanly:
    # 1. C2 -> A1
    d.add_arrow(350, 260, 485, 205, stroke="#1971c2")
    d.add_text(360, 215, "Clockwise Range", stroke="#1971c2", font_size=11, align="left", w=110)

    # 2. A1 -> B1
    d.add_arrow(655, 205, 790, 260, stroke="#2b8a3e")
    d.add_text(700, 215, "Clockwise Range", stroke="#2b8a3e", font_size=11, align="left", w=110)

    # 3. B1 -> C1 (Straight vertical)
    d.add_arrow(872, 305, 872, 410, stroke="#f59f00")
    d.add_text(882, 350, "Clockwise Range", stroke="#f59f00", font_size=11, align="left", w=110)

    # 4. C1 -> A2
    d.add_arrow(790, 435, 655, 490, stroke="#1971c2")
    d.add_text(700, 455, "Clockwise Range", stroke="#1971c2", font_size=11, align="left", w=110)

    # 5. A2 -> B2
    d.add_arrow(485, 490, 350, 435, stroke="#2b8a3e")
    d.add_text(360, 455, "Clockwise Range", stroke="#2b8a3e", font_size=11, align="left", w=110)

    # 6. B2 -> C2 (Straight vertical)
    d.add_arrow(267, 410, 267, 305, stroke="#f59f00")
    d.add_text(157, 350, "Clockwise Range", stroke="#f59f00", font_size=11, align="left", w=110)

    # Distributed Keys with clean routing arrows into nearest clockwise node:
    # Key 1: top-left (open area, gap = 60px)
    d.add_box(280, 145, 140, 48, "Key: user_88", "hash: 140 -> Node A1", bg="#f8f9fa", stroke="#495057", text_color="#212529")
    d.add_arrow(420, 169, 485, 195, stroke="#1971c2")

    # Key 2: top right (gap to Node B1 = 35px)
    d.add_box(990, 200, 140, 48, "Key: item_44", "hash: 720 -> Node B1", bg="#f8f9fa", stroke="#495057", text_color="#212529")
    d.add_arrow(990, 235, 955, 265, stroke="#2b8a3e")

    # Key 3: bottom right (gap to Node C1 = 35px)
    d.add_box(990, 440, 140, 48, "Key: order_99", "hash: 1350 -> Node C1", bg="#f8f9fa", stroke="#495057", text_color="#212529")
    d.add_arrow(990, 450, 955, 430, stroke="#f59f00")

    # Key 4: bottom left (Node B2 starts at 185, Key ends at 165 -> 20px clear gap!)
    d.add_box(45, 440, 120, 48, "Key: cart_12", "hash: 2890 -> B2", bg="#f8f9fa", stroke="#495057", text_color="#212529")
    d.add_arrow(165, 455, 185, 440, stroke="#2b8a3e")

    # Center Hash Space Label
    d.add_box(465, 320, 210, 60, "Virtual Node Mesh", ["Uniform Key Distribution", "Zero Hotspots across Nodes"], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=12)

    # Bottom Properties Container
    d.add_container(40, 605, 1140, 110, label="Core Distributed Invariants of Consistent Hashing", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_align="left")
    d.add_box(55, 642, 1110, 55, "Minimal Key Remapping & Uniform Load Balancing", [
        "• Rebalancing Cost: When a node joins or leaves, only K/N keys are redistributed (traditional hash % N invalidates 100% of cache keys).",
        "• Virtual Nodes (A1, A2... An): Guarantees uniform key dispersal across heterogeneous servers, preventing hot spots."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#2b8a3e", font_size=12)

    d.render("system-design-consistent-hashing.png")

if __name__ == "__main__":
    generate_system_architecture()
    generate_consistent_hashing()
