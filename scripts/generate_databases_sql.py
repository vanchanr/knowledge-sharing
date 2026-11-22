#!/usr/bin/env python3
"""Generate perfected SQL & Database diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_sql_joins():
    d = DiagramBuilder()
    d.add_header(
        "SQL Joins & Set Operations Visual Map",
        "Visual Guide to Relational Joins, Cartesian Products, and Recursive Hierarchies",
        x=40, y=25, w=1140, h=65
    )

    # 3x2 Grid: panels 360x250
    # ROW 1 (y=110)
    # 1. INNER JOIN
    d.add_container(40, 110, 360, 250, label="INNER JOIN", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")
    d.add_box(65, 155, 95, 60, "Table A\n(Orders)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(165, 155, 110, 60, "A ∩ B\n(Matched)", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(280, 155, 95, 60, "Table B\n(Users)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(60, 230, 320, 110, "Only matching rows in both tables", [
        "SELECT * FROM Orders O",
        "INNER JOIN Customers C",
        "  ON O.cust_id = C.id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    # 2. LEFT OUTER JOIN
    d.add_container(430, 110, 360, 250, label="LEFT OUTER JOIN", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")
    d.add_box(455, 155, 150, 60, "All of Table A\n(Preserved)", bg="#d3f9d8", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(615, 155, 150, 60, "Matched Table B\n(or NULL)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(450, 230, 320, 110, "All A rows + matching B (or NULL)", [
        "SELECT * FROM Users U",
        "LEFT JOIN Orders O",
        "  ON U.id = O.user_id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#2b8a3e", font_size=12)

    # 3. RIGHT OUTER JOIN
    d.add_container(820, 110, 360, 250, label="RIGHT OUTER JOIN", stroke="#f59f00", badge_bg="#fff3bf", badge_stroke="#f59f00", label_color="#d9480f")
    d.add_box(845, 155, 150, 60, "Matched Table A\n(or NULL)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(1005, 155, 150, 60, "All of Table B\n(Preserved)", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_box(840, 230, 320, 110, "All B rows + matching A (or NULL)", [
        "SELECT * FROM Employees E",
        "RIGHT JOIN Departments D",
        "  ON E.dept_id = D.id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#d9480f", font_size=12)

    # ROW 2 (y=380)
    # 4. FULL OUTER JOIN
    d.add_container(40, 380, 360, 250, label="FULL OUTER JOIN", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")
    d.add_box(65, 425, 150, 60, "All Table A\n(Preserved)", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(225, 425, 150, 60, "All Table B\n(Preserved)", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(60, 500, 320, 110, "Union of all matching & unmatching rows", [
        "SELECT * FROM A",
        "FULL OUTER JOIN B",
        "  ON A.id = B.id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#9c36b5", font_size=12)

    # 5. CROSS JOIN (Cartesian)
    d.add_container(430, 380, 360, 250, label="CROSS JOIN (Cartesian)", stroke="#495057", badge_bg="#f1f3f5", badge_stroke="#495057", label_color="#212529")
    d.add_box(455, 425, 110, 60, "Table A\n(M rows)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(655, 425, 110, 60, "Table B\n(N rows)", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_arrow(565, 455, 655, 455, label="M × N", stroke="#495057", label_offset_y=-18, font_size=11)
    d.add_box(450, 500, 320, 110, "Cartesian product: pairs every row", [
        "SELECT * FROM Colors",
        "CROSS JOIN Sizes;",
        "-- Produces M * N combinations"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#212529", font_size=12)

    # 6. SELF JOIN (Hierarchy)
    d.add_container(820, 380, 360, 250, label="SELF JOIN (Hierarchical)", stroke="#c92a2a", badge_bg="#ffe3e3", badge_stroke="#c92a2a", label_color="#c92a2a")
    d.add_box(840, 425, 120, 60, "Employee (E)", "id, mgr_id", bg="#fff5f5", stroke="#c92a2a", text_color="#c92a2a", font_size=12)
    d.add_box(1040, 425, 120, 60, "Manager (M)", "id, name", bg="#fff5f5", stroke="#c92a2a", text_color="#c92a2a", font_size=12)
    d.add_arrow(960, 455, 1040, 455, label="mgr = id", stroke="#c92a2a", label_offset_y=-18, font_size=11)
    d.add_box(840, 500, 320, 110, "Joins table onto itself for tree graphs", [
        "SELECT E.name, M.name AS mgr",
        "FROM Employees E",
        "LEFT JOIN Employees M ON E.mgr_id = M.id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#c92a2a", font_size=12)

    d.render("sql-joins-visual-map.png")

def generate_btree_index():
    d = DiagramBuilder()
    d.add_header(
        "Database B+ Tree Index Architecture & Search Path",
        "Balanced Multi-Way Search Tree, Doubly-Linked Leaves, and Heap Row Lookup",
        x=40, y=25, w=1100, h=65
    )

    # Level 0: Root Node
    d.add_box(440, 115, 260, 60, "Root Page [50]", "Keys < 50 (Left) | Keys >= 50 (Right)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")

    # Level 1: Internal Nodes
    d.add_box(180, 240, 270, 60, "Internal Page [20 | 35]", "< 20 | 20..34 | >= 35", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(690, 240, 270, 60, "Internal Page [65 | 80]", "< 65 | 65..79 | >= 80", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Root -> Level 1 Arrows (with label_bg="#ffffff" to prevent line collision)
    d.add_arrow(490, 175, 340, 240, label="key < 50", stroke="#1971c2", label_offset_y=-26, label_bg="#ffffff")
    d.add_arrow(650, 175, 800, 240, label="key >= 50", stroke="#1971c2", label_offset_y=-26, label_bg="#ffffff")

    # Level 2: Leaf Nodes (Target Key: 25)
    d.add_box(50, 360, 260, 65, "Leaf Page [5, 12, 18]", "Range [0 .. 19]", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")
    d.add_box(440, 360, 260, 65, "Leaf Page [20, 25, 32]", "Target key: 25 -> FOUND", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")
    d.add_box(830, 360, 260, 65, "Leaf Page [35, 41, 48]", "Range [35 .. 49]", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f")

    # Internal -> Leaves Arrows (with label_bg="#ffffff")
    d.add_arrow(230, 300, 170, 360, label="< 20", stroke="#2b8a3e", label_offset_y=-24, label_bg="#ffffff", font_size=11)
    d.add_arrow(315, 300, 480, 360, label="20..34", stroke="#2b8a3e", label_offset_y=-24, label_bg="#ffffff", font_size=11)
    d.add_arrow(400, 300, 850, 360, label=">= 35", stroke="#2b8a3e", label_offset_y=-24, label_bg="#ffffff", font_size=11)

    # Doubly Linked List Arrows between Leaves (130px gaps)
    d.add_arrow(310, 392, 440, 392, label="next", stroke="#f59f00", label_offset_y=-18, font_size=11)
    d.add_arrow(700, 392, 830, 392, label="next", stroke="#f59f00", label_offset_y=-18, font_size=11)

    # Row Pointer to Heap
    d.add_arrow(570, 425, 570, 485, stroke="#9c36b5")
    d.add_text(585, 445, "Row Pointer (RID / TID)", font_size=11, stroke="#9c36b5", align="left", w=160)

    # Level 3: Table Heap Container
    d.add_container(50, 485, 1040, 150, label="Table Heap Storage (Actual Physical Row Record on Disk)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")
    d.add_box(70, 525, 1000, 85, "Row Record [ID: 25 | Name: 'Alice' | Email: 'alice@domain.com' | Status: 'ACTIVE']", [
        "• O(log N) page reads locate leaf page in index; 1 random I/O read retrieves row record from Table Heap.",
        "• Covering Index Optimization: When all queried SELECT columns exist in index keys, Table Heap lookup is bypassed."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#9c36b5", font_size=12)

    d.render("database-btree-index-search.png")

if __name__ == "__main__":
    generate_sql_joins()
    generate_btree_index()
