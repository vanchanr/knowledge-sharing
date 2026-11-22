#!/usr/bin/env python3
"""Generate perfected Redis diagrams with zero defects."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_event_loop():
    d = DiagramBuilder()
    d.add_header(
        "Redis Single-Threaded Event Loop Architecture (Reactor Pattern)",
        "Non-Blocking I/O Multiplexing, Event Demultiplexer, and In-Memory Command Execution",
        x=40, y=25, w=1140, h=65
    )

    # 1. Clients Container
    d.add_container(40, 110, 190, 330, label="Concurrent Clients", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_align="left")
    d.add_box(55, 160, 160, 48, "Client 1 (Socket 1)", "TCP Connection", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(55, 225, 160, 48, "Client 2 (Socket 2)", "TCP Connection", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(55, 290, 160, 48, "Client 3 (Socket 3)", "TCP Connection", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # 2. I/O Multiplexer
    d.add_box(290, 165, 190, 175, "I/O Multiplexer", [
        "epoll (Linux) / kqueue",
        "",
        "• Monitors 10,000+ FDs",
        "• Edge-triggered readiness",
        "• Zero thread context switch"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=13)

    # Connecting Arrows: Clients -> Multiplexer
    d.add_arrow(215, 184, 290, 215, stroke="#1971c2")
    d.add_arrow(215, 249, 290, 249, stroke="#1971c2")
    d.add_arrow(215, 314, 290, 283, stroke="#1971c2")

    # Arrow: Multiplexer -> Execution Core (gap = 120px)
    d.add_arrow(480, 250, 600, 250, stroke="#2b8a3e")
    d.add_text(495, 230, "Ready Events", stroke="#2b8a3e", font_size=11, align="left", w=95)

    # 3. Execution Core Container
    d.add_container(600, 110, 560, 330, label="Single-Threaded Execution Core (aeEventLoop)", stroke="#c92a2a", badge_bg="#ffe3e3", badge_stroke="#c92a2a", label_color="#c92a2a", badge_align="left")
    d.add_box(620, 155, 520, 50, "File Event Dispatcher (Queue)", "Dispatches ready socket events sequentially to command handlers", bg="#ffffff", stroke="#c92a2a", text_color="#c92a2a", font_size=12)

    # Arrow down
    d.add_arrow(880, 205, 880, 240, stroke="#c92a2a")

    d.add_box(620, 240, 520, 180, "In-Memory Key-Value Store", [
        "Pure In-Memory Command Execution Engine",
        "",
        "• Strings (SDS) | Hashes (dict/listpack) | Lists (quicklist)",
        "• Sets (intset/hashtable) | Sorted Sets (skiplist + dict)",
        "• Sub-millisecond latency: Zero mutex locking or thread race conditions"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=13)

    # 4. Bottom Container: Multi-threaded background
    d.add_container(40, 465, 1120, 145, label="Why Redis Is Single-Threaded for Commands yet Multi-Threaded Underneath", stroke="#495057", badge_bg="#f1f3f5", badge_stroke="#495057", label_color="#212529", badge_align="left")
    d.add_box(60, 505, 1080, 85, "Background Asynchronous Offloading Architecture", [
        "• BIO Threads: Socket network reads/writes, AOF fsync flushes, and UNLINK lazy-freeing large keys run on background threads.",
        "• Forked Child Process: BGSAVE snapshotting and BGREWRITEAOF log compaction use Linux Copy-on-Write (CoW) memory pages."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=12)

    d.render("redis-event-loop-architecture.png")


def generate_cluster_persistence():
    d = DiagramBuilder()
    d.add_header(
        "Redis High Availability: Persistence & Sharded Cluster",
        "RDB & AOF Durability, Sentinel Failover Quorum, and 16,384 Hash Slot Topology",
        x=40, y=25, w=1140, h=65
    )

    # 1. Persistence Container (Left)
    d.add_container(40, 110, 490, 250, label="Persistence & Durability Engines", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_align="left")
    d.add_box(60, 155, 450, 85, "RDB (Redis Database Snapshots)", [
        "• Point-in-time binary dump generated via background fork()",
        "• Ultra-fast recovery during server restarts, highly compact"
    ], bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(60, 255, 450, 85, "AOF (Append-Only File Log)", [
        "• Transaction log of all write commands (fsync: everysec)",
        "• Auto-compacted via BGREWRITEAOF, guarantees minimal data loss"
    ], bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)

    # 2. Sentinel Container (Right)
    d.add_container(560, 110, 570, 250, label="High Availability: Master-Replica + Sentinel", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_align="left")
    d.add_box(580, 155, 200, 60, "Master Node", "Primary (Writes & Reads)", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(910, 155, 200, 60, "Replica Node", "Read Scale-out (Async)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # Replication Arrow (gap = 130px)
    d.add_arrow(780, 185, 910, 185, stroke="#2b8a3e")
    d.add_text(800, 165, "Async PSYNC", stroke="#2b8a3e", font_size=11, align="left", w=90)

    # Sentinel Quorum
    d.add_box(580, 245, 530, 95, "Redis Sentinel Quorum (3+ Monitor Nodes)", [
        "• Continuous heartbeat monitoring (PING / PONG) detects node crash",
        "• Quorum agreement triggers auto-failover, promoting replica to master"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)

    # 3. Bottom Sharded Cluster Container
    d.add_container(40, 385, 1090, 235, label="Redis Sharded Cluster: 16,384 Hash Slots & Decentralized Mesh", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_align="left")

    # 3 Shard Nodes
    d.add_box(65, 435, 270, 95, "Master Node 1", [
        "Hash Slots: [0 - 5,460]",
        "• Stores CRC16(key) % 16384",
        "• Replicated by Slave 1"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    d.add_box(450, 435, 270, 95, "Master Node 2", [
        "Hash Slots: [5,461 - 10,922]",
        "• Smart client slot cache",
        "• Replicated by Slave 2"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)

    d.add_box(835, 435, 270, 95, "Master Node 3", [
        "Hash Slots: [10,923 - 16,383]",
        "• Seamless online resharding",
        "• Replicated by Slave 3"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)

    # Gossip Arrows (gaps = 115px)
    d.add_arrow(335, 482, 450, 482, stroke="#495057")
    d.add_text(355, 462, "Gossip Bus", stroke="#495057", font_size=11, align="left", w=80)

    d.add_arrow(720, 482, 835, 482, stroke="#495057")
    d.add_text(740, 462, "Gossip Bus", stroke="#495057", font_size=11, align="left", w=80)

    # Note at bottom
    d.add_box(65, 550, 1040, 50, "Decentralized Routing: Smart clients query any node directly and follow -MOVED redirects without any proxy overhead.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("redis-cluster-persistence.png")

if __name__ == "__main__":
    generate_event_loop()
    generate_cluster_persistence()
