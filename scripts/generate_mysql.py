#!/usr/bin/env python3
"""Generate perfected MySQL Server & InnoDB Architecture diagram."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_mysql():
    d = DiagramBuilder()
    d.add_header(
        "MySQL Server & InnoDB Storage Engine Architecture",
        "Server Layer (Optimizer & Execution), InnoDB In-Memory Buffer Pool, and On-Disk WAL Persistence",
        x=40, y=20, w=1220, h=65
    )

    # 1. MySQL Server Layer (x=40..1240, w=1200, h=145)
    d.add_container(40, 100, 1200, 145, label="1. MySQL Server Layer (Pluggable Storage Engine Interface)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=460)

    # 4 Server Components
    d.add_box(60, 145, 265, 75, "Connection Pool & Threads", "Client auth, SSL termination, thread cache,\nmax_connections resource management", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(325, 182, 355, 182, stroke="#1971c2")

    d.add_box(355, 145, 265, 75, "SQL Parser & Preprocessor", "Lexical tokens, AST syntax parse tree,\nTable & column privilege verification", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(620, 182, 650, 182, stroke="#1971c2")

    d.add_box(650, 145, 265, 75, "Query Optimizer (CBO)", "Cost-based execution plan, index selection,\nJoin ordering & subquery flattening", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(915, 182, 945, 182, stroke="#1971c2")

    d.add_box(945, 145, 275, 75, "Execution Engine", "Iterates execution plan; calls storage engine\nvia standardized Handler API methods", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Down arrows from Server Layer to Storage Engine (clear of badges)
    d.add_arrow(782, 220, 782, 280, label="Reads & Queries", stroke="#1971c2", label_offset_y=-10, label_bg="#ffffff", font_size=11)
    d.add_arrow(1082, 220, 1082, 280, label="Handler API Calls", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # 2. InnoDB In-Memory Structures (x=40..1240, w=1200, h=215)
    d.add_container(40, 280, 1200, 215, label="2. InnoDB In-Memory Structures (Buffer Pool & Memory Management)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_w=520)

    # 4 In-Memory Components
    d.add_box(60, 325, 350, 95, "Buffer Pool (innodb_buffer_pool_size)", [
        "• Data Pages: Caches 16KB data & index pages.",
        "• LRU List: Midpoint insertion (5/8 new, 3/8 old sublists).",
        "• Flush List: Tracks dirty pages modified in memory."
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(430, 325, 250, 95, "Change Buffer", [
        "• Buffers secondary index writes.",
        "• Merges changes asynchronously",
        "  when pages are read into pool.",
        "• Avoids expensive random disk I/O."
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(700, 325, 250, 95, "Adaptive Hash Index (AHI)", [
        "• In-memory hash lookup for B-tree.",
        "• Auto-built for hot index pages.",
        "• Bypasses B-tree root-to-leaf path",
        "  yielding O(1) in-memory point reads."
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(970, 325, 250, 95, "Redo Log Buffer (WAL)", [
        "• In-memory circular buffer for WAL.",
        "• Flushed to disk on commit (fsync)",
        "  via innodb_flush_log_at_trx_commit.",
        "• Guarantees ACID Durability (D)."
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    d.add_box(60, 430, 1160, 50, "In-Memory Invariant: Updates modify pages in the Buffer Pool and append to the Redo Log Buffer in RAM. Pages become 'dirty' and are lazily flushed to disk via background checkpoint threads.", bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Down arrows from In-Memory to On-Disk
    d.add_arrow(235, 495, 235, 525, label="Page Cleaner (fsync)", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)
    d.add_arrow(1095, 495, 1095, 525, label="WAL Flush on Commit", stroke="#f59f00", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # 3. InnoDB On-Disk Storage Structures (x=40..1240, w=1200, h=155)
    d.add_container(40, 525, 1200, 155, label="3. InnoDB On-Disk Storage Structures (Persistence & Recovery)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_w=500, badge_align="center")

    # 4 Disk Components
    d.add_box(60, 570, 275, 75, "Tablespaces (*.ibd)", "B+ Tree Clustered Indexes, Secondary Indexes,\n16KB Pages, Extents (1MB = 64 Pages)", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(355, 570, 275, 75, "Doublewrite Buffer", "Sequential disk area where dirty pages\nare written before .ibd to guard against\ntorn page crashes during power failure", bg="#f1f3f5", stroke="#495057", text_color="#212529", font_size=11)

    d.add_box(650, 570, 275, 75, "Undo Tablespaces (undo_*)", "Stores historical row versions for MVCC\n(Multi-Version Concurrency Control snapshots)", bg="#e5dbff", stroke="#7950f2", text_color="#7950f2", font_size=11)

    d.add_box(945, 570, 275, 75, "Redo Logs (ib_logfile0 / 1)", "Circular disk log files for crash recovery;\nReplays unwritten committed pages on reboot", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    d.add_box(60, 652, 1160, 22, "Crash Recovery: If MySQL crashes, InnoDB replays Redo Logs up to the latest LSN checkpoint and uses Undo Logs to roll back uncommitted transactions.", bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Master Bottom Banner
    d.add_box(40, 690, 1220, 45, "InnoDB Core Invariant: Write-Ahead Logging (WAL) ensures transactions are committed to disk sequentially via Redo Logs before random data page writes happen.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("mysql-innodb-architecture.png")

if __name__ == "__main__":
    generate_mysql()
