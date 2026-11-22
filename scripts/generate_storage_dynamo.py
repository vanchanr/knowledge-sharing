#!/usr/bin/env python3
"""Generate perfected Storage & DynamoDB diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_storage_hierarchy():
    d = DiagramBuilder()
    d.add_header(
        "Computer Storage Hierarchy: Latency, Cost & Capacity Trade-offs",
        "From CPU Registers to Cold Cloud Archives — Volatile Cache vs Non-Volatile Persistence",
        x=40, y=25, w=1140, h=65
    )

    # Pyramid steps (centered around x=580)
    d.add_box(430, 105, 300, 52, "CPU Registers (< 1 ns, Bytes)", "Flip-flops inside CPU core | Zero bus delay", bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a", font_size=12)
    d.add_box(370, 167, 420, 52, "L1 / L2 / L3 CPU Cache (1 - 10 ns, MBs)", "SRAM cache lines on CPU die | Hardware prefetching", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_box(310, 229, 540, 52, "Main Memory DRAM (50 - 100 ns, 16 - 512 GB)", "Byte-addressable system RAM | Volatile execution space", bg="#fff9db", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_box(240, 291, 680, 52, "NVMe / PCIe SSD (10 - 50 µs, Terabytes)", "NAND Flash memory | High IOPS, non-volatile storage", bg="#d3f9d8", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(170, 353, 820, 52, "Mechanical HDD / SATA (1 - 10 ms, Terabytes)", "Rotating magnetic platters | High sequential, slow random I/O", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(100, 415, 960, 52, "Cloud Object Storage & Tape (100 ms - hours, Petabytes+)", "AWS S3 / Glacier / LTO Tape | Immutable, 11 9s durability", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)

    # Left Side: Speed & Cost Arrow (Red, pointing UP)
    d.add_arrow(50, 467, 50, 105, stroke="#e03131", stroke_width=2.5)
    d.add_text(60, 270, "Higher Speed\n& Cost / GB", font_size=12, stroke="#e03131", align="left", w=90)

    # Right Side: Capacity & Durability Arrow (Purple, pointing DOWN)
    d.add_arrow(1110, 105, 1110, 467, stroke="#9c36b5", stroke_width=2.5)
    d.add_text(1010, 270, "Higher Capacity\n& Durability", font_size=12, stroke="#9c36b5", align="right", w=95)

    # Bottom Architectural Invariants Note
    d.add_box(100, 485, 960, 85, "Storage Hierarchy Architectural Invariants", [
        "• Latency Disparity: Accessing RAM (100 ns) is 100,000x faster than reading an HDD (10 ms) and 1,000x faster than NVMe SSD.",
        "• Volatility Line: Registers, Caches, and DRAM are volatile (data lost on power off); SSD, HDD, and Tape are non-volatile persistent.",
        "• Locality Principle: Temporal (reuse recent data) and Spatial (use adjacent data) caching make this pyramid efficient."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("storage-hierarchy-pyramid.png")

def generate_dynamodb_partitioning():
    d = DiagramBuilder()
    d.add_header(
        "Amazon DynamoDB: Partition Key Hashing & Global Secondary Index (GSI)",
        "Consistent Hash Partition Routing, Local Sort Key B-Tree, and Async GSI Projection",
        x=40, y=25, w=1160, h=65
    )

    # 1. Base Table Container (Left: 40..550, w=510)
    d.add_container(40, 110, 510, 430, label="Base Table: Request Routing & Storage Partitions", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # Item Write Request
    d.add_box(60, 155, 470, 50, "Item Write: { PK: 'USER#123', SK: 'ORDER#991', Total: $99 }", "Base Table Primary Key = Partition Key (PK) + Sort Key (SK)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # Router Arrow
    d.add_arrow(295, 205, 295, 240, label="MD5 Hash(PK)", stroke="#1971c2", label_offset_y=-18, font_size=11)

    # Storage Partitions (3 physical SSD nodes)
    d.add_box(60, 240, 145, 100, "Partition 1", [
        "Hash: 00 - 55",
        "SSD Storage Node",
        "Local B-Tree"
    ], bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=11)

    d.add_box(215, 240, 160, 100, "Partition 2", [
        "Hash: 56 - AA",
        "Target Match!",
        "Order #991 written"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(385, 240, 145, 100, "Partition 3", [
        "Hash: AB - FF",
        "SSD Storage Node",
        "Local B-Tree"
    ], bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=11)

    # Bottom Card inside Base Table
    d.add_box(60, 355, 470, 165, "Primary Key Mechanics (PK + SK)", [
        "• Partition Key (PK): Passed through MD5 hash to find physical partition node.",
        "• Sort Key (SK): Organizes items into contiguous local B-Tree pages on SSD.",
        "• Query Pattern: PK requires exact equality match.",
        "  SK supports range queries (begins_with, between, >, <)."
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#1971c2", font_size=11)

    # Connecting Arrow: Base Table -> GSI (gap = 550..660 = 110px!)
    d.add_arrow(550, 180, 660, 180, label="Streams CDC", stroke="#2b8a3e", label_offset_y=-18, font_size=11)

    # 2. GSI Container (Right: 660..1180, w=520)
    d.add_container(660, 110, 520, 430, label="Global Secondary Index (GSI): Asynchronous Inverted Table", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    # Streams Box
    d.add_box(680, 155, 480, 50, "DynamoDB Streams (Change Data Capture)", "Asynchronous replication log captures item mutations without blocking base write", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)

    # Arrow down
    d.add_arrow(920, 205, 920, 240, label="Projects Attributes", stroke="#2b8a3e", label_offset_y=-18, font_size=11)

    # GSI Inverted Table
    d.add_box(680, 240, 480, 100, "GSI Inverted Index Table: { PK: 'Status#PAID', SK: '2026-01-15' }", [
        "• Inverted Partition Key: Queries all orders by Status (avoids full table scan)",
        "• Inverted Sort Key: CreatedAt timestamp enables chronological range queries",
        "• Projected Attributes: Total, OrderId (INCLUDE or ALL projections)"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Bottom Card inside GSI
    d.add_box(680, 355, 480, 165, "GSI Architectural Trade-offs", [
        "• Eventual Consistency: GSI updates are asynchronous (typically < 10ms).",
        "• Dedicated Capacity: GSIs maintain their own provisioned RCU / WCU.",
        "  Throttling the GSI will throttle base table writes!",
        "• Single-Table Design: Enables querying across heterogeneous entity types."
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#2b8a3e", font_size=11)

    # Bottom Master Note
    d.add_box(40, 555, 1140, 75, "DynamoDB Single-Table Design Paradigm", [
        "• Overloading generic PK and SK attributes models complex relational graphs in a single DynamoDB table.",
        "• Combines predictable O(1) single-digit millisecond latency with infinite horizontal partition scaling."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("dynamodb-partitioning-gsi.png")

if __name__ == "__main__":
    generate_storage_hierarchy()
    generate_dynamodb_partitioning()
