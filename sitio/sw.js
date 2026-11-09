/* Legado a Tu Paso — service worker.
   Generado por herramientas/generar_sitio.py: no editar sitio/sw.js a mano.

   Estrategia:
   - Cáscara (HTML, CSS, JS, fuentes, logos e iconos): precarga y red primero
     para las páginas, caché primero para los recursos estáticos.
   - Fotos y audios: caché persistente bajo demanda, con soporte de Range para
     que el audio se pueda reproducir y buscar sin conexión.
   - Mapa, tiempo y enlaces externos: no se interceptan; necesitan conexión. */

const VERSION = "1cdf4095ac9a";
const SHELL_CACHE = "legado-shell-" + VERSION;
const MEDIA_CACHE = "legado-media-v1";
const PRECACHE = [
  "index.html",
  "avila.html",
  "alcala-de-henares.html",
  "cordoba.html",
  "merida.html",
  "salamanca.html",
  "santiago-de-compostela.html",
  "segovia.html",
  "toledo.html",
  "accesibilidad.html",
  "verificacion.html",
  "creditos.html",
  "404.html",
  "assets/estilos.css",
  "assets/app.js",
  "assets/leaflet/leaflet.css",
  "assets/leaflet/leaflet.js",
  "assets/logo.svg",
  "assets/logo-claro.svg",
  "assets/logo-emblema.svg",
  "assets/logo-emblema-claro.svg",
  "assets/favicon.svg",
  "assets/social/og.png",
  "favicon.ico",
  "manifest.webmanifest",
  "assets/fuente/atkinson-400-latin-ext.woff2",
  "assets/fuente/atkinson-400-latin.woff2",
  "assets/fuente/atkinson-700-latin-ext.woff2",
  "assets/fuente/atkinson-700-latin.woff2",
  "assets/fuente/literata-600-latin-ext.woff2",
  "assets/fuente/literata-600-latin.woff2",
  "assets/iconos/apple-touch-icon.png",
  "assets/iconos/icono-192.png",
  "assets/iconos/icono-512.png",
  "assets/iconos/icono-maskable-512.png"
];
const TIEMPO_MAXIMO_RED = 3500;

function absoluta(ruta) {
  return new URL(ruta, self.registration.scope).href;
}

function sinConexion() {
  return new Response("", {
    status: 504,
    statusText: "Sin conexión"
  });
}

function conLimite(promesa, milisegundos) {
  return new Promise(function (resolver, rechazar) {
    const temporizador = setTimeout(function () {
      rechazar(new Error("Tiempo de espera agotado"));
    }, milisegundos);
    promesa.then(
      function (valor) {
        clearTimeout(temporizador);
        resolver(valor);
      },
      function (error) {
        clearTimeout(temporizador);
        rechazar(error);
      }
    );
  });
}

/* ---------------------------------------------------------------- ciclo de vida */
self.addEventListener("install", function (evento) {
  evento.waitUntil(
    (async function () {
      const cache = await caches.open(SHELL_CACHE);
      await Promise.all(
        PRECACHE.map(function (ruta) {
          return cache
            .add(new Request(absoluta(ruta), { cache: "reload" }))
            .catch(function () {
              /* Un recurso que falle no debe impedir instalar la app. */
            });
        })
      );
      await self.skipWaiting();
    })()
  );
});

self.addEventListener("activate", function (evento) {
  evento.waitUntil(
    (async function () {
      const claves = await caches.keys();
      await Promise.all(
        claves.map(function (clave) {
          if (clave.indexOf("legado-shell-") === 0 && clave !== SHELL_CACHE) {
            return caches.delete(clave);
          }
          return null;
        })
      );
      await self.clients.claim();
    })()
  );
});

/* ---------------------------------------------------------------------- fetch */
self.addEventListener("fetch", function (evento) {
  const peticion = evento.request;
  if (peticion.method !== "GET") return;

  const url = new URL(peticion.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.endsWith("/sw.js")) return;

  if (peticion.mode === "navigate") {
    evento.respondWith(navegacion(peticion));
    return;
  }

  if (url.pathname.indexOf("/audio/") !== -1) {
    evento.respondWith(audio(peticion));
    return;
  }

  if (url.pathname.indexOf("/assets/fotos/") !== -1) {
    evento.respondWith(media(peticion));
    return;
  }

  evento.respondWith(estatico(peticion));
});

async function navegacion(peticion) {
  const cache = await caches.open(SHELL_CACHE);
  try {
    const respuesta = await conLimite(
      fetch(peticion),
      TIEMPO_MAXIMO_RED
    );
    /* Un 502 de un proxy o de un servidor caído no debe sustituir a la copia
       guardada: solo se usa la red si la respuesta es correcta. */
    if (respuesta && respuesta.ok) {
      cache.put(peticion, respuesta.clone()).catch(function () {});
      return respuesta;
    }
  } catch (error) {
    /* Sin red: se continúa con la caché. */
  }

  const guardada = await cache.match(peticion, { ignoreSearch: true });
  if (guardada) return guardada;
  const inicio = await cache.match(absoluta("index.html"));
  if (inicio) return inicio;
  return new Response(
    "<!doctype html><html lang=\"es\"><meta charset=\"utf-8\">" +
      "<title>Sin conexión | Legado a Tu Paso</title>" +
      "<p>Sin conexión. Abre la app una vez con internet para guardar las " +
      "guías que quieras consultar después.</p></html>",
    {
      status: 503,
      headers: { "Content-Type": "text/html; charset=utf-8" }
    }
  );
}

async function estatico(peticion) {
  const cache = await caches.open(SHELL_CACHE);
  const guardada = await cache.match(peticion, { ignoreSearch: true });

  if (guardada) {
    fetch(peticion)
      .then(function (respuesta) {
        if (respuesta && respuesta.ok) {
          cache.put(peticion, respuesta.clone()).catch(function () {});
        }
      })
      .catch(function () {});
    return guardada;
  }

  try {
    const respuesta = await fetch(peticion);
    if (respuesta && respuesta.ok) {
      cache.put(peticion, respuesta.clone()).catch(function () {});
    }
    return respuesta;
  } catch (error) {
    return sinConexion();
  }
}

async function media(peticion) {
  const cache = await caches.open(MEDIA_CACHE);
  const guardada = await cache.match(peticion, { ignoreSearch: true });
  if (guardada) return guardada;

  try {
    const respuesta = await fetch(peticion);
    if (respuesta && respuesta.ok) {
      cache.put(peticion, respuesta.clone()).catch(function () {});
    }
    return respuesta;
  } catch (error) {
    return sinConexion();
  }
}

/* ----------------------------------------------------------------------- audio */
function leerRango(cabecera, tamano) {
  const coincidencia = /^bytes=(\d*)-(\d*)$/.exec((cabecera || "").trim());
  if (!coincidencia) return null;

  let inicio =
    coincidencia[1] === "" ? null : parseInt(coincidencia[1], 10);
  let fin = coincidencia[2] === "" ? null : parseInt(coincidencia[2], 10);

  if (inicio === null) {
    if (fin === null || fin === 0) return null;
    inicio = Math.max(0, tamano - fin);
    fin = tamano - 1;
  } else if (fin === null || fin >= tamano) {
    fin = tamano - 1;
  }

  if (inicio < 0 || inicio >= tamano || inicio > fin) return null;
  return { inicio: inicio, fin: fin };
}

async function recortar(respuesta, rango) {
  const datos = await respuesta.arrayBuffer();
  const tamano = datos.byteLength;
  const limites = leerRango(rango, tamano);
  const cabeceras = new Headers();
  cabeceras.set("Accept-Ranges", "bytes");
  cabeceras.set(
    "Content-Type",
    respuesta.headers.get("Content-Type") || "application/octet-stream"
  );

  if (!limites) {
    cabeceras.set("Content-Range", "bytes */" + tamano);
    return new Response(null, {
      status: 416,
      statusText: "Range Not Satisfiable",
      headers: cabeceras
    });
  }

  const trozo = datos.slice(limites.inicio, limites.fin + 1);
  cabeceras.set(
    "Content-Range",
    "bytes " + limites.inicio + "-" + limites.fin + "/" + tamano
  );
  cabeceras.set("Content-Length", String(trozo.byteLength));
  cabeceras.set("Cache-Control", "no-store");
  return new Response(trozo, {
    status: 206,
    statusText: "Partial Content",
    headers: cabeceras
  });
}

async function audio(peticion) {
  const cache = await caches.open(MEDIA_CACHE);
  const clave = new Request(peticion.url);
  let guardada = await cache.match(clave, { ignoreSearch: true });

  if (!guardada) {
    try {
      const respuesta = await fetch(clave, { cache: "reload" });
      if (!respuesta || !respuesta.ok) {
        return respuesta || sinConexion();
      }
      await cache.put(clave, respuesta.clone());
      guardada = await cache.match(clave, { ignoreSearch: true });
    } catch (error) {
      return sinConexion();
    }
  }

  if (!guardada) return sinConexion();

  const rango = peticion.headers.get("Range");
  if (!rango) return guardada;
  return recortar(guardada, rango);
}

/* ------------------------------------------------------------------ mensajes */
function avisar(cliente, mensaje) {
  if (cliente && cliente.postMessage) {
    cliente.postMessage(mensaje);
  }
}

async function guardarCiudad(datos, cliente) {
  const urls = (datos.urls || []).map(absoluta);
  const cache = await caches.open(MEDIA_CACHE);
  let hechos = 0;
  let fallos = 0;

  for (const url of urls) {
    try {
      const existente = await cache.match(url, { ignoreSearch: true });
      if (!existente) {
        const respuesta = await fetch(url, { cache: "reload" });
        if (!respuesta || !respuesta.ok) {
          throw new Error("HTTP " + (respuesta ? respuesta.status : "sin respuesta"));
        }
        await cache.put(url, respuesta);
      }
    } catch (error) {
      fallos += 1;
    }
    hechos += 1;
    avisar(cliente, {
      type: "CITY_PROGRESS",
      city: datos.city,
      done: hechos,
      total: urls.length,
      failed: fallos
    });
  }

  avisar(cliente, {
    type: "CITY_DONE",
    city: datos.city,
    done: hechos,
    total: urls.length,
    failed: fallos
  });
}

async function borrarCiudad(datos, cliente) {
  const urls = (datos.urls || []).map(absoluta);
  const cache = await caches.open(MEDIA_CACHE);
  let hechos = 0;
  let fallos = 0;

  for (const url of urls) {
    try {
      await cache.delete(url, { ignoreSearch: true });
    } catch (error) {
      fallos += 1;
    }
    hechos += 1;
  }

  avisar(cliente, {
    type: "CITY_CLEARED",
    city: datos.city,
    done: hechos,
    total: urls.length,
    failed: fallos
  });
}

async function estadoCiudad(datos, cliente) {
  const urls = (datos.urls || []).map(absoluta);
  const cache = await caches.open(MEDIA_CACHE);
  let hechos = 0;

  for (const url of urls) {
    if (await cache.match(url, { ignoreSearch: true })) {
      hechos += 1;
    }
  }

  avisar(cliente, {
    type: "CITY_STATUS",
    city: datos.city,
    done: hechos,
    total: urls.length
  });
}

self.addEventListener("message", function (evento) {
  const datos = evento.data || {};
  const cliente = evento.source;

  if (datos.type === "CACHE_CITY") {
    evento.waitUntil(guardarCiudad(datos, cliente));
  } else if (datos.type === "CLEAR_CITY") {
    evento.waitUntil(borrarCiudad(datos, cliente));
  } else if (datos.type === "CITY_STATUS") {
    evento.waitUntil(estadoCiudad(datos, cliente));
  }
});
