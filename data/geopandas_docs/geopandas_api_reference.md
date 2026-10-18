Title: Live Content

Description: Fetched live

Source: https://geopandas.org/en/stable/docs/reference.html

---


<!DOCTYPE html>


<html lang="en" data-content_root="../" >

  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>API reference &#8212; GeoPandas 1.1.4+0.g91ec4af.dirty documentation</title>
  
  
  
  <script data-cfasync="false">
    document.documentElement.dataset.mode = localStorage.getItem("mode") || "";
    document.documentElement.dataset.theme = localStorage.getItem("theme") || "";
  </script>
  <!--
    this give us a css class that will be invisible only if js is disabled
  -->
  <noscript>
    <style>
      .pst-js-only { display: none !important; }

    </style>
  </noscript>
  
  <!-- Loaded before other Sphinx assets -->
  <link href="../_static/styles/theme.css?digest=a95f357e85573c9b56d5" rel="stylesheet" />
<link href="../_static/styles/pydata-sphinx-theme.css?digest=a95f357e85573c9b56d5" rel="stylesheet" />

    <link rel="stylesheet" type="text/css" href="../_static/pygments.css?v=03e43079" />
    <link rel="stylesheet" type="text/css" href="../_static/plot_directive.css" />
    <link rel="stylesheet" type="text/css" href="../_static/custom.css?v=165729ea" />
    <link rel="stylesheet" type="text/css" href="../_static/sg_gallery.css?v=fd6457a4" />
  
  <!-- So that users can add custom icons -->
  <script defer src="../_static/scripts/fontawesome.js?digest=a95f357e85573c9b56d5"></script>
  <!-- Pre-loaded scripts that we'll load fully later -->
  <link rel="preload" as="script" href="../_static/scripts/bootstrap.js?digest=a95f357e85573c9b56d5" />
<link rel="preload" as="script" href="../_static/scripts/pydata-sphinx-theme.js?digest=a95f357e85573c9b56d5" />

    <script src="../_static/documentation_options.js?v=1e19e3e2"></script>
    <script src="../_static/doctools.js?v=fd6eb6e6"></script>
    <script src="../_static/sphinx_highlight.js?v=6ffebe34"></script>
    <script src="../_static/toggleprompt.js?v=5801b3bb"></script>
    <script crossorigin="anonymous" integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"></script>
    <script>DOCUMENTATION_OPTIONS.pagename = 'docs/reference';</script>
    <script>DOCUMENTATION_OPTIONS.search_as_you_type = false;</script>
    <link rel="canonical" href="https://geopandas.org/en/stable/docs/reference.html" />
    <link rel="icon" href="../_static/favicon.png"/>
    <link rel="author" title="About these documents" href="../about.html" />
    <link rel="index" title="Index" href="../genindex.html" />
    <link rel="search" title="Search" href="../search.html" />
    <link rel="next" title="GeoSeries" href="reference/geoseries.html" />
    <link rel="prev" title="Migration from the Fiona to the Pyogrio read/write engine" href="user_guide/fiona_to_pyogrio.html" />
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="docsearch:language" content="en"/>
  <meta name="docsearch:version" content="1.1.4" />
  
    
    <script src="../_static/searchtools.js"></script>
    <script src="../_static/language_data.js"></script>
    <script src="../searchindex.js"></script>
  
  <script async type="text/javascript" src="/_/static/javascript/readthedocs-addons.js"></script><meta name="readthedocs-project-slug" content="geopandas" /><meta name="readthedocs-version-slug" content="stable" /><meta name="readthedocs-resolver-filename" content="/docs/reference.html" /><meta name="readthedocs-http-status" content="200" /></head>
  <body data-default-mode="">
  
  
  <div id="pst-skip-link" class="skip-link d-print-none"><a href="#main-content">Skip to main content</a></div>

  
  <div id="pst-scroll-pixel-helper"></div>
  
  <button type="button" class="btn rounded-pill" id="pst-back-to-top">
    <i class="fa-solid fa-arrow-up"></i>Back to top</button>
  
  
  
  
  <dialog id="pst-search-dialog">
    
<form class="bd-search d-flex align-items-center"
      action="../search.html"
      method="get">
  <i class="fa-solid fa-magnifying-glass"></i>
  <input type="search"
         class="form-control"
         name="q"
         placeholder="Search the docs ..."
         aria-label="Search the docs ..."
         autocomplete="off"
         autocorrect="off"
         autocapitalize="off"
         spellcheck="false"/>
  <span class="search-button__kbd-shortcut"><kbd class="kbd-shortcut__modifier">Ctrl</kbd>+<kbd>K</kbd></span>
</form>
  </dialog>

  <div class="pst-async-banner-revealer d-none">
  <aside id="bd-header-version-warning" class="d-none d-print-none" aria-label="Version warning"></aside>
</div>

  
    <header id="pst-header" class="bd-header navbar navbar-expand-lg bd-navbar d-print-none">
<div class="bd-header__inner bd-page-width">
  <button class="pst-navbar-icon sidebar-toggle primary-toggle" aria-label="Site navigation">
    <span class="fa-solid fa-bars"></span>
  </button>
  
  
  <div class="col-lg-3 navbar-header-items__start">
    
      <div class="navbar-item">

  
    
  

<a class="navbar-brand logo" href="../index.html">
  
  
  
  
  
    
    
      
    
    
    <img src="../_static/geopandas_logo_web.svg" class="logo__image only-light" alt="GeoPandas 1.1.4+0.g91ec4af.dirty documentation - Home"/>
    <img src="../_static/geopandas_logo_web.svg" class="logo__image only-dark pst-js-only" alt="GeoPandas 1.1.4+0.g91ec4af.dirty documentation - Home"/>
  
  
</a></div>
    
  </div>
  
  <div class="col-lg-9 navbar-header-items">
    
    <div class="me-auto navbar-header-items__center">
      
        <div class="navbar-item">
<nav>
  <ul class="bd-navbar-elements navbar-nav">
    
<li class="nav-item ">
  <a class="nav-link nav-internal" href="../index.html">
    Home
  </a>
</li>


<li class="nav-item ">
  <a class="nav-link nav-internal" href="../about.html">
    About
  </a>
</li>


<li class="nav-item ">
  <a class="nav-link nav-internal" href="../getting_started.html">
    Getting started
  </a>
</li>


<li class="nav-item current active">
  <a class="nav-link nav-internal" href="../docs.html">
    Documentation
  </a>
</li>


<li class="nav-item ">
  <a class="nav-link nav-internal" href="../community.html">
    Community
  </a>
</li>

  </ul>
</nav></div>
      
    </div>
    
    
    <div class="navbar-header-items__end">
      
        <div class="navbar-item navbar-persistent--container">
          

<button class="btn search-button-field search-button__button pst-js-only" title="Search" aria-label="Search" data-bs-placement="bottom" data-bs-toggle="tooltip">
 <i class="fa-solid fa-magnifying-glass"></i>
 <span class="search-button__default-text">Search</span>
 <span class="search-button__kbd-shortcut"><kbd class="kbd-shortcut__modifier">Ctrl</kbd>+<kbd class="kbd-shortcut__modifier">K</kbd></span>
</button>
        </div>
      
      
        <div class="navbar-item">

<div class="theme-switch-container dropdown pst-js-only" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Color mode">
  <button class="btn btn-sm nav-link pst-navbar-icon theme-switch-button dropdown-toggle" aria-label="Color mode" data-bs-toggle="dropdown">
    <i class="theme-switch fa-solid fa-sun fa-lg fa-fw" data-mode="light" title="Light"></i>
    <i class="theme-switch fa-solid fa-moon fa-lg fa-fw" data-mode="dark" title="Dark"></i>
    <i class="theme-switch fa-solid fa-circle-half-stroke fa-lg fa-fw" data-mode="auto" title="System Settings"></i>
  </button>
  <ul class="dropdown-menu dropdown-menu-end">
    <li><button class="dropdown-item d-flex align-items-center theme-change-button" data-mode="auto"><i class="fa-solid fa-circle-half-stroke fa-lg fa-fw me-1"></i>System Settings</button></li>
    <li><button class="dropdown-item d-flex align-items-center theme-change-button" data-mode="light"><i class="fa-solid fa-sun fa-lg fa-fw me-1"></i>Light</button></li>
    <li><button class="dropdown-item d-flex align-items-center theme-change-button" data-mode="dark"><i class="fa-solid fa-moon fa-lg fa-fw me-1"></i>Dark</button></li>
  </ul>
</div></div>
      
        <div class="navbar-item"><ul class="navbar-icon-links"
    aria-label="Icon Links">
        <li class="nav-item">
          
          
          
          
          
          
          
          
          <a href="https://github.com/geopandas/geopandas" title="GitHub" class="nav-link pst-navbar-icon" rel="noopener" target="_blank" data-bs-toggle="tooltip" data-bs-placement="bottom"><i class="fab fa-github-square fa-xl fa-lg" aria-hidden="true"></i><span class="visually-hidden">GitHub</span></a>
        </li>
</ul></div>
      
    </div>
    
  </div>
  
  
    <div class="navbar-persistent--mobile">

<button class="btn search-button-field search-button__button pst-js-only" title="Search" aria-label="Search" data-bs-placement="bottom" data-bs-toggle="tooltip">
 <i class="fa-solid fa-magnifying-glass"></i>
 <span class="search-button__default-text">Search</span>
 <span class="search-button__kbd-shortcut"><kbd class="kbd-shortcut__modifier">Ctrl</kbd>+<kbd class="kbd-shortcut__modifier">K</kbd></span>
</button>
    </div>
  

  
    <button class="pst-navbar-icon sidebar-toggle secondary-toggle" aria-label="On this page">
      <span class="fa-solid fa-outdent"></span>
    </button>
  
</div>

    </header>
  

  <div class="bd-container">
    <div class="bd-container__inner bd-page-width">
      
      
      
      <dialog id="pst-primary-sidebar-modal"></dialog>
      <div id="pst-primary-sidebar" class="bd-sidebar-primary bd-sidebar">
        

  
  <div class="sidebar-header-items sidebar-primary__section">
    
    
      <div class="sidebar-header-items__center">
        
          
          
            <div class="navbar-item">
<nav>
  <ul class="bd-navbar-elements navbar-nav">
    
<li class="nav-item ">
  <a class="nav-link nav-internal" href="../index.html">
    Home
  </a>
</li>


<li class="nav-item ">
  <a class="nav-link nav-internal" href="../about.html">
    About
  </a>
</li>


<li class="nav-item ">
  <a class="nav-link nav-internal" href="../getting_started.html">
    Getting started
  </a>
</li>


<li class="nav-item current active">
  <a class="nav-link nav-internal" href="../docs.html">
    Documentation
  </a>
</li>


<li class="nav-item ">
  <a class="nav-link nav-internal" href="../community.html">
    Community
  </a>
</li>

  </ul>
</nav></div>
          
        
      </div>
    
    
    
      <div class="sidebar-header-items__end">
        
          <div class="navbar-item">

<div class="theme-switch-container dropdown pst-js-only" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Color mode">
  <button class="btn btn-sm nav-link pst-navbar-icon theme-switch-button dropdown-toggle" aria-label="Color mode" data-bs-toggle="dropdown">
    <i class="theme-switch fa-solid fa-sun fa-lg fa-fw" data-mode="light" title="Light"></i>
    <i class="theme-switch fa-solid fa-moon fa-lg fa-fw" data-mode="dark" title="Dark"></i>
    <i class="theme-switch fa-solid fa-circle-half-stroke fa-lg fa-fw" data-mode="auto" title="System Settings"></i>
  </button>
  <ul class="dropdown-menu dropdown-menu-end">
    <li><button class="dropdown-item d-flex align-items-center theme-change-button" data-mode="auto"><i class="fa-solid fa-circle-half-stroke fa-lg fa-fw me-1"></i>System Settings</button></li>
    <li><button class="dropdown-item d-flex align-items-center theme-change-button" data-mode="light"><i class="fa-solid fa-sun fa-lg fa-fw me-1"></i>Light</button></li>
    <li><button class="dropdown-item d-flex align-items-center theme-change-button" data-mode="dark"><i class="fa-solid fa-moon fa-lg fa-fw me-1"></i>Dark</button></li>
  </ul>
</div></div>
        
          <div class="navbar-item"><ul class="navbar-icon-links"
    aria-label="Icon Links">
        <li class="nav-item">
          
          
          
          
          
          
          
          
          <a href="https://github.com/geopandas/geopandas" title="GitHub" class="nav-link pst-navbar-icon" rel="noopener" target="_blank" data-bs-toggle="tooltip" data-bs-placement="bottom"><i class="fab fa-github-square fa-xl fa-lg" aria-hidden="true"></i><span class="visually-hidden">GitHub</span></a>
        </li>
</ul></div>
        
      </div>
    
  </div>
  
    <div class="sidebar-primary-items__start sidebar-primary__section">
        <div class="sidebar-primary-item pst-sidebar-collapse"><button id="pst-collapse-sidebar-button" aria-expanded="true" aria-controls="pst-primary-sidebar"><svg class="pst-icon svg-inline--fa" role="img" aria-hidden="true" focusable="false" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
    <path fill="currentColor" d="M3 15.5C2.36232 15.5 1.74874 15.2564 1.28478 14.8189C0.820828 14.3815 0.541576 13.7832 0.504167 13.1467L0.5 13L0.5 3C0.499965 2.36232 0.743605 1.74874 1.18107 1.28478C1.61854 0.820828 2.21676 0.541576 2.85333 0.504167L3 0.5L13 0.5C13.6377 0.499965 14.2513 0.743605 14.7152 1.18107C15.1792 1.61854 15.4584 2.21676 15.4958 2.85333L15.5 3L15.5 13C15.5 13.6377 15.2564 14.2513 14.8189 14.7152C14.3815 15.1792 13.7832 15.4584 13.1467 15.4958L13 15.5L3 15.5ZM3 13.8333L10.5 13.8333L10.5 2.16667L3 2.16667C2.79589 2.16669 2.59889 2.24163 2.44636 2.37726C2.29383 2.5129 2.19638 2.69979 2.1725 2.9025L2.16667 3L2.16667 13C2.16669 13.2041 2.24163 13.4011 2.37726 13.5536C2.5129 13.7062 2.69979 13.8036 2.9025 13.8275L3 13.8333ZM6.65583 10.325L6.5775 10.2558L4.91083 8.58917C4.76735 8.44567 4.68116 8.25476 4.66843 8.05223C4.65569 7.84971 4.71729 7.6495 4.84167 7.48917L4.91083 7.41083L6.5775 5.74417C6.72747 5.59471 6.9287 5.50794 7.14032 5.50148C7.35194 5.49502 7.55809 5.56935 7.7169 5.70937C7.8757 5.8494 7.97525 6.04463 7.99533 6.25539C8.01541 6.46616 7.95451 6.67667 7.825 6.84417L7.75583 6.9225L6.67917 8L7.75583 9.0775C7.89931 9.22099 7.98551 9.41191 7.99824 9.61443C8.01097 9.81695 7.94938 10.0172 7.825 10.1775L7.75583 10.2558C7.61234 10.3993 7.42142 10.4855 7.2189 10.4982C7.01638 10.511 6.81617 10.4494 6.65583 10.325Z"/>
  </svg>
  <span class="pst-collapse-sidebar-label">Collapse Sidebar</span>
  <span class="pst-expand-sidebar-label">Expand Sidebar</span>
</button></div>
        <div class="sidebar-primary-item">

<nav class="bd-docs-nav bd-links"
     aria-label="Section Navigation">
  <p class="bd-links__title" role="heading" aria-level="1">Section Navigation</p>
  <div class="bd-toc-item navbar-nav"><p aria-level="2" class="caption" role="heading"><span class="caption-text">Documentation</span></p>
<ul class="current nav bd-sidenav">
<li class="toctree-l1 has-children"><a class="reference internal" href="user_guide.html">User guide</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l2"><a class="reference internal" href="user_guide/data_structures.html">Data structures</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/io.html">Reading and writing files</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/indexing.html">Indexing and selecting data</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/mapping.html">Making maps and plots</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/interactive_mapping.html">Interactive mapping</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/projections.html">Projections</a></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="user_guide/geometric_manipulations.html">Geometric manipulations</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul class="simple">
</ul>
</details></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="user_guide/set_operations.html">Set operations with overlay</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul class="simple">
</ul>
</details></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="user_guide/aggregation_with_dissolve.html">Aggregation with dissolve</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul class="simple">
</ul>
</details></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/mergingdata.html">Merging data</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/geocoding.html">Geocoding</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/sampling.html">Sampling points</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/how_to.html">How to...</a></li>
</ul>
</details></li>
<li class="toctree-l1 has-children"><a class="reference internal" href="advanced_guide.html">Advanced guide</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l2"><a class="reference internal" href="user_guide/spatial_indexing.html">Spatial indexing</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/missing_empty.html">Missing and empty geometries</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/reproject_fiona.html">Re-projecting using GDAL with Rasterio and Fiona</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/pygeos_to_shapely.html">Migration from PyGEOS geometry backend to Shapely 2.0</a></li>
<li class="toctree-l2"><a class="reference internal" href="user_guide/fiona_to_pyogrio.html">Migration from the Fiona to the Pyogrio read/write engine</a></li>
</ul>
</details></li>
<li class="toctree-l1 current active has-children"><a class="current reference internal" href="#">API reference</a><details open="open"><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l2 has-children"><a class="reference internal" href="reference/geoseries.html">GeoSeries</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.html">geopandas.GeoSeries</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.area.html">geopandas.GeoSeries.area</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.boundary.html">geopandas.GeoSeries.boundary</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.bounds.html">geopandas.GeoSeries.bounds</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.total_bounds.html">geopandas.GeoSeries.total_bounds</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.length.html">geopandas.GeoSeries.length</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.geom_type.html">geopandas.GeoSeries.geom_type</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.offset_curve.html">geopandas.GeoSeries.offset_curve</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.distance.html">geopandas.GeoSeries.distance</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.hausdorff_distance.html">geopandas.GeoSeries.hausdorff_distance</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.frechet_distance.html">geopandas.GeoSeries.frechet_distance</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.representative_point.html">geopandas.GeoSeries.representative_point</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.exterior.html">geopandas.GeoSeries.exterior</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.interiors.html">geopandas.GeoSeries.interiors</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.minimum_bounding_radius.html">geopandas.GeoSeries.minimum_bounding_radius</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.minimum_clearance.html">geopandas.GeoSeries.minimum_clearance</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.x.html">geopandas.GeoSeries.x</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.y.html">geopandas.GeoSeries.y</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.z.html">geopandas.GeoSeries.z</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.m.html">geopandas.GeoSeries.m</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.get_coordinates.html">geopandas.GeoSeries.get_coordinates</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.count_coordinates.html">geopandas.GeoSeries.count_coordinates</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.count_geometries.html">geopandas.GeoSeries.count_geometries</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.count_interior_rings.html">geopandas.GeoSeries.count_interior_rings</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.set_precision.html">geopandas.GeoSeries.set_precision</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.get_precision.html">geopandas.GeoSeries.get_precision</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.get_geometry.html">geopandas.GeoSeries.get_geometry</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_closed.html">geopandas.GeoSeries.is_closed</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_empty.html">geopandas.GeoSeries.is_empty</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_ring.html">geopandas.GeoSeries.is_ring</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_simple.html">geopandas.GeoSeries.is_simple</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_valid.html">geopandas.GeoSeries.is_valid</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_valid_reason.html">geopandas.GeoSeries.is_valid_reason</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_valid_coverage.html">geopandas.GeoSeries.is_valid_coverage</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.invalid_coverage_edges.html">geopandas.GeoSeries.invalid_coverage_edges</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.has_m.html">geopandas.GeoSeries.has_m</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.has_z.html">geopandas.GeoSeries.has_z</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.is_ccw.html">geopandas.GeoSeries.is_ccw</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.contains.html">geopandas.GeoSeries.contains</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.contains_properly.html">geopandas.GeoSeries.contains_properly</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.crosses.html">geopandas.GeoSeries.crosses</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.disjoint.html">geopandas.GeoSeries.disjoint</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.dwithin.html">geopandas.GeoSeries.dwithin</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.geom_equals.html">geopandas.GeoSeries.geom_equals</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.geom_equals_exact.html">geopandas.GeoSeries.geom_equals_exact</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.geom_equals_identical.html">geopandas.GeoSeries.geom_equals_identical</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.intersects.html">geopandas.GeoSeries.intersects</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.overlaps.html">geopandas.GeoSeries.overlaps</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.touches.html">geopandas.GeoSeries.touches</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.within.html">geopandas.GeoSeries.within</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.covers.html">geopandas.GeoSeries.covers</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.covered_by.html">geopandas.GeoSeries.covered_by</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.relate.html">geopandas.GeoSeries.relate</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.relate_pattern.html">geopandas.GeoSeries.relate_pattern</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.clip_by_rect.html">geopandas.GeoSeries.clip_by_rect</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.difference.html">geopandas.GeoSeries.difference</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.intersection.html">geopandas.GeoSeries.intersection</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.symmetric_difference.html">geopandas.GeoSeries.symmetric_difference</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.union.html">geopandas.GeoSeries.union</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.boundary.html">geopandas.GeoSeries.boundary</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.buffer.html">geopandas.GeoSeries.buffer</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.centroid.html">geopandas.GeoSeries.centroid</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.concave_hull.html">geopandas.GeoSeries.concave_hull</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.convex_hull.html">geopandas.GeoSeries.convex_hull</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.envelope.html">geopandas.GeoSeries.envelope</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.extract_unique_points.html">geopandas.GeoSeries.extract_unique_points</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.force_2d.html">geopandas.GeoSeries.force_2d</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.force_3d.html">geopandas.GeoSeries.force_3d</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.make_valid.html">geopandas.GeoSeries.make_valid</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.minimum_bounding_circle.html">geopandas.GeoSeries.minimum_bounding_circle</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.maximum_inscribed_circle.html">geopandas.GeoSeries.maximum_inscribed_circle</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.minimum_clearance.html">geopandas.GeoSeries.minimum_clearance</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.minimum_clearance_line.html">geopandas.GeoSeries.minimum_clearance_line</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.minimum_rotated_rectangle.html">geopandas.GeoSeries.minimum_rotated_rectangle</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.normalize.html">geopandas.GeoSeries.normalize</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.orient_polygons.html">geopandas.GeoSeries.orient_polygons</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.remove_repeated_points.html">geopandas.GeoSeries.remove_repeated_points</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.reverse.html">geopandas.GeoSeries.reverse</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.sample_points.html">geopandas.GeoSeries.sample_points</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.segmentize.html">geopandas.GeoSeries.segmentize</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.shortest_line.html">geopandas.GeoSeries.shortest_line</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.simplify.html">geopandas.GeoSeries.simplify</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.simplify_coverage.html">geopandas.GeoSeries.simplify_coverage</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.snap.html">geopandas.GeoSeries.snap</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.transform.html">geopandas.GeoSeries.transform</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.affine_transform.html">geopandas.GeoSeries.affine_transform</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.rotate.html">geopandas.GeoSeries.rotate</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.scale.html">geopandas.GeoSeries.scale</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.skew.html">geopandas.GeoSeries.skew</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.translate.html">geopandas.GeoSeries.translate</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.interpolate.html">geopandas.GeoSeries.interpolate</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.line_merge.html">geopandas.GeoSeries.line_merge</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.project.html">geopandas.GeoSeries.project</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.shared_paths.html">geopandas.GeoSeries.shared_paths</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.build_area.html">geopandas.GeoSeries.build_area</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.constrained_delaunay_triangles.html">geopandas.GeoSeries.constrained_delaunay_triangles</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.delaunay_triangles.html">geopandas.GeoSeries.delaunay_triangles</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.explode.html">geopandas.GeoSeries.explode</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.intersection_all.html">geopandas.GeoSeries.intersection_all</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.polygonize.html">geopandas.GeoSeries.polygonize</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.union_all.html">geopandas.GeoSeries.union_all</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.voronoi_polygons.html">geopandas.GeoSeries.voronoi_polygons</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.from_arrow.html">geopandas.GeoSeries.from_arrow</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.from_file.html">geopandas.GeoSeries.from_file</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.from_wkb.html">geopandas.GeoSeries.from_wkb</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.from_wkt.html">geopandas.GeoSeries.from_wkt</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.from_xy.html">geopandas.GeoSeries.from_xy</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.to_arrow.html">geopandas.GeoSeries.to_arrow</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.to_file.html">geopandas.GeoSeries.to_file</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.to_json.html">geopandas.GeoSeries.to_json</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.to_wkb.html">geopandas.GeoSeries.to_wkb</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.to_wkt.html">geopandas.GeoSeries.to_wkt</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.crs.html">geopandas.GeoSeries.crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.set_crs.html">geopandas.GeoSeries.set_crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.to_crs.html">geopandas.GeoSeries.to_crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.estimate_utm_crs.html">geopandas.GeoSeries.estimate_utm_crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.fillna.html">geopandas.GeoSeries.fillna</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.isna.html">geopandas.GeoSeries.isna</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.notna.html">geopandas.GeoSeries.notna</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.clip.html">geopandas.GeoSeries.clip</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.plot.html">geopandas.GeoSeries.plot</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.explore.html">geopandas.GeoSeries.explore</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.sindex.html">geopandas.GeoSeries.sindex</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.has_sindex.html">geopandas.GeoSeries.has_sindex</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.cx.html">geopandas.GeoSeries.cx</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.__geo_interface__.html">geopandas.GeoSeries.__geo_interface__</a></li>
</ul>
</details></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="reference/geodataframe.html">GeoDataFrame</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.html">geopandas.GeoDataFrame</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.from_file.html">geopandas.GeoDataFrame.from_file</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.from_features.html">geopandas.GeoDataFrame.from_features</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.from_postgis.html">geopandas.GeoDataFrame.from_postgis</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.from_arrow.html">geopandas.GeoDataFrame.from_arrow</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_file.html">geopandas.GeoDataFrame.to_file</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_json.html">geopandas.GeoDataFrame.to_json</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_geo_dict.html">geopandas.GeoDataFrame.to_geo_dict</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_parquet.html">geopandas.GeoDataFrame.to_parquet</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_arrow.html">geopandas.GeoDataFrame.to_arrow</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_feather.html">geopandas.GeoDataFrame.to_feather</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_postgis.html">geopandas.GeoDataFrame.to_postgis</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_wkb.html">geopandas.GeoDataFrame.to_wkb</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_wkt.html">geopandas.GeoDataFrame.to_wkt</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.crs.html">geopandas.GeoDataFrame.crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.set_crs.html">geopandas.GeoDataFrame.set_crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_crs.html">geopandas.GeoDataFrame.to_crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.estimate_utm_crs.html">geopandas.GeoDataFrame.estimate_utm_crs</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.rename_geometry.html">geopandas.GeoDataFrame.rename_geometry</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.set_geometry.html">geopandas.GeoDataFrame.set_geometry</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.active_geometry_name.html">geopandas.GeoDataFrame.active_geometry_name</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.dissolve.html">geopandas.GeoDataFrame.dissolve</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.explode.html">geopandas.GeoDataFrame.explode</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.sjoin.html">geopandas.GeoDataFrame.sjoin</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.sjoin_nearest.html">geopandas.GeoDataFrame.sjoin_nearest</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.clip.html">geopandas.GeoDataFrame.clip</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.overlay.html">geopandas.GeoDataFrame.overlay</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.explore.html">geopandas.GeoDataFrame.explore</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.plot.html">geopandas.GeoDataFrame.plot</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.sindex.html">geopandas.GeoDataFrame.sindex</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.has_sindex.html">geopandas.GeoDataFrame.has_sindex</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.cx.html">geopandas.GeoDataFrame.cx</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.__geo_interface__.html">geopandas.GeoDataFrame.__geo_interface__</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.iterfeatures.html">geopandas.GeoDataFrame.iterfeatures</a></li>
</ul>
</details></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="reference/io.html">Input/output</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.list_layers.html">geopandas.list_layers</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.read_file.html">geopandas.read_file</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_file.html">geopandas.GeoDataFrame.to_file</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.read_postgis.html">geopandas.read_postgis</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_postgis.html">geopandas.GeoDataFrame.to_postgis</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.read_feather.html">geopandas.read_feather</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_feather.html">geopandas.GeoDataFrame.to_feather</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.read_parquet.html">geopandas.read_parquet</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoDataFrame.to_parquet.html">geopandas.GeoDataFrame.to_parquet</a></li>
</ul>
</details></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="reference/tools.html">Tools</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sjoin.html">geopandas.sjoin</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sjoin_nearest.html">geopandas.sjoin_nearest</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.overlay.html">geopandas.overlay</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.clip.html">geopandas.clip</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.tools.geocode.html">geopandas.tools.geocode</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.tools.reverse_geocode.html">geopandas.tools.reverse_geocode</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.tools.collect.html">geopandas.tools.collect</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.points_from_xy.html">geopandas.points_from_xy</a></li>
</ul>
</details></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="reference/sindex.html">Spatial index</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.GeoSeries.sindex.html">geopandas.GeoSeries.sindex</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sindex.SpatialIndex.intersection.html">geopandas.sindex.SpatialIndex.intersection</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sindex.SpatialIndex.is_empty.html">geopandas.sindex.SpatialIndex.is_empty</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sindex.SpatialIndex.nearest.html">geopandas.sindex.SpatialIndex.nearest</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sindex.SpatialIndex.query.html">geopandas.sindex.SpatialIndex.query</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sindex.SpatialIndex.size.html">geopandas.sindex.SpatialIndex.size</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.sindex.SpatialIndex.valid_query_predicates.html">geopandas.sindex.SpatialIndex.valid_query_predicates</a></li>
</ul>
</details></li>
<li class="toctree-l2 has-children"><a class="reference internal" href="reference/testing.html">Testing</a><details><summary><span class="toctree-toggle" role="presentation"><i class="fa-solid fa-chevron-down"></i></span></summary><ul>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.testing.assert_geoseries_equal.html">geopandas.testing.assert_geoseries_equal</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference/api/geopandas.testing.assert_geodataframe_equal.html">geopandas.testing.assert_geodataframe_equal</a></li>
</ul>
</details></li>
</ul>
</details></li>
<li class="toctree-l1"><a class="reference internal" href="changelog.html">Changelog</a></li>
</ul>
</div>
</nav></div>
    </div>
  
  
  <div class="sidebar-primary-items__end sidebar-primary__section">
      <div class="sidebar-primary-item">
<div id="ethical-ad-placement"
      class="flat"
      data-ea-publisher="readthedocs"
      data-ea-type="readthedocs-sidebar"
      data-ea-manual="true">
</div></div>
  </div>


      </div>
      
      <main id="main-content" class="bd-main" role="main">
        
        
          <div class="bd-content">
            <div class="bd-article-container">
              
              <div class="bd-header-article d-print-none">
<div class="header-article-items header-article__inner">
  
    <div class="header-article-items__start">
      
        <div class="header-article-item">

<nav aria-label="Breadcrumb" class="d-print-none">
  <ul class="bd-breadcrumbs">
    
    <li class="breadcrumb-item breadcrumb-home">
      <a href="../index.html" class="nav-link" aria-label="Home">
        <i class="fa-solid fa-home"></i>
      </a>
    </li>
    
    <li class="breadcrumb-item"><a href="../docs.html" class="nav-link">Documentation</a></li>
    
    <li class="breadcrumb-item active" aria-current="page"><span class="ellipsis">API reference</span></li>
  </ul>
</nav>
</div>
      
    </div>
  
  
</div>
</div>
              
              
              
                
<div id="searchbox"></div>
                <article class="bd-article">
                  
  <section id="api-reference">
<span id="reference"></span><h1>API reference<a class="headerlink" href="#api-reference" title="Link to this heading">#</a></h1>
<p>The API reference provides an overview of all public objects, functions and methods implemented in GeoPandas. All classes and function exposed in <code class="docutils literal notranslate"><span class="pre">geopandas.*</span></code> namespace plus those listed in the reference are public.</p>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>The <code class="docutils literal notranslate"><span class="pre">geopandas.array</span></code> and <code class="docutils literal notranslate"><span class="pre">geopandas.base</span></code> modules are private. Stable functionality in such modules is not guaranteed.</p>
</div>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="reference/geoseries.html">GeoSeries</a><ul>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#constructor">Constructor</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#general-methods-and-attributes">General methods and attributes</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#unary-predicates">Unary predicates</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#binary-predicates">Binary predicates</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#set-theoretic-methods">Set-theoretic methods</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#constructive-methods-and-attributes">Constructive methods and attributes</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#affine-transformations">Affine transformations</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#linestring-operations">Linestring operations</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#aggregating-and-exploding">Aggregating and exploding</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#serialization-io-conversion">Serialization / IO / conversion</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#projection-handling">Projection handling</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#missing-values">Missing values</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#overlay-operations">Overlay operations</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#plotting">Plotting</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#spatial-index">Spatial index</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#indexing">Indexing</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geoseries.html#interface">Interface</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="reference/geodataframe.html">GeoDataFrame</a><ul>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#constructor">Constructor</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#serialization-io-conversion">Serialization / IO / conversion</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#projection-handling">Projection handling</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#active-geometry-handling">Active geometry handling</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#aggregating-and-exploding">Aggregating and exploding</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#spatial-joins">Spatial joins</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#overlay-operations">Overlay operations</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#plotting">Plotting</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#spatial-index">Spatial index</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#indexing">Indexing</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/geodataframe.html#interface">Interface</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="reference/io.html">Input/output</a><ul>
<li class="toctree-l2"><a class="reference internal" href="reference/io.html#gis-vector-files">GIS vector files</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/io.html#postgis">PostGIS</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/io.html#feather">Feather</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/io.html#parquet">Parquet</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="reference/tools.html">Tools</a><ul>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.sjoin.html">geopandas.sjoin</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.sjoin_nearest.html">geopandas.sjoin_nearest</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.overlay.html">geopandas.overlay</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.clip.html">geopandas.clip</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.tools.geocode.html">geopandas.tools.geocode</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.tools.reverse_geocode.html">geopandas.tools.reverse_geocode</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.tools.collect.html">geopandas.tools.collect</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.points_from_xy.html">geopandas.points_from_xy</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="reference/sindex.html">Spatial index</a><ul>
<li class="toctree-l2"><a class="reference internal" href="reference/sindex.html#constructor">Constructor</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/sindex.html#spatial-index-object">Spatial index object</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="reference/testing.html">Testing</a><ul>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.testing.assert_geoseries_equal.html">geopandas.testing.assert_geoseries_equal</a></li>
<li class="toctree-l2"><a class="reference internal" href="reference/api/geopandas.testing.assert_geodataframe_equal.html">geopandas.testing.assert_geodataframe_equal</a></li>
</ul>
</li>
</ul>
</div>
</section>


                </article>
              
              
              
              
              
                <footer class="prev-next-footer d-print-none">
                  
<div class="prev-next-area">
    <a class="left-prev"
       href="user_guide/fiona_to_pyogrio.html"
       title="previous page">
      <i class="fa-solid fa-angle-left"></i>
      <div class="prev-next-info">
        <p class="prev-next-subtitle">previous</p>
        <p class="prev-next-title">Migration from the Fiona to the Pyogrio read/write engine</p>
      </div>
    </a>
    <a class="right-next"
       href="reference/geoseries.html"
       title="next page">
      <div class="prev-next-info">
        <p class="prev-next-subtitle">next</p>
        <p class="prev-next-title">GeoSeries</p>
      </div>
      <i class="fa-solid fa-angle-right"></i>
    </a>
</div>
                </footer>
              
            </div>
            
            
              
                <dialog id="pst-secondary-sidebar-modal"></dialog>
                <div id="pst-secondary-sidebar" class="bd-sidebar-secondary bd-toc"><div class="sidebar-secondary-items sidebar-secondary__inner">


  <div class="sidebar-secondary-item">

  <div class="tocsection sourcelink">
    <a href="../_sources/docs/reference.rst.txt">
      <i class="fa-solid fa-file-lines"></i> Show Source
    </a>
  </div>
</div>

</div></div>
              
            
          </div>
          <footer class="bd-footer-content">
            
          </footer>
        
      </main>
    </div>
  </div>
  
  <!-- Scripts loaded after <body> so the DOM is not blocked -->
  <script defer src="../_static/scripts/bootstrap.js?digest=a95f357e85573c9b56d5"></script>
<script defer src="../_static/scripts/pydata-sphinx-theme.js?digest=a95f357e85573c9b56d5"></script>

  <footer class="bd-footer">
<div class="bd-footer__inner bd-page-width">
  
    <div class="footer-items__start">
      
        <div class="footer-item">

  <p class="copyright">
    
      © Copyright 2013–, GeoPandas developers.
      <br/>
    
  </p>
</div>
      
        <div class="footer-item">

  <p class="sphinx-version">
    Created using <a href="https://www.sphinx-doc.org/">Sphinx</a> 9.1.0.
    <br/>
  </p>
</div>
      
    </div>
  
  
  
    <div class="footer-items__end">
      
        <div class="footer-item">
<p class="theme-version">
  <!-- # L10n: Setting the PST URL as an argument as this does not need to be localized -->
  Built with the <a href="https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html">PyData Sphinx Theme</a> 0.19.0.
</p></div>
      
    </div>
  
</div>

  </footer>
  </body>
</html>

