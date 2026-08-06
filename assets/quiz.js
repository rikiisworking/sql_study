/**
 * Minimal quiz widget.
 * Markup:
 * <div class="quiz" data-answer="1" data-ok="..." data-no="...">
 *   <h3>...</h3>
 *   <ul class="choices">
 *     <li><button type="button" class="choice" data-i="0">...</button></li>
 *   </ul>
 *   <p class="feedback" hidden></p>
 * </div>
 * Answer indices are 0-based in data-answer.
 */
(function () {
  function initQuiz(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = "1";
    var answer = parseInt(root.dataset.answer, 10);
    var ok = root.dataset.ok || "Correct.";
    var no = root.dataset.no || "Not quite.";
    var feedback = root.querySelector(".feedback");
    var buttons = root.querySelectorAll("button.choice");

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var i = parseInt(btn.dataset.i, 10);
        buttons.forEach(function (b) {
          b.disabled = true;
          var bi = parseInt(b.dataset.i, 10);
          if (bi === answer) b.classList.add("correct");
          else if (b === btn && bi !== answer) b.classList.add("wrong");
        });
        if (feedback) {
          feedback.hidden = false;
          feedback.classList.add("show");
          if (i === answer) {
            feedback.classList.add("ok");
            feedback.textContent = ok;
          } else {
            feedback.classList.add("no");
            feedback.textContent = no;
          }
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".quiz").forEach(initQuiz);
  });
})();
