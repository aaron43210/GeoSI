Title: Live Content

Description: Fetched live

Source: https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/processing.html

---

<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="../../">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>17. Writing a Processing plugin &mdash; QGIS Documentation  documentation</title>
      <link rel="stylesheet" type="text/css" href="../../_static/pygments.css?v=80d5e7a1" />
      <link rel="stylesheet" type="text/css" href="../../_static/css/qgis_docs.css?v=01847ad1" />
      <link rel="stylesheet" type="text/css" href="../../_static/togglebutton.css?v=13237357" />
      <link rel="stylesheet" type="text/css" href="../../_static/copybutton.css?v=76b2166b" />
      <link rel="stylesheet" type="text/css" href="../../_static/css/qgis_topbar.css?v=5613a779" />

  
    <link rel="shortcut icon" href="../../_static/qgis_logo.ico"/>
    <link rel="canonical" href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/processing.html"/>
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
    <link rel="next" title="18. Using Plugin Layers" href="pluginlayer.html" />
    <link rel="prev" title="16.4. Releasing your plugin" href="plugins/releasing.html" />
  <meta name="description" content="QGIS 3.34 documentation: 17. Writing a Processing plugin">
  <meta name="robots" content="noindex">
</head>

<body class="wy-body-for-nav">

  <nav class="release_status_topbar">
    <div class="row outdated">
     This documentation is for a QGIS version which has reached end of life. Instead visit the <a href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/processing.html">latest version</a>.
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
<li class="toctree-l2 current"><a class="current reference internal" href="#">17. Writing a Processing plugin</a><ul>
<li class="toctree-l3"><a class="reference internal" href="#creating-from-scratch">17.1. Creating from scratch</a></li>
<li class="toctree-l3"><a class="reference internal" href="#updating-a-plugin">17.2. Updating a plugin</a></li>
</ul>
</li>
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
      <li class="breadcrumb-item active"><span class="section-number">17. </span>Writing a Processing plugin</li>

    <li style="float: right; text-align: right;">
	<ul>
		
      <li class="wy-breadcrumbs-aside">
            <a href="../../_sources/docs/pyqgis_developer_cookbook/processing.rst.txt" rel="nofollow"> View page source</a>
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
        <a href="plugins/releasing.html" class="btn btn-neutral float-left" title="16.4. Releasing your plugin" accesskey="p"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="pluginlayer.html" class="btn btn-neutral float-right" title="18. Using Plugin Layers" accesskey="n">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
  </div>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <blockquote>
<div></div></blockquote>
<section id="writing-a-processing-plugin">
<span id="processing-plugin"></span><span id="index-0"></span><h1><span class="section-number">17. </span>Writing a Processing plugin<a class="headerlink" href="#writing-a-processing-plugin" title="Link to this heading"></a></h1>
<nav class="contents local" id="contents">
<ul class="simple">
<li><p><a class="reference internal" href="#creating-from-scratch" id="id1">Creating from scratch</a></p></li>
<li><p><a class="reference internal" href="#updating-a-plugin" id="id2">Updating a plugin</a></p></li>
</ul>
</nav>
<p>Depending on the kind of plugin that you are going to develop, it might be a better
option to add its functionality as a Processing algorithm (or a set of them).
That would provide a better integration within QGIS, additional functionality (since
it can be run in the components of Processing, such as the modeler or the batch
processing interface), and a quicker development time (since Processing will take of
a large part of the work).</p>
<p>To distribute those algorithms, you should create a new plugin that adds them to the
Processing Toolbox. The plugin should contain an algorithm provider, which has to be
registered when the plugin is instantiated.</p>
<section id="creating-from-scratch">
<h2><a class="toc-backref" href="#id1" role="doc-backlink"><span class="section-number">17.1. </span>Creating from scratch</a><a class="headerlink" href="#creating-from-scratch" title="Link to this heading"></a></h2>
<p>To create a plugin from scratch which contains an algorithm provider, you can
follow these steps using the Plugin Builder:</p>
<ol class="arabic simple">
<li><p>Install the <strong>Plugin Builder</strong> plugin</p></li>
<li><p>Create a new plugin using the Plugin Builder. When the Plugin Builder asks you for
the template to use, select “Processing provider”.</p></li>
<li><p>The created plugin contains a provider with a single algorithm. Both the provider
file and the algorithm file are fully commented and contain information about how to
modify the provider and add additional algorithms. Refer to them for more information.</p></li>
</ol>
</section>
<section id="updating-a-plugin">
<h2><a class="toc-backref" href="#id2" role="doc-backlink"><span class="section-number">17.2. </span>Updating a plugin</a><a class="headerlink" href="#updating-a-plugin" title="Link to this heading"></a></h2>
<p>If you want to add your existing plugin to Processing, you need to add some code.</p>
<ol class="arabic">
<li><p>In your <code class="file docutils literal notranslate"><span class="pre">metadata.txt</span></code> file, you need to add a variable:</p>
<div class="highlight-ini notranslate"><div class="highlight"><pre><span></span><span class="na">hasProcessingProvider</span><span class="o">=</span><span class="s">yes</span>
</pre></div>
</div>
</li>
<li><p>In the Python file where your plugin is setup with the <code class="docutils literal notranslate"><span class="pre">initGui</span></code> method,
you need to adapt some lines like this:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="n">QgsApplication</span>
<span class="linenos"> 2</span><span class="kn">from</span> <span class="nn">.processing_provider.provider</span> <span class="kn">import</span> <span class="n">Provider</span>
<span class="linenos"> 3</span>
<span class="linenos"> 4</span><span class="k">class</span> <span class="nc">YourPluginName</span><span class="p">:</span>
<span class="linenos"> 5</span>
<span class="linenos"> 6</span>    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos"> 7</span>        <span class="bp">self</span><span class="o">.</span><span class="n">provider</span> <span class="o">=</span> <span class="kc">None</span>
<span class="linenos"> 8</span>
<span class="linenos"> 9</span>    <span class="k">def</span> <span class="nf">initProcessing</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">10</span>        <span class="bp">self</span><span class="o">.</span><span class="n">provider</span> <span class="o">=</span> <span class="n">Provider</span><span class="p">()</span>
<span class="linenos">11</span>        <span class="n">QgsApplication</span><span class="o">.</span><span class="n">processingRegistry</span><span class="p">()</span><span class="o">.</span><span class="n">addProvider</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">provider</span><span class="p">)</span>
<span class="linenos">12</span>
<span class="linenos">13</span>    <span class="k">def</span> <span class="nf">initGui</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">14</span>        <span class="bp">self</span><span class="o">.</span><span class="n">initProcessing</span><span class="p">()</span>
<span class="linenos">15</span>
<span class="linenos">16</span>    <span class="k">def</span> <span class="nf">unload</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">17</span>        <span class="n">QgsApplication</span><span class="o">.</span><span class="n">processingRegistry</span><span class="p">()</span><span class="o">.</span><span class="n">removeProvider</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">provider</span><span class="p">)</span>
</pre></div>
</div>
</li>
<li><p>You can create a folder <code class="file docutils literal notranslate"><span class="pre">processing_provider</span></code> with three files in it:</p>
<ul>
<li><p><code class="file docutils literal notranslate"><span class="pre">__init__.py</span></code> with nothing in it. This is necessary to make a valid
Python package.</p></li>
<li><p><code class="file docutils literal notranslate"><span class="pre">provider.py</span></code> which will create the Processing provider and expose
your algorithms.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 1</span><span class="kn">from</span> <span class="nn">qgis.core</span> <span class="kn">import</span> <span class="n">QgsProcessingProvider</span>
<span class="linenos"> 2</span><span class="kn">from</span> <span class="nn">qgis.PyQt.QtGui</span> <span class="kn">import</span> <span class="n">QIcon</span>
<span class="linenos"> 3</span>
<span class="linenos"> 4</span><span class="kn">from</span> <span class="nn">.example_processing_algorithm</span> <span class="kn">import</span> <span class="n">ExampleProcessingAlgorithm</span>
<span class="linenos"> 5</span>
<span class="linenos"> 6</span>
<span class="linenos"> 7</span><span class="k">class</span> <span class="nc">Provider</span><span class="p">(</span><span class="n">QgsProcessingProvider</span><span class="p">):</span>
<span class="linenos"> 8</span>
<span class="linenos"> 9</span><span class="w">    </span><span class="sd">&quot;&quot;&quot; The provider of our plugin. &quot;&quot;&quot;</span>
<span class="linenos">10</span>
<span class="linenos">11</span>    <span class="k">def</span> <span class="nf">loadAlgorithms</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos">12</span><span class="w">        </span><span class="sd">&quot;&quot;&quot; Load each algorithm into the current provider. &quot;&quot;&quot;</span>
<span class="linenos">13</span>        <span class="bp">self</span><span class="o">.</span><span class="n">addAlgorithm</span><span class="p">(</span><span class="n">ExampleProcessingAlgorithm</span><span class="p">())</span>
<span class="linenos">14</span>        <span class="c1"># add additional algorithms here</span>
<span class="linenos">15</span>        <span class="c1"># self.addAlgorithm(MyOtherAlgorithm())</span>
<span class="linenos">16</span>
<span class="linenos">17</span>    <span class="k">def</span> <span class="nf">id</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">str</span><span class="p">:</span>
<span class="linenos">18</span><span class="w">        </span><span class="sd">&quot;&quot;&quot;The ID of your plugin, used for identifying the provider.</span>
<span class="linenos">19</span>
<span class="linenos">20</span><span class="sd">        This string should be a unique, short, character only string,</span>
<span class="linenos">21</span><span class="sd">        eg &quot;qgis&quot; or &quot;gdal&quot;. This string should not be localised.</span>
<span class="linenos">22</span><span class="sd">        &quot;&quot;&quot;</span>
<span class="linenos">23</span>        <span class="k">return</span> <span class="s1">&#39;yourplugin&#39;</span>
<span class="linenos">24</span>
<span class="linenos">25</span>    <span class="k">def</span> <span class="nf">name</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">str</span><span class="p">:</span>
<span class="linenos">26</span><span class="w">        </span><span class="sd">&quot;&quot;&quot;The human friendly name of your plugin in Processing.</span>
<span class="linenos">27</span>
<span class="linenos">28</span><span class="sd">        This string should be as short as possible (e.g. &quot;Lastools&quot;, not</span>
<span class="linenos">29</span><span class="sd">        &quot;Lastools version 1.0.1 64-bit&quot;) and localised.</span>
<span class="linenos">30</span><span class="sd">        &quot;&quot;&quot;</span>
<span class="linenos">31</span>        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">tr</span><span class="p">(</span><span class="s1">&#39;Your plugin&#39;</span><span class="p">)</span>
<span class="linenos">32</span>
<span class="linenos">33</span>    <span class="k">def</span> <span class="nf">icon</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">QIcon</span><span class="p">:</span>
<span class="linenos">34</span><span class="w">        </span><span class="sd">&quot;&quot;&quot;Should return a QIcon which is used for your provider inside</span>
<span class="linenos">35</span><span class="sd">        the Processing toolbox.</span>
<span class="linenos">36</span><span class="sd">        &quot;&quot;&quot;</span>
<span class="linenos">37</span>        <span class="k">return</span> <span class="n">QgsProcessingProvider</span><span class="o">.</span><span class="n">icon</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
</pre></div>
</div>
</li>
<li><p><code class="file docutils literal notranslate"><span class="pre">example_processing_algorithm.py</span></code> which contains the example
algorithm file. Copy/paste the content of the <a class="reference external" href="https://github.com/qgis/QGIS/blob/release-3_34/python/plugins/processing/script/ScriptTemplate.py">script template
file</a> and
update it according to your needs.</p></li>
</ul>
</li>
</ol>
<p>You should have a tree similar to this :</p>
<div class="highlight-bash notranslate"><div class="highlight"><pre><span></span><span class="linenos">1</span>└──<span class="w"> </span>your_plugin_root_folder
<span class="linenos">2</span><span class="w">   </span>├──<span class="w"> </span>__init__.py
<span class="linenos">3</span><span class="w">   </span>├──<span class="w"> </span>LICENSE
<span class="linenos">4</span><span class="w">   </span>├──<span class="w"> </span>metadata.txt
<span class="linenos">5</span><span class="w">   </span>└──<span class="w"> </span>processing_provider
<span class="linenos">6</span><span class="w">         </span>├──<span class="w"> </span>example_processing_algorithm.py
<span class="linenos">7</span><span class="w">         </span>├──<span class="w"> </span>__init__.py
<span class="linenos">8</span><span class="w">         </span>└──<span class="w"> </span>provider.py
</pre></div>
</div>
<ol class="arabic simple">
<li><p>Now you can reload your plugin in QGIS and you should see your example
script in the Processing toolbox and modeler.</p></li>
</ol>
</section>
</section>


           </div>
          </div>
          <footer><div class="rst-footer-buttons" role="navigation" aria-label="Footer">
        <a href="plugins/releasing.html" class="btn btn-neutral float-left" title="16.4. Releasing your plugin" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>
        <a href="pluginlayer.html" class="btn btn-neutral float-right" title="18. Using Plugin Layers" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>
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
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/processing.html">en</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/cs/docs/pyqgis_developer_cookbook/processing.html">cs</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/de/docs/pyqgis_developer_cookbook/processing.html">de</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/es/docs/pyqgis_developer_cookbook/processing.html">es</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/fr/docs/pyqgis_developer_cookbook/processing.html">fr</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/hu/docs/pyqgis_developer_cookbook/processing.html">hu</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/it/docs/pyqgis_developer_cookbook/processing.html">it</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ja/docs/pyqgis_developer_cookbook/processing.html">ja</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ko/docs/pyqgis_developer_cookbook/processing.html">ko</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/lt/docs/pyqgis_developer_cookbook/processing.html">lt</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/nl/docs/pyqgis_developer_cookbook/processing.html">nl</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_BR/docs/pyqgis_developer_cookbook/processing.html">pt_BR</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/pt_PT/docs/pyqgis_developer_cookbook/processing.html">pt_PT</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ro/docs/pyqgis_developer_cookbook/processing.html">ro</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/ru/docs/pyqgis_developer_cookbook/processing.html">ru</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/zh-Hans/docs/pyqgis_developer_cookbook/processing.html">zh-Hans</a></dd>
        
      </dl>

      <dl>
        <dt>Versions</dt>
        
          <dd><a href="https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/processing.html">testing</a></dd>
        
          <dd><a href="https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/processing.html">latest</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/processing.html">3.40</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/processing.html">3.34</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/processing.html">3.28</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/processing.html">3.22</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/processing.html">3.16</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.10/en/docs/pyqgis_developer_cookbook/processing.html">3.10</a></dd>
        
          <dd><a href="https://docs.qgis.org/3.4/en/docs/pyqgis_developer_cookbook/processing.html">3.4</a></dd>
        
          <dd><a href="https://docs.qgis.org/2.18/en/docs/pyqgis_developer_cookbook/processing.html">2.18</a></dd>
        
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

