"""validate_xslt.py — Validate XSLT files as well-formed XML."""
import os
import sys
import xml.etree.ElementTree as ET

HERE  = os.path.dirname(os.path.abspath(__file__))
FILES = ["browser.xsl", "constraint_graph.xsl"]

all_valid = True
for name in FILES:
    path = os.path.join(HERE, name)
    try:
        ET.parse(path)
        print(f"VALID    {name}")
    except ET.ParseError as e:
        print(f"INVALID  {name}: {e}")
        all_valid = False

if not all_valid:
    sys.exit(1)
print("All XSLT files valid XML.")
