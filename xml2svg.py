"""
xml2svg.py — Ahmad's XMLToSVG compiler
Architecture: XML → XML Parser/AST → Semantic Validation → SVG IR/Nodes → SVG Code Generator → SVG
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional


# ─── SVG IR Nodes ────────────────────────────────────────────────────────────

@dataclass
class SVGNode:
    tag: str
    attrs: dict
    children: List["SVGNode"] = field(default_factory=list)
    text: Optional[str] = None


# ─── Semantic Validation ──────────────────────────────────────────────────────

SUPPORTED_NODES = {"rect", "circle", "line", "path", "text", "group"}


def validate_node(elem: ET.Element):
    tag = elem.tag
    if tag not in SUPPORTED_NODES:
        raise ValueError(f"Unsupported node tag: <{tag}>")


# ─── XML → SVG IR ─────────────────────────────────────────────────────────────

def xml_elem_to_ir(elem: ET.Element) -> SVGNode:
    validate_node(elem)
    tag = elem.tag
    attrs = dict(elem.attrib)
    text_content = elem.text.strip() if elem.text and elem.text.strip() else None
    children = [xml_elem_to_ir(child) for child in elem]
    return SVGNode(tag=tag, attrs=attrs, children=children, text=text_content)


# ─── SVG Code Generator ───────────────────────────────────────────────────────

def attrs_to_str(attrs: dict) -> str:
    def _escape(v: str) -> str:
        return v.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    return " ".join(f'{k}="{_escape(v)}"' for k, v in attrs.items())


def ir_to_svg(node: SVGNode, indent: int = 2) -> str:
    pad = " " * indent
    tag = node.tag if node.tag != "group" else "g"
    attrs_str = (" " + attrs_to_str(node.attrs)) if node.attrs else ""

    if node.children:
        inner = "\n".join(ir_to_svg(child, indent + 2) for child in node.children)
        return f"{pad}<{tag}{attrs_str}>\n{inner}\n{pad}</{tag}>"
    elif node.text is not None:
        return f"{pad}<{tag}{attrs_str}>{node.text}</{tag}>"
    else:
        return f"{pad}<{tag}{attrs_str}/>"


# ─── XMLToSVG Compiler ────────────────────────────────────────────────────────

class XMLToSVG:
    """
    Compiles a sovereign XML scene description into an SVG string.

    Supported nodes: rect, circle, line, path, text, group
    Root element must be <scene width="..." height="...">.
    """

    def compile(self, xml_source: str) -> str:
        root = ET.fromstring(xml_source)

        if root.tag != "scene":
            raise ValueError(f"Root element must be <scene>, got <{root.tag}>")

        width = root.attrib.get("width", "800")
        height = root.attrib.get("height", "600")

        ir_nodes = [xml_elem_to_ir(child) for child in root]

        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
        ]
        for node in ir_nodes:
            lines.append(ir_to_svg(node))
        lines.append("</svg>")

        return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def _cli():
    import sys
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: xml2svg <input.xml> [output.svg]")
        print("  Compiles a sovereign XML <scene> to SVG.")
        sys.exit(0)
    src = open(sys.argv[1], encoding="utf-8").read()
    svg = XMLToSVG().compile(src)
    if len(sys.argv) >= 3:
        open(sys.argv[2], "w", encoding="utf-8").write(svg)
    else:
        print(svg)


if __name__ == "__main__":
    _cli()
