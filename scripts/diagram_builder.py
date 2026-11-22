#!/usr/bin/env python3
"""
Excalidraw Diagram Generator Engine
Generates pristine, professional Excalidraw diagrams and renders them to high-res PNGs.
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

    def _base_element(self, el_type, x, y, w, h, stroke="#1e1e1e", bg="transparent", fill="solid", stroke_width=2, stroke_style="solid", roughness=1, roundness=3):
        return {
            "id": str(uuid.uuid4())[:8],
            "type": el_type,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
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

    def add_box(self, x, y, w, h, title, subtitle=None, bg="#e7f5ff", stroke="#1971c2", font_size=16, roundness=3):
        # Card background
        box = self._base_element("rectangle", x, y, w, h, stroke=stroke, bg=bg, roundness=roundness)
        self.elements.append(box)

        # Title text
        if title:
            t_y = y + (h // 2 - 12 if not subtitle else h // 2 - 20)
            t = self._base_element("text", x + 10, t_y, w - 20, 24, stroke=stroke)
            t.update({
                "text": title,
                "fontSize": font_size,
                "fontFamily": 1,
                "textAlign": "center",
                "verticalAlign": "middle",
                "containerId": box["id"]
            })
            self.elements.append(t)

        # Subtitle / description
        if subtitle:
            s_y = y + h // 2 + 4
            s = self._base_element("text", x + 10, s_y, w - 20, 18, stroke="#495057")
            s.update({
                "text": subtitle,
                "fontSize": font_size - 4,
                "fontFamily": 1,
                "textAlign": "center",
                "verticalAlign": "middle",
                "containerId": box["id"]
            })
            self.elements.append(s)

        return box["id"]

    def add_container(self, x, y, w, h, label=None, stroke="#adb5bd", stroke_style="dashed", bg="transparent"):
        c = self._base_element("rectangle", x, y, w, h, stroke=stroke, bg=bg, stroke_width=2, stroke_style=stroke_style, roughness=0, roundness=2)
        self.elements.append(c)
        if label:
            lbl = self._base_element("text", x + 16, y - 12, len(label) * 10, 20, stroke=stroke)
            lbl.update({
                "text": f" {label} ",
                "fontSize": 14,
                "fontFamily": 1,
                "backgroundColor": "#ffffff",
                "fillStyle": "solid",
                "textAlign": "left"
            })
            self.elements.append(lbl)
        return c["id"]

    def add_arrow(self, x1, y1, x2, y2, label=None, stroke="#495057", stroke_width=2, stroke_style="solid", end_arrow="arrow"):
        dx = x2 - x1
        dy = y2 - y1
        a = self._base_element("arrow", x1, y1, abs(dx), abs(dy), stroke=stroke, stroke_width=stroke_width, stroke_style=stroke_style, roundness=None)
        a.update({
            "points": [[0, 0], [dx, dy]],
            "endArrowhead": end_arrow
        })
        self.elements.append(a)

        if label:
            mx = x1 + dx // 2
            my = y1 + dy // 2 - 18
            lbl = self._base_element("text", mx - 40, my, 80, 16, stroke=stroke)
            lbl.update({
                "text": label,
                "fontSize": 12,
                "fontFamily": 1,
                "textAlign": "center"
            })
            self.elements.append(lbl)

    def add_text(self, x, y, text, font_size=16, stroke="#1e1e1e", align="center", w=200):
        t = self._base_element("text", x, y, w, 24, stroke=stroke)
        t.update({
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1,
            "textAlign": align
        })
        self.elements.append(t)

    def render(self, output_filename, scale=2, padding=30):
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
