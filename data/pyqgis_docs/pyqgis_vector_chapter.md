Title: Live Content

Description: Fetched live

Source: https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/vector.html

---

<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="../../">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>6. Using Vector Layers &mdash; QGIS Documentation  documentation</title>
      <link rel="stylesheet" type="text/css" href="../../_static/pygments.css?v=80d5e7a1" />
      <link rel="stylesheet" type="text/css" href="../../_static/css/qgis_docs.css?v=01847ad1" />
      <link rel="stylesheet" type="text/css" href="../../_static/togglebutton.css?v=13237357" />
      <link rel="stylesheet" type="text/css" href="../../_static/copybutton.css?v=76b2166b" />
      <link rel="stylesheet" type="text/css" href="../../_static/css/qgis_topbar.css?v=5613a779" />

  
    <link rel="shortcut icon" href="../../_static/qgis_logo.ico"/>
    <link rel="canonical" href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/vector.html"/>
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
    <link rel="next" title="7. Geometry Handling" href="geometry.html" />
    <link rel="prev" title="5. Using Raster Layers" href="raster.html" />
  <meta name="description" content="QGIS 3.34 documentation: 6. Using Vector Layers">
  <meta name="robots" content="noindex">
</head>

<body class="wy-body-for-nav">

  <nav class="release_status_topbar">
    <div class="row outdated">
     This documentation is for a QGIS version which has reached end of life. Instead visit the <a href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/vector.html">latest version</a>.
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
<li class="toctree-l1 current"><a class="reference internal" href="index.html">PyQGIS Cookbook (QGIS 3.34)</a><ul class="current">
<li class="toctree-l2"><a class="reference internal" href="intro.html">1. Introduction</a></li>
<li class="toctree-l2"><a class="reference internal" href="loadproject.html">2. Loading Projects</a></li>
<li class="toctree-l2"><a class="reference internal" href="loadlayer.html">3. Loading Layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="legend.html">4. Accessing the Table Of Contents (TOC)</a></li>
<li class="toctree-l2"><a class="reference internal" href="raster.html">5. Using Raster Layers</a></li>
<li class="toctree-l2 current"><a class="current reference internal" href="#">6. Using Vector Layers</a><ul>
<li class="toctree-l3"><a class="reference internal" href="#retrieving-information-about-attributes">6.1. Retrieving information about attributes</a></li>
<li class="toctree-l3"><a class="reference internal" href="#iterating-over-vector-layer">6.2. Iterating over Vector Layer</a></li>
<li class="toctree-l3"><a class="reference internal" href="#selecting-features">6.3. Selecting features</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#accessing-attributes">6.3.1. Accessing attributes</a></li>
<li class="toctree-l4"><a class="reference internal" href="#iterating-over-selected-features">6.3.2. Iterating over selected features</a></li>
<li class="toctree-l4"><a class="reference internal" href="#iterating-over-a-subset-of-features">6.3.3. Iterating over a subset of features</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="#modifying-vector-layers">6.4. Modifying Vector Layers</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#add-features">6.4.1. Add Features</a></li>
<li class="toctree-l4"><a class="reference internal" href="#delete-features">6.4.2. Delete Features</a></li>
<li class="toctree-l4"><a class="reference internal" href="#modify-features">6.4.3. Modify Features</a></li>
<li class="toctree-l4"><a class="reference internal" href="#modifying-vector-layers-with-an-editing-buffer">6.4.4. Modifying Vector Layers with an Editing Buffer</a></li>
<li class="toctree-l4"><a class="reference internal" href="#adding-and-removing-fields">6.4.5. Adding and Removing Fields</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="#using-spatial-index">6.5. Using Spatial Index</a></li>
<li class="toctree-l3"><a class="reference internal" href="#the-qgsvectorlayerutils-class">6.6. The QgsVectorLayerUtils class</a></li>
<li class="toctree-l3"><a class="reference internal" href="#creating-vector-layers">6.7. Creating Vector Layers</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#from-an-instance-of-qgsvectorfilewriter">6.7.1. From an instance of <code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorFileWriter</span></code></a></li>
<li class="toctree-l4"><a class="reference internal" href="#directly-from-features">6.7.2. Directly from features</a></li>
<li class="toctree-l4"><a class="reference internal" href="#from-an-instance-of-qgsvectorlayer">6.7.3. From an instance of <code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="#appearance-symbology-of-vector-layers">6.8. Appearance (Symbology) of Vector Layers</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#single-symbol-renderer">6.8.1. Single Symbol Renderer</a></li>
<li class="toctree-l4"><a class="reference internal" href="#categorized-symbol-renderer">6.8.2. Categorized Symbol Renderer</a></li>
<li class="toctree-l4"><a class="reference internal" href="#graduated-symbol-renderer">6.8.3. Graduated Symbol Renderer</a></li>
<li class="toctree-l4"><a class="reference internal" href="#working-with-symbols">6.8.4. Working with Symbols</a></li>
<li class="toctree-l4"><a class="reference internal" href="#creating-custom-renderers">6.8.5. Creating Custom Renderers</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="#further-topics">6.9. Further Topics</a></li>
</ul>
</li>
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
          <li class="breadcrumb-item"><a href="index.html">PyQGIS Developer Cookbook</a></li>
      <li class="breadcrumb-item active"><span class="section-number">6. </span>Using Vector Layers</li>

    <li style="float: right; text-align: right;">
	<ul>
		
      <li class="wy-breadcrumbs-aside">
            <a href="../../_sources/docs/pyqgis_developer_cookbook/vector.rst.txt" rel="nofollow"> View page source</a>
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
        <a href="raster.html" class="btn btn-neutral float-left" title="5. Using Raster Layers" accesskey="p"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="geometry.html" class="btn btn-neutral float-right" title="7. Geometry Handling" accesskey="n">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
  </div>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <blockquote>
<div></div></blockquote>
<section id="using-vector-layers">
<span id="vector"></span><h1><span class="section-number">6. </span>Using Vector Layers<a class="headerlink" href="#using-vector-layers" title="Link to this heading"></a></h1>
<div class="admonition hint">
<p class="admonition-title">Hint</p>
<p>The code snippets on this page need the following imports if you’re outside the pyqgis console:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="p">(</span>
<span class="linenos"> 2</span>  <span class="n">QgsApplication</span><span class="p">,</span>
<span class="linenos"> 3</span>  <span class="n">QgsDataSourceUri</span><span class="p">,</span>
<span class="linenos"> 4</span>  <span class="n">QgsCategorizedSymbolRenderer</span><span class="p">,</span>
<span class="linenos"> 5</span>  <span class="n">QgsClassificationRange</span><span class="p">,</span>
<span class="linenos"> 6</span>  <span class="n">QgsPointXY</span><span class="p">,</span>
<span class="linenos"> 7</span>  <span class="n">QgsProject</span><span class="p">,</span>
<span class="linenos"> 8</span>  <span class="n">QgsExpression</span><span class="p">,</span>
<span class="linenos"> 9</span>  <span class="n">QgsField</span><span class="p">,</span>
<span class="linenos">10</span>  <span class="n">QgsFields</span><span class="p">,</span>
<span class="linenos">11</span>  <span class="n">QgsFeature</span><span class="p">,</span>
<span class="linenos">12</span>  <span class="n">QgsFeatureRequest</span><span class="p">,</span>
<span class="linenos">13</span>  <span class="n">QgsFeatureRenderer</span><span class="p">,</span>
<span class="linenos">14</span>  <span class="n">QgsGeometry</span><span class="p">,</span>
<span class="linenos">15</span>  <span class="n">QgsGraduatedSymbolRenderer</span><span class="p">,</span>
<span class="linenos">16</span>  <span class="n">QgsMarkerSymbol</span><span class="p">,</span>
<span class="linenos">17</span>  <span class="n">QgsMessageLog</span><span class="p">,</span>
<span class="linenos">18</span>  <span class="n">QgsRectangle</span><span class="p">,</span>
<span class="linenos">19</span>  <span class="n">QgsRendererCategory</span><span class="p">,</span>
<span class="linenos">20</span>  <span class="n">QgsRendererRange</span><span class="p">,</span>
<span class="linenos">21</span>  <span class="n">QgsSymbol</span><span class="p">,</span>
<span class="linenos">22</span>  <span class="n">QgsVectorDataProvider</span><span class="p">,</span>
<span class="linenos">23</span>  <span class="n">QgsVectorLayer</span><span class="p">,</span>
<span class="linenos">24</span>  <span class="n">QgsVectorFileWriter</span><span class="p">,</span>
<span class="linenos">25</span>  <span class="n">QgsWkbTypes</span><span class="p">,</span>
<span class="linenos">26</span>  <span class="n">QgsSpatialIndex</span><span class="p">,</span>
<span class="linenos">27</span>  <span class="n">QgsVectorLayerUtils</span>
<span class="linenos">28</span><span class="p">)</span>
<span class="linenos">29</span>
<span class="linenos">30</span><span class="kn">from</span> <span class="nn">qgis.core.additions.edit</span> <span class="kn">import</span> <span class="n">edit</span>
<span class="linenos">31</span>
<span class="linenos">32</span><span class="kn">from</span> <span class="nn">qgis.PyQt.QtGui</span> <span class="kn">import</span> <span class="p">(</span>
<span class="linenos">33</span>    <span class="n">QColor</span><span class="p">,</span>
<span class="linenos">34</span><span class="p">)</span>
</pre></div>
</div>
</div>
<nav class="contents local" id="contents">
<ul class="simple">
<li><p><a class="reference internal" href="#retrieving-information-about-attributes" id="id1">Retrieving information about attributes</a></p></li>
<li><p><a class="reference internal" href="#iterating-over-vector-layer" id="id2">Iterating over Vector Layer</a></p></li>
<li><p><a class="reference internal" href="#selecting-features" id="id3">Selecting features</a></p>
<ul>
<li><p><a class="reference internal" href="#accessing-attributes" id="id4">Accessing attributes</a></p></li>
<li><p><a class="reference internal" href="#iterating-over-selected-features" id="id5">Iterating over selected features</a></p></li>
<li><p><a class="reference internal" href="#iterating-over-a-subset-of-features" id="id6">Iterating over a subset of features</a></p></li>
</ul>
</li>
<li><p><a class="reference internal" href="#modifying-vector-layers" id="id7">Modifying Vector Layers</a></p>
<ul>
<li><p><a class="reference internal" href="#add-features" id="id8">Add Features</a></p></li>
<li><p><a class="reference internal" href="#delete-features" id="id9">Delete Features</a></p></li>
<li><p><a class="reference internal" href="#modify-features" id="id10">Modify Features</a></p></li>
<li><p><a class="reference internal" href="#modifying-vector-layers-with-an-editing-buffer" id="id11">Modifying Vector Layers with an Editing Buffer</a></p></li>
<li><p><a class="reference internal" href="#adding-and-removing-fields" id="id12">Adding and Removing Fields</a></p></li>
</ul>
</li>
<li><p><a class="reference internal" href="#using-spatial-index" id="id13">Using Spatial Index</a></p></li>
<li><p><a class="reference internal" href="#the-qgsvectorlayerutils-class" id="id14">The QgsVectorLayerUtils class</a></p></li>
<li><p><a class="reference internal" href="#creating-vector-layers" id="id15">Creating Vector Layers</a></p>
<ul>
<li><p><a class="reference internal" href="#from-an-instance-of-qgsvectorfilewriter" id="id16">From an instance of <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorFileWriter.html#qgis.core.QgsVectorFileWriter" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorFileWriter</span></code></a></a></p></li>
<li><p><a class="reference internal" href="#directly-from-features" id="id17">Directly from features</a></p></li>
<li><p><a class="reference internal" href="#from-an-instance-of-qgsvectorlayer" id="id18">From an instance of <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a></a></p></li>
</ul>
</li>
<li><p><a class="reference internal" href="#appearance-symbology-of-vector-layers" id="id19">Appearance (Symbology) of Vector Layers</a></p>
<ul>
<li><p><a class="reference internal" href="#single-symbol-renderer" id="id20">Single Symbol Renderer</a></p></li>
<li><p><a class="reference internal" href="#categorized-symbol-renderer" id="id21">Categorized Symbol Renderer</a></p></li>
<li><p><a class="reference internal" href="#graduated-symbol-renderer" id="id22">Graduated Symbol Renderer</a></p></li>
<li><p><a class="reference internal" href="#working-with-symbols" id="id23">Working with Symbols</a></p>
<ul>
<li><p><a class="reference internal" href="#working-with-symbol-layers" id="id24">Working with Symbol Layers</a></p></li>
<li><p><a class="reference internal" href="#creating-custom-symbol-layer-types" id="id25">Creating Custom Symbol Layer Types</a></p></li>
</ul>
</li>
<li><p><a class="reference internal" href="#creating-custom-renderers" id="id26">Creating Custom Renderers</a></p></li>
</ul>
</li>
<li><p><a class="reference internal" href="#further-topics" id="id27">Further Topics</a></p></li>
</ul>
</nav>
<p>This section summarizes various actions that can be done with vector layers.</p>
<p>Most work here is based on the methods of the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a> class.</p>
<section id="retrieving-information-about-attributes">
<span id="index-0"></span><h2><a class="toc-backref" href="#id1" role="doc-backlink"><span class="section-number">6.1. </span>Retrieving information about attributes</a><a class="headerlink" href="#retrieving-information-about-attributes" title="Link to this heading"></a></h2>
<p>You can retrieve information about the fields associated with a vector layer
by calling <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.fields" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">fields()</span></code></a> on a
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a> object:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">vlayer</span> <span class="o">=</span> <span class="n">QgsVectorLayer</span><span class="p">(</span><span class="s2">&quot;testdata/airports.shp&quot;</span><span class="p">,</span> <span class="s2">&quot;airports&quot;</span><span class="p">,</span> <span class="s2">&quot;ogr&quot;</span><span class="p">)</span>
<span class="k">for</span> <span class="n">field</span> <span class="ow">in</span> <span class="n">vlayer</span><span class="o">.</span><span class="n">fields</span><span class="p">():</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">field</span><span class="o">.</span><span class="n">name</span><span class="p">(),</span> <span class="n">field</span><span class="o">.</span><span class="n">typeName</span><span class="p">())</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span>ID Integer64
<span class="linenos">2</span>fk_region Integer64
<span class="linenos">3</span>ELEV Real
<span class="linenos">4</span>NAME String
<span class="linenos">5</span>USE String
</pre></div>
</div>
<p>The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.displayField" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">displayField()</span></code></a> and
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMapLayer.html#qgis.core.QgsMapLayer.mapTipTemplate" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">mapTipTemplate()</span></code></a> methods provide
information on the field and template used in the <a class="reference internal" href="../user_manual/working_with_vector/vector_properties.html#maptips"><span class="std std-ref">Display Properties</span></a> tab.</p>
<p>When you load a vector layer, a field is always chosen by QGIS as the
<code class="docutils literal notranslate"><span class="pre">Display</span> <span class="pre">Name</span></code>, while the <code class="docutils literal notranslate"><span class="pre">HTML</span> <span class="pre">Map</span> <span class="pre">Tip</span></code> is empty by default. With these
methods you can easily get both:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">vlayer</span> <span class="o">=</span> <span class="n">QgsVectorLayer</span><span class="p">(</span><span class="s2">&quot;testdata/airports.shp&quot;</span><span class="p">,</span> <span class="s2">&quot;airports&quot;</span><span class="p">,</span> <span class="s2">&quot;ogr&quot;</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">vlayer</span><span class="o">.</span><span class="n">displayField</span><span class="p">())</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>NAME
</pre></div>
</div>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>If you change the <code class="docutils literal notranslate"><span class="pre">Display</span> <span class="pre">Name</span></code> from a field to an expression, you have to
use <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.displayExpression" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">displayExpression()</span></code></a>
instead of <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.displayField" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">displayField()</span></code></a>.</p>
</div>
</section>
<section id="iterating-over-vector-layer">
<span id="index-1"></span><h2><a class="toc-backref" href="#id2" role="doc-backlink"><span class="section-number">6.2. </span>Iterating over Vector Layer</a><a class="headerlink" href="#iterating-over-vector-layer" title="Link to this heading"></a></h2>
<p>Iterating over the features in a vector layer is one of the most common tasks.
Below is an example of the simple basic code to perform this task and showing
some information about each feature. The <code class="docutils literal notranslate"><span class="pre">layer</span></code> variable is assumed to have
a <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a> object.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># &quot;layer&quot; is a QgsVectorLayer instance</span>
<span class="linenos"> 2</span><span class="n">layer</span> <span class="o">=</span> <span class="n">iface</span><span class="o">.</span><span class="n">activeLayer</span><span class="p">()</span>
<span class="linenos"> 3</span><span class="n">features</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">getFeatures</span><span class="p">()</span>
<span class="linenos"> 4</span>
<span class="linenos"> 5</span><span class="k">for</span> <span class="n">feature</span> <span class="ow">in</span> <span class="n">features</span><span class="p">:</span>
<span class="linenos"> 6</span>    <span class="c1"># retrieve every feature with its geometry and attributes</span>
<span class="linenos"> 7</span>    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Feature ID: &quot;</span><span class="p">,</span> <span class="n">feature</span><span class="o">.</span><span class="n">id</span><span class="p">())</span>
<span class="linenos"> 8</span>    <span class="c1"># fetch geometry</span>
<span class="linenos"> 9</span>    <span class="c1"># show some information about the feature geometry</span>
<span class="linenos">10</span>    <span class="n">geom</span> <span class="o">=</span> <span class="n">feature</span><span class="o">.</span><span class="n">geometry</span><span class="p">()</span>
<span class="linenos">11</span>    <span class="n">geomSingleType</span> <span class="o">=</span> <span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">isSingleType</span><span class="p">(</span><span class="n">geom</span><span class="o">.</span><span class="n">wkbType</span><span class="p">())</span>
<span class="linenos">12</span>    <span class="k">if</span> <span class="n">geom</span><span class="o">.</span><span class="n">type</span><span class="p">()</span> <span class="o">==</span> <span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">PointGeometry</span><span class="p">:</span>
<span class="linenos">13</span>        <span class="c1"># the geometry type can be of single or multi type</span>
<span class="linenos">14</span>        <span class="k">if</span> <span class="n">geomSingleType</span><span class="p">:</span>
<span class="linenos">15</span>            <span class="n">x</span> <span class="o">=</span> <span class="n">geom</span><span class="o">.</span><span class="n">asPoint</span><span class="p">()</span>
<span class="linenos">16</span>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Point: &quot;</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span>
<span class="linenos">17</span>        <span class="k">else</span><span class="p">:</span>
<span class="linenos">18</span>            <span class="n">x</span> <span class="o">=</span> <span class="n">geom</span><span class="o">.</span><span class="n">asMultiPoint</span><span class="p">()</span>
<span class="linenos">19</span>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;MultiPoint: &quot;</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span>
<span class="linenos">20</span>    <span class="k">elif</span> <span class="n">geom</span><span class="o">.</span><span class="n">type</span><span class="p">()</span> <span class="o">==</span> <span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">LineGeometry</span><span class="p">:</span>
<span class="linenos">21</span>        <span class="k">if</span> <span class="n">geomSingleType</span><span class="p">:</span>
<span class="linenos">22</span>            <span class="n">x</span> <span class="o">=</span> <span class="n">geom</span><span class="o">.</span><span class="n">asPolyline</span><span class="p">()</span>
<span class="linenos">23</span>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Line: &quot;</span><span class="p">,</span> <span class="n">x</span><span class="p">,</span> <span class="s2">&quot;length: &quot;</span><span class="p">,</span> <span class="n">geom</span><span class="o">.</span><span class="n">length</span><span class="p">())</span>
<span class="linenos">24</span>        <span class="k">else</span><span class="p">:</span>
<span class="linenos">25</span>            <span class="n">x</span> <span class="o">=</span> <span class="n">geom</span><span class="o">.</span><span class="n">asMultiPolyline</span><span class="p">()</span>
<span class="linenos">26</span>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;MultiLine: &quot;</span><span class="p">,</span> <span class="n">x</span><span class="p">,</span> <span class="s2">&quot;length: &quot;</span><span class="p">,</span> <span class="n">geom</span><span class="o">.</span><span class="n">length</span><span class="p">())</span>
<span class="linenos">27</span>    <span class="k">elif</span> <span class="n">geom</span><span class="o">.</span><span class="n">type</span><span class="p">()</span> <span class="o">==</span> <span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">PolygonGeometry</span><span class="p">:</span>
<span class="linenos">28</span>        <span class="k">if</span> <span class="n">geomSingleType</span><span class="p">:</span>
<span class="linenos">29</span>            <span class="n">x</span> <span class="o">=</span> <span class="n">geom</span><span class="o">.</span><span class="n">asPolygon</span><span class="p">()</span>
<span class="linenos">30</span>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Polygon: &quot;</span><span class="p">,</span> <span class="n">x</span><span class="p">,</span> <span class="s2">&quot;Area: &quot;</span><span class="p">,</span> <span class="n">geom</span><span class="o">.</span><span class="n">area</span><span class="p">())</span>
<span class="linenos">31</span>        <span class="k">else</span><span class="p">:</span>
<span class="linenos">32</span>            <span class="n">x</span> <span class="o">=</span> <span class="n">geom</span><span class="o">.</span><span class="n">asMultiPolygon</span><span class="p">()</span>
<span class="linenos">33</span>            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;MultiPolygon: &quot;</span><span class="p">,</span> <span class="n">x</span><span class="p">,</span> <span class="s2">&quot;Area: &quot;</span><span class="p">,</span> <span class="n">geom</span><span class="o">.</span><span class="n">area</span><span class="p">())</span>
<span class="linenos">34</span>    <span class="k">else</span><span class="p">:</span>
<span class="linenos">35</span>        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Unknown or invalid geometry&quot;</span><span class="p">)</span>
<span class="linenos">36</span>    <span class="c1"># fetch attributes</span>
<span class="linenos">37</span>    <span class="n">attrs</span> <span class="o">=</span> <span class="n">feature</span><span class="o">.</span><span class="n">attributes</span><span class="p">()</span>
<span class="linenos">38</span>    <span class="c1"># attrs is a list. It contains all the attribute values of this feature</span>
<span class="linenos">39</span>    <span class="nb">print</span><span class="p">(</span><span class="n">attrs</span><span class="p">)</span>
<span class="linenos">40</span>    <span class="c1"># for this test only print the first feature</span>
<span class="linenos">41</span>    <span class="k">break</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>Feature ID:  1
Point:  &lt;QgsPointXY: POINT(7 45)&gt;
[1, &#39;First feature&#39;]
</pre></div>
</div>
</section>
<section id="selecting-features">
<span id="index-2"></span><h2><a class="toc-backref" href="#id3" role="doc-backlink"><span class="section-number">6.3. </span>Selecting features</a><a class="headerlink" href="#selecting-features" title="Link to this heading"></a></h2>
<p>In QGIS desktop, features can be selected in different ways: the user can click
on a feature, draw a rectangle on the map canvas or use an expression filter.
Selected features are normally highlighted in a different color (default
is yellow) to draw user’s attention on the selection.</p>
<p>Sometimes it can be useful to programmatically select features or to change the
default color.</p>
<p>To select all the features, the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.selectAll" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">selectAll()</span></code></a> method can be used:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="c1"># Get the active layer (must be a vector layer)</span>
<span class="n">layer</span> <span class="o">=</span> <span class="n">iface</span><span class="o">.</span><span class="n">activeLayer</span><span class="p">()</span>
<span class="n">layer</span><span class="o">.</span><span class="n">selectAll</span><span class="p">()</span>
</pre></div>
</div>
<p>To select using an expression, use the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.selectByExpression" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">selectByExpression()</span></code></a> method:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="c1"># Assumes that the active layer is points.shp file from the QGIS test suite</span>
<span class="c1"># (Class (string) and Heading (number) are attributes in points.shp)</span>
<span class="n">layer</span> <span class="o">=</span> <span class="n">iface</span><span class="o">.</span><span class="n">activeLayer</span><span class="p">()</span>
<span class="n">layer</span><span class="o">.</span><span class="n">selectByExpression</span><span class="p">(</span><span class="s1">&#39;&quot;Class&quot;=</span><span class="se">\&#39;</span><span class="s1">B52</span><span class="se">\&#39;</span><span class="s1"> and &quot;Heading&quot; &gt; 10 and &quot;Heading&quot; &lt;70&#39;</span><span class="p">,</span> <span class="n">QgsVectorLayer</span><span class="o">.</span><span class="n">SetSelection</span><span class="p">)</span>
</pre></div>
</div>
<p>To change the selection color you can use <a class="reference external" href="https://qgis.org/pyqgis/3.34/gui/QgsMapCanvas.html#qgis.gui.QgsMapCanvas.setSelectionColor" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setSelectionColor()</span></code></a> method of
<a class="reference external" href="https://qgis.org/pyqgis/3.34/gui/QgsMapCanvas.html#qgis.gui.QgsMapCanvas" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsMapCanvas</span></code></a> as shown in the following example:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">iface</span><span class="o">.</span><span class="n">mapCanvas</span><span class="p">()</span><span class="o">.</span><span class="n">setSelectionColor</span><span class="p">(</span> <span class="n">QColor</span><span class="p">(</span><span class="s2">&quot;red&quot;</span><span class="p">)</span> <span class="p">)</span>
</pre></div>
</div>
<p>To add features to the selected features list for a given layer, you
can call <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.select" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">select()</span></code></a> passing to it the list of features IDs:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="n">selected_fid</span> <span class="o">=</span> <span class="p">[]</span>
<span class="linenos">2</span>
<span class="linenos">3</span><span class="c1"># Get the first feature id from the layer</span>
<span class="linenos">4</span><span class="n">feature</span> <span class="o">=</span> <span class="nb">next</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">getFeatures</span><span class="p">())</span>
<span class="linenos">5</span><span class="k">if</span> <span class="n">feature</span><span class="p">:</span>
<span class="linenos">6</span>    <span class="n">selected_fid</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">feature</span><span class="o">.</span><span class="n">id</span><span class="p">())</span>
<span class="linenos">7</span>
<span class="linenos">8</span><span class="c1"># Add that features to the selected list</span>
<span class="linenos">9</span><span class="n">layer</span><span class="o">.</span><span class="n">select</span><span class="p">(</span><span class="n">selected_fid</span><span class="p">)</span>
</pre></div>
</div>
<p>To clear the selection:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">layer</span><span class="o">.</span><span class="n">removeSelection</span><span class="p">()</span>
</pre></div>
</div>
<section id="accessing-attributes">
<h3><a class="toc-backref" href="#id4" role="doc-backlink"><span class="section-number">6.3.1. </span>Accessing attributes</a><a class="headerlink" href="#accessing-attributes" title="Link to this heading"></a></h3>
<p>Attributes can be referred to by their name:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="n">feature</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">])</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>First feature
</pre></div>
</div>
<p>Alternatively, attributes can be referred to by index.
This is a bit faster than using the name.
For example, to get the second attribute:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="n">feature</span><span class="p">[</span><span class="mi">1</span><span class="p">])</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>First feature
</pre></div>
</div>
</section>
<section id="iterating-over-selected-features">
<h3><a class="toc-backref" href="#id5" role="doc-backlink"><span class="section-number">6.3.2. </span>Iterating over selected features</a><a class="headerlink" href="#iterating-over-selected-features" title="Link to this heading"></a></h3>
<p>If you only need selected features, you can use the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.selectedFeatures" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">selectedFeatures()</span></code></a> method from the vector layer:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">selection</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">selectedFeatures</span><span class="p">()</span>
<span class="k">for</span> <span class="n">feature</span> <span class="ow">in</span> <span class="n">selection</span><span class="p">:</span>
    <span class="c1"># do whatever you need with the feature</span>
    <span class="k">pass</span>
</pre></div>
</div>
</section>
<section id="iterating-over-a-subset-of-features">
<h3><a class="toc-backref" href="#id6" role="doc-backlink"><span class="section-number">6.3.3. </span>Iterating over a subset of features</a><a class="headerlink" href="#iterating-over-a-subset-of-features" title="Link to this heading"></a></h3>
<p>If you want to iterate over a given subset of features in a layer, such as
those within a given area, you have to add a <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRequest.html#qgis.core.QgsFeatureRequest" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFeatureRequest</span></code></a> object
to the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.getFeatures" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">getFeatures()</span></code></a> call. Here’s an example:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="n">areaOfInterest</span> <span class="o">=</span> <span class="n">QgsRectangle</span><span class="p">(</span><span class="mi">450290</span><span class="p">,</span><span class="mi">400520</span><span class="p">,</span> <span class="mi">450750</span><span class="p">,</span><span class="mi">400780</span><span class="p">)</span>
<span class="linenos">2</span>
<span class="linenos">3</span><span class="n">request</span> <span class="o">=</span> <span class="n">QgsFeatureRequest</span><span class="p">()</span><span class="o">.</span><span class="n">setFilterRect</span><span class="p">(</span><span class="n">areaOfInterest</span><span class="p">)</span>
<span class="linenos">4</span>
<span class="linenos">5</span><span class="k">for</span> <span class="n">feature</span> <span class="ow">in</span> <span class="n">layer</span><span class="o">.</span><span class="n">getFeatures</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="linenos">6</span>    <span class="c1"># do whatever you need with the feature</span>
<span class="linenos">7</span>    <span class="k">pass</span>
</pre></div>
</div>
<p>For the sake of speed, the intersection is often done only using feature’s
bounding box. There is however a flag <code class="docutils literal notranslate"><span class="pre">ExactIntersect</span></code> that makes sure that
only intersecting features will be returned:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">request</span> <span class="o">=</span> <span class="n">QgsFeatureRequest</span><span class="p">()</span><span class="o">.</span><span class="n">setFilterRect</span><span class="p">(</span><span class="n">areaOfInterest</span><span class="p">)</span> \
                             <span class="o">.</span><span class="n">setFlags</span><span class="p">(</span><span class="n">QgsFeatureRequest</span><span class="o">.</span><span class="n">ExactIntersect</span><span class="p">)</span>
</pre></div>
</div>
<p>With <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRequest.html#qgis.core.QgsFeatureRequest.setLimit" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setLimit()</span></code></a> you can limit the number of requested features.
Here’s an example:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">request</span> <span class="o">=</span> <span class="n">QgsFeatureRequest</span><span class="p">()</span>
<span class="n">request</span><span class="o">.</span><span class="n">setLimit</span><span class="p">(</span><span class="mi">2</span><span class="p">)</span>
<span class="k">for</span> <span class="n">feature</span> <span class="ow">in</span> <span class="n">layer</span><span class="o">.</span><span class="n">getFeatures</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">feature</span><span class="p">)</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>&lt;qgis._core.QgsFeature object at 0x7f9b78590948&gt;
&lt;qgis._core.QgsFeature object at 0x7faef5881670&gt;
</pre></div>
</div>
<p>If you need an attribute-based filter instead (or in addition) of a spatial
one like shown in the examples above, you can build a <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsExpression.html#qgis.core.QgsExpression" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsExpression</span></code></a> object and pass it to the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRequest.html#qgis.core.QgsFeatureRequest" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFeatureRequest</span></code></a> constructor. Here’s an example:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="c1"># The expression will filter the features where the field &quot;location_name&quot;</span>
<span class="c1"># contains the word &quot;Lake&quot; (case insensitive)</span>
<span class="n">exp</span> <span class="o">=</span> <span class="n">QgsExpression</span><span class="p">(</span><span class="s1">&#39;location_name ILIKE </span><span class="se">\&#39;</span><span class="si">%La</span><span class="s1">ke%</span><span class="se">\&#39;</span><span class="s1">&#39;</span><span class="p">)</span>
<span class="n">request</span> <span class="o">=</span> <span class="n">QgsFeatureRequest</span><span class="p">(</span><span class="n">exp</span><span class="p">)</span>
</pre></div>
</div>
<p>See <a class="reference internal" href="expressions.html#expressions"><span class="std std-ref">Expressions, Filtering and Calculating Values</span></a> for the details about the syntax supported by <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsExpression.html#qgis.core.QgsExpression" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsExpression</span></code></a>.</p>
<p>The request can be used to define the data retrieved for each feature, so the
iterator returns all features, but returns partial data for each of them.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># Only return selected fields to increase the &quot;speed&quot; of the request</span>
<span class="linenos"> 2</span><span class="n">request</span><span class="o">.</span><span class="n">setSubsetOfAttributes</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span><span class="mi">2</span><span class="p">])</span>
<span class="linenos"> 3</span>
<span class="linenos"> 4</span><span class="c1"># More user friendly version</span>
<span class="linenos"> 5</span><span class="n">request</span><span class="o">.</span><span class="n">setSubsetOfAttributes</span><span class="p">([</span><span class="s1">&#39;name&#39;</span><span class="p">,</span><span class="s1">&#39;id&#39;</span><span class="p">],</span><span class="n">layer</span><span class="o">.</span><span class="n">fields</span><span class="p">())</span>
<span class="linenos"> 6</span>
<span class="linenos"> 7</span><span class="c1"># Don&#39;t return geometry objects to increase the &quot;speed&quot; of the request</span>
<span class="linenos"> 8</span><span class="n">request</span><span class="o">.</span><span class="n">setFlags</span><span class="p">(</span><span class="n">QgsFeatureRequest</span><span class="o">.</span><span class="n">NoGeometry</span><span class="p">)</span>
<span class="linenos"> 9</span>
<span class="linenos">10</span><span class="c1"># Fetch only the feature with id 45</span>
<span class="linenos">11</span><span class="n">request</span><span class="o">.</span><span class="n">setFilterFid</span><span class="p">(</span><span class="mi">45</span><span class="p">)</span>
<span class="linenos">12</span>
<span class="linenos">13</span><span class="c1"># The options may be chained</span>
<span class="linenos">14</span><span class="n">request</span><span class="o">.</span><span class="n">setFilterRect</span><span class="p">(</span><span class="n">areaOfInterest</span><span class="p">)</span><span class="o">.</span><span class="n">setFlags</span><span class="p">(</span><span class="n">QgsFeatureRequest</span><span class="o">.</span><span class="n">NoGeometry</span><span class="p">)</span><span class="o">.</span><span class="n">setFilterFid</span><span class="p">(</span><span class="mi">45</span><span class="p">)</span><span class="o">.</span><span class="n">setSubsetOfAttributes</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span><span class="mi">2</span><span class="p">])</span>
</pre></div>
</div>
</section>
</section>
<section id="modifying-vector-layers">
<span id="editing"></span><span id="index-3"></span><h2><a class="toc-backref" href="#id7" role="doc-backlink"><span class="section-number">6.4. </span>Modifying Vector Layers</a><a class="headerlink" href="#modifying-vector-layers" title="Link to this heading"></a></h2>
<p>Most vector data providers support editing of layer data. Sometimes they support
just a subset of possible editing actions. Use the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorDataProvider.html#qgis.core.QgsVectorDataProvider.capabilities" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">capabilities()</span></code></a> function
to find out what set of functionality is supported.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">caps</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">capabilities</span><span class="p">()</span>
<span class="c1"># Check if a particular capability is supported:</span>
<span class="k">if</span> <span class="n">caps</span> <span class="o">&amp;</span> <span class="n">QgsVectorDataProvider</span><span class="o">.</span><span class="n">DeleteFeatures</span><span class="p">:</span>
    <span class="nb">print</span><span class="p">(</span><span class="s1">&#39;The layer supports DeleteFeatures&#39;</span><span class="p">)</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>The layer supports DeleteFeatures
</pre></div>
</div>
<p>For a list of all available capabilities, please refer to the
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorDataProvider.html#qgis.core.QgsVectorDataProvider" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">API</span> <span class="pre">Documentation</span> <span class="pre">of</span> <span class="pre">QgsVectorDataProvider</span></code></a>.</p>
<p>To print layer’s capabilities textual description in a comma separated list you
can use <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorDataProvider.html#qgis.core.QgsVectorDataProvider.capabilitiesString" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">capabilitiesString()</span></code></a>
as in the following example:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="n">caps_string</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">capabilitiesString</span><span class="p">()</span>
<span class="linenos">2</span><span class="c1"># Print:</span>
<span class="linenos">3</span><span class="c1"># &#39;Add Features, Delete Features, Change Attribute Values, Add Attributes,</span>
<span class="linenos">4</span><span class="c1"># Delete Attributes, Rename Attributes, Fast Access to Features at ID,</span>
<span class="linenos">5</span><span class="c1"># Presimplify Geometries, Presimplify Geometries with Validity Check,</span>
<span class="linenos">6</span><span class="c1"># Transactions, Curved Geometries&#39;</span>
</pre></div>
</div>
<p>By using any of the following methods for vector layer editing, the changes are
directly committed to the underlying data store (a file, database etc). In case
you would like to do only temporary changes, skip to the next section that
explains how to do <a class="reference internal" href="#editing-buffer"><span class="std std-ref">modifications with editing buffer</span></a>.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>If you are working inside QGIS (either from the console or from a plugin),
it might be necessary to force a redraw of the map canvas in order to see
the changes you’ve done to the geometry, to the style or to the attributes:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="c1"># If caching is enabled, a simple canvas refresh might not be sufficient</span>
<span class="linenos">2</span><span class="c1"># to trigger a redraw and you must clear the cached image for the layer</span>
<span class="linenos">3</span><span class="k">if</span> <span class="n">iface</span><span class="o">.</span><span class="n">mapCanvas</span><span class="p">()</span><span class="o">.</span><span class="n">isCachingEnabled</span><span class="p">():</span>
<span class="linenos">4</span>    <span class="n">layer</span><span class="o">.</span><span class="n">triggerRepaint</span><span class="p">()</span>
<span class="linenos">5</span><span class="k">else</span><span class="p">:</span>
<span class="linenos">6</span>    <span class="n">iface</span><span class="o">.</span><span class="n">mapCanvas</span><span class="p">()</span><span class="o">.</span><span class="n">refresh</span><span class="p">()</span>
</pre></div>
</div>
</div>
<section id="add-features">
<h3><a class="toc-backref" href="#id8" role="doc-backlink"><span class="section-number">6.4.1. </span>Add Features</a><a class="headerlink" href="#add-features" title="Link to this heading"></a></h3>
<p>Create some <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeature.html#qgis.core.QgsFeature" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFeature</span></code></a> instances and pass a list of them to the provider
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorDataProvider.html#qgis.core.QgsVectorDataProvider" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorDataProvider</span></code></a> <code class="docutils literal notranslate"><span class="pre">addFeatures()</span></code> method. It will return two values:
result (<code class="xref py py-const docutils literal notranslate"><span class="pre">True</span></code> or <code class="xref py py-const docutils literal notranslate"><span class="pre">False</span></code>) and
list of added features (their ID is set by the data store).</p>
<p>To set up the attributes of the feature, you can either initialize the feature passing a
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFields.html#qgis.core.QgsFields" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFields</span></code></a> object (you can obtain that from the
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.fields" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">fields()</span></code></a> method of the vector layer)
or call <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeature.html#qgis.core.QgsFeature.initAttributes" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">initAttributes()</span></code></a> passing
the number of fields you want to be added.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="k">if</span> <span class="n">caps</span> <span class="o">&amp;</span> <span class="n">QgsVectorDataProvider</span><span class="o">.</span><span class="n">AddFeatures</span><span class="p">:</span>
<span class="linenos">2</span>    <span class="n">feat</span> <span class="o">=</span> <span class="n">QgsFeature</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">fields</span><span class="p">())</span>
<span class="linenos">3</span>    <span class="n">feat</span><span class="o">.</span><span class="n">setAttributes</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="s1">&#39;hello&#39;</span><span class="p">])</span>
<span class="linenos">4</span>    <span class="c1"># Or set a single attribute by key or by index:</span>
<span class="linenos">5</span>    <span class="n">feat</span><span class="o">.</span><span class="n">setAttribute</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="s1">&#39;hello&#39;</span><span class="p">)</span>
<span class="linenos">6</span>    <span class="n">feat</span><span class="o">.</span><span class="n">setAttribute</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="s1">&#39;hello&#39;</span><span class="p">)</span>
<span class="linenos">7</span>    <span class="n">feat</span><span class="o">.</span><span class="n">setGeometry</span><span class="p">(</span><span class="n">QgsGeometry</span><span class="o">.</span><span class="n">fromPointXY</span><span class="p">(</span><span class="n">QgsPointXY</span><span class="p">(</span><span class="mi">123</span><span class="p">,</span> <span class="mi">456</span><span class="p">)))</span>
<span class="linenos">8</span>    <span class="p">(</span><span class="n">res</span><span class="p">,</span> <span class="n">outFeats</span><span class="p">)</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">addFeatures</span><span class="p">([</span><span class="n">feat</span><span class="p">])</span>
</pre></div>
</div>
</section>
<section id="delete-features">
<h3><a class="toc-backref" href="#id9" role="doc-backlink"><span class="section-number">6.4.2. </span>Delete Features</a><a class="headerlink" href="#delete-features" title="Link to this heading"></a></h3>
<p>To delete some features, just provide a list of their feature IDs.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="k">if</span> <span class="n">caps</span> <span class="o">&amp;</span> <span class="n">QgsVectorDataProvider</span><span class="o">.</span><span class="n">DeleteFeatures</span><span class="p">:</span>
    <span class="n">res</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">deleteFeatures</span><span class="p">([</span><span class="mi">5</span><span class="p">,</span> <span class="mi">10</span><span class="p">])</span>
</pre></div>
</div>
</section>
<section id="modify-features">
<h3><a class="toc-backref" href="#id10" role="doc-backlink"><span class="section-number">6.4.3. </span>Modify Features</a><a class="headerlink" href="#modify-features" title="Link to this heading"></a></h3>
<p>It is possible to either change feature’s geometry or to change some attributes.
The following example first changes values of attributes with index 0 and 1,
then it changes the feature’s geometry.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="n">fid</span> <span class="o">=</span> <span class="mi">100</span>   <span class="c1"># ID of the feature we will modify</span>
<span class="linenos">2</span>
<span class="linenos">3</span><span class="k">if</span> <span class="n">caps</span> <span class="o">&amp;</span> <span class="n">QgsVectorDataProvider</span><span class="o">.</span><span class="n">ChangeAttributeValues</span><span class="p">:</span>
<span class="linenos">4</span>    <span class="n">attrs</span> <span class="o">=</span> <span class="p">{</span> <span class="mi">0</span> <span class="p">:</span> <span class="s2">&quot;hello&quot;</span><span class="p">,</span> <span class="mi">1</span> <span class="p">:</span> <span class="mi">123</span> <span class="p">}</span>
<span class="linenos">5</span>    <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">changeAttributeValues</span><span class="p">({</span> <span class="n">fid</span> <span class="p">:</span> <span class="n">attrs</span> <span class="p">})</span>
<span class="linenos">6</span>
<span class="linenos">7</span><span class="k">if</span> <span class="n">caps</span> <span class="o">&amp;</span> <span class="n">QgsVectorDataProvider</span><span class="o">.</span><span class="n">ChangeGeometries</span><span class="p">:</span>
<span class="linenos">8</span>    <span class="n">geom</span> <span class="o">=</span> <span class="n">QgsGeometry</span><span class="o">.</span><span class="n">fromPointXY</span><span class="p">(</span><span class="n">QgsPointXY</span><span class="p">(</span><span class="mi">111</span><span class="p">,</span><span class="mi">222</span><span class="p">))</span>
<span class="linenos">9</span>    <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">changeGeometryValues</span><span class="p">({</span> <span class="n">fid</span> <span class="p">:</span> <span class="n">geom</span> <span class="p">})</span>
</pre></div>
</div>
<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p><strong>Favor QgsVectorLayerEditUtils class for geometry-only edits</strong></p>
<p>If you only need to change geometries, you might consider using
the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayerEditUtils.html#qgis.core.QgsVectorLayerEditUtils" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayerEditUtils</span></code></a> which provides some useful
methods to edit geometries (translate, insert or move vertex, etc.).</p>
</div>
</section>
<section id="modifying-vector-layers-with-an-editing-buffer">
<span id="editing-buffer"></span><h3><a class="toc-backref" href="#id11" role="doc-backlink"><span class="section-number">6.4.4. </span>Modifying Vector Layers with an Editing Buffer</a><a class="headerlink" href="#modifying-vector-layers-with-an-editing-buffer" title="Link to this heading"></a></h3>
<p>When editing vectors within QGIS application, you have to first start editing
mode for a particular layer, then do some modifications and finally commit (or
rollback) the changes. All the changes you make are not written until you commit
them — they stay in layer’s in-memory editing buffer. It is possible to use
this functionality also programmatically — it is just another method for
vector layer editing that complements the direct usage of data providers. Use
this option when providing some GUI tools for vector layer editing, since this
will allow user to decide whether to commit/rollback and allows the usage of
undo/redo. When changes are committed, all changes from the editing buffer are
saved to data provider.</p>
<p>The methods are similar to the ones we have seen in the provider, but they are
called on the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a>
object instead.</p>
<p>For these methods to work, the layer must be in editing mode. To start the editing mode,
use the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.startEditing" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">startEditing()</span></code></a> method.
To stop editing, use the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.commitChanges" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">commitChanges()</span></code></a>
or <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.rollBack" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">rollBack()</span></code></a> methods.
The first one will commit all your changes to the data source, while the second
one will discard them and will not modify the data source at all.</p>
<p>To find out whether a layer is in editing mode, use the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.isEditable" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">isEditable()</span></code></a> method.</p>
<p>Here you have some examples that demonstrate how to use these editing methods.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.PyQt.QtCore</span> <span class="kn">import</span> <span class="n">QVariant</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="n">feat1</span> <span class="o">=</span> <span class="n">feat2</span> <span class="o">=</span> <span class="n">QgsFeature</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">fields</span><span class="p">())</span>
<span class="linenos"> 4</span><span class="n">fid</span> <span class="o">=</span> <span class="mi">99</span>
<span class="linenos"> 5</span><span class="n">feat1</span><span class="o">.</span><span class="n">setId</span><span class="p">(</span><span class="n">fid</span><span class="p">)</span>
<span class="linenos"> 6</span>
<span class="linenos"> 7</span><span class="c1"># add two features (QgsFeature instances)</span>
<span class="linenos"> 8</span><span class="n">layer</span><span class="o">.</span><span class="n">addFeatures</span><span class="p">([</span><span class="n">feat1</span><span class="p">,</span><span class="n">feat2</span><span class="p">])</span>
<span class="linenos"> 9</span><span class="c1"># delete a feature with specified ID</span>
<span class="linenos">10</span><span class="n">layer</span><span class="o">.</span><span class="n">deleteFeature</span><span class="p">(</span><span class="n">fid</span><span class="p">)</span>
<span class="linenos">11</span>
<span class="linenos">12</span><span class="c1"># set new geometry (QgsGeometry instance) for a feature</span>
<span class="linenos">13</span><span class="n">geometry</span> <span class="o">=</span> <span class="n">QgsGeometry</span><span class="o">.</span><span class="n">fromWkt</span><span class="p">(</span><span class="s2">&quot;POINT(7 45)&quot;</span><span class="p">)</span>
<span class="linenos">14</span><span class="n">layer</span><span class="o">.</span><span class="n">changeGeometry</span><span class="p">(</span><span class="n">fid</span><span class="p">,</span> <span class="n">geometry</span><span class="p">)</span>
<span class="linenos">15</span><span class="c1"># update an attribute with given field index (int) to a given value</span>
<span class="linenos">16</span><span class="n">fieldIndex</span> <span class="o">=</span><span class="mi">1</span>
<span class="linenos">17</span><span class="n">value</span> <span class="o">=</span><span class="s1">&#39;My new name&#39;</span>
<span class="linenos">18</span><span class="n">layer</span><span class="o">.</span><span class="n">changeAttributeValue</span><span class="p">(</span><span class="n">fid</span><span class="p">,</span> <span class="n">fieldIndex</span><span class="p">,</span> <span class="n">value</span><span class="p">)</span>
<span class="linenos">19</span>
<span class="linenos">20</span><span class="c1"># add new field</span>
<span class="linenos">21</span><span class="n">layer</span><span class="o">.</span><span class="n">addAttribute</span><span class="p">(</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;mytext&quot;</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">String</span><span class="p">))</span>
<span class="linenos">22</span><span class="c1"># remove a field</span>
<span class="linenos">23</span><span class="n">layer</span><span class="o">.</span><span class="n">deleteAttribute</span><span class="p">(</span><span class="n">fieldIndex</span><span class="p">)</span>
</pre></div>
</div>
<p>In order to make undo/redo work properly, the above mentioned calls have to be
wrapped into undo commands. (If you do not care about undo/redo and want to
have the changes stored immediately, then you will have easier work by
<a class="reference internal" href="#editing"><span class="std std-ref">editing with data provider</span></a>.)</p>
<p>Here is how you can use the undo functionality:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="n">layer</span><span class="o">.</span><span class="n">beginEditCommand</span><span class="p">(</span><span class="s2">&quot;Feature triangulation&quot;</span><span class="p">)</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="c1"># ... call layer&#39;s editing methods ...</span>
<span class="linenos"> 4</span>
<span class="linenos"> 5</span><span class="k">if</span> <span class="n">problem_occurred</span><span class="p">:</span>
<span class="linenos"> 6</span>  <span class="n">layer</span><span class="o">.</span><span class="n">destroyEditCommand</span><span class="p">()</span>
<span class="linenos"> 7</span>  <span class="c1"># ... tell the user that there was a problem</span>
<span class="linenos"> 8</span>  <span class="c1"># and return</span>
<span class="linenos"> 9</span>
<span class="linenos">10</span><span class="c1"># ... more editing ...</span>
<span class="linenos">11</span>
<span class="linenos">12</span><span class="n">layer</span><span class="o">.</span><span class="n">endEditCommand</span><span class="p">()</span>
</pre></div>
</div>
<p>The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.beginEditCommand" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">beginEditCommand()</span></code></a> method will create an internal “active” command and will
record subsequent changes in vector layer. With the call to <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.endEditCommand" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">endEditCommand()</span></code></a>
the command is pushed onto the undo stack and the user will be able to undo/redo
it from GUI. In case something went wrong while doing the changes, the
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.destroyEditCommand" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">destroyEditCommand()</span></code></a> method will remove the command and rollback all
changes done while this command was active.</p>
<p>You can also use the <code class="code docutils literal notranslate"><span class="pre">with</span> <span class="pre">edit(layer)</span></code>-statement to wrap commit and rollback into
a more semantic code block as shown in the example below:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="k">with</span> <span class="n">edit</span><span class="p">(</span><span class="n">layer</span><span class="p">):</span>
  <span class="n">feat</span> <span class="o">=</span> <span class="nb">next</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">getFeatures</span><span class="p">())</span>
  <span class="n">feat</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="mi">5</span>
  <span class="n">layer</span><span class="o">.</span><span class="n">updateFeature</span><span class="p">(</span><span class="n">feat</span><span class="p">)</span>
</pre></div>
</div>
<p>This will automatically call <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.commitChanges" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">commitChanges()</span></code></a> in the end.
If any exception occurs, it will <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.rollBack" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">rollBack()</span></code></a> all the changes.
In case a problem is encountered within <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.commitChanges" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">commitChanges()</span></code></a> (when the method
returns False) a <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsEditError.html#qgis.core.QgsEditError" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsEditError</span></code></a> exception will be raised.</p>
</section>
<section id="adding-and-removing-fields">
<h3><a class="toc-backref" href="#id12" role="doc-backlink"><span class="section-number">6.4.5. </span>Adding and Removing Fields</a><a class="headerlink" href="#adding-and-removing-fields" title="Link to this heading"></a></h3>
<p>To add fields (attributes), you need to specify a list of field definitions.
For deletion of fields just provide a list of field indexes.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="kn">from</span> <span class="nn">qgis.PyQt.QtCore</span> <span class="kn">import</span> <span class="n">QVariant</span>
<span class="linenos">2</span>
<span class="linenos">3</span><span class="k">if</span> <span class="n">caps</span> <span class="o">&amp;</span> <span class="n">QgsVectorDataProvider</span><span class="o">.</span><span class="n">AddAttributes</span><span class="p">:</span>
<span class="linenos">4</span>    <span class="n">res</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">addAttributes</span><span class="p">(</span>
<span class="linenos">5</span>        <span class="p">[</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;mytext&quot;</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">String</span><span class="p">),</span>
<span class="linenos">6</span>        <span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;myint&quot;</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">Int</span><span class="p">)])</span>
<span class="linenos">7</span>
<span class="linenos">8</span><span class="k">if</span> <span class="n">caps</span> <span class="o">&amp;</span> <span class="n">QgsVectorDataProvider</span><span class="o">.</span><span class="n">DeleteAttributes</span><span class="p">:</span>
<span class="linenos">9</span>    <span class="n">res</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">deleteAttributes</span><span class="p">([</span><span class="mi">0</span><span class="p">])</span>
</pre></div>
</div>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># Alternate methods for removing fields</span>
<span class="linenos"> 2</span><span class="c1"># first create temporary fields to be removed (f1-3)</span>
<span class="linenos"> 3</span><span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">addAttributes</span><span class="p">([</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;f1&quot;</span><span class="p">,</span><span class="n">QVariant</span><span class="o">.</span><span class="n">Int</span><span class="p">),</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;f2&quot;</span><span class="p">,</span><span class="n">QVariant</span><span class="o">.</span><span class="n">Int</span><span class="p">),</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;f3&quot;</span><span class="p">,</span><span class="n">QVariant</span><span class="o">.</span><span class="n">Int</span><span class="p">)])</span>
<span class="linenos"> 4</span><span class="n">layer</span><span class="o">.</span><span class="n">updateFields</span><span class="p">()</span>
<span class="linenos"> 5</span><span class="n">count</span><span class="o">=</span><span class="n">layer</span><span class="o">.</span><span class="n">fields</span><span class="p">()</span><span class="o">.</span><span class="n">count</span><span class="p">()</span> <span class="c1"># count of layer fields</span>
<span class="linenos"> 6</span><span class="n">ind_list</span><span class="o">=</span><span class="nb">list</span><span class="p">((</span><span class="n">count</span><span class="o">-</span><span class="mi">3</span><span class="p">,</span> <span class="n">count</span><span class="o">-</span><span class="mi">2</span><span class="p">))</span> <span class="c1"># create list</span>
<span class="linenos"> 7</span>
<span class="linenos"> 8</span><span class="c1"># remove a single field with an index</span>
<span class="linenos"> 9</span><span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">deleteAttributes</span><span class="p">([</span><span class="n">count</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span>
<span class="linenos">10</span>
<span class="linenos">11</span><span class="c1"># remove multiple fields with a list of indices</span>
<span class="linenos">12</span><span class="n">layer</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span><span class="o">.</span><span class="n">deleteAttributes</span><span class="p">(</span><span class="n">ind_list</span><span class="p">)</span>
</pre></div>
</div>
<p>After adding or removing fields in the data provider the layer’s fields need
to be updated because the changes are not automatically propagated.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">layer</span><span class="o">.</span><span class="n">updateFields</span><span class="p">()</span>
</pre></div>
</div>
<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p><strong>Directly save changes using</strong> <code class="docutils literal notranslate"><span class="pre">with</span></code> <strong>based command</strong></p>
<p>Using <code class="docutils literal notranslate"><span class="pre">with</span> <span class="pre">edit(layer):</span></code> the changes will be committed automatically
calling <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.commitChanges" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">commitChanges()</span></code></a> at the end. If any exception occurs, it will
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.rollBack" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">rollBack()</span></code></a> all the changes. See <a class="reference internal" href="#editing-buffer"><span class="std std-ref">Modifying Vector Layers with an Editing Buffer</span></a>.</p>
</div>
</section>
</section>
<section id="using-spatial-index">
<span id="index-4"></span><h2><a class="toc-backref" href="#id13" role="doc-backlink"><span class="section-number">6.5. </span>Using Spatial Index</a><a class="headerlink" href="#using-spatial-index" title="Link to this heading"></a></h2>
<p>Spatial indexes can dramatically improve the performance of your code if you
need to do frequent queries to a vector layer. Imagine, for instance, that you
are writing an interpolation algorithm, and that for a given location you need
to know the 10 closest points from a points layer, in order to use those point
for calculating the interpolated value. Without a spatial index, the only way
for QGIS to find those 10 points is to compute the distance from each and every
point to the specified location and then compare those distances. This can be a
very time consuming task, especially if it needs to be repeated for several
locations. If a spatial index exists for the layer, the operation is much more
effective.</p>
<p>Think of a layer without a spatial index as a telephone book in which telephone
numbers are not ordered or indexed. The only way to find the telephone number
of a given person is to read from the beginning until you find it.</p>
<p>Spatial indexes are not created by default for a QGIS vector layer, but you can
create them easily. This is what you have to do:</p>
<ul>
<li><p>create spatial index using the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSpatialIndex.html#qgis.core.QgsSpatialIndex" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSpatialIndex</span></code></a>
class:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">index</span> <span class="o">=</span> <span class="n">QgsSpatialIndex</span><span class="p">()</span>
</pre></div>
</div>
</li>
<li><p>add features to index — index takes <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeature.html#qgis.core.QgsFeature" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFeature</span></code></a> object and adds it
to the internal data structure. You can create the object manually or use
one from a previous call to the provider’s
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorDataProvider.html#qgis.core.QgsVectorDataProvider.getFeatures" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">getFeatures()</span></code></a> method.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">index</span><span class="o">.</span><span class="n">addFeature</span><span class="p">(</span><span class="n">feat</span><span class="p">)</span>
</pre></div>
</div>
</li>
<li><p>alternatively, you can load all features of a layer at once using bulk loading</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">index</span> <span class="o">=</span> <span class="n">QgsSpatialIndex</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">getFeatures</span><span class="p">())</span>
</pre></div>
</div>
</li>
<li><p>once spatial index is filled with some values, you can do some queries</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="c1"># returns array of feature IDs of five nearest features</span>
<span class="linenos">2</span><span class="n">nearest</span> <span class="o">=</span> <span class="n">index</span><span class="o">.</span><span class="n">nearestNeighbor</span><span class="p">(</span><span class="n">QgsPointXY</span><span class="p">(</span><span class="mf">25.4</span><span class="p">,</span> <span class="mf">12.7</span><span class="p">),</span> <span class="mi">5</span><span class="p">)</span>
<span class="linenos">3</span>
<span class="linenos">4</span><span class="c1"># returns array of IDs of features which intersect the rectangle</span>
<span class="linenos">5</span><span class="n">intersect</span> <span class="o">=</span> <span class="n">index</span><span class="o">.</span><span class="n">intersects</span><span class="p">(</span><span class="n">QgsRectangle</span><span class="p">(</span><span class="mf">22.5</span><span class="p">,</span> <span class="mf">15.3</span><span class="p">,</span> <span class="mf">23.1</span><span class="p">,</span> <span class="mf">17.2</span><span class="p">))</span>
</pre></div>
</div>
</li>
</ul>
<p>You can also use the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSpatialIndexKDBush.html#qgis.core.QgsSpatialIndexKDBush" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSpatialIndexKDBush</span></code></a>
spatial index. This index is similar to the <em>standard</em> <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSpatialIndex.html#qgis.core.QgsSpatialIndex" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSpatialIndex</span></code></a>
but:</p>
<ul class="simple">
<li><p>supports <strong>only</strong> single point features</p></li>
<li><p>is <strong>static</strong> (no additional features can be added to the index after the
construction)</p></li>
<li><p>is <strong>much faster!</strong></p></li>
<li><p>allows direct retrieval of the original feature’s points, without requiring
additional feature requests</p></li>
<li><p>supports true <em>distance based</em> searches, i.e. return all points within a
radius from a search point</p></li>
</ul>
</section>
<section id="the-qgsvectorlayerutils-class">
<span id="index-5"></span><h2><a class="toc-backref" href="#id14" role="doc-backlink"><span class="section-number">6.6. </span>The QgsVectorLayerUtils class</a><a class="headerlink" href="#the-qgsvectorlayerutils-class" title="Link to this heading"></a></h2>
<p>The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayerUtils.html#qgis.core.QgsVectorLayerUtils" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayerUtils</span></code></a> class contains
some very useful methods that you can use with vector layers.</p>
<p>For example the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayerUtils.html#qgis.core.QgsVectorLayerUtils.createFeature" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createFeature()</span></code></a>
method prepares a <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeature.html#qgis.core.QgsFeature" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFeature</span></code></a> to be added to
a vector layer keeping all the eventual constraints and default values of each
field:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">vlayer</span> <span class="o">=</span> <span class="n">QgsVectorLayer</span><span class="p">(</span><span class="s2">&quot;testdata/airports.shp&quot;</span><span class="p">,</span> <span class="s2">&quot;airports&quot;</span><span class="p">,</span> <span class="s2">&quot;ogr&quot;</span><span class="p">)</span>
<span class="n">feat</span> <span class="o">=</span> <span class="n">QgsVectorLayerUtils</span><span class="o">.</span><span class="n">createFeature</span><span class="p">(</span><span class="n">vlayer</span><span class="p">)</span>
</pre></div>
</div>
<p>The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayerUtils.html#qgis.core.QgsVectorLayerUtils.getValues" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">getValues()</span></code></a> method allows
you to quickly get the values of a field or expression:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="n">vlayer</span> <span class="o">=</span> <span class="n">QgsVectorLayer</span><span class="p">(</span><span class="s2">&quot;testdata/airports.shp&quot;</span><span class="p">,</span> <span class="s2">&quot;airports&quot;</span><span class="p">,</span> <span class="s2">&quot;ogr&quot;</span><span class="p">)</span>
<span class="linenos">2</span><span class="c1"># select only the first feature to make the output shorter</span>
<span class="linenos">3</span><span class="n">vlayer</span><span class="o">.</span><span class="n">selectByIds</span><span class="p">([</span><span class="mi">1</span><span class="p">])</span>
<span class="linenos">4</span><span class="n">val</span> <span class="o">=</span> <span class="n">QgsVectorLayerUtils</span><span class="o">.</span><span class="n">getValues</span><span class="p">(</span><span class="n">vlayer</span><span class="p">,</span> <span class="s2">&quot;NAME&quot;</span><span class="p">,</span> <span class="n">selectedOnly</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="linenos">5</span><span class="nb">print</span><span class="p">(</span><span class="n">val</span><span class="p">)</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>([&#39;AMBLER&#39;], True)
</pre></div>
</div>
</section>
<section id="creating-vector-layers">
<span id="index-6"></span><h2><a class="toc-backref" href="#id15" role="doc-backlink"><span class="section-number">6.7. </span>Creating Vector Layers</a><a class="headerlink" href="#creating-vector-layers" title="Link to this heading"></a></h2>
<p>There are several ways to generate a vector layer dataset:</p>
<ul class="simple">
<li><p>the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorFileWriter.html#qgis.core.QgsVectorFileWriter" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorFileWriter</span></code></a> class:
A convenient class for writing vector files to disk, using either a static
call to <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorFileWriter.html#qgis.core.QgsVectorFileWriter.writeAsVectorFormatV3" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">writeAsVectorFormatV3()</span></code></a> which saves the whole
vector layer or creating an instance of the class and issue calls to
inherited <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureSink.html#qgis.core.QgsFeatureSink.addFeature" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">addFeature()</span></code></a>. This class
supports all the vector formats that GDAL supports (GeoPackage, Shapefile,
GeoJSON, KML and others).</p></li>
<li><p>the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a> class: instantiates
a data provider that interprets the supplied path (url) of the data source
to connect to and access the data. It can be used to create temporary,
memory-based layers (<code class="docutils literal notranslate"><span class="pre">memory</span></code>) and connect to GDAL vector datasets (<code class="docutils literal notranslate"><span class="pre">ogr</span></code>),
databases (<code class="docutils literal notranslate"><span class="pre">postgres</span></code>, <code class="docutils literal notranslate"><span class="pre">spatialite</span></code>, <code class="docutils literal notranslate"><span class="pre">mysql</span></code>, <code class="docutils literal notranslate"><span class="pre">mssql</span></code>) and
more (<code class="docutils literal notranslate"><span class="pre">wfs</span></code>, <code class="docutils literal notranslate"><span class="pre">gpx</span></code>, <code class="docutils literal notranslate"><span class="pre">delimitedtext</span></code>…).</p></li>
</ul>
<section id="from-an-instance-of-qgsvectorfilewriter">
<h3><a class="toc-backref" href="#id16" role="doc-backlink"><span class="section-number">6.7.1. </span>From an instance of <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorFileWriter.html#qgis.core.QgsVectorFileWriter" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorFileWriter</span></code></a></a><a class="headerlink" href="#from-an-instance-of-qgsvectorfilewriter" title="Link to this heading"></a></h3>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># SaveVectorOptions contains many settings for the writer process</span>
<span class="linenos"> 2</span><span class="n">save_options</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">SaveVectorOptions</span><span class="p">()</span>
<span class="linenos"> 3</span><span class="n">transform_context</span> <span class="o">=</span> <span class="n">QgsProject</span><span class="o">.</span><span class="n">instance</span><span class="p">()</span><span class="o">.</span><span class="n">transformContext</span><span class="p">()</span>
<span class="linenos"> 4</span><span class="c1"># Write to a GeoPackage (default)</span>
<span class="linenos"> 5</span><span class="n">error</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">writeAsVectorFormatV3</span><span class="p">(</span><span class="n">layer</span><span class="p">,</span>
<span class="linenos"> 6</span>                                                  <span class="s2">&quot;testdata/my_new_file.gpkg&quot;</span><span class="p">,</span>
<span class="linenos"> 7</span>                                                  <span class="n">transform_context</span><span class="p">,</span>
<span class="linenos"> 8</span>                                                  <span class="n">save_options</span><span class="p">)</span>
<span class="linenos"> 9</span><span class="k">if</span> <span class="n">error</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">NoError</span><span class="p">:</span>
<span class="linenos">10</span>    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;success!&quot;</span><span class="p">)</span>
<span class="linenos">11</span><span class="k">else</span><span class="p">:</span>
<span class="linenos">12</span>  <span class="nb">print</span><span class="p">(</span><span class="n">error</span><span class="p">)</span>
</pre></div>
</div>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># Write to an ESRI Shapefile format dataset using UTF-8 text encoding</span>
<span class="linenos"> 2</span><span class="n">save_options</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">SaveVectorOptions</span><span class="p">()</span>
<span class="linenos"> 3</span><span class="n">save_options</span><span class="o">.</span><span class="n">driverName</span> <span class="o">=</span> <span class="s2">&quot;ESRI Shapefile&quot;</span>
<span class="linenos"> 4</span><span class="n">save_options</span><span class="o">.</span><span class="n">fileEncoding</span> <span class="o">=</span> <span class="s2">&quot;UTF-8&quot;</span>
<span class="linenos"> 5</span><span class="n">transform_context</span> <span class="o">=</span> <span class="n">QgsProject</span><span class="o">.</span><span class="n">instance</span><span class="p">()</span><span class="o">.</span><span class="n">transformContext</span><span class="p">()</span>
<span class="linenos"> 6</span><span class="n">error</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">writeAsVectorFormatV3</span><span class="p">(</span><span class="n">layer</span><span class="p">,</span>
<span class="linenos"> 7</span>                                                  <span class="s2">&quot;testdata/my_new_shapefile&quot;</span><span class="p">,</span>
<span class="linenos"> 8</span>                                                  <span class="n">transform_context</span><span class="p">,</span>
<span class="linenos"> 9</span>                                                  <span class="n">save_options</span><span class="p">)</span>
<span class="linenos">10</span><span class="k">if</span> <span class="n">error</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">NoError</span><span class="p">:</span>
<span class="linenos">11</span>    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;success again!&quot;</span><span class="p">)</span>
<span class="linenos">12</span><span class="k">else</span><span class="p">:</span>
<span class="linenos">13</span>  <span class="nb">print</span><span class="p">(</span><span class="n">error</span><span class="p">)</span>
</pre></div>
</div>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># Write to an ESRI GDB file</span>
<span class="linenos"> 2</span><span class="n">save_options</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">SaveVectorOptions</span><span class="p">()</span>
<span class="linenos"> 3</span><span class="n">save_options</span><span class="o">.</span><span class="n">driverName</span> <span class="o">=</span> <span class="s2">&quot;FileGDB&quot;</span>
<span class="linenos"> 4</span><span class="c1"># if no geometry</span>
<span class="linenos"> 5</span><span class="n">save_options</span><span class="o">.</span><span class="n">overrideGeometryType</span> <span class="o">=</span> <span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">Unknown</span>
<span class="linenos"> 6</span><span class="n">save_options</span><span class="o">.</span><span class="n">actionOnExistingFile</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">CreateOrOverwriteLayer</span>
<span class="linenos"> 7</span><span class="n">save_options</span><span class="o">.</span><span class="n">layerName</span> <span class="o">=</span> <span class="s1">&#39;my_new_layer_name&#39;</span>
<span class="linenos"> 8</span><span class="n">transform_context</span> <span class="o">=</span> <span class="n">QgsProject</span><span class="o">.</span><span class="n">instance</span><span class="p">()</span><span class="o">.</span><span class="n">transformContext</span><span class="p">()</span>
<span class="linenos"> 9</span><span class="n">gdb_path</span> <span class="o">=</span> <span class="s2">&quot;testdata/my_example.gdb&quot;</span>
<span class="linenos">10</span><span class="n">error</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">writeAsVectorFormatV3</span><span class="p">(</span><span class="n">layer</span><span class="p">,</span>
<span class="linenos">11</span>                                                <span class="n">gdb_path</span><span class="p">,</span>
<span class="linenos">12</span>                                                <span class="n">transform_context</span><span class="p">,</span>
<span class="linenos">13</span>                                                <span class="n">save_options</span><span class="p">)</span>
<span class="linenos">14</span><span class="k">if</span> <span class="n">error</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">NoError</span><span class="p">:</span>
<span class="linenos">15</span>  <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;success!&quot;</span><span class="p">)</span>
<span class="linenos">16</span><span class="k">else</span><span class="p">:</span>
<span class="linenos">17</span>  <span class="nb">print</span><span class="p">(</span><span class="n">error</span><span class="p">)</span>
</pre></div>
</div>
<p>You can also convert fields to make them compatible with different formats by
using the  <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorFileWriter.html#qgis.core.QgsVectorFileWriter.FieldValueConverter" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">FieldValueConverter</span></code></a>.
For example, to convert array variable types (e.g. in Postgres) to a text type,
you can do the following:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="n">LIST_FIELD_NAME</span> <span class="o">=</span> <span class="s1">&#39;xxxx&#39;</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="k">class</span> <span class="nc">ESRIValueConverter</span><span class="p">(</span><span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">FieldValueConverter</span><span class="p">):</span>
<span class="linenos"> 4</span>
<span class="linenos"> 5</span>  <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">layer</span><span class="p">,</span> <span class="n">list_field</span><span class="p">):</span>
<span class="linenos"> 6</span>    <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">FieldValueConverter</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
<span class="linenos"> 7</span>    <span class="bp">self</span><span class="o">.</span><span class="n">layer</span> <span class="o">=</span> <span class="n">layer</span>
<span class="linenos"> 8</span>    <span class="bp">self</span><span class="o">.</span><span class="n">list_field_idx</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">layer</span><span class="o">.</span><span class="n">fields</span><span class="p">()</span><span class="o">.</span><span class="n">indexFromName</span><span class="p">(</span><span class="n">list_field</span><span class="p">)</span>
<span class="linenos"> 9</span>
<span class="linenos">10</span>  <span class="k">def</span> <span class="nf">convert</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fieldIdxInLayer</span><span class="p">,</span> <span class="n">value</span><span class="p">):</span>
<span class="linenos">11</span>    <span class="k">if</span> <span class="n">fieldIdxInLayer</span> <span class="o">==</span> <span class="bp">self</span><span class="o">.</span><span class="n">list_field_idx</span><span class="p">:</span>
<span class="linenos">12</span>      <span class="k">return</span> <span class="n">QgsListFieldFormatter</span><span class="p">()</span><span class="o">.</span><span class="n">representValue</span><span class="p">(</span><span class="n">layer</span><span class="o">=</span><span class="n">vlayer</span><span class="p">,</span>
<span class="linenos">13</span>                                                    <span class="n">fieldIndex</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">list_field_idx</span><span class="p">,</span>
<span class="linenos">14</span>                                                    <span class="n">config</span><span class="o">=</span><span class="p">{},</span>
<span class="linenos">15</span>                                                    <span class="n">cache</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span>
<span class="linenos">16</span>                                                    <span class="n">value</span><span class="o">=</span><span class="n">value</span><span class="p">)</span>
<span class="linenos">17</span>    <span class="k">else</span><span class="p">:</span>
<span class="linenos">18</span>      <span class="k">return</span> <span class="n">value</span>
<span class="linenos">19</span>
<span class="linenos">20</span>  <span class="k">def</span> <span class="nf">fieldDefinition</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">field</span><span class="p">):</span>
<span class="linenos">21</span>    <span class="n">idx</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">layer</span><span class="o">.</span><span class="n">fields</span><span class="p">()</span><span class="o">.</span><span class="n">indexFromName</span><span class="p">(</span><span class="n">field</span><span class="o">.</span><span class="n">name</span><span class="p">())</span>
<span class="linenos">22</span>    <span class="k">if</span> <span class="n">idx</span> <span class="o">==</span> <span class="bp">self</span><span class="o">.</span><span class="n">list_field_idx</span><span class="p">:</span>
<span class="linenos">23</span>      <span class="k">return</span> <span class="n">QgsField</span><span class="p">(</span><span class="n">LIST_FIELD_NAME</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">String</span><span class="p">)</span>
<span class="linenos">24</span>    <span class="k">else</span><span class="p">:</span>
<span class="linenos">25</span>      <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">layer</span><span class="o">.</span><span class="n">fields</span><span class="p">()[</span><span class="n">idx</span><span class="p">]</span>
<span class="linenos">26</span>
<span class="linenos">27</span><span class="n">converter</span> <span class="o">=</span> <span class="n">ESRIValueConverter</span><span class="p">(</span><span class="n">vlayer</span><span class="p">,</span> <span class="n">LIST_FIELD_NAME</span><span class="p">)</span>
<span class="linenos">28</span><span class="n">opts</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">SaveVectorOptions</span><span class="p">()</span>
<span class="linenos">29</span><span class="n">opts</span><span class="o">.</span><span class="n">fieldValueConverter</span> <span class="o">=</span> <span class="n">converter</span>
</pre></div>
</div>
<p>A destination CRS may also be specified — if a valid instance of
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsCoordinateReferenceSystem.html#qgis.core.QgsCoordinateReferenceSystem" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsCoordinateReferenceSystem</span></code></a>
is passed as the fourth parameter, the layer is transformed to that CRS.</p>
<p>For valid driver names please call the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorFileWriter.html#qgis.core.QgsVectorFileWriter.supportedFiltersAndFormats" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">supportedFiltersAndFormats()</span></code></a> method
or consult the <a class="reference external" href="https://gdal.org/en/latest/drivers/vector/index.html">supported formats by OGR</a> — you
should pass the value in the “Code” column as the driver name.</p>
<p>Optionally you can set whether to export only selected features, pass further
driver-specific options for creation or tell the writer not to create attributes…
There are a number of other (optional) parameters; see the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorFileWriter.html#qgis.core.QgsVectorFileWriter" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorFileWriter</span></code></a> documentation for details.</p>
</section>
<section id="directly-from-features">
<h3><a class="toc-backref" href="#id17" role="doc-backlink"><span class="section-number">6.7.2. </span>Directly from features</a><a class="headerlink" href="#directly-from-features" title="Link to this heading"></a></h3>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.PyQt.QtCore</span> <span class="kn">import</span> <span class="n">QVariant</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="c1"># define fields for feature attributes. A QgsFields object is needed</span>
<span class="linenos"> 4</span><span class="n">fields</span> <span class="o">=</span> <span class="n">QgsFields</span><span class="p">()</span>
<span class="linenos"> 5</span><span class="n">fields</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;first&quot;</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">Int</span><span class="p">))</span>
<span class="linenos"> 6</span><span class="n">fields</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;second&quot;</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">String</span><span class="p">))</span>
<span class="linenos"> 7</span>
<span class="linenos"> 8</span><span class="sd">&quot;&quot;&quot; create an instance of vector file writer, which will create the vector file.</span>
<span class="linenos"> 9</span><span class="sd">Arguments:</span>
<span class="linenos">10</span><span class="sd">1. path to new file (will fail if exists already)</span>
<span class="linenos">11</span><span class="sd">2. field map</span>
<span class="linenos">12</span><span class="sd">3. geometry type - from WKBTYPE enum</span>
<span class="linenos">13</span><span class="sd">4. layer&#39;s spatial reference (instance of</span>
<span class="linenos">14</span><span class="sd">   QgsCoordinateReferenceSystem)</span>
<span class="linenos">15</span><span class="sd">5. coordinate transform context</span>
<span class="linenos">16</span><span class="sd">6. save options (driver name for the output file, encoding etc.)</span>
<span class="linenos">17</span><span class="sd">&quot;&quot;&quot;</span>
<span class="linenos">18</span>
<span class="linenos">19</span><span class="n">crs</span> <span class="o">=</span> <span class="n">QgsProject</span><span class="o">.</span><span class="n">instance</span><span class="p">()</span><span class="o">.</span><span class="n">crs</span><span class="p">()</span>
<span class="linenos">20</span><span class="n">transform_context</span> <span class="o">=</span> <span class="n">QgsProject</span><span class="o">.</span><span class="n">instance</span><span class="p">()</span><span class="o">.</span><span class="n">transformContext</span><span class="p">()</span>
<span class="linenos">21</span><span class="n">save_options</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">SaveVectorOptions</span><span class="p">()</span>
<span class="linenos">22</span><span class="n">save_options</span><span class="o">.</span><span class="n">driverName</span> <span class="o">=</span> <span class="s2">&quot;ESRI Shapefile&quot;</span>
<span class="linenos">23</span><span class="n">save_options</span><span class="o">.</span><span class="n">fileEncoding</span> <span class="o">=</span> <span class="s2">&quot;UTF-8&quot;</span>
<span class="linenos">24</span>
<span class="linenos">25</span><span class="n">writer</span> <span class="o">=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
<span class="linenos">26</span>  <span class="s2">&quot;testdata/my_new_shapefile.shp&quot;</span><span class="p">,</span>
<span class="linenos">27</span>  <span class="n">fields</span><span class="p">,</span>
<span class="linenos">28</span>  <span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">Point</span><span class="p">,</span>
<span class="linenos">29</span>  <span class="n">crs</span><span class="p">,</span>
<span class="linenos">30</span>  <span class="n">transform_context</span><span class="p">,</span>
<span class="linenos">31</span>  <span class="n">save_options</span>
<span class="linenos">32</span><span class="p">)</span>
<span class="linenos">33</span>
<span class="linenos">34</span><span class="k">if</span> <span class="n">writer</span><span class="o">.</span><span class="n">hasError</span><span class="p">()</span> <span class="o">!=</span> <span class="n">QgsVectorFileWriter</span><span class="o">.</span><span class="n">NoError</span><span class="p">:</span>
<span class="linenos">35</span>    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Error when creating shapefile: &quot;</span><span class="p">,</span>  <span class="n">writer</span><span class="o">.</span><span class="n">errorMessage</span><span class="p">())</span>
<span class="linenos">36</span>
<span class="linenos">37</span><span class="c1"># add a feature</span>
<span class="linenos">38</span><span class="n">fet</span> <span class="o">=</span> <span class="n">QgsFeature</span><span class="p">()</span>
<span class="linenos">39</span>
<span class="linenos">40</span><span class="n">fet</span><span class="o">.</span><span class="n">setGeometry</span><span class="p">(</span><span class="n">QgsGeometry</span><span class="o">.</span><span class="n">fromPointXY</span><span class="p">(</span><span class="n">QgsPointXY</span><span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">10</span><span class="p">)))</span>
<span class="linenos">41</span><span class="n">fet</span><span class="o">.</span><span class="n">setAttributes</span><span class="p">([</span><span class="mi">1</span><span class="p">,</span> <span class="s2">&quot;text&quot;</span><span class="p">])</span>
<span class="linenos">42</span><span class="n">writer</span><span class="o">.</span><span class="n">addFeature</span><span class="p">(</span><span class="n">fet</span><span class="p">)</span>
<span class="linenos">43</span>
<span class="linenos">44</span><span class="c1"># delete the writer to flush features to disk</span>
<span class="linenos">45</span><span class="k">del</span> <span class="n">writer</span>
</pre></div>
</div>
</section>
<section id="from-an-instance-of-qgsvectorlayer">
<span id="index-7"></span><h3><a class="toc-backref" href="#id18" role="doc-backlink"><span class="section-number">6.7.3. </span>From an instance of <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a></a><a class="headerlink" href="#from-an-instance-of-qgsvectorlayer" title="Link to this heading"></a></h3>
<p>Among all the data providers supported by the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a> class, let’s focus on the memory-based layers.
Memory provider is intended to be used mainly by plugin or 3rd party app
developers. It does not store data on disk, allowing developers to use it as a
fast backend for some temporary layers.</p>
<p>The provider supports string, int and double fields.</p>
<p>The memory provider also supports spatial indexing, which is enabled by calling
the provider’s <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorDataProvider.html#qgis.core.QgsVectorDataProvider.createSpatialIndex" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createSpatialIndex()</span></code></a> function. Once the spatial index is
created you will be able to iterate over features within smaller regions faster
(since it’s not necessary to traverse all the features, only those in specified
rectangle).</p>
<p>A memory provider is created by passing <code class="docutils literal notranslate"><span class="pre">&quot;memory&quot;</span></code> as the provider string to
the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a> constructor.</p>
<p>The constructor also takes a URI defining the geometry type of the layer,
one of: <code class="docutils literal notranslate"><span class="pre">&quot;Point&quot;</span></code>, <code class="docutils literal notranslate"><span class="pre">&quot;LineString&quot;</span></code>, <code class="docutils literal notranslate"><span class="pre">&quot;Polygon&quot;</span></code>, <code class="docutils literal notranslate"><span class="pre">&quot;MultiPoint&quot;</span></code>,
<code class="docutils literal notranslate"><span class="pre">&quot;MultiLineString&quot;</span></code>, <code class="docutils literal notranslate"><span class="pre">&quot;MultiPolygon&quot;</span></code> or <code class="docutils literal notranslate"><span class="pre">&quot;None&quot;</span></code>.</p>
<p>The URI can also specify the coordinate reference system, fields, and indexing
of the memory provider in the URI. The syntax is:</p>
<dl class="simple">
<dt>crs=definition</dt><dd><p>Specifies the coordinate reference system, where definition may be any
of the forms accepted by <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsCoordinateReferenceSystem.html#qgis.core.QgsCoordinateReferenceSystem.createFromString" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">QgsCoordinateReferenceSystem.createFromString()</span></code></a></p>
</dd>
<dt>index=yes</dt><dd><p>Specifies that the provider will use a spatial index</p>
</dd>
<dt>field=name:type(length,precision)</dt><dd><p>Specifies an attribute of the layer.  The attribute has a name, and
optionally a type (integer, double, or string), length, and precision.
There may be multiple field definitions.</p>
</dd>
</dl>
<p>The following example of a URI incorporates all these options</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="s2">&quot;Point?crs=epsg:4326&amp;field=id:integer&amp;field=name:string(20)&amp;index=yes&quot;</span>
</pre></div>
</div>
<p>The following example code illustrates creating and populating a memory provider</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.PyQt.QtCore</span> <span class="kn">import</span> <span class="n">QVariant</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="c1"># create layer</span>
<span class="linenos"> 4</span><span class="n">vl</span> <span class="o">=</span> <span class="n">QgsVectorLayer</span><span class="p">(</span><span class="s2">&quot;Point&quot;</span><span class="p">,</span> <span class="s2">&quot;temporary_points&quot;</span><span class="p">,</span> <span class="s2">&quot;memory&quot;</span><span class="p">)</span>
<span class="linenos"> 5</span><span class="n">pr</span> <span class="o">=</span> <span class="n">vl</span><span class="o">.</span><span class="n">dataProvider</span><span class="p">()</span>
<span class="linenos"> 6</span>
<span class="linenos"> 7</span><span class="c1"># add fields</span>
<span class="linenos"> 8</span><span class="n">pr</span><span class="o">.</span><span class="n">addAttributes</span><span class="p">([</span><span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;name&quot;</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">String</span><span class="p">),</span>
<span class="linenos"> 9</span>                    <span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;age&quot;</span><span class="p">,</span>  <span class="n">QVariant</span><span class="o">.</span><span class="n">Int</span><span class="p">),</span>
<span class="linenos">10</span>                    <span class="n">QgsField</span><span class="p">(</span><span class="s2">&quot;size&quot;</span><span class="p">,</span> <span class="n">QVariant</span><span class="o">.</span><span class="n">Double</span><span class="p">)])</span>
<span class="linenos">11</span><span class="n">vl</span><span class="o">.</span><span class="n">updateFields</span><span class="p">()</span> <span class="c1"># tell the vector layer to fetch changes from the provider</span>
<span class="linenos">12</span>
<span class="linenos">13</span><span class="c1"># add a feature</span>
<span class="linenos">14</span><span class="n">fet</span> <span class="o">=</span> <span class="n">QgsFeature</span><span class="p">()</span>
<span class="linenos">15</span><span class="n">fet</span><span class="o">.</span><span class="n">setGeometry</span><span class="p">(</span><span class="n">QgsGeometry</span><span class="o">.</span><span class="n">fromPointXY</span><span class="p">(</span><span class="n">QgsPointXY</span><span class="p">(</span><span class="mi">10</span><span class="p">,</span><span class="mi">10</span><span class="p">)))</span>
<span class="linenos">16</span><span class="n">fet</span><span class="o">.</span><span class="n">setAttributes</span><span class="p">([</span><span class="s2">&quot;Johny&quot;</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mf">0.3</span><span class="p">])</span>
<span class="linenos">17</span><span class="n">pr</span><span class="o">.</span><span class="n">addFeatures</span><span class="p">([</span><span class="n">fet</span><span class="p">])</span>
<span class="linenos">18</span>
<span class="linenos">19</span><span class="c1"># update layer&#39;s extent when new features have been added</span>
<span class="linenos">20</span><span class="c1"># because change of extent in provider is not propagated to the layer</span>
<span class="linenos">21</span><span class="n">vl</span><span class="o">.</span><span class="n">updateExtents</span><span class="p">()</span>
</pre></div>
</div>
<p>Finally, let’s check whether everything went well</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># show some stats</span>
<span class="linenos"> 2</span><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;fields:&quot;</span><span class="p">,</span> <span class="nb">len</span><span class="p">(</span><span class="n">pr</span><span class="o">.</span><span class="n">fields</span><span class="p">()))</span>
<span class="linenos"> 3</span><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;features:&quot;</span><span class="p">,</span> <span class="n">pr</span><span class="o">.</span><span class="n">featureCount</span><span class="p">())</span>
<span class="linenos"> 4</span><span class="n">e</span> <span class="o">=</span> <span class="n">vl</span><span class="o">.</span><span class="n">extent</span><span class="p">()</span>
<span class="linenos"> 5</span><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;extent:&quot;</span><span class="p">,</span> <span class="n">e</span><span class="o">.</span><span class="n">xMinimum</span><span class="p">(),</span> <span class="n">e</span><span class="o">.</span><span class="n">yMinimum</span><span class="p">(),</span> <span class="n">e</span><span class="o">.</span><span class="n">xMaximum</span><span class="p">(),</span> <span class="n">e</span><span class="o">.</span><span class="n">yMaximum</span><span class="p">())</span>
<span class="linenos"> 6</span>
<span class="linenos"> 7</span><span class="c1"># iterate over features</span>
<span class="linenos"> 8</span><span class="n">features</span> <span class="o">=</span> <span class="n">vl</span><span class="o">.</span><span class="n">getFeatures</span><span class="p">()</span>
<span class="linenos"> 9</span><span class="k">for</span> <span class="n">fet</span> <span class="ow">in</span> <span class="n">features</span><span class="p">:</span>
<span class="linenos">10</span>    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;F:&quot;</span><span class="p">,</span> <span class="n">fet</span><span class="o">.</span><span class="n">id</span><span class="p">(),</span> <span class="n">fet</span><span class="o">.</span><span class="n">attributes</span><span class="p">(),</span> <span class="n">fet</span><span class="o">.</span><span class="n">geometry</span><span class="p">()</span><span class="o">.</span><span class="n">asPoint</span><span class="p">())</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>fields: 3
features: 1
extent: 10.0 10.0 10.0 10.0
F: 1 [&#39;Johny&#39;, 2, 0.3] &lt;QgsPointXY: POINT(10 10)&gt;
</pre></div>
</div>
</section>
</section>
<section id="appearance-symbology-of-vector-layers">
<span id="index-8"></span><h2><a class="toc-backref" href="#id19" role="doc-backlink"><span class="section-number">6.8. </span>Appearance (Symbology) of Vector Layers</a><a class="headerlink" href="#appearance-symbology-of-vector-layers" title="Link to this heading"></a></h2>
<p>When a vector layer is being rendered, the appearance of the data is given by
<strong>renderer</strong> and <strong>symbols</strong> associated with the layer.  Symbols are classes
which take care of drawing of visual representation of features, while
renderers determine what symbol will be used for a particular feature.</p>
<p>The renderer for a given layer can be obtained as shown below:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">renderer</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">renderer</span><span class="p">()</span>
</pre></div>
</div>
<p>And with that reference, let us explore it a bit</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Type:&quot;</span><span class="p">,</span> <span class="n">renderer</span><span class="o">.</span><span class="n">type</span><span class="p">())</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>Type: singleSymbol
</pre></div>
</div>
<p>There are several known renderer types available in the QGIS core library:</p>
<table class="docutils align-default">
<thead>
<tr class="row-odd"><th class="head"><p>Type</p></th>
<th class="head"><p>Class</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>singleSymbol</p></td>
<td><p><a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSingleSymbolRenderer.html#qgis.core.QgsSingleSymbolRenderer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSingleSymbolRenderer</span></code></a></p></td>
<td><p>Renders all features with the same symbol</p></td>
</tr>
<tr class="row-odd"><td><p>categorizedSymbol</p></td>
<td><p><a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsCategorizedSymbolRenderer.html#qgis.core.QgsCategorizedSymbolRenderer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsCategorizedSymbolRenderer</span></code></a></p></td>
<td><p>Renders features using a different symbol for each category</p></td>
</tr>
<tr class="row-even"><td><p>graduatedSymbol</p></td>
<td><p><a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsGraduatedSymbolRenderer.html#qgis.core.QgsGraduatedSymbolRenderer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsGraduatedSymbolRenderer</span></code></a></p></td>
<td><p>Renders features using a different symbol for each range of values</p></td>
</tr>
</tbody>
</table>
<p>There might be also some custom renderer types, so never make an assumption
there are just these types. You can query the application’s <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererRegistry.html#qgis.core.QgsRendererRegistry" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsRendererRegistry</span></code></a>
to find out currently available renderers:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="n">QgsApplication</span><span class="o">.</span><span class="n">rendererRegistry</span><span class="p">()</span><span class="o">.</span><span class="n">renderersList</span><span class="p">())</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>[&#39;nullSymbol&#39;, &#39;singleSymbol&#39;, &#39;categorizedSymbol&#39;, &#39;graduatedSymbol&#39;, &#39;RuleRenderer&#39;, &#39;pointDisplacement&#39;, &#39;pointCluster&#39;, &#39;mergedFeatureRenderer&#39;, &#39;invertedPolygonRenderer&#39;, &#39;heatmapRenderer&#39;, &#39;25dRenderer&#39;, &#39;embeddedSymbol&#39;]
</pre></div>
</div>
<p>It is possible to obtain a dump of a renderer contents in text form — can be
useful for debugging</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">renderer</span><span class="o">.</span><span class="n">dump</span><span class="p">()</span>
</pre></div>
</div>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">SINGLE</span><span class="p">:</span> <span class="n">MARKER</span> <span class="n">SYMBOL</span> <span class="p">(</span><span class="mi">1</span> <span class="n">layers</span><span class="p">)</span> <span class="n">color</span> <span class="mi">190</span><span class="p">,</span><span class="mi">207</span><span class="p">,</span><span class="mi">80</span><span class="p">,</span><span class="mi">255</span>
</pre></div>
</div>
<section id="single-symbol-renderer">
<span id="index-9"></span><h3><a class="toc-backref" href="#id20" role="doc-backlink"><span class="section-number">6.8.1. </span>Single Symbol Renderer</a><a class="headerlink" href="#single-symbol-renderer" title="Link to this heading"></a></h3>
<p>You can get the symbol used for rendering by calling <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSingleSymbolRenderer.html#qgis.core.QgsSingleSymbolRenderer.symbol" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">symbol()</span></code></a> method and
change it with <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSingleSymbolRenderer.html#qgis.core.QgsSingleSymbolRenderer.setSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setSymbol()</span></code></a> method (note for C++ devs: the renderer takes
ownership of the symbol.)</p>
<p>You can change the symbol used by a particular vector layer by calling
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSingleSymbolRenderer.html#qgis.core.QgsSingleSymbolRenderer.setSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setSymbol()</span></code></a> passing an instance of the appropriate symbol instance.
Symbols for <em>point</em>, <em>line</em> and <em>polygon</em> layers can be created by calling
the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol.createSimple" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createSimple()</span></code></a> function of the corresponding classes
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsMarkerSymbol</span></code></a>, <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsLineSymbol.html#qgis.core.QgsLineSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsLineSymbol</span></code></a> and
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFillSymbol.html#qgis.core.QgsFillSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFillSymbol</span></code></a>.</p>
<p>The dictionary passed to <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol.createSimple" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createSimple()</span></code></a> sets the style properties of the
symbol.</p>
<p>For example you can replace the symbol used by a particular <strong>point</strong> layer
by calling <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSingleSymbolRenderer.html#qgis.core.QgsSingleSymbolRenderer.setSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setSymbol()</span></code></a> passing an instance of a <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsMarkerSymbol</span></code></a>,
as in the following code example:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">symbol</span> <span class="o">=</span> <span class="n">QgsMarkerSymbol</span><span class="o">.</span><span class="n">createSimple</span><span class="p">({</span><span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="s1">&#39;square&#39;</span><span class="p">,</span> <span class="s1">&#39;color&#39;</span><span class="p">:</span> <span class="s1">&#39;red&#39;</span><span class="p">})</span>
<span class="n">layer</span><span class="o">.</span><span class="n">renderer</span><span class="p">()</span><span class="o">.</span><span class="n">setSymbol</span><span class="p">(</span><span class="n">symbol</span><span class="p">)</span>
<span class="c1"># show the change</span>
<span class="n">layer</span><span class="o">.</span><span class="n">triggerRepaint</span><span class="p">()</span>
</pre></div>
</div>
<p><code class="docutils literal notranslate"><span class="pre">name</span></code> indicates the shape of the marker, and can be any of the following:</p>
<ul class="simple">
<li><p><code class="docutils literal notranslate"><span class="pre">circle</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">square</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">cross</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">rectangle</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">diamond</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">pentagon</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">triangle</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">equilateral_triangle</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">star</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">regular_star</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">arrow</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">filled_arrowhead</span></code></p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">x</span></code></p></li>
</ul>
<p>To get the full list of properties for the first symbol layer of a symbol
instance you can follow the example code:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">renderer</span><span class="p">()</span><span class="o">.</span><span class="n">symbol</span><span class="p">()</span><span class="o">.</span><span class="n">symbolLayers</span><span class="p">()[</span><span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">properties</span><span class="p">())</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>{&#39;angle&#39;: &#39;0&#39;, &#39;cap_style&#39;: &#39;square&#39;, &#39;color&#39;: &#39;255,0,0,255&#39;, &#39;horizontal_anchor_point&#39;: &#39;1&#39;, &#39;joinstyle&#39;: &#39;bevel&#39;, &#39;name&#39;: &#39;square&#39;, &#39;offset&#39;: &#39;0,0&#39;, &#39;offset_map_unit_scale&#39;: &#39;3x:0,0,0,0,0,0&#39;, &#39;offset_unit&#39;: &#39;MM&#39;, &#39;outline_color&#39;: &#39;35,35,35,255&#39;, &#39;outline_style&#39;: &#39;solid&#39;, &#39;outline_width&#39;: &#39;0&#39;, &#39;outline_width_map_unit_scale&#39;: &#39;3x:0,0,0,0,0,0&#39;, &#39;outline_width_unit&#39;: &#39;MM&#39;, &#39;scale_method&#39;: &#39;diameter&#39;, &#39;size&#39;: &#39;2&#39;, &#39;size_map_unit_scale&#39;: &#39;3x:0,0,0,0,0,0&#39;, &#39;size_unit&#39;: &#39;MM&#39;, &#39;vertical_anchor_point&#39;: &#39;1&#39;}
</pre></div>
</div>
<p>This can be useful if you want to alter some properties:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="c1"># You can alter a single property...</span>
<span class="linenos"> 2</span><span class="n">layer</span><span class="o">.</span><span class="n">renderer</span><span class="p">()</span><span class="o">.</span><span class="n">symbol</span><span class="p">()</span><span class="o">.</span><span class="n">symbolLayer</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span><span class="o">.</span><span class="n">setSize</span><span class="p">(</span><span class="mi">3</span><span class="p">)</span>
<span class="linenos"> 3</span><span class="c1"># ... but not all properties are accessible from methods,</span>
<span class="linenos"> 4</span><span class="c1"># you can also replace the symbol completely:</span>
<span class="linenos"> 5</span><span class="n">props</span> <span class="o">=</span> <span class="n">layer</span><span class="o">.</span><span class="n">renderer</span><span class="p">()</span><span class="o">.</span><span class="n">symbol</span><span class="p">()</span><span class="o">.</span><span class="n">symbolLayer</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span><span class="o">.</span><span class="n">properties</span><span class="p">()</span>
<span class="linenos"> 6</span><span class="n">props</span><span class="p">[</span><span class="s1">&#39;color&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;yellow&#39;</span>
<span class="linenos"> 7</span><span class="n">props</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;square&#39;</span>
<span class="linenos"> 8</span><span class="n">layer</span><span class="o">.</span><span class="n">renderer</span><span class="p">()</span><span class="o">.</span><span class="n">setSymbol</span><span class="p">(</span><span class="n">QgsMarkerSymbol</span><span class="o">.</span><span class="n">createSimple</span><span class="p">(</span><span class="n">props</span><span class="p">))</span>
<span class="linenos"> 9</span><span class="c1"># show the changes</span>
<span class="linenos">10</span><span class="n">layer</span><span class="o">.</span><span class="n">triggerRepaint</span><span class="p">()</span>
</pre></div>
</div>
</section>
<section id="categorized-symbol-renderer">
<span id="index-10"></span><h3><a class="toc-backref" href="#id21" role="doc-backlink"><span class="section-number">6.8.2. </span>Categorized Symbol Renderer</a><a class="headerlink" href="#categorized-symbol-renderer" title="Link to this heading"></a></h3>
<p>When using a categorized renderer, you can query and set the attribute that is used for classification: use the
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsCategorizedSymbolRenderer.html#qgis.core.QgsCategorizedSymbolRenderer.classAttribute" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">classAttribute()</span></code></a> and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsCategorizedSymbolRenderer.html#qgis.core.QgsCategorizedSymbolRenderer.setClassAttribute" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setClassAttribute()</span></code></a> methods.</p>
<p>To get a list of categories</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="n">categorized_renderer</span> <span class="o">=</span> <span class="n">QgsCategorizedSymbolRenderer</span><span class="p">()</span>
<span class="linenos">2</span><span class="c1"># Add a few categories</span>
<span class="linenos">3</span><span class="n">cat1</span> <span class="o">=</span> <span class="n">QgsRendererCategory</span><span class="p">(</span><span class="s1">&#39;1&#39;</span><span class="p">,</span> <span class="n">QgsMarkerSymbol</span><span class="p">(),</span> <span class="s1">&#39;category 1&#39;</span><span class="p">)</span>
<span class="linenos">4</span><span class="n">cat2</span> <span class="o">=</span> <span class="n">QgsRendererCategory</span><span class="p">(</span><span class="s1">&#39;2&#39;</span><span class="p">,</span> <span class="n">QgsMarkerSymbol</span><span class="p">(),</span> <span class="s1">&#39;category 2&#39;</span><span class="p">)</span>
<span class="linenos">5</span><span class="n">categorized_renderer</span><span class="o">.</span><span class="n">addCategory</span><span class="p">(</span><span class="n">cat1</span><span class="p">)</span>
<span class="linenos">6</span><span class="n">categorized_renderer</span><span class="o">.</span><span class="n">addCategory</span><span class="p">(</span><span class="n">cat2</span><span class="p">)</span>
<span class="linenos">7</span>
<span class="linenos">8</span><span class="k">for</span> <span class="n">cat</span> <span class="ow">in</span> <span class="n">categorized_renderer</span><span class="o">.</span><span class="n">categories</span><span class="p">():</span>
<span class="linenos">9</span>    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;</span><span class="si">{}</span><span class="s2">: </span><span class="si">{}</span><span class="s2"> :: </span><span class="si">{}</span><span class="s2">&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">cat</span><span class="o">.</span><span class="n">value</span><span class="p">(),</span> <span class="n">cat</span><span class="o">.</span><span class="n">label</span><span class="p">(),</span> <span class="n">cat</span><span class="o">.</span><span class="n">symbol</span><span class="p">()))</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>1: category 1 :: &lt;qgis._core.QgsMarkerSymbol object at 0x7f378ffcd9d8&gt;
2: category 2 :: &lt;qgis._core.QgsMarkerSymbol object at 0x7f378ffcd9d8&gt;
</pre></div>
</div>
<p>Where <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererCategory.html#qgis.core.QgsRendererCategory.value" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">value()</span></code></a> is the value used for discrimination between categories,
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererCategory.html#qgis.core.QgsRendererCategory.label" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">label()</span></code></a> is a text used for category description and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererCategory.html#qgis.core.QgsRendererCategory.symbol" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">symbol()</span></code></a> method
returns the assigned symbol.</p>
<p>The renderer usually stores also original symbol and color ramp which were used
for the classification: <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsCategorizedSymbolRenderer.html#qgis.core.QgsCategorizedSymbolRenderer.sourceColorRamp" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">sourceColorRamp()</span></code></a> and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsCategorizedSymbolRenderer.html#qgis.core.QgsCategorizedSymbolRenderer.sourceSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">sourceSymbol()</span></code></a> methods.</p>
</section>
<section id="graduated-symbol-renderer">
<span id="index-11"></span><h3><a class="toc-backref" href="#id22" role="doc-backlink"><span class="section-number">6.8.3. </span>Graduated Symbol Renderer</a><a class="headerlink" href="#graduated-symbol-renderer" title="Link to this heading"></a></h3>
<p>This renderer is very similar to the categorized symbol renderer described
above, but instead of one attribute value per class it works with ranges of
values and thus can be used only with numerical attributes.</p>
<p>To find out more about ranges used in the renderer</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="n">graduated_renderer</span> <span class="o">=</span> <span class="n">QgsGraduatedSymbolRenderer</span><span class="p">()</span>
<span class="linenos"> 2</span><span class="c1"># Add a few categories</span>
<span class="linenos"> 3</span><span class="n">graduated_renderer</span><span class="o">.</span><span class="n">addClassRange</span><span class="p">(</span><span class="n">QgsRendererRange</span><span class="p">(</span><span class="n">QgsClassificationRange</span><span class="p">(</span><span class="s1">&#39;class 0-100&#39;</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">100</span><span class="p">),</span> <span class="n">QgsMarkerSymbol</span><span class="p">()))</span>
<span class="linenos"> 4</span><span class="n">graduated_renderer</span><span class="o">.</span><span class="n">addClassRange</span><span class="p">(</span><span class="n">QgsRendererRange</span><span class="p">(</span><span class="n">QgsClassificationRange</span><span class="p">(</span><span class="s1">&#39;class 101-200&#39;</span><span class="p">,</span> <span class="mi">101</span><span class="p">,</span> <span class="mi">200</span><span class="p">),</span> <span class="n">QgsMarkerSymbol</span><span class="p">()))</span>
<span class="linenos"> 5</span>
<span class="linenos"> 6</span><span class="k">for</span> <span class="n">ran</span> <span class="ow">in</span> <span class="n">graduated_renderer</span><span class="o">.</span><span class="n">ranges</span><span class="p">():</span>
<span class="linenos"> 7</span>    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;</span><span class="si">{}</span><span class="s2"> - </span><span class="si">{}</span><span class="s2">: </span><span class="si">{}</span><span class="s2"> </span><span class="si">{}</span><span class="s2">&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
<span class="linenos"> 8</span>        <span class="n">ran</span><span class="o">.</span><span class="n">lowerValue</span><span class="p">(),</span>
<span class="linenos"> 9</span>        <span class="n">ran</span><span class="o">.</span><span class="n">upperValue</span><span class="p">(),</span>
<span class="linenos">10</span>        <span class="n">ran</span><span class="o">.</span><span class="n">label</span><span class="p">(),</span>
<span class="linenos">11</span>        <span class="n">ran</span><span class="o">.</span><span class="n">symbol</span><span class="p">()</span>
<span class="linenos">12</span>      <span class="p">))</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>0.0 - 100.0: class 0-100 &lt;qgis._core.QgsMarkerSymbol object at 0x7f8bad281b88&gt;
101.0 - 200.0: class 101-200 &lt;qgis._core.QgsMarkerSymbol object at 0x7f8bad281b88&gt;
</pre></div>
</div>
<p>you can again use the
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsGraduatedSymbolRenderer.html#qgis.core.QgsGraduatedSymbolRenderer.classAttribute" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">classAttribute()</span></code></a>
(to find the classification attribute name),
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsGraduatedSymbolRenderer.html#qgis.core.QgsGraduatedSymbolRenderer.sourceSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">sourceSymbol()</span></code></a>
and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsGraduatedSymbolRenderer.html#qgis.core.QgsGraduatedSymbolRenderer.sourceColorRamp" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">sourceColorRamp()</span></code></a> methods.
Additionally there is the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsGraduatedSymbolRenderer.html#qgis.core.QgsGraduatedSymbolRenderer.mode" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">mode()</span></code></a>
method which determines how the ranges were created:
using equal intervals, quantiles or some other method.</p>
<p>If you wish to create your own graduated symbol renderer you can do so as
illustrated in the example snippet below (which creates a simple two class
arrangement)</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.PyQt</span> <span class="kn">import</span> <span class="n">QtGui</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="n">myVectorLayer</span> <span class="o">=</span> <span class="n">QgsVectorLayer</span><span class="p">(</span><span class="s2">&quot;testdata/airports.shp&quot;</span><span class="p">,</span> <span class="s2">&quot;airports&quot;</span><span class="p">,</span> <span class="s2">&quot;ogr&quot;</span><span class="p">)</span>
<span class="linenos"> 4</span><span class="n">myTargetField</span> <span class="o">=</span> <span class="s1">&#39;ELEV&#39;</span>
<span class="linenos"> 5</span><span class="n">myRangeList</span> <span class="o">=</span> <span class="p">[]</span>
<span class="linenos"> 6</span><span class="n">myOpacity</span> <span class="o">=</span> <span class="mi">1</span>
<span class="linenos"> 7</span><span class="c1"># Make our first symbol and range...</span>
<span class="linenos"> 8</span><span class="n">myMin</span> <span class="o">=</span> <span class="mf">0.0</span>
<span class="linenos"> 9</span><span class="n">myMax</span> <span class="o">=</span> <span class="mf">50.0</span>
<span class="linenos">10</span><span class="n">myLabel</span> <span class="o">=</span> <span class="s1">&#39;Group 1&#39;</span>
<span class="linenos">11</span><span class="n">myColour</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QColor</span><span class="p">(</span><span class="s1">&#39;#ffee00&#39;</span><span class="p">)</span>
<span class="linenos">12</span><span class="n">mySymbol1</span> <span class="o">=</span> <span class="n">QgsSymbol</span><span class="o">.</span><span class="n">defaultSymbol</span><span class="p">(</span><span class="n">myVectorLayer</span><span class="o">.</span><span class="n">geometryType</span><span class="p">())</span>
<span class="linenos">13</span><span class="n">mySymbol1</span><span class="o">.</span><span class="n">setColor</span><span class="p">(</span><span class="n">myColour</span><span class="p">)</span>
<span class="linenos">14</span><span class="n">mySymbol1</span><span class="o">.</span><span class="n">setOpacity</span><span class="p">(</span><span class="n">myOpacity</span><span class="p">)</span>
<span class="linenos">15</span><span class="n">myRange1</span> <span class="o">=</span> <span class="n">QgsRendererRange</span><span class="p">(</span><span class="n">myMin</span><span class="p">,</span> <span class="n">myMax</span><span class="p">,</span> <span class="n">mySymbol1</span><span class="p">,</span> <span class="n">myLabel</span><span class="p">)</span>
<span class="linenos">16</span><span class="n">myRangeList</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">myRange1</span><span class="p">)</span>
<span class="linenos">17</span><span class="c1">#now make another symbol and range...</span>
<span class="linenos">18</span><span class="n">myMin</span> <span class="o">=</span> <span class="mf">50.1</span>
<span class="linenos">19</span><span class="n">myMax</span> <span class="o">=</span> <span class="mi">100</span>
<span class="linenos">20</span><span class="n">myLabel</span> <span class="o">=</span> <span class="s1">&#39;Group 2&#39;</span>
<span class="linenos">21</span><span class="n">myColour</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QColor</span><span class="p">(</span><span class="s1">&#39;#00eeff&#39;</span><span class="p">)</span>
<span class="linenos">22</span><span class="n">mySymbol2</span> <span class="o">=</span> <span class="n">QgsSymbol</span><span class="o">.</span><span class="n">defaultSymbol</span><span class="p">(</span>
<span class="linenos">23</span>     <span class="n">myVectorLayer</span><span class="o">.</span><span class="n">geometryType</span><span class="p">())</span>
<span class="linenos">24</span><span class="n">mySymbol2</span><span class="o">.</span><span class="n">setColor</span><span class="p">(</span><span class="n">myColour</span><span class="p">)</span>
<span class="linenos">25</span><span class="n">mySymbol2</span><span class="o">.</span><span class="n">setOpacity</span><span class="p">(</span><span class="n">myOpacity</span><span class="p">)</span>
<span class="linenos">26</span><span class="n">myRange2</span> <span class="o">=</span> <span class="n">QgsRendererRange</span><span class="p">(</span><span class="n">myMin</span><span class="p">,</span> <span class="n">myMax</span><span class="p">,</span> <span class="n">mySymbol2</span><span class="p">,</span> <span class="n">myLabel</span><span class="p">)</span>
<span class="linenos">27</span><span class="n">myRangeList</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">myRange2</span><span class="p">)</span>
<span class="linenos">28</span><span class="n">myRenderer</span> <span class="o">=</span> <span class="n">QgsGraduatedSymbolRenderer</span><span class="p">(</span><span class="s1">&#39;&#39;</span><span class="p">,</span> <span class="n">myRangeList</span><span class="p">)</span>
<span class="linenos">29</span><span class="n">myClassificationMethod</span> <span class="o">=</span> <span class="n">QgsApplication</span><span class="o">.</span><span class="n">classificationMethodRegistry</span><span class="p">()</span><span class="o">.</span><span class="n">method</span><span class="p">(</span><span class="s2">&quot;EqualInterval&quot;</span><span class="p">)</span>
<span class="linenos">30</span><span class="n">myRenderer</span><span class="o">.</span><span class="n">setClassificationMethod</span><span class="p">(</span><span class="n">myClassificationMethod</span><span class="p">)</span>
<span class="linenos">31</span><span class="n">myRenderer</span><span class="o">.</span><span class="n">setClassAttribute</span><span class="p">(</span><span class="n">myTargetField</span><span class="p">)</span>
<span class="linenos">32</span>
<span class="linenos">33</span><span class="n">myVectorLayer</span><span class="o">.</span><span class="n">setRenderer</span><span class="p">(</span><span class="n">myRenderer</span><span class="p">)</span>
</pre></div>
</div>
</section>
<section id="working-with-symbols">
<span id="index-12"></span><h3><a class="toc-backref" href="#id23" role="doc-backlink"><span class="section-number">6.8.4. </span>Working with Symbols</a><a class="headerlink" href="#working-with-symbols" title="Link to this heading"></a></h3>
<p>For representation of symbols, there is <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbol.html#qgis.core.QgsSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSymbol</span></code></a> base class with
three derived classes:</p>
<ul class="simple">
<li><p><a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsMarkerSymbol</span></code></a> — for point features</p></li>
<li><p><a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsLineSymbol.html#qgis.core.QgsLineSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsLineSymbol</span></code></a> — for line features</p></li>
<li><p><a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFillSymbol.html#qgis.core.QgsFillSymbol" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFillSymbol</span></code></a> — for polygon features</p></li>
</ul>
<p><strong>Every symbol consists of one or more symbol layers</strong> (classes derived from
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSymbolLayer</span></code></a>). The symbol layers do the actual rendering, the
symbol class itself serves only as a container for the symbol layers.</p>
<p>Having an instance of a symbol (e.g. from a renderer), it is possible to
explore it: the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbol.html#qgis.core.QgsSymbol.type" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">type()</span></code></a> method says whether it is a
marker, line or fill symbol. There is a <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbol.html#qgis.core.QgsSymbol.dump" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">dump()</span></code></a>
method which returns a brief description of the symbol. To get a list of symbol
layers:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">marker_symbol</span> <span class="o">=</span> <span class="n">QgsMarkerSymbol</span><span class="p">()</span>
<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">marker_symbol</span><span class="o">.</span><span class="n">symbolLayerCount</span><span class="p">()):</span>
    <span class="n">lyr</span> <span class="o">=</span> <span class="n">marker_symbol</span><span class="o">.</span><span class="n">symbolLayer</span><span class="p">(</span><span class="n">i</span><span class="p">)</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;</span><span class="si">{}</span><span class="s2">: </span><span class="si">{}</span><span class="s2">&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">lyr</span><span class="o">.</span><span class="n">layerType</span><span class="p">()))</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span>0: SimpleMarker
</pre></div>
</div>
<p>To find out symbol’s color use <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbol.html#qgis.core.QgsSymbol.color" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">color()</span></code></a> method
and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbol.html#qgis.core.QgsSymbol.setColor" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setColor()</span></code></a> to
change its color. With marker symbols additionally you can query for the symbol
size and rotation with the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol.size" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">size()</span></code></a>
and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol.angle" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">angle()</span></code></a> methods. For line symbols
the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsLineSymbol.html#qgis.core.QgsLineSymbol.width" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">width()</span></code></a> method returns the line width.</p>
<p>Size and width are in millimeters by default, angles are in degrees.</p>
<section id="working-with-symbol-layers">
<span id="index-13"></span><h4><a class="toc-backref" href="#id24" role="doc-backlink"><span class="section-number">6.8.4.1. </span>Working with Symbol Layers</a><a class="headerlink" href="#working-with-symbol-layers" title="Link to this heading"></a></h4>
<p>As said before, symbol layers (subclasses of <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSymbolLayer</span></code></a>)
determine the appearance of the features.  There are several basic symbol layer
classes for general use. It is possible to implement new symbol layer types and
thus arbitrarily customize how features will be rendered. The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.layerType" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">layerType()</span></code></a>
method uniquely identifies the symbol layer class — the basic and default
ones are <code class="docutils literal notranslate"><span class="pre">SimpleMarker</span></code>, <code class="docutils literal notranslate"><span class="pre">SimpleLine</span></code> and <code class="docutils literal notranslate"><span class="pre">SimpleFill</span></code> symbol layers types.</p>
<p>You can get a complete list of the types of symbol layers you can create for a
given symbol layer class with the following code:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="n">QgsSymbolLayerRegistry</span>
<span class="linenos">2</span><span class="n">myRegistry</span> <span class="o">=</span> <span class="n">QgsApplication</span><span class="o">.</span><span class="n">symbolLayerRegistry</span><span class="p">()</span>
<span class="linenos">3</span><span class="n">myMetadata</span> <span class="o">=</span> <span class="n">myRegistry</span><span class="o">.</span><span class="n">symbolLayerMetadata</span><span class="p">(</span><span class="s2">&quot;SimpleFill&quot;</span><span class="p">)</span>
<span class="linenos">4</span><span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">myRegistry</span><span class="o">.</span><span class="n">symbolLayersForType</span><span class="p">(</span><span class="n">QgsSymbol</span><span class="o">.</span><span class="n">Marker</span><span class="p">):</span>
<span class="linenos">5</span>    <span class="nb">print</span><span class="p">(</span><span class="n">item</span><span class="p">)</span>
</pre></div>
</div>
<div class="highlight-none notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span>AnimatedMarker
<span class="linenos"> 2</span>EllipseMarker
<span class="linenos"> 3</span>FilledMarker
<span class="linenos"> 4</span>FontMarker
<span class="linenos"> 5</span>GeometryGenerator
<span class="linenos"> 6</span>MaskMarker
<span class="linenos"> 7</span>RasterMarker
<span class="linenos"> 8</span>SimpleMarker
<span class="linenos"> 9</span>SvgMarker
<span class="linenos">10</span>VectorField
</pre></div>
</div>
<p>The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayerRegistry.html#qgis.core.QgsSymbolLayerRegistry" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsSymbolLayerRegistry</span></code></a> class manages
a database of all available symbol layer types.</p>
<p>To access symbol layer data, use its <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.properties" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">properties()</span></code></a> method that returns a
key-value dictionary of properties which determine the appearance. Each symbol
layer type has a specific set of properties that it uses. Additionally, there
are the generic methods <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbol.html#qgis.core.QgsSymbol.color" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">color()</span></code></a>, <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol.size" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">size()</span></code></a>, <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbol.html#qgis.core.QgsMarkerSymbol.angle" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">angle()</span></code></a> and
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsLineSymbol.html#qgis.core.QgsLineSymbol.width" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">width()</span></code></a>,
with their setter counterparts. Of course size and angle are available only for
marker symbol layers and width for line symbol layers.</p>
</section>
<section id="creating-custom-symbol-layer-types">
<span id="index-14"></span><h4><a class="toc-backref" href="#id25" role="doc-backlink"><span class="section-number">6.8.4.2. </span>Creating Custom Symbol Layer Types</a><a class="headerlink" href="#creating-custom-symbol-layer-types" title="Link to this heading"></a></h4>
<p>Imagine you would like to customize the way how the data gets rendered. You can
create your own symbol layer class that will draw the features exactly as you
wish. Here is an example of a marker that draws red circles with specified
radius</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="n">QgsMarkerSymbolLayer</span>
<span class="linenos"> 2</span><span class="kn">from</span> <span class="nn">qgis.PyQt.QtGui</span> <span class="kn">import</span> <span class="n">QColor</span>
<span class="linenos"> 3</span>
<span class="linenos"> 4</span><span class="k">class</span> <span class="nc">FooSymbolLayer</span><span class="p">(</span><span class="n">QgsMarkerSymbolLayer</span><span class="p">):</span>
<span class="linenos"> 5</span>
<span class="linenos"> 6</span>  <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">radius</span><span class="o">=</span><span class="mf">4.0</span><span class="p">):</span>
<span class="linenos"> 7</span>      <span class="n">QgsMarkerSymbolLayer</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
<span class="linenos"> 8</span>      <span class="bp">self</span><span class="o">.</span><span class="n">radius</span> <span class="o">=</span> <span class="n">radius</span>
<span class="linenos"> 9</span>      <span class="bp">self</span><span class="o">.</span><span class="n">color</span> <span class="o">=</span> <span class="n">QColor</span><span class="p">(</span><span class="mi">255</span><span class="p">,</span><span class="mi">0</span><span class="p">,</span><span class="mi">0</span><span class="p">)</span>
<span class="linenos">10</span>
<span class="linenos">11</span>  <span class="k">def</span> <span class="nf">layerType</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">12</span>     <span class="k">return</span> <span class="s2">&quot;FooMarker&quot;</span>
<span class="linenos">13</span>
<span class="linenos">14</span>  <span class="k">def</span> <span class="nf">properties</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">15</span>      <span class="k">return</span> <span class="p">{</span> <span class="s2">&quot;radius&quot;</span> <span class="p">:</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">radius</span><span class="p">)</span> <span class="p">}</span>
<span class="linenos">16</span>
<span class="linenos">17</span>  <span class="k">def</span> <span class="nf">startRender</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">context</span><span class="p">):</span>
<span class="linenos">18</span>    <span class="k">pass</span>
<span class="linenos">19</span>
<span class="linenos">20</span>  <span class="k">def</span> <span class="nf">stopRender</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">context</span><span class="p">):</span>
<span class="linenos">21</span>      <span class="k">pass</span>
<span class="linenos">22</span>
<span class="linenos">23</span>  <span class="k">def</span> <span class="nf">renderPoint</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">point</span><span class="p">,</span> <span class="n">context</span><span class="p">):</span>
<span class="linenos">24</span>      <span class="c1"># Rendering depends on whether the symbol is selected (QGIS &gt;= 1.5)</span>
<span class="linenos">25</span>      <span class="n">color</span> <span class="o">=</span> <span class="n">context</span><span class="o">.</span><span class="n">selectionColor</span><span class="p">()</span> <span class="k">if</span> <span class="n">context</span><span class="o">.</span><span class="n">selected</span><span class="p">()</span> <span class="k">else</span> <span class="bp">self</span><span class="o">.</span><span class="n">color</span>
<span class="linenos">26</span>      <span class="n">p</span> <span class="o">=</span> <span class="n">context</span><span class="o">.</span><span class="n">renderContext</span><span class="p">()</span><span class="o">.</span><span class="n">painter</span><span class="p">()</span>
<span class="linenos">27</span>      <span class="n">p</span><span class="o">.</span><span class="n">setPen</span><span class="p">(</span><span class="n">color</span><span class="p">)</span>
<span class="linenos">28</span>      <span class="n">p</span><span class="o">.</span><span class="n">drawEllipse</span><span class="p">(</span><span class="n">point</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">radius</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">radius</span><span class="p">)</span>
<span class="linenos">29</span>
<span class="linenos">30</span>  <span class="k">def</span> <span class="nf">clone</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">31</span>      <span class="k">return</span> <span class="n">FooSymbolLayer</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">radius</span><span class="p">)</span>
</pre></div>
</div>
<p>The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.layerType" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">layerType()</span></code></a> method determines
the name of the symbol layer; it has to be unique among all symbol layers.
The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.properties" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">properties()</span></code></a> method is used
for persistence of attributes. The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.clone" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">clone()</span></code></a>
method must return a copy of the symbol layer with
all attributes being exactly the same. Finally there are rendering methods:
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.startRender" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">startRender()</span></code></a> is called before
rendering the first feature, <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.stopRender" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">stopRender()</span></code></a>
when the rendering is done, and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsMarkerSymbolLayer.html#qgis.core.QgsMarkerSymbolLayer.renderPoint" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">renderPoint()</span></code></a> is called to do the rendering.
The coordinates of the point(s) are already transformed to the output coordinates.</p>
<p>For polylines and polygons the only difference would be in the rendering
method: you would use
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsLineSymbolLayer.html#qgis.core.QgsLineSymbolLayer.renderPolyline" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">renderPolyline()</span></code></a>
which receives a list of lines,
while <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFillSymbolLayer.html#qgis.core.QgsFillSymbolLayer.renderPolygon" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">renderPolygon()</span></code></a>
receives a list of points on the outer ring as the
first parameter and a list of inner rings (or None) as a second parameter.</p>
<p>Usually it is convenient to add a GUI for setting attributes of the symbol
layer type to allow users to customize the appearance: in case of our example
above we can let user set circle radius. The following code implements such
widget</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.gui</span> <span class="kn">import</span> <span class="n">QgsSymbolLayerWidget</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="k">class</span> <span class="nc">FooSymbolLayerWidget</span><span class="p">(</span><span class="n">QgsSymbolLayerWidget</span><span class="p">):</span>
<span class="linenos"> 4</span>    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">parent</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
<span class="linenos"> 5</span>        <span class="n">QgsSymbolLayerWidget</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">parent</span><span class="p">)</span>
<span class="linenos"> 6</span>
<span class="linenos"> 7</span>        <span class="bp">self</span><span class="o">.</span><span class="n">layer</span> <span class="o">=</span> <span class="kc">None</span>
<span class="linenos"> 8</span>
<span class="linenos"> 9</span>        <span class="c1"># setup a simple UI</span>
<span class="linenos">10</span>        <span class="bp">self</span><span class="o">.</span><span class="n">label</span> <span class="o">=</span> <span class="n">QLabel</span><span class="p">(</span><span class="s2">&quot;Radius:&quot;</span><span class="p">)</span>
<span class="linenos">11</span>        <span class="bp">self</span><span class="o">.</span><span class="n">spinRadius</span> <span class="o">=</span> <span class="n">QDoubleSpinBox</span><span class="p">()</span>
<span class="linenos">12</span>        <span class="bp">self</span><span class="o">.</span><span class="n">hbox</span> <span class="o">=</span> <span class="n">QHBoxLayout</span><span class="p">()</span>
<span class="linenos">13</span>        <span class="bp">self</span><span class="o">.</span><span class="n">hbox</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">label</span><span class="p">)</span>
<span class="linenos">14</span>        <span class="bp">self</span><span class="o">.</span><span class="n">hbox</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">spinRadius</span><span class="p">)</span>
<span class="linenos">15</span>        <span class="bp">self</span><span class="o">.</span><span class="n">setLayout</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">hbox</span><span class="p">)</span>
<span class="linenos">16</span>        <span class="bp">self</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">spinRadius</span><span class="p">,</span> <span class="n">SIGNAL</span><span class="p">(</span><span class="s2">&quot;valueChanged(double)&quot;</span><span class="p">),</span> \
<span class="linenos">17</span>            <span class="bp">self</span><span class="o">.</span><span class="n">radiusChanged</span><span class="p">)</span>
<span class="linenos">18</span>
<span class="linenos">19</span>    <span class="k">def</span> <span class="nf">setSymbolLayer</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">layer</span><span class="p">):</span>
<span class="linenos">20</span>        <span class="k">if</span> <span class="n">layer</span><span class="o">.</span><span class="n">layerType</span><span class="p">()</span> <span class="o">!=</span> <span class="s2">&quot;FooMarker&quot;</span><span class="p">:</span>
<span class="linenos">21</span>            <span class="k">return</span>
<span class="linenos">22</span>        <span class="bp">self</span><span class="o">.</span><span class="n">layer</span> <span class="o">=</span> <span class="n">layer</span>
<span class="linenos">23</span>        <span class="bp">self</span><span class="o">.</span><span class="n">spinRadius</span><span class="o">.</span><span class="n">setValue</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">radius</span><span class="p">)</span>
<span class="linenos">24</span>
<span class="linenos">25</span>    <span class="k">def</span> <span class="nf">symbolLayer</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">26</span>        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">layer</span>
<span class="linenos">27</span>
<span class="linenos">28</span>    <span class="k">def</span> <span class="nf">radiusChanged</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">value</span><span class="p">):</span>
<span class="linenos">29</span>        <span class="bp">self</span><span class="o">.</span><span class="n">layer</span><span class="o">.</span><span class="n">radius</span> <span class="o">=</span> <span class="n">value</span>
<span class="linenos">30</span>        <span class="bp">self</span><span class="o">.</span><span class="n">emit</span><span class="p">(</span><span class="n">SIGNAL</span><span class="p">(</span><span class="s2">&quot;changed()&quot;</span><span class="p">))</span>
</pre></div>
</div>
<p>This widget can be embedded into the symbol properties dialog. When the symbol
layer type is selected in symbol properties dialog, it creates an instance of
the symbol layer and an instance of the symbol layer widget. Then it calls
the <a class="reference external" href="https://qgis.org/pyqgis/3.34/gui/QgsSymbolLayerWidget.html#qgis.gui.QgsSymbolLayerWidget.setSymbolLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setSymbolLayer()</span></code></a> method to
assign the symbol layer to the widget. In that
method the widget should update the UI to reflect the attributes of the symbol
layer. The <a class="reference external" href="https://qgis.org/pyqgis/3.34/gui/QgsSymbolLayerWidget.html#qgis.gui.QgsSymbolLayerWidget.symbolLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">symbolLayer()</span></code></a> method
is used to retrieve the symbol layer again
by the properties dialog to use it for the symbol.</p>
<p>On every change of attributes, the widget should emit the <a class="reference external" href="https://qgis.org/pyqgis/3.34/gui/QgsSymbolLayerWidget.html#qgis.gui.QgsSymbolLayerWidget.changed" title="(in QGIS Python API v3.34)"><code class="xref any docutils literal notranslate"><span class="pre">changed()</span></code></a> signal
to let the properties dialog update the symbol preview.</p>
<p>Now we are missing only the final glue: to make QGIS aware of these new classes.
This is done by adding the symbol layer to registry. It is possible to use the
symbol layer also without adding it to the registry, but some functionality
will not work: e.g. loading of project files with the custom symbol layers or
inability to edit the layer’s attributes in GUI.</p>
<p>We will have to create metadata for the symbol layer</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="n">QgsSymbol</span><span class="p">,</span> <span class="n">QgsSymbolLayerAbstractMetadata</span><span class="p">,</span> <span class="n">QgsSymbolLayerRegistry</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span><span class="k">class</span> <span class="nc">FooSymbolLayerMetadata</span><span class="p">(</span><span class="n">QgsSymbolLayerAbstractMetadata</span><span class="p">):</span>
<span class="linenos"> 4</span>
<span class="linenos"> 5</span>  <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos"> 6</span>    <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="s2">&quot;FooMarker&quot;</span><span class="p">,</span> <span class="s2">&quot;My new Foo marker&quot;</span><span class="p">,</span> <span class="n">QgsSymbol</span><span class="o">.</span><span class="n">Marker</span><span class="p">)</span>
<span class="linenos"> 7</span>
<span class="linenos"> 8</span>  <span class="k">def</span> <span class="nf">createSymbolLayer</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">props</span><span class="p">):</span>
<span class="linenos"> 9</span>    <span class="n">radius</span> <span class="o">=</span> <span class="nb">float</span><span class="p">(</span><span class="n">props</span><span class="p">[</span><span class="s2">&quot;radius&quot;</span><span class="p">])</span> <span class="k">if</span> <span class="s2">&quot;radius&quot;</span> <span class="ow">in</span> <span class="n">props</span> <span class="k">else</span> <span class="mf">4.0</span>
<span class="linenos">10</span>    <span class="k">return</span> <span class="n">FooSymbolLayer</span><span class="p">(</span><span class="n">radius</span><span class="p">)</span>
<span class="linenos">11</span>
<span class="linenos">12</span><span class="n">fslmetadata</span> <span class="o">=</span> <span class="n">FooSymbolLayerMetadata</span><span class="p">()</span>
</pre></div>
</div>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">QgsApplication</span><span class="o">.</span><span class="n">symbolLayerRegistry</span><span class="p">()</span><span class="o">.</span><span class="n">addSymbolLayerType</span><span class="p">(</span><span class="n">fslmetadata</span><span class="p">)</span>
</pre></div>
</div>
<p>You should pass layer type (the same as returned by the layer) and symbol type
(marker/line/fill) to the constructor of the parent class. The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayerAbstractMetadata.html#qgis.core.QgsSymbolLayerAbstractMetadata.createSymbolLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createSymbolLayer()</span></code></a> method
takes care of creating an instance of symbol layer with attributes specified in
the <cite>props</cite> dictionary. And there is the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsSymbolLayerAbstractMetadata.html#qgis.core.QgsSymbolLayerAbstractMetadata.createSymbolLayerWidget" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createSymbolLayerWidget()</span></code></a> method which
returns the settings widget for this symbol layer type.</p>
<p>The last step is to add this symbol layer to the registry — and we are done.</p>
</section>
</section>
<section id="creating-custom-renderers">
<span id="index-15"></span><h3><a class="toc-backref" href="#id26" role="doc-backlink"><span class="section-number">6.8.5. </span>Creating Custom Renderers</a><a class="headerlink" href="#creating-custom-renderers" title="Link to this heading"></a></h3>
<p>It might be useful to create a new renderer implementation if you would like to
customize the rules how to select symbols for rendering of features. Some use
cases where you would want to do it: symbol is determined from a combination of
fields, size of symbols changes depending on current scale etc.</p>
<p>The following code shows a simple custom renderer that creates two marker
symbols and chooses randomly one of them for every feature</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">import</span> <span class="nn">random</span>
<span class="linenos"> 2</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="n">QgsWkbTypes</span><span class="p">,</span> <span class="n">QgsSymbol</span><span class="p">,</span> <span class="n">QgsFeatureRenderer</span>
<span class="linenos"> 3</span>
<span class="linenos"> 4</span>
<span class="linenos"> 5</span><span class="k">class</span> <span class="nc">RandomRenderer</span><span class="p">(</span><span class="n">QgsFeatureRenderer</span><span class="p">):</span>
<span class="linenos"> 6</span>  <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">syms</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
<span class="linenos"> 7</span>    <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="s2">&quot;RandomRenderer&quot;</span><span class="p">)</span>
<span class="linenos"> 8</span>    <span class="bp">self</span><span class="o">.</span><span class="n">syms</span> <span class="o">=</span> <span class="n">syms</span> <span class="k">if</span> <span class="n">syms</span> <span class="k">else</span> <span class="p">[</span>
<span class="linenos"> 9</span>      <span class="n">QgsSymbol</span><span class="o">.</span><span class="n">defaultSymbol</span><span class="p">(</span><span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">geometryType</span><span class="p">(</span><span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">Point</span><span class="p">)),</span>
<span class="linenos">10</span>      <span class="n">QgsSymbol</span><span class="o">.</span><span class="n">defaultSymbol</span><span class="p">(</span><span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">geometryType</span><span class="p">(</span><span class="n">QgsWkbTypes</span><span class="o">.</span><span class="n">Point</span><span class="p">))</span>
<span class="linenos">11</span>    <span class="p">]</span>
<span class="linenos">12</span>
<span class="linenos">13</span>  <span class="k">def</span> <span class="nf">symbolForFeature</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">feature</span><span class="p">,</span> <span class="n">context</span><span class="p">):</span>
<span class="linenos">14</span>    <span class="k">return</span> <span class="n">random</span><span class="o">.</span><span class="n">choice</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">syms</span><span class="p">)</span>
<span class="linenos">15</span>
<span class="linenos">16</span>  <span class="k">def</span> <span class="nf">startRender</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">context</span><span class="p">,</span> <span class="n">fields</span><span class="p">):</span>
<span class="linenos">17</span>    <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">startRender</span><span class="p">(</span><span class="n">context</span><span class="p">,</span> <span class="n">fields</span><span class="p">)</span>
<span class="linenos">18</span>    <span class="k">for</span> <span class="n">s</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">syms</span><span class="p">:</span>
<span class="linenos">19</span>      <span class="n">s</span><span class="o">.</span><span class="n">startRender</span><span class="p">(</span><span class="n">context</span><span class="p">,</span> <span class="n">fields</span><span class="p">)</span>
<span class="linenos">20</span>
<span class="linenos">21</span>  <span class="k">def</span> <span class="nf">stopRender</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">context</span><span class="p">):</span>
<span class="linenos">22</span>    <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">stopRender</span><span class="p">(</span><span class="n">context</span><span class="p">)</span>
<span class="linenos">23</span>    <span class="k">for</span> <span class="n">s</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">syms</span><span class="p">:</span>
<span class="linenos">24</span>      <span class="n">s</span><span class="o">.</span><span class="n">stopRender</span><span class="p">(</span><span class="n">context</span><span class="p">)</span>
<span class="linenos">25</span>
<span class="linenos">26</span>  <span class="k">def</span> <span class="nf">usedAttributes</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">context</span><span class="p">):</span>
<span class="linenos">27</span>    <span class="k">return</span> <span class="p">[]</span>
<span class="linenos">28</span>
<span class="linenos">29</span>  <span class="k">def</span> <span class="nf">clone</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">30</span>    <span class="k">return</span> <span class="n">RandomRenderer</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">syms</span><span class="p">)</span>
</pre></div>
</div>
<p>The constructor of the parent <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRenderer.html#qgis.core.QgsFeatureRenderer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsFeatureRenderer</span></code></a>
class needs a renderer name (which has to be unique among renderers). The
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRenderer.html#qgis.core.QgsFeatureRenderer.symbolForFeature" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">symbolForFeature()</span></code></a> method
is the one that decides what symbol will be used for a particular feature.
<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRenderer.html#qgis.core.QgsFeatureRenderer.startRender" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">startRender()</span></code></a> and <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRenderer.html#qgis.core.QgsFeatureRenderer.stopRender" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">stopRender()</span></code></a> take care of initialization/finalization
of symbol rendering. The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRenderer.html#qgis.core.QgsFeatureRenderer.usedAttributes" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">usedAttributes()</span></code></a>
method can return a list of field names that the renderer expects to be present.
Finally, the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsFeatureRenderer.html#qgis.core.QgsFeatureRenderer.clone" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">clone()</span></code></a> method
should return a copy of the renderer.</p>
<p>Like with symbol layers, it is possible to attach a GUI for configuration of
the renderer. It has to be derived from <a class="reference external" href="https://qgis.org/pyqgis/3.34/gui/QgsRendererWidget.html#qgis.gui.QgsRendererWidget" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsRendererWidget</span></code></a>.
The following sample code creates a button that allows the user to set the
first symbol</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.gui</span> <span class="kn">import</span> <span class="n">QgsRendererWidget</span><span class="p">,</span> <span class="n">QgsColorButton</span>
<span class="linenos"> 2</span>
<span class="linenos"> 3</span>
<span class="linenos"> 4</span><span class="k">class</span> <span class="nc">RandomRendererWidget</span><span class="p">(</span><span class="n">QgsRendererWidget</span><span class="p">):</span>
<span class="linenos"> 5</span>  <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">layer</span><span class="p">,</span> <span class="n">style</span><span class="p">,</span> <span class="n">renderer</span><span class="p">):</span>
<span class="linenos"> 6</span>    <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="n">layer</span><span class="p">,</span> <span class="n">style</span><span class="p">)</span>
<span class="linenos"> 7</span>    <span class="k">if</span> <span class="n">renderer</span> <span class="ow">is</span> <span class="kc">None</span> <span class="ow">or</span> <span class="n">renderer</span><span class="o">.</span><span class="n">type</span><span class="p">()</span> <span class="o">!=</span> <span class="s2">&quot;RandomRenderer&quot;</span><span class="p">:</span>
<span class="linenos"> 8</span>      <span class="bp">self</span><span class="o">.</span><span class="n">r</span> <span class="o">=</span> <span class="n">RandomRenderer</span><span class="p">()</span>
<span class="linenos"> 9</span>    <span class="k">else</span><span class="p">:</span>
<span class="linenos">10</span>      <span class="bp">self</span><span class="o">.</span><span class="n">r</span> <span class="o">=</span> <span class="n">renderer</span>
<span class="linenos">11</span>    <span class="c1"># setup UI</span>
<span class="linenos">12</span>    <span class="bp">self</span><span class="o">.</span><span class="n">btn1</span> <span class="o">=</span> <span class="n">QgsColorButton</span><span class="p">()</span>
<span class="linenos">13</span>    <span class="bp">self</span><span class="o">.</span><span class="n">btn1</span><span class="o">.</span><span class="n">setColor</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">r</span><span class="o">.</span><span class="n">syms</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">color</span><span class="p">())</span>
<span class="linenos">14</span>    <span class="bp">self</span><span class="o">.</span><span class="n">vbox</span> <span class="o">=</span> <span class="n">QVBoxLayout</span><span class="p">()</span>
<span class="linenos">15</span>    <span class="bp">self</span><span class="o">.</span><span class="n">vbox</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">btn1</span><span class="p">)</span>
<span class="linenos">16</span>    <span class="bp">self</span><span class="o">.</span><span class="n">setLayout</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">vbox</span><span class="p">)</span>
<span class="linenos">17</span>    <span class="bp">self</span><span class="o">.</span><span class="n">btn1</span><span class="o">.</span><span class="n">colorChanged</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">setColor1</span><span class="p">)</span>
<span class="linenos">18</span>
<span class="linenos">19</span>  <span class="k">def</span> <span class="nf">setColor1</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">20</span>    <span class="n">color</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">btn1</span><span class="o">.</span><span class="n">color</span><span class="p">()</span>
<span class="linenos">21</span>    <span class="k">if</span> <span class="ow">not</span> <span class="n">color</span><span class="o">.</span><span class="n">isValid</span><span class="p">():</span> <span class="k">return</span>
<span class="linenos">22</span>    <span class="bp">self</span><span class="o">.</span><span class="n">r</span><span class="o">.</span><span class="n">syms</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">setColor</span><span class="p">(</span><span class="n">color</span><span class="p">)</span>
<span class="linenos">23</span>
<span class="linenos">24</span>  <span class="k">def</span> <span class="nf">renderer</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">25</span>    <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">r</span>
</pre></div>
</div>
<p>The constructor receives instances of the active layer (<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsVectorLayer</span></code></a>), the global style (<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsStyle.html#qgis.core.QgsStyle" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsStyle</span></code></a>) and the current renderer. If there is no
renderer or the renderer has different type, it will be replaced with our new
renderer, otherwise we will use the current renderer (which has already the
type we need). The widget contents should be updated to show current state of
the renderer. When the renderer dialog is accepted, the widget’s <a class="reference external" href="https://qgis.org/pyqgis/3.34/gui/QgsRendererWidget.html#qgis.gui.QgsRendererWidget.renderer" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">renderer()</span></code></a> method is called to get the current
renderer — it will be assigned to the layer.</p>
<p>The last missing bit is the renderer metadata and registration in registry,
otherwise loading of layers with the renderer will not work and user will not
be able to select it from the list of renderers. Let us finish our
RandomRenderer example</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="p">(</span>
<span class="linenos"> 2</span>  <span class="n">QgsRendererAbstractMetadata</span><span class="p">,</span>
<span class="linenos"> 3</span>  <span class="n">QgsRendererRegistry</span><span class="p">,</span>
<span class="linenos"> 4</span>  <span class="n">QgsApplication</span>
<span class="linenos"> 5</span><span class="p">)</span>
<span class="linenos"> 6</span>
<span class="linenos"> 7</span><span class="k">class</span> <span class="nc">RandomRendererMetadata</span><span class="p">(</span><span class="n">QgsRendererAbstractMetadata</span><span class="p">):</span>
<span class="linenos"> 8</span>
<span class="linenos"> 9</span>  <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">10</span>    <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="s2">&quot;RandomRenderer&quot;</span><span class="p">,</span> <span class="s2">&quot;Random renderer&quot;</span><span class="p">)</span>
<span class="linenos">11</span>
<span class="linenos">12</span>  <span class="k">def</span> <span class="nf">createRenderer</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">element</span><span class="p">):</span>
<span class="linenos">13</span>    <span class="k">return</span> <span class="n">RandomRenderer</span><span class="p">()</span>
<span class="linenos">14</span>
<span class="linenos">15</span>  <span class="k">def</span> <span class="nf">createRendererWidget</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">layer</span><span class="p">,</span> <span class="n">style</span><span class="p">,</span> <span class="n">renderer</span><span class="p">):</span>
<span class="linenos">16</span>    <span class="k">return</span> <span class="n">RandomRendererWidget</span><span class="p">(</span><span class="n">layer</span><span class="p">,</span> <span class="n">style</span><span class="p">,</span> <span class="n">renderer</span><span class="p">)</span>
<span class="linenos">17</span>
<span class="linenos">18</span><span class="n">rrmetadata</span> <span class="o">=</span> <span class="n">RandomRendererMetadata</span><span class="p">()</span>
</pre></div>
</div>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">QgsApplication</span><span class="o">.</span><span class="n">rendererRegistry</span><span class="p">()</span><span class="o">.</span><span class="n">addRenderer</span><span class="p">(</span><span class="n">rrmetadata</span><span class="p">)</span>
</pre></div>
</div>
<p>Similarly as with symbol layers, abstract metadata constructor awaits renderer
name, name visible for users and optionally name of renderer’s icon.
The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererAbstractMetadata.html#qgis.core.QgsRendererAbstractMetadata.createRenderer" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createRenderer()</span></code></a>
method passes a <code class="xref py py-class docutils literal notranslate"><span class="pre">QDomElement</span></code> instance that can be
used to restore the renderer’s state from the DOM tree. The <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererAbstractMetadata.html#qgis.core.QgsRendererAbstractMetadata.createRendererWidget" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">createRendererWidget()</span></code></a>
method creates the configuration widget. It does not have to be present or can
return <code class="docutils literal notranslate"><span class="pre">None</span></code> if the renderer does not come with GUI.</p>
<p>To associate an icon with the renderer you can assign it in
the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererAbstractMetadata.html#qgis.core.QgsRendererAbstractMetadata" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsRendererAbstractMetadata</span></code></a>
constructor as a third (optional)
argument — the base class constructor in the RandomRendererMetadata <code class="xref py py-func docutils literal notranslate"><span class="pre">__init__()</span></code>
function becomes</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="n">QgsRendererAbstractMetadata</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
       <span class="s2">&quot;RandomRenderer&quot;</span><span class="p">,</span>
       <span class="s2">&quot;Random renderer&quot;</span><span class="p">,</span>
       <span class="n">QIcon</span><span class="p">(</span><span class="n">QPixmap</span><span class="p">(</span><span class="s2">&quot;RandomRendererIcon.png&quot;</span><span class="p">,</span> <span class="s2">&quot;png&quot;</span><span class="p">)))</span>
</pre></div>
</div>
<p>The icon can also be associated at any later time using the <a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsRendererAbstractMetadata.html#qgis.core.QgsRendererAbstractMetadata.setIcon" title="(in QGIS Python API v3.34)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">setIcon()</span></code></a> method
of the metadata class. The icon can be loaded from a file (as shown above) or
can be loaded from a <a class="reference external" href="https://doc.qt.io/qt-5/resources.html">Qt resource</a>
(PyQt5 includes .qrc compiler for Python).</p>
</section>
</section>
<section id="further-topics">
<h2><a class="toc-backref" href="#id27" role="doc-backlink"><span class="section-number">6.9. </span>Further Topics</a><a class="headerlink" href="#further-topics" title="Link to this heading"></a></h2>
<p><strong>TODO:</strong></p>
<ul class="simple">
<li><p>creating/modifying symbols</p></li>
<li><p>working with style (<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsStyle.html#qgis.core.QgsStyle" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsStyle</span></code></a>)</p></li>
<li><p>working with color ramps (<a class="reference external" href="https://qgis.org/pyqgis/3.34/core/QgsColorRamp.html#qgis.core.QgsColorRamp" title="(in QGIS Python API v3.34)"><code class="xref py py-class docutils literal notranslate"><span class="pre">QgsColorRamp</span></code></a>)</p></li>
<li><p>exploring symbol layer and renderer registries</p></li>
</ul>
</section>
</section>


           </div>
          </div>
          <footer><div class="rst-footer-buttons" role="navigation" aria-label="Footer">
        <a href="raster.html" class="btn btn-neutral float-left" title="5. Using Raster Layers" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="geometry.html" class="btn btn-neutral float-right" title="7. Geometry Handling" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
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
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/vector.html">en</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/cs/docs/pyqgis_developer_cookbook/vector.html">cs</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/de/docs/pyqgis_developer_cookbook/vector.html">de</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/es/docs/pyqgis_developer_cookbook/vector.html">es</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/fr/docs/pyqgis_developer_cookbook/vector.html">fr</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/hu/docs/pyqgis_developer_cookbook/vector.html">hu</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/it/docs/pyqgis_developer_cookbook/vector.html">it</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ja/docs/pyqgis_developer_cookbook/vector.html">ja</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ko/docs/pyqgis_developer_cookbook/vector.html">ko</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/lt/docs/pyqgis_developer_cookbook/vector.html">lt</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/nl/docs/pyqgis_developer_cookbook/vector.html">nl</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_BR/docs/pyqgis_developer_cookbook/vector.html">pt_BR</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_PT/docs/pyqgis_developer_cookbook/vector.html">pt_PT</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ro/docs/pyqgis_developer_cookbook/vector.html">ro</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ru/docs/pyqgis_developer_cookbook/vector.html">ru</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/zh-Hans/docs/pyqgis_developer_cookbook/vector.html">zh-Hans</a></dd>
        
      </dl>

      <dl>
        <dt>Versions</dt>
        
          <dd><a href="https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/vector.html">testing</a></dd>
        
          <dd><a href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/vector.html">latest</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/vector.html">3.40</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/vector.html">3.34</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/vector.html">3.28</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/vector.html">3.22</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/vector.html">3.16</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.10/en/docs/pyqgis_developer_cookbook/vector.html">3.10</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.4/en/docs/pyqgis_developer_cookbook/vector.html">3.4</a></dd>
        
          <dd><a href="https://docs.qgis.org/2.18/en/docs/pyqgis_developer_cookbook/vector.html">2.18</a></dd>
        
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

