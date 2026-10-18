Title: Live Content

Description: Fetched live

Source: https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/index.html

---

<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="../../">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PyQGIS Developer Cookbook &mdash; QGIS Documentation  documentation</title>
      <link rel="stylesheet" type="text/css" href="../../_static/pygments.css?v=80d5e7a1" />
      <link rel="stylesheet" type="text/css" href="../../_static/css/qgis_docs.css?v=01847ad1" />
      <link rel="stylesheet" type="text/css" href="../../_static/togglebutton.css?v=13237357" />
      <link rel="stylesheet" type="text/css" href="../../_static/copybutton.css?v=76b2166b" />
      <link rel="stylesheet" type="text/css" href="../../_static/css/qgis_topbar.css?v=5613a779" />

  
    <link rel="shortcut icon" href="../../_static/qgis_logo.ico"/>
    <link rel="canonical" href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/index.html"/>
  <!--[if lt IE 9]>
    <script src="../../_static/js/html5shiv.min.js"></script>
  <![endif]-->
  
        <script src="../../_static/jquery.js?v=5d32c60e"></script>
        <script src="../../_static/_sphinx_javascript_frameworks_compat.js?v=2cd50e6c"></script>
        <script src="../../_static/documentation_options.js?v=5929fcd5"></script>
        <script src="../../_static/doctools.js?v=888ff710"></script>
        <script src="../../_static/sphinx_highlight.js?v=dc90522c"></script>
        <script src="../../_static/clipboard.min.js?v=a7894cd8"></script>
        <script src="../../_static/copybutton.js?v=f281be69"></script>
        <script>let toggleHintShow = 'Click to show';</script>
        <script>let toggleHintHide = 'Click to hide';</script>
        <script>let toggleOpenOnPrint = 'true';</script>
        <script src="../../_static/togglebutton.js?v=4a39c7ea"></script>
        <script>var togglebuttonSelector = '.toggle, .admonition.dropdown';</script>
        <script>var togglebuttonSelector = '.toggle, .admonition.dropdown';</script>
    <script src="../../_static/js/theme.js"></script>
    <link rel="index" title="Index" href="../../genindex.html" />
    <link rel="search" title="Search" href="../../search.html" />
    <link rel="next" title="1. Introduction" href="intro.html" />
    <link rel="prev" title="5. Substitutions" href="../documentation_guidelines/substitutions.html" />
  <meta name="description" content="QGIS 3.34 documentation: PyQGIS Developer Cookbook">
  <meta name="robots" content="noindex">
</head>

<body class="wy-body-for-nav">

  <nav class="release_status_topbar">
    <div class="row outdated">
     This documentation is for a QGIS version which has reached end of life. Instead visit the <a href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/index.html">latest version</a>.
    </div>
  </nav>

   

 
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search" >
   

          
          
          <a href="../index.html" class="icon icon-home">
            QGIS Documentation
              <img src="../../_static/logo.png" class="logo" alt="Logo"/>
          </a>
              <div class="version">
                3.34
              </div>
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="../../search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" aria-label="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>
   <a href= "../../genindex.html">Index</a>
 
        </div><div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="Navigation menu">
              <p class="caption" role="heading"><span class="caption-text">For Users</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="../user_manual/index.html">QGIS Desktop User Guide/Manual (QGIS 3.34)</a></li>
<li class="toctree-l1"><a class="reference internal" href="../server_manual/index.html">QGIS Server Guide/Manual (QGIS 3.34)</a></li>
<li class="toctree-l1"><a class="reference internal" href="../training_manual/index.html">Training Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../gentle_gis_introduction/index.html">A Gentle Introduction to GIS</a></li>
</ul>
<p class="caption" role="heading"><span class="caption-text">For Writers</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="../documentation_guidelines/index.html">Documentation Guidelines</a></li>
</ul>
<p class="caption" role="heading"><span class="caption-text">For Developers</span></p>
<ul class="current">
<li class="toctree-l1 current"><a class="current reference internal" href="#">PyQGIS Cookbook (QGIS 3.34)</a><ul>
<li class="toctree-l2"><a class="reference internal" href="intro.html">1. Introduction</a></li>
<li class="toctree-l2"><a class="reference internal" href="loadproject.html">2. Loading Projects</a></li>
<li class="toctree-l2"><a class="reference internal" href="loadlayer.html">3. Loading Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="legend.html">4. Accessing the Table Of Contents (TOC)</a></li>
<li class="toctree-l2"><a class="reference internal" href="raster.html">5. Using Raster Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html">6. Using Vector Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="geometry.html">7. Geometry Handling</a></li>
<li class="toctree-l2"><a class="reference internal" href="crs.html">8. Projections Support</a></li>
<li class="toctree-l2"><a class="reference internal" href="canvas.html">9. Using the Map Canvas</a></li>
<li class="toctree-l2"><a class="reference internal" href="composer.html">10. Map Rendering and Printing</a></li>
<li class="toctree-l2"><a class="reference internal" href="expressions.html">11. Expressions, Filtering and Calculating Values</a></li>
<li class="toctree-l2"><a class="reference internal" href="settings.html">12. Reading And Storing Settings</a></li>
<li class="toctree-l2"><a class="reference internal" href="communicating.html">13. Communicating with the user</a></li>
<li class="toctree-l2"><a class="reference internal" href="authentication.html">14. Authentication infrastructure</a></li>
<li class="toctree-l2"><a class="reference internal" href="tasks.html">15. Tasks - doing heavy work in the background</a></li>
<li class="toctree-l2"><a class="reference internal" href="plugins/index.html">16. Developing Python Plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="processing.html">17. Writing a Processing plugin</a></li>
<li class="toctree-l2"><a class="reference internal" href="pluginlayer.html">18. Using Plugin Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="network_analysis.html">19. Network analysis library</a></li>
<li class="toctree-l2"><a class="reference internal" href="server.html">20. QGIS Server and Python</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html">21. Cheat sheet for PyQGIS</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="../developers_guide/index.html">Developers Guide</a></li>
</ul>

        </div>
      </div>
    </nav>

    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap"><nav class="wy-nav-top" aria-label="Mobile navigation menu" >
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="../index.html">QGIS Documentation</a>
      </nav>

      <div class="wy-nav-content">
        <div class="rst-content">
          <div role="navigation" aria-label="Page navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="../index.html" class="icon icon-home" aria-label="Home"></a></li>
      <li class="breadcrumb-item active">PyQGIS Developer Cookbook</li>

    <li style="float: right; text-align: right;">
	<ul>
		
      <li class="wy-breadcrumbs-aside">
            <a href="../../_sources/docs/pyqgis_developer_cookbook/index.rst.txt" rel="nofollow"> View page source</a>
      </li>
	</ul>

        <!-- Add a button to guide potential contributors
	     To do: add a more generic page for contributing in QGIS docs to keep users in the same website
	     <a class="qgis-edit-guidelines" href="https://docs.qgis.org/3.34/en/docs/documentation_guidelines/index.html">
	-->
	<a class="qgis-edit-guidelines" href="https://qgis.org/community/involve/">
		Learn how to contribute!
	</a>
    </li>


  </ul><div class="rst-breadcrumbs-buttons" role="navigation" aria-label="Sequential page navigation">
        <a href="../documentation_guidelines/substitutions.html" class="btn btn-neutral float-left" title="5. Substitutions" accesskey="p"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="intro.html" class="btn btn-neutral float-right" title="1. Introduction" accesskey="n">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
  </div>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <blockquote>
<div></div></blockquote>
<section id="pyqgis-developer-cookbook">
<span id="id1"></span><h1>PyQGIS Developer Cookbook<a class="headerlink" href="#pyqgis-developer-cookbook" title="Link to this heading"></a></h1>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="intro.html">1. Introduction</a><ul>
<li class="toctree-l2"><a class="reference internal" href="intro.html#scripting-in-the-python-console">1.1. Scripting in the Python Console</a></li>
<li class="toctree-l2"><a class="reference internal" href="intro.html#python-plugins">1.2. Python Plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="intro.html#running-python-code-when-qgis-starts">1.3. Running Python code when QGIS starts</a></li>
<li class="toctree-l2"><a class="reference internal" href="intro.html#python-applications">1.4. Python Applications</a></li>
<li class="toctree-l2"><a class="reference internal" href="intro.html#technical-notes-on-pyqt-and-sip">1.5. Technical notes on PyQt and SIP</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="loadproject.html">2. Loading Projects</a><ul>
<li class="toctree-l2"><a class="reference internal" href="loadproject.html#resolving-bad-paths">2.1. Resolving bad paths</a></li>
<li class="toctree-l2"><a class="reference internal" href="loadproject.html#using-flags-to-speed-up-things">2.2. Using flags to speed up things</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="loadlayer.html">3. Loading Layers</a><ul>
<li class="toctree-l2"><a class="reference internal" href="loadlayer.html#vector-layers">3.1. Vector Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="loadlayer.html#raster-layers">3.2. Raster Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="loadlayer.html#qgsproject-instance">3.3. QgsProject instance</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="legend.html">4. Accessing the Table Of Contents (TOC)</a><ul>
<li class="toctree-l2"><a class="reference internal" href="legend.html#the-qgsproject-class">4.1. The QgsProject class</a></li>
<li class="toctree-l2"><a class="reference internal" href="legend.html#qgslayertreegroup-class">4.2. QgsLayerTreeGroup class</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="raster.html">5. Using Raster Layers</a><ul>
<li class="toctree-l2"><a class="reference internal" href="raster.html#layer-details">5.1. Layer Details</a></li>
<li class="toctree-l2"><a class="reference internal" href="raster.html#renderer">5.2. Renderer</a></li>
<li class="toctree-l2"><a class="reference internal" href="raster.html#query-values">5.3. Query Values</a></li>
<li class="toctree-l2"><a class="reference internal" href="raster.html#editing-raster-data">5.4. Editing raster data</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vector.html">6. Using Vector Layers</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vector.html#retrieving-information-about-attributes">6.1. Retrieving information about attributes</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#iterating-over-vector-layer">6.2. Iterating over Vector Layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#selecting-features">6.3. Selecting features</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#modifying-vector-layers">6.4. Modifying Vector Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#using-spatial-index">6.5. Using Spatial Index</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#the-qgsvectorlayerutils-class">6.6. The QgsVectorLayerUtils class</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#creating-vector-layers">6.7. Creating Vector Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#appearance-symbology-of-vector-layers">6.8. Appearance (Symbology) of Vector Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="vector.html#further-topics">6.9. Further Topics</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="geometry.html">7. Geometry Handling</a><ul>
<li class="toctree-l2"><a class="reference internal" href="geometry.html#geometry-construction">7.1. Geometry Construction</a></li>
<li class="toctree-l2"><a class="reference internal" href="geometry.html#access-to-geometry">7.2. Access to Geometry</a></li>
<li class="toctree-l2"><a class="reference internal" href="geometry.html#geometry-predicates-and-operations">7.3. Geometry Predicates and Operations</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="crs.html">8. Projections Support</a><ul>
<li class="toctree-l2"><a class="reference internal" href="crs.html#coordinate-reference-systems">8.1. Coordinate reference systems</a></li>
<li class="toctree-l2"><a class="reference internal" href="crs.html#crs-transformation">8.2. CRS Transformation</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="canvas.html">9. Using the Map Canvas</a><ul>
<li class="toctree-l2"><a class="reference internal" href="canvas.html#embedding-map-canvas">9.1. Embedding Map Canvas</a></li>
<li class="toctree-l2"><a class="reference internal" href="canvas.html#rubber-bands-and-vertex-markers">9.2. Rubber Bands and Vertex Markers</a></li>
<li class="toctree-l2"><a class="reference internal" href="canvas.html#using-map-tools-with-canvas">9.3. Using Map Tools with Canvas</a></li>
<li class="toctree-l2"><a class="reference internal" href="canvas.html#writing-custom-map-tools">9.4. Writing Custom Map Tools</a></li>
<li class="toctree-l2"><a class="reference internal" href="canvas.html#writing-custom-map-canvas-items">9.5. Writing Custom Map Canvas Items</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="composer.html">10. Map Rendering and Printing</a><ul>
<li class="toctree-l2"><a class="reference internal" href="composer.html#simple-rendering">10.1. Simple Rendering</a></li>
<li class="toctree-l2"><a class="reference internal" href="composer.html#rendering-layers-with-different-crs">10.2. Rendering layers with different CRS</a></li>
<li class="toctree-l2"><a class="reference internal" href="composer.html#output-using-print-layout">10.3. Output using print layout</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="expressions.html">11. Expressions, Filtering and Calculating Values</a><ul>
<li class="toctree-l2"><a class="reference internal" href="expressions.html#parsing-expressions">11.1. Parsing Expressions</a></li>
<li class="toctree-l2"><a class="reference internal" href="expressions.html#evaluating-expressions">11.2. Evaluating Expressions</a></li>
<li class="toctree-l2"><a class="reference internal" href="expressions.html#handling-expression-errors">11.3. Handling expression errors</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="settings.html">12. Reading And Storing Settings</a></li>
<li class="toctree-l1"><a class="reference internal" href="communicating.html">13. Communicating with the user</a><ul>
<li class="toctree-l2"><a class="reference internal" href="communicating.html#showing-messages-the-qgsmessagebar-class">13.1. Showing messages. The QgsMessageBar class</a></li>
<li class="toctree-l2"><a class="reference internal" href="communicating.html#showing-progress">13.2. Showing progress</a></li>
<li class="toctree-l2"><a class="reference internal" href="communicating.html#logging">13.3. Logging</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="authentication.html">14. Authentication infrastructure</a><ul>
<li class="toctree-l2"><a class="reference internal" href="authentication.html#introduction">14.1. Introduction</a></li>
<li class="toctree-l2"><a class="reference internal" href="authentication.html#glossary">14.2. Glossary</a></li>
<li class="toctree-l2"><a class="reference internal" href="authentication.html#qgsauthmanager-the-entry-point">14.3. QgsAuthManager the entry point</a></li>
<li class="toctree-l2"><a class="reference internal" href="authentication.html#adapt-plugins-to-use-authentication-infrastructure">14.4. Adapt plugins to use Authentication infrastructure</a></li>
<li class="toctree-l2"><a class="reference internal" href="authentication.html#authentication-guis">14.5. Authentication GUIs</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="tasks.html">15. Tasks - doing heavy work in the background</a><ul>
<li class="toctree-l2"><a class="reference internal" href="tasks.html#introduction">15.1. Introduction</a></li>
<li class="toctree-l2"><a class="reference internal" href="tasks.html#examples">15.2. Examples</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="plugins/index.html">16. Developing Python Plugins</a><ul>
<li class="toctree-l2"><a class="reference internal" href="plugins/plugins.html">16.1. Structuring Python Plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="plugins/snippets.html">16.2. Code Snippets</a></li>
<li class="toctree-l2"><a class="reference internal" href="plugins/ide_debugging.html">16.3. IDE settings for writing and debugging plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="plugins/releasing.html">16.4. Releasing your plugin</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="processing.html">17. Writing a Processing plugin</a><ul>
<li class="toctree-l2"><a class="reference internal" href="processing.html#creating-from-scratch">17.1. Creating from scratch</a></li>
<li class="toctree-l2"><a class="reference internal" href="processing.html#updating-a-plugin">17.2. Updating a plugin</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="pluginlayer.html">18. Using Plugin Layers</a><ul>
<li class="toctree-l2"><a class="reference internal" href="pluginlayer.html#subclassing-qgspluginlayer">18.1. Subclassing QgsPluginLayer</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="network_analysis.html">19. Network analysis library</a><ul>
<li class="toctree-l2"><a class="reference internal" href="network_analysis.html#general-information">19.1. General information</a></li>
<li class="toctree-l2"><a class="reference internal" href="network_analysis.html#building-a-graph">19.2. Building a graph</a></li>
<li class="toctree-l2"><a class="reference internal" href="network_analysis.html#graph-analysis">19.3. Graph analysis</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="server.html">20. QGIS Server and Python</a><ul>
<li class="toctree-l2"><a class="reference internal" href="server.html#introduction">20.1. Introduction</a></li>
<li class="toctree-l2"><a class="reference internal" href="server.html#server-api-basics">20.2. Server API basics</a></li>
<li class="toctree-l2"><a class="reference internal" href="server.html#standalone-or-embedding">20.3. Standalone or embedding</a></li>
<li class="toctree-l2"><a class="reference internal" href="server.html#id1">20.4. Server plugins</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="cheat_sheet.html">21. Cheat sheet for PyQGIS</a><ul>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#user-interface">21.1. User Interface</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#settings">21.2. Settings</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#toolbars">21.3. Toolbars</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#menus">21.4. Menus</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#canvas">21.5. Canvas</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#layers">21.6. Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#table-of-contents">21.7. Table of contents</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#advanced-toc">21.8. Advanced TOC</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#processing-algorithms">21.9. Processing algorithms</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#decorators">21.10. Decorators</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#composer">21.11. Composer</a></li>
<li class="toctree-l2"><a class="reference internal" href="cheat_sheet.html#sources">21.12. Sources</a></li>
</ul>
</li>
</ul>
</div>
</section>


           </div>
          </div>
          <footer><div class="rst-footer-buttons" role="navigation" aria-label="Footer">
        <a href="../documentation_guidelines/substitutions.html" class="btn btn-neutral float-left" title="5. Substitutions" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="intro.html" class="btn btn-neutral float-right" title="1. Introduction" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
    </div>

  <hr/>

  <div role="contentinfo">
    <p>&#169; Copyright 2002-now, QGIS project.
      <span class="lastupdated">Last updated on 2025 May 20, 20:40 +0000.
      </span></p>
  </div>

  Built with <a href="https://www.sphinx-doc.org/">Sphinx</a> using a
    <a href="https://github.com/readthedocs/sphinx_rtd_theme">theme</a>
    provided by <a href="https://readthedocs.org">Read the Docs</a>.
   

</footer>
        </div>
      </div>
    </section>
  </div>
  <!-- Transifex follows a particular logic to build target pages:
Expected French translation link for https://docs.qgis.org/3.28/en/docs/user_manual/print_composer/overview_composer.html
would return https://app.transifex.com/qgis/qgis-documentation/translate/#fr/aa6d8bc653526d38b295ca94bf8eee5e
with the md5 value of "github#qgis/QGIS-Documentation#release_3.28#locale/en/LC_MESSAGES/docs/user_manual/print_composer/overview_composer.po"-->
<!--Make sure that mismatching language codes between Transifex and Sphinx are converted-->


  <div class="rst-versions" data-toggle="rst-versions" role="note" aria-label="versions">
    <span class="rst-current-version" data-toggle="rst-current-version">
      <span class="fa fa-info-circle"> QGIS Documentation </span>
      v: 3.34
      <span class="fa fa-caret-down"></span>
    </span>

    <div class="rst-other-versions">
      <dl>
        <dt>Languages</dt>
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/index.html">en</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/cs/docs/pyqgis_developer_cookbook/index.html">cs</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/de/docs/pyqgis_developer_cookbook/index.html">de</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/es/docs/pyqgis_developer_cookbook/index.html">es</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/fr/docs/pyqgis_developer_cookbook/index.html">fr</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/hu/docs/pyqgis_developer_cookbook/index.html">hu</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/it/docs/pyqgis_developer_cookbook/index.html">it</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ja/docs/pyqgis_developer_cookbook/index.html">ja</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ko/docs/pyqgis_developer_cookbook/index.html">ko</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/lt/docs/pyqgis_developer_cookbook/index.html">lt</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/nl/docs/pyqgis_developer_cookbook/index.html">nl</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_BR/docs/pyqgis_developer_cookbook/index.html">pt_BR</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_PT/docs/pyqgis_developer_cookbook/index.html">pt_PT</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ro/docs/pyqgis_developer_cookbook/index.html">ro</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ru/docs/pyqgis_developer_cookbook/index.html">ru</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/zh-Hans/docs/pyqgis_developer_cookbook/index.html">zh-Hans</a></dd>
        
      </dl>

      <dl>
        <dt>Versions</dt>
        
          <dd><a href="https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/index.html">testing</a></dd>
        
          <dd><a href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/index.html">latest</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html">3.40</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/index.html">3.34</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/index.html">3.28</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/index.html">3.22</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/index.html">3.16</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.10/en/docs/pyqgis_developer_cookbook/index.html">3.10</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.4/en/docs/pyqgis_developer_cookbook/index.html">3.4</a></dd>
        
          <dd><a href="https://docs.qgis.org/2.18/en/docs/pyqgis_developer_cookbook/index.html">2.18</a></dd>
        
      </dl>

       
       <dl>
        <dt>Downloads</dt>
        
          <dd><a href="https://docs.qgis.org/3.34/pdf">PDF</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/zip">HTML</a></dd>
        
      </dl>
      

      
      

      <dl>
        <dt>On QGIS Project</dt>
          <dd>
            <a href="https://qgis.org" target="_blank" rel="noopener noreferrer">Home</a>
          </dd>
          <dd>
            <a href="https://qgis.org/api/3.34" target="_blank" rel="noopener noreferrer">C++ API</a>
          </dd>
          <dd>
            <a href="https://qgis.org/pyqgis/3.34" target="_blank" rel="noopener noreferrer">PyQGIS API</a>
          </dd>
          <dd>
            <a href="https://github.com/qgis/QGIS/tree/release-3_34" target="_blank" rel="noopener noreferrer">Source</a>
          </dd>
      </dl>

    </div>
  </div><script>
      jQuery(function () {
          SphinxRtdTheme.Navigation.enable(true);
      });
  </script> 

<script defer src="https://static.cloudflareinsights.com/beacon.min.js/v4513226cdae34746b4dedf0b4dfa099e1781791509496" integrity="sha512-ZE9pZaUXND66v380QUtch/5sE9tPFh2zg45pR2PB0CVkCtOREv2AJKkSidISWkysEuQ0EH8faUU5du78bx87UQ==" data-cf-beacon='{"version":"2024.11.0","token":"ac8be2df3ab74d3aaa486243ef005a36","r":1,"server_timing":{"name":{"cfCacheStatus":true,"cfEdge":true,"cfExtPri":true,"cfL4":true,"cfOrigin":true,"cfSpeedBrain":true},"location_startswith":null}}' crossorigin="anonymous"></script>
</body>
</html>

