/* Ashfaq Tailor — site behaviour (no libraries). Reads settings from site-config.js */
(function () {
  "use strict";
  var S = window.SITE || {};
  var PLACEHOLDER_DOMAIN = "https://YOUR-DOMAIN.com";
  var addr = S.address || {};
  var fullAddress = [addr.street, addr.city, addr.countryName].filter(Boolean).join(", ");

  /* ---------- helpers ---------- */
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : String(t); return d.innerHTML; }
  function waLink(msg) {
    var m = msg || S.defaultMessage || "";
    return "https://wa.me/" + (S.whatsappNumber || "") + "?text=" + encodeURIComponent(m);
  }
  function telLink() { return "tel:" + (S.phoneNumber || ""); }
  function directionsUrl() {
    if (S.mapUrl) return S.mapUrl;
    return "https://www.google.com/maps/dir/?api=1&destination=" + encodeURIComponent(S.businessName + ", " + fullAddress);
  }

  /* ---------- analytics (GA4 + clear event names) ---------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  if (/^G-[A-Z0-9]{6,}$/.test(S.ga4Id || "")) {
    var gs = document.createElement("script");
    gs.async = true;
    gs.src = "https://www.googletagmanager.com/gtag/js?id=" + S.ga4Id;
    document.head.appendChild(gs);
    gtag("js", new Date());
    gtag("config", S.ga4Id);
  }
  function track(name, params) {
    try { gtag("event", name, params || {}); } catch (e) { /* analytics must never break the page */ }
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-wa],[data-call],[data-directions],[data-track]");
    if (!el) return;
    var sec = el.closest("[data-loc]");
    var p = { link_location: sec ? sec.getAttribute("data-loc") : "page", page_path: location.pathname };
    if (el.hasAttribute("data-wa")) track("whatsapp_click", p);
    else if (el.hasAttribute("data-call")) track("phone_click", p);
    else if (el.hasAttribute("data-directions")) track("directions_click", p);
    else track(el.getAttribute("data-track") || "cta_click", p);
  });

  /* ---------- fill contact links & text ---------- */
  $$("[data-wa]").forEach(function (a) {
    a.href = waLink(a.getAttribute("data-msg") || ""); a.target = "_blank"; a.rel = "noopener";
  });
  $$("[data-call]").forEach(function (a) { a.href = telLink(); });
  $$("[data-directions]").forEach(function (a) { a.href = directionsUrl(); a.target = "_blank"; a.rel = "noopener"; });
  var fields = {
    phone: S.phoneDisplay, whatsapp: S.whatsappDisplay, owner: S.ownerName, name: S.businessName,
    address: fullAddress, year: String(new Date().getFullYear())
  };
  $$("[data-f]").forEach(function (el) { var v = fields[el.getAttribute("data-f")]; if (v) el.textContent = v; });

  /* social links: hidden until a real link is supplied */
  $$("[data-social]").forEach(function (a) {
    var url = (S.social || {})[a.getAttribute("data-social")];
    var holder = a.closest("li") || a;
    if (url) { a.href = url; a.target = "_blank"; a.rel = "noopener me"; } else { holder.hidden = true; }
  });
  var anySocial = S.social && (S.social.facebook || S.social.instagram || S.social.tiktok);
  $$("[data-social-wrap]").forEach(function (w) { w.hidden = !anySocial; });

  /* google review link (falls back to WhatsApp feedback) */
  $$("[data-review-link]").forEach(function (a) {
    if (S.googleReviewUrl) { a.href = S.googleReviewUrl; a.target = "_blank"; a.rel = "noopener"; }
    else { a.href = waLink("Assalam-o-Alaikum Ashfaq Tailor, I would like to share my feedback about your stitching."); a.target = "_blank"; a.rel = "noopener"; a.textContent = "Share Your Feedback on WhatsApp"; }
  });

  /* ---------- hours ---------- */
  $$("[data-hours]").forEach(function (el) {
    var h = (S.hours || []).filter(function (x) { return x && x.label; });
    if (!h.length) {
      el.innerHTML = '<span class="hours-fallback">Message us on WhatsApp to confirm today’s timings.</span>';
      return;
    }
    el.innerHTML = h.map(function (x) {
      return "<div>" + esc(x.label) + ": <strong>" + esc(x.closed ? "Closed" : (x.display || (x.opens + " – " + x.closes))) + "</strong></div>";
    }).join("");
  });

  /* ---------- announcement banner ---------- */
  if (S.banner && S.banner.enabled && S.banner.text) {
    var b = document.createElement("div");
    b.className = "banner"; b.setAttribute("role", "region"); b.setAttribute("aria-label", "Announcement");
    b.innerHTML = esc(S.banner.text) + ' <a data-wa data-track="banner_click" href="#">' + esc(S.banner.linkText || "WhatsApp us") + "</a>";
    document.body.insertBefore(b, document.body.firstChild);
    var ba = $("a", b); ba.href = waLink("Assalam-o-Alaikum Ashfaq Tailor, " + S.banner.text); ba.target = "_blank"; ba.rel = "noopener";
  }

  /* ---------- map embed (loaded only when scrolled near) ---------- */
  var mapBox = $("[data-map]");
  if (mapBox) {
    var ov = document.createElement("a");
    ov.className = "map-open"; ov.target = "_blank"; ov.rel = "noopener";
    ov.href = S.mapUrl || ("https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(S.businessName + ", " + fullAddress));
    ov.setAttribute("aria-label", "Open " + S.businessName + " location in Google Maps");
    ov.innerHTML = "<span>Open shop location in Google Maps</span>";
    mapBox.appendChild(ov);
    var loadMap = function () {
      if (mapBox.querySelector("iframe")) return;
      var f = document.createElement("iframe");
      f.title = "Map showing the location of " + S.businessName;
      f.loading = "lazy"; f.referrerPolicy = "no-referrer-when-downgrade"; f.allowFullscreen = true;
      f.src = S.mapEmbedUrl || ("https://maps.google.com/maps?q=" + encodeURIComponent(fullAddress) + "&output=embed");
      mapBox.insertBefore(f, ov);
    };
    if ("IntersectionObserver" in window) {
      var mo = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { loadMap(); mo.disconnect(); } }, { rootMargin: "300px" });
      mo.observe(mapBox);
    } else loadMap();
    $$("[data-map-note]").forEach(function (n) { n.hidden = !!S.mapUrl || !!S.mapEmbedUrl; });
  }

  /* ---------- reviews & before/after ---------- */
  var rv = $("[data-reviews]");
  if (rv && S.reviews && S.reviews.length) {
    rv.className = "reviews";
    rv.innerHTML = S.reviews.map(function (r) {
      return '<blockquote class="review"><p>“' + esc(r.text) + '”</p><footer>— ' + esc(r.name) + "</footer></blockquote>";
    }).join("");
  }
  var baSec = $("[data-before-after]");
  if (baSec && S.beforeAfter && S.beforeAfter.length) {
    baSec.hidden = false;
    $("[data-ba-list]", baSec).innerHTML = S.beforeAfter.map(function (x) {
      return '<div class="ba"><figure><img loading="lazy" src="' + esc(x.before) + '" alt="Before: ' + esc(x.caption) + '"><figcaption>Before</figcaption></figure>' +
        '<figure><img loading="lazy" src="' + esc(x.after) + '" alt="After: ' + esc(x.caption) + '"><figcaption>After — ' + esc(x.caption) + "</figcaption></figure></div>";
    }).join("");
  }

  /* ---------- schema.org (merges the verified details from settings) ---------- */
  var ld = $("#ld-business");
  if (ld) {
    try {
      var data = JSON.parse(ld.textContent);
      if (S.phoneNumber) data.telephone = S.phoneNumber;
      var specs = (S.hours || []).filter(function (x) { return x && x.opens && x.closes && x.days && !x.closed; }).map(function (x) {
        return { "@type": "OpeningHoursSpecification", dayOfWeek: x.days, opens: x.opens, closes: x.closes };
      });
      if (specs.length) data.openingHoursSpecification = specs;
      var same = [S.social && S.social.facebook, S.social && S.social.instagram, S.social && S.social.tiktok].filter(Boolean);
      if (same.length) data.sameAs = same;
      if (S.mapUrl) data.hasMap = S.mapUrl;
      var txt = JSON.stringify(data);
      if (S.siteUrl) txt = txt.split(PLACEHOLDER_DOMAIN).join(S.siteUrl.replace(/\/$/, ""));
      ld.textContent = txt;
    } catch (e) { /* leave static schema as is */ }
  }

  /* ---------- mobile menu ---------- */
  var tg = $(".nav-toggle"), mn = $("#mobile-nav");
  if (tg && mn) {
    tg.addEventListener("click", function () {
      var o = tg.getAttribute("aria-expanded") === "true";
      tg.setAttribute("aria-expanded", String(!o)); mn.classList.toggle("open", !o);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && mn.classList.contains("open")) { mn.classList.remove("open"); tg.setAttribute("aria-expanded", "false"); tg.focus(); }
    });
    $$("a", mn).forEach(function (a) { a.addEventListener("click", function () { mn.classList.remove("open"); tg.setAttribute("aria-expanded", "false"); }); });
  }

  /* ---------- work filters ---------- */
  var chips = $$(".chip[data-filter]");
  if (chips.length) {
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (x) { x.setAttribute("aria-pressed", String(x === c)); });
        var f = c.getAttribute("data-filter");
        $$(".work-item").forEach(function (it) { it.hidden = !(f === "all" || it.getAttribute("data-cat") === f); });
      });
    });
  }

  /* ---------- lightbox ---------- */
  var lbBtns = $$("[data-lb]");
  if (lbBtns.length && typeof HTMLDialogElement !== "undefined") {
    var dlg = document.createElement("dialog");
    dlg.className = "lb"; dlg.setAttribute("aria-label", "Photo viewer");
    dlg.innerHTML = '<div class="lb-inner"><img alt=""><div class="lb-bar"><span class="lb-title"></span><a class="btn btn--wa btn--sm lb-wa" target="_blank" rel="noopener" data-track="lightbox_whatsapp_click">Like This Style? Discuss It on WhatsApp</a></div></div>' +
      '<button class="lb-btn lb-close" aria-label="Close">×</button><button class="lb-btn lb-prev" aria-label="Previous photo">‹</button><button class="lb-btn lb-next" aria-label="Next photo">›</button>';
    document.body.appendChild(dlg);
    var lbImg = $("img", dlg), lbTitle = $(".lb-title", dlg), lbWa = $(".lb-wa", dlg);
    var list = [], idx = 0, opener = null;
    function show(i) {
      idx = (i + list.length) % list.length;
      var b = list[idx];
      lbImg.src = b.getAttribute("data-full"); lbImg.alt = b.getAttribute("data-alt") || "";
      var t = b.getAttribute("data-title") || "";
      lbTitle.textContent = t;
      var wantWa = b.hasAttribute("data-lb-wa");
      lbWa.hidden = !wantWa;
      if (wantWa) lbWa.href = waLink("Assalam-o-Alaikum Ashfaq Tailor, I like this style: " + t + ". I would like to discuss it.");
      $(".lb-prev", dlg).hidden = $(".lb-next", dlg).hidden = list.length < 2;
    }
    lbBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        opener = b;
        var grp = b.closest("[data-lb-group]") || document;
        list = $$("[data-lb]", grp).filter(function (x) { return !x.closest("[hidden]"); });
        dlg.showModal(); show(list.indexOf(b));
      });
    });
    $(".lb-close", dlg).addEventListener("click", function () { dlg.close(); });
    $(".lb-prev", dlg).addEventListener("click", function () { show(idx - 1); });
    $(".lb-next", dlg).addEventListener("click", function () { show(idx + 1); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.classList.contains("lb-inner")) dlg.close(); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") show(idx - 1); else if (e.key === "ArrowRight") show(idx + 1);
    });
    dlg.addEventListener("close", function () { if (opener) opener.focus(); });
  }

  /* ---------- choose your style ---------- */
  var chooser = $("#style-chooser");
  if (chooser) {
    var opts = S.styleOptions || {};
    function build(boxSel, name, arr) {
      var box = $(boxSel, chooser); if (!box) return;
      box.innerHTML = (arr || []).map(function (v, i) {
        return '<label class="opt"><input type="radio" name="' + name + '" value="' + esc(v) + '"><span>' + esc(v) + "</span></label>";
      }).join("");
    }
    build("[data-garments]", "garment", opts.garments); build("[data-fits]", "fit", opts.fits);
    var prev = $(".preview", chooser), go = $("#style-go", chooser), hint = $("#style-hint", chooser);
    function sel(n) { var c = $('input[name="' + n + '"]:checked', chooser); return c ? c.value : ""; }
    function update() {
      var g = sel("garment"), f = sel("fit");
      if (!g) { prev.textContent = "Pick a garment to begin."; go.setAttribute("aria-disabled", "true"); go.style.opacity = ".55"; go.href = "#style-chooser"; return; }
      prev.textContent = g + (f ? " — " + f : "");
      var msg = "Assalam-o-Alaikum Ashfaq Tailor. I am interested in a " + g + (f ? " with " + f : "") + ". I would like to discuss stitching details.";
      go.href = waLink(msg); go.removeAttribute("aria-disabled"); go.style.opacity = "1"; hint.textContent = "";
    }
    chooser.addEventListener("change", update);
    go.addEventListener("click", function (e) {
      if (go.getAttribute("aria-disabled") === "true") { e.preventDefault(); hint.textContent = "Please choose a garment first."; var r = $('input[name="garment"]', chooser); if (r) r.focus(); }
      else track("style_chooser_whatsapp", { garment: sel("garment"), fit: sel("fit") });
    });
    go.target = "_blank"; go.rel = "noopener"; update();
  }

  /* ---------- inquiry form -> WhatsApp ---------- */
  var form = $("#inquiry-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      function check(id, cond) { var f = $("#" + id).closest(".field"); f.classList.toggle("bad", !cond); if (!cond && ok) { $("#" + id).focus(); } ok = ok && cond; }
      var name = $("#f-name").value.trim(), svc = $("#f-service").value;
      check("f-name", name.length > 1); check("f-service", !!svc);
      if (!ok) return;
      var phone = $("#f-phone").value.trim(), date = $("#f-date").value, msg = $("#f-message").value.trim();
      var lines = ["Assalam-o-Alaikum Ashfaq Tailor,", "I would like to make an inquiry from your website.", "", "*Name:* " + name];
      if (phone) lines.push("*Phone:* " + phone);
      lines.push("*Service:* " + svc);
      if (date) lines.push("*Preferred date:* " + date);
      if (msg) lines.push("*Message:* " + msg);
      track("inquiry_submit", { service: svc, page_path: location.pathname });
      var url = waLink(lines.join("\n"));
      var done = $("#form-done"); if (done) { done.hidden = false; }
      var w = window.open(url, "_blank");
      if (w) { try { w.opener = null; } catch (err) { /* ignore */ } } else { location.href = url; }
    });
    $$(".field input,.field select", form).forEach(function (i) { i.addEventListener("input", function () { i.closest(".field").classList.remove("bad"); }); });
    var di = $("#f-date"); if (di) di.min = new Date().toISOString().slice(0, 10);
  }

  /* ---------- subtle reveal-on-scroll ---------- */
  var rev = $$(".reveal");
  if (rev.length && "IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } });
    }, { threshold: .12, rootMargin: "0px 0px -40px 0px" });
    rev.forEach(function (r) { io.observe(r); });
  } else rev.forEach(function (r) { r.classList.add("in"); });
})();
