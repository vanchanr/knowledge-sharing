#!/usr/bin/env python3
"""Generate perfected System Design diagrams."""
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
    d.add_container(40, 110, 160, 340, label="Client Tier", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")
    d.add_box(55, 155, 130, 48, "Web Browser", "React / Vue SPA", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(55, 220, 130, 48, "Mobile App", "iOS / Android Native", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(55, 285, 130, 48, "External Clients", "3rd-Party Webhooks", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")

    # Arrow: Clients -> Edge (gap = 75px)
    d.add_arrow(200, 250, 275, 250, label="HTTPS", stroke="#1971c2", label_offset_y=-20)

    # 2. Edge Layer (w=160, x=275..435)
    d.add_container(275, 110, 165, 340, label="Edge & Routing", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")
    d.add_box(290, 165, 135, 55, "Route 53 / DNS", "Anycast Geo-DNS", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(290, 245, 135, 55, "CDN Edge Cache", "CloudFront / Cloudflare", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e")

    # Arrow: Edge -> Gateway (gap = 75px)
    d.add_arrow(440, 242, 515, 242, label="TLS", stroke="#2b8a3e", label_offset_y=-20)

    # 3. API Gateway / Load Balancer (w=150, x=515..665)
    d.add_box(515, 205, 150, 75, "API Gateway", ["L7 Load Balancer", "Auth & Rate Limit"], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")

    # Arrow: Gateway -> App Cluster (gap = 75px)
    d.add_arrow(665, 242, 740, 242, label="LB Route", stroke="#f59f00", label_offset_y=-20)

    # 4. Stateless App Cluster (w=165, x=740..905)
    d.add_container(740, 110, 170, 340, label="App Cluster", stroke="#f59f00", badge_bg="#fff3bf", badge_stroke="#f59f00", label_color="#d9480f")
    d.add_box(755, 155, 140, 48, "App Service 1", "Stateless Worker", bg="#ffffff", stroke="#f59f00", text_color="#d9480f")
    d.add_box(755, 220, 140, 48, "App Service 2", "Autoscaling Group", bg="#ffffff", stroke="#f59f00", text_color="#d9480f")
    d.add_box(755, 285, 140, 48, "App Service 3", "Container / Pod", bg="#ffffff", stroke="#f59f00", text_color="#d9480f")

    # Arrows: App Cluster -> Data Layer (gap = 75px)
    d.add_arrow(910, 174, 980, 174, label="Cache", stroke="#e03131", label_offset_y=-18, font_size=11)
    d.add_arrow(910, 239, 980, 239, label="Write", stroke="#9c36b5", label_offset_y=-18, font_size=11)
    d.add_arrow(910, 304, 980, 304, label="Read", stroke="#9c36b5", label_offset_y=-18, font_size=11)

    # 5. Data & Storage Tier (w=200, x=980..1180)
    d.add_container(980, 110, 200, 340, label="Data & Storage", stroke="#c92a2a", badge_bg="#ffe3e3", badge_stroke="#c92a2a", label_color="#c92a2a")
    d.add_box(995, 150, 170, 48, "Redis Cluster", "Cache & Session", bg="#ffffff", stroke="#e03131", text_color="#c92a2a")
    d.add_box(995, 215, 170, 48, "Primary DB", "ACID Master (Writes)", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5")
    d.add_box(995, 280, 170, 48, "Read Replicas", "Scale-Out Reads", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5")
    d.add_box(995, 345, 170, 48, "Object Store (S3)", "Blobs & Backups", bg="#ffffff", stroke="#1098ad", text_color="#0c8599")

    # DB Replication Arrow
    d.add_arrow(1080, 263, 1080, 280, stroke="#9c36b5", stroke_style="dashed")

    # 6. Bottom Async Streaming Tier
    d.add_container(275, 470, 905, 140, label="Asynchronous Event Streaming & Worker Pipeline", stroke="#0ca678", badge_bg="#e6fcf5", badge_stroke="#0ca678", label_color="#0ca678")
    d.add_box(295, 515, 240, 60, "Kafka Message Bus", "Durable Event Partitions", bg="#ffffff", stroke="#0ca678", text_color="#0ca678")
    d.add_box(610, 515, 240, 60, "Async Worker Pool", "Background Jobs / Celery", bg="#ffffff", stroke="#0ca678", text_color="#0ca678")
    d.add_box(920, 515, 240, 60, "Elasticsearch & S3", "Log Aggregation & Search", bg="#ffffff", stroke="#0ca678", text_color="#0ca678")

    # App Cluster to Kafka (downward arrow)
    d.add_arrow(825, 450, 825, 470, stroke="#0ca678")

    # Pipeline arrows
    d.add_arrow(535, 545, 610, 545, label="Consume Events", stroke="#0ca678", label_offset_y=-18)
    d.add_arrow(850, 545, 920, 545, label="Sync / Index", stroke="#0ca678", label_offset_y=-18)

    d.render("system-design-architecture.png")

def generate_consistent_hashing():
    d = DiagramBuilder()
    d.add_header(
        "Consistent Hashing Ring Topology with Virtual Nodes",
        "O(1) Distributed Routing, Minimal Key Remapping, and Resilient Rebalancing",
        x=40, y=25, w=1040, h=65
    )

    # Master Ring Container encompassing everything cleanly
    d.add_container(40, 110, 1040, 400, label="Consistent Hash Ring: Modulo Range [0, 2^32 - 1]", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # Keys inside the container
    # Key 1
    d.add_box(65, 175, 160, 55, "Key 1 (hash: 104)", "user_id: 88291", bg="#f8f9fa", stroke="#495057", text_color="#212529")
    # Key 2
    d.add_box(895, 175, 160, 55, "Key 2 (hash: 850)", "item_id: 44012", bg="#f8f9fa", stroke="#495057", text_color="#212529")
    # Key 3
    d.add_box(895, 365, 160, 55, "Key 3 (hash: 1420)", "order_id: 9931", bg="#f8f9fa", stroke="#495057", text_color="#212529")

    # Nodes on the Ring
    d.add_box(300, 170, 170, 60, "Node A1", "Server A (Primary)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(650, 170, 170, 60, "Node B1", "Server B (Primary)", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(650, 360, 170, 60, "Node C1", "Server C (Primary)", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")
    d.add_box(300, 360, 170, 60, "Node A2", "Virtual Node (Server A)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")

    # Routing arrows from keys to nodes (clear spacing, label above line)
    d.add_arrow(225, 200, 300, 200, label="Routes to", stroke="#1971c2", label_offset_y=-22, font_size=11)
    d.add_arrow(895, 200, 820, 200, label="Routes to", stroke="#2b8a3e", label_offset_y=-22, font_size=11)
    d.add_arrow(895, 390, 820, 390, label="Routes to", stroke="#f59f00", label_offset_y=-22, font_size=11)

    # Clockwise Ring Connections
    d.add_arrow(470, 200, 650, 200, label="Clockwise Range", stroke="#1971c2", label_offset_y=-22)
    # Vertical arrow from B1 to C1 (pointing down)
    d.add_arrow(735, 230, 735, 360, stroke="#2b8a3e")
    d.add_text(745, 285, "Clockwise Range", font_size=11, stroke="#2b8a3e", align="left", w=120)

    # Bottom arrow from C1 to A2 (pointing left)
    d.add_arrow(650, 390, 470, 390, label="Clockwise Range", stroke="#f59f00", label_offset_y=16)

    # Vertical arrow from A2 to A1 (pointing up)
    d.add_arrow(385, 360, 385, 230, stroke="#1971c2")
    d.add_text(285, 285, "Clockwise Range", font_size=11, stroke="#1971c2", align="left", w=120)

    # Bottom Properties Container
    d.add_container(40, 530, 1040, 120, label="Core Distributed Properties of Consistent Hashing", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")
    d.add_box(60, 570, 1000, 60, "Minimal Key Remapping & Uniform Load Balancing", [
        "• Rebalancing Cost: When a node joins or leaves, only K/N keys are redistributed (traditional hash % N invalidates 100%).",
        "• Virtual Nodes (A1, A2... An): Prevents hot spots and guarantees uniform hash distribution across heterogeneous servers."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#2b8a3e", font_size=12)

    d.render("system-design-consistent-hashing.png")

if __name__ == "__main__":
    generate_system_architecture()
    generate_consistent_hashing()
