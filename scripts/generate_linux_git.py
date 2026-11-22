#!/usr/bin/env python3
"""Generate perfected Linux OS and Git Architecture diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_linux():
    d = DiagramBuilder()
    d.add_header(
        "Linux Operating System Architecture: Kernel & User Space Separation",
        "Ring 3 (Unprivileged) vs Ring 0 (Privileged), System Call Interface (SCI), and Hardware Subsystems",
        x=40, y=20, w=1220, h=65
    )

    # 1. User Space Container (Ring 3) (x=40..1240, w=1200, h=160)
    d.add_container(40, 100, 1200, 160, label="User Space (Ring 3 - Isolated, Unprivileged Mode)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=400)

    # 4 User Space components (w=265, gap=15)
    d.add_box(60, 145, 265, 80, "User Applications", "Web servers (Nginx), JVM, Python;\nDirect hardware access blocked", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(345, 145, 275, 80, "C Standard Library (glibc / musl)", "POSIX wrapper APIs (read, fork, mmap);\nTranslates calls to syscall traps", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(640, 145, 275, 80, "System Daemons (systemd, sshd)", "Service supervisor, journald logging,\nCron scheduler & network daemons", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(935, 145, 285, 80, "Shells & Core Utilities", "bash, zsh; coreutils (ls, ps, grep);\nEnvironment variables & pipes (|)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # 2. System Call Interface (SCI) Boundary (y=280..335)
    d.add_box(60, 285, 1160, 50, "System Call Interface (SCI) | Context Switch Boundary (User Mode -> Kernel Mode)", "Software Interrupt (syscall instruction / int 0x80) switches CPU from Ring 3 to Ring 0: clone(), read(), write(), epoll_wait(), mmap()", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Down arrow from glibc to SCI
    d.add_arrow(482, 225, 482, 285, label="Syscall Trap", stroke="#f59f00", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # 3. Kernel Space Container (Ring 0) (x=40..1240, w=1200, h=230)
    d.add_container(40, 355, 1200, 230, label="Kernel Space (Ring 0 - Monolithic Architecture, Direct Hardware Access)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_w=540, badge_align="right")

    # Arrow from SCI into Kernel Space
    d.add_arrow(482, 335, 482, 400, label="Ring 0 Transition", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # 5 Kernel Subsystems (w=220, gap=15)
    d.add_box(60, 400, 220, 85, "Process Scheduler", "CFS / EEVDF scheduler;\nTask contexts & CPU time slices", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(295, 400, 220, 85, "Memory Manager", "Virtual Memory (VMM / MMU);\nPage tables, TLB, swap & OOM", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(530, 400, 220, 85, "Virtual File System", "VFS: 'Everything is a file';\next4, XFS, tmpfs, inodes & fds", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(765, 400, 220, 85, "Networking Stack", "Socket buffers (sk_buff);\nTCP windowing, Netfilter, eBPF", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(1000, 400, 220, 85, "Device Drivers", "Block (NVMe), char (tty), NIC;\nDynamically loadable modules", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_box(60, 500, 1160, 65, "Kernel Architectural Invariants", [
        "• Ring 0 Privilege: Monolithic kernel code executes with full CPU hardware privileges.",
        "• Fault Isolation: A crash in user space kills only the process; a crash in Ring 0 triggers a Kernel Panic.",
        "• Virtual Memory: User space processes cannot read or write to kernel memory addresses (KPTI)."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 4. Hardware Infrastructure Container (x=40..1240, w=1200, h=85)
    d.add_box(60, 605, 1160, 50, "Physical Hardware Infrastructure", "CPU Cores (x86_64 / ARM64, MMU, L1/L2/L3 Caches) | Physical RAM | NVMe SSD Storage | Network Interface Cards (NIC)", bg="#f1f3f5", stroke="#495057", text_color="#212529", font_size=11)
    d.add_arrow(640, 565, 640, 605, label="Bus & IRQ Interrupts", stroke="#495057", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # Master Bottom Banner
    d.add_box(40, 675, 1220, 45, "Core Linux Philosophy: Hardware protection rings ensure application crashes cannot corrupt kernel memory; VFS abstracts all resources as file descriptors.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("linux-kernel-architecture.png")

def generate_git():
    d = DiagramBuilder()
    d.add_header(
        "Git Internal Architecture: The Four Areas & Branch Integration",
        "Working Directory, Staging Area (Index), Local Repository (.git), and Remote Tracking + Merge vs Rebase",
        x=40, y=20, w=1220, h=65
    )

    # Part 1: Top Master Container: The Four Git Areas (x=40..1240, w=1200, h=255)
    d.add_container(40, 100, 1200, 255, label="The Four Core Git Areas & Object Transitions", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=340)

    # Area 1: Working Directory
    d.add_box(60, 145, 250, 100, "1. Working Directory", [
        "• Local files on disk",
        "• Untracked or Modified",
        "• Sandbox where code is edited",
        "• Discard: 'git restore .'"
    ], bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a", font_size=11)

    # Arrow 1: Forward (git add) & Reverse (git restore)
    d.add_arrow(310, 175, 360, 175, label="git add", stroke="#1971c2", label_offset_y=-14, font_size=11)
    d.add_arrow(360, 215, 310, 215, label="git restore", stroke="#e03131", label_offset_y=14, font_size=11)

    # Area 2: Staging Area
    d.add_box(360, 145, 250, 100, "2. Staging Area (Index)", [
        "• .git/index binary file",
        "• Snapshot of next commit",
        "• Creates SHA-1 blob objects",
        "• Unstage: 'git restore --staged'"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Arrow 2: Forward (git commit) & Reverse (git reset)
    d.add_arrow(610, 175, 660, 175, label="git commit", stroke="#2b8a3e", label_offset_y=-14, font_size=11)
    d.add_arrow(660, 215, 610, 215, label="git reset HEAD~1", stroke="#f59f00", label_offset_y=14, font_size=11)

    # Area 3: Local Repository
    d.add_box(660, 145, 250, 100, "3. Local Repo (.git Objects)", [
        "• Immutable DAG of commits",
        "• Trees, Blobs, Commits, Tags",
        "• HEAD branch reference pointer",
        "• Offline commits & branches"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Arrow 3: Forward (git push) & Reverse (git pull)
    d.add_arrow(910, 175, 960, 175, label="git push", stroke="#1971c2", label_offset_y=-14, font_size=11)
    d.add_arrow(960, 215, 910, 215, label="git pull", stroke="#1971c2", label_offset_y=14, font_size=11)

    # Area 4: Remote Repository
    d.add_box(960, 145, 260, 100, "4. Remote Repo (GitHub)", [
        "• Hosted bare repository",
        "• Tracking refs (origin/main)",
        "• Team collaboration via PRs",
        "• CI/CD pipeline webhooks"
    ], bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Summary note for Part 1
    d.add_box(60, 265, 1160, 75, "Git Object Model Invariant", [
        "• Blobs: Store file contents. Trees: Store directory listings and filenames pointing to blobs.",
        "• Commits: Point to a top-level Tree object, author/committer metadata, and parent commit SHAs.",
        "• Branches: Lightweight movable pointers (41 bytes: 40-char SHA + newline) in .git/refs/heads/."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Part 2: Bottom Master Container: Merge vs Rebase (x=40..1240, w=1200, h=275)
    d.add_container(40, 375, 1200, 275, label="Branch Integration Architecture: Git Merge vs Git Rebase", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_w=460)

    # Left Half: Git Merge (x=60..620, w=560)
    d.add_box(60, 420, 560, 130, "git merge feature (3-Way Merge Commit)", [
        "• Graph Topology: Preserves complete historical branch graph as it actually happened.",
        "• 3-Way Merge: Compares Base Ancestor (C0) with Main Tip (M2) and Feature Tip (F2).",
        "• Merge Commit (M3): Generates a new commit with TWO parents (Parent 1: M2, Parent 2: F2).",
        "• Invariant: Completely non-destructive. Commit hashes are never rewritten or altered.",
        "• Best Practice: Use when merging Pull Requests into shared production branches (main)."
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    # Right Half: Git Rebase (x=660..1220, w=560)
    d.add_container(660, 420, 560, 130, label="git rebase main (Linear History Replay)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_w=310, badge_align="right")
    d.add_box(680, 455, 520, 85, "Replays Feature Commits on Tip of Main", [
        "• Unwinds feature commits and fast-forwards feature base to latest Main commit (M2).",
        "• Re-applies changes as brand new commits (F1', F2') with NEW SHA hashes.",
        "• Linear Graph: Produces a clean, single line of commit history without merge bubbles.",
        "• Golden Rule: NEVER rebase shared/public branches! Only rebase local private branches."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Summary note for Part 2
    d.add_box(60, 570, 1160, 65, "Golden Rule of Rebase & Collaboration", [
        "• Private Feature Branches: Rebase and squash local commits to create clean, reviewable PRs.",
        "• Public / Production Branches: Always use Merge to preserve genuine timeline and audit trail.",
        "• Fast-Forward: If main has not diverged, git merge simply moves the branch pointer forward."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=11)

    # Master Bottom Banner
    d.add_box(40, 675, 1220, 45, "Core Git Philosophy: Git is an immutable, content-addressable key-value store (DAG) masked by a familiar version control command line.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("git-workflow-architecture.png")

if __name__ == "__main__":
    generate_linux()
    generate_git()
