Title: Live Content

Description: Fetched live

Source: https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/index.html

---

<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="../../../../">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>28.1. QGIS algorithm provider &mdash; QGIS Documentation  documentation</title>
      <link rel="stylesheet" type="text/css" href="../../../../_static/pygments.css?v=80d5e7a1" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/css/qgis_docs.css?v=01847ad1" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/togglebutton.css?v=13237357" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/copybutton.css?v=76b2166b" />
      <link rel="stylesheet" type="text/css" href="../../../../_static/css/qgis_topbar.css?v=5613a779" />

  
    <link rel="shortcut icon" href="../../../../_static/qgis_logo.ico"/>
    <link rel="canonical" href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/index.html"/>
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
    <link rel="next" title="28.1.1. 3D Tiles" href="3dtiles.html" />
    <link rel="prev" title="28. Processing providers and algorithms" href="../index.html" />
  <meta name="description" content="QGIS 3.34 documentation: 28.1. QGIS algorithm provider">
  <meta name="robots" content="noindex">
</head>

<body class="wy-body-for-nav">

  <nav class="release_status_topbar">
    <div class="row outdated">
     This documentation is for a QGIS version which has reached end of life. Instead visit the <a href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/index.html">latest version</a>.
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
<li class="toctree-l3 current"><a class="current reference internal" href="#">28.1. QGIS algorithm provider</a><ul>
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
      <li class="breadcrumb-item active"><span class="section-number">28.1. </span>QGIS algorithm provider</li>

    <li style="float: right; text-align: right;">
	<ul>
		
      <li class="wy-breadcrumbs-aside">
            <a href="../../../../_sources/docs/user_manual/processing_algs/qgis/index.rst.txt" rel="nofollow"> View page source</a>
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
        <a href="../index.html" class="btn btn-neutral float-left" title="28. Processing providers and algorithms" accesskey="p"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="3dtiles.html" class="btn btn-neutral float-right" title="28.1.1. 3D Tiles" accesskey="n">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
  </div>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <blockquote>
<div></div></blockquote>
<section id="qgis-algorithm-provider">
<span id="qgis-algorithms"></span><h1><span class="section-number">28.1. </span>QGIS algorithm provider<a class="headerlink" href="#qgis-algorithm-provider" title="Link to this heading"></a></h1>
<p>QGIS algorithm provider implements various analysis and geoprocessing operations
using mostly only QGIS API. So almost all algorithms from this provider will work
“out of the box” without any additional configuration.</p>
<p>This provider incorporates some algorithms from plugins and also adds its own
algorithms.</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="3dtiles.html">28.1.1. 3D Tiles</a><ul>
<li class="toctree-l2"><a class="reference internal" href="3dtiles.html#convert-b3dm-to-gltf">28.1.1.1. Convert B3DM to GLTF</a></li>
<li class="toctree-l2"><a class="reference internal" href="3dtiles.html#convert-gltf-to-vector-features">28.1.1.2. Convert GLTF to vector features</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="cartography.html">28.1.2. Cartography</a><ul>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#align-points-to-features">28.1.2.1. Align points to features</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#combine-style-databases">28.1.2.2. Combine style databases</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#create-categorized-renderer-from-styles">28.1.2.3. Create categorized renderer from styles</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#create-style-database-from-project">28.1.2.4. Create style database from project</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#export-atlas-layout-as-image">28.1.2.5. Export atlas layout as image</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#export-atlas-layout-as-pdf-multiple-files">28.1.2.6. Export atlas layout as PDF (multiple files)</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#export-atlas-layout-as-pdf-single-file">28.1.2.7. Export atlas layout as PDF (single file)</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#export-print-layout-as-image">28.1.2.8. Export print layout as image</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#export-print-layout-as-pdf">28.1.2.9. Export print layout as PDF</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#extract-labels">28.1.2.10. Extract labels</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#print-layout-map-extent-to-layer">28.1.2.11. Print layout map extent to layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#set-layer-style">28.1.2.12. Set layer style</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#topological-coloring">28.1.2.13. Topological coloring</a></li>
<li class="toctree-l2"><a class="reference internal" href="cartography.html#transfer-annotations-from-main-layer">28.1.2.14. Transfer annotations from main layer</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="database.html">28.1.3. Database</a><ul>
<li class="toctree-l2"><a class="reference internal" href="database.html#export-to-postgresql">28.1.3.1. Export to PostgreSQL</a></li>
<li class="toctree-l2"><a class="reference internal" href="database.html#export-to-spatialite">28.1.3.2. Export to SpatiaLite</a></li>
<li class="toctree-l2"><a class="reference internal" href="database.html#package-layers">28.1.3.3. Package layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="database.html#postgresql-execute-and-load-sql">28.1.3.4. PostgreSQL execute and load SQL</a></li>
<li class="toctree-l2"><a class="reference internal" href="database.html#postgresql-execute-sql">28.1.3.5. PostgreSQL execute SQL</a></li>
<li class="toctree-l2"><a class="reference internal" href="database.html#spatialite-execute-sql">28.1.3.6. SpatiaLite execute SQL</a></li>
<li class="toctree-l2"><a class="reference internal" href="database.html#spatialite-execute-sql-registered-db">28.1.3.7. SpatiaLite execute SQL (registered DB)</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="filetools.html">28.1.4. File tools</a><ul>
<li class="toctree-l2"><a class="reference internal" href="filetools.html#download-file">28.1.4.1. Download file</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="gps.html">28.1.5. GPS</a><ul>
<li class="toctree-l2"><a class="reference internal" href="gps.html#convert-gps-data">28.1.5.1. Convert GPS data</a></li>
<li class="toctree-l2"><a class="reference internal" href="gps.html#convert-gpx-feature-type">28.1.5.2. Convert GPX feature type</a></li>
<li class="toctree-l2"><a class="reference internal" href="gps.html#download-gps-data-from-device">28.1.5.3. Download GPS data from device</a></li>
<li class="toctree-l2"><a class="reference internal" href="gps.html#upload-gps-data-to-device">28.1.5.4. Upload GPS data to device</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="interpolation.html">28.1.6. Interpolation</a><ul>
<li class="toctree-l2"><a class="reference internal" href="interpolation.html#heatmap-kernel-density-estimation">28.1.6.1. Heatmap (kernel density estimation)</a></li>
<li class="toctree-l2"><a class="reference internal" href="interpolation.html#qgisidwinterpolation">28.1.6.2. IDW Interpolation</a></li>
<li class="toctree-l2"><a class="reference internal" href="interpolation.html#line-density">28.1.6.3. Line Density</a></li>
<li class="toctree-l2"><a class="reference internal" href="interpolation.html#tin-interpolation">28.1.6.4. TIN Interpolation</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="layertools.html">28.1.7. Layer tools</a><ul>
<li class="toctree-l2"><a class="reference internal" href="layertools.html#export-layer-s-information">28.1.7.1. Export layer(s) information</a></li>
<li class="toctree-l2"><a class="reference internal" href="layertools.html#export-to-spreadsheet">28.1.7.2. Export to spreadsheet</a></li>
<li class="toctree-l2"><a class="reference internal" href="layertools.html#extract-layer-extent">28.1.7.3. Extract layer extent</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="mesh.html">28.1.8. Mesh</a><ul>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#export-contours">28.1.8.1. Export contours</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#export-cross-section-dataset-values-on-lines-from-mesh">28.1.8.2. Export cross section dataset values on lines from mesh</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#export-mesh-edges">28.1.8.3. Export mesh edges</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#export-mesh-faces">28.1.8.4. Export mesh faces</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#export-mesh-on-grid">28.1.8.5. Export mesh on grid</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#export-mesh-vertices">28.1.8.6. Export mesh vertices</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#export-time-series-values-from-points-of-a-mesh-dataset">28.1.8.7. Export time series values from points of a mesh dataset</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#rasterize-mesh-dataset">28.1.8.8. Rasterize mesh dataset</a></li>
<li class="toctree-l2"><a class="reference internal" href="mesh.html#tin-mesh-creation">28.1.8.9. TIN mesh creation</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="modelertools.html">28.1.9. Modeler tools</a><ul>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#calculate-expression">28.1.9.1. Calculate expression</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#conditional-branch">28.1.9.2. Conditional branch</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#create-directory">28.1.9.3. Create directory</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#feature-filter">28.1.9.4. Feature filter</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#filter-layers-by-type">28.1.9.5. Filter layers by type</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#load-layer-into-project">28.1.9.6. Load layer into project</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#raise-exception">28.1.9.7. Raise exception</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#raise-message">28.1.9.8. Raise message</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#raise-warning">28.1.9.9. Raise warning</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#rename-layer">28.1.9.10. Rename layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#save-log-to-file">28.1.9.11. Save log to file</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#set-project-variable">28.1.9.12. Set project variable</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#string-concatenation">28.1.9.13. String concatenation</a></li>
<li class="toctree-l2"><a class="reference internal" href="modelertools.html#variable-distance-buffer">28.1.9.14. Variable distance buffer</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="networkanalysis.html">28.1.10. Network analysis</a><ul>
<li class="toctree-l2"><a class="reference internal" href="networkanalysis.html#service-area-from-layer">28.1.10.1. Service area (from layer)</a></li>
<li class="toctree-l2"><a class="reference internal" href="networkanalysis.html#service-area-from-point">28.1.10.2. Service area (from point)</a></li>
<li class="toctree-l2"><a class="reference internal" href="networkanalysis.html#shortest-path-layer-to-point">28.1.10.3. Shortest path (layer to point)</a></li>
<li class="toctree-l2"><a class="reference internal" href="networkanalysis.html#shortest-path-point-to-layer">28.1.10.4. Shortest path (point to layer)</a></li>
<li class="toctree-l2"><a class="reference internal" href="networkanalysis.html#shortest-path-point-to-point">28.1.10.5. Shortest path (point to point)</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="plots.html">28.1.11. Plots</a><ul>
<li class="toctree-l2"><a class="reference internal" href="plots.html#bar-plot">28.1.11.1. Bar plot</a></li>
<li class="toctree-l2"><a class="reference internal" href="plots.html#box-plot">28.1.11.2. Box plot</a></li>
<li class="toctree-l2"><a class="reference internal" href="plots.html#mean-and-standard-deviation-plot">28.1.11.3. Mean and standard deviation plot</a></li>
<li class="toctree-l2"><a class="reference internal" href="plots.html#polar-plot">28.1.11.4. Polar plot</a></li>
<li class="toctree-l2"><a class="reference internal" href="plots.html#raster-layer-histogram">28.1.11.5. Raster layer histogram</a></li>
<li class="toctree-l2"><a class="reference internal" href="plots.html#vector-layer-histogram">28.1.11.6. Vector layer histogram</a></li>
<li class="toctree-l2"><a class="reference internal" href="plots.html#vector-layer-scatterplot">28.1.11.7. Vector layer scatterplot</a></li>
<li class="toctree-l2"><a class="reference internal" href="plots.html#vector-layer-scatterplot-3d">28.1.11.8. Vector layer scatterplot 3D</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="pointcloudconversion.html">28.1.12. Point Cloud Conversion</a><ul>
<li class="toctree-l2"><a class="reference internal" href="pointcloudconversion.html#convert-format">28.1.12.1. Convert format</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointcloudconversion.html#export-to-raster">28.1.12.2. Export to raster</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointcloudconversion.html#export-raster-using-triangulation">28.1.12.3. Export raster (using triangulation)</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointcloudconversion.html#export-to-vector">28.1.12.4. Export to vector</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="pointclouddatamanagement.html">28.1.13. Point Cloud Data Management</a><ul>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#assign-projection">28.1.13.1. Assign projection</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#build-virtual-point-cloud-vpc">28.1.13.2. Build virtual point cloud (VPC)</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#clip">28.1.13.3. Clip</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#create-copc">28.1.13.4. Create COPC</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#information">28.1.13.5. Information</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#merge">28.1.13.6. Merge</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#reproject">28.1.13.7. Reproject</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#thin-by-sampling-radius">28.1.13.8. Thin (by sampling radius)</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#thin-by-skipping-points">28.1.13.9. Thin (by skipping points)</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointclouddatamanagement.html#tile">28.1.13.10. Tile</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="pointcloudextraction.html">28.1.14. Point Cloud Extraction</a><ul>
<li class="toctree-l2"><a class="reference internal" href="pointcloudextraction.html#boundary">28.1.14.1. Boundary</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointcloudextraction.html#density">28.1.14.2. Density</a></li>
<li class="toctree-l2"><a class="reference internal" href="pointcloudextraction.html#filter">28.1.14.3. Filter</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="rasteranalysis.html">28.1.15. Raster analysis</a><ul>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#cell-stack-percent-rank-from-value">28.1.15.1. Cell stack percent rank from value</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#cell-stack-percentile">28.1.15.2. Cell stack percentile</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#cell-stack-percentrank-from-raster-layer">28.1.15.3. Cell stack percentrank from raster layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#cell-statistics">28.1.15.4. Cell statistics</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#equal-to-frequency">28.1.15.5. Equal to frequency</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#fuzzify-raster-gaussian-membership">28.1.15.6. Fuzzify raster (gaussian membership)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#fuzzify-raster-large-membership">28.1.15.7. Fuzzify raster (large membership)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#fuzzify-raster-linear-membership">28.1.15.8. Fuzzify raster (linear membership)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#fuzzify-raster-near-membership">28.1.15.9. Fuzzify raster (near membership)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#fuzzify-raster-power-membership">28.1.15.10. Fuzzify raster (power membership)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#fuzzify-raster-small-membership">28.1.15.11. Fuzzify raster (small membership)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#greater-than-frequency">28.1.15.12. Greater than frequency</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#highest-position-in-raster-stack">28.1.15.13. Highest position in raster stack</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#less-than-frequency">28.1.15.14. Less than frequency</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#lowest-position-in-raster-stack">28.1.15.15. Lowest position in raster stack</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-boolean-and">28.1.15.16. Raster boolean AND</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-boolean-or">28.1.15.17. Raster boolean OR</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-calculator">28.1.15.18. Raster calculator</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-calculator-virtual">28.1.15.19. Raster calculator (virtual)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-layer-properties">28.1.15.20. Raster layer properties</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-layer-statistics">28.1.15.21. Raster layer statistics</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-layer-unique-values-report">28.1.15.22. Raster layer unique values report</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-layer-zonal-statistics">28.1.15.23. Raster layer zonal statistics</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#raster-surface-volume">28.1.15.24. Raster surface volume</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#reclassify-by-layer">28.1.15.25. Reclassify by layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#reclassify-by-table">28.1.15.26. Reclassify by table</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#rescale-raster">28.1.15.27. Rescale raster</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#round-raster">28.1.15.28. Round raster</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#sample-raster-values">28.1.15.29. Sample raster values</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#zonal-histogram">28.1.15.30. Zonal histogram</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasteranalysis.html#zonal-statistics">28.1.15.31. Zonal statistics</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="rastercreation.html">28.1.16. Raster Creation</a><ul>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-constant-raster-layer">28.1.16.1. Create constant raster layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-binomial-distribution">28.1.16.2. Create random raster layer (binomial distribution)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-exponential-distribution">28.1.16.3. Create random raster layer (exponential distribution)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-gamma-distribution">28.1.16.4. Create random raster layer (gamma distribution)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-geometric-distribution">28.1.16.5. Create random raster layer (geometric distribution)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-negative-binomial-distribution">28.1.16.6. Create random raster layer (negative binomial distribution)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-normal-distribution">28.1.16.7. Create random raster layer (normal distribution)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-poisson-distribution">28.1.16.8. Create random raster layer (poisson distribution)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastercreation.html#create-random-raster-layer-uniform-distribution">28.1.16.9. Create random raster layer (uniform distribution)</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="rasterterrainanalysis.html">28.1.17. Raster terrain analysis</a><ul>
<li class="toctree-l2"><a class="reference internal" href="rasterterrainanalysis.html#aspect">28.1.17.1. Aspect</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasterterrainanalysis.html#dtm-filter-slope-based">28.1.17.2. DTM filter (slope-based)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasterterrainanalysis.html#hillshade">28.1.17.3. Hillshade</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasterterrainanalysis.html#hypsometric-curves">28.1.17.4. Hypsometric curves</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasterterrainanalysis.html#relief">28.1.17.5. Relief</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasterterrainanalysis.html#ruggedness-index">28.1.17.6. Ruggedness index</a></li>
<li class="toctree-l2"><a class="reference internal" href="rasterterrainanalysis.html#slope">28.1.17.7. Slope</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="rastertools.html">28.1.18. Raster tools</a><ul>
<li class="toctree-l2"><a class="reference internal" href="rastertools.html#align-raster">28.1.18.1. Align raster</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastertools.html#align-rasters">28.1.18.2. Align rasters</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastertools.html#convert-map-to-raster">28.1.18.3. Convert map to raster</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastertools.html#fill-nodata-cells">28.1.18.4. Fill NoData cells</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastertools.html#generate-xyz-tiles-directory">28.1.18.5. Generate XYZ tiles (Directory)</a></li>
<li class="toctree-l2"><a class="reference internal" href="rastertools.html#generate-xyz-tiles-mbtiles">28.1.18.6. Generate XYZ tiles (MBTiles)</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectoranalysis.html">28.1.19. Vector analysis</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#basic-statistics-for-fields">28.1.19.1. Basic statistics for fields</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#climb-along-line">28.1.19.2. Climb along line</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#count-points-in-polygon">28.1.19.3. Count points in polygon</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#dbscan-clustering">28.1.19.4. DBSCAN clustering</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#distance-matrix">28.1.19.5. Distance matrix</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#distance-to-nearest-hub-line-to-hub">28.1.19.6. Distance to nearest hub (line to hub)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#distance-to-nearest-hub-points">28.1.19.7. Distance to nearest hub (points)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#join-by-lines-hub-lines">28.1.19.8. Join by lines (hub lines)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#k-means-clustering">28.1.19.9. K-means clustering</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#list-unique-values">28.1.19.10. List unique values</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#mean-coordinate-s">28.1.19.11. Mean coordinate(s)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#nearest-neighbour-analysis">28.1.19.12. Nearest neighbour analysis</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#overlap-analysis">28.1.19.13. Overlap analysis</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#shortest-line-between-features">28.1.19.14. Shortest line between features</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#st-dbscan-clustering">28.1.19.15. ST-DBSCAN clustering</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#statistics-by-categories">28.1.19.16. Statistics by categories</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoranalysis.html#sum-line-lengths">28.1.19.17. Sum line lengths</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectorcreation.html">28.1.20. Vector creation</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#array-of-offset-parallel-lines">28.1.20.1. Array of offset (parallel) lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#array-of-translated-features">28.1.20.2. Array of translated features</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#create-grid">28.1.20.3. Create grid</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#create-points-layer-from-table">28.1.20.4. Create points layer from table</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#generate-points-pixel-centroids-along-line">28.1.20.5. Generate points (pixel centroids) along line</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#generate-points-pixel-centroids-inside-polygon">28.1.20.6. Generate points (pixel centroids) inside polygon</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#import-geotagged-photos">28.1.20.7. Import geotagged photos</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#points-to-path">28.1.20.8. Points to path</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#random-points-along-line">28.1.20.9. Random points along line</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#random-points-in-extent">28.1.20.10. Random points in extent</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#random-points-in-layer-bounds">28.1.20.11. Random points in layer bounds</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#random-points-in-polygons">28.1.20.12. Random points in polygons</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#random-points-inside-polygons">28.1.20.13. Random points inside polygons</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#random-points-on-lines">28.1.20.14. Random points on lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#raster-pixels-to-points">28.1.20.15. Raster pixels to points</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#raster-pixels-to-polygons">28.1.20.16. Raster pixels to polygons</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorcreation.html#regular-points">28.1.20.17. Regular points</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectorgeneral.html">28.1.21. Vector general</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#assign-projection">28.1.21.1. Assign projection</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#batch-nominatim-geocoder">28.1.21.2. Batch Nominatim geocoder</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#convert-layer-to-spatial-bookmarks">28.1.21.3. Convert layer to spatial bookmarks</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#convert-spatial-bookmarks-to-layer">28.1.21.4. Convert spatial bookmarks to layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#create-attribute-index">28.1.21.5. Create attribute index</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#create-spatial-index">28.1.21.6. Create spatial index</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#define-shapefile-projection">28.1.21.7. Define Shapefile projection</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#delete-duplicate-geometries">28.1.21.8. Delete duplicate geometries</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#delete-duplicates-by-attribute">28.1.21.9. Delete duplicates by attribute</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#detect-dataset-changes">28.1.21.10. Detect dataset changes</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#drop-geometries">28.1.21.11. Drop geometries</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#execute-sql">28.1.21.12. Execute SQL</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#export-layers-to-dxf">28.1.21.13. Export layers to DXF</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#extract-selected-features">28.1.21.14. Extract selected features</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#extract-shapefile-encoding">28.1.21.15. Extract Shapefile encoding</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#find-projection">28.1.21.16. Find projection</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#flatten-relationship">28.1.21.17. Flatten relationship</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#join-attributes-by-field-value">28.1.21.18. Join attributes by field value</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#join-attributes-by-location">28.1.21.19. Join attributes by location</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#join-attributes-by-location-summary">28.1.21.20. Join attributes by location (summary)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#join-attributes-by-nearest">28.1.21.21. Join attributes by nearest</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#merge-vector-layers">28.1.21.22. Merge vector layers</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#order-by-expression">28.1.21.23. Order by expression</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#repair-shapefile">28.1.21.24. Repair Shapefile</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#reproject-layer">28.1.21.25. Reproject layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#save-vector-features-to-file">28.1.21.26. Save vector features to file</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#set-layer-encoding">28.1.21.27. Set layer encoding</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#split-features-by-character">28.1.21.28. Split features by character</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#split-vector-layer">28.1.21.29. Split vector layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeneral.html#truncate-table">28.1.21.30. Truncate table</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectorgeometry.html">28.1.22. Vector geometry</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#add-geometry-attributes">28.1.22.1. Add geometry attributes</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#affine-transform">28.1.22.2. Affine transform</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#aggregate">28.1.22.3. Aggregate</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#boundary">28.1.22.4. Boundary</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#bounding-boxes">28.1.22.5. Bounding boxes</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#buffer">28.1.22.6. Buffer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#centroids">28.1.22.7. Centroids</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#check-validity">28.1.22.8. Check validity</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#collect-geometries">28.1.22.9. Collect geometries</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#concave-hull">28.1.22.10. Concave hull</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#convert-geometry-type">28.1.22.11. Convert geometry type</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#convert-to-curved-geometries">28.1.22.12. Convert to curved geometries</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#convex-hull">28.1.22.13. Convex hull</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#create-layer-from-extent">28.1.22.14. Create layer from extent</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#create-layer-from-point">28.1.22.15. Create layer from point</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#create-wedge-buffers">28.1.22.16. Create wedge buffers</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#delaunay-triangulation">28.1.22.17. Delaunay triangulation</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#delete-holes">28.1.22.18. Delete holes</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#densify-by-count">28.1.22.19. Densify by count</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#densify-by-interval">28.1.22.20. Densify by interval</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#dissolve">28.1.22.21. Dissolve</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#drape-set-z-value-from-raster">28.1.22.22. Drape (set Z value from raster)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#drop-m-z-values">28.1.22.23. Drop M/Z values</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#eliminate-selected-polygons">28.1.22.24. Eliminate selected polygons</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#explode-lines">28.1.22.25. Explode lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#extend-lines">28.1.22.26. Extend lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#extract-m-values">28.1.22.27. Extract M values</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#extract-specific-vertices">28.1.22.28. Extract specific vertices</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#extract-vertices">28.1.22.29. Extract vertices</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#extract-z-values">28.1.22.30. Extract Z values</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#filter-vertices-by-m-value">28.1.22.31. Filter vertices by M value</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#filter-vertices-by-z-value">28.1.22.32. Filter vertices by Z value</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#fix-geometries">28.1.22.33. Fix geometries</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#force-right-hand-rule">28.1.22.34. Force right-hand-rule</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#geodesic-line-split-at-antimeridian">28.1.22.35. Geodesic line split at antimeridian</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#geometry-by-expression">28.1.22.36. Geometry by expression</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#interpolate-point-on-line">28.1.22.37. Interpolate point on line</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#keep-n-biggest-parts">28.1.22.38. Keep N biggest parts</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#line-substring">28.1.22.39. Line substring</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#lines-to-polygons">28.1.22.40. Lines to polygons</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#merge-lines">28.1.22.41. Merge lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#minimum-bounding-geometry">28.1.22.42. Minimum bounding geometry</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#minimum-enclosing-circles">28.1.22.43. Minimum enclosing circles</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#multi-ring-buffer-constant-distance">28.1.22.44. Multi-ring buffer (constant distance)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#multipart-to-singleparts">28.1.22.45. Multipart to singleparts</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#offset-lines">28.1.22.46. Offset lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#oriented-minimum-bounding-box">28.1.22.47. Oriented minimum bounding box</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#orthogonalize">28.1.22.48. Orthogonalize</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#point-on-surface">28.1.22.49. Point on Surface</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#points-along-geometry">28.1.22.50. Points along geometry</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#points-displacement">28.1.22.51. Points displacement</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#pole-of-inaccessibility">28.1.22.52. Pole of inaccessibility</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#polygonize">28.1.22.53. Polygonize</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#polygons-to-lines">28.1.22.54. Polygons to lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#project-points-cartesian">28.1.22.55. Project points (Cartesian)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#promote-to-multipart">28.1.22.56. Promote to multipart</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#rectangles-ovals-diamonds">28.1.22.57. Rectangles, ovals, diamonds</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#remove-duplicate-vertices">28.1.22.58. Remove duplicate vertices</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#remove-null-geometries">28.1.22.59. Remove null geometries</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#reverse-line-direction">28.1.22.60. Reverse line direction</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#rotate">28.1.22.61. Rotate</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#roundness">28.1.22.62. Roundness</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#segmentize-by-maximum-angle">28.1.22.63. Segmentize by maximum angle</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#segmentize-by-maximum-distance">28.1.22.64. Segmentize by maximum distance</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#set-m-value">28.1.22.65. Set M value</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#set-m-value-from-raster">28.1.22.66. Set M value from raster</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#set-z-value">28.1.22.67. Set Z value</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#simplify">28.1.22.68. Simplify</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#single-sided-buffer">28.1.22.69. Single sided buffer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#smooth">28.1.22.70. Smooth</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#snap-geometries-to-layer">28.1.22.71. Snap geometries to layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#snap-points-to-grid">28.1.22.72. Snap points to grid</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#split-lines-by-maximum-length">28.1.22.73. Split lines by maximum length</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#subdivide">28.1.22.74. Subdivide</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#swap-x-and-y-coordinates">28.1.22.75. Swap X and Y coordinates</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#tapered-buffers">28.1.22.76. Tapered buffers</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#tessellate">28.1.22.77. Tessellate</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#transect">28.1.22.78. Transect</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#translate">28.1.22.79. Translate</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#variable-width-buffer-by-m-value">28.1.22.80. Variable width buffer (by M value)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorgeometry.html#voronoi-polygons">28.1.22.81. Voronoi polygons</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectoroverlay.html">28.1.23. Vector overlay</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#clip">28.1.23.1. Clip</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#difference">28.1.23.2. Difference</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#difference-multiple">28.1.23.3. Difference (multiple)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#extract-clip-by-extent">28.1.23.4. Extract/clip by extent</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#intersection">28.1.23.5. Intersection</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#intersection-multiple">28.1.23.6. Intersection (multiple)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#line-intersections">28.1.23.7. Line intersections</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#split-with-lines">28.1.23.8. Split with lines</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#symmetrical-difference">28.1.23.9. Symmetrical difference</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#union">28.1.23.10. Union</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectoroverlay.html#union-multiple">28.1.23.11. Union (multiple)</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectorselection.html">28.1.24. Vector selection</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#extract-by-attribute">28.1.24.1. Extract by attribute</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#extract-by-expression">28.1.24.2. Extract by expression</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#extract-by-location">28.1.24.3. Extract by location</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#extract-within-distance">28.1.24.4. Extract within distance</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#filter-by-geometry-type">28.1.24.5. Filter by geometry type</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#random-extract">28.1.24.6. Random extract</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#random-extract-within-subsets">28.1.24.7. Random extract within subsets</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#random-selection">28.1.24.8. Random selection</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#random-selection-within-subsets">28.1.24.9. Random selection within subsets</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#select-by-attribute">28.1.24.10. Select by attribute</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#select-by-expression">28.1.24.11. Select by expression</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#select-by-location">28.1.24.12. Select by location</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectorselection.html#select-within-distance">28.1.24.13. Select within distance</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectortable.html">28.1.25. Vector table</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#add-autoincremental-field">28.1.25.1. Add autoincremental field</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#add-field-to-attributes-table">28.1.25.2. Add field to attributes table</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#add-unique-value-index-field">28.1.25.3. Add unique value index field</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#add-x-y-fields-to-layer">28.1.25.4. Add X/Y fields to layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#advanced-python-field-calculator">28.1.25.5. Advanced Python field calculator</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#drop-field-s">28.1.25.6. Drop field(s)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#explode-hstore-field">28.1.25.7. Explode HStore Field</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#extract-binary-field">28.1.25.8. Extract binary field</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#field-calculator">28.1.25.9. Field calculator</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#refactor-fields">28.1.25.10. Refactor fields</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#rename-field">28.1.25.11. Rename field</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#retain-fields">28.1.25.12. Retain fields</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortable.html#text-to-float">28.1.25.13. Text to float</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="vectortiles.html">28.1.26. Vector Tiles</a><ul>
<li class="toctree-l2"><a class="reference internal" href="vectortiles.html#download-vector-tiles">28.1.26.1. Download vector tiles</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortiles.html#write-vector-tiles-mbtiles">28.1.26.2. Write vector tiles (MBTiles)</a></li>
<li class="toctree-l2"><a class="reference internal" href="vectortiles.html#write-vector-tiles-xyz">28.1.26.3. Write vector tiles (XYZ)</a></li>
</ul>
</li>
</ul>
</div>
</section>


           </div>
          </div>
          <footer><div class="rst-footer-buttons" role="navigation" aria-label="Footer">
        <a href="../index.html" class="btn btn-neutral float-left" title="28. Processing providers and algorithms" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="3dtiles.html" class="btn btn-neutral float-right" title="28.1.1. 3D Tiles" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
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
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/index.html">en</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/cs/docs/user_manual/processing_algs/qgis/index.html">cs</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/de/docs/user_manual/processing_algs/qgis/index.html">de</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/es/docs/user_manual/processing_algs/qgis/index.html">es</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/fr/docs/user_manual/processing_algs/qgis/index.html">fr</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/hu/docs/user_manual/processing_algs/qgis/index.html">hu</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/it/docs/user_manual/processing_algs/qgis/index.html">it</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ja/docs/user_manual/processing_algs/qgis/index.html">ja</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ko/docs/user_manual/processing_algs/qgis/index.html">ko</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/lt/docs/user_manual/processing_algs/qgis/index.html">lt</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/nl/docs/user_manual/processing_algs/qgis/index.html">nl</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_BR/docs/user_manual/processing_algs/qgis/index.html">pt_BR</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_PT/docs/user_manual/processing_algs/qgis/index.html">pt_PT</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ro/docs/user_manual/processing_algs/qgis/index.html">ro</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ru/docs/user_manual/processing_algs/qgis/index.html">ru</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/zh-Hans/docs/user_manual/processing_algs/qgis/index.html">zh-Hans</a></dd>
        
      </dl>

      <dl>
        <dt>Versions</dt>
        
          <dd><a href="https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/index.html">testing</a></dd>
        
          <dd><a href="https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/index.html">latest</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/index.html">3.40</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/index.html">3.34</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/index.html">3.28</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.22/en/docs/user_manual/processing_algs/qgis/index.html">3.22</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.16/en/docs/user_manual/processing_algs/qgis/index.html">3.16</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.10/en/docs/user_manual/processing_algs/qgis/index.html">3.10</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.4/en/docs/user_manual/processing_algs/qgis/index.html">3.4</a></dd>
        
          <dd><a href="https://docs.qgis.org/2.18/en/docs/user_manual/processing_algs/qgis/index.html">2.18</a></dd>
        
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

