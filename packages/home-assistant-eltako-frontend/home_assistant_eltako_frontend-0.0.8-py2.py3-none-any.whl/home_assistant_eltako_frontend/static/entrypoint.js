function loadES5() {
    var el = document.createElement('script');
    el.src = '/eltako/assets/index-BYw5rWpL.js';
    document.body.appendChild(el);
  }
  if (/.*Version\/(?:11|12)(?:\.\d+)*.*Safari\//.test(navigator.userAgent)) {
      loadES5();
  } else {
    try {
      new Function("import('/eltako/assets/index-BYw5rWpL.js')")();
    } catch (err) {
      loadES5();
    }
  }