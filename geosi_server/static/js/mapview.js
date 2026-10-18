/* GeoSI console — MapLibre 2D/3D map wrapper. */
(function (G) {
  "use strict";

  const DEM = {
    type: "raster-dem", tileSize: 256, encoding: "terrarium", maxzoom: 15,
    tiles: ["https://elevation-tiles-prod.s3.amazonaws.com/terrarium/{z}/{x}/{y}.png"],
    attribution: "Terrain: Mapzen/AWS",
  };

  function rasterStyle(tiles, attribution) {
    return {
      version: 8,
      sources: { base: { type: "raster", tileSize: 256, tiles, attribution } },
      layers: [{ id: "base", type: "raster", source: "base" }],
    };
  }

  const BASEMAPS = {
    vector: "https://demotiles.maplibre.org/style.json",
    osm: rasterStyle(["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      "© OpenStreetMap contributors"),
    dark: rasterStyle(["https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"],
      "© OpenStreetMap · © CARTO"),
  };

  const PALETTE = ["#4ea1ff", "#7c5cff", "#3fb950", "#d29922", "#f85149",
                   "#00c2d1", "#ff7ab6", "#b7e000"];

  const MapView = {
    map: null,
    _overlays: {},      // name -> {type, color, visible, opacity, data, bounds, extrude, extrudeField}
    _basemap: "vector",
    _is3D: false,
    _terrain: false,
    _colorIdx: 0,

    init() {
      this.map = new maplibregl.Map({
        container: "map",
        style: BASEMAPS[this._basemap],
        center: [0, 20], zoom: 1.6, pitch: 0, bearing: 0,
        attributionControl: { compact: true },
      });
      this.map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), "top-right");
      this.map.addControl(new maplibregl.ScaleControl({ unit: "metric" }), "bottom-right");
      this.map.on("style.load", () => this._reapply());
      return this;
    },

    nextColor() { return PALETTE[this._colorIdx++ % PALETTE.length]; },

    setBasemap(name) {
      if (!BASEMAPS[name]) return;
      this._basemap = name;
      this.map.setStyle(BASEMAPS[name]);  // _reapply() runs on style.load
    },

    set3D(on) {
      this._is3D = on;
      this.map.easeTo({ pitch: on ? 60 : 0, bearing: on ? -20 : 0, duration: 600 });
    },

    toggleTerrain() {
      this._terrain = !this._terrain;
      this._applyTerrain();
      if (this._terrain && !this._is3D) this.set3D(true);
      return this._terrain;
    },

    _applyTerrain() {
      const m = this.map;
      if (this._terrain) {
        if (!m.getSource("__dem")) m.addSource("__dem", DEM);
        m.setTerrain({ source: "__dem", exaggeration: 1.3 });
        if (!m.getLayer("__sky")) {
          m.addLayer({ id: "__sky", type: "sky",
            paint: { "sky-type": "atmosphere", "sky-atmosphere-sun-intensity": 12 } });
        }
      } else {
        m.setTerrain(null);
      }
    },

    // Re-add every overlay after a basemap/style swap (setStyle wipes them).
    _reapply() {
      if (this._terrain) this._applyTerrain();
      Object.keys(this._overlays).forEach((name) => {
        const o = this._overlays[name];
        if (o.type === "raster") this._paintRaster(name, o);
        else this._paintVector(name, o);
      });
    },

    _sid(name) { return "ol::" + name; },

    _primaryGeom(fc) {
      const f = (fc.features || []).find((x) => x && x.geometry);
      const t = (f && f.geometry && f.geometry.type) || (fc._meta && fc._meta.geometry_type) || "";
      if (/point/i.test(t)) return "point";
      if (/line/i.test(t)) return "line";
      if (/polygon/i.test(t)) return "polygon";
      return "polygon";
    },

    _paintVector(name, o) {
      const m = this.map, sid = this._sid(name);
      if (!m.getSource(sid)) m.addSource(sid, { type: "geojson", data: o.data });
      else m.getSource(sid).setData(o.data);
      const geom = this._primaryGeom(o.data);
      const vis = o.visible ? "visible" : "none";

      if (geom === "point") {
        this._layer({ id: sid + ":pt", type: "circle", source: sid, layout: { visibility: vis },
          paint: { "circle-radius": 5, "circle-color": o.color, "circle-opacity": o.opacity,
                   "circle-stroke-width": 1, "circle-stroke-color": "#0d1117" } });
      } else if (geom === "line") {
        this._layer({ id: sid + ":ln", type: "line", source: sid, layout: { visibility: vis },
          paint: { "line-color": o.color, "line-width": 2.2, "line-opacity": o.opacity } });
      } else {
        if (o.extrude) {
          this._layer({ id: sid + ":ex", type: "fill-extrusion", source: sid, layout: { visibility: vis },
            paint: { "fill-extrusion-color": o.color, "fill-extrusion-opacity": Math.max(o.opacity, .6),
              "fill-extrusion-height": o.extrudeField
                ? ["coalesce", ["to-number", ["get", o.extrudeField]], 0] : 500,
              "fill-extrusion-base": 0 } });
        } else {
          this._layer({ id: sid + ":fl", type: "fill", source: sid, layout: { visibility: vis },
            paint: { "fill-color": o.color, "fill-opacity": o.opacity * 0.5 } });
          this._layer({ id: sid + ":ol", type: "line", source: sid, layout: { visibility: vis },
            paint: { "line-color": o.color, "line-width": 1.4, "line-opacity": o.opacity } });
        }
      }
      this._bindPopup(name, sid, geom, o.extrude);
    },

    _layer(def) {
      if (this.map.getLayer(def.id)) this.map.removeLayer(def.id);
      this.map.addLayer(def);
    },

    _bindPopup(name, sid, geom, extrude) {
      const hit = sid + (geom === "point" ? ":pt" : geom === "line" ? ":ln"
        : extrude ? ":ex" : ":fl");
      if (this._popupBound && this._popupBound[hit]) return;
      this._popupBound = this._popupBound || {};
      this._popupBound[hit] = true;
      const m = this.map;
      m.on("click", hit, (e) => {
        const f = e.features && e.features[0];
        if (!f) return;
        const props = f.properties || {};
        const rows = Object.keys(props).slice(0, 12)
          .map((k) => `<div><strong>${G.esc(k)}</strong>: ${G.esc(props[k])}</div>`).join("");
        new maplibregl.Popup({ closeButton: true })
          .setLngLat(e.lngLat)
          .setHTML(`<div style="max-width:240px"><b>${G.esc(name)}</b>${rows || "<div>(no attributes)</div>"}</div>`)
          .addTo(m);
      });
      m.on("mouseenter", hit, () => { m.getCanvas().style.cursor = "pointer"; });
      m.on("mouseleave", hit, () => { m.getCanvas().style.cursor = ""; });
    },

    _paintRaster(name, o) {
      const m = this.map, sid = this._sid(name);
      if (!o.data || !o.bounds) return;
      const [w, s, e, n] = o.bounds;
      if (!m.getSource(sid)) {
        m.addSource(sid, { type: "image", url: o.data,
          coordinates: [[w, n], [e, n], [e, s], [w, s]] });
      }
      this._layer({ id: sid + ":img", type: "raster", source: sid,
        layout: { visibility: o.visible ? "visible" : "none" },
        paint: { "raster-opacity": o.opacity } });
    },

    _layerIds(name) {
      const sid = this._sid(name);
      return [":pt", ":ln", ":fl", ":ol", ":ex", ":img"].map((x) => sid + x)
        .filter((id) => this.map.getLayer(id));
    },

    // ── Public overlay API ──────────────────────────────────────────
    addVector(name, geojson, color) {
      const o = this._overlays[name] || { visible: true, opacity: 1, extrude: false };
      o.type = "vector"; o.data = geojson;
      o.color = o.color || color || this.nextColor();
      o.bounds = this._boundsOf(geojson);
      this._overlays[name] = o;
      this._paintVector(name, o);
      return o;
    },

    addRaster(name, info) {
      const o = this._overlays[name] || { visible: true, opacity: 1 };
      o.type = "raster"; o.data = info.image; o.bounds = info.bounds_wgs84;
      o.color = o.color || this.nextColor();
      this._overlays[name] = o;
      this._paintRaster(name, o);
      return o;
    },

    setVisible(name, on) {
      const o = this._overlays[name]; if (!o) return;
      o.visible = on;
      this._layerIds(name).forEach((id) =>
        this.map.setLayoutProperty(id, "visibility", on ? "visible" : "none"));
    },

    setOpacity(name, v) {
      const o = this._overlays[name]; if (!o) return;
      o.opacity = v;
      if (o.type === "raster") { this._safe(this._sid(name) + ":img", "raster-opacity", v); return; }
      this._safe(this._sid(name) + ":pt", "circle-opacity", v);
      this._safe(this._sid(name) + ":ln", "line-opacity", v);
      this._safe(this._sid(name) + ":ol", "line-opacity", v);
      this._safe(this._sid(name) + ":fl", "fill-opacity", v * 0.5);
      this._safe(this._sid(name) + ":ex", "fill-extrusion-opacity", Math.max(v, .6));
    },

    _safe(id, prop, v) {
      if (this.map.getLayer(id)) { try { this.map.setPaintProperty(id, prop, v); } catch (e) {} }
    },

    setColor(name, color) {
      const o = this._overlays[name]; if (!o) return;
      o.color = color;
      if (o.type === "raster") return;
      this._safe(this._sid(name) + ":pt", "circle-color", color);
      this._safe(this._sid(name) + ":ln", "line-color", color);
      this._safe(this._sid(name) + ":ol", "line-color", color);
      this._safe(this._sid(name) + ":fl", "fill-color", color);
      this._safe(this._sid(name) + ":ex", "fill-extrusion-color", color);
    },

    setExtrude(name, on, field) {
      const o = this._overlays[name]; if (!o || o.type !== "vector") return;
      o.extrude = on; o.extrudeField = field || o.extrudeField;
      this._layerIds(name).forEach((id) => this.map.removeLayer(id));
      this._paintVector(name, o);
      if (on && !this._is3D) this.set3D(true);
    },

    remove(name) {
      this._layerIds(name).forEach((id) => this.map.removeLayer(id));
      const sid = this._sid(name);
      if (this.map.getSource(sid)) this.map.removeSource(sid);
      delete this._overlays[name];
    },

    _boundsOf(fc) {
      let a = [Infinity, Infinity, -Infinity, -Infinity];
      const walk = (c) => {
        if (typeof c[0] === "number") {
          a[0] = Math.min(a[0], c[0]); a[1] = Math.min(a[1], c[1]);
          a[2] = Math.max(a[2], c[0]); a[3] = Math.max(a[3], c[1]);
        } else c.forEach(walk);
      };
      (fc.features || []).forEach((f) => f.geometry && f.geometry.coordinates && walk(f.geometry.coordinates));
      return isFinite(a[0]) ? a : null;
    },

    fitTo(name) {
      const o = this._overlays[name];
      if (o && o.bounds) this.map.fitBounds(
        [[o.bounds[0], o.bounds[1]], [o.bounds[2], o.bounds[3]]],
        { padding: 60, maxZoom: 16, duration: 800 });
    },

    fitAll() {
      let a = null;
      Object.values(this._overlays).forEach((o) => {
        if (!o.bounds) return;
        if (!a) a = o.bounds.slice();
        else {
          a[0] = Math.min(a[0], o.bounds[0]); a[1] = Math.min(a[1], o.bounds[1]);
          a[2] = Math.max(a[2], o.bounds[2]); a[3] = Math.max(a[3], o.bounds[3]);
        }
      });
      if (a) this.map.fitBounds([[a[0], a[1]], [a[2], a[3]]],
        { padding: 60, maxZoom: 16, duration: 800 });
    },

    has(name) { return !!this._overlays[name]; },
    get(name) { return this._overlays[name]; },
  };

  G.MapView = MapView;
})(window.GeoSI);

