<p align="center">

```
███████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗ ██████╗ ███╗   ██╗
██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║██╔════╝ ████╗  ██║
███████╗██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║██║  ███╗██╔██╗ ██║
╚════██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║██║   ██║██║╚██╗██║
███████║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗██║╚██████╔╝██║ ╚████║
╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

    ██╗  ██╗███╗   ███╗██╗          ██████╗ ██████╗ ███╗   ███╗██████╗
    ╚██╗██╔╝████╗ ████║██║         ██╔════╝██╔═══██╗████╗ ████║██╔══██╗
     ╚███╔╝ ██╔████╔██║██║         ██║     ██║   ██║██╔████╔██║██████╔╝
     ██╔██╗ ██║╚██╔╝██║██║         ██║     ██║   ██║██║╚██╔╝██║██╔═══╝
    ██╔╝ ██╗██║ ╚═╝ ██║███████╗    ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║
    ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝
```

</p>

<h3 align="center">XML in. SVG out. Zero dependencies.</h3>

<p align="center">
  <img src="https://img.shields.io/badge/language-Python-3776AB?style=flat-square"/>
  <img src="https://img.shields.io/badge/deps-zero-black?style=flat-square"/>
  <img src="https://img.shields.io/badge/tests-6_passing-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/also-XSLT_in_browser-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square"/>
</p>

---

## What Is This?

Two compilers that turn XML into visual output:

1. **XMLToSVG** — takes a scene description in XML, outputs a standalone SVG image
2. **ConstraintGraphCompiler** — takes a directed graph in XML, outputs both an SVG visualization AND a runtime execution pipeline (topological order via Kahn's algorithm)

Both run server-side (Python), client-side (XSLT in any browser), and as a CLI. No lxml. No numpy. No external packages. Pure Python stdlib.

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   YOUR XML                          OUTPUT                       ║
║   ────────                          ──────                       ║
║                                                                  ║
║   <scene width="800" height="600">  ┌─────────────────────────┐ ║
║     <rect .../>                     │                         │ ║
║     <circle .../>          ──────>  │   Beautiful SVG image   │ ║
║     <text .../>                     │   (dark theme, styled)  │ ║
║   </scene>                          └─────────────────────────┘ ║
║                                                                  ║
║   <graph>                           ┌─────────────────────────┐ ║
║     <node id="A"/>                  │  SVG graph diagram      │ ║
║     <node id="B"/>         ──────>  │  + execution pipeline   │ ║
║     <edge from="A" to="B"/>         │  ["A", "B", "C"]       │ ║
║   </graph>                          └─────────────────────────┘ ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Quick Start

```bash
# From source
git clone https://github.com/SNAPKITTYWEST/sovereign-xml-compiler
cd sovereign-xml-compiler

# Scene to SVG
python xml2svg.py examples/scene.xml > output.svg

# Constraint graph to SVG
python constraint_graph_svg.py examples/constraint_graph.xml > graph.svg

# Run in browser (no server-side code needed)
python -m http.server 8000
# open http://localhost:8000/browser/graph_browser.html
```

---

## Install

```bash
# pip (installs CLI commands: xml2svg, constraint-graph)
pip install sovereign-xml-compiler

# from source (editable)
pip install -e .

# docker
docker run -p 8000:8000 ghcr.io/snapkittywest/sovereign-xml-compiler
# open http://localhost:8000/browser/graph_browser.html
```

Requires Python 3.9+. Zero external dependencies.

---

## User Guide

### Compiler 1: XML Scene to SVG

Write a scene in XML using simple shape primitives:

```xml
<scene width="800" height="600">
  <rect x="10" y="10" width="200" height="100" fill="#1a1a2e" stroke="#e94560"/>
  <circle cx="400" cy="300" r="50" fill="#e94560"/>
  <line x1="0" y1="0" x2="800" y2="600" stroke="white" stroke-width="2"/>
  <text x="100" y="50" fill="white" font-size="24">Hello, Sovereign</text>
  <group transform="translate(50,50)">
    <rect x="0" y="0" width="50" height="50" fill="gold"/>
  </group>
</scene>
```

Compile it:

```bash
# CLI
xml2svg scene.xml output.svg

# Python
from xml2svg import XMLToSVG
svg_string = XMLToSVG().compile(open("scene.xml").read())
```

Supported elements: `rect`, `circle`, `line`, `path`, `text`, `group`

### Compiler 2: Constraint Graph to SVG + Runtime

Define a processing pipeline as a directed graph:

```xml
<graph>
  <node id="input"     type="Input"     label="Raw Data"/>
  <node id="validate"  type="Transform" label="Validate"/>
  <node id="transform" type="Transform" label="Process"/>
  <node id="output"    type="Output"    label="Result"/>

  <edge from="input"    to="validate"/>
  <edge from="validate" to="transform"/>
  <edge from="transform" to="output"/>
</graph>
```

Get both a visualization AND an execution order:

```python
from constraint_graph_svg import ConstraintGraphCompiler

compiler = ConstraintGraphCompiler()

# Dark-themed SVG visualization of the graph
svg = compiler.compile_to_svg(xml_string)

# Executable runtime dict with topological pipeline
runtime = compiler.compile_to_runtime(xml_string)
# runtime = {
#   "nodes": [...],
#   "edges": [...],
#   "pipeline": ["input", "validate", "transform", "output"]
# }
```

The `pipeline` field is computed via **Kahn's algorithm** — guaranteed topological order. Cycles are detected and rejected.

### Browser Mode (XSLT, No Server)

Open `browser/graph_browser.html` in any modern browser. It uses the browser's native `XSLTProcessor` to transform XML into SVG client-side. No JavaScript frameworks. No build step.

```
╔══════════════════════════════════════════════════════════════╗
║  browser/graph_browser.html                                  ║
║       │                                                      ║
║       ├── fetches constraint_graph.xml                       ║
║       ├── fetches constraint_graph.xsl                       ║
║       ├── applies XSLTProcessor (browser-native)             ║
║       └── renders SVG in sandboxed <iframe>                  ║
║                                                              ║
║  Zero JavaScript dependencies. Pure XML/XSLT/CSS.           ║
╚══════════════════════════════════════════════════════════════╝
```

---

## CLI Reference

```bash
# XML scene → SVG
xml2svg input.xml                    # stdout
xml2svg input.xml output.svg         # file

# Constraint graph → SVG
constraint-graph input.xml           # stdout (SVG)
constraint-graph input.xml out.svg   # file (SVG)
constraint-graph input.xml --runtime # stdout (JSON pipeline)
```

---

## Architecture

```
  XML Source Document
        │
        ▼
  xml.etree.ElementTree.fromstring()     ← stdlib, no lxml
        │
        ▼
  ┌─────────────────────────────────────────────────────┐
  │  SEMANTIC VALIDATION                                 │
  │                                                      │
  │  XMLToSVG:   whitelist {rect,circle,line,path,       │
  │              text,group} — rejects unknown elements   │
  │                                                      │
  │  GraphComp:  Kahn's topological sort                 │
  │              cycle detection → error on DAG violation │
  └─────────────────────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────────────────────┐
  │  IR CONSTRUCTION                                     │
  │                                                      │
  │  XMLToSVG:   SVGNode dataclass tree                  │
  │  GraphComp:  {nodes: list, edges: list, pipeline}    │
  └─────────────────────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────────────────────┐
  │  CODE GENERATION                                     │
  │                                                      │
  │  XMLToSVG:   recursive ir_to_svg() → SVG string     │
  │  GraphComp:  _render_svg() → dark-theme SVG         │
  │              compile_to_runtime() → JSON dict        │
  └─────────────────────────────────────────────────────┘
```

---

## Files

```
sovereign-xml-compiler/
├── xml2svg.py                  XMLToSVG compiler (scene → SVG)
├── constraint_graph_svg.py     ConstraintGraphCompiler (graph → SVG + runtime)
├── pyproject.toml              Package config + CLI entry points
├── test_compilers.py           6 tests, zero dependencies
├── Dockerfile                  Containerized browser server
├── examples/
│   ├── scene.xml               800x600 scene with shapes + text
│   └── constraint_graph.xml    7-node processing pipeline
└── browser/
    ├── index.html              Sovereign browser host page
    ├── graph_browser.html      XSLT graph visualizer (no JS deps)
    ├── browser.xsl             HTML transform (dark theme, CSS nav)
    ├── constraint_graph.xsl    SVG transform (graph → visual)
    ├── browser.xml             2-page sovereign browser source
    └── validate_xslt.py        CI: validates XSL as well-formed XML
```

---

## Tests

```bash
python test_compilers.py
# 6 tests: 6 passed, 0 failed
```

Tests cover: scene compilation, graph compilation, topological sort correctness, cycle detection, empty input handling, SVG well-formedness.

---

<p align="center"><b>Built by Ahmad Ali Parr + SnapKitty Collective</b></p>
<p align="center"><i>XML is a compiler target. SVG is the output format. Python stdlib is the only dependency.</i></p>
