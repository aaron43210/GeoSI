Title: Live Content

Description: Fetched live

Source: https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html

---

<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="../../../../">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>28.1.22. Vector geometry &mdash; QGIS Documentation  documentation</title>
      <link rel="stylesheet" type="text/css" href="../../../../_static/pygments.css?v=80d5e7a1" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/css/qgis_docs.css?v=01847ad1" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/togglebutton.css?v=13237357" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/copybutton.css?v=76b2166b" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/css/qgis_topbar.css?v=5613a779" />

  
    <link rel="shortcut icon" href="../../../../_static/qgis_logo.ico"/>
    <link rel="canonical" href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html"/>
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
    <link rel="next" title="28.1.23. Vector overlay" href="vectoroverlay.html" />
    <link rel="prev" title="28.1.21. Vector general" href="vectorgeneral.html" />
  <meta name="description" content="QGIS 3.34 documentation: 28.1.22. Vector geometry">
  <meta name="robots" content="noindex">
</head>

<body class="wy-body-for-nav">

  <nav class="release_status_topbar">
    <div class="row outdated">
     This documentation is for a QGIS version which has reached end of life. Instead visit the <a href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">latest version</a>.
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
<li class="toctree-l4"><a class="reference internal" href="rasteranalysis.html">28.1.15. Raster analysis</a></li>
<li class="toctree-l4"><a class="reference internal" href="rastercreation.html">28.1.16. Raster Creation</a></li>
<li class="toctree-l4"><a class="reference internal" href="rasterterrainanalysis.html">28.1.17. Raster terrain analysis</a></li>
<li class="toctree-l4"><a class="reference internal" href="rastertools.html">28.1.18. Raster tools</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectoranalysis.html">28.1.19. Vector analysis</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectorcreation.html">28.1.20. Vector creation</a></li>
<li class="toctree-l4"><a class="reference internal" href="vectorgeneral.html">28.1.21. Vector general</a></li>
<li class="toctree-l4 current"><a class="current reference internal" href="#">28.1.22. Vector geometry</a></li>
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
      <li class="breadcrumb-item active"><span class="section-number">28.1.22. </span>Vector geometry</li>

    <li style="float: right; text-align: right;">
	<ul>
		
      <li class="wy-breadcrumbs-aside">
            <a href="../../../../_sources/docs/user_manual/processing_algs/qgis/vectorgeometry.rst.txt" rel="nofollow"> View page source</a>
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
        <a href="vectorgeneral.html" class="btn btn-neutral float-left" title="28.1.21. Vector general" accesskey="p"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="vectoroverlay.html" class="btn btn-neutral float-right" title="28.1.23. Vector overlay" accesskey="n">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
  </div>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <blockquote>
<div></div></blockquote>
<section id="vector-geometry">
<h1><span class="section-number">28.1.22. </span>Vector geometry<a class="headerlink" href="#vector-geometry" title="Link to this heading"></a></h1>
<nav class="contents toc-columns local" id="contents">
<ul class="simple">
<li><p><a class="reference internal" href="#add-geometry-attributes" id="id305">Add geometry attributes</a></p></li>
<li><p><a class="reference internal" href="#affine-transform" id="id306">Affine transform</a></p></li>
<li><p><a class="reference internal" href="#aggregate" id="id307">Aggregate</a></p></li>
<li><p><a class="reference internal" href="#boundary" id="id308">Boundary</a></p></li>
<li><p><a class="reference internal" href="#bounding-boxes" id="id309">Bounding boxes</a></p></li>
<li><p><a class="reference internal" href="#buffer" id="id310">Buffer</a></p></li>
<li><p><a class="reference internal" href="#centroids" id="id311">Centroids</a></p></li>
<li><p><a class="reference internal" href="#check-validity" id="id312">Check validity</a></p></li>
<li><p><a class="reference internal" href="#collect-geometries" id="id313">Collect geometries</a></p></li>
<li><p><a class="reference internal" href="#concave-hull" id="id314">Concave hull</a></p></li>
<li><p><a class="reference internal" href="#convert-geometry-type" id="id315">Convert geometry type</a></p></li>
<li><p><a class="reference internal" href="#convert-to-curved-geometries" id="id316">Convert to curved geometries</a></p></li>
<li><p><a class="reference internal" href="#convex-hull" id="id317">Convex hull</a></p></li>
<li><p><a class="reference internal" href="#create-layer-from-extent" id="id318">Create layer from extent</a></p></li>
<li><p><a class="reference internal" href="#create-layer-from-point" id="id319">Create layer from point</a></p></li>
<li><p><a class="reference internal" href="#create-wedge-buffers" id="id320">Create wedge buffers</a></p></li>
<li><p><a class="reference internal" href="#delaunay-triangulation" id="id321">Delaunay triangulation</a></p></li>
<li><p><a class="reference internal" href="#delete-holes" id="id322">Delete holes</a></p></li>
<li><p><a class="reference internal" href="#densify-by-count" id="id323">Densify by count</a></p></li>
<li><p><a class="reference internal" href="#densify-by-interval" id="id324">Densify by interval</a></p></li>
<li><p><a class="reference internal" href="#dissolve" id="id325">Dissolve</a></p></li>
<li><p><a class="reference internal" href="#drape-set-z-value-from-raster" id="id326">Drape (set Z value from raster)</a></p></li>
<li><p><a class="reference internal" href="#drop-m-z-values" id="id327">Drop M/Z values</a></p></li>
<li><p><a class="reference internal" href="#eliminate-selected-polygons" id="id328">Eliminate selected polygons</a></p></li>
<li><p><a class="reference internal" href="#explode-lines" id="id329">Explode lines</a></p></li>
<li><p><a class="reference internal" href="#extend-lines" id="id330">Extend lines</a></p></li>
<li><p><a class="reference internal" href="#extract-m-values" id="id331">Extract M values</a></p></li>
<li><p><a class="reference internal" href="#extract-specific-vertices" id="id332">Extract specific vertices</a></p></li>
<li><p><a class="reference internal" href="#extract-vertices" id="id333">Extract vertices</a></p></li>
<li><p><a class="reference internal" href="#extract-z-values" id="id334">Extract Z values</a></p></li>
<li><p><a class="reference internal" href="#filter-vertices-by-m-value" id="id335">Filter vertices by M value</a></p></li>
<li><p><a class="reference internal" href="#filter-vertices-by-z-value" id="id336">Filter vertices by Z value</a></p></li>
<li><p><a class="reference internal" href="#fix-geometries" id="id337">Fix geometries</a></p></li>
<li><p><a class="reference internal" href="#force-right-hand-rule" id="id338">Force right-hand-rule</a></p></li>
<li><p><a class="reference internal" href="#geodesic-line-split-at-antimeridian" id="id339">Geodesic line split at antimeridian</a></p></li>
<li><p><a class="reference internal" href="#geometry-by-expression" id="id340">Geometry by expression</a></p></li>
<li><p><a class="reference internal" href="#interpolate-point-on-line" id="id341">Interpolate point on line</a></p></li>
<li><p><a class="reference internal" href="#keep-n-biggest-parts" id="id342">Keep N biggest parts</a></p></li>
<li><p><a class="reference internal" href="#line-substring" id="id343">Line substring</a></p></li>
<li><p><a class="reference internal" href="#lines-to-polygons" id="id344">Lines to polygons</a></p></li>
<li><p><a class="reference internal" href="#merge-lines" id="id345">Merge lines</a></p></li>
<li><p><a class="reference internal" href="#minimum-bounding-geometry" id="id346">Minimum bounding geometry</a></p></li>
<li><p><a class="reference internal" href="#minimum-enclosing-circles" id="id347">Minimum enclosing circles</a></p></li>
<li><p><a class="reference internal" href="#multi-ring-buffer-constant-distance" id="id348">Multi-ring buffer (constant distance)</a></p></li>
<li><p><a class="reference internal" href="#multipart-to-singleparts" id="id349">Multipart to singleparts</a></p></li>
<li><p><a class="reference internal" href="#offset-lines" id="id350">Offset lines</a></p></li>
<li><p><a class="reference internal" href="#oriented-minimum-bounding-box" id="id351">Oriented minimum bounding box</a></p></li>
<li><p><a class="reference internal" href="#orthogonalize" id="id352">Orthogonalize</a></p></li>
<li><p><a class="reference internal" href="#point-on-surface" id="id353">Point on Surface</a></p></li>
<li><p><a class="reference internal" href="#points-along-geometry" id="id354">Points along geometry</a></p></li>
<li><p><a class="reference internal" href="#points-displacement" id="id355">Points displacement</a></p></li>
<li><p><a class="reference internal" href="#pole-of-inaccessibility" id="id356">Pole of inaccessibility</a></p></li>
<li><p><a class="reference internal" href="#polygonize" id="id357">Polygonize</a></p></li>
<li><p><a class="reference internal" href="#polygons-to-lines" id="id358">Polygons to lines</a></p></li>
<li><p><a class="reference internal" href="#project-points-cartesian" id="id359">Project points (Cartesian)</a></p></li>
<li><p><a class="reference internal" href="#promote-to-multipart" id="id360">Promote to multipart</a></p></li>
<li><p><a class="reference internal" href="#rectangles-ovals-diamonds" id="id361">Rectangles, ovals, diamonds</a></p></li>
<li><p><a class="reference internal" href="#remove-duplicate-vertices" id="id362">Remove duplicate vertices</a></p></li>
<li><p><a class="reference internal" href="#remove-null-geometries" id="id363">Remove null geometries</a></p></li>
<li><p><a class="reference internal" href="#reverse-line-direction" id="id364">Reverse line direction</a></p></li>
<li><p><a class="reference internal" href="#rotate" id="id365">Rotate</a></p></li>
<li><p><a class="reference internal" href="#roundness" id="id366">Roundness</a></p></li>
<li><p><a class="reference internal" href="#segmentize-by-maximum-angle" id="id367">Segmentize by maximum angle</a></p></li>
<li><p><a class="reference internal" href="#segmentize-by-maximum-distance" id="id368">Segmentize by maximum distance</a></p></li>
<li><p><a class="reference internal" href="#set-m-value" id="id369">Set M value</a></p></li>
<li><p><a class="reference internal" href="#set-m-value-from-raster" id="id370">Set M value from raster</a></p></li>
<li><p><a class="reference internal" href="#set-z-value" id="id371">Set Z value</a></p></li>
<li><p><a class="reference internal" href="#simplify" id="id372">Simplify</a></p></li>
<li><p><a class="reference internal" href="#single-sided-buffer" id="id373">Single sided buffer</a></p></li>
<li><p><a class="reference internal" href="#smooth" id="id374">Smooth</a></p></li>
<li><p><a class="reference internal" href="#snap-geometries-to-layer" id="id375">Snap geometries to layer</a></p></li>
<li><p><a class="reference internal" href="#snap-points-to-grid" id="id376">Snap points to grid</a></p></li>
<li><p><a class="reference internal" href="#split-lines-by-maximum-length" id="id377">Split lines by maximum length</a></p></li>
<li><p><a class="reference internal" href="#subdivide" id="id378">Subdivide</a></p></li>
<li><p><a class="reference internal" href="#swap-x-and-y-coordinates" id="id379">Swap X and Y coordinates</a></p></li>
<li><p><a class="reference internal" href="#tapered-buffers" id="id380">Tapered buffers</a></p></li>
<li><p><a class="reference internal" href="#tessellate" id="id381">Tessellate</a></p></li>
<li><p><a class="reference internal" href="#transect" id="id382">Transect</a></p></li>
<li><p><a class="reference internal" href="#translate" id="id383">Translate</a></p></li>
<li><p><a class="reference internal" href="#variable-width-buffer-by-m-value" id="id384">Variable width buffer (by M value)</a></p></li>
<li><p><a class="reference internal" href="#voronoi-polygons" id="id385">Voronoi polygons</a></p></li>
</ul>
</nav>
<section id="add-geometry-attributes">
<span id="qgisexportaddgeometrycolumns"></span><h2><a class="toc-backref" href="#id305" role="doc-backlink"><span class="section-number">28.1.22.1. </span>Add geometry attributes</a><a class="headerlink" href="#add-geometry-attributes" title="Link to this heading"></a></h2>
<p>Computes geometric properties of the features in a vector layer and
includes them in the output layer.</p>
<p>It generates a new vector layer with the same content as the input one,
but with additional attributes, containing geometric measurements
based on a selected CRS.</p>
<p>The attributes added to the table depend on the geometry type and
dimension of the input layer:</p>
<ul class="simple">
<li><p>for <strong>point</strong> layers: X (<code class="docutils literal notranslate"><span class="pre">xcoord</span></code>), Y (<code class="docutils literal notranslate"><span class="pre">ycoord</span></code>), Z (<code class="docutils literal notranslate"><span class="pre">zcoord</span></code>)
coordinates and/or M value (<code class="docutils literal notranslate"><span class="pre">mvalue</span></code>)</p></li>
<li><p>for <strong>line</strong> layers: <code class="docutils literal notranslate"><span class="pre">length</span></code> and, for the LineString and
CompoundCurve geometry types, the feature <code class="docutils literal notranslate"><span class="pre">sinuosity</span></code> and straight
distance (<code class="docutils literal notranslate"><span class="pre">straightdis</span></code>)</p></li>
<li><p>for <strong>polygon</strong> layers: <code class="docutils literal notranslate"><span class="pre">perimeter</span></code> and <code class="docutils literal notranslate"><span class="pre">area</span></code></p></li>
</ul>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<section id="parameters">
<h3>Parameters<a class="headerlink" href="#parameters" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Calculate using</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">CALC_METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Calculation parameters to use for the geometric properties.
One of:</p>
<ul class="simple">
<li><p>0 — Layer CRS</p></li>
<li><p>1 — Project CRS</p></li>
<li><p>2 — Ellipsoidal</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Added geom info</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (input copy with geometry) layer.
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
<section id="outputs">
<h3>Outputs<a class="headerlink" href="#outputs" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Added geom info</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Copy of the input vector layer with the addition of the geometry fields</p></td>
</tr>
</tbody>
</table>
</section>
<section id="python-code">
<h3>Python code<a class="headerlink" href="#python-code" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:exportaddgeometrycolumns</span></code></p>
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
<section id="affine-transform">
<span id="qgisaffinetransform"></span><h2><a class="toc-backref" href="#id306" role="doc-backlink"><span class="section-number">28.1.22.2. </span>Affine transform</a><a class="headerlink" href="#affine-transform" title="Link to this heading"></a></h2>
<p>Applies an affine transformation to the layer geometries.
Affine transformations can include translation, scaling and rotation.
The operations are performed in the following order: scale, rotation, and translation.</p>
<p>Z and M values (if present) can be translated and scaled.</p>
<figure class="align-center" id="id243">
<img alt="../../../../_images/affinetransform.png" src="../../../../_images/affinetransform.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.59 </span><span class="caption-text">Vector point layer (green dots) before (left), and after (right) an affine transformation (translation).</span><a class="headerlink" href="#id243" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgistranslategeometry"><span class="std std-ref">Translate</span></a></p>
</div>
<section id="id1">
<h3>Parameters<a class="headerlink" href="#id1" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Translation (x-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_X</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0</p>
</td>
<td><p>Displacement to apply on the X axis.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Translation (y-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_Y</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0</p>
</td>
<td><p>Displacement to apply on the Y axis.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Translation (z-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_Z</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0</p>
</td>
<td><p>Displacement to apply on the Z axis.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Translation (m-values)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_M</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0</p>
</td>
<td><p>Offset to apply on m values.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Scale factor (x-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SCALE_X</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1</p>
</td>
<td><p>Scaling value (expansion or contraction) to apply on the X axis.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Scale factor (y-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SCALE_Y</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1</p>
</td>
<td><p>Scaling value (expansion or contraction) to apply on the Y axis.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Scale factor (z-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SCALE_Z</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1</p>
</td>
<td><p>Scaling value (expansion or contraction) to apply on the Z axis.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Scale factor (m-values)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SCALE_M</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1</p>
</td>
<td><p>Scaling value (expansion or contraction) to apply on m values.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Rotation around z-axis (degrees counter-clockwise)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ROTATION_Z</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0</p>
</td>
<td><p>Angle of the rotation in degrees.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Transformed</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer.
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
<section id="id2">
<h3>Outputs<a class="headerlink" href="#id2" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Transformed</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output (transformed) vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id3">
<h3>Python code<a class="headerlink" href="#id3" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:affinetransform</span></code></p>
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
<section id="aggregate">
<span id="qgisaggregate"></span><h2><a class="toc-backref" href="#id307" role="doc-backlink"><span class="section-number">28.1.22.3. </span>Aggregate</a><a class="headerlink" href="#aggregate" title="Link to this heading"></a></h2>
<p>Takes a vector or table layer and creates a new layer by aggregating
features based on a <code class="docutils literal notranslate"><span class="pre">group</span> <span class="pre">by</span></code> expression.</p>
<p>Features for which <code class="docutils literal notranslate"><span class="pre">group</span> <span class="pre">by</span></code> expression returns the same value are
grouped together.</p>
<p>It is possible to group all source features together using constant
value in <code class="docutils literal notranslate"><span class="pre">group</span> <span class="pre">by</span></code> parameter, example: NULL.</p>
<p>It is also possible to group features by multiple fields using Array
function, example: Array(“Field1”, “Field2”).</p>
<p>Geometries (if present) are combined into one multipart geometry for
each group.
Output attributes are computed depending on each given aggregate
definition.</p>
<p>This algorithm allows to use the default
<a class="reference internal" href="../../expressions/functions_list.html#aggregates-function"><span class="std std-ref">aggregates functions</span></a> of the QGIS Expression engine.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgiscollect"><span class="std std-ref">Collect geometries</span></a>, <a class="reference internal" href="#qgisdissolve"><span class="std std-ref">Dissolve</span></a></p>
</div>
<section id="id4">
<h3>Parameters<a class="headerlink" href="#id4" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Group by expression</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">GROUP_BY</span></code></p></td>
<td><p>[tablefield: any]</p>
<p>Default: ‘NULL’</p>
</td>
<td><p>Choose the grouping field.
If <em>NULL</em> all features will be grouped.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Aggregates</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">AGGREGATES</span></code></p></td>
<td><p>[list]</p></td>
<td><p>List of output layer field definitions.
Example of a field definition:</p>
<p><em>{‘aggregate’: ‘sum’, ‘delimiter’: ‘,’, ‘input’: ‘ $area’,
‘length’: 10, ‘name’: ‘totarea’, ‘precision’: 0, ‘type’: 6}</em></p>
<p>By default, the list contains all the fields of the input layer.
In the GUI, you can edit these fields and their definitions,
and you can also:</p>
<ul class="simple">
<li><p>Click the <a class="reference internal" href="../../../../_images/mActionNewAttribute.png"><img alt="newAttribute" src="../../../../_images/mActionNewAttribute.png" style="width: 1.5em;" /></a> button to add a new field.</p></li>
<li><p>Click <a class="reference internal" href="../../../../_images/mActionDeleteAttribute.png"><img alt="deleteAttribute" src="../../../../_images/mActionDeleteAttribute.png" style="width: 1.5em;" /></a> to delete the selected field.</p></li>
<li><p>Use <a class="reference internal" href="../../../../_images/mActionArrowUp.png"><img alt="arrowUp" src="../../../../_images/mActionArrowUp.png" style="width: 1.5em;" /></a> and <a class="reference internal" href="../../../../_images/mActionArrowDown.png"><img alt="arrowDown" src="../../../../_images/mActionArrowDown.png" style="width: 1.5em;" /></a> to change order of the fields.</p></li>
<li><p>Click <a class="reference internal" href="../../../../_images/mIconClearText.png"><img alt="clearText" src="../../../../_images/mIconClearText.png" style="width: 1.5em;" /></a> to reset to the default (the fields of the
input layer).</p></li>
</ul>
<p>For each of the fields you’d like to retrieve information from,
you need to define the following:</p>
<dl>
<dt><code class="docutils literal notranslate"><span class="pre">Input</span> <span class="pre">expression</span></code> [expression] (<code class="docutils literal notranslate"><span class="pre">input</span></code>)</dt><dd><p>Field or expression from the input layer.</p>
</dd>
<dt><code class="docutils literal notranslate"><span class="pre">Aggregate</span> <span class="pre">function</span></code> [enumeration] (<code class="docutils literal notranslate"><span class="pre">aggregate</span></code>)</dt><dd><p><a class="reference internal" href="../../expressions/functions_list.html#aggregates-function"><span class="std std-ref">Function</span></a> to use on the input
expression to return the aggregated value.</p>
<p>Default: <em>concatenate</em> (for string data type), <em>sum</em> (for
numeric data type)</p>
</dd>
<dt><code class="docutils literal notranslate"><span class="pre">Delimiter</span></code> [string] (<code class="docutils literal notranslate"><span class="pre">delimiter</span></code>)</dt><dd><p>Text string to separate aggregated values, for example in
case of concatenation.</p>
<p>Default: <em>,</em></p>
</dd>
<dt><code class="docutils literal notranslate"><span class="pre">Output</span> <span class="pre">field</span> <span class="pre">name</span></code> [string] (<code class="docutils literal notranslate"><span class="pre">name</span></code>)</dt><dd><p>Name of the aggregated field in the output layer.
By default input field name is kept.</p>
</dd>
<dt><code class="docutils literal notranslate"><span class="pre">Type</span></code> [enumeration] (<code class="docutils literal notranslate"><span class="pre">type</span></code>)</dt><dd><p>Data type of the output field. One of:</p>
<ul class="simple">
<li><p>1 — Boolean</p></li>
<li><p>2 — Integer</p></li>
<li><p>4 — Integer64</p></li>
<li><p>6 — Double</p></li>
<li><p>10 — String</p></li>
<li><p>14 — Date</p></li>
<li><p>16 — DateTime</p></li>
</ul>
</dd>
<dt><code class="docutils literal notranslate"><span class="pre">Length</span></code> [number] (<code class="docutils literal notranslate"><span class="pre">length</span></code>)</dt><dd><p>Length of the output field.</p>
</dd>
<dt><code class="docutils literal notranslate"><span class="pre">Precision</span></code> [number] (<code class="docutils literal notranslate"><span class="pre">precision</span></code>)</dt><dd><p>Precision of the output field.</p>
</dd>
</dl>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Load fields from layer</strong></p></td>
<td><p>GUI only</p></td>
<td><p>[vector: any]</p></td>
<td><p>You can load fields from another layer and use them for the
aggregation</p></td>
</tr>
<tr class="row-even"><td><p><strong>Aggregated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (aggregate) layer
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
<tr class="row-even"><td><p><strong>Aggregated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Multigeometry vector layer with the aggregated values</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id6">
<h3>Python code<a class="headerlink" href="#id6" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:aggregate</span></code></p>
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
<section id="boundary">
<span id="qgisboundary"></span><h2><a class="toc-backref" href="#id308" role="doc-backlink"><span class="section-number">28.1.22.4. </span>Boundary</a><a class="headerlink" href="#boundary" title="Link to this heading"></a></h2>
<p>Returns the closure of the combinatorial boundary of the input
geometries (i.e. the topological boundary of the geometry).</p>
<p>Only for polygon and line layers.</p>
<p>For <strong>polygon geometries</strong> , the boundary consists of all the lines
making up the rings of the polygon.</p>
<figure class="align-center" id="id244">
<img alt="../../../../_images/boundary_polygon.png" src="../../../../_images/boundary_polygon.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.60 </span><span class="caption-text">Boundaries (black dashed line) of the source polygon layer</span><a class="headerlink" href="#id244" title="Link to this image"></a></p>
</figcaption>
</figure>
<p>For <strong>lines geometries</strong>, the boundaries are their end points.</p>
<figure class="align-center" id="id245">
<img alt="../../../../_images/boundary_lines.png" src="../../../../_images/boundary_lines.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.61 </span><span class="caption-text">Boundary layer (red points) for lines. In yellow a selected feature.</span><a class="headerlink" href="#id245" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id7">
<h3>Parameters<a class="headerlink" href="#id7" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Boundary</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point, line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (boundary) layer.
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
<section id="id8">
<h3>Outputs<a class="headerlink" href="#id8" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Boundary</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point, line]</p></td>
<td><p>Boundaries from the input layer (point for line, and line
for polygon)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id9">
<h3>Python code<a class="headerlink" href="#id9" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:boundary</span></code></p>
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
<section id="bounding-boxes">
<span id="qgisboundingboxes"></span><h2><a class="toc-backref" href="#id309" role="doc-backlink"><span class="section-number">28.1.22.5. </span>Bounding boxes</a><a class="headerlink" href="#bounding-boxes" title="Link to this heading"></a></h2>
<p>Calculates the bounding box (envelope) of each feature in an input layer.
Polygon and line geometries are supported.</p>
<figure class="align-center" id="id246">
<img alt="../../../../_images/bounding_box.png" src="../../../../_images/bounding_box.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.62 </span><span class="caption-text">Black lines represent the bounding boxes of each polygon feature</span><a class="headerlink" href="#id246" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisminimumboundinggeometry"><span class="std std-ref">Minimum bounding geometry</span></a></p>
</div>
<section id="id10">
<h3>Parameters<a class="headerlink" href="#id10" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Bounds</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (bounding box) layer.
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
<tr class="row-even"><td><p><strong>Bounds</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Bounding boxes of input layer.
Other than the input attributes, the output layer also contains following fields:
<code class="docutils literal notranslate"><span class="pre">width</span></code>, <code class="docutils literal notranslate"><span class="pre">height</span></code>, <code class="docutils literal notranslate"><span class="pre">area</span></code> and <code class="docutils literal notranslate"><span class="pre">perimeter</span></code> of the generated polygon.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id12">
<h3>Python code<a class="headerlink" href="#id12" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:boundingboxes</span></code></p>
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
<section id="buffer">
<span id="qgisbuffer"></span><h2><a class="toc-backref" href="#id310" role="doc-backlink"><span class="section-number">28.1.22.6. </span>Buffer</a><a class="headerlink" href="#buffer" title="Link to this heading"></a></h2>
<p>Computes a buffer area for all the features in an input layer, using
a fixed or data defined distance.</p>
<p>It is possible to use a negative distance for polygon input layers.
In this case the buffer will result in a smaller polygon (setback).</p>
<figure class="align-center" id="id247">
<img alt="../../../../_images/buffer1.png" src="../../../../_images/buffer1.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.63 </span><span class="caption-text">Buffer (in yellow) of points, line, polygon with positive buffer,
and polygon with negative buffer</span><a class="headerlink" href="#id247" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geoprocessing Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="modelertools.html#qgisvariabledistancebuffer"><span class="std std-ref">Variable distance buffer</span></a>,
<a class="reference internal" href="#qgismultiringconstantbuffer"><span class="std std-ref">Multi-ring buffer (constant distance)</span></a>, <a class="reference internal" href="#qgisbufferbym"><span class="std std-ref">Variable width buffer (by M value)</span></a></p>
</div>
<section id="id13">
<h3>Parameters<a class="headerlink" href="#id13" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Input layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 10.0</p>
</td>
<td><p>Buffer distance (from the boundary of each feature).
You can use the Data Defined button on the right to choose
a field from which the radius will be calculated.
This way you can have different radius for each feature
(see <a class="reference internal" href="modelertools.html#qgisvariabledistancebuffer"><span class="std std-ref">Variable distance buffer</span></a>).</p></td>
</tr>
<tr class="row-even"><td><p><strong>Segments</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEGMENTS</span></code></p></td>
<td><p>[number]</p>
<p>Default: 5</p>
</td>
<td><p>Controls the number of line segments to use to approximate
a quarter circle when creating rounded offsets.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>End cap style</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">END_CAP_STYLE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Controls how line endings are handled in the buffer.
One of:</p>
<ul class="simple">
<li><p>0 — Round</p></li>
<li><p>1 — Flat</p></li>
<li><p>2 — Square</p></li>
</ul>
<figure class="align-center" id="id248">
<a class="reference internal image-reference" href="../../../../_images/buffer_cap_style.png"><img alt="../../../../_images/buffer_cap_style.png" src="../../../../_images/buffer_cap_style.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.64 </span><span class="caption-text">Round, flat and square cap styles</span><a class="headerlink" href="#id248" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-even"><td><p><strong>Join style</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">JOIN_STYLE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Specifies whether round, miter or beveled joins should be
used when offsetting corners in a line.
Options are:</p>
<ul class="simple">
<li><p>0 — Round</p></li>
<li><p>1 — Miter</p></li>
<li><p>2 — Bevel</p></li>
</ul>
<figure class="align-center" id="id249">
<a class="reference internal image-reference" href="../../../../_images/buffer_join_style.png"><img alt="../../../../_images/buffer_join_style.png" src="../../../../_images/buffer_join_style.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.65 </span><span class="caption-text">Round, miter, and bevel join styles</span><a class="headerlink" href="#id249" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Miter limit</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MITER_LIMIT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 2.0</p>
</td>
<td><p>Sets the maximum distance from the offset geometry to use
when creating a mitered join as a factor of the offset distance (only applicable for miter
join styles).
Minimum: 1.0</p>
<figure class="align-center" id="id250">
<a class="reference internal image-reference" href="../../../../_images/buffer_miter_limit.png"><img alt="../../../../_images/buffer_miter_limit.png" src="../../../../_images/buffer_miter_limit.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.66 </span><span class="caption-text">A 10m buffer with a limit of 2 and a 10m buffer with a limit of 1</span><a class="headerlink" href="#id250" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-even"><td><p><strong>Dissolve result</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISSOLVE</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Dissolve the final buffer. If <code class="docutils literal notranslate"><span class="pre">True</span></code> (checked), overlapping
buffers will be dissolved (combined) into a single multipart feature.</p>
<figure class="align-center" id="id251">
<a class="reference internal image-reference" href="../../../../_images/buffer_dissolve1.png"><img alt="../../../../_images/buffer_dissolve1.png" src="../../../../_images/buffer_dissolve1.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.67 </span><span class="caption-text">Standard (three single part features - left), dissolved (1 multipart feature with 2 parts - right)</span><a class="headerlink" href="#id251" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Buffered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (buffer) layer.
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
<section id="advanced-parameters">
<h4>Advanced parameters<a class="headerlink" href="#advanced-parameters" title="Link to this heading"></a></h4>
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
<tr class="row-even"><td><p><strong>Keep disjoint features separate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEPARATE_DISJOINT</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>If <code class="docutils literal notranslate"><span class="pre">True</span></code> (checked) and dissolved is checked, features that do not overlap or touch will be exported as
separate features
(instead of parts of a multipart feature).</p>
<figure class="align-center" id="id252">
<img alt="../../../../_images/buffer_disjoint.png" src="../../../../_images/buffer_disjoint.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.68 </span><span class="caption-text">Results in 2 single part features</span><a class="headerlink" href="#id252" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id14">
<h3>Outputs<a class="headerlink" href="#id14" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Buffered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Output (buffer) polygon layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id15">
<h3>Python code<a class="headerlink" href="#id15" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:buffer</span></code></p>
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
<section id="centroids">
<span id="qgiscentroids"></span><h2><a class="toc-backref" href="#id311" role="doc-backlink"><span class="section-number">28.1.22.7. </span>Centroids</a><a class="headerlink" href="#centroids" title="Link to this heading"></a></h2>
<p>Creates a new point layer, with points representing the centroids
of the geometries of the input layer.</p>
<p>The centroid is a single point representing the barycenter (of all
parts) of the feature, so it can be outside the feature borders.
But can also be a point on each part of the feature.</p>
<p>The attributes of the points in the output layer are the same
as for the original features.</p>
<figure class="align-center" id="id253">
<img alt="../../../../_images/centroids1.png" src="../../../../_images/centroids1.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.69 </span><span class="caption-text">The red stars represent the centroids of the features of the
input layer.</span><a class="headerlink" href="#id253" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point features</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgispointonsurface"><span class="std std-ref">Point on Surface</span></a></p>
</div>
<section id="id16">
<h3>Parameters<a class="headerlink" href="#id16" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Create centroid for each part</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ALL_PARTS</span></code></p></td>
<td><p>[boolean <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: False</p>
</td>
<td><p>If True (checked), a centroid will be created for each part
of the geometry</p></td>
</tr>
<tr class="row-even"><td><p><strong>Centroids</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (centroid) layer.
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
<section id="id17">
<h3>Outputs<a class="headerlink" href="#id17" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Centroids</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>Output point vector layer (centroids)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id18">
<h3>Python code<a class="headerlink" href="#id18" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:centroids</span></code></p>
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
<section id="check-validity">
<span id="qgischeckvalidity"></span><h2><a class="toc-backref" href="#id312" role="doc-backlink"><span class="section-number">28.1.22.8. </span>Check validity</a><a class="headerlink" href="#check-validity" title="Link to this heading"></a></h2>
<p>Performs a validity check on the geometries of a vector layer.</p>
<p>The geometries are classified in three groups (valid, invalid and
error) and for each group, a vector layer with its features is
generated:</p>
<ul class="simple">
<li><p>The <strong>Valid output</strong> layer contains only the valid features (without
topological errors).</p></li>
<li><p>The <strong>Invalid output</strong> layer contains all the invalid features found
by the algorithm.</p></li>
<li><p>The <strong>Error output</strong> layer is a point layer that points to where the
invalid features were found.</p></li>
</ul>
<p>The attribute tables of the generated layers will contain some
additional information (“message” for the <strong>error</strong> layer, “FID” and
“_errors” for the <strong>invalid</strong> layer and  only “FID” for the <strong>valid</strong>
layer):</p>
<p>The attribute table of each generated vector layer will contain some
additional information (number of errors found and types of error):</p>
<figure class="align-center" id="id254">
<img alt="../../../../_images/check_validity.png" src="../../../../_images/check_validity.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.70 </span><span class="caption-text">Left: the input layer. Right: the valid layer (green), the invalid
layer (orange)</span><a class="headerlink" href="#id254" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfixgeometries"><span class="std std-ref">Fix geometries</span></a> and the core plugin
<a class="reference internal" href="../../plugins/core_plugins/plugins_geometry_checker.html#geometry-checker"><span class="std std-ref">Geometry Checker Plugin</span></a></p>
</div>
<section id="id19">
<h3>Parameters<a class="headerlink" href="#id19" title="Link to this heading"></a></h3>
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
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT_LAYER</span></code></p></td>
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Method</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 2</p>
</td>
<td><p>Method to use to check validity.
Options:</p>
<ul class="simple">
<li><p>0: The one selected in digitizing settings</p></li>
<li><p>1: QGIS</p></li>
<li><p>2: GEOS</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Ignore ring self intersection</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">IGNORE_RING_SELF_INTERSECTION</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Ignore self intersecting rings when checking for validity.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Valid output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VALID_OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the vector layer to contain a copy of the valid
features of the source layer. One of:</p>
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
<tr class="row-even"><td><p><strong>Invalid output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INVALID_OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Vector layer containing copy of the invalid features of
the source layer with the field  <code class="docutils literal notranslate"><span class="pre">_errors</span></code> listing the
summary of the error(s) found. One of:</p>
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
<tr class="row-odd"><td><p><strong>Error output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ERROR_OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Point layer of the exact position of the validity
problems detected with the <code class="docutils literal notranslate"><span class="pre">message</span></code> field describing
the error(s) found. One of:</p>
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
<section id="id20">
<h3>Outputs<a class="headerlink" href="#id20" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Count of errors</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ERROR_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of geometries that caused errors.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Error output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ERROR_OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>Point layer of the exact position of the validity
problems detected with the <code class="docutils literal notranslate"><span class="pre">message</span></code> field describing
the error(s) found.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Count of invalid features</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INVALID_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of invalid geometries.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Invalid output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INVALID_OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Vector layer containing copy of the invalid features of
the source layer with the field  <code class="docutils literal notranslate"><span class="pre">_errors</span></code> listing the
summary of the error(s) found.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Count of valid features</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VALID_COUNT</span></code></p></td>
<td><p>[number]</p></td>
<td><p>The number of valid geometries.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Valid output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VALID_OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Vector layer containing a copy of the valid features of
the source layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id21">
<h3>Python code<a class="headerlink" href="#id21" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:checkvalidity</span></code></p>
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
<section id="types-of-error-messages-and-their-meanings">
<span id="typesofgeomerrors"></span><span id="index-0"></span><h3>Types of error messages and their meanings<a class="headerlink" href="#types-of-error-messages-and-their-meanings" title="Link to this heading"></a></h3>
<table class="longtable docutils align-default" id="id255">
<caption><span class="caption-number">Table 28.1 </span><span class="caption-text">If the GEOS method is used the following error messages can occur:</span><a class="headerlink" href="#id255" title="Link to this table"></a></caption>
<colgroup>
<col style="width: 30.0%" />
<col style="width: 30.0%" />
<col style="width: 40.0%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Error message</p></th>
<th class="head"><p>Explanation</p></th>
<th class="head"><p>Example</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>Repeated point</p></td>
<td><p>This error happens when a given vertex is repeated.</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/geos_rep_point.png" src="../../../../_images/geos_rep_point.png" />
</figure>
</td>
</tr>
<tr class="row-odd"><td><p>Ring self-intersection</p></td>
<td><p>This error happens when a geometry touches itself and generates
a ring.</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/geos_ring_inter.png" src="../../../../_images/geos_ring_inter.png" />
</figure>
</td>
</tr>
<tr class="row-even"><td><p>Self-intersection</p></td>
<td><p>This error happens when a geometry touches itself.</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/geos_self_inter.png" src="../../../../_images/geos_self_inter.png" />
</figure>
</td>
</tr>
<tr class="row-odd"><td><p>Topology validation error</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-even"><td><p>Hole lies outside shell</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-odd"><td><p>Holes are nested</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-even"><td><p>Interior is disconnected</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-odd"><td><p>Nested shells</p></td>
<td><p>This error happens when a polygon geometry is on top of another
polygon geometry.</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/geos_nest_shell.png" src="../../../../_images/geos_nest_shell.png" />
</figure>
</td>
</tr>
<tr class="row-even"><td><p>Duplicate rings</p></td>
<td><p>This error happens when two rings (exterior or interior) of a
polygon geometry are identical</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/geos_dupl_rings.png" src="../../../../_images/geos_dupl_rings.png" />
</figure>
</td>
</tr>
<tr class="row-odd"><td><p>Too few points in geometry component</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-even"><td><p>Invalid coordinate</p></td>
<td><p>For a point geometry, this error happens when the geometry does
not have a proper coordinate pair.
The coordinate pair does not contain a latitude value and a
longitude value in that order.</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p>Ring is not closed</p></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
<table class="longtable docutils align-default" id="id256">
<caption><span class="caption-number">Table 28.2 </span><span class="caption-text">If the QGIS method is used the following error messages can occur:</span><a class="headerlink" href="#id256" title="Link to this table"></a></caption>
<colgroup>
<col style="width: 33.3%" />
<col style="width: 33.3%" />
<col style="width: 33.3%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Error message</p></th>
<th class="head"><p>Explanation</p></th>
<th class="head"><p>Example</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>Segment %1 of ring %2 of polygon %3 intersects segment %4
of ring %5 of polygon %6 at %7</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-odd"><td><p>Ring %1 with less than four points</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-even"><td><p>Ring %1 not closed</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-odd"><td><p>Line %1 with less than two points</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-even"><td><p>Line %1 contains %n duplicate node(s) at %2</p></td>
<td><p>This error happens when consecutive points on a line have the
same coordinates.</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/geos_rep_point.png" src="../../../../_images/geos_rep_point.png" />
</figure>
</td>
</tr>
<tr class="row-odd"><td><p>Segments %1 and %2 of line %3 intersect at %4</p></td>
<td><p>This error happens when a line self intersects (two segments
of the line intersect each other).</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/qgis_seg_line_int.png" src="../../../../_images/qgis_seg_line_int.png" />
</figure>
</td>
</tr>
<tr class="row-even"><td><p>Ring self-intersection</p></td>
<td><p>This error happens when an outer or inner (island) ring /
boundary of a polygon geometry intersects itself.</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/geos_ring_inter.png" src="../../../../_images/geos_ring_inter.png" />
</figure>
</td>
</tr>
<tr class="row-odd"><td><p>Ring %1 of polygon %2 not in exterior ring</p></td>
<td></td>
<td></td>
</tr>
<tr class="row-even"><td><p>Polygon %1 lies inside polygon %2</p></td>
<td><p>This error happens when a part of a MultiPolygon geometry is
inside a hole of a MultiPolygon geometry.</p></td>
<td><figure class="align-center">
<img alt="../../../../_images/qgis_poliinside_.png" src="../../../../_images/qgis_poliinside_.png" />
</figure>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="collect-geometries">
<span id="qgiscollect"></span><h2><a class="toc-backref" href="#id313" role="doc-backlink"><span class="section-number">28.1.22.9. </span>Collect geometries</a><a class="headerlink" href="#collect-geometries" title="Link to this heading"></a></h2>
<p>Takes a vector layer and collects its geometries into new multipart
geometries.</p>
<p>One or more attributes can be specified to collect only geometries
belonging to the same class (having the same value for the specified
attributes), alternatively all geometries can be collected.</p>
<p>All output geometries will be converted to multi geometries, even
those with just a single part.
This algorithm does not dissolve overlapping geometries - they will
be collected together without modifying the shape of each geometry
part.</p>
<p>See the ‘Promote to multipart’ or ‘Aggregate’ algorithms for
alternative options.</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisaggregate"><span class="std std-ref">Aggregate</span></a>, <a class="reference internal" href="#qgispromotetomulti"><span class="std std-ref">Promote to multipart</span></a>,
<a class="reference internal" href="#qgisdissolve"><span class="std std-ref">Dissolve</span></a></p>
</div>
<section id="id22">
<h3>Parameters<a class="headerlink" href="#id22" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Unique ID fields</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">FIELD</span></code></p></td>
<td><p>[tablefield: any] [list]</p></td>
<td><p>Choose one or more attributes to collect the geometries</p></td>
</tr>
<tr class="row-even"><td><p><strong>Collected</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Vector layer with collected geometries</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id23">
<h3>Outputs<a class="headerlink" href="#id23" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Collected</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer for the collected geometries.
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
<section id="id24">
<h3>Python code<a class="headerlink" href="#id24" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:collect</span></code></p>
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
<section id="concave-hull">
<span id="qgisconcavehull"></span><h2><a class="toc-backref" href="#id314" role="doc-backlink"><span class="section-number">28.1.22.10. </span>Concave hull</a><a class="headerlink" href="#concave-hull" title="Link to this heading"></a></h2>
<p>Computes the concave hull of the features from an input point layer.</p>
<figure class="align-center" id="id257">
<img alt="../../../../_images/concave_hull_threshold.png" src="../../../../_images/concave_hull_threshold.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.71 </span><span class="caption-text">Concave hulls with different thresholds (0.3, 0.6, 0.9)</span><a class="headerlink" href="#id257" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisconvexhull"><span class="std std-ref">Convex hull</span></a></p>
</div>
<section id="id25">
<h3>Parameters<a class="headerlink" href="#id25" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Input point layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>Input point vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Threshold</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ALPHA</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.3</p>
</td>
<td><p>Number from 0 (maximum concave hull) to 1 (convex hull).</p></td>
</tr>
<tr class="row-even"><td><p><strong>Allow holes</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HOLES</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: True</p>
</td>
<td><p>Choose whether to allow holes in the final concave hull</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Split multipart geometry into singlepart geometries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NO_MULTIGEOMETRY</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Check if you want to have singlepart geometries
instead of multipart ones.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Concave hull</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id26">
<h3>Outputs<a class="headerlink" href="#id26" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Concave hull</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id27">
<h3>Python code<a class="headerlink" href="#id27" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:concavehull</span></code></p>
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
<section id="convert-geometry-type">
<span id="qgisconvertgeometrytype"></span><h2><a class="toc-backref" href="#id315" role="doc-backlink"><span class="section-number">28.1.22.11. </span>Convert geometry type</a><a class="headerlink" href="#convert-geometry-type" title="Link to this heading"></a></h2>
<p>Generates a new layer based on an existing one, with a different type
of geometry.</p>
<p>The attribute table of the output layer is the same as the one of
the input layer.</p>
<p>Not all conversions are possible. For instance, a line layer
can be converted to a point layer, but a point layer cannot
be converted to a line layer.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgispolygonize"><span class="std std-ref">Polygonize</span></a>, <a class="reference internal" href="#qgislinestopolygons"><span class="std std-ref">Lines to polygons</span></a>, <a class="reference internal" href="#qgispolygonstolines"><span class="std std-ref">Polygons to lines</span></a>,
<a class="reference internal" href="vectorcreation.html#qgispointstopath"><span class="std std-ref">Points to path</span></a></p>
</div>
<section id="id28">
<h3>Parameters<a class="headerlink" href="#id28" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>New geometry type</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TYPE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Geometry type to apply to the output features.
One of:</p>
<ul class="simple">
<li><p>0 — Centroids</p></li>
<li><p>1 — Nodes</p></li>
<li><p>2 — Linestrings</p></li>
<li><p>3 — Multilinestrings</p></li>
<li><p>4 — Polygons</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Converted</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: any]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer.
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
<section id="id29">
<h3>Outputs<a class="headerlink" href="#id29" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Converted</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: any]</p></td>
<td><p>Output vector layer - the type depends on the parameters</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id30">
<h3>Python code<a class="headerlink" href="#id30" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:convertgeometrytype</span></code></p>
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
<section id="convert-to-curved-geometries">
<span id="qgisconverttocurves"></span><h2><a class="toc-backref" href="#id316" role="doc-backlink"><span class="section-number">28.1.22.12. </span>Convert to curved geometries</a><a class="headerlink" href="#convert-to-curved-geometries" title="Link to this heading"></a></h2>
<p>Converts a geometry into its curved geometry equivalent.</p>
<p>Already curved geometries will be retained without change.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features</p>
<section id="id31">
<h3>Parameters<a class="headerlink" href="#id31" title="Link to this heading"></a></h3>
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
<td><p>[vector: line or polygon]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum distance tolerance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.000001</p>
</td>
<td><p>The maximum distance allowed between the original location of vertices
and where they would fall on the converted curved geometries</p></td>
</tr>
<tr class="row-even"><td><p><strong>Maximum angle tolerance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ANGLE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.000001</p>
</td>
<td><p>Segments are considered as suitable for replacing with an arc
if the points are all regularly spaced on the candidate arc.
This parameter specifies the maximum angular deviation (in degrees)
allowed when testing for regular point spacing. Between 0 and 45°.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Curves</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: compoundcurve or curvepolygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer.
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
<section id="id32">
<h3>Outputs<a class="headerlink" href="#id32" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Curves</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: compoundcurve or curvepolygon]</p></td>
<td><p>Output vector layer with curved geometries</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id33">
<h3>Python code<a class="headerlink" href="#id33" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:converttocurves</span></code></p>
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
<section id="convex-hull">
<span id="qgisconvexhull"></span><h2><a class="toc-backref" href="#id317" role="doc-backlink"><span class="section-number">28.1.22.13. </span>Convex hull</a><a class="headerlink" href="#convex-hull" title="Link to this heading"></a></h2>
<p>Calculates the convex hull for each feature in an input layer.</p>
<p>See the ‘Minimum bounding geometry’ algorithm for a convex hull
calculation which covers the whole layer or grouped subsets of
features.</p>
<figure class="align-center" id="id258">
<img alt="../../../../_images/convex_hull.png" src="../../../../_images/convex_hull.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.72 </span><span class="caption-text">Black lines identify the convex hull for each layer feature</span><a class="headerlink" href="#id258" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geoprocessing Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisminimumboundinggeometry"><span class="std std-ref">Minimum bounding geometry</span></a>,
<a class="reference internal" href="#qgisconcavehull"><span class="std std-ref">Concave hull</span></a></p>
</div>
<section id="id34">
<h3>Parameters<a class="headerlink" href="#id34" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Convex hull</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id35">
<h3>Outputs<a class="headerlink" href="#id35" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Convex hull</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output (convex hull) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id36">
<h3>Python code<a class="headerlink" href="#id36" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:convexhull</span></code></p>
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
<section id="create-layer-from-extent">
<span id="qgisextenttolayer"></span><h2><a class="toc-backref" href="#id318" role="doc-backlink"><span class="section-number">28.1.22.14. </span>Create layer from extent</a><a class="headerlink" href="#create-layer-from-extent" title="Link to this heading"></a></h2>
<p>Creates a new vector layer that contains a single feature with
geometry matching the extent of the input layer.</p>
<p>It can be used in models to convert a literal extent (<code class="docutils literal notranslate"><span class="pre">xmin</span></code>,
<code class="docutils literal notranslate"><span class="pre">xmax</span></code>, <code class="docutils literal notranslate"><span class="pre">ymin</span></code>, <code class="docutils literal notranslate"><span class="pre">ymax</span></code> format) into a layer which can be used
for other algorithms which require a layer based input.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgispointtolayer"><span class="std std-ref">Create layer from point</span></a></p>
</div>
<section id="id37">
<h3>Parameters<a class="headerlink" href="#id37" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Extent (xmin, xmax, ymin, ymax)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[extent]</p></td>
<td><p>Input extent</p>
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
<tr class="row-odd"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id38">
<h3>Outputs<a class="headerlink" href="#id38" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Extent</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output (extent) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id39">
<h3>Python code<a class="headerlink" href="#id39" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:extenttolayer</span></code></p>
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
<section id="create-layer-from-point">
<span id="qgispointtolayer"></span><h2><a class="toc-backref" href="#id319" role="doc-backlink"><span class="section-number">28.1.22.15. </span>Create layer from point</a><a class="headerlink" href="#create-layer-from-point" title="Link to this heading"></a></h2>
<p>Creates a new vector layer that contains a single feature with
geometry matching a point parameter.
It can be used in models to convert a point into a point layer for
algorithms which require a layer based input.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisextenttolayer"><span class="std std-ref">Create layer from extent</span></a></p>
</div>
<section id="id40">
<h3>Parameters<a class="headerlink" href="#id40" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Point</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[coordinates]</p></td>
<td><p>Input point, including CRS info
(example: <code class="docutils literal notranslate"><span class="pre">397254,6214446</span> <span class="pre">[EPSG:32632]</span></code>).</p>
<p>If the CRS is not provided, the Project CRS will be used.</p>
<p>The point can be specified by clicking on the map canvas.</p>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Point</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output layer.
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
<section id="id41">
<h3>Outputs<a class="headerlink" href="#id41" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Point</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output point vector layer containing the input point.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id42">
<h3>Python code<a class="headerlink" href="#id42" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:pointtolayer</span></code></p>
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
<section id="create-wedge-buffers">
<span id="qgiswedgebuffers"></span><h2><a class="toc-backref" href="#id320" role="doc-backlink"><span class="section-number">28.1.22.16. </span>Create wedge buffers</a><a class="headerlink" href="#create-wedge-buffers" title="Link to this heading"></a></h2>
<p>Creates wedge shaped buffers from input points.</p>
<figure class="align-center" id="id259">
<img alt="../../../../_images/wedge_buffers.png" src="../../../../_images/wedge_buffers.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.73 </span><span class="caption-text">Wedge buffers</span><a class="headerlink" href="#id259" title="Link to this image"></a></p>
</figcaption>
</figure>
<p>The native output from this algorithm are CurvePolygon geometries,
but these may be automatically segmentized to Polygons depending
on the output format.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisbuffer"><span class="std std-ref">Buffer</span></a>, <a class="reference internal" href="#qgisbufferbym"><span class="std std-ref">Variable width buffer (by M value)</span></a>,
<a class="reference internal" href="#qgistaperedbuffer"><span class="std std-ref">Tapered buffers</span></a></p>
</div>
<section id="id43">
<h3>Parameters<a class="headerlink" href="#id43" title="Link to this heading"></a></h3>
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
<td><p>[vector: point]</p></td>
<td><p>Input point vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Azimuth (degrees from North)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">AZIMUTH</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Angle (in degrees) as the middle value of the wedge</p></td>
</tr>
<tr class="row-even"><td><p><strong>Wedge width (in degrees)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 45.0</p>
</td>
<td><p>Width (in degrees) of the buffer.
The wedge will extend to half of the angular width either side
of the azimuth direction.</p>
<figure class="align-center" id="id260">
<img alt="../../../../_images/wedge_buffers_azimuth_width.png" src="../../../../_images/wedge_buffers_azimuth_width.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.74 </span><span class="caption-text">Azimuth and width values of the wedge buffer</span><a class="headerlink" href="#id260" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Outer radius</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTER_RADIUS</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>The outer <em>size</em> (length) of the wedge:
the size is meant from the source point to the edge of the
wedge shape.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Inner radius</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">INNER_RADIUS</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Inner radius value.
If 0 the wedge will begin from the source point.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Buffers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<tr class="row-even"><td><p><strong>Buffers</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output (wedge buffer) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id45">
<h3>Python code<a class="headerlink" href="#id45" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:wedgebuffers</span></code></p>
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
<section id="delaunay-triangulation">
<span id="qgisdelaunaytriangulation"></span><h2><a class="toc-backref" href="#id321" role="doc-backlink"><span class="section-number">28.1.22.17. </span>Delaunay triangulation</a><a class="headerlink" href="#delaunay-triangulation" title="Link to this heading"></a></h2>
<p>Creates a polygon layer with the Delaunay triangulation corresponding
to the input point layer.</p>
<figure class="align-center" id="id261">
<img alt="../../../../_images/delaunay.png" src="../../../../_images/delaunay.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.75 </span><span class="caption-text">Delaunay triangulation on points</span><a class="headerlink" href="#id261" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<section id="id46">
<h3>Parameters<a class="headerlink" href="#id46" title="Link to this heading"></a></h3>
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
<td><p>[vector: point]</p></td>
<td><p>Input point vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Tolerance</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOLERANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.0</p>
</td>
<td><p>Specifies an optional snapping tolerance which can be used to improve the robustness of the triangulation.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Add point IDs to output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ADD_ATTRIBUTES</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: True</p>
</td>
<td><p>Specifies whether fields storing involved point features ID should be added to the output.
If False, an <code class="docutils literal notranslate"><span class="pre">id</span></code> field is used to identify the polygons.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Delaunay triangulation</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id47">
<h3>Outputs<a class="headerlink" href="#id47" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Delaunay triangulation</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output (Delaunay triangulation) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id48">
<h3>Python code<a class="headerlink" href="#id48" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:delaunaytriangulation</span></code></p>
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
<section id="delete-holes">
<span id="qgisdeleteholes"></span><h2><a class="toc-backref" href="#id322" role="doc-backlink"><span class="section-number">28.1.22.18. </span>Delete holes</a><a class="headerlink" href="#delete-holes" title="Link to this heading"></a></h2>
<p>Takes a polygon layer and removes holes in polygons.
It creates a new vector layer in which polygons with holes have been
replaced by polygons with only their external ring.
Attributes are not modified.</p>
<p>An optional minimum area parameter allows removing only holes which
are smaller than a specified area threshold. Leaving this parameter at
<code class="docutils literal notranslate"><span class="pre">0.0</span></code> results in all holes being removed.</p>
<figure class="align-center" id="id262">
<img alt="../../../../_images/delete_holes.png" src="../../../../_images/delete_holes.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.76 </span><span class="caption-text">Before and after the cleaning</span><a class="headerlink" href="#id262" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<section id="id49">
<h3>Parameters<a class="headerlink" href="#id49" title="Link to this heading"></a></h3>
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
<td><p>[vector: polygon]</p></td>
<td><p>Input polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Remove holes with area less than</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">MIN_AREA</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Only holes with an area less than this threshold will be
deleted.
With a value of <code class="docutils literal notranslate"><span class="pre">0.0</span></code>, <strong>all</strong> the holes will be deleted.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Cleaned</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id50">
<h3>Outputs<a class="headerlink" href="#id50" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Cleaned</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output (cleaned) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id51">
<h3>Python code<a class="headerlink" href="#id51" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:deleteholes</span></code></p>
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
<section id="densify-by-count">
<span id="qgisdensifygeometries"></span><h2><a class="toc-backref" href="#id323" role="doc-backlink"><span class="section-number">28.1.22.19. </span>Densify by count</a><a class="headerlink" href="#densify-by-count" title="Link to this heading"></a></h2>
<p>Takes a polygon or line layer and generates a new one in which the
geometries have a larger number of vertices than the original one.</p>
<p>If the geometries have Z or M values present then these will be
linearly interpolated at the added vertices.</p>
<p>The number of new vertices to add to each segment is specified as an
input parameter.</p>
<figure class="align-center" id="id263">
<img alt="../../../../_images/densify_geometry.png" src="../../../../_images/densify_geometry.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.77 </span><span class="caption-text">Red points show the vertices before and after the densify</span><a class="headerlink" href="#id263" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisdensifygeometriesgivenaninterval"><span class="std std-ref">Densify by interval</span></a></p>
</div>
<section id="id52">
<h3>Parameters<a class="headerlink" href="#id52" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Vertices to add</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VERTICES</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1</p>
</td>
<td><p>Number of vertices to add to each segment</p></td>
</tr>
<tr class="row-even"><td><p><strong>Densified</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id53">
<h3>Outputs<a class="headerlink" href="#id53" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Densified</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output (densified) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id54">
<h3>Python code<a class="headerlink" href="#id54" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:densifygeometries</span></code></p>
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
<section id="densify-by-interval">
<span id="qgisdensifygeometriesgivenaninterval"></span><h2><a class="toc-backref" href="#id324" role="doc-backlink"><span class="section-number">28.1.22.20. </span>Densify by interval</a><a class="headerlink" href="#densify-by-interval" title="Link to this heading"></a></h2>
<p>Takes a polygon or line layer and generates a new one in which the
geometries have a larger number of vertices than the original one.</p>
<p>The geometries are densified by adding regularly placed extra
vertices inside each segment so that the maximum distance between
any two vertices does not exceed the specified distance.</p>
<p>If the geometries have Z or M values present then these will be
linearly interpolated at the added vertices.</p>
<p><strong>Example</strong></p>
<p>Specifying a distance of 3 would cause the segment
<code class="docutils literal notranslate"><span class="pre">[0</span> <span class="pre">0]</span> <span class="pre">-&gt;</span> <span class="pre">[10</span> <span class="pre">0]</span></code> to be converted to
<code class="docutils literal notranslate"><span class="pre">[0</span> <span class="pre">0]</span> <span class="pre">-&gt;</span> <span class="pre">[2.5</span> <span class="pre">0]</span> <span class="pre">-&gt;</span> <span class="pre">[5</span> <span class="pre">0]</span> <span class="pre">-&gt;</span> <span class="pre">[7.5</span> <span class="pre">0]</span> <span class="pre">-&gt;</span> <span class="pre">[10</span> <span class="pre">0]</span></code>,
since 3 extra vertices are required on the segment and spacing these
at 2.5 increments allows them to be evenly spaced over the segment.</p>
<figure class="align-center" id="id264">
<img alt="../../../../_images/densify_geometry_interval.png" src="../../../../_images/densify_geometry_interval.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.78 </span><span class="caption-text">Densify geometry at a given interval</span><a class="headerlink" href="#id264" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisdensifygeometries"><span class="std std-ref">Densify by count</span></a></p>
</div>
<section id="id55">
<h3>Parameters<a class="headerlink" href="#id55" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Interval between vertices to add</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INTERVAL</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Maximum distance between two consecutive vertices</p></td>
</tr>
<tr class="row-even"><td><p><strong>Densified</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id56">
<h3>Outputs<a class="headerlink" href="#id56" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Densified</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output (densified) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id57">
<h3>Python code<a class="headerlink" href="#id57" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:densifygeometriesgivenaninterval</span></code></p>
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
<section id="dissolve">
<span id="qgisdissolve"></span><h2><a class="toc-backref" href="#id325" role="doc-backlink"><span class="section-number">28.1.22.21. </span>Dissolve</a><a class="headerlink" href="#dissolve" title="Link to this heading"></a></h2>
<p>Takes a vector layer and combines its features into new features.
One or more attributes can be specified to dissolve features
belonging to the same class (having the same value for the specified
attributes), alternatively all features can be dissolved to a single
feature.</p>
<p>All output geometries will be converted to multi geometries.
In case the input is a polygon layer, common boundaries of adjacent
polygons being dissolved will get erased.
If enabled, the optional “Keep disjoint features separate” setting will
cause features and parts that do not overlap or touch to be exported as
separate features (instead of parts of a single multipart feature).</p>
<p>The resulting attribute table will have the same fields as the input
layer.
The values in the output layer’s fields are the ones of the first
input feature that happens to be processed.</p>
<figure class="align-center" id="id265">
<img alt="../../../../_images/dissolve.png" src="../../../../_images/dissolve.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.79 </span><span class="caption-text">Dissolving a layer into a single multipart feature</span><a class="headerlink" href="#id265" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geoprocessing Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisaggregate"><span class="std std-ref">Aggregate</span></a>, <a class="reference internal" href="#qgiscollect"><span class="std std-ref">Collect geometries</span></a></p>
</div>
<section id="id58">
<h3>Parameters<a class="headerlink" href="#id58" title="Link to this heading"></a></h3>
<section id="id59">
<h4>Basic parameters<a class="headerlink" href="#id59" title="Link to this heading"></a></h4>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Dissolve field(s)</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">FIELD</span></code></p></td>
<td><p>[tablefield: any] [list]</p>
<p>Default: []</p>
</td>
<td><p>Features having the same value for the
selected field(s) will be replaced with a
single one and their geometries are merged.</p>
<p>If no field is provided then all the
features are dissolved, resulting in a
single (multipart) feature.</p>
<figure class="align-center" id="id266">
<img alt="../../../../_images/dissolve_field.png" src="../../../../_images/dissolve_field.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.80 </span><span class="caption-text">Dissolve the polygon layer on a common attribute (2 multipart features)</span><a class="headerlink" href="#id266" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-even"><td><p><strong>Dissolved</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id60">
<h4>Advanced parameters<a class="headerlink" href="#id60" title="Link to this heading"></a></h4>
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
<tr class="row-even"><td><p><strong>Keep disjoint features separate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEPARATE_DISJOINT</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Parts of dissolved features are exported as separate features
(instead of parts of a multipart feature).</p>
<figure class="align-center" id="id267">
<img alt="../../../../_images/dissolve_disjoint.png" src="../../../../_images/dissolve_disjoint.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.81 </span><span class="caption-text">source (left), dissolve all (3 distinct features - right)</span><a class="headerlink" href="#id267" title="Link to this image"></a></p>
</figcaption>
</figure>
<figure class="align-center" id="id268">
<img alt="../../../../_images/dissolve_disjoint_field.png" src="../../../../_images/dissolve_disjoint_field.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.82 </span><span class="caption-text">source (left), dissolve on field (5 distinct features - right)</span><a class="headerlink" href="#id268" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
</tbody>
</table>
</section>
</section>
<section id="id61">
<h3>Outputs<a class="headerlink" href="#id61" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Dissolved</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer with dissolved geometries</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id62">
<h3>Python code<a class="headerlink" href="#id62" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:dissolve</span></code></p>
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
<section id="drape-set-z-value-from-raster">
<span id="qgissetzfromraster"></span><h2><a class="toc-backref" href="#id326" role="doc-backlink"><span class="section-number">28.1.22.22. </span>Drape (set Z value from raster)</a><a class="headerlink" href="#drape-set-z-value-from-raster" title="Link to this heading"></a></h2>
<p>Uses values sampled from a band within a raster layer to set the Z
value for every overlapping vertex in the feature geometry.
The raster values can optionally be scaled by a preset amount.</p>
<p>If Z values already exist in the layer, they will be overwritten with
the new value.
If no Z values exist, the geometry will be upgraded to include the Z
dimension.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features with Z enabled</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissetmfromraster"><span class="std std-ref">Set M value from raster</span></a>, <a class="reference internal" href="#qgissetzvalue"><span class="std std-ref">Set Z value</span></a></p>
</div>
<section id="id63">
<h3>Parameters<a class="headerlink" href="#id63" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Raster layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Raster layer with Z values</p></td>
</tr>
<tr class="row-even"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: 1</p>
</td>
<td><p>The raster band to take the Z values from</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Value for NoData or non-intersecting vertices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0</p>
</td>
<td><p>Value to use in case the vertex does not intersect
(a valid pixel of) the raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Scale factor</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SCALE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Scaling value: the band values are multiplied
by this value.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Offset</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OFFSET</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Offset value: it is algebraically added to the band
values after applying the “Scale factor”.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Updated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer (with Z values
from the raster layer). One of:</p>
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
<section id="id64">
<h3>Outputs<a class="headerlink" href="#id64" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Updated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer with Z values from the
raster layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id65">
<h3>Python code<a class="headerlink" href="#id65" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:setzfromraster</span></code></p>
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
<section id="drop-m-z-values">
<span id="qgisdropmzvalues"></span><h2><a class="toc-backref" href="#id327" role="doc-backlink"><span class="section-number">28.1.22.23. </span>Drop M/Z values</a><a class="headerlink" href="#drop-m-z-values" title="Link to this heading"></a></h2>
<p>Removes M (measure) or Z (altitude) values from input geometries.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissetmvalue"><span class="std std-ref">Set M value</span></a>, <a class="reference internal" href="#qgissetzvalue"><span class="std std-ref">Set Z value</span></a></p>
</div>
<section id="id66">
<h3>Parameters<a class="headerlink" href="#id66" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer with M or Z values</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Drop M Values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DROP_M_VALUES</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Removes the M values from the geometries</p></td>
</tr>
<tr class="row-even"><td><p><strong>Drop Z Values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DROP_Z_VALUES</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Removes the Z values from the geometries</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Z/M Dropped</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id67">
<h3>Outputs<a class="headerlink" href="#id67" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Z/M Dropped</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (identical to the input layer,
except that the M and/or Z dimensions have been removed
from the geometries).</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id68">
<h3>Python code<a class="headerlink" href="#id68" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:dropmzvalues</span></code></p>
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
<section id="eliminate-selected-polygons">
<span id="qgiseliminateselectedpolygons"></span><h2><a class="toc-backref" href="#id328" role="doc-backlink"><span class="section-number">28.1.22.24. </span>Eliminate selected polygons</a><a class="headerlink" href="#eliminate-selected-polygons" title="Link to this heading"></a></h2>
<p>Combines selected polygons of the input layer with certain adjacent
polygons by erasing their common boundary.
The adjacent polygon can be either the one with the largest or
smallest area or the one sharing the largest common boundary with the
polygon to be eliminated.</p>
<p>Eliminate is normally used to get rid of sliver polygons, i.e. tiny
polygons that are a result of polygon intersection processes where
boundaries of the inputs are similar but not identical.</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geoprocessing Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfixgeometries"><span class="std std-ref">Fix geometries</span></a></p>
</div>
<section id="id69">
<h3>Parameters<a class="headerlink" href="#id69" title="Link to this heading"></a></h3>
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
<td><p>[vector: polygon]</p></td>
<td><p>Input polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Merge selection with the neighboring polygon with the</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MODE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: None</p>
</td>
<td><p>Choose the parameter to use in order to get rid of
the selected polygons:</p>
<ul class="simple">
<li><p>0 — Largest Area</p></li>
<li><p>1 — Smallest Area</p></li>
<li><p>2 — Largest Common Boundary</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Eliminated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id70">
<h3>Outputs<a class="headerlink" href="#id70" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Eliminated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output polygon vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id71">
<h3>Python code<a class="headerlink" href="#id71" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:eliminateselectedpolygons</span></code></p>
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
<section id="explode-lines">
<span id="qgisexplodelines"></span><h2><a class="toc-backref" href="#id329" role="doc-backlink"><span class="section-number">28.1.22.25. </span>Explode lines</a><a class="headerlink" href="#explode-lines" title="Link to this heading"></a></h2>
<p>Takes a lines layer and creates a new one in which each line layer is
replaced by a set of lines representing the segments in the original
line.</p>
<p>Each line in the resulting layer contains only a start and an end
point, with no intermediate vertices between them.</p>
<figure class="align-center" id="id269">
<img alt="../../../../_images/explode_lines.png" src="../../../../_images/explode_lines.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.83 </span><span class="caption-text">The original line layer and the exploded one</span><a class="headerlink" href="#id269" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissubdivide"><span class="std std-ref">Subdivide</span></a>, <a class="reference internal" href="#qgislinesubstring"><span class="std std-ref">Line substring</span></a></p>
</div>
<section id="id72">
<h3>Parameters<a class="headerlink" href="#id72" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Exploded</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id73">
<h3>Outputs<a class="headerlink" href="#id73" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Exploded</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The output line vector layer with features representing
each segment of the input layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id74">
<h3>Python code<a class="headerlink" href="#id74" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:explodelines</span></code></p>
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
<section id="extend-lines">
<span id="qgisextendlines"></span><h2><a class="toc-backref" href="#id330" role="doc-backlink"><span class="section-number">28.1.22.26. </span>Extend lines</a><a class="headerlink" href="#extend-lines" title="Link to this heading"></a></h2>
<p>Extends line geometry by a specified amount at the start and end of
the line.</p>
<p>Lines are extended using the bearing of the first and last segment in
the line.</p>
<figure class="align-center" id="id270">
<img alt="../../../../_images/extend_lines.png" src="../../../../_images/extend_lines.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.84 </span><span class="caption-text">The red dashes represent the initial and final extension of the
original layer</span><a class="headerlink" href="#id270" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgislinesubstring"><span class="std std-ref">Line substring</span></a></p>
</div>
<section id="id75">
<h3>Parameters<a class="headerlink" href="#id75" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Start distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">START_DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p></td>
<td><p>Distance by which to extend the first segment of the line
(starting point)</p></td>
</tr>
<tr class="row-even"><td><p><strong>End distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">END_DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p></td>
<td><p>Distance by which to extend the last segment of the line
(ending point)</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Extended</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id76">
<h3>Outputs<a class="headerlink" href="#id76" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Extended</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The output (extended) line vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id77">
<h3>Python code<a class="headerlink" href="#id77" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:extendlines</span></code></p>
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
<section id="extract-m-values">
<span id="qgisextractmvalues"></span><h2><a class="toc-backref" href="#id331" role="doc-backlink"><span class="section-number">28.1.22.27. </span>Extract M values</a><a class="headerlink" href="#extract-m-values" title="Link to this heading"></a></h2>
<p>Extracts M values from geometries into feature attributes.</p>
<p>By default only the M value from the first vertex of each feature is
extracted, however the algorithm can optionally calculate statistics
on all of the geometry’s M values, including sum, mean, minimum and
maximum.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisextractzvalues"><span class="std std-ref">Extract Z values</span></a>, <a class="reference internal" href="#qgissetmvalue"><span class="std std-ref">Set M value</span></a>, <a class="reference internal" href="#qgisdropmzvalues"><span class="std std-ref">Drop M/Z values</span></a></p>
</div>
<section id="id78">
<h3>Parameters<a class="headerlink" href="#id78" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Summaries to calculate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SUMMARIES</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: [0]</p>
</td>
<td><p>Statistics on the M values of a geometry.
One or more of:</p>
<ul class="simple">
<li><p>0 — First</p></li>
<li><p>1 — Last</p></li>
<li><p>2 — Count</p></li>
<li><p>3 — Sum</p></li>
<li><p>4 — Mean</p></li>
<li><p>5 — Median</p></li>
<li><p>6 — St.dev (pop)</p></li>
<li><p>7 — Minimum</p></li>
<li><p>8 — Maximum</p></li>
<li><p>9 — Range</p></li>
<li><p>10 — Minority</p></li>
<li><p>11 — Majority</p></li>
<li><p>12 — Variety</p></li>
<li><p>13 — Q1</p></li>
<li><p>14 — Q3</p></li>
<li><p>15 — IQR</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Output column prefix</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">COLUMN_PREFIX</span></code></p></td>
<td><p>[string]</p>
<p>Default: ‘m_’</p>
</td>
<td><p>The prefix for the output (M) column</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Extracted</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output layer.
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
<section id="id79">
<h3>Outputs<a class="headerlink" href="#id79" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Extracted</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (with M values)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id80">
<h3>Python code<a class="headerlink" href="#id80" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:extractmvalues</span></code></p>
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
<section id="extract-specific-vertices">
<span id="qgisextractspecificvertices"></span><h2><a class="toc-backref" href="#id332" role="doc-backlink"><span class="section-number">28.1.22.28. </span>Extract specific vertices</a><a class="headerlink" href="#extract-specific-vertices" title="Link to this heading"></a></h2>
<p>Takes a vector layer and generates a point layer with points
representing specific vertices in the input geometries.</p>
<p>For instance, this algorithm can be used to extract the first or last
vertices in the geometry.
The attributes associated to each point are the same ones associated
to the feature that the vertex belongs to.</p>
<p>The vertex indices parameter accepts a comma separated string
specifying the indices of the vertices to extract.
The first vertex corresponds to an index of 0, the second vertex has
an index of 1, etc. Negative indices can be used to find vertices at
the end of the geometry, e.g., an index of -1 corresponds to the last
vertex, -2 corresponds to the second last vertex, etc.</p>
<p>Additional fields are added to the vertices indicating the specific
vertex position (e.g., 0, -1, etc), the original vertex index, the
vertex’s part and its index within the part (as well as its ring for
polygons), distance along the original geometry and bisector angle of
vertex for the original geometry.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisextractvertices"><span class="std std-ref">Extract vertices</span></a>, <a class="reference internal" href="#qgisfilterverticesbym"><span class="std std-ref">Filter vertices by M value</span></a>,
<a class="reference internal" href="#qgisfilterverticesbyz"><span class="std std-ref">Filter vertices by Z value</span></a></p>
</div>
<section id="id81">
<h3>Parameters<a class="headerlink" href="#id81" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Vertex indices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VERTICES</span></code></p></td>
<td><p>[string]</p>
<p>Default: ‘0’</p>
</td>
<td><p>Comma-separated string of the indices of the vertices to
extract.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Vertices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id82">
<h3>Outputs<a class="headerlink" href="#id82" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Vertices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output (point) vector layer containing the specified
vertices from the input layer geometries.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id83">
<h3>Python code<a class="headerlink" href="#id83" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:extractspecificvertices</span></code></p>
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
<section id="extract-vertices">
<span id="qgisextractvertices"></span><h2><a class="toc-backref" href="#id333" role="doc-backlink"><span class="section-number">28.1.22.29. </span>Extract vertices</a><a class="headerlink" href="#extract-vertices" title="Link to this heading"></a></h2>
<p>Takes a vector layer and generates a point layer with points
representing the vertices in the input geometries.</p>
<p>The attributes associated to each point are the same ones associated
to the feature that the vertex belongs to.</p>
<p>Additional fields are added to the vertices indicating the vertex
index (beginning at 0), the feature’s part and its index within the
part (as well as its ring for polygons), distance along original
geometry and bisector angle of vertex for original geometry.</p>
<figure class="align-center" id="id271">
<img alt="../../../../_images/extract_nodes.png" src="../../../../_images/extract_nodes.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.85 </span><span class="caption-text">Vertices extracted for line and polygon layer</span><a class="headerlink" href="#id271" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point features</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisextractspecificvertices"><span class="std std-ref">Extract specific vertices</span></a>,
<a class="reference internal" href="#qgisfilterverticesbym"><span class="std std-ref">Filter vertices by M value</span></a>, <a class="reference internal" href="#qgisfilterverticesbyz"><span class="std std-ref">Filter vertices by Z value</span></a></p>
</div>
<section id="id84">
<h3>Parameters<a class="headerlink" href="#id84" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Vertices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id85">
<h3>Outputs<a class="headerlink" href="#id85" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Vertices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output (point) vector layer containing the vertices from
the input layer geometries.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id86">
<h3>Python code<a class="headerlink" href="#id86" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:extractvertices</span></code></p>
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
<section id="extract-z-values">
<span id="qgisextractzvalues"></span><h2><a class="toc-backref" href="#id334" role="doc-backlink"><span class="section-number">28.1.22.30. </span>Extract Z values</a><a class="headerlink" href="#extract-z-values" title="Link to this heading"></a></h2>
<p>Extracts Z values from geometries into feature attributes.</p>
<p>By default only the Z value from the first vertex of each feature is
extracted, however the algorithm can optionally calculate statistics
on all of the geometry’s Z values, including sum, mean, minimum and
maximum.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisextractmvalues"><span class="std std-ref">Extract M values</span></a>, <a class="reference internal" href="#qgissetzvalue"><span class="std std-ref">Set Z value</span></a>,
<a class="reference internal" href="#qgisdropmzvalues"><span class="std std-ref">Drop M/Z values</span></a></p>
</div>
<section id="id87">
<h3>Parameters<a class="headerlink" href="#id87" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Summaries to calculate</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SUMMARIES</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: [0]</p>
</td>
<td><p>Statistics on the Z values of a geometry.
One or more of:</p>
<ul class="simple">
<li><p>0 — First</p></li>
<li><p>1 — Last</p></li>
<li><p>2 — Count</p></li>
<li><p>3 — Sum</p></li>
<li><p>4 — Mean</p></li>
<li><p>5 — Median</p></li>
<li><p>6 — St.dev (pop)</p></li>
<li><p>7 — Minimum</p></li>
<li><p>8 — Maximum</p></li>
<li><p>9 — Range</p></li>
<li><p>10 — Minority</p></li>
<li><p>11 — Majority</p></li>
<li><p>12 — Variety</p></li>
<li><p>13 — Q1</p></li>
<li><p>14 — Q3</p></li>
<li><p>15 — IQR</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Output column prefix</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">COLUMN_PREFIX</span></code></p></td>
<td><p>[string]</p>
<p>Default: ‘z_’</p>
</td>
<td><p>The prefix for the output (Z) column</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Extracted</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output layer.
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
<section id="id88">
<h3>Outputs<a class="headerlink" href="#id88" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Extracted</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (with Z values)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id89">
<h3>Python code<a class="headerlink" href="#id89" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:extractzvalues</span></code></p>
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
<section id="filter-vertices-by-m-value">
<span id="qgisfilterverticesbym"></span><h2><a class="toc-backref" href="#id335" role="doc-backlink"><span class="section-number">28.1.22.31. </span>Filter vertices by M value</a><a class="headerlink" href="#filter-vertices-by-m-value" title="Link to this heading"></a></h2>
<p>Filters away vertices based on their M value, returning geometries
with only vertex points that have a M value greater than or equal to
the specified minimum value and/or less than or equal to the maximum
value.</p>
<p>If the minimum value is not specified then only the maximum value is
tested, and similarly if the maximum value is not specified then only
the minimum value is tested.</p>
<figure class="align-center" id="id272">
<img alt="../../../../_images/filter_zm.png" src="../../../../_images/filter_zm.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.86 </span><span class="caption-text">The red line represents the black line with only vertices whose M
value is &lt;=10.</span><a class="headerlink" href="#id272" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features with M enabled</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Depending on the input geometry attributes and the filters
used, the resultant geometries created by this algorithm may no
longer be valid.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfilterverticesbyz"><span class="std std-ref">Filter vertices by Z value</span></a>, <a class="reference internal" href="#qgisextractvertices"><span class="std std-ref">Extract vertices</span></a>,
<a class="reference internal" href="#qgisextractspecificvertices"><span class="std std-ref">Extract specific vertices</span></a></p>
</div>
<section id="id90">
<h3>Parameters<a class="headerlink" href="#id90" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer
to remove vertices from</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Minimum</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">MIN</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: <em>Not set</em></p>
</td>
<td><p>Minimum of M values allowed</p></td>
</tr>
<tr class="row-even"><td><p><strong>Maximum</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAX</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: <em>Not set</em></p>
</td>
<td><p>Maximum of M values allowed</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Filtered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id91">
<h3>Outputs<a class="headerlink" href="#id91" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Filtered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer of features
with only the filtered vertices.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id92">
<h3>Python code<a class="headerlink" href="#id92" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:filterverticesbym</span></code></p>
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
<section id="filter-vertices-by-z-value">
<span id="qgisfilterverticesbyz"></span><h2><a class="toc-backref" href="#id336" role="doc-backlink"><span class="section-number">28.1.22.32. </span>Filter vertices by Z value</a><a class="headerlink" href="#filter-vertices-by-z-value" title="Link to this heading"></a></h2>
<p>Filters away vertices based on their Z value, returning geometries
with only vertex points that have a Z value greater than or equal to
the specified minimum value and/or less than or equal to the maximum
value.</p>
<p>If the minimum value is not specified then only the maximum value is
tested, and similarly if the maximum value is not specified then only
the minimum value is tested.</p>
<figure class="align-center" id="id273">
<img alt="../../../../_images/filter_zm.png" src="../../../../_images/filter_zm.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.87 </span><span class="caption-text">The red line represents the black line with only vertices whose Z
value is &lt;=10.</span><a class="headerlink" href="#id273" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features with Z enabled</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Depending on the input geometry attributes and the filters
used, the resultant geometries created by this algorithm may no
longer be valid.
You may need to run the <a class="reference internal" href="#qgisfixgeometries"><span class="std std-ref">Fix geometries</span></a> algorithm to
ensure their validity.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisfilterverticesbym"><span class="std std-ref">Filter vertices by M value</span></a>, <a class="reference internal" href="#qgisextractvertices"><span class="std std-ref">Extract vertices</span></a>,
<a class="reference internal" href="#qgisextractspecificvertices"><span class="std std-ref">Extract specific vertices</span></a></p>
</div>
<section id="id93">
<h3>Parameters<a class="headerlink" href="#id93" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer
to remove vertices from</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Minimum</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">MIN</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: <em>Not set</em></p>
</td>
<td><p>Minimum of Z values allowed</p></td>
</tr>
<tr class="row-even"><td><p><strong>Maximum</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAX</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: <em>Not set</em></p>
</td>
<td><p>Maximum of Z values allowed</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Filtered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id94">
<h3>Outputs<a class="headerlink" href="#id94" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Filtered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer of features
with only the filtered vertices.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id95">
<h3>Python code<a class="headerlink" href="#id95" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:filterverticesbyz</span></code></p>
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
<section id="fix-geometries">
<span id="qgisfixgeometries"></span><h2><a class="toc-backref" href="#id337" role="doc-backlink"><span class="section-number">28.1.22.33. </span>Fix geometries</a><a class="headerlink" href="#fix-geometries" title="Link to this heading"></a></h2>
<p>Attempts to create a valid representation of a given invalid geometry
without losing any of the input vertices.
Already valid geometries are returned without further intervention.
Always outputs multi-geometry layer.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features without M enabled</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>M values will be dropped from the output.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgischeckvalidity"><span class="std std-ref">Check validity</span></a></p>
</div>
<section id="id96">
<h3>Parameters<a class="headerlink" href="#id96" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Repair method</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 1</p>
</td>
<td><p>Method used to repair the geometries. One of:</p>
<ul class="simple">
<li><p>0 — <code class="docutils literal notranslate"><span class="pre">Linework</span></code>: combines all rings into a set of noded lines and
then extracts valid polygons from that linework</p></li>
<li><p>1 — <code class="docutils literal notranslate"><span class="pre">Structure</span></code>: first makes all rings valid and then merges shells
and subtracts holes from shells to generate valid result.
Assumes that holes and shells are correctly categorized.
Requires QGIS version built with GEOS 3.10 or later
(check <span class="menuselection">Help ► About</span> menu).</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Fixed geometries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<tr class="row-even"><td><p><strong>Fixed geometries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer with fixed geometries.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id98">
<h3>Python code<a class="headerlink" href="#id98" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:fixgeometries</span></code></p>
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
<section id="force-right-hand-rule">
<span id="qgisforcerhr"></span><h2><a class="toc-backref" href="#id338" role="doc-backlink"><span class="section-number">28.1.22.34. </span>Force right-hand-rule</a><a class="headerlink" href="#force-right-hand-rule" title="Link to this heading"></a></h2>
<p>Forces polygon geometries to respect the Right-Hand-Rule, in which
the area that is bounded by a polygon is to the right of the boundary.
In particular, the exterior ring is oriented in a clockwise
direction and any interior rings in a counter-clockwise direction.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<section id="id99">
<h3>Parameters<a class="headerlink" href="#id99" title="Link to this heading"></a></h3>
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
<td><p>[vector: polygon]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reoriented</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id100">
<h3>Outputs<a class="headerlink" href="#id100" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Reoriented</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output vector layer with reoriented geometries.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id101">
<h3>Python code<a class="headerlink" href="#id101" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:forcerhr</span></code></p>
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
<section id="geodesic-line-split-at-antimeridian">
<span id="qgisantimeridiansplit"></span><h2><a class="toc-backref" href="#id339" role="doc-backlink"><span class="section-number">28.1.22.35. </span>Geodesic line split at antimeridian</a><a class="headerlink" href="#geodesic-line-split-at-antimeridian" title="Link to this heading"></a></h2>
<p>Splits a line into multiple geodesic segments, whenever
the line crosses the antimeridian (±180 degrees longitude).</p>
<p>Splitting at the antimeridian helps the visual display of the lines in
some projections.
The returned geometry will always be a multi-part geometry.</p>
<p>Whenever line segments in the input geometry cross the antimeridian,
they will be split into two segments, with the latitude of the
breakpoint being determined using a geodesic line connecting the
points either side of this segment.
The current project ellipsoid setting will be used when calculating
this breakpoint.</p>
<p>If the input geometry contains M or Z values, these will be linearly
interpolated for the new vertices created at the antimeridian.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<section id="id102">
<h3>Parameters<a class="headerlink" href="#id102" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Split</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output line vector layer. One of:</p>
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
<section id="id103">
<h3>Outputs<a class="headerlink" href="#id103" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Split</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The output line vector layer split at the antimeridian.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id104">
<h3>Python code<a class="headerlink" href="#id104" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:antimeridiansplit</span></code></p>
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
<section id="geometry-by-expression">
<span id="qgisgeometrybyexpression"></span><h2><a class="toc-backref" href="#id340" role="doc-backlink"><span class="section-number">28.1.22.36. </span>Geometry by expression</a><a class="headerlink" href="#geometry-by-expression" title="Link to this heading"></a></h2>
<p>Updates existing geometries (or creates new geometries) for input
features by use of a QGIS expression.</p>
<p>This allows complex geometry modifications which can utilize all the
flexibility of the QGIS expression engine to manipulate and create
geometries for output features.</p>
<p>For help with QGIS expression functions, see the inbuilt help available
in the <a class="reference internal" href="../../expressions/expression.html#vector-expressions"><span class="std std-ref">expression builder</span></a>.</p>
<section id="id105">
<h3>Parameters<a class="headerlink" href="#id105" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output geometry type</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT_GEOMETRY</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>The output geometry strongly depends on the expression: for
instance, if you create a buffer the geometry type has to be
polygon.
One of:</p>
<ul class="simple">
<li><p>0 — Polygon</p></li>
<li><p>1 — Line</p></li>
<li><p>2 — Point</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Output geometry has z values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WITH_Z</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Choose if the output geometry should include the Z dimension</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Output geometry has m values</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WITH_M</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Choose if the output geometry should include the M dimension</p></td>
</tr>
<tr class="row-even"><td><p><strong>Geometry expression</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">EXPRESSION</span></code></p></td>
<td><p>[expression]</p>
<p>Default: ‘$geometry’</p>
</td>
<td><p>Add the geometry expression you want to use.
You can use the button to open the Expression Dialog.
The dialog lists all the relevant expressions, together
with their help and guide.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Modified geometry</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: any]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id106">
<h3>Outputs<a class="headerlink" href="#id106" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Modified geometry</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: any]</p></td>
<td><p>The output vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id107">
<h3>Python code<a class="headerlink" href="#id107" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:geometrybyexpression</span></code></p>
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
<section id="interpolate-point-on-line">
<span id="qgisinterpolatepoint"></span><h2><a class="toc-backref" href="#id341" role="doc-backlink"><span class="section-number">28.1.22.37. </span>Interpolate point on line</a><a class="headerlink" href="#interpolate-point-on-line" title="Link to this heading"></a></h2>
<p>Creates a point geometry interpolated at a set distance along line or
curve geometries.</p>
<p>Z and M values are linearly interpolated from existing values.</p>
<p>If a multipart geometry is encountered, only the first part is
considered when calculating the substring.</p>
<p>If the specified distance is greater than the input feature’s length,
the resultant feature will have a null geometry.</p>
<figure class="align-center" id="id274">
<img alt="../../../../_images/interpolated_point.png" src="../../../../_images/interpolated_point.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.88 </span><span class="caption-text">Interpolated point at 500m of the beginning of the line</span><a class="headerlink" href="#id274" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgispointsalonglines"><span class="std std-ref">Points along geometry</span></a></p>
</div>
<section id="id108">
<h3>Parameters<a class="headerlink" href="#id108" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Distance from the beginning of the line</p></td>
</tr>
<tr class="row-even"><td><p><strong>Interpolated points</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id109">
<h3>Outputs<a class="headerlink" href="#id109" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Interpolated points</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output point vector layer with features
at a set distance along the line or polygon boundary</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id110">
<h3>Python code<a class="headerlink" href="#id110" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:interpolatepoint</span></code></p>
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
<section id="keep-n-biggest-parts">
<span id="qgiskeepnbiggestparts"></span><h2><a class="toc-backref" href="#id342" role="doc-backlink"><span class="section-number">28.1.22.38. </span>Keep N biggest parts</a><a class="headerlink" href="#keep-n-biggest-parts" title="Link to this heading"></a></h2>
<p>Takes a layer with polygons or multipolygons and returns a new layer
in which only the <em>n</em> largest polygons of each multipolygon feature
are kept.
If a feature has <em>n</em> or fewer parts, the feature will just be copied.</p>
<figure class="align-center" id="id275">
<img alt="../../../../_images/n_biggest.png" src="../../../../_images/n_biggest.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.89 </span><span class="caption-text">Clockwise from top left: original multipart feature, one, two and
three biggest parts kept</span><a class="headerlink" href="#id275" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id111">
<h3>Parameters<a class="headerlink" href="#id111" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Polygons</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">INPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Input polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Parts to keep</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">PARTS</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1</p>
</td>
<td><p>Number of parts to keep. If 1, only the biggest part of the
feature will be kept.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Parts</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id112">
<h3>Outputs<a class="headerlink" href="#id112" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Parts</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output polygon vector layer with the N biggest parts of
each feature</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id113">
<h3>Python code<a class="headerlink" href="#id113" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:keepnbiggestparts</span></code></p>
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
<section id="line-substring">
<span id="qgislinesubstring"></span><h2><a class="toc-backref" href="#id343" role="doc-backlink"><span class="section-number">28.1.22.39. </span>Line substring</a><a class="headerlink" href="#line-substring" title="Link to this heading"></a></h2>
<p>Returns the portion of a line (or curve) which falls between the
specified start and end distances (measured from the beginning of the
line).</p>
<p>Z and M values are linearly interpolated from existing values.</p>
<p>If a multipart geometry is encountered, only the first part is
considered when calculating the substring.</p>
<figure class="align-center" id="id276">
<img alt="../../../../_images/substring.png" src="../../../../_images/substring.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.90 </span><span class="caption-text">Substring line with starting distance set at 0 meters and the
ending distance at 250 meters.</span><a class="headerlink" href="#id276" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows <a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisextendlines"><span class="std std-ref">Extend lines</span></a></p>
</div>
<section id="id114">
<h3>Parameters<a class="headerlink" href="#id114" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Start distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">START_DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p></td>
<td><p>Distance along the input line to the start point of
the output feature</p></td>
</tr>
<tr class="row-even"><td><p><strong>End distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">END_DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p></td>
<td><p>Distance along the input line to the end point of
the output feature</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Substring</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output line vector layer. One of:</p>
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
<section id="id115">
<h3>Outputs<a class="headerlink" href="#id115" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Substring</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The output line vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id116">
<h3>Python code<a class="headerlink" href="#id116" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:linesubstring</span></code></p>
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
<section id="lines-to-polygons">
<span id="qgislinestopolygons"></span><h2><a class="toc-backref" href="#id344" role="doc-backlink"><span class="section-number">28.1.22.40. </span>Lines to polygons</a><a class="headerlink" href="#lines-to-polygons" title="Link to this heading"></a></h2>
<p>Generates a polygon layer using as polygon rings the lines from an
input line layer.</p>
<p>The attribute table of the output layer is the same as the one of
the input layer.</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgispolygonstolines"><span class="std std-ref">Polygons to lines</span></a>, <a class="reference internal" href="#qgispolygonize"><span class="std std-ref">Polygonize</span></a>, <a class="reference internal" href="#qgisconvertgeometrytype"><span class="std std-ref">Convert geometry type</span></a></p>
</div>
<section id="id117">
<h3>Parameters<a class="headerlink" href="#id117" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Polygons</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id118">
<h3>Outputs<a class="headerlink" href="#id118" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Polygons</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output polygon vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id119">
<h3>Python code<a class="headerlink" href="#id119" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:linestopolygons</span></code></p>
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
<section id="merge-lines">
<span id="qgismergelines"></span><h2><a class="toc-backref" href="#id345" role="doc-backlink"><span class="section-number">28.1.22.41. </span>Merge lines</a><a class="headerlink" href="#merge-lines" title="Link to this heading"></a></h2>
<p>Joins all connected parts of MultiLineString geometries into single
LineString geometries.</p>
<p>If any parts of the input MultiLineString geometries are not
connected, the resultant geometry will be a MultiLineString containing
any lines which could be merged and any non-connected line parts.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<section id="id120">
<h3>Parameters<a class="headerlink" href="#id120" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Merged</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output line vector layer. One of:</p>
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
<section id="id121">
<h3>Outputs<a class="headerlink" href="#id121" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Merged</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The output (merged) line vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id122">
<h3>Python code<a class="headerlink" href="#id122" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:mergelines</span></code></p>
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
<section id="minimum-bounding-geometry">
<span id="qgisminimumboundinggeometry"></span><h2><a class="toc-backref" href="#id346" role="doc-backlink"><span class="section-number">28.1.22.42. </span>Minimum bounding geometry</a><a class="headerlink" href="#minimum-bounding-geometry" title="Link to this heading"></a></h2>
<p>Creates geometries which enclose the features from an input layer.
The features can be grouped by a field.
The output layer will then contain one feature per group value with
a geometry (MBB) that covers the geometries of the features with
matching value.</p>
<p>The following enclosing geometry types are supported:</p>
<ul class="simple">
<li><p>bounding box (envelope)</p></li>
<li><p>oriented rectangle</p></li>
<li><p>circle</p></li>
<li><p>convex hull</p></li>
</ul>
<figure class="align-center" id="id277">
<img alt="../../../../_images/minimum_bounding.png" src="../../../../_images/minimum_bounding.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.91 </span><span class="caption-text">Clockwise from top left: envelope, oriented rectangle,
circle, convex hull</span><a class="headerlink" href="#id277" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisminimumenclosingcircle"><span class="std std-ref">Minimum enclosing circles</span></a></p>
</div>
<section id="id123">
<h3>Parameters<a class="headerlink" href="#id123" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Field</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">FIELD</span></code></p></td>
<td><p>[tablefield: any]</p></td>
<td><p>Features can be grouped by a field.
If set, this causes the output layer to contain one feature per
grouped value with a minimal geometry covering only the
features with matching values.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Geometry type</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TYPE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Enclosing geometry types. One of:</p>
<ul class="simple">
<li><p>0 — Envelope (Bounding Box)</p></li>
<li><p>1 — Minimum Oriented Rectangle</p></li>
<li><p>2 — Minimum Enclosing Circle</p></li>
<li><p>3 — Convex Hull</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Bounding geometry</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id124">
<h3>Outputs<a class="headerlink" href="#id124" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Bounding geometry</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output (bounding) polygon vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id125">
<h3>Python code<a class="headerlink" href="#id125" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:minimumboundinggeometry</span></code></p>
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
<section id="minimum-enclosing-circles">
<span id="qgisminimumenclosingcircle"></span><h2><a class="toc-backref" href="#id347" role="doc-backlink"><span class="section-number">28.1.22.43. </span>Minimum enclosing circles</a><a class="headerlink" href="#minimum-enclosing-circles" title="Link to this heading"></a></h2>
<p>Calculates the minimum enclosing circles of the features in the input
layer.</p>
<figure class="align-center" id="id278">
<img alt="../../../../_images/minimum_enclosing_circles.png" src="../../../../_images/minimum_enclosing_circles.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.92 </span><span class="caption-text">Enclosing circles for each feature</span><a class="headerlink" href="#id278" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisminimumboundinggeometry"><span class="std std-ref">Minimum bounding geometry</span></a></p>
</div>
<section id="id126">
<h3>Parameters<a class="headerlink" href="#id126" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Number of segments in circles</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEGMENTS</span></code></p></td>
<td><p>[number]</p>
<p>Default: 72</p>
</td>
<td><p>The number of segments used to approximate a circle.
Minimum 8, maximum 100000.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Minimum enclosing circles</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id127">
<h3>Outputs<a class="headerlink" href="#id127" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Minimum enclosing circles</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output polygon vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id128">
<h3>Python code<a class="headerlink" href="#id128" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:minimumenclosingcircle</span></code></p>
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
<section id="multi-ring-buffer-constant-distance">
<span id="qgismultiringconstantbuffer"></span><h2><a class="toc-backref" href="#id348" role="doc-backlink"><span class="section-number">28.1.22.44. </span>Multi-ring buffer (constant distance)</a><a class="headerlink" href="#multi-ring-buffer-constant-distance" title="Link to this heading"></a></h2>
<p>Computes multi-ring (<em>donut</em>) buffer for the features of the
input layer, using a fixed or dynamic distance and number of rings.</p>
<figure class="align-center" id="id279">
<img alt="../../../../_images/multiringbuffer.png" src="../../../../_images/multiringbuffer.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.93 </span><span class="caption-text">Multi-ring buffer for a line, point and polygon layer</span><a class="headerlink" href="#id279" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisbuffer"><span class="std std-ref">Buffer</span></a>,
<a class="reference internal" href="modelertools.html#qgisvariabledistancebuffer"><span class="std std-ref">Variable distance buffer</span></a>,
<a class="reference internal" href="#qgisrectanglesovalsdiamonds"><span class="std std-ref">Rectangles, ovals, diamonds</span></a>,
<a class="reference internal" href="#qgissinglesidedbuffer"><span class="std std-ref">Single sided buffer</span></a></p>
</div>
<section id="id129">
<h3>Parameters<a class="headerlink" href="#id129" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Number of rings</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RINGS</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1</p>
</td>
<td><p>The number of rings.
It can be a unique value (same number of rings for all the
features) or it can be taken from features data (the number of
rings depends on feature values).</p></td>
</tr>
<tr class="row-even"><td><p><strong>Distance between rings</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Distance between the rings.
It can be a unique value (same distance for all the features)
or it can be taken from features data (the distance depends on
feature values).</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Multi-ring buffer (constant distance)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id130">
<h3>Outputs<a class="headerlink" href="#id130" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Multi-ring buffer (constant distance)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output polygon vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id131">
<h3>Python code<a class="headerlink" href="#id131" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:multiringconstantbuffer</span></code></p>
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
<section id="multipart-to-singleparts">
<span id="qgismultiparttosingleparts"></span><h2><a class="toc-backref" href="#id349" role="doc-backlink"><span class="section-number">28.1.22.45. </span>Multipart to singleparts</a><a class="headerlink" href="#multipart-to-singleparts" title="Link to this heading"></a></h2>
<p>Splits multipart features in the input layer into singlepart
features.</p>
<p>The attributes of the output layer are the same as the original ones
but divided into single features.</p>
<figure class="align-center" id="id280">
<img alt="../../../../_images/multipart.png" src="../../../../_images/multipart.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.94 </span><span class="caption-text">Left the multipart source layer and right the single part output
result</span><a class="headerlink" href="#id280" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgiscollect"><span class="std std-ref">Collect geometries</span></a>, <a class="reference internal" href="#qgispromotetomulti"><span class="std std-ref">Promote to multipart</span></a></p>
</div>
<section id="id132">
<h3>Parameters<a class="headerlink" href="#id132" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Single parts</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id133">
<h3>Outputs<a class="headerlink" href="#id133" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Single parts</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id134">
<h3>Python code<a class="headerlink" href="#id134" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:multiparttosingleparts</span></code></p>
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
<section id="offset-lines">
<span id="qgisoffsetline"></span><h2><a class="toc-backref" href="#id350" role="doc-backlink"><span class="section-number">28.1.22.46. </span>Offset lines</a><a class="headerlink" href="#offset-lines" title="Link to this heading"></a></h2>
<p>Offsets lines by a specified distance.
Positive distances will offset lines to the left, and negative
distances will offset them to the right.</p>
<figure class="align-center" id="id281">
<img alt="../../../../_images/offset_lines.png" src="../../../../_images/offset_lines.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.95 </span><span class="caption-text">In blue the source layer, in red the offset one</span><a class="headerlink" href="#id281" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="vectorcreation.html#qgisarrayoffsetlines"><span class="std std-ref">Array of offset (parallel) lines</span></a>, <a class="reference internal" href="#qgistranslategeometry"><span class="std std-ref">Translate</span></a></p>
</div>
<section id="id135">
<h3>Parameters<a class="headerlink" href="#id135" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 10.0</p>
</td>
<td><p>Offset distance.
You can use the Data Defined button on the right to choose
a field from which the radius will be calculated.
This way you can have different radius for each feature
(see <a class="reference internal" href="modelertools.html#qgisvariabledistancebuffer"><span class="std std-ref">Variable distance buffer</span></a>).</p></td>
</tr>
<tr class="row-even"><td><p><strong>Segments</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEGMENTS</span></code></p></td>
<td><p>[number]</p>
<p>Default: 8</p>
</td>
<td><p>Controls the number of line segments to use to approximate
a quarter circle when creating rounded offsets.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Join style</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">JOIN_STYLE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Specifies whether round, miter or beveled joins should be
used when offsetting corners in a line.
Options are:</p>
<ul class="simple">
<li><p>0 — Round</p></li>
<li><p>1 — Miter</p></li>
<li><p>2 — Bevel</p></li>
</ul>
<figure class="align-center" id="id282">
<a class="reference internal image-reference" href="../../../../_images/buffer_join_style.png"><img alt="../../../../_images/buffer_join_style.png" src="../../../../_images/buffer_join_style.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.96 </span><span class="caption-text">Round, miter, and bevel join styles</span><a class="headerlink" href="#id282" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-even"><td><p><strong>Miter limit</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MITER_LIMIT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 2.0</p>
</td>
<td><p>Sets the maximum distance from the offset geometry to use
when creating a mitered join as a factor of the offset distance (only applicable for miter
join styles).
Minimum: 1.0</p>
<figure class="align-center" id="id283">
<a class="reference internal image-reference" href="../../../../_images/buffer_miter_limit.png"><img alt="../../../../_images/buffer_miter_limit.png" src="../../../../_images/buffer_miter_limit.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.97 </span><span class="caption-text">A 10m buffer with a limit of 2 and a 10m buffer with a limit of 1</span><a class="headerlink" href="#id283" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Offset</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (offset) layer.
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
<section id="id136">
<h3>Outputs<a class="headerlink" href="#id136" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Offset</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>Output (offset) line layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id137">
<h3>Python code<a class="headerlink" href="#id137" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:offsetline</span></code></p>
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
<section id="oriented-minimum-bounding-box">
<span id="qgisorientedminimumboundingbox"></span><h2><a class="toc-backref" href="#id351" role="doc-backlink"><span class="section-number">28.1.22.47. </span>Oriented minimum bounding box</a><a class="headerlink" href="#oriented-minimum-bounding-box" title="Link to this heading"></a></h2>
<p>Calculates the minimum area rotated rectangle for each feature in the
input layer.</p>
<figure class="align-center" id="id284">
<img alt="../../../../_images/oriented_minimum_bounding_box.png" src="../../../../_images/oriented_minimum_bounding_box.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.98 </span><span class="caption-text">Oriented minimum bounding box</span><a class="headerlink" href="#id284" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisminimumboundinggeometry"><span class="std std-ref">Minimum bounding geometry</span></a></p>
</div>
<section id="id138">
<h3>Parameters<a class="headerlink" href="#id138" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Bounding boxes</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id139">
<h3>Outputs<a class="headerlink" href="#id139" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Bounding boxes</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output polygon vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id140">
<h3>Python code<a class="headerlink" href="#id140" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:orientedminimumboundingbox</span></code></p>
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
<section id="orthogonalize">
<span id="qgisorthogonalize"></span><h2><a class="toc-backref" href="#id352" role="doc-backlink"><span class="section-number">28.1.22.48. </span>Orthogonalize</a><a class="headerlink" href="#orthogonalize" title="Link to this heading"></a></h2>
<p>Attempts to orthogonalize the geometries of the input line or polygon
layer.
This process shifts the vertices in the geometries to try to make
every angle in the geometry either a right angle or a straight line.</p>
<figure class="align-center" id="id285">
<img alt="../../../../_images/orthogonize.png" src="../../../../_images/orthogonize.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.99 </span><span class="caption-text">In blue the source layer and in the red orthogonalized
result</span><a class="headerlink" href="#id285" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features</p>
<section id="id141">
<h3>Parameters<a class="headerlink" href="#id141" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum angle tolerance (degrees)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ANGLE_TOLERANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 15</p>
</td>
<td><p>Specify the maximum deviation from a right angle or straight
line a vertex can have for it to be adjusted.
Smaller tolerances mean that only vertices which are already
closer to right angles will be adjusted, and larger tolerances
mean that vertices which deviate further from right angles will
also be adjusted.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Maximum algorithm iterations</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAX_ITERATIONS</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1000</p>
</td>
<td><p>Setting a larger number for the maximum number of iterations
will result in a more orthogonal geometry at the cost of extra
processing time.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Orthogonalized</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id142">
<h3>Outputs<a class="headerlink" href="#id142" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Orthogonalized</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output polygon vector layer with adjusted angles.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id143">
<h3>Python code<a class="headerlink" href="#id143" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:orthogonalize</span></code></p>
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
<section id="point-on-surface">
<span id="qgispointonsurface"></span><h2><a class="toc-backref" href="#id353" role="doc-backlink"><span class="section-number">28.1.22.49. </span>Point on Surface</a><a class="headerlink" href="#point-on-surface" title="Link to this heading"></a></h2>
<p>For each feature of the input layer, returns a point that is
guaranteed to lie on the surface of the feature geometry.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgiscentroids"><span class="std std-ref">Centroids</span></a></p>
</div>
<section id="id144">
<h3>Parameters<a class="headerlink" href="#id144" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Create point on surface for each part</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ANGLE_TOLERANCE</span></code></p></td>
<td><p>[boolean <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p></td>
<td><p>If checked, a point will be created for each part of the
geometry.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Point</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output point vector layer. One of:</p>
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
<section id="id145">
<h3>Outputs<a class="headerlink" href="#id145" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Point</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output point vector layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id146">
<h3>Python code<a class="headerlink" href="#id146" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:pointonsurface</span></code></p>
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
<section id="points-along-geometry">
<span id="qgispointsalonglines"></span><h2><a class="toc-backref" href="#id354" role="doc-backlink"><span class="section-number">28.1.22.50. </span>Points along geometry</a><a class="headerlink" href="#points-along-geometry" title="Link to this heading"></a></h2>
<p>Creates points at regular intervals along line or polygon geometries.
Created points will have new attributes added for the distance along
the geometry and the angle of the line at the point.</p>
<p>An optional start and end offset can be specified, which controls how
far from the start and end of the geometry the points should be
created.</p>
<figure class="align-center" id="id286">
<img alt="../../../../_images/points_along_line.png" src="../../../../_images/points_along_line.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.100 </span><span class="caption-text">Points created along the source line layer</span><a class="headerlink" href="#id286" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisinterpolatepoint"><span class="std std-ref">Interpolate point on line</span></a></p>
</div>
<section id="id147">
<h3>Parameters<a class="headerlink" href="#id147" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Distance between two consecutive points along the line</p></td>
</tr>
<tr class="row-even"><td><p><strong>Start offset</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">START_OFFSET</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Distance from the beginning of the input line, representing the
position of the first point.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>End offset</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">END_OFFSET</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Distance from the end of the input line, representing the
position beyond which no point feature shoud be created.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Interpolated points</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id148">
<h3>Outputs<a class="headerlink" href="#id148" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Interpolated points</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>Point vector layer with features placed along lines or polygon
boundaries of the input layer.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id149">
<h3>Python code<a class="headerlink" href="#id149" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:pointsalonglines</span></code></p>
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
<section id="points-displacement">
<span id="qgispointsdisplacement"></span><h2><a class="toc-backref" href="#id355" role="doc-backlink"><span class="section-number">28.1.22.51. </span>Points displacement</a><a class="headerlink" href="#points-displacement" title="Link to this heading"></a></h2>
<p>Given a distance of proximity, identifies nearby point features and
radially distributes them over a circle whose center represents their
barycenter.
A convenient tool to scatter overlaid features.</p>
<section id="id150">
<h3>Parameters<a class="headerlink" href="#id150" title="Link to this heading"></a></h3>
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
<td><p>[vector: point]</p></td>
<td><p>Input point vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Minimum distance to other points</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">PROXIMITY</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1.0</p>
</td>
<td><p>Distance below which point features are
considered close.
Close features are distributed altogether.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Displacement distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1.0</p>
</td>
<td><p>Radius of the circle on which close features are placed</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Horizontal distribution for two point case</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HORIZONTAL</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>When only two points are identified as close, aligns them
horizontally on the circle instead of vertically.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Displaced</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id151">
<h3>Outputs<a class="headerlink" href="#id151" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Displaced</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>Output point vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id152">
<h3>Python code<a class="headerlink" href="#id152" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">qgis:pointsdisplacement</span></code></p>
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
<section id="pole-of-inaccessibility">
<span id="qgispoleofinaccessibility"></span><h2><a class="toc-backref" href="#id356" role="doc-backlink"><span class="section-number">28.1.22.52. </span>Pole of inaccessibility</a><a class="headerlink" href="#pole-of-inaccessibility" title="Link to this heading"></a></h2>
<p>Calculates the pole of inaccessibility for a polygon layer, which is
the most distant internal point from the boundary of the surface.</p>
<p>This algorithm uses the ‘polylabel’ algorithm (Vladimir Agafonkin,
2016), which is an iterative approach guaranteed to find the true pole
of inaccessibility within a specified tolerance.
A more precise tolerance (lower value) requires more iterations and
will take longer to calculate.</p>
<p>The distance from the calculated pole to the polygon boundary will be
stored as a new attribute in the output layer.</p>
<figure class="align-center" id="id287">
<img alt="../../../../_images/pole_inaccessibility.png" src="../../../../_images/pole_inaccessibility.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.101 </span><span class="caption-text">Pole of inaccessibility</span><a class="headerlink" href="#id287" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id153">
<h3>Parameters<a class="headerlink" href="#id153" title="Link to this heading"></a></h3>
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
<td><p>[vector: polygon]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Tolerance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOLERANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 1.0</p>
</td>
<td><p>Set the tolerance for the calculation</p></td>
</tr>
<tr class="row-even"><td><p><strong>Point</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id154">
<h3>Outputs<a class="headerlink" href="#id154" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Point</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output point vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id155">
<h3>Python code<a class="headerlink" href="#id155" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:poleofinaccessibility</span></code></p>
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
<section id="polygonize">
<span id="qgispolygonize"></span><h2><a class="toc-backref" href="#id357" role="doc-backlink"><span class="section-number">28.1.22.53. </span>Polygonize</a><a class="headerlink" href="#polygonize" title="Link to this heading"></a></h2>
<p>Creates a polygon layer whose features boundaries are generated from a
line layer of <strong>closed</strong> features.</p>
<figure class="align-center" id="id288">
<img alt="../../../../_images/polygonize1.png" src="../../../../_images/polygonize1.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.102 </span><span class="caption-text">The yellow polygons generated from the closed lines</span><a class="headerlink" href="#id288" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>The line layer must have closed shapes in order to be
transformed into a polygon.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgispolygonstolines"><span class="std std-ref">Polygons to lines</span></a>, <a class="reference internal" href="#qgislinestopolygons"><span class="std std-ref">Lines to polygons</span></a>, <a class="reference internal" href="#qgisconvertgeometrytype"><span class="std std-ref">Convert geometry type</span></a></p>
</div>
<section id="id156">
<h3>Parameters<a class="headerlink" href="#id156" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Keep fields from the input layer</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">KEEP_FIELDS</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: False</p>
</td>
<td><p>Check to keep the fields (only the table structure, not the values) of the input layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Polygons from lines</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output polygon vector layer. One of:</p>
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
<section id="id157">
<h3>Outputs<a class="headerlink" href="#id157" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Polygons from lines</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output polygon vector layer from lines</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id158">
<h3>Python code<a class="headerlink" href="#id158" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:polygonize</span></code></p>
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
<section id="polygons-to-lines">
<span id="qgispolygonstolines"></span><h2><a class="toc-backref" href="#id358" role="doc-backlink"><span class="section-number">28.1.22.54. </span>Polygons to lines</a><a class="headerlink" href="#polygons-to-lines" title="Link to this heading"></a></h2>
<p>Takes a polygon layer and creates a line layer, with lines
representing the boundaries of the polygons in the input layer.</p>
<p>The attribute table of the output layer is the same as the one of
the input layer.</p>
<figure class="align-center" id="id289">
<img alt="../../../../_images/polygon_to_lines.png" src="../../../../_images/polygon_to_lines.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.103 </span><span class="caption-text">Black lines as the result of the algorithm</span><a class="headerlink" href="#id289" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgislinestopolygons"><span class="std std-ref">Lines to polygons</span></a>, <a class="reference internal" href="#qgispolygonize"><span class="std std-ref">Polygonize</span></a>, <a class="reference internal" href="#qgisconvertgeometrytype"><span class="std std-ref">Convert geometry type</span></a></p>
</div>
<section id="id159">
<h3>Parameters<a class="headerlink" href="#id159" title="Link to this heading"></a></h3>
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
<td><p>[vector: polygon]</p></td>
<td><p>Input polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Lines</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output line vector layer. One of:</p>
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
<section id="id160">
<h3>Outputs<a class="headerlink" href="#id160" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Lines</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The output line vector layer from polygons</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id161">
<h3>Python code<a class="headerlink" href="#id161" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:polygonstolines</span></code></p>
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
<section id="project-points-cartesian">
<span id="qgisprojectpointcartesian"></span><h2><a class="toc-backref" href="#id359" role="doc-backlink"><span class="section-number">28.1.22.55. </span>Project points (Cartesian)</a><a class="headerlink" href="#project-points-cartesian" title="Link to this heading"></a></h2>
<p>Projects point geometries by a specified distance and bearing (azimuth).</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point features</p>
<section id="id162">
<h3>Parameters<a class="headerlink" href="#id162" title="Link to this heading"></a></h3>
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
<td><p>[vector: point]</p></td>
<td><p>Input point vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Bearing (degrees from North)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BEARING</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Clockwise angle starting from North, in degree (°) unit</p></td>
</tr>
<tr class="row-even"><td><p><strong>Distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Distance to offset geometries, in layer units</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Projected</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output point vector layer. One of:</p>
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
<section id="id163">
<h3>Outputs<a class="headerlink" href="#id163" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Projected</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: point]</p></td>
<td><p>The output (projected) point vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id164">
<h3>Python code<a class="headerlink" href="#id164" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:projectpointcartesian</span></code></p>
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
<section id="promote-to-multipart">
<span id="qgispromotetomulti"></span><h2><a class="toc-backref" href="#id360" role="doc-backlink"><span class="section-number">28.1.22.56. </span>Promote to multipart</a><a class="headerlink" href="#promote-to-multipart" title="Link to this heading"></a></h2>
<p>Takes a vector layer with singlepart geometries and generates a new
one in which all geometries are multipart.</p>
<p>Input features which are already multipart features will remain
unchanged.</p>
<p>This algorithm can be used to force geometries to multipart types in
order to be compatible with data providers that require multipart
features.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisaggregate"><span class="std std-ref">Aggregate</span></a>, <a class="reference internal" href="#qgiscollect"><span class="std std-ref">Collect geometries</span></a></p>
</div>
<section id="id165">
<h3>Parameters<a class="headerlink" href="#id165" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Multiparts</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output multipart vector layer. One of:</p>
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
<section id="id166">
<h3>Outputs<a class="headerlink" href="#id166" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Multiparts</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output multipart vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id167">
<h3>Python code<a class="headerlink" href="#id167" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:promotetomulti</span></code></p>
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
<section id="rectangles-ovals-diamonds">
<span id="qgisrectanglesovalsdiamonds"></span><h2><a class="toc-backref" href="#id361" role="doc-backlink"><span class="section-number">28.1.22.57. </span>Rectangles, ovals, diamonds</a><a class="headerlink" href="#rectangles-ovals-diamonds" title="Link to this heading"></a></h2>
<p>Creates a buffer area with a rectangle, oval or diamond shape
for each feature of the input point layer.</p>
<p>The shape parameters can be fixed for all features or dynamic using a field or
an expression.</p>
<figure class="align-center" id="id290">
<img alt="../../../../_images/rectangles_ovals_diamond_variable.png" src="../../../../_images/rectangles_ovals_diamond_variable.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.104 </span><span class="caption-text">Different buffer shapes with dynamic parameters</span><a class="headerlink" href="#id290" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id168">
<h3>Parameters<a class="headerlink" href="#id168" title="Link to this heading"></a></h3>
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
<td><p>[vector: point]</p></td>
<td><p>Input point vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Buffer shape</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SHAPE</span></code></p></td>
<td><p>[enumeration]</p></td>
<td><p>The shape to use. One of:</p>
<ul class="simple">
<li><p>0 — Rectangles</p></li>
<li><p>1 — Ovals</p></li>
<li><p>2 — Diamonds</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Width</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">WIDTH</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Width of the buffer shape</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Height</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HEIGHT</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Height of the buffer shape</p></td>
</tr>
<tr class="row-even"><td><p><strong>Rotation</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">ROTATION</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: None</p>
</td>
<td><p>Rotation of the buffer shape</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Number of segments</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEGMENTS</span></code></p></td>
<td><p>[number]</p>
<p>Default: 36</p>
</td>
<td><p>Number of segments for a full circle (<em>Ovals</em> shape)</p></td>
</tr>
<tr class="row-even"><td><p><strong>Output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id169">
<h3>Outputs<a class="headerlink" href="#id169" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Output</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>The output vector layer (with the buffer shapes)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id170">
<h3>Python code<a class="headerlink" href="#id170" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rectanglesovalsdiamonds</span></code></p>
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
<section id="remove-duplicate-vertices">
<span id="qgisremoveduplicatevertices"></span><h2><a class="toc-backref" href="#id362" role="doc-backlink"><span class="section-number">28.1.22.58. </span>Remove duplicate vertices</a><a class="headerlink" href="#remove-duplicate-vertices" title="Link to this heading"></a></h2>
<p>Removes duplicate vertices from features, wherever removing the
vertices does not result in a degenerate geometry.</p>
<p>The tolerance parameter specifies the tolerance for coordinates when
determining whether vertices are identical.</p>
<p>By default, Z values are not considered when detecting duplicate
vertices.
E.g. two vertices with the same X and Y coordinate but different Z
values will still be considered duplicate and one will be removed.
If the <span class="guilabel">Use Z Value</span> parameter is true, then the Z values
are also tested and vertices with the same X and Y but different Z
will be maintained.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows <a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Duplicate vertices are not tested between different parts
of a multipart geometry, e.g. a multipoint geometry with
overlapping points will not be changed by this method.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisextractvertices"><span class="std std-ref">Extract vertices</span></a>,
<a class="reference internal" href="#qgisextractspecificvertices"><span class="std std-ref">Extract specific vertices</span></a>,
<a class="reference internal" href="vectorgeneral.html#qgisdeleteduplicategeometries"><span class="std std-ref">Delete duplicate geometries</span></a></p>
</div>
<section id="id171">
<h3>Parameters<a class="headerlink" href="#id171" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Tolerance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOLERANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.000001</p>
</td>
<td><p>Vertices closer than the specified distance are considered
duplicates</p></td>
</tr>
<tr class="row-even"><td><p><strong>Use Z value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">USE_Z_VALUE</span></code></p></td>
<td><p>[boolean <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: False</p>
</td>
<td><p>If the <span class="guilabel">Use Z Value</span> parameter is true, then the Z
values are also tested and vertices with the same X and Y but
different Z will be maintained.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Cleaned</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer. One of:</p>
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
<section id="id172">
<h3>Outputs<a class="headerlink" href="#id172" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Cleaned</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (without duplicate vertices)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id173">
<h3>Python code<a class="headerlink" href="#id173" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:removeduplicatevertices</span></code></p>
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
<section id="remove-null-geometries">
<span id="qgisremovenullgeometries"></span><h2><a class="toc-backref" href="#id363" role="doc-backlink"><span class="section-number">28.1.22.59. </span>Remove null geometries</a><a class="headerlink" href="#remove-null-geometries" title="Link to this heading"></a></h2>
<p>Removes any features which do not have a geometry from a vector layer.
All other features will be copied unchanged.</p>
<p>The features with null geometries can be saved to a separate layer.</p>
<p>If <span class="guilabel">Also remove empty geometries</span> is checked, the algorithm
removes features whose geometries have no coordinates, i.e., geometries
that are empty.
In that case, also the null output will reflect this option, containing
both null and empty geometries.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="vectorgeneral.html#qgisdeleteduplicategeometries"><span class="std std-ref">Delete duplicate geometries</span></a></p>
</div>
<section id="id174">
<h3>Parameters<a class="headerlink" href="#id174" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer (with non-NULL geometries)</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Also remove empty geometries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REMOVE_EMPTY</span></code></p></td>
<td><p>[boolean]</p></td>
<td></td>
</tr>
<tr class="row-even"><td><p><strong>Non null geometries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p>
<p>Optional</p>
</td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer for the non-NULL (and
non-empty) geometries.
One of:</p>
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
<tr class="row-odd"><td><p><strong>Null geometries</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">NULL_OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Skip</span> <span class="pre">output]</span></code></p>
</td>
<td><p>Specify the output vector layer for the NULL (and empty) geometries.
One of:</p>
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
<section id="id175">
<h3>Outputs<a class="headerlink" href="#id175" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Null geometries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NULL_OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output vector layer (for NULL and, if chosen, empty geometries)</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Non null geometries</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (without NULL and, if chosen, empty geometries)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id176">
<h3>Python code<a class="headerlink" href="#id176" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:removenullgeometries</span></code></p>
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
<section id="reverse-line-direction">
<span id="qgisreverselinedirection"></span><h2><a class="toc-backref" href="#id364" role="doc-backlink"><span class="section-number">28.1.22.60. </span>Reverse line direction</a><a class="headerlink" href="#reverse-line-direction" title="Link to this heading"></a></h2>
<p>Inverts the direction of a line layer.</p>
<figure class="align-center" id="id291">
<img alt="../../../../_images/reverse_line.png" src="../../../../_images/reverse_line.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.105 </span><span class="caption-text">Before and after the direction inversion</span><a class="headerlink" href="#id291" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows <a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<section id="id177">
<h3>Parameters<a class="headerlink" href="#id177" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reversed</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output line vector layer.
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
<section id="id178">
<h3>Outputs<a class="headerlink" href="#id178" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Reversed</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The output line vector layer (with reversed lines)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id179">
<h3>Python code<a class="headerlink" href="#id179" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:reverselinedirection</span></code></p>
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
<section id="rotate">
<span id="qgisrotatefeatures"></span><h2><a class="toc-backref" href="#id365" role="doc-backlink"><span class="section-number">28.1.22.61. </span>Rotate</a><a class="headerlink" href="#rotate" title="Link to this heading"></a></h2>
<p>Rotates feature geometries by the specified angle clockwise.
The rotation occurs around each feature’s centroid, or optionally
around a unique preset point.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgistranslategeometry"><span class="std std-ref">Translate</span></a>, <a class="reference internal" href="#qgisswapxy"><span class="std std-ref">Swap X and Y coordinates</span></a></p>
</div>
<section id="id180">
<h3>Parameters<a class="headerlink" href="#id180" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Rotation (degrees clockwise)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ANGLE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Angle of the rotation in degrees</p></td>
</tr>
<tr class="row-even"><td><p><strong>Rotation anchor point (x, y)</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">ANCHOR</span></code></p></td>
<td><p>[point]</p>
<p>Default: None</p>
</td>
<td><p>X,Y coordinates of the point to rotate the
features around.
If not set the rotation occurs around each
feature’s centroid.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Rotated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer (with rotated geometries).
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
<section id="id181">
<h3>Outputs<a class="headerlink" href="#id181" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Rotated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer with rotated geometries</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id182">
<h3>Python code<a class="headerlink" href="#id182" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:rotatefeatures</span></code></p>
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
<section id="roundness">
<span id="qgisroundness"></span><h2><a class="toc-backref" href="#id366" role="doc-backlink"><span class="section-number">28.1.22.62. </span>Roundness</a><a class="headerlink" href="#roundness" title="Link to this heading"></a></h2>
<p>Calculates the roundness of each feature and stores it as a new field. The input vector layer must contain polygons.</p>
<p>The roundness of a polygon is defined as 4π × polygon area / perimeter².
The roundness value varies between 0 and 1. A perfect circle has a roundness of 1,
while a completely flat polygon has a roundness of 0.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>The algorithm returns NULL for multipart polygon features.</p>
</div>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<section id="id183">
<h3>Parameters<a class="headerlink" href="#id183" title="Link to this heading"></a></h3>
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
<td><p>[vector: polygon]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Roundness</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer (with roundness field).
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
<section id="id184">
<h3>Outputs<a class="headerlink" href="#id184" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Rotated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer with roundness value in a field</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id185">
<h3>Python code<a class="headerlink" href="#id185" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:roundness</span></code></p>
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
<section id="segmentize-by-maximum-angle">
<span id="qgissegmentizebymaxangle"></span><h2><a class="toc-backref" href="#id367" role="doc-backlink"><span class="section-number">28.1.22.63. </span>Segmentize by maximum angle</a><a class="headerlink" href="#segmentize-by-maximum-angle" title="Link to this heading"></a></h2>
<p>Segmentizes a geometry by converting curved sections to linear
sections.</p>
<p>The segmentization is performed by specifying the maximum allowed
radius angle between vertices on the straightened geometry (e.g the
angle of the arc created from the original arc center to consecutive
output vertices on the linearized geometry).
Non-curved geometries will be retained without change.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissegmentizebymaxdistance"><span class="std std-ref">Segmentize by maximum distance</span></a>,
<a class="reference internal" href="#qgissimplifygeometries"><span class="std std-ref">Simplify</span></a>, <a class="reference internal" href="#qgissmoothgeometry"><span class="std std-ref">Smooth</span></a></p>
</div>
<section id="id186">
<h3>Parameters<a class="headerlink" href="#id186" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum angle between vertices (degrees)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ANGLE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 5.0</p>
</td>
<td><p>Maximum allowed radius angle between vertices
on the straightened geometry</p></td>
</tr>
<tr class="row-even"><td><p><strong>Segmentized</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer (with segmentized geometries).
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
<section id="id187">
<h3>Outputs<a class="headerlink" href="#id187" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Segmentized</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer with segmentized geometries</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id188">
<h3>Python code<a class="headerlink" href="#id188" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:segmentizebymaxangle</span></code></p>
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
<section id="segmentize-by-maximum-distance">
<span id="qgissegmentizebymaxdistance"></span><h2><a class="toc-backref" href="#id368" role="doc-backlink"><span class="section-number">28.1.22.64. </span>Segmentize by maximum distance</a><a class="headerlink" href="#segmentize-by-maximum-distance" title="Link to this heading"></a></h2>
<p>Segmentizes a geometry by converting curved sections to linear
sections.</p>
<p>The segmentization is performed by specifying the maximum allowed
offset distance between the original curve and the segmentized
representation.
Non-curved geometries will be retained without change.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissegmentizebymaxangle"><span class="std std-ref">Segmentize by maximum angle</span></a>,
<a class="reference internal" href="#qgissimplifygeometries"><span class="std std-ref">Simplify</span></a>, <a class="reference internal" href="#qgissmoothgeometry"><span class="std std-ref">Smooth</span></a></p>
</div>
<section id="id189">
<h3>Parameters<a class="headerlink" href="#id189" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum offset distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Maximum allowed offset distance between the
original curve and the segmentized representation,
in the layer units.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Segmentized</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer (with segmentized geometries).
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
<section id="id190">
<h3>Outputs<a class="headerlink" href="#id190" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Segmentized</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer with segmentized geometries</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id191">
<h3>Python code<a class="headerlink" href="#id191" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:segmentizebymaxdistance</span></code></p>
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
<section id="set-m-value">
<span id="qgissetmvalue"></span><h2><a class="toc-backref" href="#id369" role="doc-backlink"><span class="section-number">28.1.22.65. </span>Set M value</a><a class="headerlink" href="#set-m-value" title="Link to this heading"></a></h2>
<p>Sets the M value for geometries in a layer.</p>
<p>If M values already exist in the layer, they will be overwritten
with the new value.
If no M values exist, the geometry will be upgraded to include M
values and the specified value used as the initial M value for all
geometries.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features with M enabled</p>
<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p>Use the <a class="reference internal" href="../../../../_images/mActionIdentify.png"><img alt="identify" src="../../../../_images/mActionIdentify.png" style="width: 1.5em;" /></a><sup>Identify Features</sup> button to check
the added M value: the results are available in the
<span class="guilabel">Identify Results</span> dialog.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissetmfromraster"><span class="std std-ref">Set M value from raster</span></a>, <a class="reference internal" href="#qgissetzvalue"><span class="std std-ref">Set Z value</span></a>,
<a class="reference internal" href="#qgisdropmzvalues"><span class="std std-ref">Drop M/Z values</span></a></p>
</div>
<section id="id192">
<h3>Parameters<a class="headerlink" href="#id192" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>M Value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">M_VALUE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>M value to assign to the feature geometries</p></td>
</tr>
<tr class="row-even"><td><p><strong>M Added</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer.
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
<section id="id193">
<h3>Outputs<a class="headerlink" href="#id193" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>M Added</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (with M values assigned to the
geometries)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id194">
<h3>Python code<a class="headerlink" href="#id194" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:setmvalue</span></code></p>
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
<section id="set-m-value-from-raster">
<span id="qgissetmfromraster"></span><h2><a class="toc-backref" href="#id370" role="doc-backlink"><span class="section-number">28.1.22.66. </span>Set M value from raster</a><a class="headerlink" href="#set-m-value-from-raster" title="Link to this heading"></a></h2>
<p>Uses values sampled from a band within a raster layer to set the M
value for every overlapping vertex in the feature geometry.
The raster values can optionally be scaled by a preset amount.</p>
<p>If M values already exist in the layer, they will be overwritten with
the new value.
If no M values exist, the geometry will be upgraded to include M
values.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features with M enabled</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissetzfromraster"><span class="std std-ref">Drape (set Z value from raster)</span></a>, <a class="reference internal" href="#qgissetmvalue"><span class="std std-ref">Set M value</span></a></p>
</div>
<section id="id195">
<h3>Parameters<a class="headerlink" href="#id195" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Raster layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">RASTER</span></code></p></td>
<td><p>[raster]</p></td>
<td><p>Raster layer with M values</p></td>
</tr>
<tr class="row-even"><td><p><strong>Band number</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BAND</span></code></p></td>
<td><p>[raster band]</p>
<p>Default: 1</p>
</td>
<td><p>The raster band from which the M values are taken</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Value for NoData or non-intersecting vertices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">NODATA</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Value to use in case the vertex does not intersect
(a valid pixel of) the raster</p></td>
</tr>
<tr class="row-even"><td><p><strong>Scale factor</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SCALE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Scaling value: the band values are multiplied by this value.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Offset</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OFFSET</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Offset value: it is algebraically added to the band
values after applying the “Scale factor”.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Updated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer (with updated M values).
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
<section id="id196">
<h3>Outputs<a class="headerlink" href="#id196" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Updated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (with updated M values)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id197">
<h3>Python code<a class="headerlink" href="#id197" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:setmfromraster</span></code></p>
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
<section id="set-z-value">
<span id="qgissetzvalue"></span><h2><a class="toc-backref" href="#id371" role="doc-backlink"><span class="section-number">28.1.22.67. </span>Set Z value</a><a class="headerlink" href="#set-z-value" title="Link to this heading"></a></h2>
<p>Sets the Z value for geometries in a layer.</p>
<p>If Z values already exist in the layer, they will be overwritten
with the new value.
If no Z values exist, the geometry will be upgraded to include Z
values and the specified value used as the initial Z value for all
geometries.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features with Z enabled</p>
<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p>Use the <a class="reference internal" href="../../../../_images/mActionIdentify.png"><img alt="identify" src="../../../../_images/mActionIdentify.png" style="width: 1.5em;" /></a><sup>Identify Features</sup> button to check
the added Z value: the results are available in the
<span class="guilabel">Identify Results</span> dialog.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissetzfromraster"><span class="std std-ref">Drape (set Z value from raster)</span></a>, <a class="reference internal" href="#qgissetmvalue"><span class="std std-ref">Set M value</span></a>,
<a class="reference internal" href="#qgisdropmzvalues"><span class="std std-ref">Drop M/Z values</span></a></p>
</div>
<section id="id198">
<h3>Parameters<a class="headerlink" href="#id198" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Z Value</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">Z_VALUE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Z value to assign to the feature geometries</p></td>
</tr>
<tr class="row-even"><td><p><strong>Z Added</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer.
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
<section id="id199">
<h3>Outputs<a class="headerlink" href="#id199" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Z Added</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output vector layer (with Z values assigned)</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id200">
<h3>Python code<a class="headerlink" href="#id200" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:setzvalue</span></code></p>
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
<section id="simplify">
<span id="qgissimplifygeometries"></span><h2><a class="toc-backref" href="#id372" role="doc-backlink"><span class="section-number">28.1.22.68. </span>Simplify</a><a class="headerlink" href="#simplify" title="Link to this heading"></a></h2>
<p>Simplifies the geometries in a line or polygon layer.
It creates a new layer with the same features as the ones in the input
layer, but with geometries containing a lower number of vertices.</p>
<p>The algorithm gives a choice of simplification methods, including
distance based (the “Douglas-Peucker” algorithm), area based
(“Visvalingam” algorithm) and snapping geometries to grid.</p>
<figure class="align-center" id="id292">
<img alt="../../../../_images/simplify_geometries.png" src="../../../../_images/simplify_geometries.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.106 </span><span class="caption-text">From left to right, source layer and increasing simplification tolerances</span><a class="headerlink" href="#id292" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows <a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features</p>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissmoothgeometry"><span class="std std-ref">Smooth</span></a>, <a class="reference internal" href="#qgisdensifygeometries"><span class="std std-ref">Densify by count</span></a>,
<a class="reference internal" href="#qgisdensifygeometriesgivenaninterval"><span class="std std-ref">Densify by interval</span></a></p>
</div>
<section id="id201">
<h3>Parameters<a class="headerlink" href="#id201" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Simplification method</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">METHOD</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Simplification method. One of:</p>
<ul class="simple">
<li><p>0 — Distance (Douglas-Peucker)</p></li>
<li><p>1 — Snap to grid</p></li>
<li><p>2 — Area (Visvalingam)</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Tolerance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOLERANCE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Threshold tolerance (in units of the layer):
if the distance between two nodes is smaller than
the tolerance value, the segment will be simplified
and vertices will be removed.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Simplified</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (simplified) vector layer.
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
<section id="id202">
<h3>Outputs<a class="headerlink" href="#id202" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Simplified</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>The output (simplified) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id203">
<h3>Python code<a class="headerlink" href="#id203" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:simplifygeometries</span></code></p>
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
<section id="single-sided-buffer">
<span id="qgissinglesidedbuffer"></span><h2><a class="toc-backref" href="#id373" role="doc-backlink"><span class="section-number">28.1.22.69. </span>Single sided buffer</a><a class="headerlink" href="#single-sided-buffer" title="Link to this heading"></a></h2>
<p>Computes a buffer on lines by a specified distance on one side of
the line only.</p>
<p>Buffer always results in a polygon layer.</p>
<figure class="align-center" id="id293">
<img alt="../../../../_images/single_side_buffer.png" src="../../../../_images/single_side_buffer.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.107 </span><span class="caption-text">Left versus right side buffer on the same vector line layer</span><a class="headerlink" href="#id293" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisbuffer"><span class="std std-ref">Buffer</span></a></p>
</div>
<section id="id204">
<h3>Parameters<a class="headerlink" href="#id204" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Distance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DISTANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 10.0</p>
</td>
<td><p>Buffer distance.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Side</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SIDE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Which side to create the buffer on.
One of:</p>
<ul class="simple">
<li><p>0 – Left</p></li>
<li><p>1 – Right</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Segments</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEGMENTS</span></code></p></td>
<td><p>[number]</p>
<p>Default: 8</p>
</td>
<td><p>Controls the number of line segments to use to approximate
a quarter circle when creating rounded offsets.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Join style</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">JOIN_STYLE</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Specifies whether round, miter or beveled joins should be
used when offsetting corners in a line.
Options are:</p>
<ul class="simple">
<li><p>0 — Round</p></li>
<li><p>1 — Miter</p></li>
<li><p>2 — Bevel</p></li>
</ul>
<figure class="align-center" id="id294">
<a class="reference internal image-reference" href="../../../../_images/buffer_join_style.png"><img alt="../../../../_images/buffer_join_style.png" src="../../../../_images/buffer_join_style.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.108 </span><span class="caption-text">Round, miter, and bevel join styles</span><a class="headerlink" href="#id294" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-odd"><td><p><strong>Miter limit</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MITER_LIMIT</span></code></p></td>
<td><p>[number]</p>
<p>Default: 2.0</p>
</td>
<td><p>Sets the maximum distance from the offset geometry to use
when creating a mitered join as a factor of the offset distance (only applicable for miter
join styles).
Minimum: 1.0</p>
<figure class="align-center" id="id295">
<a class="reference internal image-reference" href="../../../../_images/buffer_miter_limit.png"><img alt="../../../../_images/buffer_miter_limit.png" src="../../../../_images/buffer_miter_limit.png" style="width: 100%;" /></a>
<figcaption>
<p><span class="caption-number">Fig. 28.109 </span><span class="caption-text">A 10m buffer with a limit of 2 and a 10m buffer with a limit of 1</span><a class="headerlink" href="#id295" title="Link to this image"></a></p>
</figcaption>
</figure>
</td>
</tr>
<tr class="row-even"><td><p><strong>Buffer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (buffer) layer.
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
<section id="id205">
<h3>Outputs<a class="headerlink" href="#id205" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Buffer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Output (buffer) polygon layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id206">
<h3>Python code<a class="headerlink" href="#id206" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:singlesidedbuffer</span></code></p>
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
<section id="smooth">
<span id="qgissmoothgeometry"></span><h2><a class="toc-backref" href="#id374" role="doc-backlink"><span class="section-number">28.1.22.70. </span>Smooth</a><a class="headerlink" href="#smooth" title="Link to this heading"></a></h2>
<p>Smooths the geometries in a line or polygon layer by
adding more <strong>vertices and corners</strong> to the feature geometries.</p>
<p>The iterations parameter dictates how many smoothing iterations will
be applied to each geometry.
A higher number of iterations results in smoother geometries with the
cost of greater number of nodes in the geometries.</p>
<figure class="align-center" id="id296">
<img alt="../../../../_images/smooth_geometry_1.png" src="../../../../_images/smooth_geometry_1.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.110 </span><span class="caption-text">Increasing number of iterations causes smoother geometries</span><a class="headerlink" href="#id296" title="Link to this image"></a></p>
</figcaption>
</figure>
<p>The offset parameter controls how “tightly” the smoothed geometries
follow the original geometries. Smaller values results in a tighter
fit, and larger values will create a looser fit.</p>
<figure class="align-center" id="id297">
<img alt="../../../../_images/smooth_geometry_2.png" src="../../../../_images/smooth_geometry_2.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.111 </span><span class="caption-text">Blue: the input layer. Offset 0.25 gives the red line, while
offset 0.50 gives the green line.</span><a class="headerlink" href="#id297" title="Link to this image"></a></p>
</figcaption>
</figure>
<p>The maximum angle parameter can be used to prevent smoothing of nodes
with large angles.
Any node where the angle of the segments to either side is larger than
this will not be smoothed. For example, setting the maximum angle to
90 degrees or lower would preserve right angles in the geometry.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissimplifygeometries"><span class="std std-ref">Simplify</span></a>,
<a class="reference internal" href="#qgisdensifygeometries"><span class="std std-ref">Densify by count</span></a>,
<a class="reference internal" href="#qgisdensifygeometriesgivenaninterval"><span class="std std-ref">Densify by interval</span></a></p>
</div>
<section id="id207">
<h3>Parameters<a class="headerlink" href="#id207" title="Link to this heading"></a></h3>
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
<td><p>[vector: line, polygon]</p></td>
<td><p>Input line or polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Iterations</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ITERATIONS</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1</p>
</td>
<td><p>Increasing the number of iterations will give smoother
geometries (and more vertices).</p></td>
</tr>
<tr class="row-even"><td><p><strong>Offset</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OFFSET</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.25</p>
</td>
<td><p>Increasing values will <em>move</em> the smoothed lines / boundaries
further away from the input lines / boundaries.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum node angle to smooth</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAX_ANGLE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 180.0</p>
</td>
<td><p>Every node below this value will be smoothed</p></td>
</tr>
<tr class="row-even"><td><p><strong>Smoothed</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (smoothed) layer.
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
<section id="id208">
<h3>Outputs<a class="headerlink" href="#id208" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Smoothed</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output (smoothed) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id209">
<h3>Python code<a class="headerlink" href="#id209" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:smoothgeometry</span></code></p>
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
<section id="snap-geometries-to-layer">
<span id="qgissnapgeometries"></span><h2><a class="toc-backref" href="#id375" role="doc-backlink"><span class="section-number">28.1.22.71. </span>Snap geometries to layer</a><a class="headerlink" href="#snap-geometries-to-layer" title="Link to this heading"></a></h2>
<p>Snaps the geometries in a layer either to the geometries from
another layer, or to geometries within the same layer.</p>
<p>Matching is done based on a tolerance distance, and vertices will be
inserted or removed as required to make the geometries match the
reference geometries.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissnappointstogrid"><span class="std std-ref">Snap points to grid</span></a></p>
</div>
<section id="id210">
<h3>Parameters<a class="headerlink" href="#id210" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Reference layer</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">REFERENCE_LAYER</span></code></p></td>
<td><p>[vector: any]</p></td>
<td><p>Vector layer to snap to</p></td>
</tr>
<tr class="row-even"><td><p><strong>Tolerance</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOLERANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 10.0</p>
</td>
<td><p>Control how close input vertices need to be to the
reference layer geometries before they are snapped.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Behavior</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BEHAVIOR</span></code></p></td>
<td><p>[enumeration]</p>
<p>Default: 0</p>
</td>
<td><p>Snapping can be done to an existing node or a
segment (its closest point to the vertex to move).
Available snapping options:</p>
<ul>
<li><p>0 — Prefer aligning nodes, insert extra vertices where
required</p>
<p>Prefer to snap to nodes, even when a segment may be closer
than a node. New nodes will be inserted to make geometries
follow each other exactly when inside allowable tolerance.</p>
</li>
<li><p>1 — Prefer closest point, insert extra vertices where
required</p>
<p>Snap to closest point, regardless of it is a node or a
segment. New nodes will be inserted to make geometries
follow each other exactly when inside allowable tolerance.</p>
</li>
<li><p>2 — Prefer aligning nodes, don’t insert new vertices</p>
<p>Prefer to snap to nodes, even when a segment may be closer
than a node. No new nodes will be inserted.</p>
</li>
<li><p>3 — Prefer closest point, don’t insert new vertices</p>
<p>Snap to closest point, regardless of it is a node or a
segment. No new nodes will be inserted.</p>
</li>
<li><p>4 — Move end points only, prefer aligning nodes</p>
<p>Only snap start/end points of lines (point features will
also be snapped, polygon features will not be modified),
prefer to snap to nodes.</p>
</li>
<li><p>5 — Move end points only, prefer closest point</p>
<p>Only snap start/end points of lines (point features will
also be snapped, polygon features will not be modified),
snap to closest point</p>
</li>
<li><p>6 — Snap end points to end points only</p>
<p>Only snap the start/end points of lines to other start/end points of lines</p>
</li>
<li><p>7 — Snap to anchor nodes (single layer only)</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Snapped geometry</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (snapped) layer.
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
<section id="id211">
<h3>Outputs<a class="headerlink" href="#id211" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Snapped geometry</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output (snapped) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id212">
<h3>Python code<a class="headerlink" href="#id212" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:snapgeometries</span></code></p>
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
<section id="snap-points-to-grid">
<span id="qgissnappointstogrid"></span><h2><a class="toc-backref" href="#id376" role="doc-backlink"><span class="section-number">28.1.22.72. </span>Snap points to grid</a><a class="headerlink" href="#snap-points-to-grid" title="Link to this heading"></a></h2>
<p>Modifies the coordinates of geometries in a vector layer, so that all
points or vertices are snapped to the closest point of a grid.</p>
<p>If the snapped geometry cannot be calculated (or is totally collapsed)
the feature’s geometry will be cleared.</p>
<p>Snapping can be performed on the X, Y, Z or M axis. A grid spacing of
0 for any axis will disable snapping for that axis.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Snapping to grid may generate an invalid geometry in some
corner cases.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgissnapgeometries"><span class="std std-ref">Snap geometries to layer</span></a></p>
</div>
<section id="id213">
<h3>Parameters<a class="headerlink" href="#id213" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>X Grid Spacing</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">HSPACING</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Grid spacing on the X axis</p></td>
</tr>
<tr class="row-even"><td><p><strong>Y Grid Spacing</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">VSPACING</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 1.0</p>
</td>
<td><p>Grid spacing on the Y axis</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Z Grid Spacing</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ZSPACING</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Grid spacing on the Z axis</p></td>
</tr>
<tr class="row-even"><td><p><strong>M Grid Spacing</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MSPACING</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Grid spacing on the M axis</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Snapped</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (snapped) layer.
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
<section id="id214">
<h3>Outputs<a class="headerlink" href="#id214" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Snapped</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output (snapped) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id215">
<h3>Python code<a class="headerlink" href="#id215" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:snappointstogrid</span></code></p>
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
<section id="split-lines-by-maximum-length">
<span id="qgissplitlinesbylength"></span><h2><a class="toc-backref" href="#id377" role="doc-backlink"><span class="section-number">28.1.22.73. </span>Split lines by maximum length</a><a class="headerlink" href="#split-lines-by-maximum-length" title="Link to this heading"></a></h2>
<p>Takes a line (or curve) layer and splits each feature into
multiple parts, where each part is of a specified maximum length.
Z and M values at the start and end of the new line substrings are
linearly interpolated from existing values.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of line features</p>
<section id="id216">
<h3>Parameters<a class="headerlink" href="#id216" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>The input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum line length</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">LENGTH</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 10.0</p>
</td>
<td><p>The maximum length of a line in the output.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Split</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output line vector layer.
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
<section id="id217">
<h3>Outputs<a class="headerlink" href="#id217" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Split</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>The new line vector layer - the length of the feature geometries
is less than or equal to the length specified in
the LENGTH parameter.</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id218">
<h3>Python code<a class="headerlink" href="#id218" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:splitlinesbylength</span></code></p>
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
<section id="subdivide">
<span id="qgissubdivide"></span><h2><a class="toc-backref" href="#id378" role="doc-backlink"><span class="section-number">28.1.22.74. </span>Subdivide</a><a class="headerlink" href="#subdivide" title="Link to this heading"></a></h2>
<p>Subdivides the geometry. The returned geometry will be a collection
containing subdivided parts from the original geometry, where no part
has more than the specified maximum number of nodes.</p>
<p>This is useful for dividing a complex geometry into less complex
parts, easier to spatially index and faster to perform spatial
operations.
Curved geometries will be segmentized before subdivision.</p>
<figure class="align-center" id="id298">
<img alt="../../../../_images/subdivide.png" src="../../../../_images/subdivide.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.112 </span><span class="caption-text">Left the input layer, middle maximum nodes value is 100 and right
maximum value is 200</span><a class="headerlink" href="#id298" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Subdividing a geometry can generate geometry parts that may
not be valid and may contain self-intersections.</p>
</div>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisexplodelines"><span class="std std-ref">Explode lines</span></a>, <a class="reference internal" href="#qgislinesubstring"><span class="std std-ref">Line substring</span></a></p>
</div>
<section id="id219">
<h3>Parameters<a class="headerlink" href="#id219" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>The input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Maximum nodes in parts</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">MAX_NODES</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 256</p>
</td>
<td><p>Maximum number of vertices each new
geometry part is allowed to have.
Fewer <em>sub-parts</em> for higher values.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Subdivided</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (subdivided) vector layer.
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
<section id="id220">
<h3>Outputs<a class="headerlink" href="#id220" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Subdivided</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id221">
<h3>Python code<a class="headerlink" href="#id221" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:subdivide</span></code></p>
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
<section id="swap-x-and-y-coordinates">
<span id="qgisswapxy"></span><h2><a class="toc-backref" href="#id379" role="doc-backlink"><span class="section-number">28.1.22.75. </span>Swap X and Y coordinates</a><a class="headerlink" href="#swap-x-and-y-coordinates" title="Link to this heading"></a></h2>
<p>Switches the X and Y coordinate values in input geometries.</p>
<p>It can be used to repair geometries which have accidentally had their
latitude and longitude values reversed.</p>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgistranslategeometry"><span class="std std-ref">Translate</span></a>, <a class="reference internal" href="#qgisrotatefeatures"><span class="std std-ref">Rotate</span></a></p>
</div>
<section id="id222">
<h3>Parameters<a class="headerlink" href="#id222" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>The input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Swapped</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer.
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
<section id="id223">
<h3>Outputs<a class="headerlink" href="#id223" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Swapped</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output (swapped) vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id224">
<h3>Python code<a class="headerlink" href="#id224" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:swapxy</span></code></p>
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
<section id="tapered-buffers">
<span id="qgistaperedbuffer"></span><h2><a class="toc-backref" href="#id380" role="doc-backlink"><span class="section-number">28.1.22.76. </span>Tapered buffers</a><a class="headerlink" href="#tapered-buffers" title="Link to this heading"></a></h2>
<p>Creates tapered buffer along line geometries, using a specified start
and end buffer diameter.</p>
<figure class="align-center" id="id299">
<img alt="../../../../_images/tapered_buffer.png" src="../../../../_images/tapered_buffer.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.113 </span><span class="caption-text">Tapered buffer example</span><a class="headerlink" href="#id299" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgisbufferbym"><span class="std std-ref">Variable width buffer (by M value)</span></a>, <a class="reference internal" href="#qgisbuffer"><span class="std std-ref">Buffer</span></a>,
<a class="reference internal" href="#qgiswedgebuffers"><span class="std std-ref">Create wedge buffers</span></a></p>
</div>
<section id="id225">
<h3>Parameters<a class="headerlink" href="#id225" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Start width</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">START_WIDTH</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Represents the radius of the buffer applied
at the start point of the line feature</p></td>
</tr>
<tr class="row-even"><td><p><strong>End width</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">END_WIDTH</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Represents the radius of the buffer applied
at the end point of the line feature.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Segments</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEGMENTS</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 16</p>
</td>
<td><p>Controls the number of line segments to use to approximate
a quarter circle when creating rounded offsets.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Buffered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (buffer) layer.
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
<section id="id226">
<h3>Outputs<a class="headerlink" href="#id226" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Buffered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Output (buffer) polygon layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id227">
<h3>Python code<a class="headerlink" href="#id227" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:taperedbuffer</span></code></p>
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
<section id="tessellate">
<span id="qgistessellate"></span><h2><a class="toc-backref" href="#id381" role="doc-backlink"><span class="section-number">28.1.22.77. </span>Tessellate</a><a class="headerlink" href="#tessellate" title="Link to this heading"></a></h2>
<p>Tessellates a polygon geometry layer, dividing the geometries into
triangular components.</p>
<p>The output layer consists of multipolygon geometries for each input
feature, with each multipolygon consisting of multiple triangle
component polygons.</p>
<figure class="align-center" id="id300">
<img alt="../../../../_images/tessellated.png" src="../../../../_images/tessellated.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.114 </span><span class="caption-text">Tessellated polygon (right)</span><a class="headerlink" href="#id300" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of polygon features</p>
<section id="id228">
<h3>Parameters<a class="headerlink" href="#id228" title="Link to this heading"></a></h3>
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
<td><p>[vector: polygon]</p></td>
<td><p>Input polygon vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Tesselated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output layer.
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
<section id="id229">
<h3>Outputs<a class="headerlink" href="#id229" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Tesselated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Output multipolygonZ layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id230">
<h3>Python code<a class="headerlink" href="#id230" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">3d:tessellate</span></code></p>
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
<section id="transect">
<span id="qgistransect"></span><h2><a class="toc-backref" href="#id382" role="doc-backlink"><span class="section-number">28.1.22.78. </span>Transect</a><a class="headerlink" href="#transect" title="Link to this heading"></a></h2>
<p>Creates transects on vertices for (multi)linestring.</p>
<p>A transect is a line oriented from an angle (by default perpendicular)
to the input polylines (at vertices).</p>
<p>Field(s) from feature(s) are returned in the transect with these
new fields:</p>
<ul class="simple">
<li><p>TR_FID: ID of the original feature</p></li>
<li><p>TR_ID: ID of the transect. Each transect have an unique ID</p></li>
<li><p>TR_SEGMENT: ID of the segment of the linestring</p></li>
<li><p>TR_ANGLE: Angle in degrees from the original line at the vertex</p></li>
<li><p>TR_LENGTH: Total length of the transect returned</p></li>
<li><p>TR_ORIENT: Side of the transect (only on the left or right of
the line, or both side)</p></li>
</ul>
<figure class="align-center" id="id301">
<img alt="../../../../_images/transect.png" src="../../../../_images/transect.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.115 </span><span class="caption-text">Dashed red lines represent the transect of the input line layer</span><a class="headerlink" href="#id301" title="Link to this image"></a></p>
</figcaption>
</figure>
<section id="id231">
<h3>Parameters<a class="headerlink" href="#id231" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Length of the transect</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">LENGTH</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 5.0</p>
</td>
<td><p>Length in map unit of the transect</p></td>
</tr>
<tr class="row-even"><td><p><strong>Angle in degrees from the original line at the vertices</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">ANGLE</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 90.0</p>
</td>
<td><p>Change the angle of the transect</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Side to create the transect</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SIDE</span></code></p></td>
<td><p>[enumeration]</p></td>
<td><p>Choose the side of the transect. Available options are:</p>
<ul class="simple">
<li><p>0 — Left</p></li>
<li><p>1 — Right</p></li>
<li><p>2 — Both</p></li>
</ul>
</td>
</tr>
<tr class="row-even"><td><p><strong>Transect</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output line layer.
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
<section id="id232">
<h3>Outputs<a class="headerlink" href="#id232" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Transect</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: line]</p></td>
<td><p>Output line layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id233">
<h3>Python code<a class="headerlink" href="#id233" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:transect</span></code></p>
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
<section id="translate">
<span id="qgistranslategeometry"></span><h2><a class="toc-backref" href="#id383" role="doc-backlink"><span class="section-number">28.1.22.79. </span>Translate</a><a class="headerlink" href="#translate" title="Link to this heading"></a></h2>
<p>Moves the geometries within a layer, by offsetting with a predefined
X and Y displacement.</p>
<p>Z and M values present in the geometry can also be translated.</p>
<figure class="align-center" id="id302">
<img alt="../../../../_images/translate_geometry.png" src="../../../../_images/translate_geometry.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.116 </span><span class="caption-text">Dashed lines represent the translated geometry of the input layer</span><a class="headerlink" href="#id302" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><a class="reference internal" href="../../../../_images/checkbox.png"><img alt="checkbox" src="../../../../_images/checkbox.png" style="width: 1.3em;" /></a> Allows
<a class="reference internal" href="../../working_with_vector/editing_geometry_attributes.html#processing-inplace-edit"><span class="std std-ref">features in-place modification</span></a>
of point, line, and polygon features</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="vectorcreation.html#qgisarraytranslatedfeatures"><span class="std std-ref">Array of translated features</span></a>,
<a class="reference internal" href="#qgisoffsetline"><span class="std std-ref">Offset lines</span></a>, <a class="reference internal" href="#qgisrotatefeatures"><span class="std std-ref">Rotate</span></a>, <a class="reference internal" href="#qgisswapxy"><span class="std std-ref">Swap X and Y coordinates</span></a></p>
</div>
<section id="id234">
<h3>Parameters<a class="headerlink" href="#id234" title="Link to this heading"></a></h3>
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
<td><p>[vector: any]</p></td>
<td><p>Input vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Offset distance (x-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_X</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Displacement to apply on the X axis</p></td>
</tr>
<tr class="row-even"><td><p><strong>Offset distance (y-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_Y</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Displacement to apply on the Y axis</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Offset distance (z-axis)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_Z</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Displacement to apply on the Z axis</p></td>
</tr>
<tr class="row-even"><td><p><strong>Offset distance (m values)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">DELTA_M</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 0.0</p>
</td>
<td><p>Displacement to apply on the M axis</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Translated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output vector layer.
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
<section id="id235">
<h3>Outputs<a class="headerlink" href="#id235" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Translated</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[same as input]</p></td>
<td><p>Output vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id236">
<h3>Python code<a class="headerlink" href="#id236" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:translategeometry</span></code></p>
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
<section id="variable-width-buffer-by-m-value">
<span id="qgisbufferbym"></span><h2><a class="toc-backref" href="#id384" role="doc-backlink"><span class="section-number">28.1.22.80. </span>Variable width buffer (by M value)</a><a class="headerlink" href="#variable-width-buffer-by-m-value" title="Link to this heading"></a></h2>
<p>Creates variable width buffers along lines, using the M value of the
line geometries as the diameter of the buffer at each vertex.</p>
<figure class="align-center" id="id303">
<img alt="../../../../_images/variable_buffer_m.png" src="../../../../_images/variable_buffer_m.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.117 </span><span class="caption-text">Variable buffer example</span><a class="headerlink" href="#id303" title="Link to this image"></a></p>
</figcaption>
</figure>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<p><a class="reference internal" href="#qgistaperedbuffer"><span class="std std-ref">Tapered buffers</span></a>, <a class="reference internal" href="#qgisbuffer"><span class="std std-ref">Buffer</span></a>,
<a class="reference internal" href="#qgissetmvalue"><span class="std std-ref">Set M value</span></a>, <a class="reference internal" href="modelertools.html#qgisvariabledistancebuffer"><span class="std std-ref">Variable distance buffer</span></a></p>
</div>
<section id="id237">
<h3>Parameters<a class="headerlink" href="#id237" title="Link to this heading"></a></h3>
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
<td><p>[vector: line]</p></td>
<td><p>Input line vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Segments</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">SEGMENTS</span></code></p></td>
<td><p>[number <a class="reference internal" href="../../../../_images/mIconDataDefine.png"><img alt="dataDefine" src="../../../../_images/mIconDataDefine.png" style="width: 1.5em;" /></a>]</p>
<p>Default: 16</p>
</td>
<td><p>Number of the buffer segments per quarter circle.
It can be a unique value (same value for all the features),
or it can be taken from features data (the value can
depend on feature attributes).</p></td>
</tr>
<tr class="row-even"><td><p><strong>Buffered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output (buffer) layer.
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
<section id="id238">
<h3>Outputs<a class="headerlink" href="#id238" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Buffered</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Variable buffer polygon layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id239">
<h3>Python code<a class="headerlink" href="#id239" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:bufferbym</span></code></p>
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
<section id="voronoi-polygons">
<span id="qgisvoronoipolygons"></span><h2><a class="toc-backref" href="#id385" role="doc-backlink"><span class="section-number">28.1.22.81. </span>Voronoi polygons</a><a class="headerlink" href="#voronoi-polygons" title="Link to this heading"></a></h2>
<p>Takes a point layer and generates a polygon layer containing
the Voronoi polygons (known also as Thiessen polygons) corresponding
to those input points.</p>
<p>Any location within a Voronoi polygon is closer to the associated
point than to any other point.</p>
<figure class="align-center" id="id304">
<img alt="../../../../_images/voronoi1.png" src="../../../../_images/voronoi1.png" />
<figcaption>
<p><span class="caption-number">Fig. 28.118 </span><span class="caption-text">Voronoi polygons</span><a class="headerlink" href="#id304" title="Link to this image"></a></p>
</figcaption>
</figure>
<p><strong>Default menu</strong>: <span class="menuselection">Vector ► Geometry Tools</span></p>
<section id="id240">
<h3>Parameters<a class="headerlink" href="#id240" title="Link to this heading"></a></h3>
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
<td><p>[vector: point]</p></td>
<td><p>Input point vector layer</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Buffer region (% of extent)</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">BUFFER</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.0</p>
</td>
<td><p>The extent of the output layer will be this much
bigger than the extent of the input layer</p></td>
</tr>
<tr class="row-even"><td><p><strong>Tolerance</strong></p>
<p>Optional</p>
</td>
<td><p><code class="docutils literal notranslate"><span class="pre">TOLERANCE</span></code></p></td>
<td><p>[number]</p>
<p>Default: 0.0</p>
</td>
<td><p>Specifies an optional snapping tolerance which can be used to improve the robustness of the voronoi.</p></td>
</tr>
<tr class="row-odd"><td><p><strong>Copy attributes from input features</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">COPY_ATTRIBUTES</span></code></p></td>
<td><p>[boolean]</p>
<p>Default: True</p>
</td>
<td><p>Specifies whether fields storing involved point features ID should be added to the output.
If False, an <code class="docutils literal notranslate"><span class="pre">id</span></code> field is created to identify the polygons.</p></td>
</tr>
<tr class="row-even"><td><p><strong>Voronoi polygons</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p>
<p>Default: <code class="docutils literal notranslate"><span class="pre">[Create</span> <span class="pre">temporary</span> <span class="pre">layer]</span></code></p>
</td>
<td><p>Specify the output layer (with the Voronoi polygons).
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
<section id="id241">
<h3>Outputs<a class="headerlink" href="#id241" title="Link to this heading"></a></h3>
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
<tr class="row-even"><td><p><strong>Voronoi polygons</strong></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">OUTPUT</span></code></p></td>
<td><p>[vector: polygon]</p></td>
<td><p>Voronoi polygons of the input point vector layer</p></td>
</tr>
</tbody>
</table>
</section>
<section id="id242">
<h3>Python code<a class="headerlink" href="#id242" title="Link to this heading"></a></h3>
<p><strong>Algorithm ID</strong>: <code class="docutils literal notranslate"><span class="pre">native:voronoipolygons</span></code></p>
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
        <a href="vectorgeneral.html" class="btn btn-neutral float-left" title="28.1.21. Vector general" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="vectoroverlay.html" class="btn btn-neutral float-right" title="28.1.23. Vector overlay" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
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
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">en</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/cs/docs/user_manual/processing_algs/qgis/vectorgeometry.html">cs</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/de/docs/user_manual/processing_algs/qgis/vectorgeometry.html">de</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/es/docs/user_manual/processing_algs/qgis/vectorgeometry.html">es</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/fr/docs/user_manual/processing_algs/qgis/vectorgeometry.html">fr</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/hu/docs/user_manual/processing_algs/qgis/vectorgeometry.html">hu</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/it/docs/user_manual/processing_algs/qgis/vectorgeometry.html">it</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ja/docs/user_manual/processing_algs/qgis/vectorgeometry.html">ja</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ko/docs/user_manual/processing_algs/qgis/vectorgeometry.html">ko</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/lt/docs/user_manual/processing_algs/qgis/vectorgeometry.html">lt</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/nl/docs/user_manual/processing_algs/qgis/vectorgeometry.html">nl</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_BR/docs/user_manual/processing_algs/qgis/vectorgeometry.html">pt_BR</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_PT/docs/user_manual/processing_algs/qgis/vectorgeometry.html">pt_PT</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ro/docs/user_manual/processing_algs/qgis/vectorgeometry.html">ro</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ru/docs/user_manual/processing_algs/qgis/vectorgeometry.html">ru</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/zh-Hans/docs/user_manual/processing_algs/qgis/vectorgeometry.html">zh-Hans</a></dd>
        
      </dl>

      <dl>
        <dt>Versions</dt>
        
          <dd><a href="https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">testing</a></dd>
        
          <dd><a href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">latest</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">3.40</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">3.34</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">3.28</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.22/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">3.22</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.16/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">3.16</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.10/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">3.10</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.4/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">3.4</a></dd>
        
          <dd><a href="https://docs.qgis.org/2.18/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html">2.18</a></dd>
        
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

