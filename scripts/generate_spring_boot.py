#!/usr/bin/env python3
"""Generate perfected Spring Boot diagrams with zero defects."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_mvc_lifecycle():
    d = DiagramBuilder()
    d.add_header(
        "Spring MVC Request Lifecycle & Architecture",
        "Front Controller Pattern, Handler Mapping, Adapter Dispatch, and HttpMessageConverter",
        x=40, y=25, w=1140, h=65
    )

    # Client (40..150, w=110)
    d.add_box(40, 225, 110, 75, "Client Browser", [
        "Web / Mobile App",
        "GET /api/users/1"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # DispatcherServlet (Center Front Controller: 310..530, w=220)
    d.add_box(310, 195, 220, 140, "DispatcherServlet", [
        "Front Controller Hub",
        "",
        "• Resolves HandlerMapping",
        "• Delegates to HandlerAdapter",
        "• Coordinates Interceptors",
        "• Serializes Output via Converters"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=13)

    # Top Entity: HandlerMapping (310..530, y=95..150)
    d.add_box(310, 95, 220, 55, "HandlerMapping", "Matches URL route to target @RequestMapping", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)

    # Up arrow to HandlerMapping
    d.add_arrow(420, 195, 420, 150, stroke="#2b8a3e")
    d.add_text(430, 165, "Get Handler", font_size=11, stroke="#2b8a3e", align="left", w=90)

    # Client -> DispatcherServlet (160px gap from 150 to 310!)
    d.add_arrow(150, 245, 310, 245, stroke="#1971c2")
    d.add_text(175, 225, "1. HTTP Req", stroke="#1971c2", font_size=11, align="left", w=75)

    # DispatcherServlet -> Client (Return HTTP 200)
    d.add_arrow(310, 280, 150, 280, stroke="#1971c2", stroke_style="dashed")
    d.add_text(175, 285, "7. 200 OK (JSON)", stroke="#1971c2", font_size=10, align="left", w=90)

    # HandlerAdapter (620..800, gap = 90px from 530 to 620)
    d.add_box(620, 205, 180, 65, "HandlerAdapter", "Reflectively invokes target controller method", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_arrow(530, 237, 620, 237, stroke="#f59f00")
    d.add_text(545, 217, "2. Invoke", stroke="#f59f00", font_size=11, align="left", w=70)

    # Controller Layer (890..1130, gap = 90px)
    d.add_box(890, 205, 240, 65, "@RestController", "Extracts @PathVariable, calls Service", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_arrow(800, 237, 890, 237, stroke="#9c36b5")
    d.add_text(815, 217, "3. Dispatch", stroke="#9c36b5", font_size=11, align="left", w=75)

    # Service Layer
    d.add_box(890, 305, 240, 60, "@Service (Business Logic)", "Transactional boundary (@Transactional)", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_arrow(1010, 270, 1010, 305, stroke="#9c36b5")

    # Repository Layer
    d.add_box(890, 395, 240, 60, "@Repository (Spring Data)", "Hibernate / JDBC query to Database", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_arrow(1010, 365, 1010, 395, stroke="#9c36b5")

    # HttpMessageConverter (620..800, y=340)
    d.add_box(620, 340, 180, 70, "HttpMessageConverter", "Jackson / JSON Serialization", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=12)

    # Return DTO from Controller to Converter (clean open space above diagonal line)
    d.add_arrow(890, 260, 800, 355, stroke="#495057", stroke_style="dashed")
    d.add_text(815, 260, "Return DTO", stroke="#495057", font_size=11, align="left", w=75)

    # Converter to DispatcherServlet
    d.add_arrow(620, 375, 530, 325, stroke="#495057", stroke_style="dashed")
    d.add_text(540, 360, "JSON Bytes", stroke="#495057", font_size=11, align="left", w=75)

    # Bottom Architectural Notes
    d.add_box(40, 485, 1090, 85, "Spring MVC Architectural Principles", [
        "• Front Controller Pattern: A single centralized servlet (DispatcherServlet) manages the entire request-response lifecycle.",
        "• Separation of Concerns: HandlerMapping resolves routes, HandlerAdapter executes methods, and HttpMessageConverter serializes payloads.",
        "• View Resolution vs REST: In @RestController, @ResponseBody signals Jackson to write directly into response stream, bypassing ViewResolvers."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=12)

    d.render("spring-boot-mvc-lifecycle.png")


def generate_security_filterchain():
    d = DiagramBuilder()
    d.add_header(
        "Spring Security Filter Chain Architecture",
        "DelegatingFilterProxy, FilterChainProxy, and Ordered Security Filters",
        x=40, y=25, w=1160, h=65
    )

    # Master Container with left-aligned badge
    d.add_container(40, 110, 1160, 520, label="Spring Security Architecture: Web Integration & SecurityFilterChain Flow", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_align="left")

    # 1. Left Lane: Servlet Container to Spring Bridge (60..410, w=350)
    d.add_box(60, 155, 350, 50, "Incoming HTTP Request", "URL: /api/protected (Header: Authorization Bearer ...)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # DelegatingFilterProxy
    d.add_box(60, 240, 350, 75, "DelegatingFilterProxy", [
        "Standard javax.servlet.Filter in Servlet container",
        "Delegates to Spring bean 'springSecurityFilterChain'"
    ], bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=12)
    d.add_arrow(235, 205, 235, 240, stroke="#1971c2")

    # FilterChainProxy
    d.add_box(60, 350, 350, 95, "FilterChainProxy (Spring Security Master)", [
        "Central entry point for all Spring Security processing",
        "• Matches request against SecurityFilterChain rules",
        "• Cleans up SecurityContextHolder at request end",
        "• Defends against attacks via StrictHttpFirewall"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_arrow(235, 315, 235, 350, stroke="#f59f00")

    # DispatcherServlet at bottom left
    d.add_box(60, 485, 350, 65, "DispatcherServlet (Spring MVC Controller)", "Reached only when ALL security filters allow request through", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)

    # 2. Right Lane: SecurityFilterChain Ordered Filter Stack (570..1160, w=590)
    filters = [
        ("1. SecurityContextHolderFilter", "Populates SecurityContext from SecurityContextRepository (session/token)"),
        ("2. CorsFilter & CsrfFilter", "Evaluates CORS preflight headers & validates CSRF tokens (for stateful web)"),
        ("3. BearerTokenAuth / UsernamePasswordAuthFilter", "Extracts Bearer JWT, validates claims/signature, sets Authentication"),
        ("4. ExceptionTranslationFilter", "Catches AuthenticationException (returns 401) and AccessDeniedException (returns 403)"),
        ("5. AuthorizationFilter (FilterSecurityInterceptor)", "Enforces method/URL access rules (.hasRole('ADMIN'), .authenticated())")
    ]

    curr_y = 155
    for title, sub in filters:
        d.add_box(570, curr_y, 570, 52, title, sub, bg="#fff5f5", stroke="#e03131", text_color="#c92a2a", font_size=12)
        curr_y += 62

    # Clean Open-Space Arrows between Left and Right Lanes (160px gap between 410 and 570!)
    # Entry: FilterChainProxy (410, 397) -> Filter 1 (570, 181)
    d.add_arrow(410, 397, 570, 181, stroke="#f59f00")
    d.add_text(440, 240, "Executes Chain", stroke="#f59f00", font_size=11, align="left", w=95)

    # Exit: Filter 5 (570, 430) -> DispatcherServlet (410, 517)
    d.add_arrow(570, 430, 410, 517, stroke="#2b8a3e")
    d.add_text(435, 450, "Authorized -> Proceed", stroke="#2b8a3e", font_size=11, align="left", w=130)

    # Security Summary note
    d.add_box(570, 475, 570, 75, "Spring Security Filter Chain Invariants", [
        "• Filter Execution Order: Filters execute strictly in sequential order (1 -> 2 -> 3 -> 4 -> 5).",
        "• Short-Circuiting: If authentication fails, ExceptionTranslationFilter halts chain and returns 401 immediately."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("spring-boot-security-filterchain.png")

if __name__ == "__main__":
    generate_mvc_lifecycle()
    generate_security_filterchain()
