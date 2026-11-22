#!/usr/bin/env python3
"""
Excalidraw Diagram Generator Engine (Enhanced V2)
Generates pristine, professional Excalidraw diagrams and renders them to high-res PNGs.
Designed for high legibility, proper sequence lifelines, zero text-border collisions, and publication-ready architecture diagrams.
"""

import json
import uuid
import time
import subprocess
import os

DIAGRAMS_DIR = "/data/data/com.termux/files/home/knowledge-sharing/assets/diagrams"
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

class DiagramBuilder:
    def __init__(self, bg_color="#ffffff"):
        self.elements = []
        self.bg_color = bg_color

    def _base_element(self, el_type, x, y, w, h, stroke="#1e1e1e", bg="transparent", fill="solid", stroke_width=2, stroke_style="solid", roughness=0, roundness=3):
        return {
            "id": str(uuid.uuid4())[:8],
            "type": el_type,
            "x": round(x, 1),
            "y": round(y, 1),
            "width": max(1, round(w, 1)),
            "height": max(1, round(h, 1)),
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": stroke_width,
            "strokeStyle": stroke_style,
            "roughness": roughness,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": roundness} if roundness else None,
            "seed": int(time.time() * 1000) % 1000000,
            "version": 1,
            "versionNonce": 1,
            "isDeleted": False,
            "boundElements": None,
            "updated": int(time.time() * 1000),
            "link": None,
            "locked": False
        }

    def add_box(self, x, y, w, h, title, subtitle=None, bg="#e7f5ff", stroke="#1971c2", text_color=None, font_size=15, roundness=3, roughness=0):
        """Draws a card/box with centered title and optional subtitle lines."""
        box = self._base_element("rectangle", x, y, w, h, stroke=stroke, bg=bg, roundness=roundness, roughness=roughness)
        self.elements.append(box)

        t_color = text_color if text_color else stroke

        if subtitle:
            sub_lines = subtitle if isinstance(subtitle, list) else [subtitle]
            total_lines = 1 + len(sub_lines)
            line_height = font_size + 6
            start_y = y + (h - (total_lines * line_height)) // 2

            # Title
            t = self._base_element("text", x + 8, start_y, w - 16, line_height, stroke=t_color)
            t.update({
                "text": title,
                "fontSize": font_size,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(t)

            # Subtitle lines
            curr_y = start_y + line_height
            for s_line in sub_lines:
                if not s_line or not s_line.strip():
                    curr_y += line_height // 2
                    continue
                is_bullet = s_line.strip().startswith("•") or s_line.strip().startswith("-")
                s_align = "left" if is_bullet else "center"
                s_x = x + 24 if is_bullet else x + 8
                s_w = w - 40 if is_bullet else w - 16

                s = self._base_element("text", s_x, curr_y, s_w, line_height - 4, stroke="#495057")
                s.update({
                    "text": s_line,
                    "fontSize": max(11, font_size - 4),
                    "fontFamily": 1,
                    "textAlign": s_align
                })
                self.elements.append(s)
                curr_y += line_height - 2
        else:
            t = self._base_element("text", x + 8, y + (h - font_size) // 2 - 2, w - 16, font_size + 6, stroke=t_color)
            t.update({
                "text": title,
                "fontSize": font_size,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(t)

        return box["id"]

    def add_container(self, x, y, w, h, label=None, stroke="#adb5bd", stroke_style="dashed", bg="transparent", badge_bg="#f1f3f5", badge_stroke=None, label_color="#343a40", badge_w=None, badge_align="left"):
        """Draws a group container boundary with an interior header badge to completely eliminate border clipping."""
        c = self._base_element("rectangle", x, y, w, h, stroke=stroke, bg=bg, stroke_width=2, stroke_style=stroke_style, roughness=0, roundness=2)
        self.elements.append(c)

        if label:
            if badge_w is None:
                badge_w = min(w - 24, max(140, len(label) * 9 + 30))
            badge_h = 28
            if badge_align == "right":
                badge_x = x + w - badge_w - 12
            elif badge_align == "center":
                badge_x = x + (w - badge_w) // 2
            else:
                badge_x = x + 12
            badge_y = y + 10

            b_stroke = badge_stroke if badge_stroke else stroke
            badge = self._base_element("rectangle", badge_x, badge_y, badge_w, badge_h, stroke=b_stroke, bg=badge_bg, fill="solid", stroke_width=1.5, stroke_style="solid", roughness=0, roundness=2)
            self.elements.append(badge)

            lbl = self._base_element("text", badge_x + 8, badge_y + 4, badge_w - 16, 20, stroke=label_color)
            lbl.update({
                "text": label,
                "fontSize": 13,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(lbl)

        return c["id"]

    def add_lifeline(self, x, y_start, y_end, stroke="#868e96", stroke_width=2, stroke_style="dashed"):
        """Draws a clean vertical lifeline for sequence diagrams."""
        height = y_end - y_start
        line = self._base_element("line", x, y_start, 0, height, stroke=stroke, stroke_width=stroke_width, stroke_style=stroke_style, roughness=0, roundness=None)
        line.update({
            "points": [[0, 0], [0, height]]
        })
        self.elements.append(line)
        return line["id"]

    def add_arrow(self, x1, y1, x2, y2, label=None, stroke="#495057", stroke_width=2, stroke_style="solid", end_arrow="arrow", label_offset_y=-18, label_bg=None, font_size=12):
        """Draws an arrow with optional label centered above it without destructive background masks."""
        dx = x2 - x1
        dy = y2 - y1
        a = self._base_element("arrow", x1, y1, abs(dx), abs(dy), stroke=stroke, stroke_width=stroke_width, stroke_style=stroke_style, roughness=0, roundness=None)
        a.update({
            "points": [[0, 0], [dx, dy]],
            "endArrowhead": end_arrow
        })
        self.elements.append(a)

        if label:
            mx = x1 + dx // 2
            my = y1 + dy // 2 + label_offset_y
            lbl_w = int(len(label) * 7.5 + 16)

            if label_bg:
                mask = self._base_element("rectangle", mx - lbl_w // 2, my - 2, lbl_w, font_size + 6, stroke="transparent", bg=label_bg, fill="solid", roundness=2, roughness=0)
                self.elements.append(mask)

            lbl = self._base_element("text", mx - lbl_w // 2, my, lbl_w, font_size + 4, stroke=stroke)
            lbl.update({
                "text": label,
                "fontSize": font_size,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(lbl)

    def add_sequence_message(self, x1, x2, y, label, stroke="#1971c2", is_response=False, font_size=12, label_bg="#ffffff"):
        """Convenience method for sequence diagram message passing between lifelines."""
        stroke_style = "dashed" if is_response else "solid"
        self.add_arrow(x1, y, x2, y, label=label, stroke=stroke, stroke_style=stroke_style, label_offset_y=-21, label_bg=label_bg, font_size=font_size)

    def add_pill(self, x, y, w, h, text, bg="#e7f5ff", stroke="#1971c2", text_color=None, font_size=12):
        """Draws a compact pill/tag."""
        pill = self._base_element("rectangle", x, y, w, h, stroke=stroke, bg=bg, roundness=3, roughness=0)
        self.elements.append(pill)
        t_color = text_color if text_color else stroke
        t = self._base_element("text", x + 4, y + (h - font_size) // 2 - 2, w - 8, font_size + 4, stroke=t_color)
        t.update({
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1,
            "textAlign": "center"
        })
        self.elements.append(t)
        return pill["id"]

    def add_text(self, x, y, text, font_size=15, stroke="#1e1e1e", align="center", w=300):
        """Adds standalone text."""
        t = self._base_element("text", x, y, w, font_size + 8, stroke=stroke)
        t.update({
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1,
            "textAlign": align
        })
        self.elements.append(t)
        return t["id"]

    def add_header(self, title, subtitle=None, x=40, y=25, w=960, h=65, bg="#f8f9fa", stroke="#343a40"):
        """Draws a top diagram header banner."""
        banner = self._base_element("rectangle", x, y, w, h, stroke=stroke, bg=bg, fill="solid", roundness=3, roughness=0)
        self.elements.append(banner)

        if subtitle:
            t = self._base_element("text", x + 10, y + 10, w - 20, 26, stroke=stroke)
            t.update({
                "text": title,
                "fontSize": 20,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(t)

            s = self._base_element("text", x + 10, y + 38, w - 20, 20, stroke="#495057")
            s.update({
                "text": subtitle,
                "fontSize": 13,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(s)
        else:
            t = self._base_element("text", x + 10, y + (h - 22) // 2, w - 20, 26, stroke=stroke)
            t.update({
                "text": title,
                "fontSize": 20,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(t)

    def render(self, output_filename, scale=2, padding=35):
        """Renders scene to .excalidraw and high-res PNG."""
        out_png = os.path.join(DIAGRAMS_DIR, output_filename)
        out_json = out_png.replace(".png", ".excalidraw")

        scene = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {
                "viewBackgroundColor": self.bg_color,
                "gridSize": None
            },
            "files": {}
        }

        with open(out_json, "w") as f:
            json.dump(scene, f, indent=2)

        cmd = [
            "mcp-excalidraw-server", "render", out_json,
            "--out", out_png,
            "--format", "png",
            "--scale", str(scale),
            "--padding", str(padding)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Render failed: {res.stderr}")
        print(f"Generated: {out_png}")
        return out_png
