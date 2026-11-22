#!/usr/bin/env python3
"""Generate perfected Docker and Kubernetes architecture diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_docker():
    d = DiagramBuilder()
    d.add_header(
        "Virtualization Architecture: Virtual Machines vs Docker Containers",
        "Hypervisor Hardware Emulation vs Linux Kernel Isolation (Namespaces, Cgroups & UnionFS)",
        x=40, y=25, w=1160, h=65
    )

    # 1. Left Container: Virtual Machines (x=40..570, w=530)
    d.add_container(40, 110, 530, 480, label="Virtual Machines (Hypervisor Architecture)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")

    # Apps
    d.add_box(60, 155, 150, 55, "App 1", "Bins & Libs A", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)
    d.add_box(230, 155, 150, 55, "App 2", "Bins & Libs B", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)
    d.add_box(400, 155, 150, 55, "App 3", "Bins & Libs C", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    # Guest OS
    d.add_box(60, 225, 490, 55, "Guest Operating System (Ubuntu / Windows Server)", "Full OS kernel instance, system daemons & drivers (1-10 GB per VM)", bg="#e5dbff", stroke="#7950f2", text_color="#7950f2", font_size=11)

    # Hypervisor
    d.add_box(60, 295, 490, 55, "Hypervisor (Type 1: ESXi, KVM | Type 2: VirtualBox)", "Hardware virtualization layer emulating virtual CPU, RAM, and disk controllers", bg="#d0bfff", stroke="#5f3dc4", text_color="#5f3dc4", font_size=11)

    # Host OS & Hardware
    d.add_box(60, 365, 490, 55, "Host Operating System & Physical Hardware", "Host OS Kernel | Bare-Metal CPU, Physical RAM, NVMe Storage, NIC", bg="#f1f3f5", stroke="#495057", text_color="#212529", font_size=11)

    # VM Characteristics
    d.add_box(60, 435, 490, 135, "VM Architecture Invariants", [
        "• Strict Hardware Isolation: Hardware boundary; guest kernel failure is isolated.",
        "• High Resource Overhead: Duplicates full OS kernels; multi-GB RAM footprint.",
        "• Slow Cold Startup: Minutes to boot guest kernel, initialize systemd & daemons.",
        "• Massive Images: Heavyweight VM images (10s of GBs) with hypervisor lock-in."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 2. Right Container: Docker Containers (x=610..1200, w=590)
    d.add_container(610, 110, 590, 480, label="Docker Containers (OS-Level Virtualization)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # Containers
    d.add_box(630, 155, 170, 55, "Container 1 (Node.js)", "App + Bundled Libs", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(820, 155, 170, 55, "Container 2 (Go)", "Static Binary + Assets", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(1010, 155, 170, 55, "Container 3 (Python)", "App + Virtualenv Libs", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Docker Engine / Container Runtime
    d.add_box(630, 225, 550, 55, "Container Runtime (Docker Engine / containerd)", "Translates Dockerfiles to OCI specifications, configures veth bridges & namespaces", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Linux Kernel Isolation Primitives
    d.add_box(630, 295, 550, 65, "Linux Kernel Primitives (Namespaces & Cgroups)", [
        "• Namespaces: Process isolation (pid, net, mnt, ipc, uts, user)",
        "• Cgroups v2: Resource metering & ceilings (CPU shares, Memory limits, Disk I/O)"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Storage: OverlayFS
    d.add_box(630, 375, 550, 45, "OverlayFS Storage Driver: UpperDir (R/W) + LowerDir (Read-Only Image Layers)", "Copy-on-Write (CoW) enables instant spin-up and tiny storage footprint", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Container Characteristics
    d.add_box(630, 435, 550, 135, "Container Architecture Invariants", [
        "• Process-Level Isolation: Isolated host processes sharing the host Linux kernel.",
        "• Zero Hypervisor Overhead: Sub-second startup, native CPU execution, dynamic RAM.",
        "• High Density: Hundreds of containers run efficiently on a single physical host.",
        "• Standardized Portability: Immutable OCI image layers run identically anywhere."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Master Banner
    d.add_box(40, 605, 1160, 50, "Core Takeaway: Containers are NOT lightweight VMs; they are isolated Linux host processes restricted by kernel namespaces and cgroups.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("docker-container-architecture.png")

def generate_kubernetes():
    d = DiagramBuilder()
    d.add_header(
        "Kubernetes (K8s) Cluster Architecture",
        "Control Plane Master Orchestration, Worker Node Daemons, and Pod Execution Model",
        x=40, y=25, w=1220, h=65
    )

    # 1. Left Container: Control Plane (x=40..580, w=540)
    d.add_container(40, 110, 540, 520, label="Control Plane (Master Node)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # kube-apiserver
    d.add_box(60, 155, 500, 60, "kube-apiserver (Central Gateway & Control Plane Hub)", "Validates & configures data for all API objects | Exposes secure REST endpoints", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # etcd Box (Left: 60..280, w=220)
    d.add_box(60, 255, 230, 140, "etcd (Key-Value Store)", [
        "• Consistent, HA state storage",
        "• Raft consensus protocol",
        "• Watches & revision history",
        "• Single source of cluster truth",
        "• apiserver is sole client"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    # Arrow: apiserver <-> etcd (Left)
    d.add_arrow(175, 215, 175, 255, label="R/W State (Raft)", stroke="#9c36b5", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # Control Loops & Scheduler (Right: 310..560, w=250)
    d.add_container(310, 245, 250, 160, label="Master Controllers & Schedulers", stroke="#f59f00", badge_bg="#fff3bf", badge_stroke="#f59f00", label_color="#d9480f")
    d.add_box(320, 280, 230, 55, "kube-scheduler", "Filters & scores nodes for pods", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_box(320, 345, 230, 50, "kube-controller-manager", "Runs Node, ReplicaSet, Endpoints loops", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Arrow: apiserver <-> Master Controllers
    d.add_arrow(435, 215, 435, 245, label="Watch & Reconcile", stroke="#f59f00", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # Control Plane Note
    d.add_box(60, 420, 500, 190, "Control Plane Architectural Invariants", [
        "• Gatekeeper Rule: kube-apiserver is the ONLY component allowed to speak with etcd.",
        "• Declarative Reconciliation: Controllers poll desired state vs current state.",
        "• Stateless Apiservers: All state lives in etcd; apiservers scale horizontally.",
        "• Concurrency: etcd uses resource revisions to prevent write collisions."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 2. Right Container: Worker Node (x=660..1260, w=600)
    d.add_container(660, 110, 600, 520, label="Worker Node (Data Plane)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    # Worker Daemons
    d.add_box(680, 155, 260, 60, "kubelet (Node Agent)", "Watches PodSpecs, drives CRI runtime", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(960, 155, 280, 60, "kube-proxy (Network Proxy)", "Programs iptables / IPVS Service routes", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Arrow: apiserver -> kubelet (between containers, gap = 100px)
    d.add_arrow(560, 185, 680, 185, label="PodSpec Sync", stroke="#1971c2", label_offset_y=-18, label_bg="#ffffff", font_size=11)

    # CRI Runtime Box
    d.add_box(680, 245, 560, 50, "Container Runtime Interface (CRI: containerd / CRI-O)", "Pulls images, sets up namespaces/cgroups via runc, manages container lifecycle", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Arrow: kubelet -> CRI
    d.add_arrow(810, 215, 810, 245, label="gRPC CRI", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    # Pod Container (Atomic Scheduling Unit)
    d.add_container(680, 310, 560, 160, label="Pod: 'order-service-pod' (Atomic Scheduling Unit)", stroke="#f59f00", badge_bg="#fff3bf", badge_stroke="#f59f00", label_color="#d9480f")
    d.add_box(700, 345, 250, 55, "App Container", "Spring Boot Service (Port 8080)", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(970, 345, 250, 55, "Sidecar Container", "Envoy Mesh Proxy / Fluentd", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)
    d.add_box(700, 410, 520, 48, "Shared Pod Boundary: Shared Network Namespace (localhost) & Volume Mounts", "Containers communicate over localhost; share network IP, port space, and lifecycle", bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Arrow: CRI -> Pod
    d.add_arrow(960, 295, 960, 310, stroke="#1971c2")

    # Worker Node Note
    d.add_box(680, 485, 560, 125, "Worker Node Architectural Invariants", [
        "• Pod Isolation: Pod is the atomic unit of scheduling; containers in a Pod co-exist on same node.",
        "• IP-per-Pod Model: Every Pod gets a unique cluster-routable IP; no port-mapping conflicts.",
        "• Decoupled Network: kube-proxy programs Linux kernel packet filters for instant L4 routing."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Master Banner
    d.add_box(40, 645, 1220, 50, "Kubernetes Invariant: kube-apiserver is the single point of entry; nodes and controllers never communicate with etcd directly.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("kubernetes-architecture-overview.png")

if __name__ == "__main__":
    generate_docker()
    generate_kubernetes()
