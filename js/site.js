(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  document.querySelectorAll(".acc-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", open ? "false" : "true");
      if (panel) panel.hidden = open;
    });
  });

  var reveals = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) {
      el.classList.add("is-in");
    });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    reveals.forEach(function (el) {
      io.observe(el);
    });
  }

  var form = document.getElementById("booking-form");
  if (!form) return;

  var params = new URLSearchParams(location.search);
  var wanted = params.get("artist");
  var select = form.querySelector("[name=artist]");
  if (wanted && select) {
    Array.prototype.forEach.call(select.options, function (option) {
      if (option.value === wanted) select.value = wanted;
    });
  }

  var host = location.hostname;
  var onNetlify = /(^|\.)netlify\.app$/.test(host);
  var note = document.getElementById("pages-note");
  if (onNetlify && note) note.hidden = true;

  var fallback = document.getElementById("form-fallback");
  var copy = document.getElementById("form-copy");
  var mail = document.getElementById("mailto-link");

  form.addEventListener("submit", function (event) {
    if (onNetlify) return;
    event.preventDefault();
    var honeypot = form.querySelector("[name=bot-field]");
    if (honeypot && honeypot.value) {
      if (fallback) {
        fallback.hidden = false;
        fallback.innerHTML = "<p>Thanks. If this was a real note, the shop would write back.</p>";
      }
      return;
    }

    var lines = [];
    var data = new FormData(form);
    data.forEach(function (value, key) {
      if (key === "bot-field" || key === "form-name") return;
      if (value instanceof File) {
        lines.push(key + ": " + (value.name ? value.name + " (file not attached from this preview)" : "(none)"));
        return;
      }
      if (String(value).trim()) lines.push(key + ": " + value);
    });
    var body = lines.join("\n");
    var href =
      "mailto:?subject=" +
      encodeURIComponent("Tattoo consult — Tooth & Nail") +
      "&body=" +
      encodeURIComponent(body);
    if (mail) mail.href = href;
    if (copy) copy.textContent = body;
    if (fallback) {
      fallback.hidden = false;
      fallback.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    }
  });
})();
