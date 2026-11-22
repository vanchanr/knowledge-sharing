#!/usr/bin/env python3
"""Generate perfected Spring Boot diagrams."""
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

    # Client (ends at 180)
    d.add_box(40, 225, 140, 75, "Client Browser", [
        "Web / Mobile App",
        "GET /api/users/1"
    ], bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # DispatcherServlet (Center Front Controller: 260..480, w=220)
    d.add_box(260, 195, 220, 140, "DispatcherServlet", [
        "Front Controller Hub",
        "",
        "• Resolves HandlerMapping",
        "• Delegates to HandlerAdapter",
        "• Coordinates Interceptors",
        "• Serializes Output via Converters"
    ], bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=13)

    # Top Entity: HandlerMapping (260..480, y=95..150)
    d.add_box(260, 95, 220, 55, "HandlerMapping", "Matches URL route to target @RequestMapping", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)

    # Up arrow to HandlerMapping (text placed to the right in open space)
    d.add_arrow(370, 195, 370, 150, stroke="#2b8a3e")
    d.add_text(380, 165, "Get Handler", font_size=11, stroke="#2b8a3e", align="left", w=100)

    # Client -> DispatcherServlet (gap = 80px)
    d.add_arrow(180, 245, 260, 245, label="1. HTTP Req", stroke="#1971c2", label_offset_y=-18, font_size=11)

    # HandlerAdapter (580..760, gap = 100px)
    d.add_box(580, 205, 180, 65, "HandlerAdapter", "Reflectively invokes target controller method", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_arrow(480, 237, 580, 237, label="2. Invoke", stroke="#f59f00", label_offset_y=-18, font_size=11)

    # Controller Layer (860..1100, gap = 100px)
    d.add_box(860, 205, 240, 65, "@RestController", "Extracts @PathVariable, calls Service", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_arrow(760, 237, 860, 237, label="3. Dispatch", stroke="#9c36b5", label_offset_y=-18, font_size=11)

    # Service Layer
    d.add_box(860, 305, 240, 60, "@Service (Business Logic)", "Transactional boundary (@Transactional)", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_arrow(980, 270, 980, 305, stroke="#9c36b5")

    # Repository Layer
    d.add_box(860, 395, 240, 60, "@Repository (Spring Data)", "Hibernate / JDBC query to Database", bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_arrow(980, 365, 980, 395, stroke="#9c36b5")

    # HttpMessageConverter (580..760, y=335)
    d.add_box(580, 335, 180, 70, "HttpMessageConverter", "Jackson / JSON Serialization", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=12)

    # Return DTO from Controller to Converter
    d.add_arrow(860, 255, 760, 345, label="Return DTO", stroke="#495057", stroke_style="dashed", label_offset_y=-24, font_size=11)

    # Converter to DispatcherServlet (label placed below arrow line)
    d.add_arrow(580, 370, 480, 330, label="JSON Bytes", stroke="#495057", stroke_style="dashed", label_offset_y=12, font_size=11)

    # DispatcherServlet -> Client (Return HTTP 200)
    d.add_arrow(260, 280, 180, 280, label="7. 200 OK (JSON)", stroke="#1971c2", stroke_style="dashed", label_offset_y=-18, font_size=11)

    # Bottom Architectural Notes
    d.add_box(40, 480, 1060, 85, "Spring MVC Architectural Principles", [
        "• Front Controller Pattern: A single centralized servlet (DispatcherServlet) manages the entire request-response lifecycle.",
        "• Separation of Concerns: HandlerMapping resolves routes, HandlerAdapter executes methods, and HttpMessageConverter serializes payloads.",
        "• View Resolution vs REST: In @RestController, @ResponseBody signals Jackson to write directly into response stream, bypassing ViewResolvers."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("spring-boot-mvc-lifecycle.png")

def generate_security_filterchain():
    d = DiagramBuilder()
    d.add_header(
        "Spring Security Filter Chain Architecture",
        "DelegatingFilterProxy, FilterChainProxy, and Ordered Security Filters",
        x=40, y=25, w=1160, h=65
    )

    # Master Container encompassing Web Bridge + SecurityFilterChain Flow
    d.add_container(40, 110, 1160, 520, label="Spring Security Architecture: Web Integration & SecurityFilterChain Flow", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # 1. Left Lane: Servlet Container to Spring Bridge (60..430, w=370)
    d.add_box(60, 155, 370, 50, "Incoming HTTP Request", "URL: /api/protected (Header: Authorization Bearer ...)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # DelegatingFilterProxy
    d.add_box(60, 240, 370, 75, "DelegatingFilterProxy", [
        "Standard javax.servlet.Filter in Servlet container",
        "Delegates to Spring bean 'springSecurityFilterChain'"
    ], bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=12)
    d.add_arrow(245, 205, 245, 240, stroke="#1971c2")

    # FilterChainProxy
    d.add_box(60, 350, 370, 95, "FilterChainProxy (Spring Security Master)", [
        "Central entry point for all Spring Security processing",
        "• Matches request against SecurityFilterChain rules",
        "• Cleans up SecurityContextHolder at request end",
        "• Defends against attacks via StrictHttpFirewall"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_arrow(245, 315, 245, 350, stroke="#f59f00")

    # DispatcherServlet at bottom left
    d.add_box(60, 485, 370, 65, "DispatcherServlet (Spring MVC Controller)", "Reached only when ALL security filters allow request through", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)

    # 2. Right Lane: SecurityFilterChain Ordered Filter Stack (540..1160, w=620)
    filters = [
        ("1. SecurityContextHolderFilter", "Populates SecurityContext from SecurityContextRepository (session/token)"),
        ("2. CorsFilter & CsrfFilter", "Evaluates CORS preflight headers & validates CSRF tokens (for stateful web)"),
        ("3. BearerTokenAuth / UsernamePasswordAuthFilter", "Extracts Bearer JWT, validates claims/signature, sets Authentication"),
        ("4. ExceptionTranslationFilter", "Catches AuthenticationException (returns 401) and AccessDeniedException (returns 403)"),
        ("5. AuthorizationFilter (FilterSecurityInterceptor)", "Enforces method/URL access rules (.hasRole('ADMIN'), .authenticated())")
    ]

    curr_y = 155
    for title, sub in filters:
        d.add_box(540, curr_y, 620, 52, title, sub, bg="#fff5f5", stroke="#e03131", text_color="#c92a2a", font_size=12)
        curr_y += 62

    # Clean Open-Space Arrows between Left and Right Lanes (110px gap between 430 and 540)
    # Entry: FilterChainProxy (430, 397) -> Filter 1 (540, 181)
    d.add_arrow(430, 397, 540, 181, label="Executes Chain", stroke="#f59f00", label_offset_y=-24, font_size=11)

    # Exit: Filter 5 (540, 430) -> DispatcherServlet (430, 517)
    d.add_arrow(540, 430, 430, 517, label="Authorized -> Proceed", stroke="#2b8a3e", label_offset_y=-24, font_size=11)

    # Security Summary note
    d.add_box(540, 475, 620, 75, "Spring Security Filter Chain Invariants", [
        "• Filter Execution Order: Filters execute strictly in sequential order (1 -> 2 -> 3 -> 4 -> 5).",
        "• Short-Circuiting: If authentication fails, ExceptionTranslationFilter halts chain and returns 401 immediately."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("spring-boot-security-filterchain.png")

if __name__ == "__main__":
    generate_mvc_lifecycle()
    generate_security_filterchain()
