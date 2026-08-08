<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml" encoding="UTF-8" indent="yes"
              doctype-public="-//W3C//DTD SVG 1.1//EN"
              doctype-system="http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"/>

  <!-- Index nodes for edge coordinate lookup -->
  <xsl:key name="node-by-id" match="node" use="@id"/>

  <xsl:template match="/graph">
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 400 560"
         width="400" height="560">

      <!-- Arrowhead marker -->
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8"
                refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#0ea5e9"/>
        </marker>
      </defs>

      <!-- Background -->
      <rect width="400" height="560" fill="#07071a"/>

      <!-- Title -->
      <text x="200" y="30" fill="#7dd3fc" font-size="16"
            font-family="monospace" text-anchor="middle"
            font-weight="bold">Constraint Graph</text>

      <!-- Draw edges first (behind nodes) -->
      <xsl:for-each select="edge">
        <xsl:call-template name="draw-edge">
          <xsl:with-param name="from" select="@from"/>
          <xsl:with-param name="to" select="@to"/>
        </xsl:call-template>
      </xsl:for-each>

      <!-- Draw nodes -->
      <xsl:for-each select="node">
        <xsl:variable name="y" select="60 + (position() * 70)"/>
        <xsl:variable name="x" select="100"/>
        <!-- Node rect -->
        <rect x="{$x}" y="{$y}" width="200" height="40"
              rx="8" fill="#1a1a2e" stroke="#7dd3fc" stroke-width="1.5"/>
        <!-- Node label -->
        <text x="200" y="{$y + 25}"
              fill="#eee" font-size="14"
              font-family="monospace" text-anchor="middle">
          <xsl:value-of select="@type"/>
        </text>
      </xsl:for-each>

    </svg>
  </xsl:template>

  <!--
    draw-edge: renders a line from the bottom-center of the source node
    to the top-center of the target node.

    Node at position i has y = 60 + (i * 70).
    Bottom-center of node at position i: x=200, y = 60 + (i*70) + 40 = 100 + (i*70)
    Top-center    of node at position i: x=200, y = 60 + (i*70)

    We use xsl:for-each over all nodes to find the position of source/target.
  -->
  <xsl:template name="draw-edge">
    <xsl:param name="from"/>
    <xsl:param name="to"/>

    <!-- Find position of source node -->
    <xsl:variable name="from-pos">
      <xsl:for-each select="/graph/node">
        <xsl:if test="@id = $from">
          <xsl:value-of select="position()"/>
        </xsl:if>
      </xsl:for-each>
    </xsl:variable>

    <!-- Find position of target node -->
    <xsl:variable name="to-pos">
      <xsl:for-each select="/graph/node">
        <xsl:if test="@id = $to">
          <xsl:value-of select="position()"/>
        </xsl:if>
      </xsl:for-each>
    </xsl:variable>

    <!-- Compute coordinates -->
    <xsl:variable name="x1" select="200"/>
    <xsl:variable name="y1" select="60 + ($from-pos * 70) + 40"/>
    <xsl:variable name="x2" select="200"/>
    <xsl:variable name="y2" select="60 + ($to-pos * 70)"/>

    <line x1="{$x1}" y1="{$y1}" x2="{$x2}" y2="{$y2}"
          stroke="#0ea5e9" stroke-width="1.5" stroke-dasharray="4 2"
          marker-end="url(#arrow)"/>
  </xsl:template>


</xsl:stylesheet>
