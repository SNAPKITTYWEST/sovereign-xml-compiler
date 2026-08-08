"""
test_compilers.py — Test suite for xml2svg.py and constraint_graph_svg.py
"""

import os
import sys
import traceback

# ─── Test infrastructure ──────────────────────────────────────────────────────

passed = 0
failed = 0


def test(name: str, fn):
    global passed, failed
    try:
        fn()
        print(f"  PASS  {name}")
        passed += 1
    except Exception as e:
        print(f"  FAIL  {name}")
        traceback.print_exc()
        failed += 1


# ─── Load examples ────────────────────────────────────────────────────────────

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLES = os.path.join(HERE, "examples")

with open(os.path.join(EXAMPLES, "scene.xml"), encoding="utf-8") as f:
    SCENE_XML = f.read()

with open(os.path.join(EXAMPLES, "constraint_graph.xml"), encoding="utf-8") as f:
    GRAPH_XML = f.read()

# ─── Import compilers ─────────────────────────────────────────────────────────

from xml2svg import XMLToSVG
from constraint_graph_svg import ConstraintGraphCompiler

# ─── Tests ───────────────────────────────────────────────────────────────────

print("\nRunning tests...\n")

# 1. XMLToSVG compiles scene.xml → valid SVG
def test_xml2svg_scene():
    compiler = XMLToSVG()
    svg = compiler.compile(SCENE_XML)
    assert "<svg" in svg,   "Missing <svg"
    assert "<rect" in svg,  "Missing <rect"
    assert "<circle" in svg, "Missing <circle"
    assert "<line" in svg,  "Missing <line"
    assert "<text" in svg,  "Missing <text"

test("XMLToSVG compiles scene.xml to valid SVG containing svg/rect/circle/line/text", test_xml2svg_scene)


# 2. XMLToSVG raises ValueError on unsupported node tag
def test_xml2svg_unsupported_tag():
    compiler = XMLToSVG()
    xml = '<scene width="100" height="100"><polygon points="0,0 10,0 5,10"/></scene>'
    try:
        compiler.compile(xml)
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "Unsupported node tag" in str(e)

test("XMLToSVG raises ValueError on unsupported node tag", test_xml2svg_unsupported_tag)


# 3. XMLToSVG raises ValueError if root is not <scene>
def test_xml2svg_wrong_root():
    compiler = XMLToSVG()
    xml = '<canvas width="100" height="100"><rect x="0" y="0" width="10" height="10"/></canvas>'
    try:
        compiler.compile(xml)
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "scene" in str(e).lower()

test("XMLToSVG raises ValueError if root is not <scene>", test_xml2svg_wrong_root)


# 4. ConstraintGraphCompiler compile_to_svg produces valid SVG with all 7 node types
def test_cg_svg_all_types():
    compiler = ConstraintGraphCompiler()
    svg = compiler.compile_to_svg(GRAPH_XML)
    assert "<svg" in svg, "Missing <svg"
    for node_type in ["Input", "Memory", "Retrieval", "Transform", "Constraint", "Proof", "Output"]:
        assert node_type in svg, f"Missing node type: {node_type}"

test("ConstraintGraphCompiler compile_to_svg produces valid SVG with all 7 node types", test_cg_svg_all_types)


# 5. ConstraintGraphCompiler compile_to_runtime returns correct pipeline order
def test_cg_runtime_pipeline_order():
    compiler = ConstraintGraphCompiler()
    result = compiler.compile_to_runtime(GRAPH_XML)
    pipeline = result["pipeline"]
    expected = ["input", "memory", "retrieval", "transform", "constraint", "proof", "output"]
    assert pipeline == expected, f"Pipeline mismatch: got {pipeline}"

test("ConstraintGraphCompiler compile_to_runtime: correct pipeline order", test_cg_runtime_pipeline_order)


# 6. ConstraintGraphCompiler compile_to_runtime returns 7 nodes and 6 edges
def test_cg_runtime_counts():
    compiler = ConstraintGraphCompiler()
    result = compiler.compile_to_runtime(GRAPH_XML)
    assert len(result["nodes"]) == 7, f"Expected 7 nodes, got {len(result['nodes'])}"
    assert len(result["edges"]) == 6, f"Expected 6 edges, got {len(result['edges'])}"

test("ConstraintGraphCompiler compile_to_runtime returns 7 nodes and 6 edges", test_cg_runtime_counts)


# ─── Summary ──────────────────────────────────────────────────────────────────

print(f"\n{'-'*60}")
print(f"Results: {passed} passed, {failed} failed")
print(f"{'-'*60}\n")

sys.exit(0 if failed == 0 else 1)
