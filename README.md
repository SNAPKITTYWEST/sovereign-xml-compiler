# sovereign-xml-compiler

**XML → SVG compiler with zero dependencies.** Pure Python stdlib — no lxml, no numpy, no external packages.

Two compilers, two targets, one XML source:

```
constraint_graph.xml
        │
        ├── Python:  ConstraintGraphCompiler  →  runtime dict  {nodes, edges, pipeline}
        └── XSLT:    constraint_graph.xsl     →  SVG visualization (sandboxed iframe)
```

Works in the browser via XSLT, works on the server via Python, works as a CLI. No install required to run — just Python 3.9+.

```bash
pip install sovereign-xml-compiler
xml2svg examples/scene.xml output.svg
constraint-graph examples/constraint_graph.xml --runtime
```

```bash
docker run -p 8000:8000 ghcr.io/snapkittywest/sovereign-xml-compiler
# open http://localhost:8000/browser/graph_browser.html
```

---

## What it does

### `XMLToSVG` — sovereign XML scene → SVG

Input: an XML document with root `<scene width height>` and children `rect circle line path text group`.

```xml
<scene width="800" height="600">
  <rect x="10" y="10" width="200" height="100" fill="#1a1a2e"/>
  <circle cx="400" cy="300" r="50" fill="#e94560"/>
  <text x="100" y="50" fill="white">Hello, Sovereign</text>
</scene>
```

```python
from xml2svg import XMLToSVG
svg = XMLToSVG().compile(open("examples/scene.xml").read())
```

### `ConstraintGraphCompiler` — DAG → SVG + runtime

Input: a directed acyclic graph in XML.

```xml
<graph>
  <node id="input"     type="Input"/>
  <node id="transform" type="Transform"/>
  <edge from="input" to="transform"/>
</graph>
```

```python
from constraint_graph_svg import ConstraintGraphCompiler

compiler = ConstraintGraphCompiler()
svg     = compiler.compile_to_svg(xml)          # dark-theme SVG visualization
runtime = compiler.compile_to_runtime(xml)      # {nodes, edges, pipeline}
# runtime["pipeline"] = ["input", "transform"]  ← topological order via Kahn's
```

### XSLT in the browser

No server required for visualization — the browser applies the XSLT transform client-side:

```
browser/graph_browser.html  →  fetches constraint_graph.xml + constraint_graph.xsl
                                applies XSLTProcessor
                                renders SVG in sandboxed iframe
```

```bash
python -m http.server 8000
# open http://localhost:8000/browser/graph_browser.html
```

---

## Install

```bash
# pip
pip install sovereign-xml-compiler

# from source
git clone https://github.com/SNAPKITTYWEST/sovereign-xml-compiler
cd sovereign-xml-compiler
pip install -e .

# docker
docker run -p 8000:8000 ghcr.io/snapkittywest/sovereign-xml-compiler
```

No dependencies. Requires Python 3.9+.

---

## CLI

```bash
# XML scene → SVG
xml2svg examples/scene.xml                   # print to stdout
xml2svg examples/scene.xml output.svg        # write to file

# Constraint graph → SVG
constraint-graph examples/constraint_graph.xml
constraint-graph examples/constraint_graph.xml graph.svg

# Constraint graph → runtime dict (JSON)
constraint-graph examples/constraint_graph.xml --runtime
```

---

## Files

```
sovereign-xml-compiler/
├── xml2svg.py                  XMLToSVG compiler
├── constraint_graph_svg.py     ConstraintGraphCompiler (SVG + runtime)
├── test_compilers.py           6 tests, zero dependencies
├── examples/
│   ├── scene.xml               800x600 scene with rect/circle/line/text
│   └── constraint_graph.xml    7-node input→output pipeline
└── browser/
    ├── index.html              Sovereign browser host (XSLT → iframe)
    ├── graph_browser.html      Constraint graph visualizer
    ├── browser.xsl             XSLT → dark-theme HTML (CSS-only nav, no JS)
    ├── constraint_graph.xsl    XSLT → SVG graph visualization
    ├── browser.xml             2-page sovereign browser source
    └── validate_xslt.py        CI: validates both XSL files as well-formed XML
```

---

## Tests

```bash
python test_compilers.py
# 6 tests: 6 passed, 0 failed
```

Tests run on Python 3.9, 3.10, 3.11, 3.12 via GitHub Actions.

---

## Pipeline architecture

```
XML source
    │
    ▼  xml.etree.ElementTree.fromstring()
    │
    ▼  Semantic validation
    │  XMLToSVG:  whitelist {rect,circle,line,path,text,group}
    │  GraphComp: Kahn's topological sort, cycle detection
    │
    ▼  IR construction
    │  XMLToSVG:  SVGNode dataclass tree
    │  GraphComp: {nodes: list, edges: list, pipeline: list}
    │
    ▼  Code generation
       XMLToSVG:  recursive ir_to_svg()  →  SVG string
       GraphComp: _render_svg()           →  SVG string
                  compile_to_runtime()    →  dict
```

---

Built by Ahmad Ali Parr × SnapKitty.
