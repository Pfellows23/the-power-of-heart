/* Page-turning reader for the private book area (book-preview.html).
   build.py inlines this file into the page together with the list of pages
   (window.BOOK_PAGES). Each page is {src, alt} for a photo of a book page,
   or {html} for a page written in HTML (the welcome page).
   Wide screens show two facing pages; narrow screens show one page at a time.
   Turn pages with the arrows, the keyboard, a click on either page, or a swipe. */
(function () {
  var pages = window.BOOK_PAGES || [];
  var root = document.getElementById("reader");
  if (!root || !pages.length) return;
  var stage = root.querySelector(".reader-stage");
  var book = root.querySelector(".reader-book");
  var leftEl = root.querySelector(".reader-left");
  var rightEl = root.querySelector(".reader-right");
  var prevBtn = root.querySelector(".reader-prev");
  var nextBtn = root.querySelector(".reader-next");
  var count = root.querySelector(".reader-count");
  var slider = root.querySelector(".reader-slider");
  var live = root.querySelector(".reader-live");
  var words = root.querySelector(".reader-words");
  var N = pages.length;
  var mq = window.matchMedia("(min-width: 760px)");
  var two = mq.matches;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var busy = false;
  // pos = index of the page shown on the right (two-up) or the only page (one-up).
  // Two-up: the cover (0) sits alone on the right; then pages 1|2, 3|4, ...
  var pos = 0;

  function readHash() {
    var m = /^#page-(\d+)$/.exec(location.hash);
    return m ? Math.min(Math.max(parseInt(m[1], 10) - 1, 0), N - 1) : 0;
  }
  // Two-up: spread k shows pages 2k-1 | 2k, so pos is always even (0 = the cover alone).
  var LAST2 = 2 * Math.ceil((N - 1) / 2);
  function last() { return two ? LAST2 : N - 1; }
  function snap(i) { return two ? Math.min(i % 2 ? i + 1 : i, LAST2) : Math.min(i, N - 1); }

  function fill(el, i) {
    el.innerHTML = "";
    el.className = el.className.replace(/ ?is-(blank|html|raw)/g, "");
    if (i < 0 || i >= N) { el.className += " is-blank"; return; }
    var p = pages[i];
    if (p.raw) { el.className += " is-raw"; el.innerHTML = p.raw; return; }
    if (p.html) { el.className += " is-html"; el.innerHTML = '<div class="reader-text">' + p.html + "</div>"; return; }
    var img = document.createElement("img");
    img.src = p.src; img.alt = p.alt || ""; img.decoding = "async"; img.draggable = false;
    el.appendChild(img);
  }
  function preload(i) {
    if (i < 0 || i >= N) return;
    (pages[i].imgs || (pages[i].src ? [pages[i].src] : [])).forEach(function (u) { var im = new Image(); im.src = u; });
  }

  function label() {
    if (!two) return "Page " + (pos + 1) + " of " + N;
    var l = pos - 1, r = pos;
    if (pos === 0) return "Cover";
    if (r >= N) return "Page " + (l + 1) + " of " + N;
    return "Pages " + (l + 1) + "–" + (r + 1) + " of " + N;
  }
  function render() {
    if (two) { fill(leftEl, pos - 1); fill(rightEl, pos); }
    else { fill(rightEl, pos); }
    book.classList.toggle("is-closed", two && pos === 0);
    book.classList.toggle("is-end", two && pos >= N);
    count.textContent = label();
    if (words) words.textContent = two ? "" : (pages[pos].text || "");
    slider.value = Math.min(pos, N - 1) + 1;
    prevBtn.disabled = pos <= 0;
    nextBtn.disabled = pos >= last();
    for (var k = 1; k <= 4; k++) { preload(pos + k); preload(pos - k); }
    history.replaceState(null, "", "#page-" + (Math.min(pos, N - 1) + 1));
  }

  // The turning leaf: a two-sided sheet that rotates around the spine.
  function turn(d, to) {
    if (busy || to === pos) return;
    if (reduce) { pos = to; render(); return; }
    busy = true;
    var leaf = document.createElement("div");
    leaf.className = "reader-leaf " + (d > 0 ? "go-next" : "go-prev") + (two ? "" : " single");
    var front = document.createElement("div"), back = document.createElement("div");
    front.className = "reader-page leaf-front"; back.className = "reader-page leaf-back";
    leaf.appendChild(front); leaf.appendChild(back);
    if (two) {
      if (d > 0) { fill(front, pos); fill(back, to - 1); fill(rightEl, to); }
      else { fill(front, pos - 1); fill(back, to); fill(leftEl, to - 1); }
      // Opening from or closing to the cover moves the whole book sideways too.
      book.classList.toggle("is-closed", to === 0);
      book.classList.toggle("is-end", to >= N);
    } else {
      if (d > 0) { fill(front, pos); fill(rightEl, to); }
      else { fill(front, to); }
    }
    book.appendChild(leaf);
    leaf.getBoundingClientRect();
    leaf.classList.add("turning");
    var done = function () {
      leaf.removeEventListener("transitionend", done);
      if (leaf.parentNode) leaf.parentNode.removeChild(leaf);
      pos = to; busy = false; render();
      live.textContent = label();
    };
    leaf.addEventListener("transitionend", done);
    setTimeout(done, 1100);
  }

  function next() { if (pos < last()) turn(1, pos + (two ? 2 : 1)); }
  function prev() { if (pos > 0) turn(-1, pos - (two ? 2 : 1)); }
  function jump(i) { var to = snap(i); if (to !== pos) turn(to > pos ? 1 : -1, to); }

  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);
  slider.max = N;
  slider.addEventListener("input", function () { count.textContent = "Page " + slider.value + " of " + N; });
  slider.addEventListener("change", function () { jump(parseInt(slider.value, 10) - 1); });
  document.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest("input, textarea, select")) return;
    if (e.key === "ArrowRight") { next(); e.preventDefault(); }
    else if (e.key === "ArrowLeft") { prev(); e.preventDefault(); }
  });
  // Click the right side to go forward, the left side to go back.
  stage.addEventListener("click", function (e) {
    if (e.target.closest("a, button")) return;
    var r = book.getBoundingClientRect();
    if (e.clientX > r.left + r.width / 2) next(); else prev();
  });
  // Swipe
  var sx = null, sy = 0;
  stage.addEventListener("touchstart", function (e) { if (e.touches.length === 1) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; } }, { passive: true });
  stage.addEventListener("touchend", function (e) {
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    sx = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.2) { e.preventDefault(); dx < 0 ? next() : prev(); }
  });
  mq.addEventListener("change", function () { two = mq.matches; book.classList.toggle("two-up", two); pos = snap(pos); render(); });
  window.addEventListener("hashchange", function () { var to = snap(readHash()); if (to !== pos) { pos = to; render(); } });

  book.classList.toggle("two-up", two);
  pos = snap(readHash());
  render();
  root.classList.add("is-ready");
})();
