/* lookup.js — semantic search over the study guides (Lookup mode).
 *
 * Flow (architecture §5.6 Lookup): debounce input ~220ms -> GET /search?q&k&lecture&topic
 * -> render cards with sanitized guide HTML, topic badge, "deck · p.X" citation,
 * similarity score, and an optional slide thumbnail that opens the shared lightbox.
 *
 * Security: r.html is bleach-sanitized server-side and rendered as-is; every other
 * field (text, title, topic, source_pdf, lecture_id) is escaped via SM.escapeHtml.
 */
(function () {
  "use strict";

  const SM = window.SM;
  const DEBOUNCE_MS = 220;
  const RESULT_K = 6;

  const form = document.getElementById("searchForm");
  const input = document.getElementById("q");
  const clearBtn = document.getElementById("searchClear");
  const lectureChips = document.getElementById("lectureChips");
  const topicChips = document.getElementById("topicChips");
  const statusEl = document.getElementById("lookupStatus");
  const resultsEl = document.getElementById("lookupResults");
  const hintEl = document.getElementById("lookupHint");

  const state = { lecture: "", topic: "" };
  let timer = null;
  let activeRequest = 0; // guards against out-of-order responses

  /* --------------------------------------------------------------- chips UI */

  function makeChip(label, dataAttr, dataValue, isActive) {
    const btn = SM.el("button", {
      type: "button",
      class: "chip" + (isActive ? " is-active" : ""),
      "aria-pressed": isActive ? "true" : "false",
    });
    btn.dataset[dataAttr] = dataValue;
    btn.textContent = label;
    return btn;
  }

  function buildLectureChips(lectures, failed) {
    const group = lectureChips.querySelector(".chips");
    group.textContent = "";
    lectureChips.removeAttribute("aria-busy");

    group.appendChild(makeChip("All lectures", "lecture", "", true));

    if (failed) {
      const note = SM.el("span", { class: "chips-loading" }, "Lecture filters unavailable.");
      group.appendChild(note);
      return;
    }
    for (const lec of lectures) {
      const label = "L" + lec.lecture_num + " · " + lec.title;
      const chip = makeChip(label, "lecture", lec.lecture_id, false);
      chip.title = SM.titleForLecture(lec.lecture_id);
      group.appendChild(chip);
    }
  }

  function buildTopicChips(topics) {
    const group = topicChips.querySelector(".chips");
    group.textContent = "";
    group.appendChild(makeChip("All topics", "topic", "", true));
    for (const topic of topics) {
      group.appendChild(makeChip(topic, "topic", topic, false));
    }
    // If no topics exist, hide the whole group rather than show an empty row.
    topicChips.hidden = topics.length === 0;
  }

  function setActiveChip(group, value, attr) {
    group.querySelectorAll(".chip").forEach((chip) => {
      const isActive = (chip.dataset[attr] || "") === value;
      chip.classList.toggle("is-active", isActive);
      chip.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  lectureChips.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    state.lecture = chip.dataset.lecture || "";
    setActiveChip(lectureChips, state.lecture, "lecture");
    run(true);
  });

  topicChips.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    state.topic = chip.dataset.topic || "";
    setActiveChip(topicChips, state.topic, "topic");
    run(true);
  });

  /* --------------------------------------------------------------- results */

  function citationLabel(r) {
    const deck = SM.escapeHtml(r.source_pdf || r.title || "Study guide");
    if (r.page && r.page > 0) {
      return deck + " · p." + r.page;
    }
    return deck;
  }

  function renderCard(r) {
    const card = SM.el("article", { class: "result-card" });

    // --- meta row: lecture badge, topic, citation, score ---
    const meta = SM.el("div", { class: "result-meta" });

    if (r.lecture_id) {
      meta.appendChild(
        SM.el(
          "span",
          { class: "badge badge-lecture", title: SM.titleForLecture(r.lecture_id) },
          r.lecture_id
        )
      );
    }
    if (r.topic) {
      meta.appendChild(SM.el("span", { class: "badge badge-topic" }, r.topic));
    }

    const cite = SM.el("span", { class: "result-cite" });
    cite.textContent = (r.source_pdf || r.title || "Study guide") +
      (r.page && r.page > 0 ? " · p." + r.page : "");
    meta.appendChild(cite);

    if (typeof r.score === "number" || typeof r.score === "string") {
      meta.appendChild(SM.el("span", { class: "result-score", title: "Cosine similarity" }, "sim " + r.score));
    }
    card.appendChild(meta);

    // --- title ---
    if (r.title) {
      card.appendChild(SM.el("h3", { class: "result-title" }, r.title));
    }

    // --- body: prefer server-sanitized HTML; otherwise escaped plain text ---
    const body = SM.el("div", { class: "result-body" });
    if (r.html) {
      // r.html is sanitized server-side (bleach allowlist, architecture §9).
      body.innerHTML = r.html;
    } else {
      body.appendChild(SM.el("p", null, r.text || ""));
    }
    card.appendChild(body);

    // --- optional slide thumbnail -> lightbox ---
    if (r.img) {
      const caption =
        (r.source_pdf || "Slide") + (r.page ? " · page " + r.page : "");
      const link = SM.el("a", {
        class: "slide-link",
        href: r.img,
        target: "_blank",
        rel: "noopener",
        title: "Open slide " + caption,
      });
      link.dataset.caption = caption;
      const thumb = SM.el("img", {
        class: "slide-thumb",
        src: r.img,
        loading: "lazy",
        alt: "Slide preview — " + caption,
      });
      link.appendChild(thumb);
      link.appendChild(SM.el("span", { class: "slide-cap" }, "View source slide"));
      card.appendChild(link);
    }

    return card;
  }

  function renderResults(data, term) {
    resultsEl.textContent = "";
    const list = (data && data.results) || [];
    if (!list.length) {
      hintEl.hidden = true;
      resultsEl.appendChild(
        SM.el("div", { class: "empty-hint empty-result" }, [
          SM.el("p", { class: "empty-title" }, "No matches"),
          SM.el(
            "p",
            { class: "empty-body" },
            'Nothing in the guides matched "' + term + '"' +
              (state.lecture || state.topic ? " under the current filters." : ".") +
              " Try broader wording or clear the filters."
          ),
        ])
      );
      return;
    }
    hintEl.hidden = true;
    const frag = document.createDocumentFragment();
    for (const r of list) frag.appendChild(renderCard(r));
    resultsEl.appendChild(frag);
  }

  /* --------------------------------------------------------------- search */

  function buildUrl(term) {
    const params = new URLSearchParams();
    params.set("q", term);
    params.set("k", String(RESULT_K));
    if (state.lecture) params.set("lecture", state.lecture);
    if (state.topic) params.set("topic", state.topic);
    return "/search?" + params.toString();
  }

  async function run(immediate) {
    clearTimeout(timer);
    const exec = async () => {
      const term = input.value.trim();
      clearBtn.hidden = input.value.length === 0;

      if (term.length < 2) {
        resultsEl.textContent = "";
        statusEl.textContent = "";
        hintEl.hidden = false;
        return;
      }

      const requestId = ++activeRequest;
      statusEl.textContent = "Searching…";

      try {
        const data = await SM.getJSON(buildUrl(term));
        if (requestId !== activeRequest) return; // a newer query superseded this one
        const count = (data.results || []).length;
        const scopeBits = [];
        if (state.lecture) scopeBits.push(state.lecture);
        if (state.topic) scopeBits.push(state.topic);
        const scope = scopeBits.length ? " · " + scopeBits.join(" · ") : "";
        statusEl.textContent =
          count + (count === 1 ? " result" : " results") +
          ' for "' + term + '"' + scope;
        renderResults(data, term);
      } catch (err) {
        if (requestId !== activeRequest) return;
        statusEl.textContent = "Search failed: " + err.message;
      }
    };

    if (immediate) exec();
    else timer = setTimeout(exec, DEBOUNCE_MS);
  }

  /* ------------------------------------------------------------- listeners */

  input.addEventListener("input", () => run(false));
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    run(true);
  });
  clearBtn.addEventListener("click", () => {
    input.value = "";
    clearBtn.hidden = true;
    input.focus();
    run(true);
  });

  // Focus the search box when the user switches into Lookup mode.
  document.addEventListener("sm:modechange", (e) => {
    if (e.detail && e.detail.mode === "lookup") {
      // Defer so the panel is visible before focusing.
      window.requestAnimationFrame(() => input.focus());
    }
  });

  /* ----------------------------------------------------- slide lightbox */

  const modal = document.getElementById("slideModal");
  const modalImg = document.getElementById("slideModalImg");
  const modalCap = document.getElementById("slideModalCap");
  const modalClose = document.getElementById("slideModalClose");
  let lastFocused = null;

  function openModal(src, caption) {
    lastFocused = document.activeElement;
    modalImg.src = src;
    modalImg.alt = caption || "Slide preview";
    modalCap.textContent = caption || "";
    modal.hidden = false;
    document.body.classList.add("modal-open");
    modalClose.focus();
  }

  function closeModal() {
    modal.hidden = true;
    modalImg.removeAttribute("src"); // stop loading / free memory
    document.body.classList.remove("modal-open");
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
    lastFocused = null;
  }

  // Open when a slide thumbnail is clicked (allow modified clicks to open a tab).
  resultsEl.addEventListener("click", (e) => {
    const link = e.target.closest(".slide-link");
    if (!link) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    openModal(link.getAttribute("href"), link.dataset.caption || "Slide preview");
  });

  modal.addEventListener("click", (e) => {
    // Click on the backdrop (outside the shell) closes.
    if (e.target === modal) closeModal();
  });
  modalClose.addEventListener("click", closeModal);

  document.addEventListener("keydown", (e) => {
    if (modal.hidden) return;
    if (e.key === "Escape") {
      e.preventDefault();
      closeModal();
    } else if (e.key === "Tab") {
      // Simple focus trap: only the close button is focusable here.
      e.preventDefault();
      modalClose.focus();
    }
  });

  /* ------------------------------------------------------------- bootstrap */

  SM.onLecturesReady((lectures, failed) => {
    buildLectureChips(lectures || [], failed);
    buildTopicChips(SM.topics || []);
  });
})();
