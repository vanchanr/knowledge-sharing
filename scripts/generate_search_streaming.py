#!/usr/bin/env python3
"""Generate perfected Elasticsearch & Kafka diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_elasticsearch():
    d = DiagramBuilder()
    d.add_header(
        "Elasticsearch: Cluster Sharding & Lucene Inverted Index",
        "Master & Data Node Topologies, Primary/Replica Shards, and Term Dictionary (FST) Postings",
        x=40, y=25, w=1160, h=65
    )

    # 1. Cluster Container (Left: 40..530, w=490)
    d.add_container(40, 110, 490, 440, label="Elasticsearch Cluster Architecture", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # Master Nodes
    d.add_box(60, 155, 450, 50, "Dedicated Master Nodes (Quorum Election)", "Manages cluster state, shard routing, and index mappings", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # Data Node 1
    d.add_container(60, 220, 450, 105, label="Data Node 1 (Hot Tier SSD)", stroke="#2b8a3e", stroke_style="dotted", badge_bg="#ffffff", badge_stroke="#2b8a3e", label_color="#2b8a3e")
    d.add_box(75, 255, 205, 55, "Primary Shard 0 (P0)", "Index writes & query exec", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(290, 255, 205, 55, "Replica Shard 1 (R1)", "Backup & read scaling", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Data Node 2
    d.add_container(60, 340, 450, 105, label="Data Node 2 (Hot Tier SSD)", stroke="#2b8a3e", stroke_style="dotted", badge_bg="#ffffff", badge_stroke="#2b8a3e", label_color="#2b8a3e")
    d.add_box(75, 375, 205, 55, "Primary Shard 1 (P1)", "Index writes & query exec", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(290, 375, 205, 55, "Replica Shard 0 (R0)", "Backup & read scaling", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Left note
    d.add_box(60, 460, 450, 75, "Shard Resilience Rule", [
        "• A replica is NEVER placed on the same physical node as its primary.",
        "• Survives catastrophic loss of an entire data node without data loss."
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 2. Inverted Index Container (Right: 550..1190, w=640)
    d.add_container(550, 110, 640, 440, label="Lucene Inverted Index Structure (Inside Every Shard)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")

    # Raw Docs
    d.add_box(570, 155, 600, 45, "Raw Documents", "Doc 1: 'distributed systems' | Doc 2: 'systems architecture'", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=12)

    # Down arrow
    d.add_arrow(870, 200, 870, 240, label="Analyzer (Tokenizer + Lowercase)", stroke="#495057", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # Column Headers
    d.add_box(570, 245, 285, 36, "Term Dictionary (In-Memory FST)", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(885, 245, 285, 36, "Postings List (Doc IDs on Disk)", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # Rows
    d.add_box(570, 288, 285, 34, "architecture", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(885, 288, 285, 34, "[ Doc 2 ]", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_arrow(855, 305, 885, 305, stroke="#9c36b5")

    d.add_box(570, 328, 285, 34, "distributed", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(885, 328, 285, 34, "[ Doc 1 ]", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_arrow(855, 345, 885, 345, stroke="#9c36b5")

    d.add_box(570, 368, 285, 34, "systems", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(885, 368, 285, 34, "[ Doc 1, Doc 2 ]", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_arrow(855, 385, 885, 385, stroke="#9c36b5")

    # Right note
    d.add_box(570, 415, 600, 120, "Why Full-Text Search Is Instantaneous", [
        "• FST (Finite State Transducer): Memory-mapped dictionary locates terms in microseconds.",
        "• Roaring Bitmaps: Multi-term Boolean queries evaluate via ultra-fast CPU bitwise ops.",
        "• Eliminates slow table scans by indexing terms to document IDs directly."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Bottom Master Note
    d.add_box(40, 565, 1140, 65, "Elasticsearch Core Philosophy: Cluster-level sharding scales writes; shard-level Lucene indexes power O(1) searches.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("elasticsearch-cluster-inverted-index.png")

def generate_kafka():
    d = DiagramBuilder()
    d.add_header(
        "Apache Kafka: Partitioned Topics & Consumer Group Balancing",
        "Sequential Log Append, Consumer Group Rebalancing, and Guaranteed Per-Partition Ordering",
        x=40, y=25, w=1160, h=65
    )

    # 1. Producers (40..190, w=150)
    d.add_box(40, 195, 150, 180, "Producers", [
        "Order Service",
        "",
        "• Murmur2(key) hash",
        "• Round-robin if null",
        "• Idempotent (acks=all)",
        "• Zero batch loss"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # Arrow: Producer -> Topic (gap = 80px)
    d.add_arrow(190, 270, 270, 270, label="Produce", stroke="#1971c2", label_offset_y=-18, font_size=11)

    # 2. Topic Container (270..750, w=480)
    d.add_container(270, 110, 480, 380, label="Topic: 'order-events' (3 Partitions, Commit Log)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    d.add_box(290, 160, 440, 65, "Partition 0 [Offsets: 0, 1, 2, 3 ... 1240]", "Sequential append-only commit log on disk | PageCache backed", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(290, 240, 440, 65, "Partition 1 [Offsets: 0, 1, 2, 3 ... 982]", "Sequential append-only commit log on disk | PageCache backed", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(290, 320, 440, 65, "Partition 2 [Offsets: 0, 1, 2, 3 ... 1510]", "Sequential append-only commit log on disk | PageCache backed", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(290, 400, 440, 75, "Ordering Guarantee Invariant", [
        "• Strict ordering is guaranteed ONLY within a single partition.",
        "• Records with the same partition key always land on the same partition."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 3. Consumer Group Container (830..1160, w=330, gap = 80px)
    d.add_container(830, 110, 330, 380, label="Consumer Group: 'fulfillment-svc'", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    d.add_box(850, 160, 290, 65, "Consumer Instance 1", "Assigned: Partition 0", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(850, 240, 290, 65, "Consumer Instance 2", "Assigned: Partition 1", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(850, 320, 290, 65, "Consumer Instance 3", "Assigned: Partition 2", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)

    d.add_box(850, 400, 290, 75, "Consumer Concurrency Limit", [
        "• Maximum active consumers in a group = partition count (3).",
        "• Excess consumer instances remain idle."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Arrows between Partitions and Consumers (80px gap)
    d.add_arrow(730, 192, 850, 192, label="Read P0", stroke="#2b8a3e", label_offset_y=-18, font_size=11)
    d.add_arrow(730, 272, 850, 272, label="Read P1", stroke="#2b8a3e", label_offset_y=-18, font_size=11)
    d.add_arrow(730, 352, 850, 352, label="Read P2", stroke="#2b8a3e", label_offset_y=-18, font_size=11)

    # 4. Bottom Invariants Container
    d.add_container(40, 510, 1120, 115, label="Kafka Core Distributed Architecture Invariants", stroke="#495057", badge_bg="#f1f3f5", badge_stroke="#495057", label_color="#212529")
    d.add_box(60, 550, 1080, 60, "Zero-Copy Streaming & Consumer Group Isolation", [
        "• Multiple Independent Consumer Groups: Different groups ('analytics', 'inventory') read from the same topic simultaneously at their own offset pace.",
        "• Linux Zero-Copy: Uses sendfile() system call to stream partition data directly from OS PageCache to network NIC, bypassing JVM heap."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=12)

    d.render("kafka-topic-partition-architecture.png")

if __name__ == "__main__":
    generate_elasticsearch()
    generate_kafka()
