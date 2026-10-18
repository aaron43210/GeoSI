Title: Live Content

Description: Fetched live

Source: https://developers.google.com/earth-engine/guides/image_math

---










<!doctype html>
<html 
      lang="en"
      dir="ltr">
  <head>
    <meta name="google-signin-client-id" content="721724668570-nbkv1cfusk7kk4eni4pjvepaus73b13t.apps.googleusercontent.com"><meta name="google-signin-scope"
          content="profile email https://www.googleapis.com/auth/developerprofiles https://www.googleapis.com/auth/developerprofiles.award https://www.googleapis.com/auth/devprofiles.full_control.firstparty"><meta property="og:site_name" content="Google for Developers">
    <meta property="og:type" content="website"><meta name="theme-color" content="#1a73e8"><meta charset="utf-8">
    <meta content="IE=Edge" http-equiv="X-UA-Compatible">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    

    <link rel="manifest" href="/_pwa/developers/manifest.json"
          crossorigin="use-credentials">
    <link rel="preconnect" href="//www.gstatic.com" crossorigin>
    <link rel="preconnect" href="//fonts.googleapis.com" crossorigin>
    <link rel="preconnect" href="//www.google-analytics.com" crossorigin><link rel="stylesheet" href="//fonts.googleapis.com/css?family=Google+Sans:400,500|Roboto:400,400italic,500,500italic,700,700italic|Roboto+Mono:400,500,700&display=swap">
      <link rel="stylesheet"
            href="//fonts.googleapis.com/css2?family=Material+Icons&family=Material+Symbols+Outlined&display=block"><link rel="stylesheet" href="https://www.gstatic.com/devrel-devsite/prod/v63ff991b83776932202eabe7967909a8dae574de15846bab934768a76bf6c589/developers/css/app.css">
      <link rel="shortcut icon" href="https://www.gstatic.com/devrel-devsite/prod/v63ff991b83776932202eabe7967909a8dae574de15846bab934768a76bf6c589/developers/images/favicon-new.png">
    <link rel="apple-touch-icon" href="https://www.gstatic.com/devrel-devsite/prod/v63ff991b83776932202eabe7967909a8dae574de15846bab934768a76bf6c589/developers/images/touchicon-180-new.png"><link rel="canonical" href="https://developers.google.com/earth-engine/guides/image_math"><link rel="search" type="application/opensearchdescription+xml"
            title="Google for Developers" href="https://developers.google.com/s/opensearch.xml">
      <link rel="alternate" hreflang="en"
          href="https://developers.google.com/earth-engine/guides/image_math" /><link rel="alternate" hreflang="x-default" href="https://developers.google.com/earth-engine/guides/image_math" /><link rel="alternate" hreflang="ar"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=ar" /><link rel="alternate" hreflang="bn"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=bn" /><link rel="alternate" hreflang="zh-Hans"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=zh-cn" /><link rel="alternate" hreflang="zh-Hant"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=zh-tw" /><link rel="alternate" hreflang="fa"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=fa" /><link rel="alternate" hreflang="fr"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=fr" /><link rel="alternate" hreflang="de"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=de" /><link rel="alternate" hreflang="he"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=he" /><link rel="alternate" hreflang="hi"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=hi" /><link rel="alternate" hreflang="id"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=id" /><link rel="alternate" hreflang="it"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=it" /><link rel="alternate" hreflang="ja"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=ja" /><link rel="alternate" hreflang="ko"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=ko" /><link rel="alternate" hreflang="pl"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=pl" /><link rel="alternate" hreflang="pt-BR"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=pt-br" /><link rel="alternate" hreflang="ru"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=ru" /><link rel="alternate" hreflang="es-419"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=es-419" /><link rel="alternate" hreflang="th"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=th" /><link rel="alternate" hreflang="tr"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=tr" /><link rel="alternate" hreflang="vi"
          href="https://developers.google.com/earth-engine/guides/image_math?hl=vi" /><title>Mathematical Operations &nbsp;|&nbsp; Google Earth Engine &nbsp;|&nbsp; Google for Developers</title>

<meta property="og:title" content="Mathematical Operations &nbsp;|&nbsp; Google Earth Engine &nbsp;|&nbsp; Google for Developers"><meta property="og:url" content="https://developers.google.com/earth-engine/guides/image_math"><meta property="og:image" content="https://developers.google.com/static/earth-engine/images/og_social_media.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="675"><meta property="og:locale" content="en"><meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    
    "headline": "Mathematical Operations"
  }
</script><script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [{
      "@type": "ListItem",
      "position": 1,
      "name": "Google Earth Engine",
      "item": "https://developers.google.com/earth-engine"
    },{
      "@type": "ListItem",
      "position": 2,
      "name": "Mathematical Operations",
      "item": "https://developers.google.com/earth-engine/guides/image_math"
    }]
  }
  </script>
  
    
    
    
    
  

    </head>
  <body class="color-scheme--light"
        template="page"
        theme="google-blue"
        type="article"
        
        
        
        layout="docs"
        
        
        
        
        
        display-toc
        pending>
  
    <devsite-progress type="indeterminate" id="app-progress"></devsite-progress>
  
  
    <a href="#main-content" class="skip-link button">
      
      Skip to main content
    </a>
    <section class="devsite-wrapper">
      <devsite-cookie-notification-bar></devsite-cookie-notification-bar>
        <devsite-header role="banner">
  
    





















<div class="devsite-header--inner" data-nosnippet>
  <div class="devsite-top-logo-row-wrapper-wrapper">
    <div class="devsite-top-logo-row-wrapper">
      <div class="devsite-top-logo-row">
        <button type="button" id="devsite-hamburger-menu"
          class="devsite-header-icon-button button-flat material-icons gc-analytics-event"
          data-category="Site-Wide Custom Events"
          data-label="Navigation menu button"
          visually-hidden
          aria-label="Open menu">
        </button>
        
<div class="devsite-product-name-wrapper">

  
    
  



  
  
  <span class="devsite-product-name">
    <ul class="devsite-breadcrumb-list"
  >
  
  <li class="devsite-breadcrumb-item
             devsite-has-google-wordmark">
    
    
    
      
      
        
  <a href="https://developers.google.com/earth-engine"
      
        class="devsite-breadcrumb-link gc-analytics-event"
      
        data-category="Site-Wide Custom Events"
      
        data-label="Upper Header"
      
        data-value="1"
      
        track-type="globalNav"
      
        track-name="breadcrumb"
      
        track-metadata-position="1"
      
        track-metadata-eventdetail="Google Earth Engine"
      
    >
    
          <svg class="devsite-google-wordmark"
       xmlns="http://www.w3.org/2000/svg"
       viewBox="0 0 148 48">
    <title>Google</title>
    <path class="devsite-google-wordmark-svg-path" d="M19.58,37.65c-9.87,0-18.17-8.04-18.17-17.91c0-9.87,8.3-17.91,18.17-17.91c5.46,0,9.35,2.14,12.27,4.94l-3.45,3.45c-2.1-1.97-4.93-3.49-8.82-3.49c-7.21,0-12.84,5.81-12.84,13.02c0,7.21,5.64,13.02,12.84,13.02c4.67,0,7.34-1.88,9.04-3.58c1.4-1.4,2.32-3.41,2.66-6.16H19.58v-4.89h16.47c0.18,0.87,0.26,1.92,0.26,3.06c0,3.67-1.01,8.21-4.24,11.44C28.93,35.9,24.91,37.65,19.58,37.65z M61.78,26.12c0,6.64-5.1,11.53-11.36,11.53s-11.36-4.89-11.36-11.53c0-6.68,5.1-11.53,11.36-11.53S61.78,19.43,61.78,26.12z M56.8,26.12c0-4.15-2.96-6.99-6.39-6.99c-3.43,0-6.39,2.84-6.39,6.99c0,4.11,2.96,6.99,6.39,6.99C53.84,33.11,56.8,30.22,56.8,26.12z M87.25,26.12c0,6.64-5.1,11.53-11.36,11.53c-6.26,0-11.36-4.89-11.36-11.53c0-6.68,5.1-11.53,11.36-11.53C82.15,14.59,87.25,19.43,87.25,26.12zM82.28,26.12c0-4.15-2.96-6.99-6.39-6.99c-3.43,0-6.39,2.84-6.39,6.99c0,4.11,2.96,6.99,6.39,6.99C79.32,33.11,82.28,30.22,82.28,26.12z M112.09,15.29v20.7c0,8.52-5.02,12.01-10.96,12.01c-5.59,0-8.95-3.76-10.22-6.81l4.41-1.83c0.79,1.88,2.71,4.1,5.81,4.1c3.8,0,6.16-2.36,6.16-6.77v-1.66h-0.18c-1.14,1.4-3.32,2.62-6.07,2.62c-5.76,0-11.05-5.02-11.05-11.49c0-6.51,5.28-11.57,11.05-11.57c2.75,0,4.93,1.22,6.07,2.58h0.18v-1.88H112.09z M107.64,26.16c0-4.06-2.71-7.03-6.16-7.03c-3.49,0-6.42,2.97-6.42,7.03c0,4.02,2.93,6.94,6.42,6.94C104.93,33.11,107.64,30.18,107.64,26.16z M120.97,3.06v33.89h-5.07V3.06H120.97z M140.89,29.92l3.93,2.62c-1.27,1.88-4.32,5.11-9.61,5.11c-6.55,0-11.28-5.07-11.28-11.53c0-6.86,4.77-11.53,10.71-11.53c5.98,0,8.91,4.76,9.87,7.34l0.52,1.31l-15.42,6.38c1.18,2.31,3.01,3.49,5.59,3.49C137.79,33.11,139.58,31.84,140.89,29.92zM128.79,25.77l10.31-4.28c-0.57-1.44-2.27-2.45-4.28-2.45C132.24,19.04,128.66,21.31,128.79,25.77z"/>
  </svg>Earth Engine
        
  </a>
  
      
    
  </li>
  
</ul>
  </span>

</div>
        <div class="devsite-top-logo-row-middle">
          <div class="devsite-header-upper-tabs">
            
           </div>
          
<devsite-search
    enable-signin
    enable-search
    enable-suggestions
      enable-query-completion
    
    enable-search-summaries
    project-name="Google Earth Engine"
    tenant-name="Google for Developers"
    project-scope="/earth-engine"
    url-scoped="https://developers.google.com/s/results/earth-engine"
    
    
    
    >
  <form class="devsite-search-form" action="https://developers.google.com/s/results" method="GET">
    <div class="devsite-search-container">
      <button type="button"
              search-open
              class="devsite-search-button devsite-header-icon-button button-flat material-icons"
              
              aria-label="Open search"></button>
      <div class="devsite-searchbox">
        <input
          aria-activedescendant=""
          aria-autocomplete="list"
          
          aria-label="Search"
          aria-expanded="false"
          aria-haspopup="listbox"
          autocomplete="off"
          class="devsite-search-field devsite-search-query"
          name="q"
          
          placeholder="Search"
          role="combobox"
          type="text"
          value=""
          >
          <div class="devsite-search-image material-icons" aria-hidden="true">
            
              <svg class="devsite-search-ai-image" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <g clip-path="url(#clip0_6641_386)">
                    <path d="M19.6 21L13.3 14.7C12.8 15.1 12.225 15.4167 11.575 15.65C10.925 15.8833 10.2333 16 9.5 16C7.68333 16 6.14167 15.375 4.875 14.125C3.625 12.8583 3 11.3167 3 9.5C3 7.68333 3.625 6.15 4.875 4.9C6.14167 3.63333 7.68333 3 9.5 3C10.0167 3 10.5167 3.05833 11 3.175C11.4833 3.275 11.9417 3.43333 12.375 3.65L10.825 5.2C10.6083 5.13333 10.3917 5.08333 10.175 5.05C9.95833 5.01667 9.73333 5 9.5 5C8.25 5 7.18333 5.44167 6.3 6.325C5.43333 7.19167 5 8.25 5 9.5C5 10.75 5.43333 11.8167 6.3 12.7C7.18333 13.5667 8.25 14 9.5 14C10.6667 14 11.6667 13.625 12.5 12.875C13.35 12.1083 13.8417 11.15 13.975 10H15.975C15.925 10.6333 15.7833 11.2333 15.55 11.8C15.3333 12.3667 15.05 12.8667 14.7 13.3L21 19.6L19.6 21ZM17.5 12C17.5 10.4667 16.9667 9.16667 15.9 8.1C14.8333 7.03333 13.5333 6.5 12 6.5C13.5333 6.5 14.8333 5.96667 15.9 4.9C16.9667 3.83333 17.5 2.53333 17.5 0.999999C17.5 2.53333 18.0333 3.83333 19.1 4.9C20.1667 5.96667 21.4667 6.5 23 6.5C21.4667 6.5 20.1667 7.03333 19.1 8.1C18.0333 9.16667 17.5 10.4667 17.5 12Z" fill="#5F6368"/>
                  </g>
                <defs>
                <clipPath id="clip0_6641_386">
                <rect width="24" height="24" fill="white"/>
                </clipPath>
                </defs>
              </svg>
            
          </div>
          <div class="devsite-search-shortcut-icon-container" aria-hidden="true">
            <kbd class="devsite-search-shortcut-icon">/</kbd>
          </div>
      </div>
    </div>
  </form>
  <button type="button"
          search-close
          class="devsite-search-button devsite-header-icon-button button-flat material-icons"
          
          aria-label="Close search"></button>
</devsite-search>

        </div>

        

          

          

          

          

          
<devsite-language-selector>
  <ul role="presentation">
    
    
    <li role="presentation">
      <a role="menuitem" lang="en"
        >English</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="de"
        >Deutsch</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="es"
        >Español</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="es_419"
        >Español – América Latina</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="fr"
        >Français</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="id"
        >Indonesia</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="it"
        >Italiano</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="pl"
        >Polski</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="pt_br"
        >Português – Brasil</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="vi"
        >Tiếng Việt</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="tr"
        >Türkçe</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ru"
        >Русский</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="he"
        >עברית</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ar"
        >العربيّة</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="fa"
        >فارسی</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="hi"
        >हिंदी</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="bn"
        >বাংলা</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="th"
        >ภาษาไทย</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="zh_cn"
        >中文 – 简体</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="zh_tw"
        >中文 – 繁體</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ja"
        >日本語</a>
    </li>
    
    <li role="presentation">
      <a role="menuitem" lang="ko"
        >한국어</a>
    </li>
    
  </ul>
</devsite-language-selector>


          

        

        
          <devsite-user 
                        
                        
                          enable-profiles
                        
                        
                          fp-auth
                        
                        id="devsite-user">
            
              
              <span class="button devsite-top-button" aria-hidden="true" visually-hidden>Sign in</span>
            
          </devsite-user>
        
        
        
      </div>
    </div>
  </div>



  <div class="devsite-collapsible-section
    ">
    <div class="devsite-header-background">
      
        
      
      
        <div class="devsite-doc-set-nav-row">
          
          
            
            
  <devsite-tabs class="lower-tabs">

    <nav class="devsite-tabs-wrapper" aria-label="Lower tabs">
      
        
          <tab  >
            
    <a href="https://developers.google.com/earth-engine"
    class="devsite-tabs-content gc-analytics-event "
      track-metadata-eventdetail="https://developers.google.com/earth-engine"
    
       track-type="nav"
       track-metadata-position="nav - home"
       track-metadata-module="primary nav"
       
       
         
           data-category="Site-Wide Custom Events"
         
           data-label="Tab: Home"
         
           track-name="home"
         
       >
    Home
  
    </a>
    
  
          </tab>
        
      
        
          <tab  class="devsite-active">
            
    <a href="https://developers.google.com/earth-engine/guides"
    class="devsite-tabs-content gc-analytics-event "
      track-metadata-eventdetail="https://developers.google.com/earth-engine/guides"
    
       track-type="nav"
       track-metadata-position="nav - guides"
       track-metadata-module="primary nav"
       aria-label="Guides, selected" 
       
         
           data-category="Site-Wide Custom Events"
         
           data-label="Tab: Guides"
         
           track-name="guides"
         
       >
    Guides
  
    </a>
    
  
          </tab>
        
      
        
          <tab  >
            
    <a href="https://developers.google.com/earth-engine/apidocs"
    class="devsite-tabs-content gc-analytics-event "
      track-metadata-eventdetail="https://developers.google.com/earth-engine/apidocs"
    
       track-type="nav"
       track-metadata-position="nav - reference"
       track-metadata-module="primary nav"
       
       
         
           data-category="Site-Wide Custom Events"
         
           data-label="Tab: Reference"
         
           track-name="reference"
         
       >
    Reference
  
    </a>
    
  
          </tab>
        
      
        
          <tab  >
            
    <a href="https://developers.google.com/earth-engine/help"
    class="devsite-tabs-content gc-analytics-event "
      track-metadata-eventdetail="https://developers.google.com/earth-engine/help"
    
       track-type="nav"
       track-metadata-position="nav - support"
       track-metadata-module="primary nav"
       
       
         
           data-category="Site-Wide Custom Events"
         
           data-label="Tab: Support"
         
           track-name="support"
         
       >
    Support
  
    </a>
    
  
          </tab>
        
      
        
          <tab  >
            
    <a href="https://developers.google.com/earth-engine/tutorials"
    class="devsite-tabs-content gc-analytics-event "
      track-metadata-eventdetail="https://developers.google.com/earth-engine/tutorials"
    
       track-type="nav"
       track-metadata-position="nav - community"
       track-metadata-module="primary nav"
       
       
         
           data-category="Site-Wide Custom Events"
         
           data-label="Tab: Community"
         
           track-name="community"
         
       >
    Community
  
    </a>
    
  
          </tab>
        
      
        
          <tab  >
            
    <a href="https://developers.google.com/earth-engine/datasets"
    class="devsite-tabs-content gc-analytics-event "
      track-metadata-eventdetail="https://developers.google.com/earth-engine/datasets"
    
       track-type="nav"
       track-metadata-position="nav - data catalog"
       track-metadata-module="primary nav"
       
       
         
           data-category="Site-Wide Custom Events"
         
           data-label="Tab: Data Catalog"
         
           track-name="data catalog"
         
       >
    Data Catalog
  
    </a>
    
  
          </tab>
        
      
    </nav>

  </devsite-tabs>

          
          
        </div>
      
    </div>
  </div>

</div>



  
</devsite-header>
        <devsite-book-nav scrollbars >
          
            





















<div class="devsite-book-nav-filter"
     >
  <span class="filter-list-icon material-icons" aria-hidden="true"></span>
  <input type="text"
         placeholder="Filter"
         
         aria-label="Type to filter"
         role="searchbox">
  
  <span class="filter-clear-button hidden"
        data-title="Clear filter"
        aria-label="Clear filter"
        role="button"
        tabindex="0"></span>
</div>

<nav class="devsite-book-nav devsite-nav nocontent" data-nosnippet
     aria-label="Side menu">
  <div class="devsite-mobile-header">
    <button type="button"
            id="devsite-close-nav"
            class="devsite-header-icon-button button-flat material-icons gc-analytics-event"
            data-category="Site-Wide Custom Events"
            data-label="Close navigation"
            aria-label="Close navigation">
    </button>
    <div class="devsite-product-name-wrapper">

  
    
  


  
      <span class="devsite-product-name">
        
        
        <ul class="devsite-breadcrumb-list"
  >
  
  <li class="devsite-breadcrumb-item
             devsite-has-google-wordmark">
    
    
    
      
      
        
  <a href="https://developers.google.com/earth-engine"
      
        class="devsite-breadcrumb-link gc-analytics-event"
      
        data-category="Site-Wide Custom Events"
      
        data-label="Upper Header"
      
        data-value="1"
      
        track-type="globalNav"
      
        track-name="breadcrumb"
      
        track-metadata-position="1"
      
        track-metadata-eventdetail="Google Earth Engine"
      
    >
    
          <svg class="devsite-google-wordmark"
       xmlns="http://www.w3.org/2000/svg"
       viewBox="0 0 148 48">
    <title>Google</title>
    <path class="devsite-google-wordmark-svg-path" d="M19.58,37.65c-9.87,0-18.17-8.04-18.17-17.91c0-9.87,8.3-17.91,18.17-17.91c5.46,0,9.35,2.14,12.27,4.94l-3.45,3.45c-2.1-1.97-4.93-3.49-8.82-3.49c-7.21,0-12.84,5.81-12.84,13.02c0,7.21,5.64,13.02,12.84,13.02c4.67,0,7.34-1.88,9.04-3.58c1.4-1.4,2.32-3.41,2.66-6.16H19.58v-4.89h16.47c0.18,0.87,0.26,1.92,0.26,3.06c0,3.67-1.01,8.21-4.24,11.44C28.93,35.9,24.91,37.65,19.58,37.65z M61.78,26.12c0,6.64-5.1,11.53-11.36,11.53s-11.36-4.89-11.36-11.53c0-6.68,5.1-11.53,11.36-11.53S61.78,19.43,61.78,26.12z M56.8,26.12c0-4.15-2.96-6.99-6.39-6.99c-3.43,0-6.39,2.84-6.39,6.99c0,4.11,2.96,6.99,6.39,6.99C53.84,33.11,56.8,30.22,56.8,26.12z M87.25,26.12c0,6.64-5.1,11.53-11.36,11.53c-6.26,0-11.36-4.89-11.36-11.53c0-6.68,5.1-11.53,11.36-11.53C82.15,14.59,87.25,19.43,87.25,26.12zM82.28,26.12c0-4.15-2.96-6.99-6.39-6.99c-3.43,0-6.39,2.84-6.39,6.99c0,4.11,2.96,6.99,6.39,6.99C79.32,33.11,82.28,30.22,82.28,26.12z M112.09,15.29v20.7c0,8.52-5.02,12.01-10.96,12.01c-5.59,0-8.95-3.76-10.22-6.81l4.41-1.83c0.79,1.88,2.71,4.1,5.81,4.1c3.8,0,6.16-2.36,6.16-6.77v-1.66h-0.18c-1.14,1.4-3.32,2.62-6.07,2.62c-5.76,0-11.05-5.02-11.05-11.49c0-6.51,5.28-11.57,11.05-11.57c2.75,0,4.93,1.22,6.07,2.58h0.18v-1.88H112.09z M107.64,26.16c0-4.06-2.71-7.03-6.16-7.03c-3.49,0-6.42,2.97-6.42,7.03c0,4.02,2.93,6.94,6.42,6.94C104.93,33.11,107.64,30.18,107.64,26.16z M120.97,3.06v33.89h-5.07V3.06H120.97z M140.89,29.92l3.93,2.62c-1.27,1.88-4.32,5.11-9.61,5.11c-6.55,0-11.28-5.07-11.28-11.53c0-6.86,4.77-11.53,10.71-11.53c5.98,0,8.91,4.76,9.87,7.34l0.52,1.31l-15.42,6.38c1.18,2.31,3.01,3.49,5.59,3.49C137.79,33.11,139.58,31.84,140.89,29.92zM128.79,25.77l10.31-4.28c-0.57-1.44-2.27-2.45-4.28-2.45C132.24,19.04,128.66,21.31,128.79,25.77z"/>
  </svg>Earth Engine
        
  </a>
  
      
    
  </li>
  
</ul>
      </span>
    

</div>
  </div>

  <div class="devsite-book-nav-wrapper">
    <div class="devsite-mobile-nav-top">
      
        <ul class="devsite-nav-list">
          
            
<li class="devsite-nav-item">

  
  <a href="/earth-engine"
    
       class="devsite-nav-title gc-analytics-event
              
              "
    

    
      
        data-category="Site-Wide Custom Events"
      
        data-label="Tab: Home"
      
        track-name="home"
      
    
     data-category="Site-Wide Custom Events"
     data-label="Responsive Tab: Home"
     track-type="navMenu"
     track-metadata-eventDetail="globalMenu"
     track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip >
      Home
   </span>
    
  
  </a>
  

</li>

          
            
<li class="devsite-nav-item">

  
  <a href="/earth-engine/guides"
    
       class="devsite-nav-title gc-analytics-event
              devsite-nav-has-children
              devsite-nav-active"
    

    
      
        data-category="Site-Wide Custom Events"
      
        data-label="Tab: Guides"
      
        track-name="guides"
      
    
     data-category="Site-Wide Custom Events"
     data-label="Responsive Tab: Guides"
     track-type="navMenu"
     track-metadata-eventDetail="globalMenu"
     track-metadata-position="nav">
  
    <span class="devsite-nav-text" tooltip >
      Guides
   </span>
    
    <span class="devsite-nav-icon material-icons" data-icon="forward"
          >
    </span>
    
  
  </a>
  

</li>

          
            
<li class="devsite-nav-item">

  
  <a href="/earth-engine/apidocs"
    
       class="devsite-nav-title gc-analytics-event
              devsite-nav-has-children
              "
    

    
      
        data-category="Site-Wide Custom Events"
      
        data-label="Tab: Reference"
      
        track-name

