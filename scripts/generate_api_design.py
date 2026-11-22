#!/usr/bin/env python3
"""Generate perfected API Design diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_styles_comparison():
    d = DiagramBuilder()
    d.add_header(
        "API Architectural Styles: REST vs gRPC vs GraphQL",
        "Key Trade-offs, Data Protocols, and Optimal Production Use Cases",
        x=40, y=25, w=980, h=65
    )

    # Column 1: REST
    d.add_container(40, 110, 305, 450, label="RESTful APIs", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")
    d.add_box(55, 155, 275, 55, "Resource-Based URLs", "Hierarchical nouns (/users/123/orders)", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(55, 225, 275, 55, "Standard HTTP Verbs", "GET (safe/idempotent), POST, PUT, DELETE", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(55, 295, 275, 55, "JSON / Text Payloads", "Human-readable, stateless HTTP caching", bg="#ffffff", stroke="#1971c2", text_color="#1971c2")
    d.add_box(55, 370, 275, 165, "Best Suited For:", [
        "• Public & Third-Party Partner APIs",
        "• Standard Web & Mobile CRUD apps",
        "• High cacheability via CDN edge nodes"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#0c8599")

    # Column 2: gRPC
    d.add_container(375, 110, 310, 450, label="gRPC (Remote Procedure Call)", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")
    d.add_box(390, 155, 280, 55, "Protocol Buffers", "Strict binary schema contract (.proto)", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(390, 225, 280, 55, "HTTP/2 Multiplexing", "Bi-directional streaming & header compression", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(390, 295, 280, 55, "Ultra-Low Latency", "7-10x smaller payload than JSON", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(390, 370, 280, 165, "Best Suited For:", [
        "• Internal Microservice-to-Microservice IPC",
        "• Real-time streaming & IoT telemetry",
        "• Polyglot environments with type safety"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Column 3: GraphQL
    d.add_container(715, 110, 305, 450, label="GraphQL (Query Language)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")
    d.add_box(730, 155, 275, 55, "Single Smart Endpoint", "POST /graphql handles queries & mutations", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5")
    d.add_box(730, 225, 275, 55, "Client-Driven Queries", "Clients request exactly the fields needed", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5")
    d.add_box(730, 295, 275, 55, "Zero Over/Under-Fetching", "Resolvers compose multiple data sources", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5")
    d.add_box(730, 370, 275, 165, "Best Suited For:", [
        "• Complex Frontend & Mobile UIs (BFF pattern)",
        "• Aggregating heterogeneous backends",
        "• Fast-changing client presentation needs"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5")

    d.render("api-design-styles-comparison.png")

def generate_oauth2_pkce():
    d = DiagramBuilder()
    d.add_header(
        "OAuth 2.0 Authorization Code Flow with PKCE (RFC 7636)",
        "Secure Token Exchange Sequence for SPAs, Mobile Apps, and Public Clients",
        x=40, y=25, w=980, h=65
    )

    # Entities at top
    # Client center: 180
    d.add_box(70, 115, 220, 55, "Single-Page / Mobile Client", "Public Client (Cannot keep secrets)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")
    # Auth Server center: 530
    d.add_box(410, 115, 240, 55, "Authorization Server", "IdP (Keycloak, Auth0, Okta)", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")
    # Resource Server center: 870
    d.add_box(760, 115, 220, 55, "Resource Server", "Protected Backend API", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Vertical lifelines from bottom of entity box (170) down to 570
    d.add_lifeline(180, 170, 560, stroke="#868e96", stroke_width=2, stroke_style="dashed")
    d.add_lifeline(530, 170, 560, stroke="#868e96", stroke_width=2, stroke_style="dashed")
    d.add_lifeline(870, 170, 560, stroke="#868e96", stroke_width=2, stroke_style="dashed")

    # Sequence Messages
    # Step 1: Client -> Auth Server
    d.add_sequence_message(180, 530, 215, "1. GET /authorize (code_challenge=S256)", stroke="#1971c2", font_size=12)

    # Step 2: Auth Server -> Client
    d.add_sequence_message(530, 180, 275, "2. Redirect user with auth_code", stroke="#e67700", is_response=True, font_size=12)

    # Step 3: Client -> Auth Server
    d.add_sequence_message(180, 530, 335, "3. POST /token (auth_code + code_verifier)", stroke="#1971c2", font_size=12)

    # Step 4: Auth Server -> Client
    d.add_sequence_message(530, 180, 395, "4. Issue JWT Access Token (Verifier Validated)", stroke="#e67700", is_response=True, font_size=12)

    # Step 5: Client -> Resource Server
    d.add_sequence_message(180, 870, 465, "5. GET /api/v1/protected (Bearer JWT)", stroke="#2b8a3e", font_size=12)

    # Step 6: Resource Server -> Client
    d.add_sequence_message(870, 180, 525, "6. HTTP 200 OK (Protected Resource Payload)", stroke="#2b8a3e", is_response=True, font_size=12)

    # Security Summary Container at bottom
    d.add_container(60, 580, 920, 115, label="Why PKCE (Proof Key for Code Exchange) Is Essential", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")
    d.add_box(80, 625, 880, 55, "Prevents Authorization Code Interception Attacks on Public Clients", "Public clients (browsers, mobile apps) cannot safely store client secrets. PKCE dynamically validates authenticity via code_verifier.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=13)

    d.render("api-design-oauth2-pkce.png")

if __name__ == "__main__":
    generate_styles_comparison()
    generate_oauth2_pkce()
