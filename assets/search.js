// Client-side search + tag filter for the recipe index. No dependencies.
(function () {
  var searchInput = document.getElementById("search");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
  var tagButtons = Array.prototype.slice.call(
    document.querySelectorAll(".tag-filter")
  );
  var noResults = document.getElementById("no-results");
  var activeTag = "";

  function applyFilter() {
    var q = searchInput.value.trim().toLowerCase();
    var visible = 0;
    cards.forEach(function (card) {
      var hay = card.getAttribute("data-search") || "";
      var tagMatch =
        !activeTag || hay.indexOf(activeTag.toLowerCase()) !== -1;
      // Tags are included in data-search, but match the tag exactly-ish:
      // require the tag token to appear; good enough for a small site.
      var textMatch = !q || hay.indexOf(q) !== -1;
      var show = tagMatch && textMatch;
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });
    noResults.hidden = visible !== 0;
  }

  searchInput.addEventListener("input", applyFilter);
  tagButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      tagButtons.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      activeTag = btn.getAttribute("data-tag") || "";
      applyFilter();
    });
  });
})();
