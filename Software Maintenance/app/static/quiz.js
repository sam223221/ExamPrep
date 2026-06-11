/* quiz.js — interactive practice mode (Quiz).
 *
 * Flow (architecture §5.6 Quiz):
 *  1. User picks lecture/topic/difficulty/count -> GET /api/quiz?... (no answers in payload)
 *  2. Render one question at a time; selections are kept locally.
 *  3. On submit -> POST /api/quiz/check {answers:[{id,chosen}]}
 *  4. Render score + per-question right/wrong + revealed explanation & citation.
 *  5. Offer "Retry these" (re-attempt same questions) and "New set".
 *
 * Quizzes are ephemeral — nothing is persisted across reloads (architecture open-Q #4).
 * Security: every piece of model text (stem, option text, explanation, source) is
 * escaped via SM.escapeHtml / textContent. No raw HTML injection in this file.
 */
(function () {
  "use strict";

  const SM = window.SM;

  // Elements
  const setupForm = document.getElementById("quizSetup");
  const lectureSelect = document.getElementById("quizLecture");
  const topicSelect = document.getElementById("quizTopic");
  const difficultySelect = document.getElementById("quizDifficulty");
  const countSelect = document.getElementById("quizCount");
  const startBtn = document.getElementById("quizStart");
  const setupNote = document.getElementById("quizSetupNote");
  const statusEl = document.getElementById("quizStatus");

  const runner = document.getElementById("quizRunner");
  const progressBar = document.getElementById("quizProgressBar");
  const progressLabel = document.getElementById("quizProgressLabel");
  const questionHost = document.getElementById("quizQuestionHost");
  const prevBtn = document.getElementById("quizPrev");
  const nextBtn = document.getElementById("quizNext");
  const submitBtn = document.getElementById("quizSubmit");
  const abortBtn = document.getElementById("quizAbort");

  const resultsEl = document.getElementById("quizResults");

  // Session state (ephemeral)
  let session = null;
  /* session = {
       questions: [ { id, lecture_id, topic, difficulty, stem, options:[{key,text}] } ],
       chosen:    { [id]: "A" },        // local selections
       index:     0,                    // current question
       graded:    null,                 // results map after /check
     } */

  /* ------------------------------------------------------ populate selects */

  function populateSetup(lectures, failed) {
    if (failed) {
      setupNote.textContent = "Could not load lecture list — practice unavailable.";
      startBtn.disabled = true;
      return;
    }
    if (!lectures.length) {
      setupNote.textContent = "No lecture material is available yet.";
      startBtn.disabled = true;
      return;
    }
    // Lectures
    for (const lec of lectures) {
      const opt = SM.el("option", { value: lec.lecture_id });
      opt.textContent = "Lecture " + lec.lecture_num + " — " + lec.title;
      lectureSelect.appendChild(opt);
    }
    // Topics
    for (const topic of SM.topics) {
      const opt = SM.el("option", { value: topic });
      opt.textContent = topic;
      topicSelect.appendChild(opt);
    }
  }

  /* ----------------------------------------------------------- fetch quiz */

  function buildQuizUrl() {
    const params = new URLSearchParams();
    const lecture = lectureSelect.value || "all";
    params.set("lecture", lecture);
    if (topicSelect.value) params.set("topic", topicSelect.value);
    if (difficultySelect.value) params.set("difficulty", difficultySelect.value);
    params.set("n", countSelect.value || "10");
    return "/api/quiz?" + params.toString();
  }

  async function startQuiz(e) {
    e.preventDefault();
    statusEl.textContent = "Building your set…";
    setupNote.textContent = "";
    startBtn.disabled = true;
    resultsEl.hidden = true;
    resultsEl.textContent = "";

    try {
      const data = await SM.getJSON(buildQuizUrl());
      const questions = (data && data.questions) || [];
      if (!questions.length) {
        statusEl.textContent =
          "No questions match those filters. Try widening the scope.";
        startBtn.disabled = false;
        return;
      }
      session = {
        questions,
        chosen: Object.create(null),
        index: 0,
        graded: null,
      };
      statusEl.textContent = "";
      setupForm.hidden = true;
      runner.hidden = false;
      renderQuestion();
      // Focus the question heading for screen-reader context.
      const heading = questionHost.querySelector(".question-stem");
      if (heading) heading.focus();
    } catch (err) {
      const msg =
        err.status === 404
          ? "No questions match those filters. Try widening the scope."
          : "Could not build the set: " + err.message;
      statusEl.textContent = msg;
      startBtn.disabled = false;
    }
  }

  /* ------------------------------------------------------- render question */

  function renderQuestion() {
    if (!session) return;
    const total = session.questions.length;
    const q = session.questions[session.index];

    questionHost.textContent = "";

    const card = SM.el("div", { class: "question-card" });

    // tag row
    const tags = SM.el("div", { class: "question-tags" });
    if (q.lecture_id) {
      tags.appendChild(
        SM.el(
          "span",
          { class: "badge badge-lecture", title: SM.titleForLecture(q.lecture_id) },
          q.lecture_id
        )
      );
    }
    if (q.topic) tags.appendChild(SM.el("span", { class: "badge badge-topic" }, q.topic));
    if (q.difficulty) {
      tags.appendChild(
        SM.el(
          "span",
          { class: "badge badge-diff diff-" + SM.escapeHtml(q.difficulty) },
          SM.difficultyLabel(q.difficulty)
        )
      );
    }
    card.appendChild(tags);

    // stem (focusable for AT)
    const stem = SM.el(
      "h3",
      { class: "question-stem", id: "stem-" + q.id, tabindex: "-1" },
      q.stem || ""
    );
    card.appendChild(stem);

    // options as a radiogroup
    const group = SM.el("div", {
      class: "options",
      role: "radiogroup",
      "aria-labelledby": "stem-" + q.id,
    });
    const chosenKey = session.chosen[q.id];

    (q.options || []).forEach((opt) => {
      const checked = chosenKey === opt.key;
      const optId = "opt-" + q.id + "-" + opt.key;
      const label = SM.el("label", {
        class: "option" + (checked ? " is-selected" : ""),
        for: optId,
      });

      const radio = SM.el("input", {
        type: "radio",
        class: "option-input",
        name: "q-" + q.id,
        id: optId,
        value: opt.key,
      });
      if (checked) radio.checked = true;
      radio.addEventListener("change", () => {
        session.chosen[q.id] = opt.key;
        // Update selected styling without a full re-render.
        group.querySelectorAll(".option").forEach((el) => el.classList.remove("is-selected"));
        label.classList.add("is-selected");
        refreshNav();
      });

      const keyTag = SM.el("span", { class: "option-key", "aria-hidden": "true" }, opt.key);
      const text = SM.el("span", { class: "option-text" }, opt.text || "");

      label.appendChild(radio);
      label.appendChild(keyTag);
      label.appendChild(text);
      group.appendChild(label);
    });

    card.appendChild(group);
    questionHost.appendChild(card);

    // progress
    const answered = countAnswered();
    progressBar.style.width = ((session.index + 1) / total) * 100 + "%";
    progressLabel.textContent =
      "Question " + (session.index + 1) + " of " + total +
      " · " + answered + " answered";

    refreshNav();
  }

  function countAnswered() {
    if (!session) return 0;
    return session.questions.filter((q) => session.chosen[q.id] !== undefined).length;
  }

  function refreshNav() {
    if (!session) return;
    const total = session.questions.length;
    prevBtn.disabled = session.index === 0;
    nextBtn.disabled = session.index >= total - 1;
    const allAnswered = countAnswered() === total;
    submitBtn.disabled = !allAnswered;
    submitBtn.title = allAnswered
      ? "Grade your answers"
      : "Answer every question to submit (" + countAnswered() + "/" + total + ")";
  }

  /* ---------------------------------------------------------- navigation */

  prevBtn.addEventListener("click", () => {
    if (!session || session.index === 0) return;
    session.index--;
    renderQuestion();
    focusStem();
  });
  nextBtn.addEventListener("click", () => {
    if (!session || session.index >= session.questions.length - 1) return;
    session.index++;
    renderQuestion();
    focusStem();
  });

  function focusStem() {
    const stem = questionHost.querySelector(".question-stem");
    if (stem) stem.focus();
  }

  // Keyboard shortcuts while the runner is visible: arrow nav + A–D select.
  document.addEventListener("keydown", (e) => {
    if (!session || session.graded || runner.hidden) return;
    if (e.target && /^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName) && e.target.type !== "radio") {
      return;
    }
    const key = e.key.toUpperCase();
    if (["A", "B", "C", "D"].includes(key)) {
      const radio = questionHost.querySelector('.option-input[value="' + key + '"]');
      if (radio) {
        radio.checked = true;
        radio.dispatchEvent(new Event("change", { bubbles: true }));
        radio.focus();
        e.preventDefault();
      }
    }
  });

  abortBtn.addEventListener("click", () => {
    if (countAnswered() > 0 && !window.confirm("Discard this practice set?")) return;
    resetToSetup();
  });

  function resetToSetup() {
    session = null;
    runner.hidden = true;
    resultsEl.hidden = true;
    resultsEl.textContent = "";
    setupForm.hidden = false;
    startBtn.disabled = false;
    statusEl.textContent = "";
    questionHost.textContent = "";
    setupForm.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  /* ------------------------------------------------------------- grading */

  submitBtn.addEventListener("click", submitAnswers);

  async function submitAnswers() {
    if (!session) return;
    if (countAnswered() !== session.questions.length) return;

    submitBtn.disabled = true;
    submitBtn.textContent = "Grading…";

    const answers = session.questions.map((q) => ({
      id: q.id,
      chosen: session.chosen[q.id],
    }));

    try {
      const data = await SM.getJSON("/api/quiz/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers }),
      });
      session.graded = data;
      renderResults(data);
    } catch (err) {
      statusEl.textContent = "Grading failed: " + err.message;
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit answers";
    }
  }

  /* ------------------------------------------------------------- results */

  function renderResults(data) {
    runner.hidden = true;
    resultsEl.textContent = "";
    resultsEl.hidden = false;

    const total = data.total != null ? data.total : session.questions.length;
    const score = data.score != null ? data.score : 0;
    const pct = total ? Math.round((score / total) * 100) : 0;
    const resultMap = Object.create(null);
    for (const r of data.results || []) resultMap[r.id] = r;

    // Scoreboard
    const board = SM.el("div", { class: "scoreboard" });
    const ring = SM.el("div", {
      class: "score-ring",
      role: "img",
      "aria-label": "Score " + score + " out of " + total + ", " + pct + " percent",
    });
    ring.style.setProperty("--pct", pct);
    ring.appendChild(SM.el("span", { class: "score-pct" }, pct + "%"));
    board.appendChild(ring);

    const boardText = SM.el("div", { class: "score-text" });
    boardText.appendChild(SM.el("p", { class: "score-headline" }, score + " / " + total + " correct"));
    boardText.appendChild(
      SM.el("p", { class: "score-sub" }, gradeMessage(pct))
    );
    board.appendChild(boardText);
    resultsEl.appendChild(board);

    // Actions
    const actions = SM.el("div", { class: "results-actions" });
    const retryBtn = SM.el("button", { type: "button", class: "btn btn-ghost" }, "Retry these questions");
    retryBtn.addEventListener("click", retrySameSet);
    const newBtn = SM.el("button", { type: "button", class: "btn btn-primary" }, "New set");
    newBtn.addEventListener("click", resetToSetup);
    actions.appendChild(retryBtn);
    actions.appendChild(newBtn);
    resultsEl.appendChild(actions);

    // Per-question review
    const review = SM.el("ol", { class: "review-list" });
    session.questions.forEach((q, i) => {
      const r = resultMap[q.id] || { correct: false };
      review.appendChild(renderReviewItem(q, r, i + 1));
    });
    resultsEl.appendChild(review);

    resultsEl.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function gradeMessage(pct) {
    if (pct >= 90) return "Exam-ready on this scope. Strong recall.";
    if (pct >= 70) return "Solid. Review the misses below and run it again.";
    if (pct >= 50) return "Getting there — focus on the explanations below.";
    return "Worth a careful re-read of the cited slides, then retry.";
  }

  function renderReviewItem(q, r, ordinal) {
    const correctKey = r.answer;
    const chosenKey = session.chosen[q.id];
    const isCorrect = !!r.correct;

    const item = SM.el("li", {
      class: "review-item " + (isCorrect ? "is-correct" : "is-wrong"),
    });

    const head = SM.el("div", { class: "review-head" });
    head.appendChild(
      SM.el(
        "span",
        { class: "review-verdict", "aria-hidden": "true" },
        isCorrect ? "✓" : "✗"
      )
    );
    head.appendChild(SM.el("span", { class: "review-num" }, "Q" + ordinal));
    head.appendChild(
      SM.el(
        "span",
        { class: "review-status" },
        isCorrect ? "Correct" : "Incorrect"
      )
    );
    if (q.difficulty) {
      head.appendChild(
        SM.el(
          "span",
          { class: "badge badge-diff diff-" + SM.escapeHtml(q.difficulty) },
          SM.difficultyLabel(q.difficulty)
        )
      );
    }
    item.appendChild(head);

    item.appendChild(SM.el("p", { class: "review-stem" }, q.stem || ""));

    // Options with correct/chosen markers
    const opts = SM.el("ul", { class: "review-options" });
    (q.options || []).forEach((opt) => {
      const classes = ["review-option"];
      let marker = "";
      if (opt.key === correctKey) {
        classes.push("opt-correct");
        marker = "Correct answer";
      }
      if (opt.key === chosenKey && opt.key !== correctKey) {
        classes.push("opt-chosen-wrong");
        marker = "Your answer";
      } else if (opt.key === chosenKey && opt.key === correctKey) {
        marker = "Your answer · correct";
      }
      const li = SM.el("li", { class: classes.join(" ") });
      li.appendChild(SM.el("span", { class: "option-key", "aria-hidden": "true" }, opt.key));
      li.appendChild(SM.el("span", { class: "option-text" }, opt.text || ""));
      if (marker) li.appendChild(SM.el("span", { class: "option-marker" }, marker));
      opts.appendChild(li);
    });
    item.appendChild(opts);

    // Explanation + citation (revealed only now, post-grade)
    if (r.explanation) {
      const exp = SM.el("div", { class: "review-explanation" });
      exp.appendChild(SM.el("span", { class: "explanation-label" }, "Why"));
      exp.appendChild(SM.el("p", null, r.explanation));
      item.appendChild(exp);
    }
    if (r.source && (r.source.deck || r.source.page)) {
      const citeText =
        (r.source.deck || "Source") +
        (r.source.page ? " · p." + r.source.page : "");
      item.appendChild(SM.el("p", { class: "review-cite" }, citeText));
    }

    return item;
  }

  /* -------------------------------------------------------- retry same set */

  function retrySameSet() {
    if (!session) return;
    session.chosen = Object.create(null);
    session.index = 0;
    session.graded = null;
    resultsEl.hidden = true;
    resultsEl.textContent = "";
    runner.hidden = false;
    submitBtn.textContent = "Submit answers";
    renderQuestion();
    focusStem();
    runner.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  /* ------------------------------------------------------------- bootstrap */

  setupForm.addEventListener("submit", startQuiz);

  SM.onLecturesReady((lectures, failed) => {
    populateSetup(lectures || [], failed);
  });
})();
