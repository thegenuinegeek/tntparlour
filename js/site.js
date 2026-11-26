(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 1. Floating Header Glass-on-Scroll + Hero Logo Scroll-Past Reveal
  var header = document.querySelector(".site-header");
  var heroLogo = document.getElementById("hero-logo");
  if (header) {
    function syncScroll() {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
      if (heroLogo) {
        var rect = heroLogo.getBoundingClientRect();
        header.classList.toggle("show-brand", rect.bottom <= 12);
      }
    }
    syncScroll();
    window.addEventListener("scroll", syncScroll, { passive: true });
    window.addEventListener("resize", syncScroll, { passive: true });
  }

  // 2. Mobile Navigation Drawer
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    function setNav(open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    toggle.addEventListener("click", function () {
      setNav(!nav.classList.contains("is-open"));
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setNav(false);
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setNav(false);
        toggle.focus();
      }
    });
    document.addEventListener("click", function (e) {
      if (nav.classList.contains("is-open") && !nav.contains(e.target) && !toggle.contains(e.target)) {
        setNav(false);
      }
    });
  }

  // 3. Live Macon (America/New_York) Shop Open/Closed Status
  function getMaconTime() {
    try {
      var parts = new Intl.DateTimeFormat("en-US", {
        timeZone: "America/New_York",
        weekday: "short",
        hour: "numeric",
        minute: "numeric",
        hour12: false
      }).formatToParts(new Date());
      var map = {};
      parts.forEach(function (p) {
        map[p.type] = p.value;
      });
      var hr = parseInt(map.hour, 10);
      if (hr === 24) hr = 0;
      return {
        weekday: map.weekday,
        minutes: hr * 60 + parseInt(map.minute, 10)
      };
    } catch (_) {
      return null;
    }
  }

  function computeShopStatus() {
    var now = getMaconTime();
    if (!now) return null;
    var day = now.weekday;
    var m = now.minutes;
    var openMin = 13 * 60; // 1:00 PM
    var closeMin = null;
    var rowKey = "sun-mon";

    if (day === "Tue" || day === "Wed" || day === "Thu") {
      closeMin = 20 * 60; // 8:00 PM
      rowKey = "tue-thu";
    } else if (day === "Fri" || day === "Sat") {
      closeMin = 22 * 60; // 10:00 PM
      rowKey = "fri-sat";
    }

    if (closeMin !== null && m >= openMin && m < closeMin) {
      var closeLabel = closeMin === 20 * 60 ? "8 PM" : "10 PM";
      return { isOpen: true, mark: "\u2726", text: "Open Now \u2014 Till " + closeLabel, rowKey: rowKey };
    }
    if (closeMin !== null && m < openMin) {
      return { isOpen: false, mark: "\u25c7", text: "Doors Open Today \u00b7 1 PM", rowKey: rowKey };
    }
    if (day === "Tue" || day === "Wed" || day === "Thu" || day === "Fri") {
      return { isOpen: false, mark: "\u25c7", text: "Opens Tomorrow \u00b7 1 PM", rowKey: rowKey };
    }
    return { isOpen: false, mark: "\u25c7", text: "Closed \u00b7 Opens Tue 1 PM", rowKey: rowKey };
  }

  var status = computeShopStatus();
  if (status) {
    document.querySelectorAll("[data-shop-status]").forEach(function (el) {
      el.classList.remove("is-open", "is-closed");
      el.classList.add(status.isOpen ? "is-open" : "is-closed");
      var markEl = el.querySelector(".status-mark");
      if (markEl) markEl.textContent = status.mark;
      var textEl = el.querySelector(".status-text");
      if (textEl) textEl.textContent = status.text;
    });
    document.querySelectorAll("[data-hours-row]").forEach(function (row) {
      if (row.getAttribute("data-hours-row") === status.rowKey) {
        row.classList.add("is-today");
      }
    });
  }

  // 4. Portfolio Gallery Category Filter
  var filterBtns = document.querySelectorAll(".filter-btn");
  var galleryItems = document.querySelectorAll("[data-category]");
  if (filterBtns.length && galleryItems.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var cat = btn.getAttribute("data-filter");
        filterBtns.forEach(function (b) {
          var active = b === btn;
          b.classList.toggle("is-active", active);
          b.setAttribute("aria-pressed", active ? "true" : "false");
        });
        galleryItems.forEach(function (item) {
          var match = cat === "all" || item.getAttribute("data-category") === cat;
          item.hidden = !match;
        });
      });
    });
  }

  // 5. Accessible Portfolio Lightbox
  var lightbox = document.getElementById("lightbox");
  var triggers = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox-src]"));
  if (lightbox && triggers.length) {
    var lbImg = lightbox.querySelector("#lb-img");
    var lbTitle = lightbox.querySelector("#lb-title");
    var lbSub = lightbox.querySelector("#lb-sub");
    var lbClose = lightbox.querySelector("#lb-close");
    var lbPrev = lightbox.querySelector("#lb-prev");
    var lbNext = lightbox.querySelector("#lb-next");
    var activeTriggers = triggers;
    var currentIndex = 0;
    var lastFocused = null;

    function refreshVisibleTriggers() {
      var visible = triggers.filter(function (t) {
        var card = t.closest("[data-category]");
        return !card || !card.hidden;
      });
      activeTriggers = visible.length ? visible : triggers;
    }

    function showSlide(index) {
      if (!activeTriggers.length) return;
      currentIndex = (index + activeTriggers.length) % activeTriggers.length;
      var t = activeTriggers[currentIndex];
      lbImg.src = t.getAttribute("data-lightbox-src");
      lbImg.alt = t.getAttribute("data-lightbox-alt") || "";
      lbTitle.textContent = t.getAttribute("data-lightbox-title") || "";
      lbSub.textContent = t.getAttribute("data-lightbox-sub") || "";
    }

    function openLightbox(trigger) {
      refreshVisibleTriggers();
      var idx = activeTriggers.indexOf(trigger);
      currentIndex = idx >= 0 ? idx : 0;
      lastFocused = document.activeElement;
      showSlide(currentIndex);
      lightbox.hidden = false;
      document.body.style.overflow = "hidden";
      if (lbClose) lbClose.focus();
    }

    function closeLightbox() {
      lightbox.hidden = true;
      document.body.style.overflow = "";
      lbImg.src = "";
      if (lastFocused && typeof lastFocused.focus === "function") {
        lastFocused.focus();
      }
    }

    triggers.forEach(function (t) {
      t.addEventListener("click", function () {
        openLightbox(t);
      });
    });

    if (lbClose) lbClose.addEventListener("click", closeLightbox);
    if (lbPrev) {
      lbPrev.addEventListener("click", function () {
        showSlide(currentIndex - 1);
      });
    }
    if (lbNext) {
      lbNext.addEventListener("click", function () {
        showSlide(currentIndex + 1);
      });
    }
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener("keydown", function (e) {
      if (lightbox.hidden) return;
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowLeft") showSlide(currentIndex - 1);
      if (e.key === "ArrowRight") showSlide(currentIndex + 1);
    });
  }

  // 6. Consult Request Form UX
  var form = document.getElementById("booking-form");
  if (form) {
    var params = new URLSearchParams(location.search);
    var wanted = params.get("artist");
    var select = form.querySelector("[name=artist]");
    if (wanted && select) {
      Array.prototype.forEach.call(select.options, function (option) {
        if (option.value === wanted) select.value = wanted;
      });
    }

    var onNetlify = /(^|\.)netlify\.app$/.test(location.hostname);
    var fallback = document.getElementById("form-fallback");
    var copyPre = document.getElementById("form-copy");
    var mailLink = document.getElementById("mailto-link");
    var copyBtn = document.getElementById("copy-request-btn");

    form.addEventListener("submit", function (event) {
      if (onNetlify) return;
      event.preventDefault();

      var honeypot = form.querySelector("[name=bot-field]");
      if (honeypot && honeypot.value) return;

      var lines = [];
      var days = [];
      var data = new FormData(form);
      data.forEach(function (value, key) {
        if (key === "bot-field" || key === "form-name") return;
        if (key === "preferred-days") {
          days.push(String(value));
          return;
        }
        if (value instanceof File) {
          if (value.name) {
            lines.push("Reference Image: " + value.name + " (attach directly when emailing or bring to the shop)");
          }
          return;
        }
        var clean = String(value).trim();
        if (clean) {
          var label = key.charAt(0).toUpperCase() + key.slice(1).replace(/-/g, " ");
          lines.push(label + ": " + clean);
        }
      });
      if (days.length) lines.push("Preferred Days: " + days.join(", "));

      var summary = lines.join("\n");
      if (copyPre) copyPre.textContent = summary;
      if (mailLink) {
        mailLink.href =
          "mailto:?subject=" +
          encodeURIComponent("Consultation Request — Tooth & Nail Tattoo Parlour") +
          "&body=" +
          encodeURIComponent(summary);
      }
      if (fallback) {
        fallback.hidden = false;
        fallback.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "nearest" });
      }
    });

    if (copyBtn && copyPre) {
      copyBtn.addEventListener("click", function () {
        if (!navigator.clipboard) return;
        navigator.clipboard.writeText(copyPre.textContent).then(function () {
          copyBtn.textContent = "Copied to Clipboard";
          setTimeout(function () {
            copyBtn.textContent = "Copy Request Summary";
          }, 2200);
        });
      });
    }
  }
})();
