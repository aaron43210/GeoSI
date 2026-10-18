Title: Live Content

Description: Fetched live

Source: https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html

---

<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="../../../../">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>28.1.15. Raster analysis &mdash; QGIS Documentation  documentation</title>
      <link rel="stylesheet" type="text/css" href="../../../../_static/pygments.css?v=80d5e7a1" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/css/qgis_docs.css?v=01847ad1" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/togglebutton.css?v=13237357" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/copybutton.css?v=76b2166b" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/css/qgis_topbar.css?v=5613a779" />

  
    <link rel="shortcut icon" href="../../../../_static/qgis_logo.ico"/>
    <link rel="canonical" href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html"/>
  <!--[if lt IE 9]>
    <script src="../../../../_static/js/html5shiv.min.js"></script>
  <![endif]-->
  
        <script src="../../../../_static/jquery.js?v=5d32c60e"></script>
        <script src="../../../../_static/_sphinx_javascript_frameworks_compat.js?v=2cd50e6c"></script>
        <script src="../../../../_static/documentation_options.js?v=5929fcd5"></script>
        <script src="../../../../_static/doctools.js?v=888ff710"></script>
        <script src="../../../../_static/sphinx_highlight.js?v=dc90522c"></script>
        <script src="../../../../_static/clipboard.min.js?v=a7894cd8"></script>
        <script src="../../../../_static/copybutton.js?v=f281be69"></script>
        <script>let toggleHintShow = 'Click to show';</script>
        <script>let toggleHintHide = 'Click to hide';</script>
        <script>let toggleOpenOnPrint = 'true';</script>
        <script src="../../../../_static/togglebutton.js?v=4a39c7ea"></script>
        <script>var togglebuttonSelector = '.toggle, .admonition.dropdown';</script>
        <script>var togglebuttonSelector = '.toggle, .admonition.dropdown';</script>
    <script src="../../../../_static/js/theme.js"></script>
    <link rel="index" title="Index" href="../../../../genindex.html" />
    <link rel="search" title="Search" href="../../../../search.html" />
    <link rel="next" title="28.1.16. Raster Creation" href="rastercreation.html" />
    <link rel="prev" title="28.1.14. Point Cloud Extraction" href="pointcloudextraction.html" />
  <meta name="description" content="QGIS 3.34 documentation: 28.1.15. Raster analysis">
  <meta name="robots" content="noindex">
</head>

<body class="wy-body-for-nav">

  <nav class="release_status_topbar">
    <div class="row outdated">
     This documentation is for a QGIS version which has reached end of life. Instead visit the <a href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">latest version</a>.
    </div>
  </nav>

   

 
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search" >
   

          
          
          <a href="../../../index.html" class="icon icon-home">
            QGIS Documentation
              <img src="../../../../_static/logo.png" class="logo" alt="Logo"/>
          </a>
              <div class="version">
                3.34
              </div>
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="../../../../search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" aria-label="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>
   <a href= "../../../../genindex.html">Index</a>
 
        </div><div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="Navigation menu">
              <p class="caption" role="heading"><span class="caption-text">For Users</span></p>
<ul class="current">
<li class="toctree-l1 current"><a class="reference internal" href="../../index.html">QGIS Desktop User Guide/Manual (QGIS 3.34)</a><ul class="current">
<li class="toctree-l2"><a class="reference internal" href="../../preamble/preamble.html">1. Preamble</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../preamble/foreword.html">2. Foreword</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../preamble/conventions.html">3. Conventions</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../preamble/features.html">4. Features</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../introduction/getting_started.html">5. Getting Started</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../introduction/project_files.html">6. Working with Project Files</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../introduction/qgis_gui.html">7. QGIS GUI</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../introduction/browser.html">8. The Browser panel</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../introduction/qgis_configuration.html">9. QGIS Configuration</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_projections/working_with_projections.html">10. Working with Projections</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../map_views/index.html">11. Visualizing Maps</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../introduction/general_tools.html">12. General Tools</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../expressions/index.html">13. Level up with Expressions</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../style_library/index.html">14. The Style Library</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../managing_data_source/index.html">15. Managing Data Source</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_vector/index.html">16. Working with Vector Data</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_raster/index.html">17. Working with Raster Data</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_mesh/mesh.html">18. Working with Mesh Data</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_vector_tiles/vector_tiles.html">19. Working with Vector Tiles</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_point_clouds/point_clouds.html">20. Working with Point Clouds</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_3d_tiles/3d_tiles.html">21. Working with 3D Tiles</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../print_composer/index.html">22. Laying out the maps</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_ogc/ogc_client_support.html">23. Working with OGC / ISO protocols</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../working_with_gps/index.html">24. Working with GPS Data</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../auth_system/index.html">25. Authentication System</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../grass_integration/grass_integration.html">26. GRASS GIS Integration</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../processing/index.html">27. QGIS processing framework</a></li>
<li class="toctree-l2 current"><a class="reference internal" href="../index.html">28. Processing providers and algorithms</a><ul class="current">
<li class="toctree-l3 current"><a class="reference internal" href="index.html">28.1. QGIS algorithm provider</a><ul class="current">
<li class="toctree-l4"><a class="reference internal" href="3dtiles.html">28.1.1. 3D Tiles</a></li>
<li class="toctree-l4"><a class="reference internal" href="cartography.html">28.1.2. Cartography</a></li>
<li class="toctree-l4"><a class="reference internal" href="database.html">28.1.3. Database</a></li>
<li class="toctree-l4"><a class="reference internal" href="filetools.html">28.1.4. File tools</a></li>
<li class="toctree-l4"><a class="reference internal" href="gps.html">28.1.5. GPS</a></li>
<li class="toctree-l4"><a class="reference internal" href="interpolation.html">28.1.6. Interpolation</a></li>
<li class="toctree-l4"><a class="reference internal" href="layertools.html">28.1.7. Layer tools</a></li>
<li class="toctree-l4"><a class="reference internal" href="mesh.html">28.1.8. Mesh</a></li>
<li class="toctree-l4"><a class="reference internal" href="modelertools.html">28.1.9. Modeler tools</a></li>
<li class="toctree-l4"><a class="reference internal" href="networkanalysis.html">28.1.10. Network analysis</a></li>
<li class="toctree-l4"><a class="reference internal" href="plots.html">28.1.11. Plots</a></li>
<li class="toctree-l4"><a class="reference internal" href="pointcloudconversion.html">28.1.12. Point Cloud Conversion</a></li>
<li class="toctree-l4"><a class="reference internal" href="pointclouddatamanagement.html">28.1.13. Point Cloud Data Management</a></li>
<li class="toctree-l4"><a class="reference internal" href="pointcloudextraction.html">28.1.14. Point Cloud Extraction</a></li>
<li class="toctree-l4 current"><a class="current reference internal" href="#">28.1.15. Raster analysis</a></li>
<li class="toctree-l4"><a class="reference internal" href="rastercreation.html">28.1.16. Raster Creation</a></li>
<li class="toctree-l4"><a class="reference internal" href="rasterterrainanalysis.html">28.1.17. Raster terrain analysis</a></li>
<li class="toctree-l4"><a class="reference internal" href="rastertools.html">28.1.18. Raster tools</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectoranalysis.html">28.1.19. Vector analysis</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectorcreation.html">28.1.20. Vector creation</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectorgeneral.html">28.1.21. Vector general</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectorgeometry.html">28.1.22. Vector geometry</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectoroverlay.html">28.1.23. Vector overlay</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectorselection.html">28.1.24. Vector selection</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectortable.html">28.1.25. Vector table</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectortiles.html">28.1.26. Vector Tiles</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="../gdal/index.html">28.2. GDAL algorithm provider</a></li>
<li class="toctree-l3"><a class="reference internal" href="../otb.html">28.3. OTB applications provider</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="../../plugins/index.html">29. Plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../preamble/help_and_support.html">30. Help and Support</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../preamble/contributors.html">31. Contributors</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../appendices/index.html">32. Appendices</a></li>
<li class="toctree-l2"><a class="reference internal" href="../../literature_web/literature_and_web_references.html">33. Literature and Web References</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="../../../server_manual/index.html">QGIS Server Guide/Manual (QGIS 3.34)</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../training_manual/index.html">Training Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../gentle_gis_introduction/index.html">A Gentle Introduction to GIS</a></li>
</ul>
<p class="caption" role="heading"><span class="caption-text">For Writers</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="../../../documentation_guidelines/index.html">Documentation Guidelines</a></li>
</ul>
<p class="caption" role="heading"><span class="caption-text">For Developers</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="../../../pyqgis_developer_cookbook/index.html">PyQGIS Cookbook (QGIS 3.34)</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../../developers_guide/index.html">Developers Guide</a></li>
</ul>

        </div>
      </div>
    </nav>

    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap"><nav class="wy-nav-top" aria-label="Mobile navigation menu" >
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="../../../index.html">QGIS Documentation</a>
      </nav>

      <div class="wy-nav-content">
        <div class="rst-content">
          <div role="navigation" aria-label="Page navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="../../../index.html" class="icon icon-home" aria-label="Home"></a></li>
          <li class="breadcrumb-item"><a href="../../index.html">QGIS User Guide</a></li>
          <li class="breadcrumb-item"><a href="../index.html"><span class="section-number">28. </span>Processing providers and algorithms</a></li>
          <li class="breadcrumb-item"><a href="index.html"><span class="section-number">28.1. </span>QGIS algorithm provider</a></li>
      <li class="breadcrumb-item active"><span class="section-number">28.1.15. </span>Raster analysis</li>

    <li style="float: right; text-align: right;">
	<ul>
		
      <li class="wy-breadcrumbs-aside">
            <a href="../../../../_sources/docs/user_manual/processing_algs/qgis/rasteranalysis.rst.txt" rel="nofollow"> View page source</a>
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
        <a href="pointcloudextraction.html" class="btn btn-neutral float-left" title="28.1.14. Point Cloud Extraction" accesskey="p"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="rastercreation.html" class="btn btn-neutral float-right" title="28.1.16. Raster Creation" accesskey="n">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
  </div>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <blockquote>
<div></div></blockquote>
<section id="raster-analysis">
<h1><span class="section-number">28.1.15. </span>Raster analysis<a class="headerlink" href="#raster-analysis" title="Link to this heading"></a></h1>
<nav class="contents toc-columns local" id="contents">
<ul class="simple">
<li><p><a class="reference internal" href="#cell-stack-percent-rank-from-value" id="id132">Cell stack percent rank from value</a></p></li>
<li><p><a class="reference internal" href="#cell-stack-percentile" id="id133">Cell stack percentile</a></p></li>
<li><p><a class="reference internal" href="#cell-stack-percentrank-from-raster-layer" id="id134">Cell stack percentrank from raster layer</a></p></li>
<li><p><a class="reference internal" href="#cell-statistics" id="id135">Cell statistics</a></p></li>
<li><p><a class="reference internal" href="#equal-to-frequency" id="id136">Equal to frequency</a></p></li>
<li><p><a class="reference internal" href="#fuzzify-raster-gaussian-membership" id="id137">Fuzzify raster (gaussian membership)</a></p></li>
<li><p><a class="reference internal" href="#fuzzify-raster-large-membership" id="id138">Fuzzify raster (large membership)</a></p></li>
<li><p><a class="reference internal" href="#fuzzify-raster-linear-membership" id="id139">Fuzzify raster (linear membership)</a></p></li>
<li><p><a class="reference internal" href="#fuzzify-raster-near-membership" id="id140">Fuzzify raster (near membership)</a></p></li>
<li><p><a class="reference internal" href="#fuzzify-raster-power-membership" id="id141">Fuzzify raster (power membership)</a></p></li>
<li><p><a class="reference internal" href="#fuzzify-raster-small-membership" id="id142">Fuzzify raster (small membership)</a></p></li>
<li><p><a class="reference internal" href="#greater-than-frequency" id="id143">Greater than frequency</a></p></li>
<li><p><a class="reference internal" href="#highest-position-in-raster-stack" id="id144">Highest position in raster stack</a></p></li>
<li><p><a class="reference internal" href="#less-than-frequency" id="id145">Less than frequency</a></p></li>
<li><p><a class="reference internal" href="#lowest-position-in-raster-stack" id="id146">Lowest position in raster stack</a></p></li>
<li><p><a class="reference internal" href="#raster-boolean-and" id="id147">Raster boolean AND</a></p></li>
<li><p><a class="reference internal" href="#raster-boolean-or" id="id148">Raster boolean OR</a></p></li>
<li><p><a class="reference internal" href="#raster-calculator" id="id149">Raster calculator</a></p></li>
<li><p><a class="reference internal" href="#raster-calculator-virtual" id="id150">Raster calculator (virtual)</a></p></li>
<li><p><a class="reference internal" href="#raster-layer-properties" id="id151">Raster layer properties</a></p></li>
<li><p><a class="reference internal" href="#raster-layer-statistics" id="id152">Raster layer statistics</a></p></li>
<li><p><a class="reference internal" href="#raster-layer-unique-values-report" id="id153">Raster layer unique values report</a></p></li>
<li><p><a class="reference internal" href="#raster-layer-zonal-statistics" id="id154">Raster layer zonal statistics</a></p></li>
<li><p><a class="reference internal" href="#raster-surface-volume" id="id155">Raster surface volume</a></p></li>
<li><p><a class="reference internal" href="#reclassify-by-layer" id="id156">Reclassify by layer</a></p></li>
<li><p><a class="reference internal" href="#reclassify-by-table" id="id157">Reclassify by table</a></p></li>
<li><p><a class="reference internal" href="#rescale-raster" id="id158">Rescale raster</a></p></li>
<li><p><a class="reference internal" href="#round-raster" id="id159">Round raster</a></p></li>
<li><p><a class="reference internal" href="#sample-raster-values" id="id160">Sample raster values</a></p></li>
<li><p><a class="reference internal" href="#zonal-histogram" id="id161">Zonal histogram</a></p></li>
<li><p><a class="reference internal" href="#zonal-statistics" id="id162">Zonal statistics</a></p></li>
</ul>
</nav>
<section id="cell-stack-percent-rank-from-value">
<span id="qgiscellstackpercentrankfromvalue"></span><h2><a class="toc-backref" href="#id132" role="doc-backlink"><span class="section-number">28.1.15.1. </span>Cell stack percent rank from value</a><a class="headerlink" href="#cell-stack-percent-rank-from-value" title="Link to this heading"></a></h2>
<p>Calculates the cell-wise percentrank value of a stack of rasters based on
a single input value and writes them to an output raster.</p>
<p>At each cell location, the specified value is ranked among the respective values
in the stack of all overlaid and sorted cell values from the input rasters.
For values outside of the stack value distribution, the algorithm returns NoData
because the value cannot be ranked among the cell values.</p>
<p>There are two methods for percentile calculation:</p>
<ul class="simple">
<li><p>Inclusive linear interpolation (PERCENTRANK.INC)</p></li>
<li><p>Exclusive linear interpolation (PERCENTRANK.EXC)</p></li>
</ul>
<p>The linear interpolation methods return the unique percent rank for different values.
Both interpolation methods follow their counterpart methods implemented
by <a class="reference external" href="https://help.libreoffice.org/latest/en-US/text/scalc/01/04060184.html?DbPAR=CALC#bm_id3148807">LibreOffice</a>
or Microsoft Excel.</p>
<p>The output raster’s extent and resolution is defined by a reference raster.
Input raster layers that do not match the cell size of the reference
raster layer will be resampled using nearest neighbor resampling.
NoData values in any of the input layers will result in a NoData cell output
if the “Ignore NoData values” parameter is not set.
The output raster data type will always be <code class="docutils literal notranslate"><span class="pre">Float32</span></code>.</p>
<figure class="align-center" id="id121">
<img alt="../../../../_images/percentrankfromvalue.png" src="../../../../_images/percentrankfromvalue.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.22 </span><span class="caption-text">Percent ranking Value = 1. <code class="docutils literal notranslate"><span class="pre">NoData</span></code> cells (grey) are ignored.</span><a class="headerlink" href="#id121" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgiscellstackpercentile"><span class="std std-ref">Cell stack percentile</span></a>, <a class="reference internal" href="#qgiscellstackpercentrankfromrasterlayer"><span class="std std-ref">Cell stack percentrank from raster layer</span></a></p>
</div>
<section id="parameters">
<h3>Parameters<a class="headerlink" href="#parameters" title="Link to this heading"></a></h3>
<section id="basic-parameters">
<h4>Basic parameters<a class="headerlink" href="#basic-parameters" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>Raster layers to evaluate.
If multiband rasters are used in the data raster stack, the algorithm
will always perform the analysis on the first band of the rasters</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Method</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Method for percentile calculation:</p>
<ul class="simple">
<li><p>0 — Inclusive linear interpolation (PERCENTRANK.INC)</p></li>
<li><p>1 — Exclusive linear interpolation (PERCENTRANK.EXC)</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 10.0</p>
</td>
<td><p>Value to rank among the respective values in the stack of all overlaid
and sorted cell values from the input rasters</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: True</p>
</td>
<td><p>If unchecked, any NoData cells in the input layers will result in a NoData
cell in the output raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REFERENCE_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer for the output layer creation
(extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="advanced-parameters">
<h4>Advanced parameters<a class="headerlink" href="#advanced-parameters" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NODATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="outputs">
<h3>Outputs<a class="headerlink" href="#outputs" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="python-code">
<h3>Python code<a class="headerlink" href="#python-code" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:cellstackpercentrankfromvalue</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="cell-stack-percentile">
<span id="qgiscellstackpercentile"></span><h2><a class="toc-backref" href="#id133" role="doc-backlink"><span class="section-number">28.1.15.2. </span>Cell stack percentile</a><a class="headerlink" href="#cell-stack-percentile" title="Link to this heading"></a></h2>
<p>Calculates the cell-wise percentile value of a stack of rasters
and writes the results to an output raster. The percentile to return
is determined by the percentile input value (ranges between 0 and 1).
At each cell location, the specified percentile is obtained using the respective
value from the stack of all overlaid and sorted cell values of the input rasters.</p>
<p>There are three methods for percentile calculation:</p>
<ul class="simple">
<li><p>Nearest rank: returns the value that is nearest to the specified percentile</p></li>
<li><p>Inclusive linear interpolation (PERCENTRANK.INC)</p></li>
<li><p>Exclusive linear interpolation (PERCENTRANK.EXC)</p></li>
</ul>
<p>The linear interpolation methods return the unique values for different percentiles.
Both interpolation methods follow their counterpart methods implemented
by <a class="reference external" href="https://help.libreoffice.org/latest/en-US/text/scalc/01/04060184.html?DbPAR=CALC#bm_id3148807">LibreOffice</a>
or Microsoft Excel.</p>
<p>The output raster’s extent and resolution is defined by a reference raster.
Input raster layers that do not match the cell size of the reference
raster layer will be resampled using nearest neighbor resampling.
NoData values in any of the input layers will result in a NoData cell output
if the “Ignore NoData values” parameter is not set.
The output raster data type will always be <code class="docutils literal notranslate"><span class="pre">Float32</span></code>.</p>
<figure class="align-center" id="id122">
<img alt="../../../../_images/percentile.png" src="../../../../_images/percentile.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.23 </span><span class="caption-text">Percentile = 0.25. <code class="docutils literal notranslate"><span class="pre">NoData</span></code> cells (grey) are ignored.</span><a class="headerlink" href="#id122" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgiscellstackpercentile"><span class="std std-ref">Cell stack percentile</span></a>, <a class="reference internal" href="#qgiscellstackpercentrankfromrasterlayer"><span class="std std-ref">Cell stack percentrank from raster layer</span></a></p>
</div>
<section id="id2">
<h3>Parameters<a class="headerlink" href="#id2" title="Link to this heading"></a></h3>
<section id="id3">
<h4>Basic parameters<a class="headerlink" href="#id3" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>Raster layers to evaluate.
If multiband rasters are used in the data raster stack, the algorithm
will always perform the analysis on the first band of the rasters</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Method</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Method for percentile calculation:</p>
<ul class="simple">
<li><p>0 — Nearest rank: returns the value that is nearest to the specified percentile</p></li>
<li><p>1 — Inclusive linear interpolation (PERCENTILE.INC)</p></li>
<li><p>2 — Exclusive linear interpolation (PERCENTILE.EXC)</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Percentile</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.25</p>
</td>
<td><p>Value to rank among the respective values in the stack of all overlaid
and sorted cell values from the input rasters. Between 0 and 1.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: True</p>
</td>
<td><p>If unchecked, any NoData cells in the input layers will result in a NoData
cell in the output raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REFERENCE_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer for the output layer creation
(extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id4">
<h4>Advanced parameters<a class="headerlink" href="#id4" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NODATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id5">
<h3>Outputs<a class="headerlink" href="#id5" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id6">
<h3>Python code<a class="headerlink" href="#id6" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:cellstackpercentile</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="cell-stack-percentrank-from-raster-layer">
<span id="qgiscellstackpercentrankfromrasterlayer"></span><h2><a class="toc-backref" href="#id134" role="doc-backlink"><span class="section-number">28.1.15.3. </span>Cell stack percentrank from raster layer</a><a class="headerlink" href="#cell-stack-percentrank-from-raster-layer" title="Link to this heading"></a></h2>
<p>Calculates the cell-wise percentrank value of a stack of rasters based
on an input value raster and writes them to an output raster.</p>
<p>At each cell location, the current value of the value raster is ranked among
the respective values in the stack of all overlaid and sorted cell values of
the input rasters. For values outside of the the stack value distribution,
the algorithm returns NoData because the value cannot be ranked among the cell values.</p>
<p>There are two methods for percentile calculation:</p>
<ul class="simple">
<li><p>Inclusive linear interpolation (PERCENTRANK.INC)</p></li>
<li><p>Exclusive linear interpolation (PERCENTRANK.EXC)</p></li>
</ul>
<p>The linear interpolation methods return the unique values for different percentiles.
Both interpolation methods follow their counterpart methods implemented
by <a class="reference external" href="https://help.libreoffice.org/latest/en-US/text/scalc/01/04060184.html?DbPAR=CALC#bm_id3148807">LibreOffice</a>
or Microsoft Excel.</p>
<p>The output raster’s extent and resolution is defined by a reference raster.
Input raster layers that do not match the cell size of the reference
raster layer will be resampled using nearest neighbor resampling.
NoData values in any of the input layers will result in a NoData cell output
if the “Ignore NoData values” parameter is not set.
The output raster data type will always be <code class="docutils literal notranslate"><span class="pre">Float32</span></code>.</p>
<figure class="align-center" id="id123">
<img alt="../../../../_images/percentrankfromrasterlayer.png" src="../../../../_images/percentrankfromrasterlayer.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.24 </span><span class="caption-text">Ranking the value raster layer cells. <code class="docutils literal notranslate"><span class="pre">NoData</span></code> cells (grey) are ignored.</span><a class="headerlink" href="#id123" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgiscellstackpercentile"><span class="std std-ref">Cell stack percentile</span></a>, <a class="reference internal" href="#qgiscellstackpercentrankfromvalue"><span class="std std-ref">Cell stack percent rank from value</span></a></p>
</div>
<section id="id8">
<h3>Parameters<a class="headerlink" href="#id8" title="Link to this heading"></a></h3>
<section id="id9">
<h4>Basic parameters<a class="headerlink" href="#id9" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>Raster layers to evaluate.
If multiband rasters are used in the data raster stack, the algorithm
will always perform the analysis on the first band of the rasters</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Value raster layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VALUE_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The layer to rank the values among the stack of all overlaid layers</p></td>
</tr>
<tr class="row-even"><td><p><strong>Value raster band</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VALUE_RASTER_BAND</span></code></p></td>
<td><p>[integer]</p>
<p>Default: 1</p>
</td>
<td><p>Band of the “value raster layer” to compare to</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Method</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Method for percentile calculation:</p>
<ul class="simple">
<li><p>0 — Inclusive linear interpolation (PERCENTRANK.INC)</p></li>
<li><p>1 — Exclusive linear interpolation (PERCENTRANK.EXC)</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: True</p>
</td>
<td><p>If unchecked, any NoData cells in the input layers will result in a NoData
cell in the output raster</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REFERENCE_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer for the output layer creation
(extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id10">
<h4>Advanced parameters<a class="headerlink" href="#id10" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NODATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id11">
<h3>Outputs<a class="headerlink" href="#id11" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id12">
<h3>Python code<a class="headerlink" href="#id12" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:cellstackpercentrankfromrasterlayer</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="cell-statistics">
<span id="qgiscellstatistics"></span><h2><a class="toc-backref" href="#id135" role="doc-backlink"><span class="section-number">28.1.15.4. </span>Cell statistics</a><a class="headerlink" href="#cell-statistics" title="Link to this heading"></a></h2>
<p>Computes per-cell statistics based on input raster layers
and for each cell writes the resulting statistics to an output raster. At each
cell location, the output value is defined as a function of all overlaid
cell values of the input rasters.</p>
<p>By default, a NoData cell in ANY of the input layers will result in a
NoData cell in the output raster.
If the <span class="guilabel">Ignore NoData values</span> option is checked,
then NoData inputs will be ignored in the statistic calculation. This
may result in NoData output for locations where all cells are NoData.</p>
<p>The <span class="guilabel">Reference layer</span> parameter specifies an existing raster layer to
use as a reference when creating the output raster.
The output raster will have the same extent, CRS, and pixel dimensions
as this layer.</p>
<p><strong>Calculation details:</strong>
Input raster layers that do not match the cell size of the reference
raster layer will be resampled using <code class="docutils literal notranslate"><span class="pre">nearest</span> <span class="pre">neighbor</span> <span class="pre">resampling</span></code>.
The output raster data type will be set to the most complex
data type present in the input datasets except when using the
functions <code class="docutils literal notranslate"><span class="pre">Mean</span></code>, <code class="docutils literal notranslate"><span class="pre">Standard</span> <span class="pre">deviation</span></code> and <code class="docutils literal notranslate"><span class="pre">Variance</span></code> (data type is always
<code class="docutils literal notranslate"><span class="pre">Float32</span></code> or <code class="docutils literal notranslate"><span class="pre">Float64</span></code> depending on input float type) or <code class="docutils literal notranslate"><span class="pre">Count</span></code>
and <code class="docutils literal notranslate"><span class="pre">Variety</span></code> (data type is always <code class="docutils literal notranslate"><span class="pre">Int32</span></code>).</p>
<ul class="simple">
<li><p><code class="docutils literal notranslate"><span class="pre">Count</span></code>: The count statistic will always result in the number of cells
without NoData values at the current cell location.</p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">Median</span></code>: If the number of input layers is even, the median will be
calculated as the arithmetic mean of the two middle values of the ordered cell input values.</p></li>
<li><p><code class="docutils literal notranslate"><span class="pre">Minority/Majority</span></code>: If no unique minority or majority could be found,
the result is NoData, except all input cell values are equal.</p></li>
</ul>
<figure class="align-center" id="id124">
<img alt="../../../../_images/cell_statistics_all_stats.png" src="../../../../_images/cell_statistics_all_stats.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.25 </span><span class="caption-text">Example with all the statistic functions. <code class="docutils literal notranslate"><span class="pre">NoData</span></code> cells (grey) are taken into account.</span><a class="headerlink" href="#id124" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id13">
<h3>Parameters<a class="headerlink" href="#id13" title="Link to this heading"></a></h3>
<section id="id14">
<h4>Basic parameters<a class="headerlink" href="#id14" title="Link to this heading"></a></h4>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>Input raster layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Statistic</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">STATISTIC</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Available statistics. Options:</p>
<ul class="simple">
<li><p>0 — Sum</p></li>
<li><p>1 — Count</p></li>
<li><p>2 — Mean</p></li>
<li><p>3 — Median</p></li>
<li><p>4 — Standard deviation</p></li>
<li><p>5 — Variance</p></li>
<li><p>6 — Minimum</p></li>
<li><p>7 — Maximum</p></li>
<li><p>8 — Minority (least common value)</p></li>
<li><p>9 — Majority (most common value)</p></li>
<li><p>10 — Range (max - min)</p></li>
<li><p>11 — Variety (unique value count)</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: True</p>
</td>
<td><p>Calculate statistics also for all cells stacks, ignoring NoData occurrence.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REF_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer to create the output layer
from (extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id15">
<h4>Advanced parameters<a class="headerlink" href="#id15" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NO_DATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id16">
<h3>Outputs<a class="headerlink" href="#id16" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-even"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id17">
<h3>Python code<a class="headerlink" href="#id17" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:cellstatistics</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="equal-to-frequency">
<span id="qgisequaltofrequency"></span><h2><a class="toc-backref" href="#id136" role="doc-backlink"><span class="section-number">28.1.15.5. </span>Equal to frequency</a><a class="headerlink" href="#equal-to-frequency" title="Link to this heading"></a></h2>
<p>Evaluates on a cell-by-cell basis the frequency (number of times) the values
of an input stack of rasters are equal to the value of a value layer.
The output raster extent and resolution are defined by the input raster layer
and is always of <code class="docutils literal notranslate"><span class="pre">Int32</span></code> type.</p>
<p>If multiband rasters are used in the data raster stack, the algorithm will always
perform the analysis on the first band of the rasters - use GDAL to use other bands
in the analysis.
The output NoData value can be set manually.</p>
<figure class="align-center" id="id125">
<img alt="../../../../_images/equaltofrequency.png" src="../../../../_images/equaltofrequency.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.26 </span><span class="caption-text">For each cell in the output raster, the value represents the number of times
that the corresponding cells in the list of rasters are the same as the value raster.
<code class="docutils literal notranslate"><span class="pre">NoData</span></code> cells (grey) are taken into account.</span><a class="headerlink" href="#id125" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisgreaterthanfrequency"><span class="std std-ref">Greater than frequency</span></a>, <a class="reference internal" href="#qgislessthanfrequency"><span class="std std-ref">Less than frequency</span></a></p>
</div>
<section id="id18">
<h3>Parameters<a class="headerlink" href="#id18" title="Link to this heading"></a></h3>
<section id="id19">
<h4>Basic parameters<a class="headerlink" href="#id19" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input value raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VALUE_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The input value layer serves as reference layer for the sample layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Value raster band</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VALUE_RASTER_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>Select the band you want to use as sample</p></td>
</tr>
<tr class="row-even"><td><p><strong>Input raster layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTERS</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>Raster layers to evaluate.
If multiband rasters are used in the data raster stack, the algorithm
will always perform the analysis on the first band of the rasters</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>If unchecked, any NoData cells in the value raster or the data layer stack
will result in a NoData cell in the output raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id20">
<h4>Advanced parameters<a class="headerlink" href="#id20" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NO_DATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id21">
<h3>Outputs<a class="headerlink" href="#id21" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Count of cells with equal value occurrences</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FOUND_LOCATIONS_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Mean frequency at valid cell locations</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MEAN_FREQUENCY_PER_LOCATION</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Count of value occurrences</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OCCURRENCE_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id22">
<h3>Python code<a class="headerlink" href="#id22" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:equaltofrequency</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="fuzzify-raster-gaussian-membership">
<span id="qgisfuzzifyrastergaussianmembership"></span><h2><a class="toc-backref" href="#id137" role="doc-backlink"><span class="section-number">28.1.15.6. </span>Fuzzify raster (gaussian membership)</a><a class="headerlink" href="#fuzzify-raster-gaussian-membership" title="Link to this heading"></a></h2>
<p>Transforms an input raster to a fuzzified raster by assigning a
membership value to each pixel, using a Gaussian membership function.
Membership values range from 0 to 1.
In the fuzzified raster, a value of 0 implies no membership of the
defined fuzzy set, whereas a value of 1 means full membership.
The gaussian membership function is defined as <a class="reference internal" href="../../../../_images/fuzzy_gaussian_formula.png"><img alt="gaussian_formula" src="../../../../_images/fuzzy_gaussian_formula.png" style="height: 1.5em;" /></a>,
where <em>f1</em> is the spread and <em>f2</em> the midpoint.</p>
<figure class="align-center" id="id126">
<img alt="../../../../_images/gaussianimage.png" src="../../../../_images/gaussianimage.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.27 </span><span class="caption-text">Fuzzify raster example. Input raster source: Land Tirol -
data.tirol.gv.at.</span><a class="headerlink" href="#id126" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfuzzifyrasterlargemembership"><span class="std std-ref">Fuzzify raster (large membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterlinearmembership"><span class="std std-ref">Fuzzify raster (linear membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasternearmembership"><span class="std std-ref">Fuzzify raster (near membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterpowermembership"><span class="std std-ref">Fuzzify raster (power membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrastersmallmembership"><span class="std std-ref">Fuzzify raster (small membership)</span></a></p>
</div>
<section id="id23">
<h3>Parameters<a class="headerlink" href="#id23" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band Number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that
you want to fuzzify.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Function midpoint</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYMIDPOINT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 10</p>
</td>
<td><p>Midpoint of the gaussian function</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Function spread</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYSPREAD</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.01</p>
</td>
<td><p>Spread of the gaussian function</p></td>
</tr>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id24">
<h3>Outputs<a class="headerlink" href="#id24" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id25">
<h3>Python code<a class="headerlink" href="#id25" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:fuzzifyrastergaussianmembership</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="fuzzify-raster-large-membership">
<span id="qgisfuzzifyrasterlargemembership"></span><h2><a class="toc-backref" href="#id138" role="doc-backlink"><span class="section-number">28.1.15.7. </span>Fuzzify raster (large membership)</a><a class="headerlink" href="#fuzzify-raster-large-membership" title="Link to this heading"></a></h2>
<p>Transforms an input raster to a fuzzified raster by assigning a
membership value to each pixel, using a Large membership function.
Membership values range from 0 to 1.
In the fuzzified raster, a value of 0 implies no membership of the
defined fuzzy set, whereas a value of 1 means full membership.
The large membership function is defined as <a class="reference internal" href="../../../../_images/fuzzy_large_formula.png"><img alt="fuzzy_large_formula" src="../../../../_images/fuzzy_large_formula.png" style="height: 3.2em;" /></a>,
where <em>f1</em> is the spread and <em>f2</em> the midpoint.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfuzzifyrastergaussianmembership"><span class="std std-ref">Fuzzify raster (gaussian membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterlinearmembership"><span class="std std-ref">Fuzzify raster (linear membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasternearmembership"><span class="std std-ref">Fuzzify raster (near membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterpowermembership"><span class="std std-ref">Fuzzify raster (power membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrastersmallmembership"><span class="std std-ref">Fuzzify raster (small membership)</span></a></p>
</div>
<section id="id26">
<h3>Parameters<a class="headerlink" href="#id26" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band Number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that you want to
fuzzify.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Function midpoint</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYMIDPOINT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 50</p>
</td>
<td><p>Midpoint of the large function</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Function spread</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYSPREAD</span></code></p></td>
<td><p>[number]</p>
<p>Default: 5</p>
</td>
<td><p>Spread of the large function</p></td>
</tr>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id27">
<h3>Outputs<a class="headerlink" href="#id27" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id28">
<h3>Python code<a class="headerlink" href="#id28" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:fuzzifyrasterlargemembership</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="fuzzify-raster-linear-membership">
<span id="qgisfuzzifyrasterlinearmembership"></span><h2><a class="toc-backref" href="#id139" role="doc-backlink"><span class="section-number">28.1.15.8. </span>Fuzzify raster (linear membership)</a><a class="headerlink" href="#fuzzify-raster-linear-membership" title="Link to this heading"></a></h2>
<p>Transforms an input raster to a fuzzified raster by assigning a
membership value to each pixel, using a Linear membership function.
Membership values range from 0 to 1. In the fuzzified raster, a value
of 0 implies no membership of the defined fuzzy set, whereas a value
of 1 means full membership.
The linear function is defined as <a class="reference internal" href="../../../../_images/fuzzy_linear_formula.png"><img alt="fuzzy_linear_formula" src="../../../../_images/fuzzy_linear_formula.png" style="height: 3.8em;" /></a>, where <em>a</em>
is the low bound and <em>b</em> the high bound. This equation assigns
membership values using a linear transformation for pixel values
between the low and high bounds.
Pixels values smaller than the low bound are given 0 membership
whereas pixel values greater than the high bound are given 1
membership.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfuzzifyrastergaussianmembership"><span class="std std-ref">Fuzzify raster (gaussian membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterlargemembership"><span class="std std-ref">Fuzzify raster (large membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasternearmembership"><span class="std std-ref">Fuzzify raster (near membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterpowermembership"><span class="std std-ref">Fuzzify raster (power membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrastersmallmembership"><span class="std std-ref">Fuzzify raster (small membership)</span></a></p>
</div>
<section id="id29">
<h3>Parameters<a class="headerlink" href="#id29" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band Number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that you want to
fuzzify.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Low fuzzy membership bound</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYLOWBOUND</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0</p>
</td>
<td><p>Low bound of the linear function</p></td>
</tr>
<tr class="row-odd"><td><p><strong>High fuzzy membership bound</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYHIGHBOUND</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1</p>
</td>
<td><p>High bound of the linear function</p></td>
</tr>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id30">
<h3>Outputs<a class="headerlink" href="#id30" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id31">
<h3>Python code<a class="headerlink" href="#id31" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:fuzzifyrasterlinearmembership</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="fuzzify-raster-near-membership">
<span id="qgisfuzzifyrasternearmembership"></span><h2><a class="toc-backref" href="#id140" role="doc-backlink"><span class="section-number">28.1.15.9. </span>Fuzzify raster (near membership)</a><a class="headerlink" href="#fuzzify-raster-near-membership" title="Link to this heading"></a></h2>
<p>Transforms an input raster to a fuzzified raster by assigning a
membership value to each pixel, using a Near membership function.
Membership values range from 0 to 1.
In the fuzzified raster, a value of 0 implies no membership of the
defined fuzzy set, whereas a value of 1 means full membership.
The near membership function is defined as <a class="reference internal" href="../../../../_images/fuzzy_near_formula.png"><img alt="near_formula" src="../../../../_images/fuzzy_near_formula.png" style="height: 2.5em;" /></a>, where
<em>f1</em> is the spread and <em>f2</em> the midpoint.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfuzzifyrastergaussianmembership"><span class="std std-ref">Fuzzify raster (gaussian membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterlargemembership"><span class="std std-ref">Fuzzify raster (large membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterlinearmembership"><span class="std std-ref">Fuzzify raster (linear membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterpowermembership"><span class="std std-ref">Fuzzify raster (power membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrastersmallmembership"><span class="std std-ref">Fuzzify raster (small membership)</span></a></p>
</div>
<section id="id32">
<h3>Parameters<a class="headerlink" href="#id32" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band Number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that you want to
fuzzify.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Function midpoint</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYMIDPOINT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 50</p>
</td>
<td><p>Midpoint of the near function</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Function spread</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYSPREAD</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.01</p>
</td>
<td><p>Spread of the near function</p></td>
</tr>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id33">
<h3>Outputs<a class="headerlink" href="#id33" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id34">
<h3>Python code<a class="headerlink" href="#id34" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:fuzzifyrasternearmembership</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="fuzzify-raster-power-membership">
<span id="qgisfuzzifyrasterpowermembership"></span><h2><a class="toc-backref" href="#id141" role="doc-backlink"><span class="section-number">28.1.15.10. </span>Fuzzify raster (power membership)</a><a class="headerlink" href="#fuzzify-raster-power-membership" title="Link to this heading"></a></h2>
<p>Transforms an input raster to a fuzzified raster by assigning a
membership value to each pixel, using a Power membership function.
Membership values range from 0 to 1.
In the fuzzified raster, a value of 0 implies no membership of the
defined fuzzy set, whereas a value of 1 means full membership.
The power function is defined as <a class="reference internal" href="../../../../_images/fuzzy_power_formula.png"><img alt="power_formula" src="../../../../_images/fuzzy_power_formula.png" style="height: 4.4em;" /></a>, where <em>a</em> is the
low bound, <em>b</em> is the high bound, and <em>f1</em> the exponent.
This equation assigns membership values using the power transformation
for pixel values between the low and high bounds.
Pixels values smaller than the low bound are given 0 membership
whereas pixel values greater than the high bound are given 1
membership.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfuzzifyrastergaussianmembership"><span class="std std-ref">Fuzzify raster (gaussian membership)</span></a>, <a class="reference internal" href="#qgisfuzzifyrasterlargemembership"><span class="std std-ref">Fuzzify raster (large membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterlinearmembership"><span class="std std-ref">Fuzzify raster (linear membership)</span></a>, <a class="reference internal" href="#qgisfuzzifyrasternearmembership"><span class="std std-ref">Fuzzify raster (near membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrastersmallmembership"><span class="std std-ref">Fuzzify raster (small membership)</span></a></p>
</div>
<section id="id35">
<h3>Parameters<a class="headerlink" href="#id35" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band Number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that you want to
fuzzify.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Low fuzzy membership bound</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYLOWBOUND</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0</p>
</td>
<td><p>Low bound of the power function</p></td>
</tr>
<tr class="row-odd"><td><p><strong>High fuzzy membership bound</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYHIGHBOUND</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1</p>
</td>
<td><p>High bound of the power function</p></td>
</tr>
<tr class="row-even"><td><p><strong>High fuzzy membership bound</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYEXPONENT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 2</p>
</td>
<td><p>Exponent of the power function</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id36">
<h3>Outputs<a class="headerlink" href="#id36" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id37">
<h3>Python code<a class="headerlink" href="#id37" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:fuzzifyrasterpowermembership</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="fuzzify-raster-small-membership">
<span id="qgisfuzzifyrastersmallmembership"></span><h2><a class="toc-backref" href="#id142" role="doc-backlink"><span class="section-number">28.1.15.11. </span>Fuzzify raster (small membership)</a><a class="headerlink" href="#fuzzify-raster-small-membership" title="Link to this heading"></a></h2>
<p>Transforms an input raster to a fuzzified raster by assigning a
membership value to each pixel, using a Small membership function.
Membership values range from 0 to 1.
In the fuzzified raster, a value of 0 implies no membership of the
defined fuzzy set, whereas a value of 1 means full membership.
The small membership function is defined as <a class="reference internal" href="../../../../_images/fuzzy_small_formula.png"><img alt="small_formula" src="../../../../_images/fuzzy_small_formula.png" style="height: 3.2em;" /></a>, where
<em>f1</em> is the spread and <em>f2</em> the midpoint.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfuzzifyrastergaussianmembership"><span class="std std-ref">Fuzzify raster (gaussian membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterlargemembership"><span class="std std-ref">Fuzzify raster (large membership)</span></a>
<a class="reference internal" href="#qgisfuzzifyrasterlinearmembership"><span class="std std-ref">Fuzzify raster (linear membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasternearmembership"><span class="std std-ref">Fuzzify raster (near membership)</span></a>,
<a class="reference internal" href="#qgisfuzzifyrasterpowermembership"><span class="std std-ref">Fuzzify raster (power membership)</span></a></p>
</div>
<section id="id38">
<h3>Parameters<a class="headerlink" href="#id38" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band Number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that you want to
fuzzify.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Function midpoint</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYMIDPOINT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 50</p>
</td>
<td><p>Midpoint of the small function</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Function spread</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FUZZYSPREAD</span></code></p></td>
<td><p>[number]</p>
<p>Default: 5</p>
</td>
<td><p>Spread of the small function</p></td>
</tr>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id39">
<h3>Outputs<a class="headerlink" href="#id39" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Fuzzified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id40">
<h3>Python code<a class="headerlink" href="#id40" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:fuzzifyrastersmallmembership</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="greater-than-frequency">
<span id="qgisgreaterthanfrequency"></span><h2><a class="toc-backref" href="#id143" role="doc-backlink"><span class="section-number">28.1.15.12. </span>Greater than frequency</a><a class="headerlink" href="#greater-than-frequency" title="Link to this heading"></a></h2>
<p>Evaluates on a cell-by-cell basis the frequency (number of times) the values
of an input stack of rasters are equal to the value of a value raster.
The output raster extent and resolution is defined by the input raster layer
and is always of <code class="docutils literal notranslate"><span class="pre">Int32</span></code> type.</p>
<p>If multiband rasters are used in the data raster stack, the algorithm will always
perform the analysis on the first band of the rasters - use GDAL to use other bands
in the analysis.
The output NoData value can be set manually.</p>
<figure class="align-center" id="id127">
<img alt="../../../../_images/greaterthanfrequency.png" src="../../../../_images/greaterthanfrequency.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.28 </span><span class="caption-text">For each cell in the output raster, the value represents the number of times
that the corresponding cells in the list of rasters are greater than the value raster.
<code class="docutils literal notranslate"><span class="pre">NoData</span></code> cells (grey) are taken into account.</span><a class="headerlink" href="#id127" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisequaltofrequency"><span class="std std-ref">Equal to frequency</span></a>, <a class="reference internal" href="#qgislessthanfrequency"><span class="std std-ref">Less than frequency</span></a></p>
</div>
<section id="id41">
<h3>Parameters<a class="headerlink" href="#id41" title="Link to this heading"></a></h3>
<section id="id42">
<h4>Basic parameters<a class="headerlink" href="#id42" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input value raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VALUE_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The input value layer serves as reference layer for the sample layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Value raster band</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VALUE_RASTER_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>Select the band you want to use as sample</p></td>
</tr>
<tr class="row-even"><td><p><strong>Input raster layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTERS</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>Raster layers to evaluate.
If multiband rasters are used in the data raster stack, the algorithm
will always perform the analysis on the first band of the rasters</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>If unchecked, any NoData cells in the value raster or the data layer stack
will result in a NoData cell in the output raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id43">
<h4>Advanced parameters<a class="headerlink" href="#id43" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NO_DATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id44">
<h3>Outputs<a class="headerlink" href="#id44" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Count of cells with equal value occurrences</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FOUND_LOCATIONS_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Mean frequency at valid cell locations</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MEAN_FREQUENCY_PER_LOCATION</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Count of value occurrences</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OCCURRENCE_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id45">
<h3>Python code<a class="headerlink" href="#id45" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:greaterthanfrequency</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="highest-position-in-raster-stack">
<span id="qgishighestpositioninrasterstack"></span><h2><a class="toc-backref" href="#id144" role="doc-backlink"><span class="section-number">28.1.15.13. </span>Highest position in raster stack</a><a class="headerlink" href="#highest-position-in-raster-stack" title="Link to this heading"></a></h2>
<p>Evaluates on a cell-by-cell basis the position of the raster with the highest value
in a stack of rasters. Position counts start with 1 and range to the total number
of input rasters. The order of the input rasters is relevant for the algorithm.
If multiple rasters feature the highest value, the first raster will be used for
the position value.</p>
<p>If multiband rasters are used in the data raster stack, the algorithm will
always perform the analysis on the first band of the rasters - use GDAL to use
other bands in the analysis.
Any NoData cells in the raster layer stack will result in a NoData cell
in the output raster unless the “ignore NoData” parameter is checked.
The output NoData value can be set manually. The output rasters extent and
resolution is defined by a reference raster layer and is always of <code class="docutils literal notranslate"><span class="pre">Int32</span></code> type.</p>
<figure class="align-center">
<img alt="../../../../_images/highestposition.png" src="../../../../_images/highestposition.png" />
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgislowestpositioninrasterstack"><span class="std std-ref">Lowest position in raster stack</span></a></p>
</div>
<section id="id46">
<h3>Parameters<a class="headerlink" href="#id46" title="Link to this heading"></a></h3>
<section id="id47">
<h4>Basic parameters<a class="headerlink" href="#id47" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input raster layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTERS</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>List of raster layers to compare with</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REFERENCE_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer for the output layer creation
(extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-even"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>If unchecked, any NoData cells in the data layer stack
will result in a NoData cell in the output raster</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster containing the result.
One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id48">
<h4>Advanced parameters<a class="headerlink" href="#id48" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NODATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id49">
<h3>Outputs<a class="headerlink" href="#id49" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id50">
<h3>Python code<a class="headerlink" href="#id50" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:highestpositioninrasterstack</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="less-than-frequency">
<span id="qgislessthanfrequency"></span><h2><a class="toc-backref" href="#id145" role="doc-backlink"><span class="section-number">28.1.15.14. </span>Less than frequency</a><a class="headerlink" href="#less-than-frequency" title="Link to this heading"></a></h2>
<p>Evaluates on a cell-by-cell basis the frequency (number of times) the values
of an input stack of rasters are less than the value of a value raster.
The output raster extent and resolution is defined by the input raster layer
and is always of <code class="docutils literal notranslate"><span class="pre">Int32</span></code> type.</p>
<p>If multiband rasters are used in the data raster stack, the algorithm will always
perform the analysis on the first band of the rasters - use GDAL to use other bands
in the analysis.
The output NoData value can be set manually.</p>
<figure class="align-center" id="id128">
<img alt="../../../../_images/lessthanfrequency.png" src="../../../../_images/lessthanfrequency.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.29 </span><span class="caption-text">For each cell in the output raster, the value represents the number of times
that the corresponding cells in the list of rasters are less than the value raster.
<code class="docutils literal notranslate"><span class="pre">NoData</span></code> cells (grey) are taken into account.</span><a class="headerlink" href="#id128" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisequaltofrequency"><span class="std std-ref">Equal to frequency</span></a>, <a class="reference internal" href="#qgisgreaterthanfrequency"><span class="std std-ref">Greater than frequency</span></a></p>
</div>
<section id="id51">
<h3>Parameters<a class="headerlink" href="#id51" title="Link to this heading"></a></h3>
<section id="id52">
<h4>Basic parameters<a class="headerlink" href="#id52" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input value raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VALUE_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The input value layer serves as reference layer for the sample layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Value raster band</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VALUE_RASTER_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>Select the band you want to use as sample</p></td>
</tr>
<tr class="row-even"><td><p><strong>Input raster layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTERS</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>Raster layers to evaluate.
If multiband rasters are used in the data raster stack, the algorithm
will always perform the analysis on the first band of the rasters</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>If unchecked, any NoData cells in the value raster or the data layer stack
will result in a NoData cell in the output raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id53">
<h4>Advanced parameters<a class="headerlink" href="#id53" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NO_DATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id54">
<h3>Outputs<a class="headerlink" href="#id54" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Count of cells with equal value occurrences</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FOUND_LOCATIONS_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Mean frequency at valid cell locations</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MEAN_FREQUENCY_PER_LOCATION</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Count of value occurrences</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OCCURRENCE_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id55">
<h3>Python code<a class="headerlink" href="#id55" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:lessthanfrequency</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="lowest-position-in-raster-stack">
<span id="qgislowestpositioninrasterstack"></span><h2><a class="toc-backref" href="#id146" role="doc-backlink"><span class="section-number">28.1.15.15. </span>Lowest position in raster stack</a><a class="headerlink" href="#lowest-position-in-raster-stack" title="Link to this heading"></a></h2>
<p>Evaluates on a cell-by-cell basis the position of the raster with the lowest value
in a stack of rasters. Position counts start with 1 and range to the total number
of input rasters. The order of the input rasters is relevant for the algorithm.
If multiple rasters feature the lowest value, the first raster will be used for
the position value.</p>
<p>If multiband rasters are used in the data raster stack, the algorithm will
always perform the analysis on the first band of the rasters - use GDAL to use
other bands in the analysis.
Any NoData cells in the raster layer stack will result in a NoData cell
in the output raster unless the “ignore NoData” parameter is checked.
The output NoData value can be set manually. The output rasters extent and
resolution is defined by a reference raster layer and is always of <code class="docutils literal notranslate"><span class="pre">Int32</span></code> type.</p>
<figure class="align-center">
<img alt="../../../../_images/lowestposition.png" src="../../../../_images/lowestposition.png" />
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgishighestpositioninrasterstack"><span class="std std-ref">Highest position in raster stack</span></a></p>
</div>
<section id="id56">
<h3>Parameters<a class="headerlink" href="#id56" title="Link to this heading"></a></h3>
<section id="id57">
<h4>Basic parameters<a class="headerlink" href="#id57" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input raster layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTERS</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>List of raster layers to compare with</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REFERENCE_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer for the output layer creation
(extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-even"><td><p><strong>Ignore NoData values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_NODATA</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>If unchecked, any NoData cells in the data layer stack
will result in a NoData cell in the output raster</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster containing the result.
One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id58">
<h4>Advanced parameters<a class="headerlink" href="#id58" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_NODATA_VALUE</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id59">
<h3>Outputs<a class="headerlink" href="#id59" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id60">
<h3>Python code<a class="headerlink" href="#id60" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:lowestpositioninrasterstack</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-boolean-and">
<span id="qgisrasterbooleanand"></span><h2><a class="toc-backref" href="#id147" role="doc-backlink"><span class="section-number">28.1.15.16. </span>Raster boolean AND</a><a class="headerlink" href="#raster-boolean-and" title="Link to this heading"></a></h2>
<p>Calculates the boolean <code class="docutils literal notranslate"><span class="pre">AND</span></code> for a set of input rasters.
If all of the input rasters have a non-zero value for a pixel, that
pixel will be set to <code class="docutils literal notranslate"><span class="pre">1</span></code> in the output raster.
If any of the input rasters have <code class="docutils literal notranslate"><span class="pre">0</span></code> values for the pixel it will
be set to <code class="docutils literal notranslate"><span class="pre">0</span></code> in the output raster.</p>
<p>The reference layer parameter specifies an existing raster layer to
use as a reference when creating the output raster.
The output raster will have the same extent, CRS, and pixel dimensions
as this layer.</p>
<p>By default, a NoData pixel in ANY of the input layers will result in a
NoData pixel in the output raster.
If the <span class="guilabel">Treat NoData values as false</span> option is checked,
then NoData inputs will be treated the same as a <code class="docutils literal notranslate"><span class="pre">0</span></code> input value.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisrasterbooleanor"><span class="std std-ref">Raster boolean OR</span></a></p>
</div>
<section id="id61">
<h3>Parameters<a class="headerlink" href="#id61" title="Link to this heading"></a></h3>
<section id="id62">
<h4>Basic parameters<a class="headerlink" href="#id62" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>List of input raster layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REF_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer to create the output layer
from (extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-even"><td><p><strong>Treat NoData values as false</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_AS_FALSE</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Treat NoData values in the input files as 0 when performing the
operation</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster containing the result.
One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id63">
<h4>Advanced parameters<a class="headerlink" href="#id63" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NO_DATA</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output data type</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DATA_TYPE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 5</p>
</td>
<td><p>Output raster data type. Options:</p>
<ul class="simple">
<li><p>0 — Byte        (Eight bit unsigned integer (quint8))</p></li>
<li><p>1 — Int16       (Sixteen bit signed integer (qint16))</p></li>
<li><p>2 — UInt16      (Sixteen bit unsigned integer (quint16))</p></li>
<li><p>3 — Int32       (Thirty two bit signed integer (qint32))</p></li>
<li><p>4 — UInt32      (Thirty two bit unsigned integer (quint32))</p></li>
<li><p>5 — Float32     (Thirty two bit floating point (float))</p></li>
<li><p>6 — Float64     (Sixty four bit floating point (double))</p></li>
<li><p>7 — CInt16      (Complex Int16)</p></li>
<li><p>8 — CInt32      (Complex Int32)</p></li>
<li><p>9 — CFloat32    (Complex Float32)</p></li>
<li><p>10 — CFloat64   (Complex Float64)</p></li>
<li><p>11 — Int8       (Eight bit signed integer (qint8))</p></li>
</ul>
<p>Available options depend on the GDAL version built with QGIS
(see <span class="menuselection">Help ► About</span> menu)</p>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id64">
<h3>Outputs<a class="headerlink" href="#id64" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>NoData pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of NoData pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>True pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TRUE_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of True pixels (value = 1) in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>False pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FALSE_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of False pixels (value = 0) in the output raster
layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id65">
<h3>Python code<a class="headerlink" href="#id65" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rasterbooleanand</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-boolean-or">
<span id="qgisrasterbooleanor"></span><h2><a class="toc-backref" href="#id148" role="doc-backlink"><span class="section-number">28.1.15.17. </span>Raster boolean OR</a><a class="headerlink" href="#raster-boolean-or" title="Link to this heading"></a></h2>
<p>Calculates the boolean <code class="docutils literal notranslate"><span class="pre">OR</span></code> for a set of input rasters.
If all of the input rasters have a zero value for a pixel, that
pixel will be set to <code class="docutils literal notranslate"><span class="pre">0</span></code> in the output raster.
If any of the input rasters have <code class="docutils literal notranslate"><span class="pre">1</span></code> values for the pixel it will
be set to <code class="docutils literal notranslate"><span class="pre">1</span></code> in the output raster.</p>
<p>The reference layer parameter specifies an existing raster layer to
use as a reference when creating the output raster.
The output raster will have the same extent, CRS, and pixel dimensions
as this layer.</p>
<p>By default, a NoData pixel in ANY of the input layers will result in a
NoData pixel in the output raster.
If the <span class="guilabel">Treat NoData values as false</span> option is checked,
then NoData inputs will be treated the same as a <code class="docutils literal notranslate"><span class="pre">0</span></code> input value.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisrasterbooleanand"><span class="std std-ref">Raster boolean AND</span></a></p>
</div>
<section id="id66">
<h3>Parameters<a class="headerlink" href="#id66" title="Link to this heading"></a></h3>
<section id="id67">
<h4>Basic parameters<a class="headerlink" href="#id67" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>List of input raster layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REF_LAYER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The reference layer to create the output layer
from (extent, CRS, pixel dimensions)</p></td>
</tr>
<tr class="row-even"><td><p><strong>Treat NoData values as false</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_AS_FALSE</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Treat NoData values in the input files as 0 when performing the
operation</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster containing the result.
One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id68">
<h4>Advanced parameters<a class="headerlink" href="#id68" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NO_DATA</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to use for NoData in the output layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output data type</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DATA_TYPE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 5</p>
</td>
<td><p>Output raster data type. Options:</p>
<ul class="simple">
<li><p>0 — Byte        (Eight bit unsigned integer (quint8))</p></li>
<li><p>1 — Int16       (Sixteen bit signed integer (qint16))</p></li>
<li><p>2 — UInt16      (Sixteen bit unsigned integer (quint16))</p></li>
<li><p>3 — Int32       (Thirty two bit signed integer (qint32))</p></li>
<li><p>4 — UInt32      (Thirty two bit unsigned integer (quint32))</p></li>
<li><p>5 — Float32     (Thirty two bit floating point (float))</p></li>
<li><p>6 — Float64     (Sixty four bit floating point (double))</p></li>
<li><p>7 — CInt16      (Complex Int16)</p></li>
<li><p>8 — CInt32      (Complex Int32)</p></li>
<li><p>9 — CFloat32    (Complex Float32)</p></li>
<li><p>10 — CFloat64   (Complex Float64)</p></li>
<li><p>11 — Int8       (Eight bit signed integer (qint8))</p></li>
</ul>
<p>Available options depend on the GDAL version built with QGIS
(see <span class="menuselection">Help ► About</span> menu)</p>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id69">
<h3>Outputs<a class="headerlink" href="#id69" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>NoData pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of NoData pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>True pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TRUE_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of True pixels (value = 1) in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>False pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FALSE_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of False pixels (value = 0) in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer containing the result</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id70">
<h3>Python code<a class="headerlink" href="#id70" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rasterbooleanor</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-calculator">
<span id="qgisrastercalc"></span><h2><a class="toc-backref" href="#id149" role="doc-backlink"><span class="section-number">28.1.15.18. </span>Raster calculator</a><a class="headerlink" href="#raster-calculator" title="Link to this heading"></a></h2>
<p>Performs algebraic operations using raster layers.</p>
<p>The resulting layer will have its values computed according to an expression.
The expression can contain numerical values, operators and references
to any of the layers in the current project.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisvirtualrastercalc"><span class="std std-ref">Raster calculator (virtual)</span></a>, <a class="reference internal" href="../gdal/rastermiscellaneous.html#gdalrastercalculator"><span class="std std-ref">Raster calculator</span></a>, <a class="reference internal" href="../../working_with_raster/raster_analysis.html#label-raster-calc"><span class="std std-ref">Raster Calculator</span></a></p>
</div>
<section id="id71">
<h3>Parameters<a class="headerlink" href="#id71" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>List of input raster layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Expression</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXPRESSION</span></code></p></td>
<td><p>[expression]</p></td>
<td><p><a class="reference internal" href="../../working_with_raster/raster_analysis.html#raster-expression"><span class="std std-ref">Raster-based expression</span></a> that will be used to calculate the output raster layer.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output extent</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[extent]</p></td>
<td><p>Specify the spatial extent of the output raster layer.
If the extent is not specified, the minimum extent that covers
all the selected reference layers will be used.</p>
<p>Available methods are:</p>
<ul class="simple">
<li><p>Calculate from layer…: uses extent of a layer loaded in the current project</p></li>
<li><p>Calculate from layout map…: uses extent of a <a class="reference internal" href="../../print_composer/composer_items/composer_map.html#layout-map-item"><span class="std std-ref">layout map item</span></a>
in the active project</p></li>
<li><p>Calculate from bookmark…: uses extent of a saved <a class="reference internal" href="../../map_views/map_view.html#sec-bookmarks"><span class="std std-ref">bookmark</span></a></p></li>
<li><p>Use map canvas extent</p></li>
<li><p>Draw on canvas: click and drag a rectangle delimiting the area to take into account</p></li>
<li><p>Enter the coordinates as <code class="docutils literal notranslate"><span class="pre">xmin,</span> <span class="pre">xmax,</span> <span class="pre">ymin,</span> <span class="pre">ymax</span></code></p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Output cell size (leave empty to set automatically)</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">CELLSIZE</span></code></p></td>
<td><p>[number]</p></td>
<td><p>Cell size of the output raster layer.
If the cell size is not specified, the minimum cell size of
the selected reference layer(s) will be used.
The cell size will be the same for the X and Y axes.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output CRS</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>CRS of the output raster layer.
If the output CRS is not specified, the CRS of the first
reference layer will be used.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Calculated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id72">
<h3>Outputs<a class="headerlink" href="#id72" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Calculated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster file with the calculated values.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id73">
<h3>Python code<a class="headerlink" href="#id73" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rastercalc</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-calculator-virtual">
<span id="qgisvirtualrastercalc"></span><h2><a class="toc-backref" href="#id150" role="doc-backlink"><span class="section-number">28.1.15.19. </span>Raster calculator (virtual)</a><a class="headerlink" href="#raster-calculator-virtual" title="Link to this heading"></a></h2>
<p>Performs algebraic operations using raster layers and generates in-memory result.</p>
<p>The resulting layer will have its values computed according to an expression.
The expression can contain numerical values, operators and references
to any of the layers in the current project.</p>
<p>A virtual raster layer is a raster layer defined by its URI and whose pixels are calculated on-the-fly.
It’s not a new file on disk; the virtual layer is still connected to the rasters used in the calculation
meaning that deleting or moving these rasters would break it.
A <span class="guilabel">Layer name</span> can be provided, otherwise the calculation expression is used as such.
Removing the virtual layer from the project deletes it, and it can be made persistent in file using the layer
<span class="menuselection">Export ► Save as…</span> contextual menu.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisrastercalc"><span class="std std-ref">Raster calculator</span></a>, <a class="reference internal" href="../gdal/rastermiscellaneous.html#gdalrastercalculator"><span class="std std-ref">Raster calculator</span></a>, <a class="reference internal" href="../../working_with_raster/raster_analysis.html#label-raster-calc"><span class="std std-ref">Raster Calculator</span></a></p>
</div>
<section id="id74">
<h3>Parameters<a class="headerlink" href="#id74" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster] [list]</p></td>
<td><p>List of input raster layers</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Expression</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXPRESSION</span></code></p></td>
<td><p>[expression]</p></td>
<td><p><a class="reference internal" href="../../working_with_raster/raster_analysis.html#raster-expression"><span class="std std-ref">Raster-based expression</span></a> that will be used to calculate the output raster layer.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output extent</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[extent]</p></td>
<td><p>Specify the spatial extent of the output raster layer.
If the extent is not specified, the minimum extent that covers
all the selected reference layers will be used.</p>
<p>Available methods are:</p>
<ul class="simple">
<li><p>Calculate from layer…: uses extent of a layer loaded in the current project</p></li>
<li><p>Calculate from layout map…: uses extent of a <a class="reference internal" href="../../print_composer/composer_items/composer_map.html#layout-map-item"><span class="std std-ref">layout map item</span></a>
in the active project</p></li>
<li><p>Calculate from bookmark…: uses extent of a saved <a class="reference internal" href="../../map_views/map_view.html#sec-bookmarks"><span class="std std-ref">bookmark</span></a></p></li>
<li><p>Use map canvas extent</p></li>
<li><p>Draw on canvas: click and drag a rectangle delimiting the area to take into account</p></li>
<li><p>Enter the coordinates as <code class="docutils literal notranslate"><span class="pre">xmin,</span> <span class="pre">xmax,</span> <span class="pre">ymin,</span> <span class="pre">ymax</span></code></p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Output cell size (leave empty to set automatically)</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">CELLSIZE</span></code></p></td>
<td><p>[number]</p></td>
<td><p>Cell size of the output raster layer.
If the cell size is not specified, the minimum cell size of
the selected reference layer(s) will be used.
The cell size will be the same for the X and Y axes.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output CRS</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS</span></code></p></td>
<td><p>[crs]</p></td>
<td><p>CRS of the output raster layer.
If the output CRS is not specified, the CRS of the first
reference layer will be used.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output layer name</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">LAYER_NAME</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The name to assign to the generated layer.
If not set, the text of the calculation expression is used.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id75">
<h3>Outputs<a class="headerlink" href="#id75" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Calculated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output virtual raster layer with the calculated values.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id76">
<h3>Python code<a class="headerlink" href="#id76" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:virtualrastercalc</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-layer-properties">
<span id="qgisrasterlayerproperties"></span><h2><a class="toc-backref" href="#id151" role="doc-backlink"><span class="section-number">28.1.15.20. </span>Raster layer properties</a><a class="headerlink" href="#raster-layer-properties" title="Link to this heading"></a></h2>
<p>Returns basic properties of the given raster layer, including the extent,
size in pixels and dimensions of pixels (in map units), number of bands,
and NoData value.</p>
<p>This algorithm is intended for use as a means of extracting these useful properties
to use as the input values to other algorithms in a model - e.g. to allow to pass
an existing raster’s pixel sizes over to a GDAL raster algorithm.</p>
<section id="id77">
<h3>Parameters<a class="headerlink" href="#id77" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: Not set</p>
</td>
<td><p>Whether to also return properties of a specific band.
If a band is specified, the noData value for the selected band is also returned.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id78">
<h3>Outputs<a class="headerlink" href="#id78" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Number of bands in raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of bands in the raster</p></td>
</tr>
<tr class="row-odd"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The raster layer extent in the CRS</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band has a NoData value set</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HAS_NODATA_VALUE</span></code></p></td>
<td><p>[Boolean]</p></td>
<td><p>Indicates whether the raster layer has a value set for NoData pixels
in the selected band</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_VALUE</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The value (if set) of the NoData pixels in the selected band</p></td>
</tr>
<tr class="row-even"><td><p><strong>Pixel size (height) in map units</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">PIXEL_HEIGHT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>Vertical size in map units of the pixel</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Pixel size (width) in map units</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">PIXEL_WIDTH</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>Horizontal size in map units of the pixel</p></td>
</tr>
<tr class="row-even"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum x-coordinate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">X_MAX</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Minimum x-coordinate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">X_MIN</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum y-coordinate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">Y_MAX</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Minimum y-coordinate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">Y_MIN</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
</tbody>
</table>
</section>
<section id="id79">
<h3>Python code<a class="headerlink" href="#id79" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rasterlayerproperties</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-layer-statistics">
<span id="qgisrasterlayerstatistics"></span><h2><a class="toc-backref" href="#id152" role="doc-backlink"><span class="section-number">28.1.15.21. </span>Raster layer statistics</a><a class="headerlink" href="#raster-layer-statistics" title="Link to this heading"></a></h2>
<p>Calculates basic statistics from the values in a given band of the
raster layer.
The output is loaded in the
<span class="menuselection">Processing ► Results viewer</span> menu.</p>
<section id="id80">
<h3>Parameters<a class="headerlink" href="#id80" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the input layer</p>
</td>
<td><p>If the raster is multiband, choose the band you want to get
statistics for.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Statistics</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_HTML_FILE</span></code></p></td>
<td><p>[html]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output file:</p>
<ul class="simple">
<li><p>Skip Output</p></li>
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id81">
<h3>Outputs<a class="headerlink" href="#id81" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Maximum value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAX</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Mean value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MEAN</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Minimum value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MIN</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Statistics</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_HTML_FILE</span></code></p></td>
<td><p>[html]</p></td>
<td><p>The output file contains the following information:</p>
<ul class="simple">
<li><p>Analyzed file: path of the raster layer</p></li>
<li><p>Minimum value: minimum value of the raster</p></li>
<li><p>Maximum value: maximum value of the raster</p></li>
<li><p>Range: difference between the maximum and minimum values</p></li>
<li><p>Sum: total sum of the values</p></li>
<li><p>Mean value: mean of the values</p></li>
<li><p>Standard deviation: standard deviation of the values</p></li>
<li><p>Sum of the squares: sum of the squared differences of
each observation from the overall mean</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Range</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RANGE</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Standard deviation</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">STD_DEV</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Sum</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SUM</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><strong>Sum of the squares</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SUM_OF_SQUARES</span></code></p></td>
<td><p>[number]</p></td>
<td></td>
</tr>
</tbody>
</table>
</section>
<section id="id82">
<h3>Python code<a class="headerlink" href="#id82" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rasterlayerstatistics</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-layer-unique-values-report">
<span id="qgisrasterlayeruniquevaluesreport"></span><h2><a class="toc-backref" href="#id153" role="doc-backlink"><span class="section-number">28.1.15.22. </span>Raster layer unique values report</a><a class="headerlink" href="#raster-layer-unique-values-report" title="Link to this heading"></a></h2>
<p>Returns the count and area of each unique value in a given raster layer.
The calculation of the area is done in the area unit of the layer’s CRS.</p>
<section id="id83">
<h3>Parameters<a class="headerlink" href="#id83" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the input layer</p>
</td>
<td><p>If the raster is multiband, choose the band you want to get
statistics for.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Unique values report</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_HTML_FILE</span></code></p></td>
<td><p>[file]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output file:</p>
<ul class="simple">
<li><p>Skip Output</p></li>
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Unique values table</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_TABLE</span></code></p></td>
<td><p>[table]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Skip</span> <span class="pre">output]</span></code></p>
</td>
<td><p>Specification of the table for unique values:</p>
<ul class="simple">
<li><p>Skip Output</p></li>
<li><p>Create Temporary Layer (<code class="docutils literal notranslate"><span class="pre">TEMPORARY_OUTPUT</span></code>)</p></li>
<li><p>Save to File…</p></li>
<li><p>Save to Geopackage…</p></li>
<li><p>Save to Database Table…</p></li>
</ul>
<p>The file encoding can also be changed here.</p>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id84">
<h3>Outputs<a class="headerlink" href="#id84" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>NoData pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_PIXEL_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of NoData pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Unique values report</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_HTML_FILE</span></code></p></td>
<td><p>[html]</p></td>
<td><p>The output HTML file contains the following information:</p>
<ul class="simple">
<li><p>Analyzed file: the path of the raster layer</p></li>
<li><p>Extent: xmin, ymin, xmax, ymax coordinates of the extent</p></li>
<li><p>Projection: projection of the layer</p></li>
<li><p>Width in pixels: number of columns and pixel width size</p></li>
<li><p>Height in pixels: number of rows and pixel width size</p></li>
<li><p>Total pixel count: count of all the pixels</p></li>
<li><p>NoData pixel count: count of pixels with NoData value</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Unique values table</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_TABLE</span></code></p></td>
<td><p>[table]</p></td>
<td><p>A table with three columns:</p>
<ul class="simple">
<li><p><em>value</em>: pixel value</p></li>
<li><p><em>count</em>: count of pixels with this value</p></li>
<li><p><em>m2</em> or <em>deg2</em> or <em>ft2</em> or … : total area of pixels with this value.
The column name depends on the area unit of the layer’s CRS
and the calculation is done in that unit.</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id85">
<h3>Python code<a class="headerlink" href="#id85" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rasterlayeruniquevaluesreport</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-layer-zonal-statistics">
<span id="qgisrasterlayerzonalstats"></span><h2><a class="toc-backref" href="#id154" role="doc-backlink"><span class="section-number">28.1.15.23. </span>Raster layer zonal statistics</a><a class="headerlink" href="#raster-layer-zonal-statistics" title="Link to this heading"></a></h2>
<p>Calculates statistics for a raster layer’s values, categorized by
zones defined in another raster layer.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgiszonalstatisticsfb"><span class="std std-ref">Zonal statistics</span></a></p>
</div>
<section id="id86">
<h3>Parameters<a class="headerlink" href="#id86" title="Link to this heading"></a></h3>
<section id="id87">
<h4>Basic parameters<a class="headerlink" href="#id87" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband choose the band for which you want
to calculate the statistics.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Zones layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ZONES</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Raster layer defining zones.
Zones are given by contiguous pixels having the same pixel
value.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Zones band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ZONES_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that defines
the zones</p></td>
</tr>
<tr class="row-even"><td><p><strong>Statistics</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_TABLE</span></code></p></td>
<td><p>[table]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specification of the output report. One of:</p>
<ul class="simple">
<li><p>Create Temporary Layer (<code class="docutils literal notranslate"><span class="pre">TEMPORARY_OUTPUT</span></code>)</p></li>
<li><p>Save to File…</p></li>
<li><p>Save to Geopackage…</p></li>
<li><p>Save to Database Table…</p></li>
</ul>
<p>The file encoding can also be changed here.</p>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id88">
<h4>Advanced parameters<a class="headerlink" href="#id88" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Reference layer</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">REF_LAYER</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Raster layer used to calculate the centroids that will be
used as reference when determining the zones in the output
layer. One of:</p>
<ul class="simple">
<li><p>0 — Input layer: zones are determined by sampling the zone raster
layer value at the centroid of each pixel from the source raster layer</p></li>
<li><p>1 — Zones layer: the input raster layer will be sampled at the centroid
of each pixel from the zones raster layer</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id89">
<h3>Outputs<a class="headerlink" href="#id89" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>CRS authority identifier</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CRS_AUTHID</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The coordinate reference system of the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXTENT</span></code></p></td>
<td><p>[string]</p></td>
<td><p>The spatial extent of the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Height in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT_IN_PIXELS</span></code></p></td>
<td><p>[integer]</p></td>
<td><p>The number of rows in the output raster layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>NoData pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_PIXEL_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of NoData pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Statistics</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_TABLE</span></code></p></td>
<td><p>[table]</p></td>
<td><p>The output layer contains the following information
<strong>for each zone</strong>:</p>
<ul class="simple">
<li><p>Area: the area in square raster units in the zone;</p></li>
<li><p>Sum: the total sum of the pixel values in the zone;</p></li>
<li><p>Count: the number of pixels in the zone;</p></li>
<li><p>Min: the minimum pixel value in the zone;</p></li>
<li><p>Max: the maximum pixel value in the zone;</p></li>
<li><p>Mean: the mean of the pixel values in the zone;</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Total pixel count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOTAL_PIXEL_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The count of pixels in the output raster layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Width in pixels</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH_IN_PIXELS</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of columns in the output raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id90">
<h3>Python code<a class="headerlink" href="#id90" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rasterlayerzonalstats</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="raster-surface-volume">
<span id="qgisrastersurfacevolume"></span><h2><a class="toc-backref" href="#id155" role="doc-backlink"><span class="section-number">28.1.15.24. </span>Raster surface volume</a><a class="headerlink" href="#raster-surface-volume" title="Link to this heading"></a></h2>
<p>Calculates the volume under a raster surface relative to a given base
level. This is mainly useful for Digital Elevation Models (DEM).</p>
<section id="id91">
<h3>Parameters<a class="headerlink" href="#id91" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>INPUT layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster, representing a surface</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band that shall define
the surface.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Base level</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">LEVEL</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.0</p>
</td>
<td><p>Define a base or reference value.
This base is used in the volume calculation according to the
<code class="docutils literal notranslate"><span class="pre">Method</span></code> parameter (see below).</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Method</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Define the method for the volume calculation given by the
difference between the raster pixel value and the
<code class="docutils literal notranslate"><span class="pre">Base</span> <span class="pre">level</span></code>.
Options:</p>
<ul class="simple">
<li><p>0 — Count Only Above Base Level: only pixels above the base
level will add to the volume.</p></li>
<li><p>1 — Count Only Below Base Level: only pixels below the base
level will add to the volume.</p></li>
<li><p>2 — Subtract Volumes Below Base level: pixels above the
base level will add to the volume, pixels below the base
level will subtract from the volume.</p></li>
<li><p>3 — Add Volumes Below Base level: Add the volume
regardless whether the pixel is above or below the base
level.
This is equivalent to sum the absolute values of the
difference between the pixel value and the base level.</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Surface volume report</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_HTML_FILE</span></code></p></td>
<td><p>[html]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output HTML report. One of:</p>
<ul class="simple">
<li><p>Skip Output</p></li>
<li><p>Create Temporary Layer (<code class="docutils literal notranslate"><span class="pre">TEMPORARY_OUTPUT</span></code>)</p></li>
<li><p>Save to File…</p></li>
<li><p>Save to Geopackage…</p></li>
<li><p>Save to Database Table…</p></li>
</ul>
<p>The file encoding can also be changed here.</p>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Surface volume table</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_TABLE</span></code></p></td>
<td><p>[table]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Skip</span> <span class="pre">output]</span></code></p>
</td>
<td><p>Specification of the output table. One of:</p>
<ul class="simple">
<li><p>Skip Output</p></li>
<li><p>Create Temporary Layer (<code class="docutils literal notranslate"><span class="pre">TEMPORARY_OUTPUT</span></code>)</p></li>
<li><p>Save to File…</p></li>
<li><p>Save to Geopackage…</p></li>
<li><p>Save to Database Table…</p></li>
</ul>
<p>The file encoding can also be changed here.</p>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id92">
<h3>Outputs<a class="headerlink" href="#id92" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Volume</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VOLUME</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The calculated volume</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Area</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">AREA</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The area in square map units</p></td>
</tr>
<tr class="row-even"><td><p><strong>Pixel_count</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">PIXEL_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The total number of pixels that have been analyzed</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Surface volume report</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_HTML_FILE</span></code></p></td>
<td><p>[html]</p></td>
<td><p>The output report (containing volume, area and
pixel count) in HTML format</p></td>
</tr>
<tr class="row-even"><td><p><strong>Surface volume table</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_TABLE</span></code></p></td>
<td><p>[table]</p></td>
<td><p>The output table (containing volume, area and
pixel count)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id93">
<h3>Python code<a class="headerlink" href="#id93" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rastersurfacevolume</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="reclassify-by-layer">
<span id="qgisreclassifybylayer"></span><h2><a class="toc-backref" href="#id156" role="doc-backlink"><span class="section-number">28.1.15.25. </span>Reclassify by layer</a><a class="headerlink" href="#reclassify-by-layer" title="Link to this heading"></a></h2>
<p>Reclassifies a raster band by assigning new class values based on the
ranges specified in a vector table.</p>
<section id="id94">
<h3>Parameters<a class="headerlink" href="#id94" title="Link to this heading"></a></h3>
<section id="id95">
<h4>Basic parameters<a class="headerlink" href="#id95" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Raster layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Raster layer to reclassify</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RASTER_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the raster layer</p>
</td>
<td><p>If the raster is multiband, choose the band you want to
reclassify.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Layer containing class breaks</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_TABLE</span></code></p></td>
<td><p>[vector: any]</p></td>
<td><p>Vector layer containing the values to use for classification.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Minimum class value field</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MIN_FIELD</span></code></p></td>
<td><p>[tablefield: numeric]</p></td>
<td><p>Field with the minimum value of the range for the class.
Use <code class="docutils literal notranslate"><span class="pre">-inf</span></code> to capture the lowest possible value.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Maximum class value field</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAX_FIELD</span></code></p></td>
<td><p>[tablefield: numeric]</p></td>
<td><p>Field with the maximum value of the range for the class.
Use <code class="docutils literal notranslate"><span class="pre">inf</span></code> to capture the highest possible value.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output value field</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VALUE_FIELD</span></code></p></td>
<td><p>[tablefield: numeric]</p></td>
<td><p>Field with the value that will be assigned to the pixels that
fall in the class (between the corresponding min and max
values). Use <code class="docutils literal notranslate"><span class="pre">nan</span></code> to set the value of the range to NoData.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Reclassified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id96">
<h4>Advanced parameters<a class="headerlink" href="#id96" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NO_DATA</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to apply to NoData values.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Range boundaries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RANGE_BOUNDARIES</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Defines comparison rules for the classification.
Options:</p>
<ul class="simple">
<li><p>0 — min &lt; value &lt;= max</p></li>
<li><p>1 — min &lt;= value &lt; max</p></li>
<li><p>2 — min &lt;= value &lt;= max</p></li>
<li><p>3 — min &lt; value &lt; max</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Use NoData when no range matches value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_FOR_MISSING</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Applies the NoData value to band values that do not fall in
any class.
If False, the original value is kept.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output data type</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DATA_TYPE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 5</p>
</td>
<td><p>Defines the format of the output raster file.
Options:</p>
<ul class="simple">
<li><p>0 — Byte        (Eight bit unsigned integer (quint8))</p></li>
<li><p>1 — Int16       (Sixteen bit signed integer (qint16))</p></li>
<li><p>2 — UInt16      (Sixteen bit unsigned integer (quint16))</p></li>
<li><p>3 — Int32       (Thirty two bit signed integer (qint32))</p></li>
<li><p>4 — UInt32      (Thirty two bit unsigned integer (quint32))</p></li>
<li><p>5 — Float32     (Thirty two bit floating point (float))</p></li>
<li><p>6 — Float64     (Sixty four bit floating point (double))</p></li>
<li><p>7 — CInt16      (Complex Int16)</p></li>
<li><p>8 — CInt32      (Complex Int32)</p></li>
<li><p>9 — CFloat32    (Complex Float32)</p></li>
<li><p>10 — CFloat64   (Complex Float64)</p></li>
<li><p>11 — Int8       (Eight bit signed integer (qint8))</p></li>
</ul>
<p>Available options depend on the GDAL version built with QGIS
(see <span class="menuselection">Help ► About</span> menu)</p>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id97">
<h3>Outputs<a class="headerlink" href="#id97" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Reclassified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer with reclassified band values</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id98">
<h3>Python code<a class="headerlink" href="#id98" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:reclassifybylayer</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="reclassify-by-table">
<span id="qgisreclassifybytable"></span><h2><a class="toc-backref" href="#id157" role="doc-backlink"><span class="section-number">28.1.15.26. </span>Reclassify by table</a><a class="headerlink" href="#reclassify-by-table" title="Link to this heading"></a></h2>
<p>Reclassifies a raster band by assigning new class values based on the
ranges specified in a fixed table.</p>
<section id="id99">
<h3>Parameters<a class="headerlink" href="#id99" title="Link to this heading"></a></h3>
<section id="id100">
<h4>Basic parameters<a class="headerlink" href="#id100" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Raster layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Raster layer to reclassify</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RASTER_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: 1</p>
</td>
<td><p>Raster band for which you want to recalculate values.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Reclassification table</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TABLE</span></code></p></td>
<td><p>[table]</p></td>
<td><p>A 3-columns table to fill with the values to set the boundaries
of each class (<code class="docutils literal notranslate"><span class="pre">Minimum</span></code> and <code class="docutils literal notranslate"><span class="pre">Maximum</span></code>) and the new
<code class="docutils literal notranslate"><span class="pre">Value</span></code> to assign to the band values that fall in the class.
The value <code class="docutils literal notranslate"><span class="pre">-inf</span></code> can be used as minimum, <code class="docutils literal notranslate"><span class="pre">inf</span></code> as maximum,
and <code class="docutils literal notranslate"><span class="pre">nan</span></code> can be used to set the output value to NoData.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reclassified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster layer.
One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id101">
<h4>Advanced parameters<a class="headerlink" href="#id101" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output NoData value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NO_DATA</span></code></p></td>
<td><p>[number]</p>
<p>Default: -9999.0</p>
</td>
<td><p>Value to apply to NoData values.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Range boundaries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RANGE_BOUNDARIES</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Defines comparison rules for the classification.
Options:</p>
<ul class="simple">
<li><p>0 — min &lt; value &lt;= max</p></li>
<li><p>1 — min &lt;= value &lt; max</p></li>
<li><p>2 — min &lt;= value &lt;= max</p></li>
<li><p>3 — min &lt; value &lt; max</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Use NoData when no range matches value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA_FOR_MISSING</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Applies the NoData value to band values that do not fall in
any class.
If False, the original value is kept.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output data type</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DATA_TYPE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 5</p>
</td>
<td><p>Defines the format of the output raster file.
Options:</p>
<ul class="simple">
<li><p>0 — Byte        (Eight bit unsigned integer (quint8))</p></li>
<li><p>1 — Int16       (Sixteen bit signed integer (qint16))</p></li>
<li><p>2 — UInt16      (Sixteen bit unsigned integer (quint16))</p></li>
<li><p>3 — Int32       (Thirty two bit signed integer (qint32))</p></li>
<li><p>4 — UInt32      (Thirty two bit unsigned integer (quint32))</p></li>
<li><p>5 — Float32     (Thirty two bit floating point (float))</p></li>
<li><p>6 — Float64     (Sixty four bit floating point (double))</p></li>
<li><p>7 — CInt16      (Complex Int16)</p></li>
<li><p>8 — CInt32      (Complex Int32)</p></li>
<li><p>9 — CFloat32    (Complex Float32)</p></li>
<li><p>10 — CFloat64   (Complex Float64)</p></li>
<li><p>11 — Int8       (Eight bit signed integer (qint8))</p></li>
</ul>
<p>Available options depend on the GDAL version built with QGIS
(see <span class="menuselection">Help ► About</span> menu)</p>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id102">
<h3>Outputs<a class="headerlink" href="#id102" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Reclassified raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer with reclassified band values</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id103">
<h3>Python code<a class="headerlink" href="#id103" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:reclassifybytable</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="rescale-raster">
<span id="qgisrescaleraster"></span><h2><a class="toc-backref" href="#id158" role="doc-backlink"><span class="section-number">28.1.15.27. </span>Rescale raster</a><a class="headerlink" href="#rescale-raster" title="Link to this heading"></a></h2>
<p>Rescales raster layer to a new value range, while preserving the shape
(distribution) of the raster’s histogram (pixel values). Input values
are mapped using a linear interpolation from the source raster’s
minimum and maximum pixel values to the destination minimum and miximum
pixel range.</p>
<p>By default the algorithm preserves the original NoData value, but there
is an option to override it.</p>
<figure class="align-center" id="id129">
<img alt="../../../../_images/rescale_raster.png" src="../../../../_images/rescale_raster.png" />
<figcaption>
<p><span class="caption-text">Rescaling values of a raster layer from [0 - 50] to [100 - 1000]</span><a class="headerlink" href="#id129" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id104">
<h3>Parameters<a class="headerlink" href="#id104" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 30.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 30.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Raster layer to use for rescaling</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the input layer</p>
</td>
<td><p>If the raster is multiband, choose a band.</p></td>
</tr>
<tr class="row-even"><td><p><strong>New minimum value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MINIMUM</span></code></p></td>
<td><p>[number]</p>
<p>Default value: 0.0</p>
</td>
<td><p>Minimum pixel value to use in the rescaled layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>New maximum value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAXIMUM</span></code></p></td>
<td><p>[number]</p>
<p>Default value: 255.0</p>
</td>
<td><p>Maximum pixel value to use in the rescaled layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>New NoData value</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA</span></code></p></td>
<td><p>[number]</p>
<p>Default value: Not set</p>
</td>
<td><p>Value to assign to the NoData pixels.
If unset, original NoData values are preserved.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Rescaled</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output raster layer.
One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id105">
<h3>Outputs<a class="headerlink" href="#id105" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Rescaled</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Output raster layer with rescaled band values</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id106">
<h3>Python code<a class="headerlink" href="#id106" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rescaleraster</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="round-raster">
<span id="qgisroundrastervalues"></span><h2><a class="toc-backref" href="#id159" role="doc-backlink"><span class="section-number">28.1.15.28. </span>Round raster</a><a class="headerlink" href="#round-raster" title="Link to this heading"></a></h2>
<p>Rounds the cell values of a raster dataset according to the specified number of decimals.</p>
<p>Alternatively, a negative number of decimal places may be used to round values
to powers of a base n. For example, with a Base value n of 10 and Decimal places
of -1, the algorithm rounds cell values to multiples of 10,
-2 rounds to multiples of 100, and so on.
Arbitrary base values may be chosen, the algorithm applies the same multiplicative
principle. Rounding cell values to multiples of a base n may be used to generalize
raster layers.</p>
<p>The algorithm preserves the data type of the input raster. Therefore byte/integer
rasters can only be rounded to multiples of a base n, otherwise a warning is raised
and the raster gets copied as byte/integer raster.</p>
<figure class="align-center" id="id130">
<img alt="../../../../_images/round_raster.png" src="../../../../_images/round_raster.png" />
<figcaption>
<p><span class="caption-text">Rounding values of a raster</span><a class="headerlink" href="#id130" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id107">
<h3>Parameters<a class="headerlink" href="#id107" title="Link to this heading"></a></h3>
<section id="id108">
<h4>Basic parameters<a class="headerlink" href="#id108" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The raster to process.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1</p>
</td>
<td><p>The band of the raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Rounding direction</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ROUNDING_DIRECTION</span></code></p></td>
<td><p>[list]</p>
<p>Default: 1</p>
</td>
<td><p>How to choose the target rounded value. Options are:</p>
<ul class="simple">
<li><p>0 — Round up</p></li>
<li><p>1 — Round to nearest</p></li>
<li><p>2 — Round down</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Number of decimals places</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DECIMAL_PLACES</span></code></p></td>
<td><p>[number]</p>
<p>Default: 2</p>
</td>
<td><p>Number of decimals places to round to.
Use negative values to round cell values to a multiple of a base n</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Save</span> <span class="pre">to</span> <span class="pre">temporary</span> <span class="pre">file]</span></code></p>
</td>
<td><p>Specification of the output file. One of:</p>
<ul class="simple">
<li><p>Save to a Temporary File</p></li>
<li><p>Save to File…</p></li>
</ul>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id109">
<h4>Advanced parameters<a class="headerlink" href="#id109" title="Link to this heading"></a></h4>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Base n for rounding to multiples of n</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BASE_N</span></code></p></td>
<td><p>[number]</p>
<p>Default: 10</p>
</td>
<td><p>When the <code class="docutils literal notranslate"><span class="pre">DECIMAL_PLACES</span></code> parameter is negative,
raster values are rounded to multiples of the base n value</p></td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id110">
<h3>Outputs<a class="headerlink" href="#id110" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output raster</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>The output raster layer with values rounded for the selected band.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id111">
<h3>Python code<a class="headerlink" href="#id111" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:roundrastervalues</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="sample-raster-values">
<span id="qgisrastersampling"></span><h2><a class="toc-backref" href="#id160" role="doc-backlink"><span class="section-number">28.1.15.29. </span>Sample raster values</a><a class="headerlink" href="#sample-raster-values" title="Link to this heading"></a></h2>
<p>Extracts raster values at the point locations.
If the raster layer is multiband, each band is sampled.</p>
<p>The attribute table of the resulting layer will have as many new
columns as the raster layer band count.</p>
<section id="id112">
<h3>Parameters<a class="headerlink" href="#id112" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 30.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 30.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input Layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>Point vector layer to use for  sampling</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Raster Layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RASTERCOPY</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Raster layer to sample at the given point locations.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output column prefix</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">COLUMN_PREFIX</span></code></p></td>
<td><p>[string]</p>
<p>Default: ‘SAMPLE_’</p>
</td>
<td><p>Prefix for the names of the added columns.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Sampled</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output layer containing the sampled values.
One of:</p>
<ul class="simple">
<li><p>Create Temporary Layer (<code class="docutils literal notranslate"><span class="pre">TEMPORARY_OUTPUT</span></code>)</p></li>
<li><p>Save to File…</p></li>
<li><p>Save to Geopackage…</p></li>
<li><p>Save to Database Table…</p></li>
</ul>
<p>The file encoding can also be changed here.</p>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id113">
<h3>Outputs<a class="headerlink" href="#id113" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Sampled</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output layer containing the sampled values.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id114">
<h3>Python code<a class="headerlink" href="#id114" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rastersampling</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="zonal-histogram">
<span id="qgiszonalhistogram"></span><h2><a class="toc-backref" href="#id161" role="doc-backlink"><span class="section-number">28.1.15.30. </span>Zonal histogram</a><a class="headerlink" href="#zonal-histogram" title="Link to this heading"></a></h2>
<p>Appends fields representing counts of each unique value from a raster
layer contained within polygon features.</p>
<p>The output layer attribute table will have as many fields as the
unique values of the raster layer that intersects the polygon(s).</p>
<figure class="align-center" id="id131">
<img alt="../../../../_images/raster_histogram.png" src="../../../../_images/raster_histogram.png" />
<figcaption>
<p><span class="caption-text">Raster layer histogram example</span><a class="headerlink" href="#id131" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id115">
<h3>Parameters<a class="headerlink" href="#id115" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Raster layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RASTER_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the input layer</p>
</td>
<td><p>If the raster is multiband, choose a band.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Vector layer containing zones</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_VECTOR</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Vector polygon layer that defines the zones.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output column prefix</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">COLUMN_PREFIX</span></code></p>
<p>Optional</p>
</td>
<td><p>[string]</p>
<p>Default: ‘HISTO_’</p>
</td>
<td><p>Prefix for the output columns names.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output zones</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector polygon layer.
One of:</p>
<ul class="simple">
<li><p>Create Temporary Layer (<code class="docutils literal notranslate"><span class="pre">TEMPORARY_OUTPUT</span></code>)</p></li>
<li><p>Save to File…</p></li>
<li><p>Save to Geopackage…</p></li>
<li><p>Save to Database Table…</p></li>
</ul>
<p>The file encoding can also be changed here.</p>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id116">
<h3>Outputs<a class="headerlink" href="#id116" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Output zones</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output vector polygon layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id117">
<h3>Python code<a class="headerlink" href="#id117" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:zonalhistogram</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
<section id="zonal-statistics">
<span id="qgiszonalstatisticsfb"></span><h2><a class="toc-backref" href="#id162" role="doc-backlink"><span class="section-number">28.1.15.31. </span>Zonal statistics</a><a class="headerlink" href="#zonal-statistics" title="Link to this heading"></a></h2>
<p>Calculates statistics of a raster layer for each feature of an
overlapping polygon vector layer.</p>
<section id="id118">
<h3>Parameters<a class="headerlink" href="#id118" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Input layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Vector polygon layer that contains the zones.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Raster layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Input raster layer.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Raster band</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RASTER_BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: The first band of the input layer</p>
</td>
<td><p>If the raster is multiband, choose a band for the statistics.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output column prefix</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">COLUMN_PREFIX</span></code></p></td>
<td><p>[string]</p>
<p>Default: ‘_’</p>
</td>
<td><p>Prefix for the output columns names.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Statistics to calculate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">STATISTICS</span></code></p></td>
<td><p>[enumeration] [list]</p>
<p>Default: [0,1,2]</p>
</td>
<td><p>List of statistical operator for the output.
Options:</p>
<ul class="simple">
<li><p>0 — Count</p></li>
<li><p>1 — Sum</p></li>
<li><p>2 — Mean</p></li>
<li><p>3 — Median</p></li>
<li><p>4 — St. dev.</p></li>
<li><p>5 — Minimum</p></li>
<li><p>6 — Maximum</p></li>
<li><p>7 — Range</p></li>
<li><p>8 — Minority</p></li>
<li><p>9 — Majority</p></li>
<li><p>10 — Variety</p></li>
<li><p>11 — Variance</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Zonal Statistics</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector polygon layer.
One of:</p>
<ul class="simple">
<li><p>Create Temporary Layer (<code class="docutils literal notranslate"><span class="pre">TEMPORARY_OUTPUT</span></code>)</p></li>
<li><p>Save to File…</p></li>
<li><p>Save to Geopackage…</p></li>
<li><p>Save to Database Table…</p></li>
<li><p>Append to Layer…</p></li>
</ul>
<p>The file encoding can also be changed here.</p>
</td>
</tr>
</tbody>
</table>
</section>
<section id="id119">
<h3>Outputs<a class="headerlink" href="#id119" title="Link to this heading"></a></h3>
<table class="docutils align-default">
<colgroup>
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 20.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Label</p></th>
<th class="head"><p>Name</p></th>
<th class="head"><p>Type</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><strong>Zonal Statistics</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The zone vector layer with added statistics.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id120">
<h3>Python code<a class="headerlink" href="#id120" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:zonalstatisticsfb</span></code></p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="kn">import</span> <span class="nn">processing</span>
<span class="n">processing</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&quot;algorithm_id&quot;</span><span class="p">,</span> <span class="p">{</span><span class="n">parameter_dictionary</span><span class="p">})</span>
</pre></div>
</div>
<p>The <em>algorithm id</em> is displayed when you hover over the algorithm in
the Processing Toolbox.
The <em>parameter dictionary</em> provides the parameter NAMEs and values.
See <a class="reference internal" href="../../processing/console.html#processing-console"><span class="std std-ref">Using processing algorithms from the console</span></a> for details on how to run processing algorithms
from the Python console.</p>
</section>
</section>
</section>


           </div>
          </div>
          <footer><div class="rst-footer-buttons" role="navigation" aria-label="Footer">
        <a href="pointcloudextraction.html" class="btn btn-neutral float-left" title="28.1.14. Point Cloud Extraction" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="rastercreation.html" class="btn btn-neutral float-right" title="28.1.16. Raster Creation" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
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
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">en</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/cs/docs/user_manual/processing_algs/qgis/rasteranalysis.html">cs</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/de/docs/user_manual/processing_algs/qgis/rasteranalysis.html">de</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/es/docs/user_manual/processing_algs/qgis/rasteranalysis.html">es</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/fr/docs/user_manual/processing_algs/qgis/rasteranalysis.html">fr</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/hu/docs/user_manual/processing_algs/qgis/rasteranalysis.html">hu</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/it/docs/user_manual/processing_algs/qgis/rasteranalysis.html">it</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ja/docs/user_manual/processing_algs/qgis/rasteranalysis.html">ja</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ko/docs/user_manual/processing_algs/qgis/rasteranalysis.html">ko</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/lt/docs/user_manual/processing_algs/qgis/rasteranalysis.html">lt</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/nl/docs/user_manual/processing_algs/qgis/rasteranalysis.html">nl</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_BR/docs/user_manual/processing_algs/qgis/rasteranalysis.html">pt_BR</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_PT/docs/user_manual/processing_algs/qgis/rasteranalysis.html">pt_PT</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ro/docs/user_manual/processing_algs/qgis/rasteranalysis.html">ro</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ru/docs/user_manual/processing_algs/qgis/rasteranalysis.html">ru</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/zh-Hans/docs/user_manual/processing_algs/qgis/rasteranalysis.html">zh-Hans</a></dd>
        
      </dl>

      <dl>
        <dt>Versions</dt>
        
          <dd><a href="https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">testing</a></dd>
        
          <dd><a href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">latest</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">3.40</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">3.34</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">3.28</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.22/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">3.22</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.16/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">3.16</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.10/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">3.10</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.4/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">3.4</a></dd>
        
          <dd><a href="https://docs.qgis.org/2.18/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html">2.18</a></dd>
        
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

