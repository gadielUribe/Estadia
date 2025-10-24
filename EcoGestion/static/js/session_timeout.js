(function () {
  // Detectar si estás en la página de login (no aplicar nada)
  const path = window.location.pathname;
  if (path.includes("/account/login")) {
    return; // No hacer nada en la página de login
  }

  const thisScript = document.currentScript || (function() {
    const scripts = document.getElementsByTagName('script');
    return scripts[scripts.length - 1];
  })();

  // Tiempo máximo antes de advertir (en segundos)
  const MAX_SESSION_TIME = parseInt(thisScript.dataset.timeoutSeconds || '1000', 10); // 
  let remaining = MAX_SESSION_TIME;
  let warned = false;

  // Solo se reinicia si hay click o movimiento del mouse
  function resetTimer() {
    remaining = MAX_SESSION_TIME;
    warned = false;
  }

  ['click','mousemove','keypress','scroll','touchstart'].forEach(evt => 
    document.addEventListener(evt, resetTimer, { passive: true })
  );

  // Cuenta regresiva
  const tick = setInterval(() => {
    remaining--;

    // Muestra la advertencia cuando falte 1 minuto
    if (!warned && remaining === 60) {
      warned = true;
      alert("Tu sesión está a punto de expirar por inactividad.");
    }

    if (remaining <= 0) {
      clearInterval(tick);
      window.location.href = logout;
    }

  }, 1000);
})();
