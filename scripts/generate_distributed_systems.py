#!/usr/bin/env python3
"""Generate perfected Distributed Systems diagrams with zero defects."""
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

    # 1. Top Container: State Transitions (h=195)
    d.add_container(40, 110, 1140, 195, label="Raft Node Role Transitions & Election Lifecycle", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_align="left")

    # 3 State Boxes (y=150..205, height=55)
    d.add_box(70, 150, 210, 55, "Follower Node", "Passive, responds to incoming RPCs", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(490, 150, 220, 55, "Candidate Node", "Increments term, votes, asks ballots", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")
    d.add_box(920, 150, 210, 55, "Leader Node", "Handles writes, streams heartbeats", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Forward Transitions (Top path, y=165)
    d.add_arrow(280, 165, 490, 165, stroke="#1971c2")
    d.add_text(315, 145, "1. Election Timeout", stroke="#1971c2", font_size=11, align="left", w=150)

    d.add_arrow(710, 165, 920, 165, stroke="#2b8a3e")
    d.add_text(740, 145, "2. Quorum Won (N/2+1)", stroke="#2b8a3e", font_size=11, align="left", w=155)

    # Reversion Transitions (Bottom path, y=192, clean gap)
    d.add_arrow(490, 192, 280, 192, stroke="#c92a2a", stroke_style="dashed")
    d.add_text(315, 197, "Higher Term Seen / Split Vote", stroke="#c92a2a", font_size=10, align="left", w=160)

    d.add_arrow(920, 192, 710, 192, stroke="#c92a2a", stroke_style="dashed")
    d.add_text(745, 197, "Higher Term Discovered", stroke="#c92a2a", font_size=10, align="left", w=150)

    # Invariant bar inside top container
    d.add_box(70, 230, 1060, 55, "Election Safety Invariant", [
        "• Randomized Election Timeouts (150ms - 300ms) prevent simultaneous candidate elections and split votes.",
        "• At most ONE leader can be elected per term; log completeness guarantees only nodes with all committed entries win election."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=11)

    # 2. Bottom Container: Log Replication Pipeline (y=325..625, h=300)
    d.add_container(40, 325, 1140, 300, label="Two-Phase Log Replication Pipeline (Quorum Commit)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_align="left")

    # Client (ends at 190)
    d.add_box(60, 420, 130, 65, "Client", "SET key = 'val'", bg="#f8f9fa", stroke="#495057", text_color="#212529")

    # Leader (x=270..500, gap = 80px)
    d.add_box(270, 375, 230, 175, "Leader Node (Term T)", [
        "1. Append entry to local disk log",
        "2. Broadcast AppendEntries RPCs",
        "3. Wait for Quorum (N/2 + 1) ACKs",
        "4. Advance commitIndex",
        "5. Apply entry to State Machine"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Followers (x=630..840, gap = 130px)
    d.add_box(630, 375, 210, 60, "Follower Node 1", "Appends entry to uncommitted log", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(630, 490, 210, 60, "Follower Node 2", "Appends entry to uncommitted log", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")

    # State Machine (x=950..1150, gap = 110px)
    d.add_box(950, 400, 200, 120, "Replicated State Machine", [
        "• Deterministic Execution",
        "• Committed Disk Log",
        "• Linearizable Read Store",
        "• Consistent State across nodes"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5")

    # Pipeline Arrows:
    # Client -> Leader (Write)
    d.add_arrow(190, 440, 270, 440, stroke="#212529")
    d.add_text(200, 420, "Write Cmd", stroke="#212529", font_size=11, align="left", w=65)

    # Leader -> Client (200 OK after quorum commit)
    d.add_arrow(270, 465, 190, 465, stroke="#2b8a3e", stroke_style="dashed")
    d.add_text(198, 474, "200 Success", stroke="#2b8a3e", font_size=10, align="left", w=72)

    # Leader -> Followers (AppendEntries)
    d.add_arrow(500, 395, 630, 395, stroke="#2b8a3e")
    d.add_text(515, 375, "AppendEntries", stroke="#2b8a3e", font_size=11, align="left", w=100)

    d.add_arrow(500, 510, 630, 510, stroke="#2b8a3e")
    d.add_text(515, 490, "AppendEntries", stroke="#2b8a3e", font_size=11, align="left", w=100)

    # Followers -> Leader (Quorum ACKs)
    d.add_arrow(630, 415, 500, 415, stroke="#1971c2", stroke_style="dashed")
    d.add_text(525, 420, "ACK Entry", stroke="#1971c2", font_size=10, align="left", w=80)

    d.add_arrow(630, 530, 500, 530, stroke="#1971c2", stroke_style="dashed")
    d.add_text(525, 535, "ACK Entry", stroke="#1971c2", font_size=10, align="left", w=80)

    # Leader -> State Machine (Apply committed entry)
    d.add_arrow(500, 455, 950, 455, stroke="#9c36b5", stroke_width=2)
    d.add_text(680, 440, "Commit & Apply to State Machine", stroke="#9c36b5", font_size=11, align="center", w=200)

    # Invariant bar at bottom of container
    d.add_box(60, 575, 1100, 38, "State Machine Safety Invariant", [
        "If a server applies a log entry at a given index to its state machine, no other server will ever apply a different log entry for the same index."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#2b8a3e", font_size=11)

    d.render("distributed-systems-raft.png")


def generate_saga_pattern():
    d = DiagramBuilder()
    d.add_header(
        "Distributed Transactions: Orchestrated Saga Pattern with Compensations",
        "Forward Execution Steps vs Backward Compensating Rollback Path",
        x=40, y=25, w=1180, h=65
    )

    # Master Container
    d.add_container(40, 110, 1180, 520, label="Saga Workflow: Forward Transactions vs Compensating Rollback Path", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_align="left")

    # Saga Orchestrator on left (55..235)
    d.add_box(55, 160, 180, 310, "Saga Orchestrator", [
        "State Machine Engine",
        "",
        "• Tracks Saga Log",
        "• Invokes Commands",
        "• Handles Replies",
        "• Runs Compensations",
        "• Eventual Consistency"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=13)

    # Forward Path (Top Row)
    # Order: 320..520 (gap from Orch = 85px)
    d.add_box(320, 170, 200, 65, "1. Order Service", "T1: Create Pending Order", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    # Payment: 630..830 (gap = 110px)
    d.add_box(630, 170, 200, 65, "2. Payment Service", "T2: Authorize Card $99", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")
    # Inventory: 940..1140 (gap = 110px)
    d.add_box(940, 170, 200, 65, "3. Inventory Service", "T3: FAIL (Out of Stock!)", bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a")

    # Forward Arrows (85-110px gaps, text clearly above line)
    d.add_arrow(235, 202, 320, 202, stroke="#1971c2")
    d.add_text(240, 182, "1. Exec T1", stroke="#1971c2", font_size=11, align="left", w=75)

    d.add_arrow(520, 202, 630, 202, stroke="#2b8a3e")
    d.add_text(535, 182, "2. Success", stroke="#2b8a3e", font_size=11, align="left", w=85)

    d.add_arrow(830, 202, 940, 202, stroke="#2b8a3e")
    d.add_text(845, 182, "3. Success", stroke="#2b8a3e", font_size=11, align="left", w=85)

    # Trigger Rollback downward arrow
    d.add_arrow(1040, 235, 1040, 360, stroke="#e03131")
    d.add_text(1050, 290, "Trigger Rollback", font_size=11, stroke="#e03131", align="left", w=120)

    # Compensating Path (Bottom Row - Right to Left)
    d.add_box(940, 360, 200, 65, "Stock Failed Node", "Emits StockFailedEvent", bg="#fff5f5", stroke="#e03131", text_color="#c92a2a")
    d.add_box(630, 360, 200, 65, "Compensate Payment", "C2: Refund $99 to Card", bg="#fff5f5", stroke="#e03131", text_color="#c92a2a")
    d.add_box(320, 360, 200, 65, "Compensate Order", "C1: Cancel Order", bg="#fff5f5", stroke="#e03131", text_color="#c92a2a")

    # Compensating Arrows (Right to Left, dashed red, 110px gaps, labels placed cleanly above line)
    d.add_arrow(940, 392, 830, 392, stroke="#e03131", stroke_style="dashed")
    d.add_text(840, 372, "Fail Event", stroke="#e03131", font_size=11, align="left", w=80)

    d.add_arrow(630, 392, 520, 392, stroke="#e03131", stroke_style="dashed")
    d.add_text(530, 372, "Rollback OK", stroke="#e03131", font_size=11, align="left", w=90)

    d.add_arrow(320, 392, 235, 392, stroke="#9c36b5", stroke_style="dashed")
    d.add_text(240, 372, "Aborted", stroke="#9c36b5", font_size=11, align="left", w=75)

    # Bottom Architectural Invariant Note
    d.add_box(55, 510, 1100, 75, "Saga Invariant: Forward Recovery or Compensating Rollback", [
        "• Compensating transactions (C1, C2) MUST be idempotent and retryable until success.",
        "• Eliminates distributed 2-Phase Commit (2PC) locks, achieving high availability and eventual consistency."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=12)

    d.render("distributed-systems-saga.png")

if __name__ == "__main__":
    generate_raft_protocol()
    generate_saga_pattern()
