/*!
 * Helipad Detector — Globe → Zoom → Map intro
 * -------------------------------------------------------------------------
 * Self-contained overlay (three.js r128 loaded on demand from cdnjs). Covers
 * the Leaflet map it is embedded in, spins a dotted globe to the target
 * (São Paulo), dives in, then fades the overlay away to reveal the REAL
 * Folium map underneath. The globe and Leaflet are different renderers, so
 * there is no pixel-continuous transition: the overlay is a timed cover that
 * is replaced by the map (cross-fade).
 *
 * Safe by design: if WebGL / three.js is unavailable, the user prefers
 * reduced motion, or the intro was already seen in this browser session for
 * this map id, the overlay is removed (or never shown) and the map is simply
 * there. Land dots: Natural Earth 110m (public domain), sampled on an
 * equal-area lat/lon grid, ~178 km spacing — see build_globe_intro.py.
 */
(function (global) {
  'use strict';
  if (global.HDGlobeIntro) return;

  var THREE_URL = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
  // rows separated by ';' -> "lat10:lon0,d1,d2,..." (base36). lon0 = lon10 + 1800.
  var LAND_ENC = '__LAND__';

  function decodeLand() {
    var out = [];
    LAND_ENC.split(';').forEach(function (row) {
      var p = row.split(':'), lat = parseInt(p[0], 10) / 10, lon10 = 0;
      p[1].split(',').forEach(function (d, i) {
        var v = parseInt(d, 36);
        lon10 = (i === 0) ? v - 1800 : lon10 + v;
        out.push(lat, lon10 / 10);
      });
    });
    return out;
  }

  function clamp01(x) { return x < 0 ? 0 : (x > 1 ? 1 : x); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function easeInOutCubic(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function easeInOutQuart(t) { return t < 0.5 ? 8 * t * t * t * t : 1 - Math.pow(-2 * t + 2, 4) / 2; }
  function smooth(a, b, x) { var t = clamp01((x - a) / (b - a)); return t * t * (3 - 2 * t); }
  function el(tag, css, html) {
    var e = document.createElement(tag);
    if (css) e.style.cssText = css;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function fmtCoord(lat, lon) {
    return Math.abs(lat).toFixed(2) + '°' + (lat < 0 ? 'S' : 'N') + ' · ' +
           Math.abs(lon).toFixed(2) + '°' + (lon < 0 ? 'W' : 'E');
  }

  function loadThree(ok, fail, timeoutMs) {
    if (global.THREE) { ok(); return; }
    var done = false, s = document.createElement('script');
    var timer = setTimeout(function () { if (!done) { done = true; fail('timeout'); } }, timeoutMs);
    s.onload = function () {
      if (done) return; done = true; clearTimeout(timer);
      if (global.THREE) ok(); else fail('THREE missing');
    };
    s.onerror = function () { if (done) return; done = true; clearTimeout(timer); fail('load error'); };
    s.src = THREE_URL;
    (document.head || document.documentElement).appendChild(s);
  }

  // Debug HUD (cfg.debug, URL ?globe=debug): writes each decision/step into a small on-screen box,
  // so a "the intro does not show" report carries the reason in a screenshot.
  function makeDbg(on, id) {
    if (!on) return function () {};
    var box = document.getElementById('hd-globe-dbg');
    if (!box) {
      box = el('div', 'position:fixed;left:6px;top:6px;z-index:2147483647;max-width:92%;background:rgba(0,0,0,.82);' +
        'color:#7CFC9A;font:11px/1.35 ui-monospace,Menlo,monospace;padding:5px 8px;border-radius:6px;pointer-events:none;white-space:pre-wrap');
      box.id = 'hd-globe-dbg';
      (document.body || document.documentElement).appendChild(box);
    }
    return function (m) { box.textContent += '\n[' + id + '] ' + m; };
  }

  global.HDGlobeIntro = function (cfg) {
    cfg = cfg || {};
    var id = cfg.id || 'map';
    var storeKey = 'hd_globe_seen:' + id;
    var dbg = makeDbg(!!cfg.debug, id);
    dbg('engine started (force=' + !!cfg.force + ')');
    var target = cfg.target || [-23.5505, -46.6333];
    var duration = cfg.durationMs || 5200;
    var tealCss = cfg.pointColor || '#14b8a6';
    var markerCss = cfg.markerColor || '#ff2500';

    global.__hdGlobeRunning = global.__hdGlobeRunning || {};
    global.__hdGlobeDone = global.__hdGlobeDone || {};
    if (global.__hdGlobeRunning[id] || global.__hdGlobeDone[id]) { dbg('skip: already ran in this frame'); return; }   // re-render in same frame
    // cfg.force (URL ?globe=force) ignores the once-per-session flag and prefers-reduced-motion — handy to debug why the intro does not show.
    try { if (!cfg.force && cfg.debugT == null && global.sessionStorage.getItem(storeKey) === '1') { dbg('skip: already seen in this browser tab session (open a NEW tab / private window, or add ?globe=force)'); return; } } catch (e) { dbg('sessionStorage unavailable: ' + e); }
    // prefers-reduced-motion: instead of skipping, play a calm variant — a STILL globe already facing
    // the target (no spin, no zoom, no flash) that just fades into the map (~1.6 s). cfg.force plays the full animation.
    var reduced = false;
    try { reduced = !cfg.force && !!(global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch (e) {}
    if (reduced) { duration = Math.min(duration, 1600); dbg('prefers-reduced-motion is ON -> calm still version'); }
    global.__hdGlobeRunning[id] = true;

    // ---------- overlay (opaque from the very first frame: no map flash) ----------
    var overlay = el('div',
      'position:fixed;inset:0;z-index:2147483000;background:#050506;overflow:hidden;' +
      'font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;');
    overlay.setAttribute('data-hd-globe', id);
    var glow = el('div', 'position:absolute;inset:0;pointer-events:none;' +
      'background:radial-gradient(ellipse 70% 60% at 50% 45%,rgba(14,117,109,.16) 0%,transparent 65%);');
    var canvasBox = el('div', 'position:absolute;inset:0;');
    var hud = el('div', 'position:absolute;left:0;right:0;top:clamp(14px,5%,34px);text-align:center;pointer-events:none;');
    hud.innerHTML =
      '<div style="font-size:clamp(.5rem,1.6vw,.66rem);letter-spacing:.24em;color:' + tealCss + ';margin-bottom:6px">' +
      'HELIPAD DETECTOR</div>' +
      '<div style="font-size:clamp(1rem,3.4vw,1.7rem);font-weight:700;color:#fff;letter-spacing:-.01em">' +
      (cfg.label || 'São Paulo') + '</div>' +
      '<div data-sub style="margin-top:4px;font:500 clamp(.5rem,1.5vw,.64rem) ui-monospace,Menlo,monospace;' +
      'letter-spacing:.12em;color:rgba(255,255,255,.55)">' + (cfg.sub || fmtCoord(target[0], target[1])) + '</div>' +
      (cfg.caption ? '<div style="margin-top:6px;font-size:clamp(.5rem,1.5vw,.64rem);letter-spacing:.16em;' +
      'text-transform:uppercase;color:' + tealCss + ';opacity:.85">' + cfg.caption + '</div>' : '');
    var enter = el('div',
      'position:absolute;left:0;right:0;bottom:clamp(34px,9%,56px);text-align:center;pointer-events:none;opacity:0;' +
      'font:600 clamp(.52rem,1.6vw,.68rem) ui-monospace,Menlo,monospace;letter-spacing:.2em;color:' + tealCss + ';',
      (cfg.entering || 'Entering the map…').toUpperCase());
    var bar = el('div', 'position:absolute;left:0;bottom:0;height:3px;width:0;background:linear-gradient(90deg,' +
      tealCss + ',' + markerCss + ');pointer-events:none;');
    var reticle = el('div', 'position:absolute;left:50%;top:50%;width:0;height:0;pointer-events:none;opacity:0;');
    reticle.innerHTML =
      '<div style="position:absolute;left:-34px;top:-34px;width:68px;height:68px;border:1px solid ' + markerCss +
      ';border-radius:50%;box-shadow:0 0 18px ' + markerCss + '55"></div>' +
      '<div style="position:absolute;left:-1px;top:-58px;width:2px;height:20px;background:' + markerCss + '"></div>' +
      '<div style="position:absolute;left:-1px;top:38px;width:2px;height:20px;background:' + markerCss + '"></div>' +
      '<div style="position:absolute;top:-1px;left:-58px;height:2px;width:20px;background:' + markerCss + '"></div>' +
      '<div style="position:absolute;top:-1px;left:38px;height:2px;width:20px;background:' + markerCss + '"></div>';
    var flash = el('div', 'position:absolute;inset:0;pointer-events:none;opacity:0;' +
      'background:radial-gradient(circle at 50% 50%,rgba(20,184,166,.85) 0%,rgba(14,117,109,.35) 28%,transparent 62%);');
    var skip = el('button',
      'position:absolute;right:clamp(10px,3%,22px);top:clamp(10px,3%,22px);z-index:5;cursor:pointer;' +
      'background:rgba(13,15,16,.72);color:rgba(255,255,255,.85);border:1px solid rgba(20,184,166,.45);' +
      'border-radius:999px;padding:6px 14px;font:600 .66rem ui-monospace,Menlo,monospace;letter-spacing:.1em;',
      cfg.skip || 'Skip ▸');
    skip.type = 'button';
    [glow, canvasBox, hud, reticle, flash, enter, bar, skip].forEach(function (n) { overlay.appendChild(n); });
    (document.body || document.documentElement).appendChild(overlay);

    var finished = false, raf = 0, renderer = null, scene = null, disposeList = [];

    function cleanup() {
      try { cancelAnimationFrame(raf); } catch (e) {}
      try {
        disposeList.forEach(function (o) { if (o && o.dispose) o.dispose(); });
        if (renderer) { renderer.dispose(); if (renderer.forceContextLoss) renderer.forceContextLoss(); }
      } catch (e) {}
      try { overlay.parentNode && overlay.parentNode.removeChild(overlay); } catch (e) {}
      global.__hdGlobeRunning[id] = false;
      try { document.removeEventListener('keydown', onKey); } catch (e) {}
    }
    function finish(quick, markSeen) {
      if (finished) return; finished = true;
      if (markSeen) { global.__hdGlobeDone[id] = true; try { global.sessionStorage.setItem(storeKey, '1'); } catch (e) {} }
      if (quick) {
        overlay.style.transition = 'opacity 240ms ease';
        overlay.style.opacity = '0';
        setTimeout(cleanup, 280);
      } else { cleanup(); }
    }
    function onKey(e) { if (e.key === 'Escape') finish(true, true); }
    document.addEventListener('keydown', onKey);
    skip.addEventListener('click', function () { finish(true, true); });

    // ---------- wait for three.js, then for the frame to be actually visible ----------
    dbg('loading three.js from ' + THREE_URL);
    loadThree(function () {
      dbg('three.js loaded');
      try { begin(global.THREE); } catch (err) { dbg('ERROR in begin(): ' + err); try { console.error('HDGlobeIntro:', err); } catch (e) {} finish(true, false); }
    }, function (why) {
      dbg('three.js FAILED: ' + why + ' (blocked by browser/extension/network?)');
      try { console.warn('HDGlobeIntro skipped:', why); } catch (e) {}
      finish(true, false);
    }, cfg.loadTimeoutMs || 5000);

    function begin(THREE) {
      var R = 2.6, D2R = Math.PI / 180;
      var W = Math.max(overlay.clientWidth, 2), H = Math.max(overlay.clientHeight, 2);

      dbg('creating WebGL renderer');
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(global.devicePixelRatio || 1, 2));
      renderer.setSize(W, H);
      canvasBox.appendChild(renderer.domElement);
      renderer.domElement.style.cssText = 'display:block;width:100%;height:100%;';

      scene = new THREE.Scene();
      var camera = new THREE.PerspectiveCamera(45, W / H, 0.02, 220);

      function ll(lat, lon, r) {
        var phi = (90 - lat) * D2R, th = (lon + 180) * D2R;
        return new THREE.Vector3(-r * Math.sin(phi) * Math.cos(th), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(th));
      }
      function dot(color, sharp) {
        var c = document.createElement('canvas'); c.width = c.height = 64;
        var g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
        gr.addColorStop(0, color); gr.addColorStop(sharp ? 0.55 : 1, sharp ? color : 'rgba(0,0,0,0)');
        if (sharp) gr.addColorStop(0.6, 'rgba(0,0,0,0)');
        g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
        var tx = new THREE.CanvasTexture(c); disposeList.push(tx); return tx;
      }
      function tint(hex, a) {
        var h = hex.replace('#', ''); if (h.length === 3) h = h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
        return 'rgba(' + parseInt(h.substr(0,2),16) + ',' + parseInt(h.substr(2,2),16) + ',' + parseInt(h.substr(4,2),16) + ',' + a + ')';
      }

      // lights not needed (basic materials); stars
      var starGeo = new THREE.BufferGeometry(), sc = 1200, sp = new Float32Array(sc * 3);
      for (var i = 0; i < sc; i++) {
        var r = 60 + Math.random() * 60, th = Math.random() * Math.PI * 2, ph = Math.acos(2 * Math.random() - 1);
        sp[i*3] = r * Math.sin(ph) * Math.cos(th); sp[i*3+1] = r * Math.sin(ph) * Math.sin(th); sp[i*3+2] = r * Math.cos(ph);
      }
      starGeo.setAttribute('position', new THREE.BufferAttribute(sp, 3));
      var starMat = new THREE.PointsMaterial({ color: 0xC9D6DE, size: 1.4, sizeAttenuation: false, transparent: true, opacity: 0.7 });
      scene.add(new THREE.Points(starGeo, starMat)); disposeList.push(starGeo, starMat);

      // graticule (lat/lon lines) + opaque dark core (hides the far side)
      var gp = [], seg = 96;
      function ring(latDeg) {
        for (var s = 0; s < seg; s++) {
          var a0 = ll(latDeg, -180 + 360 * s / seg, R * 1.001), a1 = ll(latDeg, -180 + 360 * (s + 1) / seg, R * 1.001);
          gp.push(a0.x, a0.y, a0.z, a1.x, a1.y, a1.z);
        }
      }
      function meridian(lonDeg) {
        for (var s = 0; s < seg; s++) {
          var a0 = ll(-90 + 180 * s / seg, lonDeg, R * 1.001), a1 = ll(-90 + 180 * (s + 1) / seg, lonDeg, R * 1.001);
          gp.push(a0.x, a0.y, a0.z, a1.x, a1.y, a1.z);
        }
      }
      for (var la = -60; la <= 60; la += 20) ring(la);
      for (var lo = -180; lo < 180; lo += 20) meridian(lo);
      var wireGeo = new THREE.BufferGeometry(); wireGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(gp), 3));
      var wireMat = new THREE.LineBasicMaterial({ color: 0x14b8a6, transparent: true, opacity: 0.16 });
      scene.add(new THREE.LineSegments(wireGeo, wireMat));
      var coreGeo = new THREE.SphereGeometry(R * 0.996, 48, 32);
      var coreMat = new THREE.MeshBasicMaterial({ color: 0x04090b });
      scene.add(new THREE.Mesh(coreGeo, coreMat)); disposeList.push(wireGeo, wireMat, coreGeo, coreMat);

      // atmosphere halo
      var haloMat = new THREE.SpriteMaterial({ map: dot('rgba(20,184,166,0.28)', false), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
      var halo = new THREE.Sprite(haloMat); halo.scale.set(R * 2.7, R * 2.7, 1); scene.add(halo); disposeList.push(haloMat);

      // land dots
      var land = decodeLand(), lp = new Float32Array(land.length / 2 * 3);
      for (var a = 0, b = 0; a < land.length; a += 2, b += 3) { var v = ll(land[a], land[a+1], R * 1.003); lp[b] = v.x; lp[b+1] = v.y; lp[b+2] = v.z; }
      var landGeo = new THREE.BufferGeometry(); landGeo.setAttribute('position', new THREE.BufferAttribute(lp, 3));
      var landMat = new THREE.PointsMaterial({ size: 4, sizeAttenuation: false, map: dot('rgba(45,212,191,1)', true),
        transparent: true, opacity: 1, depthWrite: false, blending: THREE.AdditiveBlending });
      scene.add(new THREE.Points(landGeo, landMat)); disposeList.push(landGeo, landMat);

      // data points of this map (helipads, aircraft, ...)
      var pts = (cfg.points || []).slice(0, 600), ptMat = null;
      if (pts.length) {
        var pp = new Float32Array(pts.length * 3);
        pts.forEach(function (p, k) { var q = ll(p[0], p[1], R * 1.012); pp[k*3] = q.x; pp[k*3+1] = q.y; pp[k*3+2] = q.z; });
        var ptGeo = new THREE.BufferGeometry(); ptGeo.setAttribute('position', new THREE.BufferAttribute(pp, 3));
        ptMat = new THREE.PointsMaterial({ size: 5, sizeAttenuation: false, map: dot(tint('#ffb454', 1), false),
          transparent: true, opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending });
        scene.add(new THREE.Points(ptGeo, ptMat)); disposeList.push(ptGeo, ptMat);
      }

      // target marker (core + glow), size kept ~constant on screen
      var tpos = ll(target[0], target[1], R * 1.014);
      var coreSpr = new THREE.Sprite(new THREE.SpriteMaterial({ map: dot(tint(markerCss, 1), false), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
      var glowSpr = new THREE.Sprite(new THREE.SpriteMaterial({ map: dot(tint(markerCss, 0.9), false), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
      coreSpr.position.copy(tpos); glowSpr.position.copy(tpos); scene.add(coreSpr, glowSpr);
      disposeList.push(coreSpr.material, glowSpr.material);

      // ---------- camera path ----------
      var startLat = 16, startLon = target[1] + 105;
      var dStart = 9.4, dFinal = R + (cfg.finalGap || 0.72);
      function lonDelta(a, b) { var d = ((b - a + 540) % 360) - 180; return d; }
      function place(p1, p2) {
        var lat = lerp(startLat, target[0], p1), lon = startLon + lonDelta(startLon, target[1]) * p1;
        var dir = ll(lat, lon, 1);
        var dist = lerp(dStart, dFinal, p2);
        camera.position.copy(dir).multiplyScalar(dist);
        camera.up.set(0, 1, 0); camera.lookAt(0, 0, 0);
        return dist;
      }
      place(0, 0);

      global.addEventListener('resize', function () {
        W = Math.max(overlay.clientWidth, 2); H = Math.max(overlay.clientHeight, 2);
        camera.aspect = W / H; camera.updateProjectionMatrix(); renderer.setSize(W, H);
      });

      // ---------- run only once the frame is really visible ----------
      // Advance only while >=30% of this map is inside the browser viewport (hidden tab,
      // or scrolled below the fold, => paused). The observer is created on the PARENT
      // window so it accounts for Streamlit's own scroll containers; if the parent is
      // not reachable we fall back to "visible when the frame has a size".
      var inView = true;
      try {
        var fe = global.frameElement, PW = global.parent;
        if (fe && PW && PW !== global && PW.IntersectionObserver) {
          inView = false;
          var io = new PW.IntersectionObserver(function (ents) { inView = ents[ents.length - 1].isIntersecting; }, { threshold: [0.3] });
          io.observe(fe);
          disposeList.push({ dispose: function () { io.disconnect(); } });
        }
      } catch (e) { inView = true; }
      var elapsed = 0, last = null, waitLogged = false;
      function hasSize() { return overlay.clientWidth > 60 && overlay.clientHeight > 60; }
      function frame(now) {
        raf = requestAnimationFrame(frame);
        if (finished) return;
        if (!hasSize() || !inView) { if (!waitLogged) { waitLogged = true; dbg('waiting: frame hidden/off-screen (size ok=' + hasSize() + ', in view=' + inView + ')'); } last = null; return; }        // hidden / off-screen: pause
        if (last === null) {
          last = now;
          if (W !== overlay.clientWidth || H !== overlay.clientHeight) {
            W = overlay.clientWidth; H = overlay.clientHeight;
            camera.aspect = W / H; camera.updateProjectionMatrix(); renderer.setSize(W, H);
          }
        }
        if (elapsed === 0) dbg('playing (frame visible)');
        elapsed += now - last; last = now;
        var t = (cfg.debugT != null) ? cfg.debugT : elapsed / duration, p1 = easeInOutCubic(clamp01(t / 0.62));
        var p2 = easeInOutQuart(clamp01((t - 0.14) / 0.74));
        if (reduced) { p1 = 1; p2 = 0.55; }      // static camera: no rotation, no zoom
        var dist = place(p1, p2);

        // sizes track the zoom so the dots never turn into blobs
        landMat.size = lerp(4.2, 13, p2);
        if (ptMat) ptMat.size = lerp(4, 12, p2);
        var k = 0.05 * Math.max(dist - R, 0.05), pulse = 1 + 0.25 * Math.sin(now / 260);
        coreSpr.scale.set(k * 0.55, k * 0.55, 1); glowSpr.scale.set(k * 1.5 * pulse, k * 1.5 * pulse, 1);
        halo.material.opacity = 1 - 0.7 * p2;

        // HUD choreography
        enter.style.opacity = reduced ? '0' : String(smooth(0.66, 0.78, t) * (1 - smooth(0.93, 1.0, t)));
        reticle.style.opacity = reduced ? '0' : String(smooth(0.70, 0.84, t));
        var rs = lerp(1.9, 1, smooth(0.70, 0.88, t)); reticle.style.transform = 'scale(' + rs.toFixed(3) + ')';
        bar.style.width = (clamp01(t) * 100).toFixed(2) + '%';

        // swap: flash up, then overlay fades -> the real Folium map is revealed
        var fl = reduced ? 0 : smooth(0.80, 0.88, t) * (1 - smooth(0.88, 0.98, t));
        flash.style.opacity = String(fl);
        overlay.style.opacity = String(1 - (reduced ? smooth(0.55, 1.0, t) : smooth(0.86, 1.0, t)));
        renderer.render(scene, camera);
        if (t >= 1 && cfg.debugT == null) finish(false, true);
      }
      raf = requestAnimationFrame(frame);
    }
  };
})(window);
