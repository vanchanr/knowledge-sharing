#!/usr/bin/env python3
"""Generate perfected SQL & Database diagrams with zero defects."""
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
    d.add_container(40, 110, 360, 250, label="INNER JOIN", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2", badge_align="left")
    d.add_box(65, 155, 95, 60, "Table A\n(Orders)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(165, 155, 110, 60, "A ∩ B\n(Matched)", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(280, 155, 95, 60, "Table B\n(Users)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(60, 230, 320, 110, "Only matching rows in both tables", [
        "SELECT * FROM Orders O",
        "INNER JOIN Customers C",
        "  ON O.cust_id = C.id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#1971c2", font_size=12)

    # 2. LEFT OUTER JOIN
    d.add_container(430, 110, 360, 250, label="LEFT OUTER JOIN", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e", badge_align="left")
    d.add_box(455, 155, 150, 60, "All of Table A\n(Preserved)", bg="#d3f9d8", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(615, 155, 150, 60, "Matched Table B\n(or NULL)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(450, 230, 320, 110, "All A rows + matching B (or NULL)", [
        "SELECT * FROM Users U",
        "LEFT JOIN Orders O",
        "  ON U.id = O.user_id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#2b8a3e", font_size=12)

    # 3. RIGHT OUTER JOIN
    d.add_container(820, 110, 360, 250, label="RIGHT OUTER JOIN", stroke="#f59f00", badge_bg="#fff3bf", badge_stroke="#f59f00", label_color="#d9480f", badge_align="left")
    d.add_box(845, 155, 150, 60, "Matched Table A\n(or NULL)", bg="#ffffff", stroke="#adb5bd", text_color="#495057", font_size=12)
    d.add_box(1005, 155, 150, 60, "All of Table B\n(Preserved)", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_box(840, 230, 320, 110, "All B rows + matching A (or NULL)", [
        "SELECT * FROM Employees E",
        "RIGHT JOIN Departments D",
        "  ON E.dept_id = D.id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#d9480f", font_size=12)

    # ROW 2 (y=380)
    # 4. FULL OUTER JOIN
    d.add_container(40, 380, 360, 250, label="FULL OUTER JOIN", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_align="left")
    d.add_box(65, 425, 150, 60, "All Table A\n(Preserved)", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(225, 425, 150, 60, "All Table B\n(Preserved)", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)
    d.add_box(60, 500, 320, 110, "Union of all matching & unmatching rows", [
        "SELECT * FROM A",
        "FULL OUTER JOIN B",
        "  ON A.id = B.id;"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#9c36b5", font_size=12)

    # 5. CROSS JOIN (Cartesian)
    d.add_container(430, 380, 360, 250, label="CROSS JOIN (Cartesian)", stroke="#495057", badge_bg="#f1f3f5", badge_stroke="#495057", label_color="#212529", badge_align="left")
    d.add_box(455, 425, 110, 60, "Table A\n(M rows)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(655, 425, 110, 60, "Table B\n(N rows)", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_arrow(565, 455, 655, 455, stroke="#495057")
    d.add_text(585, 435, "M × N", stroke="#495057", font_size=11, align="left", w=50)
    d.add_box(450, 500, 320, 110, "Cartesian product: pairs every row", [
        "SELECT * FROM Colors",
        "CROSS JOIN Sizes;",
        "-- Produces M * N combinations"
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#212529", font_size=12)

    # 6. SELF JOIN (Hierarchy)
    d.add_container(820, 380, 360, 250, label="SELF JOIN (Hierarchical)", stroke="#c92a2a", badge_bg="#ffe3e3", badge_stroke="#c92a2a", label_color="#c92a2a", badge_align="left")
    d.add_box(840, 425, 120, 60, "Employee (E)", "id, mgr_id", bg="#fff5f5", stroke="#c92a2a", text_color="#c92a2a", font_size=12)
    d.add_box(1040, 425, 120, 60, "Manager (M)", "id, name", bg="#fff5f5", stroke="#c92a2a", text_color="#c92a2a", font_size=12)
    d.add_arrow(960, 455, 1040, 455, stroke="#c92a2a")
    d.add_text(970, 435, "mgr = id", stroke="#c92a2a", font_size=11, align="left", w=60)
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
        x=40, y=25, w=1140, h=65
    )

    # Level 0: Root Node (Centered)
    d.add_box(460, 110, 260, 55, "Root Page [50]", "Keys < 50 (Left) | Keys >= 50 (Right)", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2")

    # Level 1: Internal Nodes (Balanced Left and Right)
    d.add_box(160, 215, 270, 55, "Internal Page [20 | 35]", "< 20 | 20..34 | >= 35", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")
    d.add_box(750, 215, 270, 55, "Internal Page [65 | 80]", "< 65 | 65..79 | >= 80", bg="#ebfbee", stroke="#2b8a3e", text_color="#2b8a3e")

    # Root -> Level 1 Branch Arrows
    d.add_arrow(510, 165, 330, 215, stroke="#1971c2")
    d.add_text(370, 175, "key < 50", stroke="#1971c2", font_size=11, align="left", w=70)

    d.add_arrow(670, 165, 850, 215, stroke="#1971c2")
    d.add_text(740, 175, "key >= 50", stroke="#1971c2", font_size=11, align="left", w=75)

    # Level 2: 6 Leaf Pages across the bottom (y=325..385)
    # Left Subtree Leaves:
    # Leaf 1: < 20
    d.add_box(40, 325, 170, 60, "Leaf Page [5, 12, 18]", "Range [0 .. 19]", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)
    # Leaf 2: 20..34 (TARGET KEY: 25 FOUND!)
    d.add_box(230, 325, 180, 60, "Leaf Page [20, 25, 32]", "Target: 25 -> FOUND", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=11)
    # Leaf 3: 35..49
    d.add_box(430, 325, 170, 60, "Leaf Page [35, 41, 48]", "Range [35 .. 49]", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)

    # Right Subtree Leaves:
    # Leaf 4: 50..64
    d.add_box(620, 325, 165, 60, "Leaf Page [50, 58, 62]", "Range [50 .. 64]", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)
    # Leaf 5: 65..79
    d.add_box(805, 325, 165, 60, "Leaf Page [65, 71, 78]", "Range [65 .. 79]", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)
    # Leaf 6: >= 80
    d.add_box(990, 325, 165, 60, "Leaf Page [80, 88, 95]", "Range [80 .. 99]", bg="#f8f9fa", stroke="#495057", text_color="#212529", font_size=11)

    # Left Internal Node -> Left Leaves Arrows (Straight, no awkward crossing!)
    d.add_arrow(200, 270, 125, 325, stroke="#2b8a3e")
    d.add_text(130, 285, "< 20", stroke="#2b8a3e", font_size=10, align="left", w=40)

    d.add_arrow(295, 270, 320, 325, stroke="#d9480f", stroke_width=2)
    d.add_text(315, 285, "20..34 (Path)", stroke="#d9480f", font_size=10, align="left", w=80)

    d.add_arrow(390, 270, 485, 325, stroke="#2b8a3e")
    d.add_text(450, 285, ">= 35", stroke="#2b8a3e", font_size=10, align="left", w=45)

    # Right Internal Node -> Right Leaves Arrows
    d.add_arrow(790, 270, 700, 325, stroke="#2b8a3e")
    d.add_text(710, 285, "< 65", stroke="#2b8a3e", font_size=10, align="left", w=40)

    d.add_arrow(885, 270, 885, 325, stroke="#2b8a3e")
    d.add_text(895, 285, "65..79", stroke="#2b8a3e", font_size=10, align="left", w=50)

    d.add_arrow(980, 270, 1050, 325, stroke="#2b8a3e")
    d.add_text(1025, 285, ">= 80", stroke="#2b8a3e", font_size=10, align="left", w=45)

    # Doubly Linked List Arrows connecting leaves horizontally for O(N) range scans:
    d.add_arrow(210, 355, 230, 355, stroke="#f59f00")
    d.add_arrow(410, 355, 430, 355, stroke="#f59f00")
    d.add_arrow(600, 355, 620, 355, stroke="#f59f00")
    d.add_arrow(785, 355, 805, 355, stroke="#f59f00")
    d.add_arrow(970, 355, 990, 355, stroke="#f59f00")

    # Row Pointer to Heap (from Leaf Page [20, 25, 32])
    d.add_arrow(320, 385, 320, 465, stroke="#9c36b5", stroke_width=2)
    d.add_text(330, 415, "Row Pointer (RID / TID)", font_size=11, stroke="#9c36b5", align="left", w=160)

    # Level 3: Table Heap Container
    d.add_container(40, 465, 1140, 140, label="Table Heap Storage (Actual Physical Row Record on Disk)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5", badge_align="left")
    d.add_box(60, 505, 1100, 85, "Row Record [ID: 25 | Name: 'Alice' | Email: 'alice@domain.com' | Status: 'ACTIVE']", [
        "• O(log N) tree traversal reads pages from disk buffer pool; 1 random pointer read retrieves physical row record from Table Heap.",
        "• Covering Index Optimization: If all SELECT columns exist in index keys (e.g. SELECT ID), Table Heap lookup is completely bypassed."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#9c36b5", font_size=12)

    # Bottom Invariant Bar
    d.add_box(40, 620, 1140, 45, "B+ Tree Architectural Invariant", [
        "All data values reside exclusively in the leaf tier at uniform depth; leaves are doubly linked to enable instantaneous range scans."
    ], bg="#f8f9fa", stroke="#dee2e6", text_color="#495057", font_size=12)

    d.render("database-btree-index-search.png")

if __name__ == "__main__":
    generate_sql_joins()
    generate_btree_index()
