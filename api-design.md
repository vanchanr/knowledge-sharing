# API Design — From Basics to Expert

## Core Foundations & Protocols
- **API (Application Programming Interface)**: Provides a standardized contract enabling software systems to communicate and exchange data while abstracting internal implementation complexity.
- **Underlying Protocols**:
  - **DNS**: Translates human-readable API hostnames (`api.example.com`) to IP addresses.
  - **TCP/IP**: Guarantees reliable transport and segment ordering between client and API gateway.
  - **HTTP Evolution**:
    - **HTTP/1.1**: Persistent connections, chunked transfer, text-based headers.
    - **HTTP/2**: Binary framing, stream multiplexing over a single connection, HPACK header compression.
    - **HTTP/3**: Operates over UDP/QUIC, eliminating Head-of-Line blocking at the transport layer.
  - **HTTP Methods & Semantics**:
    - `GET`: Safe and idempotent; retrieves resources without modifying state.
    - `POST`: Non-idempotent; creates new resources or executes processing.
    - `PUT`: Idempotent; completely replaces the target resource state.
    - `PATCH`: Non-idempotent (or idempotent by design); applies partial modifications to a resource.
    - `DELETE`: Idempotent; removes the resource.
  - **HTTP Status Codes**:
    - `2xx (Success)`: `200 OK`, `201 Created` (with `Location` header), `202 Accepted` (async processing), `204 No Content`.
    - `3xx (Redirection)`: `301 Moved Permanently`, `302 Found` (temporary redirect), `304 Not Modified` (caching conditional GET).
    - `4xx (Client Errors)`: `400 Bad Request`, `401 Unauthorized` (missing/invalid credentials), `403 Forbidden` (authenticated, but lacking permissions), `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `429 Too Many Requests`.
    - `5xx (Server Errors)`: `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`.
  - **HTTP Headers & Content Negotiation**:
    - Standard headers: `Content-Type`, `Accept`, `Authorization`, `ETag`, `If-None-Match`.
    - **HTTP Caching**: Controlled via `Cache-Control: public, max-age=3600, stale-while-revalidate=60` and validation via `ETag` returning `304 Not Modified`.
  - **Cookies**: Small stateful tokens stored in the client browser with security attributes: `HttpOnly` (blocks JavaScript XSS access), `Secure` (HTTPS only), `SameSite=Strict|Lax` (mitigates CSRF).
  - **CORS (Cross-Origin Resource Sharing)**: Browser security mechanism governing requests made outside the origin domain. Servers return headers (`Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`) in response to preflight `OPTIONS` requests.

---

## API Architectural Styles

| Feature | RESTful APIs | gRPC | GraphQL |
| :--- | :--- | :--- | :--- |
| **Protocol** | HTTP/1.1 or HTTP/2 | HTTP/2 (Mandatory) | HTTP/1.1 or HTTP/2 |
| **Payload Format** | JSON, XML | Protocol Buffers (Binary) | JSON |
| **Typing** | Weak / Schema via OpenAPI | Strong (Protobuf `.proto` schema) | Strong (GraphQL Schema SDL) |
| **Performance** | Good (text serialization overhead) | Ultra-fast (compact binary serialization) | Moderate (query parsing & resolution overhead) |
| **Streaming** | Request/Response (SSE for 1-way) | Bidirectional streaming | Subscriptions (via WebSockets) |
| **Best For** | Public public-facing web APIs | Microservice-to-microservice internal RPCs | Complex, relational frontend data aggregation |

---

## REST API Design Best Practices

### REST Architectural Constraints
1. **Client-Server**: Separation of UI concerns from data storage concerns.
2. **Stateless**: Each request must contain all context necessary to understand and process the request; server stores no client session context.
3. **Cacheable**: Responses must explicitly define whether they are cacheable.
4. **Uniform Interface**: Resource identification in requests (URIs), manipulation of resources through representations, self-descriptive messages, and HATEOAS.
5. **Layered System**: Client cannot determine whether it is connected directly to origin server or intermediary proxy/gateway.

### Pagination Patterns
- **Offset-Based Pagination**: `GET /api/v1/orders?offset=20&limit=10`
  - *Pros*: Simple to implement (`OFFSET 20 LIMIT 10` in SQL).
  - *Cons*: Severe performance degradation on large offsets ($O(N)$ scan); data drift (missing or duplicate items if rows are inserted while paginating).
- **Cursor-Based (Keyset) Pagination**: `GET /api/v1/orders?cursor=eyJpZCI6MTA0Mn0&limit=10`
  - Uses an indexed, unique sequential attribute (e.g., `WHERE (created_at, id) < (:last_date, :last_id) ORDER BY created_at DESC, id DESC LIMIT 10`).
  - *Pros*: Consistent $O(1)$ performance, immune to insertion drift.
  - *Cons*: Cannot jump to arbitrary pages (sequential navigation only).

### Rate Limiting Algorithms
- **Token Bucket**: Tokens added to a bucket at a constant rate $r$; requests consume tokens. Allows bursts up to bucket capacity $b$.
- **Leaky Bucket**: Requests enter a FIFO queue and leak out at a constant rate. Smooths out traffic spikes into a steady stream.
- **Fixed Window Counter**: Divides time into fixed windows (e.g., 1 minute). Vulnerable to traffic spikes at window boundaries ($2\times$ burst).
- **Sliding Window Log**: Stores timestamps in Redis Sorted Set (`ZSET`). Exact, but high memory footprint.
- **Sliding Window Counter**: Hybrid combining current and previous window counts with weighted interpolation. Memory-efficient with low error margin.

### Idempotency
- Guarantees that executing an operation multiple times produces the identical side-effect as executing it once.
- Critical for non-idempotent operations like payment processing:
  - Client sends a unique UUID in `Idempotency-Key: <UUID>` header.
  - Server checks Redis for the key:
    - If processing: Returns `409 Conflict` or waits for lock.
    - If cached response exists: Returns cached response directly without re-executing business logic.
    - If key does not exist: Sets key with atomic lock (`SET key val NX EX 120`), processes transaction, caches final response, and commits.

### API Versioning Strategies
- **URI Path**: `https://api.example.com/v1/users` (Most explicit and developer-friendly).
- **Query Parameter**: `https://api.example.com/users?version=1`.
- **Custom Header**: `X-API-Version: 2026-11-22`.
- **Content Negotiation (Accept Header)**: `Accept: application/vnd.mycompany.v1+json`.

### Error Handling (RFC 7807 Problem Details)
Return standardized JSON error objects rather than arbitrary strings:
```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "Your balance of $12.50 is lower than the transaction cost of $25.00.",
  "instance": "/accounts/12345/transactions/tx_891",
  "invalid_params": []
}
```

---

## Authentication & Authorization

### Authentication Mechanisms
- **HTTP Basic Auth**: Base64 encoded `username:password` sent in `Authorization: Basic ...` header. Insecure without HTTPS; credentials sent on every request.
- **Session-Based Auth**: Server stores session record in memory/Redis; client receives an opaque cookie (`JSESSIONID`).
- **Token-Based Auth (JWT - JSON Web Tokens)**:
  - Format: `header.payload.signature`
  - Compact, URL-safe, self-contained claim container.
  - Signed via HMAC-SHA256 (symmetric) or RSA/ECDSA (asymmetric key pairs where Auth Server signs with private key, and Resource Servers verify with public JWKS).
- **OAuth 2.0 & OIDC (OpenID Connect)**:
  - **Authorization Code Grant with PKCE (Proof Key for Code Exchange)**: Standard for single-page applications, mobile apps, and web apps.
  - **Client Credentials Grant**: Machine-to-machine backend authentication without end-user context.
  - **OIDC**: Identity layer built on top of OAuth 2.0 providing an `id_token` for user authentication profile data.

### Authorization Models
- **RBAC (Role-Based Access Control)**: Permissions assigned to roles (`ADMIN`, `EDITOR`, `VIEWER`), and roles assigned to users. Coarse-grained.
- **ABAC (Attribute-Based Access Control)**: Evaluates dynamic attributes (user department, resource classification, time of day, IP address). Fine-grained.
- **ReBAC (Relationship-Based Access Control)**: Google Zanzibar model (e.g., OpenFGA). Evaluates relationships on a directed graph ("User is editor of folder that contains document").

---

## Real-Time APIs & Integration Patterns
- **WebSockets**: Full-duplex bidirectional persistent TCP connection established via HTTP `101 Switching Protocols` handshake. Low overhead; ideal for chat, gaming, real-time dashboards.
- **Server-Sent Events (SSE)**: Unidirectional push from server to client over standard HTTP (`text/event-stream`). Native browser auto-reconnect; ideal for live stock feeds and AI LLM response streaming.
- **Webhooks**: Reverse API architecture where the server pushes an asynchronous HTTP POST payload to a client-configured URL upon an event (e.g., Stripe payment completion, GitHub push). Requires signature verification (`X-Hub-Signature-256`) to ensure authenticity.
