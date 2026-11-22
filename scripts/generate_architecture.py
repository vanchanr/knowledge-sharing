#!/usr/bin/env python3
"""Generate perfected Software Architecture diagrams: Monolith vs Microservices & C4 Model."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_monolith_microservices():
    d = DiagramBuilder()
    d.add_header(
        "Architectural Evolution: Monolith vs Modular Monolith vs Microservices",
        "Trade-offs across Deployment Autonomy, Cognitive Overhead, Boundary Enforcement, and Data Consistency",
        x=40, y=20, w=1220, h=65
    )

    # 3 Columns Layout: Monolith (Left), Modular Monolith (Middle), Microservices (Right)
    # Column 1: Monolith (x=40..420, w=380)
    d.add_container(40, 105, 380, 520, label="1. Monolithic Architecture", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_w=240)

    d.add_box(60, 150, 340, 120, "Single Deployable Artifact (.war / .jar)", [
        "• UI, API, Domain Logic & Data Access in 1 unit.",
        "• Shared in-process memory; nanosecond calls.",
        "• Single git repo; simple local setup.",
        "• High coupling & hidden cross-domain calls."
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)
    d.add_arrow(230, 270, 230, 310, label="Direct JDBC / ORM Queries", stroke="#9c36b5", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    d.add_box(60, 310, 340, 60, "Single Shared Database (PostgreSQL / MySQL)", "Global tables, foreign keys & cross-domain joins", bg="#e5dbff", stroke="#7950f2", text_color="#7950f2", font_size=11)

    d.add_box(60, 385, 340, 225, "Monolith Architecture Trade-Offs", [
        "• Strengths:",
        "  - Extremely simple local development & debugging.",
        "  - ACID transactions across all entities out-of-the-box.",
        "  - Zero distributed network latency or partial failures.",
        "• Weaknesses:",
        "  - Entire app redeploys for single-line changes.",
        "  - Long build & test pipeline times as codebase grows.",
        "  - Single memory leak can crash the entire application.",
        "• Best For: Early MVPs, startups & teams < 15 engineers."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Column 2: Modular Monolith (x=460..840, w=380)
    d.add_container(460, 105, 380, 520, label="2. Modular Monolith Architecture", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=270)

    # 4 Modules Grid inside Single Artifact
    d.add_box(480, 150, 160, 52, "User Module", "Public API: UserService\nEncapsulated logic", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(660, 150, 160, 52, "Order Module", "Public API: OrderService\nEncapsulated logic", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(480, 212, 160, 52, "Payment Module", "Public API: PayService\nInternal entity access", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(660, 212, 160, 52, "Inventory Module", "Public API: StockService\nInternal entity access", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_arrow(650, 264, 650, 310, label="Strict Domain Schemas", stroke="#1971c2", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    d.add_box(480, 310, 340, 60, "Domain-Isolated DB Schemas (users, orders, pay)", "Zero cross-schema foreign keys; isolated domain tables", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(480, 385, 340, 225, "Modular Monolith Trade-Offs", [
        "• Strengths:",
        "  - Clean domain boundaries without network latency.",
        "  - Single CI/CD pipeline with low operational cost.",
        "  - Modules can be extracted to microservices if needed.",
        "• Weaknesses:",
        "  - Requires strict discipline (ArchUnit) to prevent leaks.",
        "  - Shares same CPU/RAM runtime failure domain.",
        "• Best For: Mid-to-large teams wanting high speed",
        "  without paying the distributed systems tax."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Column 3: Microservices (x=880..1260, w=380)
    d.add_container(880, 105, 380, 520, label="3. Distributed Microservices", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_w=250, badge_align="right")

    d.add_box(900, 150, 340, 42, "API Gateway / Service Mesh (Envoy / Kong)", "Reverse proxy, TLS termination, routing & rate limiting", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Services row
    d.add_box(900, 210, 165, 52, "User Microservice", "Node.js | Port 8081", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(1075, 210, 165, 52, "Order Microservice", "Spring Boot | Port 8082", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    d.add_arrow(982, 192, 982, 210, stroke="#1971c2")
    d.add_arrow(1157, 192, 1157, 210, stroke="#1971c2")

    # DBs row
    d.add_box(900, 275, 165, 42, "User DB (Mongo)", "Isolated data store", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(1075, 275, 165, 42, "Order DB (Postgres)", "Isolated data store", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_arrow(982, 262, 982, 275, stroke="#2b8a3e")
    d.add_arrow(1157, 262, 1157, 275, stroke="#2b8a3e")

    # Event Backbone
    d.add_box(900, 330, 340, 42, "Kafka Event Bus (Async Pub/Sub CDC)", "OrderCreated -> UserNotification | Eventual Consistency", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(982, 317, 982, 330, stroke="#2b8a3e")
    d.add_arrow(1157, 317, 1157, 330, stroke="#2b8a3e")

    d.add_box(900, 385, 340, 225, "Microservices Trade-Offs", [
        "• Strengths:",
        "  - Independent deployment cycles per autonomous squad.",
        "  - Polyglot technology stacks suited for specific domains.",
        "  - Fine-grained horizontal auto-scaling per service.",
        "• Weaknesses:",
        "  - High operational complexity (Kubernetes, OTel, CI/CD).",
        "  - Distributed data consistency (Sagas replace ACID).",
        "• Best For: Large engineering orgs (> 50-100 devs)."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Master Bottom Banner
    d.add_box(40, 640, 1220, 45, "Architecture Invariant: Choose microservices for organizational team autonomy — not raw performance. A modular monolith is the superior default.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("architecture-monolith-vs-microservices.png")

def generate_c4():
    d = DiagramBuilder()
    d.add_header(
        "The C4 Architecture Visualization Model (Zoom Levels 1 to 4)",
        "Hierarchical Architectural Abstraction from 10,000-Foot Context down to Class Code Structures",
        x=40, y=20, w=1220, h=65
    )

    # 4 Columns side-by-side: each w=285, gap=20
    # Level 1: System Context (x=40..325, w=285)
    d.add_container(40, 105, 285, 520, label="Level 1: System Context", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_w=200)

    d.add_box(55, 150, 255, 55, "Personal Banking Customer", "User accessing online bank accounts", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(182, 205, 182, 245, label="Uses Web/App", stroke="#1971c2", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    d.add_box(55, 245, 255, 65, "Internet Banking System", "Core software system enabling account\ntransfers, statements & bill payments", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_arrow(182, 310, 182, 350, label="Syncs Ledger / Sends", stroke="#495057", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    d.add_box(55, 350, 255, 55, "External Systems", "Mainframe Core Ledger & SendGrid Email", bg="#f1f3f5", stroke="#495057", text_color="#212529", font_size=11)

    d.add_box(55, 420, 255, 190, "Level 1 Context Details", [
        "• Scope: Entire software ecosystem.",
        "• Audience: Product owners & stakeholders.",
        "• Focus: High-level system boundaries",
        "  and user interactions with external systems.",
        "• Zero technical implementation details."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Level 2: Containers (x=345..630, w=285)
    d.add_container(345, 105, 285, 520, label="Level 2: Containers", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_w=170)

    d.add_box(360, 150, 255, 55, "Single-Page Application", "React / TypeScript client in browser", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(487, 205, 487, 245, label="JSON / HTTPS :443", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    d.add_box(360, 245, 255, 65, "Backend API Application", "Spring Boot / Java 21 REST container\nexecuting account transfer logic", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(487, 310, 487, 350, label="JDBC / SQL :5432", stroke="#2b8a3e", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    d.add_box(360, 350, 255, 55, "Database (Amazon Aurora)", "Relational PostgreSQL database cluster", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    d.add_box(360, 420, 255, 190, "Level 2 Container Details", [
        "• Scope: High-level shape of architecture.",
        "• Definition: Separately deployable units",
        "  (SPA, API container, Database).",
        "• Audience: Architects, DevOps & SREs.",
        "• Focus: High-level tech choices & protocols."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Level 3: Components (x=650..935, w=285)
    d.add_container(650, 105, 285, 520, label="Level 3: Components", stroke="#f59f00", badge_bg="#fff3bf", badge_stroke="#f59f00", label_color="#d9480f", badge_w=180)

    d.add_box(665, 150, 255, 45, "Accounts Controller", "Spring @RestController API endpoints", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_arrow(792, 195, 792, 225, stroke="#f59f00")

    d.add_box(665, 225, 255, 45, "Security Component", "Validates JWT tokens & roles", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_arrow(792, 270, 792, 300, stroke="#f59f00")

    d.add_box(665, 300, 255, 45, "Account Service", "@Service business transfer logic", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_arrow(792, 345, 792, 375, stroke="#2b8a3e")

    d.add_box(665, 375, 255, 40, "Account Repository", "Spring Data JPA persistence", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(665, 420, 255, 190, "Level 3 Component Details", [
        "• Scope: Decomposes a single container.",
        "• Definition: Structural building blocks",
        "  (Controllers, Services, Repositories).",
        "• Audience: Software engineers implementing",
        "  specific business feature capabilities."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Level 4: Code (x=955..1240, w=285)
    d.add_container(955, 105, 285, 520, label="Level 4: Code / Classes", stroke="#e03131", badge_bg="#ffe3e3", badge_stroke="#e03131", label_color="#c92a2a", badge_w=190, badge_align="right")

    d.add_box(970, 150, 255, 115, "public class AccountService", [
        "  @Transactional",
        "  public void transferMoney(",
        "    AccountId from, AccountId to,",
        "    BigDecimal amount) {",
        "    // double-entry debit/credit",
        "  }"
    ], bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a", font_size=11)
    d.add_arrow(1097, 265, 1097, 295, label="Persists", stroke="#e03131", label_offset_y=-10, label_bg="#ffffff", font_size=11)

    d.add_box(970, 295, 255, 100, "public record AccountEntity", [
        "  Long id,",
        "  String accountNumber,",
        "  BigDecimal balance,",
        "  Currency currency"
    ], bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a", font_size=11)

    d.add_box(970, 420, 255, 190, "Level 4 Code Details", [
        "• Scope: Zooming into classes & code.",
        "• Recommendation: Usually omitted or",
        "  generated on-demand via IDE PlantUML.",
        "• Audience: Developers writing unit tests",
        "  and debugging exact implementation logic."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # Master Bottom Banner
    d.add_box(40, 640, 1200, 45, "C4 Model Invariant: Architectural maps have zoom levels. Context (Level 1) aligns leadership; Containers & Components (Levels 2-3) guide engineering.", bg="#ffffff", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    d.render("architecture-c4-model-overview.png")

if __name__ == "__main__":
    generate_monolith_microservices()
    generate_c4()
