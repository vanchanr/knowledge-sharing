#!/usr/bin/env python3
"""Generate perfected Distributed Systems diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_raft_protocol():
    d = DiagramBuilder()
    d.add_header(
        "Raft Consensus Protocol: State Machine & Log Replication",
        "Leader Election, Strong Consistency Quorums, and State Machine Safety",
        x=40, y=25, w=1140, h=65
    )

    # 1. Top Container: State Transitions
    d.add_container(40, 110, 1140, 200, label="Raft Node Role Transitions & Election Lifecycle", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # 3 State Boxes (y=155..215, height=60)
    d.add_box(70, 155, 210, 60, "Follower Node", "Passive, responds to RPCs", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(490, 155, 220, 60, "Candidate Node", "Votes for self, collects ballots", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")
    d.add_box(920, 155, 210, 60, "Leader Node", "Handles writes, sends heartbeats", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Forward Transitions (Top path, y=172)
    d.add_arrow(280, 172, 490, 172, label="1. Election Timeout", stroke="#1971c2", label_offset_y=-18)
    d.add_arrow(710, 172, 920, 172, label="2. Quorum Won (N/2+1)", stroke="#2b8a3e", label_offset_y=-18)

    # Reversion Transitions (Bottom path, y=200, clean gap)
    d.add_arrow(490, 200, 280, 200, label="Higher Term / Timeout", stroke="#c92a2a", stroke_style="dashed", label_offset_y=16, font_size=11)
    d.add_arrow(920, 200, 710, 200, label="Higher Term Seen", stroke="#c92a2a", stroke_style="dashed", label_offset_y=16, font_size=11)

    # 2. Bottom Container: Log Replication Pipeline
    d.add_container(40, 330, 1140, 290, label="Two-Phase Log Replication Pipeline (Quorum Commit)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    # Client (ends at 200)
    d.add_box(60, 415, 140, 65, "Client", "SET key = 'val'", bg="#f8f9fa", stroke="#495057", text_color="#212529")

    # Leader (x=290..520, gap = 90px)
    d.add_box(290, 390, 230, 185, "Leader Node", [
        "1. Append to local log",
        "2. Broadcast AppendEntries",
        "3. Wait for Quorum (N/2+1)",
        "4. Commit & apply entry"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Followers (x=640..840, gap = 120px)
    d.add_box(640, 390, 200, 60, "Follower Node 1", "Append to Uncommitted Log", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(640, 500, 200, 60, "Follower Node 2", "Append to Uncommitted Log", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")

    # State Machine (x=960..1160, gap = 120px)
    d.add_box(960, 420, 200, 110, "State Machine", [
        "• Replicated Disk Log",
        "• Deterministic Exec",
        "• Linearizable Read"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5")

    # Pipeline Arrows
    d.add_arrow(200, 447, 290, 447, label="Write Cmd", stroke="#212529", label_offset_y=-18, font_size=11)

    # Leader to Followers (120px gap)
    d.add_arrow(520, 420, 640, 420, label="AppendEntries", stroke="#2b8a3e", label_offset_y=-18, font_size=11)
    d.add_arrow(520, 530, 640, 530, label="AppendEntries", stroke="#2b8a3e", label_offset_y=-18, font_size=11)

    # Followers to State Machine (120px gap)
    d.add_arrow(840, 420, 960, 450, label="ACK Success", stroke="#1971c2", label_offset_y=-18, font_size=11)
    d.add_arrow(840, 530, 960, 500, label="ACK Success", stroke="#1971c2", label_offset_y=16, font_size=11)

    d.render("distributed-systems-raft.png")

def generate_saga_pattern():
    d = DiagramBuilder()
    d.add_header(
        "Distributed Transactions: Orchestrated Saga Pattern with Compensations",
        "Forward Execution Steps vs Backward Compensating Rollback Path",
        x=40, y=25, w=1180, h=65
    )

    # Master Container
    d.add_container(40, 110, 1180, 500, label="Saga Workflow: Forward Transactions vs Compensating Rollback Path", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")

    # Saga Orchestrator on left (50..230)
    d.add_box(50, 160, 180, 310, "Saga Orchestrator", [
        "State Machine Engine",
        "",
        "• Tracks Saga Log",
        "• Invokes Commands",
        "• Handles Replies",
        "• Runs Compensations",
        "• Eventual Consistency"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=13)

    # Forward Path (Top Row)
    # Order: 330..530 (gap from Orch = 100px)
    d.add_box(330, 170, 200, 65, "1. Order Service", "T1: Create Pending Order", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    # Payment: 640..840 (gap = 110px)
    d.add_box(640, 170, 200, 65, "2. Payment Service", "T2: Authorize Card $99", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")
    # Inventory: 950..1150 (gap = 110px)
    d.add_box(950, 170, 200, 65, "3. Inventory Service", "T3: FAIL (Out of Stock!)", bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a")

    # Forward Arrows (100-110px gaps, labels centered)
    d.add_arrow(230, 202, 330, 202, label="1. Exec T1", stroke="#1971c2", label_offset_y=-18, font_size=11)
    d.add_arrow(530, 202, 640, 202, label="2. Success", stroke="#2b8a3e", label_offset_y=-18, font_size=11)
    d.add_arrow(840, 202, 950, 202, label="3. Success", stroke="#2b8a3e", label_offset_y=-18, font_size=11)

    # Trigger Rollback downward arrow
    d.add_arrow(1050, 235, 1050, 360, stroke="#e03131")
    d.add_text(1060, 290, "Trigger Rollback", font_size=11, stroke="#e03131", align="left", w=120)

    # Compensating Path (Bottom Row - Right to Left)
    d.add_box(950, 360, 200, 65, "Stock Failed Node", "Emits StockFailedEvent", bg="#fff5f5", stroke="#e03131", text_color="#c92a2a")
    d.add_box(640, 360, 200, 65, "Compensate Payment", "C2: Refund $99 to Card", bg="#fff5f5", stroke="#e03131", text_color="#c92a2a")
    d.add_box(330, 360, 200, 65, "Compensate Order", "C1: Cancel Order", bg="#fff5f5", stroke="#e03131", text_color="#c92a2a")

    # Compensating Arrows (Right to Left, dashed red, 110px gaps)
    d.add_arrow(950, 392, 840, 392, label="Fail Event", stroke="#e03131", stroke_style="dashed", label_offset_y=-18, font_size=11)
    d.add_arrow(640, 392, 530, 392, label="Rollback OK", stroke="#e03131", stroke_style="dashed", label_offset_y=-18, font_size=11)
    d.add_arrow(330, 392, 230, 392, label="Aborted", stroke="#9c36b5", stroke_style="dashed", label_offset_y=-18, font_size=11)

    # Bottom Architectural Note
    d.add_box(50, 505, 1100, 75, "Saga Invariant: Forward Recovery or Compensating Rollback", [
        "• Compensating transactions (C1, C2) MUST be idempotent and retryable until success.",
        "• Eliminates distributed 2-Phase Commit (2PC) locks, achieving high availability and eventual consistency."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=12)

    d.render("distributed-systems-saga.png")

if __name__ == "__main__":
    generate_raft_protocol()
    generate_saga_pattern()
