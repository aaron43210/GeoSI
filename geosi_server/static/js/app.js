/* GeoSI console — bootstrap: wires DOM controls, initializes map + chat,
   persists the API key, and tracks connection status. */
(function (G) {
  "use strict";

  const App = {
    _dot: null,

    setStatus(ok) {
      if (!this._dot) return;
      this._dot.classList.toggle("ok", !!ok);
      this._dot.classList.toggle("err", ok === false);
      this._dot.title = ok ? "Connected" : "Not connected";
    },

    _badge(text) {
      const b = document.getElementById("map-badge");
      if (!b) return;
      if (!text) { b.style.display = "none"; return; }
      b.textContent = text;
      b.style.display = "block";
    },

    async _ping() {
      try {
        const h = await G.Api.health();
        this.setStatus(!!h);
      } catch (e) { this.setStatus(false); }
    },

    _wireKey() {
      const key = document.getElementById("key");
      key.value = G.Api.loadKey();
      // The session id defaults to the API key server-side; keep layers in sync.
      G.Layers.setSession(key.value || null);
      key.addEventListener("change", () => {
        G.Api.saveKey();
        G.Layers.setSession(key.value.trim() || null);
        this._ping().then(() => G.Layers.refresh());
      });
    },

    _wireComposer() {
      const prompt = document.getElementById("prompt");
      const send = document.getElementById("send");
      const autosize = () => {
        prompt.style.height = "auto";
        prompt.style.height = Math.min(prompt.scrollHeight, 160) + "px";
      };
      prompt.addEventListener("input", autosize);
      // Enter sends; Shift+Enter inserts a newline.
      prompt.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          G.Chat.send();
        }
      });
      send.addEventListener("click", () => G.Chat.send());
      document.getElementById("chat-clear")
        .addEventListener("click", () => G.Chat.clear());
    },

    _wireMapTools() {
      document.querySelectorAll("[data-basemap]").forEach((btn) => {
        btn.addEventListener("click", () => {
          document.querySelectorAll("[data-basemap]")
            .forEach((b) => b.classList.remove("active"));
          btn.classList.add("active");
          G.MapView.setBasemap(btn.dataset.basemap);
        });
      });

      const b2d = document.getElementById("btn-2d");
      const b3d = document.getElementById("btn-3d");
      const setDim = (is3d) => {
        G.MapView.set3D(is3d);
        b3d.classList.toggle("active", is3d);
        b2d.classList.toggle("active", !is3d);
      };
      b2d.addEventListener("click", () => setDim(false));
      b3d.addEventListener("click", () => setDim(true));

      const terrain = document.getElementById("btn-terrain");
      terrain.addEventListener("click", () => {
        const on = G.MapView.toggleTerrain();
        terrain.classList.toggle("active", on);
        if (on) { b3d.classList.add("active"); b2d.classList.remove("active"); }
        this._badge(on ? "3D terrain on" : "");
      });

      document.getElementById("btn-fit")
        .addEventListener("click", () => G.MapView.fitAll());
    },

    _wireLayerPanel() {
      document.getElementById("layers-refresh")
        .addEventListener("click", () => G.Layers.refresh());

      document.getElementById("geojson-file").addEventListener("change", (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          try {
            const fc = JSON.parse(reader.result);
            const name = file.name.replace(/\.(geo)?json$/i, "");
            G.Layers.addLocalGeoJSON(name, fc);
          } catch (err) {
            alert("Could not parse GeoJSON: " + err.message);
          }
        };
        reader.readAsText(file);
        e.target.value = "";   // allow re-adding the same file
      });
    },

    async init() {
      this._dot = document.getElementById("status-dot");
      G.MapView.init();
      G.Chat.init();
      this._wireKey();
      this._wireComposer();
      this._wireMapTools();
      this._wireLayerPanel();
      await this._ping();
      G.Layers.refresh();   // show any pre-existing session layers
    },
  };

  G.App = App;
  window.addEventListener("DOMContentLoaded", () => App.init());
})(window.GeoSI);
