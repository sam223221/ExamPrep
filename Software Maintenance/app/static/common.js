/* common.js — shared foundation for the two-mode Software Maintenance study app.
 *
 * Exposes a small global `SM` namespace used by lookup.js and quiz.js:
 *   SM.escapeHtml(str)        — escape untrusted text for safe innerHTML interpolation
 *   SM.getJSON(url)           — fetch + JSON with structured error handling
 *   SM.el(tag, attrs, kids)   — tiny DOM builder (no innerHTML of model text)
 *   SM.lectures               — loaded lecture metadata (array) or null until ready
 *   SM.topics                 — derived sorted union of topics across lectures
 *   SM.titleForLecture(id)    — "L04" -> "Lecture 4 — <title>"
 *   SM.onLecturesReady(fn)     — register a callback fired once metadata is loaded
 *   SM.difficultyLabel(d)     — "very-hard" -> "Very hard"
 *
 * No build step, no dependencies. All model-derived text is escaped or sanitized
 * server-side (guide HTML arrives bleach-clean); this file never injects raw text.
 */
(function () {
  "use strict";

  const SM = (window.SM = window.SM || {});

  /* ---------------------------------------------------------------- escaping */

  const ESCAPE_MAP = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  };

  SM.escapeHtml = function escapeHtml(value) {
    if (value === null || value === undefined) return "";
    return String(value).replace(/[&<>"']/g, (c) => ESCAPE_MAP[c]);
  };

  /* --------------------------------------------------------------- fetch i/o */

  SM.getJSON = async function getJSON(url, options) {
    let res;
    try {
      res = await fetch(url, options);
    } catch (networkErr) {
      throw new Error("Could not reach the server. Is it running?");
    }
    if (!res.ok) {
      // Try to surface FastAPI's structured error detail when present.
      let detail = "";
      try {
        const body = await res.json();
        if (body && body.detail) {
          detail =
            typeof body.detail === "string"
              ? body.detail
              : JSON.stringify(body.detail);
        }
      } catch (_) {
        /* response was not JSON; fall through to status text */
      }
      const message = detail || res.statusText || "Request failed";
      const err = new Error(message);
      err.status = res.status;
      throw err;
    }
    return res.json();
  };

  /* --------------------------------------------------------------- DOM build */

  // Minimal element factory. Text content is set via textContent (never innerHTML)
  // so callers cannot accidentally inject markup through it.
  SM.el = function el(tag, attrs, children) {
    const node = document.createElement(tag);
    if (attrs) {
      for (const key of Object.keys(attrs)) {
        const val = attrs[key];
        if (val === null || val === undefined || val === false) continue;
        if (key === "class") node.className = val;
        else if (key === "text") node.textContent = val;
        else if (key === "html") node.innerHTML = val; // ONLY for server-sanitized HTML
        else if (key.startsWith("on") && typeof val === "function") {
          node.addEventListener(key.slice(2).toLowerCase(), val);
        } else if (key === "dataset") {
          for (const dk of Object.keys(val)) node.dataset[dk] = val[dk];
        } else if (val === true) {
          node.setAttribute(key, "");
        } else {
          node.setAttribute(key, val);
        }
      }
    }
    if (children !== null && children !== undefined) {
      const list = Array.isArray(children) ? children : [children];
      for (const child of list) {
        if (child === null || child === undefined || child === false) continue;
        node.appendChild(
          typeof child === "string" ? document.createTextNode(child) : child
        );
      }
    }
    return node;
  };

  /* ------------------------------------------------------------ labels/util */

  const DIFFICULTY_LABELS = {
    easy: "Easy",
    medium: "Medium",
    hard: "Hard",
    "very-hard": "Very hard",
  };

  SM.difficultyLabel = function difficultyLabel(d) {
    return DIFFICULTY_LABELS[d] || d || "";
  };

  SM.titleForLecture = function titleForLecture(lectureId) {
    if (!SM.lectures) return lectureId;
    const found = SM.lectures.find((l) => l.lecture_id === lectureId);
    if (!found) return lectureId;
    return "Lecture " + found.lecture_num + " — " + found.title;
  };

  // Short label e.g. "L04" for chips/badges.
  SM.shortLecture = function shortLecture(lectureId, lectureNum) {
    if (lectureNum !== undefined && lectureNum !== null) return "L" + lectureNum;
    return lectureId || "";
  };

  /* ----------------------------------------------------- lecture metadata */

  SM.lectures = null;
  SM.topics = [];
  let _ready = false;
  let _failed = null;
  const _readyCallbacks = [];

  SM.onLecturesReady = function onLecturesReady(fn) {
    if (typeof fn !== "function") return;
    if (_ready) {
      fn(SM.lectures, _failed);
    } else {
      _readyCallbacks.push(fn);
    }
  };

  function deriveTopics(lectures) {
    const set = new Set();
    for (const lec of lectures) {
      if (Array.isArray(lec.topics)) {
        for (const t of lec.topics) {
          if (t) set.add(t);
        }
      }
    }
    return Array.from(set).sort((a, b) => a.localeCompare(b));
  }

  async function loadLectures() {
    try {
      const data = await SM.getJSON("/api/lectures");
      // Defensive: ensure numeric ordering even if the server already sorts.
      const list = Array.isArray(data) ? data.slice() : [];
      list.sort((a, b) => (a.lecture_num || 0) - (b.lecture_num || 0));
      SM.lectures = list;
      SM.topics = deriveTopics(list);
    } catch (err) {
      _failed = err;
      SM.lectures = [];
      SM.topics = [];
    } finally {
      _ready = true;
      for (const cb of _readyCallbacks.splice(0)) {
        try {
          cb(SM.lectures, _failed);
        } catch (cbErr) {
          // A failing consumer must not break the others.
          console.error("onLecturesReady callback failed:", cbErr);
        }
      }
    }
  }

  /* ----------------------------------------------------- mode toggle (tabs) */

  function initModeToggle() {
    const toggle = document.getElementById("modeToggle");
    if (!toggle) return;
    const buttons = Array.from(toggle.querySelectorAll(".mode-btn"));
    const views = {
      lookup: document.getElementById("lookup-view"),
      quiz: document.getElementById("quiz-view"),
    };

    function activate(mode, focusPanel) {
      buttons.forEach((btn) => {
        const isActive = btn.dataset.mode === mode;
        btn.classList.toggle("is-active", isActive);
        btn.setAttribute("aria-selected", isActive ? "true" : "false");
        btn.tabIndex = isActive ? 0 : -1;
      });
      Object.keys(views).forEach((key) => {
        const view = views[key];
        if (!view) return;
        const show = key === mode;
        view.classList.toggle("is-active", show);
        view.hidden = !show;
      });
      // Let mode-specific scripts react (e.g. focus the search box).
      document.dispatchEvent(
        new CustomEvent("sm:modechange", { detail: { mode } })
      );
      if (focusPanel && views[mode]) {
        // Move focus into the newly shown panel for keyboard/AT users.
        const focusTarget = views[mode].querySelector(
          'input, select, button, [tabindex]:not([tabindex="-1"])'
        );
        if (focusTarget) focusTarget.focus();
      }
    }

    toggle.addEventListener("click", (e) => {
      const btn = e.target.closest(".mode-btn");
      if (!btn) return;
      activate(btn.dataset.mode, false);
    });

    // Roving-tabindex keyboard support for the tablist (ARIA pattern).
    toggle.addEventListener("keydown", (e) => {
      const idx = buttons.indexOf(document.activeElement);
      if (idx === -1) return;
      let nextIdx = null;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") nextIdx = (idx + 1) % buttons.length;
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp") nextIdx = (idx - 1 + buttons.length) % buttons.length;
      else if (e.key === "Home") nextIdx = 0;
      else if (e.key === "End") nextIdx = buttons.length - 1;
      if (nextIdx === null) return;
      e.preventDefault();
      const target = buttons[nextIdx];
      activate(target.dataset.mode, true);
      target.focus();
    });

    SM.activateMode = activate;
  }

  /* ------------------------------------------------------------- bootstrap */

  function boot() {
    initModeToggle();
    loadLectures();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
