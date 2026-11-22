#!/usr/bin/env python3
"""Generate perfected Computer Networks diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_osi_tcpip():
    d = DiagramBuilder()
    d.add_header(
        "Computer Networks: OSI 7-Layer vs TCP/IP 4-Layer Architecture",
        "Layer Mapping, Encapsulation Boundaries, and Protocol Data Units (PDUs)",
        x=40, y=25, w=1160, h=65
    )

    # 1. OSI 7-Layer Container (Left: 40..360, w=320)
    d.add_container(40, 110, 320, 520, label="OSI 7-Layer Reference Model (ISO)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    layers = [
        ("7. Application Layer", "HTTP, DNS, SSH, SMTP", "#e7f5ff", "#1971c2"),
        ("6. Presentation Layer", "TLS/SSL, ASCII, JSON, MIME", "#e7f5ff", "#1971c2"),
        ("5. Session Layer", "Sockets, Named Pipes, RPC", "#e7f5ff", "#1971c2"),
        ("4. Transport Layer", "TCP (Reliable) / UDP", "#ebfbee", "#2b8a3e"),
        ("3. Network Layer", "IPv4, IPv6, ICMP, Routing", "#fff3bf", "#f59f00"),
        ("2. Data Link Layer", "Ethernet 802.3, Wi-Fi MAC", "#f3d9fa", "#9c36b5"),
        ("1. Physical Layer", "Cables, Fiber, RF Signals", "#ffe3e3", "#e03131")
    ]

    curr_y = 155
    for title, sub, bg, stroke in layers:
        d.add_box(55, curr_y, 290, 44, title, sub, bg=bg, stroke=stroke, text_color=stroke, font_size=12)
        curr_y += 50

    d.add_box(55, 520, 290, 90, "OSI Reference Invariants", [
        "• Standard 7-layer theoretical taxonomy.",
        "• Each layer adds header encapsulation."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Mapping Arrows (OSI -> TCP/IP, gap = 360 to 480 = 120px)
    d.add_arrow(360, 230, 480, 230, label="Consolidates", stroke="#1971c2", label_offset_y=-18, font_size=11)
    d.add_arrow(360, 332, 480, 332, label="1 : 1 Map", stroke="#2b8a3e", label_offset_y=-18, font_size=11)
    d.add_arrow(360, 382, 480, 382, label="1 : 1 Map", stroke="#f59f00", label_offset_y=-18, font_size=11)
    d.add_arrow(360, 460, 480, 460, label="Consolidates", stroke="#9c36b5", label_offset_y=-18, font_size=11)

    # 2. TCP/IP Container (Right: 480..1180, w=700)
    d.add_container(480, 110, 720, 520, label="TCP/IP 4-Layer Internet Model & Protocol Data Units (PDUs)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    # TCP/IP Layer 4: Application
    d.add_box(500, 155, 360, 144, "Application Layer", [
        "HTTP/1.1, HTTP/2, HTTP/3 (QUIC)",
        "gRPC, DNS, SMTP, WebSockets",
        "",
        "Consolidates OSI Layers 7, 6, and 5"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(880, 185, 300, 75, "PDU: Data / Payload", "Application data stream, JSON, or protobuf", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # TCP/IP Layer 3: Transport
    d.add_box(500, 309, 360, 46, "Transport Layer (TCP / UDP)", "End-to-end ports, flow & congestion control", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(880, 309, 300, 46, "PDU: Segment (TCP) / Datagram", "TCP Header: Source/Dest Port, Seq/Ack, Flags", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # TCP/IP Layer 2: Internet
    d.add_box(500, 365, 360, 46, "Internet Layer (IPv4 / IPv6)", "Logical host addressing, routing, TTL, ICMP", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_box(880, 365, 300, 46, "PDU: IP Packet", "IP Header: Source/Dest IP, TTL, Protocol ID", bg="#ffffff", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # TCP/IP Layer 1: Network Access / Link
    d.add_box(500, 421, 360, 85, "Network Access / Link Layer", [
        "Ethernet 802.3, Wi-Fi 802.11, ARP",
        "MAC physical addressing & PHY bit signaling",
        "Consolidates OSI Layers 2 and 1"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(880, 428, 300, 70, "PDU: Frame & Raw Bits", "Ethernet Frame: MACs, VLAN, CRC FCS Checksum", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(500, 520, 680, 90, "Practical Reality: The Internet Runs on TCP/IP", [
        "• While OSI is the canonical conceptual model, TCP/IP is the practical architecture of the Internet.",
        "• Senders encapsulate headers down the stack; receivers de-encapsulate headers up the stack."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("networks-osi-tcpip-model.png")

def generate_tcp_lifecycle():
    d = DiagramBuilder()
    d.add_header(
        "TCP Connection Lifecycle: 3-Way Handshake & 4-Way Teardown",
        "Reliable Connection Establishment, Full-Duplex FIN Termination, and TIME_WAIT State",
        x=40, y=25, w=1120, h=65
    )

    # Top Entities
    # Client center: 240
    d.add_box(140, 110, 200, 55, "TCP Client", "Active Opener", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    # Server center: 880
    d.add_box(780, 110, 200, 55, "TCP Server", "Passive Listener", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Full vertical lifelines from bottom of entity box (165) down to 670
    d.add_lifeline(240, 165, 670, stroke="#868e96", stroke_width=2, stroke_style="dashed")
    d.add_lifeline(880, 165, 670, stroke="#868e96", stroke_width=2, stroke_style="dashed")

    # 1. Handshake Container (y=180..390)
    d.add_container(50, 180, 1020, 215, label="3-Way Handshake: Connection Establishment", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    # Step 1: Client -> Server
    d.add_sequence_message(240, 880, 255, "1. SYN (seq = X) [Client -> SYN_SENT]", stroke="#1971c2", font_size=12)

    # Step 2: Server -> Client
    d.add_sequence_message(880, 240, 310, "2. SYN-ACK (seq = Y, ack = X + 1) [Server -> SYN_RCVD]", stroke="#2b8a3e", is_response=True, font_size=12)

    # Step 3: Client -> Server
    d.add_sequence_message(240, 880, 365, "3. ACK (ack = Y + 1) [Connection ESTABLISHED on both ends]", stroke="#1971c2", font_size=12)

    # 2. Teardown Container (y=415..685)
    d.add_container(50, 415, 1020, 270, label="4-Way Teardown: Graceful Connection Termination", stroke="#c92a2a", badge_bg="#ffe3e3", badge_stroke="#c92a2a", label_color="#c92a2a")

    # Step 1: Client -> Server
    d.add_sequence_message(240, 880, 490, "1. FIN (Client initiates close) [Client -> FIN_WAIT_1]", stroke="#e03131", font_size=12)

    # Step 2: Server -> Client
    d.add_sequence_message(880, 240, 540, "2. ACK (Server acks FIN) [Client -> FIN_WAIT_2 | Server -> CLOSE_WAIT]", stroke="#495057", is_response=True, font_size=12)

    # Step 3: Server -> Client
    d.add_sequence_message(880, 240, 590, "3. FIN (Server closes remaining half) [Server -> LAST_ACK]", stroke="#e03131", is_response=True, font_size=12)

    # Step 4: Client -> Server
    d.add_sequence_message(240, 880, 640, "4. ACK (Client acks) [Client -> TIME_WAIT (2 x MSL) | Server -> CLOSED]", stroke="#1971c2", font_size=12)

    d.render("networks-tcp-handshake-teardown.png")

if __name__ == "__main__":
    generate_osi_tcpip()
    generate_tcp_lifecycle()
