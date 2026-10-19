/* GeoSI console — chat panel: prompt → /chat → plan/results/approval.
   Approval: calls /approval/{id}/approve (or /reject) which returns the
   *resumed* execution result — no need to re-send the original query. */
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

    _renderResults(bubble, results, warnings) {
      if (results && results.length) {
        const div = document.createElement("div");
        div.className = "results";
        div.innerHTML = results.map((r) => `<div>• ${G.esc(r)}</div>`).join("");
        bubble.appendChild(div);
      }
      if (warnings && warnings.length) {
        const div = document.createElement("div");
        div.className = "results warn";
        div.innerHTML = warnings.map((w) => `<div>⚠ ${G.esc(w)}</div>`).join("");
        bubble.appendChild(div);
      }
    },

    _renderReport(bubble, report) {
      if (!report) return;
      const details = document.createElement("details");
      details.className = "report";
      const summary = document.createElement("summary");
      summary.textContent = "Execution report";
      const pre = document.createElement("pre");
      pre.textContent = report;
      details.appendChild(summary);
      details.appendChild(pre);
      bubble.appendChild(details);
    },

    // Render the approval widget.  On approve/reject, call the approval
    // endpoint and render the result — never re-send the original query.
    _renderApproval(bubble, actionId) {
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
        const resumeBubble = this._add("GeoSI");
        resumeBubble.textContent = "Running approved step…";
        try {
          const r = await G.Api.approval(actionId, true);
          resumeBubble.textContent = r.answer || (r.error ? "" : "(no answer)");
          if (r.error) this._err(resumeBubble, r.error);
          this._renderPlan(resumeBubble, r.plan);
          this._renderResults(resumeBubble, r.results, r.warnings);
          this._renderReport(resumeBubble, r.report);
          if (r.approval_pending) this._renderApproval(resumeBubble, r.approval_pending);
          await G.Layers.refresh();
          G.MapView.fitAll();
        } catch (e) { this._err(div, "Approval failed: " + e.message); yes.disabled = no.disabled = false; }
      };

      no.onclick = async () => {
        yes.disabled = no.disabled = true;
        try {
          const r = await G.Api.approval(actionId, false);
          this._note(div, r.answer || `Action ${actionId} rejected.`);
        } catch (e) { this._err(div, "Reject failed: " + e.message); yes.disabled = no.disabled = false; }
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

    async send(queryText) {
      const promptEl = document.getElementById("prompt");
      const query = queryText != null ? queryText : promptEl.value.trim();
      if (!query) return;
      this._add("You", "user").textContent = query;
      if (queryText == null) {
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
        this._renderResults(bubble, data.results, data.warnings);
        this._renderReport(bubble, data.report);
        if (data.approval_pending) this._renderApproval(bubble, data.approval_pending);
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
