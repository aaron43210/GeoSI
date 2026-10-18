/* GeoSI console — shared namespace + API client (same-origin, Bearer auth). */
window.GeoSI = window.GeoSI || {};

(function (G) {
  "use strict";

  const KEY_STORE = "geosi.apiKey";

  const Api = {
    get key() {
      const el = document.getElementById("key");
      return (el && el.value.trim()) || "";
    },
    set key(v) {
      const el = document.getElementById("key");
      if (el) el.value = v || "";
    },
    headers(json) {
      const h = {};
      if (json) h["Content-Type"] = "application/json";
      const k = this.key;
      if (k) h["Authorization"] = "Bearer " + k;
      return h;
    },

    async chat(query, layers, sessionId) {
      const res = await fetch("/chat", {
        method: "POST",
        headers: this.headers(true),
        body: JSON.stringify({
          query,
          available_layers: layers || [],
          session_id: sessionId || null,
          surface: "web",
        }),
      });
      return { status: res.status, ok: res.ok, data: await res.json().catch(() => ({})) };
    },

    async approval(actionId, approve) {
      const verb = approve ? "approve" : "reject";
      const res = await fetch(`/approval/${encodeURIComponent(actionId)}/${verb}`, {
        method: "POST", headers: this.headers(true), body: JSON.stringify({}),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || res.statusText);
      return data;
    },

    async listLayers(sessionId) {
      const q = sessionId ? `?session_id=${encodeURIComponent(sessionId)}` : "";
      const res = await fetch(`/viz/layers${q}`, { headers: this.headers(false) });
      if (!res.ok) throw new Error(`layers ${res.status}`);
      return (await res.json()).layers || [];
    },

    async geojson(name, sessionId) {
      const q = sessionId ? `?session_id=${encodeURIComponent(sessionId)}` : "";
      const res = await fetch(`/viz/layers/${encodeURIComponent(name)}/geojson${q}`,
        { headers: this.headers(false) });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || `geojson ${res.status}`);
      return await res.json();
    },

    async raster(name, sessionId) {
      const q = sessionId ? `?session_id=${encodeURIComponent(sessionId)}` : "";
      const res = await fetch(`/viz/layers/${encodeURIComponent(name)}/raster${q}`,
        { headers: this.headers(false) });
      if (!res.ok) throw new Error(`raster ${res.status}`);
      return await res.json();
    },

    async health() {
      const res = await fetch("/health");
      return res.ok ? res.json() : null;
    },

    saveKey() { try { localStorage.setItem(KEY_STORE, this.key); } catch (e) {} },
    loadKey() { try { return localStorage.getItem(KEY_STORE) || ""; } catch (e) { return ""; } },
  };

  G.Api = Api;
  G.esc = (s) => String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
})(window.GeoSI);
