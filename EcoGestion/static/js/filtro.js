(function () {
  const form = document.getElementById("filtrosForm");
  const results = document.getElementById("results");
  if (!form || !results) return;

  const inputBuscar = document.getElementById("buscarInput") || form.querySelector('input[name="q"]');
  let timer = null;

  // Utilidad: arma querystring con los valores del form
  function buildQuery() {
    const params = new URLSearchParams(new FormData(form));
    return params.toString();
  }

  // Reemplaza solo la sección de resultados
  async function fetchResultados() {
    const qs = buildQuery();
    const url = `${window.location.pathname}?${qs}`;

    try {
      const resp = await fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
        cache: "no-store",
      });
      const html = await resp.text();

      // Parsear el HTML y extraer #results
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");
      const newResults = doc.getElementById("results");
      const newCount = doc.querySelector("p.text-muted");

      if (newResults) {
        results.replaceChildren(...newResults.childNodes);
      }
      // Actualiza el “Resultados: N” si existe
      if (newCount) {
        const currentCount = document.querySelector("p.text-muted");
        if (currentCount) currentCount.replaceWith(newCount);
      }

      // Actualiza la URL en la barra sin recargar
      window.history.replaceState(null, "", url);
    } catch (e) {
      console.error("Error al actualizar resultados:", e);
    }
  }

  // Búsqueda dinámica sin perder foco
  if (inputBuscar) {
    inputBuscar.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(fetchResultados, 400);
    });
  }

  // Cambios de fechas
  form.querySelectorAll('input[type="date"], select').forEach((el) => {
    el.addEventListener("change", fetchResultados);
  });

  // Enter = actualizar AJAX en lugar de submit
  form.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      fetchResultados();
    }
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    fetchResultados();
  });
})();
