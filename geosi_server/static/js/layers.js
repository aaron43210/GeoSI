/* GeoSI console — layer panel: syncs session layers ↔ map, handles uploads. */
(function (G) {
  "use strict";

  const Layers = {
    _meta: {},        // name -> server metadata (feature_count, fields, type…)
    _sessionId: null,

    setSession(sid) { this._sessionId = sid; },

    async refresh() {
      let list = [];
      try {
        list = await G.Api.listLayers(this._sessionId);
      } catch (e) {
        this.render();                 // keep local overlays, show what we have
        return;
      }
      for (const l of list) {
        this._meta[l.name] = l;
        if (G.MapView.has(l.name)) continue;   // already drawn — don't refetch
        try {
          if (l.layer_type === "raster") {
            const r = await G.Api.raster(l.name, this._sessionId);
            if (r.bounds_wgs84) G.MapView.addRaster(l.name, r);
          } else {
            const fc = await G.Api.geojson(l.name, this._sessionId);
            G.MapView.addVector(l.name, fc);
          }
        } catch (e) { /* geometry unavailable — card still lists it */ }
      }
      this.render();
    },

    addLocalGeoJSON(name, fc) {
      this._meta[name] = {
        name, layer_type: "vector",
        geometry_type: (fc._meta && fc._meta.geometry_type) || "GeoJSON",
        feature_count: (fc.features || []).length, fields: [], local: true,
      };
      G.MapView.addVector(name, fc);
      this.render();
      G.MapView.fitTo(name);
    },

    render() {
      const host = document.getElementById("layer-list");
      const empty = document.getElementById("layer-empty");
      const names = Object.keys(this._meta).filter((n) => G.MapView.has(n));
      host.innerHTML = "";
      empty.style.display = names.length ? "none" : "block";

      names.forEach((name) => {
        const meta = this._meta[name];
        const o = G.MapView.get(name);
        const isPoly = /polygon/i.test(meta.geometry_type || "");
        const card = document.createElement("div");
        card.className = "layer-card";
        card.innerHTML = `
          <div class="row1">
            <span class="swatch" title="Change color"></span>
            <span class="lname" title="${G.esc(name)}">${G.esc(name)}</span>
            <span class="gtype">${G.esc(meta.layer_type === "raster" ? "raster" : meta.geometry_type)}</span>
          </div>
          <div class="meta">${meta.layer_type === "raster" ? "raster overlay"
            : (meta.feature_count || 0) + " feature(s)"}${meta.local ? " · local" : ""}</div>
          <div class="ctrls"></div>`;
        card.querySelector(".swatch").style.background = o.color;
        this._wire(card, name, meta, o, isPoly);
        host.appendChild(card);
      });
    },

    _wire(card, name, meta, o, isPoly) {
      const ctrls = card.querySelector(".ctrls");

      // Visibility toggle
      const vis = document.createElement("button");
      vis.className = "icon-btn on"; vis.textContent = "👁";
      vis.title = "Toggle visibility";
      vis.onclick = () => {
        o.visible = !o.visible;
        G.MapView.setVisible(name, o.visible);
        vis.classList.toggle("on", o.visible);
      };
      ctrls.appendChild(vis);

      // Zoom-to
      const zoom = document.createElement("button");
      zoom.className = "icon-btn"; zoom.textContent = "⤢"; zoom.title = "Zoom to layer";
      zoom.onclick = () => G.MapView.fitTo(name);
      ctrls.appendChild(zoom);

      // Opacity
      const op = document.createElement("input");
      op.type = "range"; op.min = "0"; op.max = "1"; op.step = "0.05"; op.value = o.opacity;
      op.title = "Opacity";
      op.oninput = () => G.MapView.setOpacity(name, parseFloat(op.value));
      ctrls.appendChild(op);

      // Color picker (hidden input behind the swatch)
      const color = document.createElement("input");
      color.type = "color"; color.value = this._hex(o.color);
      color.style.cssText = "width:0;height:0;opacity:0;position:absolute;";
      color.oninput = () => {
        G.MapView.setColor(name, color.value);
        card.querySelector(".swatch").style.background = color.value;
      };
      card.querySelector(".swatch").onclick = () => color.click();
      ctrls.appendChild(color);

      // Remove
      const del = document.createElement("button");
      del.className = "icon-btn"; del.textContent = "✕"; del.title = "Remove from map";
      del.onclick = () => {
        G.MapView.remove(name);
        delete this._meta[name];
        this.render();
      };
      ctrls.appendChild(del);

      // 3D extrude (polygons only)
      if (isPoly) {
        const lbl = document.createElement("label");
        lbl.className = "chk3d";
        const cb = document.createElement("input");
        cb.type = "checkbox"; cb.checked = !!o.extrude;
        cb.onchange = () => {
          const field = (meta.fields || []).find((f) => /height|elev|z|floors?|stories/i.test(f));
          G.MapView.setExtrude(name, cb.checked, field);
        };
        lbl.appendChild(cb);
        lbl.appendChild(document.createTextNode("3D"));
        ctrls.appendChild(lbl);
      }
    },

    _hex(c) {
      if (!c) return "#4ea1ff";
      if (c[0] === "#") return c.length === 7 ? c : "#4ea1ff";
      const m = c.match(/\d+/g);
      if (!m) return "#4ea1ff";
      return "#" + m.slice(0, 3).map((n) => (+n).toString(16).padStart(2, "0")).join("");
    },
  };

  G.Layers = Layers;
})(window.GeoSI);
