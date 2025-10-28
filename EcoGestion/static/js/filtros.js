(function() {
  const form = document.getElementById('filtrosForm');
  const input = document.getElementById('buscarInput');
  if (!form || !input) return;

  let t = null;
  input.addEventListener('input', function() {
    clearTimeout(t);
    t = setTimeout(() => form.submit(), 400); // “dinámico”
  });

  // Auto-submit si cambian fechas
  form.querySelectorAll('input[type="date"]').forEach(el => {
    el.addEventListener('change', () => form.submit());
  });
})();
