/* GeoSI console — chat panel: prompt → /chat → plan/results/approval, then
   refresh the map so freshly-produced layers appear. */
(function (G) {
  "use strict";

  const Chat = {
    _transcript: null,

    init() {
      this._transcript = document.getElementById("transcript");
      return this;
    },

    _add(who, cls) {
      const wrap = document.createElement("div");
      wrap.className = "msg " + (cls || "");
      wrap.innerHTML = `<div class="who">${G.esc(who)}</div><div class="bubble"></div>`;
      this._transcript.appendChild(wrap);
      this._transcript.scrollTop = this._transcript.scrollHeight;
      return wrap.querySelector(".bubble");
    },

    clear() { this._transcript.innerHTML = ""; },

    _renderPlan(bubble, plan) {
      if (!plan || !Array.isArray(plan.steps) || !plan.steps.length) return;
      const div = document.createElement("div");
      div.className = "plan";
      let html = `<h4>Plan — ${G.esc(plan.plan_source || "")} (${plan.steps.length} step${plan.steps.length === 1 ? "" : "s"})</h4>`;
      plan.steps.forEach((s) => {
        const risk = s.risk_level || "read_only";
        html += `<div class="step"><span class="pill ${G.esc(risk)}">${G.esc(risk)}</span>`
          + `<span><b>${G.esc(s.tool_name)}</b> — ${G.esc(s.description || "")}</span></div>`;
      });
      div.innerHTML = html;
      bubble.appendChild(div);
    },

    _renderResults(bubble, results) {
      if (!results || !results.length) return;
      const div = document.createElement("div");
      div.className = "results";
      div.innerHTML = results.map((r) => `<div>• ${G.esc(r)}</div>`).join("");
      bubble.appendChild(div);
    },

    _renderApproval(bubble, actionId, query) {
      const div = document.createElement("div");
      div.className = "approval";
      div.innerHTML = `<b>⏸ Approval required</b>`
        + `<div>A mutating step needs confirmation (action <code>${G.esc(actionId)}</code>).</div>`;
      const act = document.createElement("div");
      act.className = "act";
      const yes = document.createElement("button");
      yes.className = "primary"; yes.textContent = "Approve & run";
      const no = document.createElement("button");
      no.className = "ghost"; no.textContent = "Reject";
      yes.onclick = async () => {
        yes.disabled = no.disabled = true;
        try {
          const r = await G.Api.approval(actionId, true);
          this._note(bubble, `Action ${actionId} → ${r.status}.`);
          await this.send(query, true);          // re-run so the approved step executes
        } catch (e) { this._err(bubble, "Approval failed: " + e.message); }
      };
      no.onclick = async () => {
        yes.disabled = no.disabled = true;
        try {
          const r = await G.Api.approval(actionId, false);
          this._note(bubble, `Action ${actionId} → ${r.status}.`);
        } catch (e) { this._err(bubble, "Reject failed: " + e.message); }
      };
      act.appendChild(yes); act.appendChild(no);
      div.appendChild(act);
      bubble.appendChild(div);
    },

    _note(bubble, text) {
      const n = document.createElement("div");
      n.className = "results"; n.textContent = text;
      bubble.appendChild(n);
    },
    _err(bubble, text) {
      const n = document.createElement("div");
      n.className = "err"; n.textContent = text;
      bubble.appendChild(n);
    },

    async send(queryText, isResume) {
      const promptEl = document.getElementById("prompt");
      const query = (queryText != null && isResume) ? queryText : promptEl.value.trim();
      if (!query) return;
      if (!isResume) {
        this._add("You", "user").textContent = query;
        promptEl.value = "";
        promptEl.style.height = "auto";
      }
      const sendBtn = document.getElementById("send");
      sendBtn.disabled = true;

      const layersEl = document.getElementById("layers-input");
      const layers = layersEl
        ? layersEl.value.split(",").map((s) => s.trim()).filter(Boolean) : [];
      const bubble = this._add("GeoSI");
      bubble.textContent = "Thinking…";

      try {
        const { status, data } = await G.Api.chat(query, layers, G.Layers._sessionId);
        if (status === 401 || status === 403) {
          bubble.innerHTML = `<span class="err">Authentication failed — check your API key.</span>`;
          G.App.setStatus(false);
          return;
        }
        G.App.setStatus(true);
        bubble.textContent = data.answer || (data.error ? "" : "(no answer)");
        if (data.error) this._err(bubble, data.error);
        this._renderPlan(bubble, data.plan);
        this._renderResults(bubble, data.results);
        if (data.approval_pending) this._renderApproval(bubble, data.approval_pending, query);
        // Pull any layers the pipeline produced onto the map.
        await G.Layers.refresh();
        G.MapView.fitAll();
      } catch (e) {
        bubble.innerHTML = `<span class="err">Request failed: ${G.esc(e.message)}</span>`;
        G.App.setStatus(false);
      } finally {
        sendBtn.disabled = false;
        this._transcript.scrollTop = this._transcript.scrollHeight;
      }
    },
  };

  G.Chat = Chat;
})(window.GeoSI);

