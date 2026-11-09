/* Legado a Tu Paso — comportamiento del sitio
   Sin dependencias, sin cookies, sin rastreo. */

(function () {
  "use strict";

  /* ------------------------------------------------------------ utilidades */
  function normalizar(texto) {
    return (texto || "")
      .toString()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();
  }

  function numero(valor, decimales) {
    var n = Number(valor);
    if (!isFinite(n)) return "—";
    return n.toLocaleString("es-ES", {
      minimumFractionDigits: decimales,
      maximumFractionDigits: decimales
    });
  }

  /* Textos de los códigos WMO que devuelve Open-Meteo. */
  var CIELO = {
    0: "despejado",
    1: "mayormente despejado",
    2: "parcialmente nublado",
    3: "nublado",
    45: "niebla",
    48: "niebla con escarcha",
    51: "llovizna ligera",
    53: "llovizna moderada",
    55: "llovizna intensa",
    56: "llovizna helada ligera",
    57: "llovizna helada intensa",
    61: "lluvia ligera",
    63: "lluvia moderada",
    65: "lluvia intensa",
    66: "lluvia helada ligera",
    67: "lluvia helada intensa",
    71: "nieve ligera",
    73: "nieve moderada",
    75: "nieve intensa",
    77: "granos de nieve",
    80: "chubascos ligeros",
    81: "chubascos moderados",
    82: "chubascos fuertes",
    85: "chubascos de nieve ligeros",
    86: "chubascos de nieve fuertes",
    95: "tormenta",
    96: "tormenta con granizo ligero",
    99: "tormenta con granizo fuerte"
  };

  function cielo(codigo) {
    return CIELO[Number(codigo)] || "sin datos";
  }

  /* ------------------------------------------------------------- catálogo */
  var rejilla = document.getElementById("rejilla");

  if (rejilla) {
    var items = Array.prototype.slice.call(
      rejilla.querySelectorAll(".rejilla__item")
    );
    var buscador = document.getElementById("buscar");
    var chips = Array.prototype.slice.call(
      document.querySelectorAll(".chip[data-filtro]")
    );
    var resultado = document.getElementById("resultado");
    var vacio = document.getElementById("sin-resultados");
    var filtro = "todas";

    function aplicar() {
      var consulta = buscador ? normalizar(buscador.value) : "";
      var visibles = 0;

      items.forEach(function (item) {
        var texto = normalizar(item.getAttribute("data-buscable"));
        var completa = item.getAttribute("data-completa") === "1";
        var coincideTexto = !consulta || texto.indexOf(consulta) !== -1;
        var coincideFiltro =
          filtro === "todas" ||
          (filtro === "completas" && completa) ||
          (filtro === "pendientes" && !completa);

        var mostrar = coincideTexto && coincideFiltro;
        item.hidden = !mostrar;
        if (mostrar) visibles += 1;
      });

      if (resultado) {
        var etiqueta =
          filtro === "completas"
            ? " con guía completa"
            : filtro === "pendientes"
            ? " en preparación"
            : "";
        resultado.textContent =
          visibles === 1
            ? "1 ciudad" + etiqueta + "."
            : visibles + " ciudades" + etiqueta + ".";
      }

      if (vacio) vacio.hidden = visibles !== 0;
      rejilla.hidden = visibles === 0;
    }

    if (buscador) {
      buscador.addEventListener("input", aplicar);
      buscador.addEventListener("search", aplicar);
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        filtro = chip.getAttribute("data-filtro") || "todas";
        chips.forEach(function (otro) {
          otro.setAttribute(
            "aria-pressed",
            otro === chip ? "true" : "false"
          );
        });
        aplicar();
      });
    });

    aplicar();
  }

  /* ------------------------------------------- tiempo del catálogo (inicio) */
  var estadoTiempo = document.getElementById("tiempo-estado");

  if (rejilla && estadoTiempo) {
    var tarjetasTiempo = Array.prototype.slice.call(
      rejilla.querySelectorAll(".rejilla__item[data-lat][data-lon]")
    );

    function horaCorta() {
      return new Date().toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit"
      });
    }

    function pintarTiempo(datos) {
      if (!Array.isArray(datos)) datos = [datos];

      datos.forEach(function (dato, indice) {
        var item = tarjetasTiempo[indice];
        if (!item) return;
        var salida = item.querySelector(".tarjeta__tiempo");
        var actual = (dato && dato.current) || {};
        if (!salida || actual.temperature_2m === undefined) return;
        salida.textContent =
          numero(actual.temperature_2m, 1) +
          " °C ahora · " +
          cielo(actual.weather_code);
        salida.hidden = false;
      });

      estadoTiempo.textContent =
        "Tiempo actualizado a las " +
        horaCorta() +
        " desde Open-Meteo. Se actualiza cada 5 minutos.";
    }

    function consultarTiempo() {
      if (!tarjetasTiempo.length) return;

      var latitudes = tarjetasTiempo.map(function (item) {
        return item.getAttribute("data-lat");
      });
      var longitudes = tarjetasTiempo.map(function (item) {
        return item.getAttribute("data-lon");
      });

      var url =
        "https://api.open-meteo.com/v1/forecast" +
        "?latitude=" + latitudes.join(",") +
        "&longitude=" + longitudes.join(",") +
        "&current=temperature_2m,weather_code" +
        "&timezone=Europe%2FMadrid";

      fetch(url, { headers: { Accept: "application/json" } })
        .then(function (respuesta) {
          if (!respuesta.ok) throw new Error("HTTP " + respuesta.status);
          return respuesta.json();
        })
        .then(function (datos) {
          pintarTiempo(datos);
        })
        .catch(function () {
          estadoTiempo.textContent =
            "No se ha podido consultar el tiempo ahora. Se mantienen los " +
            "últimos datos y se reintentará en 5 minutos.";
        });
    }

    consultarTiempo();
    window.setInterval(consultarTiempo, 5 * 60 * 1000);
  }

  /* --------------------------------------------------------------- clima */
  var panel = document.getElementById("clima-panel");

  if (panel) {
    var boton = document.getElementById("clima-actualizar");
    var estado = document.getElementById("clima-estado");
    var lista = panel.querySelector(".clima");
    var fuente = panel.querySelector(".panel__fuente");
    var lat = panel.getAttribute("data-lat");
    var lon = panel.getAttribute("data-lon");

    function anunciar(texto) {
      if (estado) estado.textContent = texto;
    }

    function fila(etiqueta, valor, viva) {
      var div = document.createElement("div");
      if (viva) div.className = "clima__vivo";
      var dt = document.createElement("dt");
      dt.textContent = etiqueta;
      var dd = document.createElement("dd");
      dd.textContent = valor;
      div.appendChild(dt);
      div.appendChild(dd);
      return div;
    }

    function pintar(datos, silencioso) {
      if (!lista) return;
      var actual = datos.current || {};
      var diario = datos.daily || {};
      var maximas = diario.temperature_2m_max || [];
      var minimas = diario.temperature_2m_min || [];
      var codigos = diario.weather_code || [];

      var ahora =
        numero(actual.temperature_2m, 1) +
        " °C; sensación " +
        numero(actual.apparent_temperature, 1) +
        " °C; " +
        cielo(actual.weather_code) +
        "; viento " +
        numero(actual.wind_speed_10m, 0) +
        " km/h; humedad " +
        numero(actual.relative_humidity_2m, 0) +
        " %.";

      lista.textContent = "";
      lista.appendChild(fila("Ahora", ahora, true));

      var dias = ["Hoy", "Mañana", "Pasado mañana"];
      for (var i = 0; i < 3 && i < maximas.length; i += 1) {
        lista.appendChild(
          fila(
            dias[i],
            "mínima " +
              numero(minimas[i], 1) +
              " °C, máxima " +
              numero(maximas[i], 1) +
              " °C; " +
              cielo(codigos[i]) +
              ".",
            false
          )
        );
      }

      var consulta = new Date();
      var hora = consulta.toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit"
      });
      var fecha = consulta.toLocaleDateString("es-ES", {
        day: "numeric",
        month: "long"
      });

      if (fuente) {
        fuente.textContent =
          "Open-Meteo, consulta del " + fecha + " a las " + hora + ".";
      }

      if (!silencioso) {
        anunciar(
          "Datos del tiempo actualizados a las " +
            hora +
            ". " +
            ahora
        );
      }
    }

    function consultar(silencioso) {
      if (!lat || !lon) {
        if (!silencioso) anunciar("No hay coordenadas para consultar el tiempo.");
        return;
      }

      var url =
        "https://api.open-meteo.com/v1/forecast" +
        "?latitude=" + encodeURIComponent(lat) +
        "&longitude=" + encodeURIComponent(lon) +
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m," +
        "weather_code,wind_speed_10m" +
        "&daily=weather_code,temperature_2m_max,temperature_2m_min" +
        "&timezone=Europe%2FMadrid&forecast_days=3";

      if (boton && !silencioso) {
        boton.disabled = true;
        boton.textContent = "Consultando…";
      }
      if (!silencioso) anunciar("Consultando el tiempo a Open-Meteo.");

      fetch(url, { headers: { Accept: "application/json" } })
        .then(function (respuesta) {
          if (!respuesta.ok) {
            throw new Error("HTTP " + respuesta.status);
          }
          return respuesta.json();
        })
        .then(function (datos) {
          pintar(datos, silencioso);
        })
        .catch(function () {
          if (silencioso) {
            if (fuente) {
              fuente.textContent =
                "No se ha podido actualizar el tiempo. Se mantienen los datos " +
                "de la última consulta y se reintentará en 5 minutos.";
            }
          } else {
            anunciar(
              "No se ha podido consultar el tiempo. Revisa tu conexión o " +
                "inténtalo más tarde. Se mantienen los datos de la última consulta."
            );
          }
        })
        .then(function () {
          if (boton && !silencioso) {
            boton.disabled = false;
            boton.textContent = "Actualizar el tiempo ahora";
          }
        });
    }

    if (boton) {
      boton.addEventListener("click", function () {
        consultar(false);
      });
    }

    /* Al abrir la página se consulta en silencio y se repite cada 5 minutos,
       para no interrumpir a quien usa lector de pantalla. */
    consultar(true);
    window.setInterval(function () {
      consultar(true);
    }, 5 * 60 * 1000);
  }

  /* ---------------------------------------------------------------- mapas */
  if (window.L && window.L.map) {
    var TESELAS = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
    var CREDITO =
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';

    function prepararMapa(elemento) {
      var mapa = L.map(elemento, {
        scrollWheelZoom: false,
        zoomControl: false,
        attributionControl: true
      });
      L.control
        .zoom({ zoomInTitle: "Acercar", zoomOutTitle: "Alejar" })
        .addTo(mapa);
      L.tileLayer(TESELAS, {
        maxZoom: 19,
        attribution: CREDITO
      }).addTo(mapa);
      mapa.attributionControl.setPrefix(
        '<a href="https://leafletjs.com/" title="Biblioteca de mapas interactivos">Leaflet</a>'
      );
      mapa.on("popupopen", function (evento) {
        var cerrar = evento.popup._closeButton;
        if (cerrar) {
          cerrar.title = "Cerrar";
          cerrar.setAttribute("aria-label", "Cerrar");
        }
      });
      return mapa;
    }

    var mapaRuta = document.getElementById("mapa-ruta");
    var datosRuta = document.getElementById("mapa-ruta-datos");

    if (mapaRuta && datosRuta) {
      try {
        var ruta = JSON.parse(datosRuta.textContent);
        var mapa = prepararMapa(mapaRuta);
        var paradas = ruta.paradas || [];
        var puntos = paradas.map(function (p) {
          return [p.lat, p.lon];
        });

        if (puntos.length) {
          L.polyline(puntos, {
            color: "#5e2e1b",
            weight: 3.5,
            opacity: 0.85
          }).addTo(mapa);

          // Los marcadores son una ayuda visual, no controles: las paradas
          // navegables están en la lista de texto. Así se evita que dos
          // marcadores cercanos solapen y rompan el tamaño de toque.
          paradas.forEach(function (p) {
            L.marker([p.lat, p.lon], {
              interactive: false,
              keyboard: false,
              title: "Parada " + p.n + ": " + p.nombre,
              icon: L.divIcon({
                className: "marcador-num",
                html: '<span aria-hidden="true">' + p.n + "</span>",
                iconSize: [30, 30],
                iconAnchor: [15, 15]
              })
            }).addTo(mapa);
          });

          mapa.fitBounds(puntos, { padding: [32, 32], maxZoom: 16 });
        } else if (ruta.centro) {
          mapa.setView(ruta.centro, 14);
        }
      } catch (error) {
        mapaRuta.hidden = true;
      }
    }

    var mapaCiudades = document.getElementById("mapa-ciudades");
    var datosCiudades = document.getElementById("mapa-ciudades-datos");

    if (mapaCiudades && datosCiudades) {
      try {
        var catalogo = JSON.parse(datosCiudades.textContent);
        var mapaCatalogo = prepararMapa(mapaCiudades);
        var esquinas = [];

        catalogo.forEach(function (c) {
          esquinas.push([c.lat, c.lon]);
          L.marker([c.lat, c.lon], {
            interactive: false,
            keyboard: false,
            title: c.nombre + " (" + c.comunidad + ")",
            icon: L.divIcon({
              className:
                "marcador-punto" +
                (c.completa ? "" : " marcador-punto--pronto"),
              html: '<span aria-hidden="true"></span>',
              iconSize: [22, 22],
              iconAnchor: [11, 11]
            })
          }).addTo(mapaCatalogo);
        });

        if (esquinas.length) {
          mapaCatalogo.fitBounds(esquinas, { padding: [24, 24], maxZoom: 7 });
        }
      } catch (error) {
        mapaCiudades.hidden = true;
      }
    }
  }

  /* --------------------------------------------------------------- tablas */
  var envoltorios = document.querySelectorAll(".tabla-envoltorio");

  function revisarTablas() {
    var avisado = false;
    Array.prototype.forEach.call(envoltorios, function (envoltorio) {
      var pista = envoltorio.nextElementSibling;
      if (!pista || !pista.classList.contains("pista-tabla")) return;
      var desborda = envoltorio.scrollWidth > envoltorio.clientWidth + 1;
      pista.hidden = !desborda || avisado;
      if (desborda) avisado = true;
    });
  }

  if (envoltorios.length) {
    revisarTablas();
    window.addEventListener("resize", revisarTablas);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(revisarTablas);
    }
  }

  /* ------------------------------------------------------- plan impreso */
  var botonImprimir = document.getElementById("imprimir");

  if (botonImprimir) {
    botonImprimir.addEventListener("click", function () {
      window.print();
    });
  }

  /* --------------------------------------------------------------- audio */
  document.addEventListener(
    "play",
    function (evento) {
      var objetivo = evento.target;
      if (!objetivo || objetivo.tagName !== "AUDIO") return;
      var todos = document.querySelectorAll("audio");
      Array.prototype.forEach.call(todos, function (otro) {
        if (otro !== objetivo && !otro.paused) otro.pause();
      });
    },
    true
  );

  /* ------------------------------------------- app instalable y sin conexión */
  var esCapacitor = false;
  try {
    esCapacitor = !!(
      window.Capacitor &&
      window.Capacitor.isNativePlatform &&
      window.Capacitor.isNativePlatform()
    );
  } catch (error) {
    esCapacitor = false;
  }

  var soportaSW = "serviceWorker" in navigator && !esCapacitor;
  var estadoConexion = document.getElementById("estado-conexion");
  var avisoConexion = document.getElementById("aviso-conexion");

  function actualizarConexion() {
    var enLinea = navigator.onLine;
    if (avisoConexion) avisoConexion.hidden = enLinea;

    if (!estadoConexion) return;
    if (esCapacitor) {
      estadoConexion.textContent = enLinea
        ? "App instalada. Las guías y sus audios están incluidos; el mapa y el tiempo necesitan conexión."
        : "Sin conexión. Las guías y sus audios están incluidos en la app; el mapa y el tiempo no se actualizan.";
    } else {
      estadoConexion.textContent = enLinea
        ? "Con conexión. Las guías descargadas siguen disponibles sin datos."
        : "Sin conexión. Puedes leer las guías descargadas y escuchar sus audios; el mapa y el tiempo no se actualizan.";
    }
  }

  window.addEventListener("online", actualizarConexion);
  window.addEventListener("offline", actualizarConexion);
  actualizarConexion();

  /* ------------------------------------------------------------- instalación */
  var botonInstalar = document.getElementById("instalar-app");
  var ayudaInstalar = document.getElementById("instalar-ayuda");
  var promptInstalar = null;
  var modoApp =
    (window.matchMedia &&
      window.matchMedia("(display-mode: standalone)").matches) ||
    navigator.standalone === true;
  var esIOS =
    /iphone|ipad|ipod/i.test(navigator.userAgent) ||
    (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

  if (esCapacitor || modoApp) {
    if (botonInstalar) botonInstalar.hidden = true;
    if (ayudaInstalar) {
      ayudaInstalar.hidden = false;
      ayudaInstalar.textContent = "Ya estás usando la app instalada.";
    }
  } else if (esIOS && soportaSW) {
    if (ayudaInstalar) {
      ayudaInstalar.hidden = false;
      ayudaInstalar.textContent =
        "En iPhone o iPad, toca Compartir y elige «Añadir a pantalla de inicio».";
    }
  } else if (!soportaSW) {
    if (ayudaInstalar) {
      ayudaInstalar.hidden = false;
      ayudaInstalar.textContent =
        "Este navegador no permite instalar la app. Puedes usar la web y descargar los audios de cada guía.";
    }
  }

  window.addEventListener("beforeinstallprompt", function (evento) {
    evento.preventDefault();
    promptInstalar = evento;
    if (botonInstalar) botonInstalar.hidden = false;
  });

  if (botonInstalar) {
    botonInstalar.addEventListener("click", function () {
      if (!promptInstalar) return;
      promptInstalar.prompt();
      promptInstalar.userChoice
        .then(function () {
          promptInstalar = null;
          botonInstalar.hidden = true;
        })
        .catch(function () {
          botonInstalar.hidden = true;
        });
    });
  }

  window.addEventListener("appinstalled", function () {
    if (botonInstalar) botonInstalar.hidden = true;
    if (ayudaInstalar) {
      ayudaInstalar.hidden = false;
      ayudaInstalar.textContent =
        "La app ya está instalada. Ábrela desde la pantalla de inicio.";
    }
  });

  /* ------------------------------------------------- descarga por ciudad */
  var seccionDescarga = document.getElementById("descarga");
  var datosDescarga = document.getElementById("descarga-datos");

  if (seccionDescarga && datosDescarga) {
    if (esCapacitor) {
      seccionDescarga.hidden = true;
    } else if (!soportaSW) {
      var botonSinSW = document.getElementById("descargar-ciudad");
      var estadoSinSW = document.getElementById("descarga-estado");
      if (botonSinSW) botonSinSW.hidden = true;
      if (estadoSinSW) {
        estadoSinSW.textContent =
          "Este navegador no puede guardar la guía completa sin conexión. " +
          "Puedes descargar los audios uno a uno desde cada parada.";
      }
    } else {
      prepararDescarga();
    }
  }

  function prepararDescarga() {
    var datos;
    try {
      datos = JSON.parse(datosDescarga.textContent);
    } catch (error) {
      seccionDescarga.hidden = true;
      return;
    }

    var urls = (datos && datos.urls) || [];
    var total = urls.length;
    var botonDescargar = document.getElementById("descargar-ciudad");
    var botonBorrar = document.getElementById("borrar-descarga");
    var estadoDescarga = document.getElementById("descarga-estado");
    var progresoDescarga = document.getElementById("descarga-progreso");
    var registroSW = null;

    if (!total) {
      seccionDescarga.hidden = true;
      return;
    }

    function enviar(mensaje) {
      if (registroSW && registroSW.active) {
        registroSW.active.postMessage(mensaje);
        return;
      }
      navigator.serviceWorker.ready
        .then(function (registro) {
          registroSW = registro;
          if (registro.active) registro.active.postMessage(mensaje);
        })
        .catch(function () {
          if (estadoDescarga) {
            estadoDescarga.textContent =
              "No se ha podido preparar la descarga. Recarga la página e inténtalo de nuevo.";
          }
        });
    }

    function mostrarProgreso(valor) {
      if (!progresoDescarga) return;
      progresoDescarga.hidden = false;
      progresoDescarga.value = valor;
      progresoDescarga.textContent = valor + " %";
    }

    function estadoGuardado(hechos) {
      if (!estadoDescarga) return;
      if (hechos === total) {
        estadoDescarga.textContent =
          "Guía guardada en este dispositivo. Ya puedes leerla y escuchar sus audios sin conexión.";
        if (botonDescargar) botonDescargar.hidden = true;
        if (botonBorrar) botonBorrar.hidden = false;
        if (progresoDescarga) progresoDescarga.hidden = true;
      } else if (hechos > 0) {
        estadoDescarga.textContent =
          "Guardada a medias (" +
          hechos +
          " de " +
          total +
          " archivos). Descarga de nuevo para completarla.";
        if (botonDescargar) {
          botonDescargar.hidden = false;
          botonDescargar.textContent = "Completar la descarga";
          botonDescargar.disabled = false;
        }
        if (botonBorrar) botonBorrar.hidden = false;
        if (progresoDescarga) progresoDescarga.hidden = true;
      } else {
        estadoDescarga.textContent =
          "Todavía no está guardada. Descarga las fotos y los audios para usarla sin conexión.";
        if (botonDescargar) {
          botonDescargar.hidden = false;
          botonDescargar.textContent = "Descargar esta ciudad";
          botonDescargar.disabled = false;
        }
        if (botonBorrar) botonBorrar.hidden = true;
        if (progresoDescarga) progresoDescarga.hidden = true;
      }
    }

    navigator.serviceWorker.addEventListener("message", function (evento) {
      var mensaje = evento.data || {};
      if (mensaje.city !== datos.ciudad) return;

      if (mensaje.type === "CITY_PROGRESS") {
        mostrarProgreso(
          mensaje.total
            ? Math.round((mensaje.done / mensaje.total) * 100)
            : 0
        );
      } else if (mensaje.type === "CITY_DONE") {
        if (mensaje.failed) {
          if (estadoDescarga) {
            estadoDescarga.textContent =
              "Se han guardado " +
              mensaje.done +
              " de " +
              mensaje.total +
              " archivos. Comprueba la conexión y reintenta la descarga.";
          }
          if (botonDescargar) {
            botonDescargar.hidden = false;
            botonDescargar.textContent = "Reintentar la descarga";
            botonDescargar.disabled = false;
          }
          if (botonBorrar) botonBorrar.hidden = false;
          if (progresoDescarga) progresoDescarga.hidden = true;
        } else {
          estadoGuardado(total);
        }
      } else if (mensaje.type === "CITY_STATUS") {
        estadoGuardado(mensaje.done || 0);
      } else if (mensaje.type === "CITY_CLEARED") {
        if (estadoDescarga) {
          estadoDescarga.textContent =
            "Descarga borrada. Puedes volver a guardar esta ciudad cuando quieras.";
        }
        if (botonDescargar) {
          botonDescargar.hidden = false;
          botonDescargar.textContent = "Descargar esta ciudad";
          botonDescargar.disabled = false;
        }
        if (botonBorrar) {
          botonBorrar.hidden = true;
          botonBorrar.disabled = false;
        }
        if (progresoDescarga) progresoDescarga.hidden = true;
      }
    });

    if (botonDescargar) {
      botonDescargar.addEventListener("click", function () {
        if (!navigator.onLine) {
          if (estadoDescarga) {
            estadoDescarga.textContent =
              "Necesitas conexión para descargar la guía por primera vez.";
          }
          return;
        }
        if (navigator.storage && navigator.storage.persist) {
          navigator.storage.persist().catch(function () {});
        }
        botonDescargar.disabled = true;
        botonDescargar.hidden = true;
        if (botonBorrar) botonBorrar.hidden = true;
        if (estadoDescarga) {
          estadoDescarga.textContent =
            "Guardando la guía sin conexión. No cierres esta página.";
        }
        mostrarProgreso(0);
        enviar({ type: "CACHE_CITY", city: datos.ciudad, urls: urls });
      });
    }

    if (botonBorrar) {
      botonBorrar.addEventListener("click", function () {
        var confirmado = window.confirm(
          "¿Borrar las fotos y los audios guardados de esta ciudad?"
        );
        if (!confirmado) return;
        botonBorrar.disabled = true;
        if (estadoDescarga) {
          estadoDescarga.textContent = "Borrando la descarga…";
        }
        enviar({ type: "CLEAR_CITY", city: datos.ciudad, urls: urls });
      });
    }

    navigator.serviceWorker.ready
      .then(function (registro) {
        registroSW = registro;
        enviar({ type: "CITY_STATUS", city: datos.ciudad, urls: urls });
      })
      .catch(function () {
        if (estadoDescarga) {
          estadoDescarga.textContent =
            "No se ha podido comprobar la descarga. Recarga la página e inténtalo de nuevo.";
        }
      });
  }

  /* ------------------------------------------------------ registro del SW */
  if (soportaSW) {
    window.addEventListener("load", function () {
      navigator.serviceWorker
        .register("sw.js", { scope: "./", updateViaCache: "none" })
        .catch(function () {
          /* Sin service worker la web sigue funcionando, solo pierde el modo
             sin conexión. No mostramos un error técnico al visitante. */
        });
    });
  }
})();
