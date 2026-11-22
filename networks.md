# Computer Networks — From Basics to Expert

## Network Models: OSI vs TCP/IP
- **OSI 7-Layer Model**:
  1. **Physical (Layer 1)**: Transmission of raw bits over physical mediums (cables, fiber, radio frequencies).
  2. **Data Link (Layer 2)**: Node-to-node framing, MAC addressing, error detection (Ethernet, Wi-Fi, ARP).
  3. **Network (Layer 3)**: Host-to-host routing and logical addressing (IP, ICMP, IPsec, BGP, OSPF).
  4. **Transport (Layer 4)**: Process-to-process communication, port multiplexing, reliability, flow and congestion control (TCP, UDP).
  5. **Session (Layer 5)**: Manages dialogs, sessions, and synchronization between endpoints (RPC, NetBIOS).
  6. **Presentation (Layer 6)**: Data formatting, serialization, compression, and encryption/decryption (TLS, JSON, ASCII, MIME).
  7. **Application (Layer 7)**: End-user application interfaces and network services (HTTP, DNS, SMTP, FTP, SSH).
- **TCP/IP 4-Layer Model**: Pragmatic internet standard:
  - **Link Layer**: OSI Layers 1 & 2.
  - **Internet Layer**: OSI Layer 3 (IPv4, IPv6, ICMP).
  - **Transport Layer**: OSI Layer 4 (TCP, UDP).
  - **Application Layer**: OSI Layers 5, 6 & 7 (HTTP, DNS, SSH, TLS).

## Transport Layer: TCP vs UDP
- **TCP (Transmission Control Protocol)**:
  - **Connection-oriented, reliable, byte-stream protocol**.
  - **Three-Way Handshake**:
    1. Client → Server: `SYN` (Synchronize sequence number $X$)
    2. Server → Client: `SYN-ACK` (Server sequence number $Y$, Acknowledges $X + 1$)
    3. Client → Server: `ACK` (Acknowledges $Y + 1$)
  - **Four-Way Teardown**: Client sends `FIN` → Server sends `ACK` → Server sends `FIN` → Client sends `ACK` (enters `TIME_WAIT` for $2 \times \text{MSL}$ to prevent delayed segment clashes).
  - **Reliability**: Checksums, sequence numbers, cumulative ACKs, selective acknowledgments (SACK), and automatic retransmissions (RTO).
  - **Flow Control**: Receiver-driven using the **Sliding Window** advertised in TCP header (`rwnd`), preventing fast senders from overwhelming slow receivers.
  - **Congestion Control**: Network-driven via congestion window (`cwnd`). Algorithms:
    - **Slow Start**: Exponential window increase until `ssthresh`.
    - **Congestion Avoidance**: Linear window growth (AIMD: Additive Increase, Multiplicative Decrease).
    - **Modern Algorithms**: BBR (Bottleneck Bandwidth and RTT - Google) model-based throughput optimization vs loss-based (Cubic).
- **UDP (User Datagram Protocol)**:
  - **Connectionless, unreliable, datagram-oriented protocol**.
  - No handshakes, no acknowledgments, no ordering, zero congestion control overhead.
  - Minimal 8-byte header (Source Port, Destination Port, Length, Checksum).
  - Ideal for latency-sensitive applications: DNS lookups, VoIP, live video streaming, multiplayer gaming, and QUIC.

## Application Layer & HTTP Evolution
- **HTTP/1.0**: One TCP connection per request/response cycle. Extremely high latency due to repeated TCP handshakes.
- **HTTP/1.1**:
  - Introduced **Persistent Connections** (`Keep-Alive`), reusing a single TCP connection for multiple requests.
  - Chunked transfer encoding and pipelining (rarely deployed due to Head-of-Line blocking).
  - **Head-of-Line (HoL) Blocking**: Later requests on a connection must wait for earlier requests to complete.
- **HTTP/2**:
  - **Binary Framing Layer**: Replaced text-based protocols with binary frames.
  - **Multiplexing**: Multiple bidirectional streams interleaved over a single TCP connection, eliminating application-level HoL blocking.
  - **HPACK**: Header compression drastically reduces overhead for repeated headers.
  - **Server Push**: Server preemptively sends critical assets (CSS/JS) before client requests them.
  - *Limitation*: TCP packet loss blocks all multiplexed streams at the transport layer (TCP-level HoL blocking).
- **HTTP/3 & QUIC**:
  - Built over **QUIC (UDP-based)** instead of TCP.
  - True multiplexing: Packet loss on one stream does not stall independent streams.
  - Integrated TLS 1.3 handshake: 0-RTT / 1-RTT connection establishment.
  - Connection Migration: Identifies connections via a 64-bit Connection ID rather than the 4-tuple (Client IP, Client Port, Server IP, Server Port), keeping connections alive across network switches (Wi-Fi to 5G).

## HTTPS & TLS Cryptography
- **Encryption Model**:
  - **Asymmetric Encryption** (RSA, ECC / ECDSA): Used during the handshake for identity authentication and secure key exchange.
  - **Symmetric Encryption** (AES-GCM, ChaCha20-Poly1305): Used for high-speed bulk data transfer once the shared session secret is derived.
- **TLS 1.3 vs TLS 1.2**:
  - **TLS 1.2**: Requires 2 round-trips (2-RTT) for the handshake.
  - **TLS 1.3**: Requires only 1 round-trip (1-RTT). Eliminates legacy cipher suites, mandates Perfect Forward Secrecy (PFS via ephemeral Diffie-Hellman), and enables 0-RTT session resumption for returning clients.
- **Digital Certificates & PKI**:
  - Servers present X.509 certificates signed by trusted Certificate Authorities (CAs).
  - Clients verify the digital signature chain against built-in root CA trust stores to defeat Man-in-the-Middle (MitM) attacks.

## DNS (Domain Name System)
- **Hierarchical Distributed Database**:
  - **Root DNS Servers** (`.`) → **Top-Level Domain (TLD) Servers** (`.com`, `.org`) → **Authoritative DNS Servers** (`example.com`).
- **Resolution Flow**:
  1. Browser checks local cache → OS resolver cache → Local DNS Resolver (ISP / 8.8.8.8 / 1.1.1.1).
  2. Recursive resolver queries Root Server → Returns TLD Server IP.
  3. Resolver queries TLD Server → Returns Authoritative Server IP.
  4. Resolver queries Authoritative Server → Returns host IP (A/AAAA record).
  5. Result cached locally governed by **TTL (Time To Live)**.
- **Core DNS Records**:
  - **A**: Maps hostname to IPv4 address.
  - **AAAA**: Maps hostname to IPv6 address.
  - **CNAME**: Alias pointing to another canonical hostname (cannot coexist with other records on apex domain).
  - **MX**: Mail exchange servers.
  - **TXT**: Arbitrary text (SPF, DKIM, domain ownership validation).

## Proxies, Gateways, Firewalls & CDNs
- **Forward Proxy**: Sits in front of clients; acts on behalf of clients to access the internet. Used for client anonymization, traffic filtering, content caching, and corporate egress inspection.
- **Reverse Proxy**: Sits in front of origin backend servers; acts on behalf of servers. Handles load balancing, SSL termination, caching, compression, and request routing (e.g., NGINX, HAProxy, Envoy).
- **API Gateway**: Reverse proxy tailored for microservices; adds rate limiting, authentication, request transformation, telemetry, and service routing.
- **Firewalls**:
  - **Packet-filtering / Layer 4**: Inspects IP addresses, TCP/UDP ports, and protocol flags (e.g., `iptables`, AWS Security Groups).
  - **Stateful Firewalls**: Tracks active connection states in a table to allow return traffic automatically.
  - **Web Application Firewall (WAF / Layer 7)**: Deep packet inspection of HTTP payloads to block OWASP Top 10 exploits (SQLi, XSS, SSRF).
- **Content Delivery Networks (CDNs)**:
  - Geographically distributed edge servers caching static and dynamic web content close to end users.
  - **Anycast Routing**: Routes client requests to the topologically nearest Point of Presence (PoP) using BGP.
  - Features: Origin shielding, edge compute (Cloudflare Workers, Lambda@Edge), DDoS mitigation, and dynamic cache revalidation (`stale-while-revalidate`).
