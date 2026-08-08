<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" encoding="UTF-8" doctype-public="-//W3C//DTD HTML 4.01//EN"/>

  <xsl:template match="/browser">
    <html>
      <head>
        <meta http-equiv="Content-Security-Policy"
              content="default-src 'none'; style-src 'unsafe-inline'; script-src 'none';"/>
        <meta charset="UTF-8"/>
        <title><xsl:value-of select="@title"/></title>
        <style>
          * { box-sizing: border-box; margin: 0; padding: 0; }

          body {
            background: #0d0d1a;
            color: #e2e8f0;
            font-family: 'Courier New', Courier, monospace;
            min-height: 100vh;
            padding: 2rem;
          }

          h1.browser-title {
            color: #7dd3fc;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 0.75rem;
          }

          .pages-container {
            position: relative;
          }

          .page {
            display: none;
            animation: fadein 0.2s ease-in;
          }

          .page:target {
            display: block;
          }

          /* Show home page by default when no target is set */
          .page#home {
            display: block;
          }

          .page:target ~ .page#home {
            display: none;
          }

          @keyframes fadein {
            from { opacity: 0; transform: translateY(4px); }
            to   { opacity: 1; transform: translateY(0); }
          }

          .page-card {
            background: #1a1a2e;
            border: 1px solid #1e3a5f;
            border-radius: 8px;
            padding: 2rem;
            max-width: 640px;
          }

          h2.page-heading {
            color: #7dd3fc;
            font-size: 1.25rem;
            margin-bottom: 1rem;
          }

          p.page-text {
            color: #cbd5e1;
            line-height: 1.7;
            margin-bottom: 1.25rem;
          }

          a.page-link {
            display: inline-block;
            color: #38bdf8;
            text-decoration: none;
            border: 1px solid #0ea5e9;
            border-radius: 4px;
            padding: 0.35rem 0.85rem;
            font-size: 0.875rem;
            transition: background 0.15s, color 0.15s;
          }

          a.page-link:hover {
            background: #0ea5e9;
            color: #0d0d1a;
          }
        </style>
      </head>
      <body>
        <h1 class="browser-title"><xsl:value-of select="@title"/></h1>
        <div class="pages-container">
          <xsl:apply-templates select="page"/>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="page">
    <div class="page" id="{@id}">
      <div class="page-card">
        <h2 class="page-heading"><xsl:value-of select="heading"/></h2>
        <p class="page-text"><xsl:value-of select="text"/></p>
        <xsl:apply-templates select="link"/>
      </div>
    </div>
  </xsl:template>

  <xsl:template match="link">
    <a class="page-link" href="#{@target}"><xsl:value-of select="."/></a>
  </xsl:template>

</xsl:stylesheet>
