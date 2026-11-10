# -*- coding: utf-8 -*-
"""Genera el sitio estático de Legado a Tu Paso a partir de contenido/*.md.

Uso:
    python herramientas/generar_sitio.py

Salida:
    sitio/index.html
    sitio/<id-ciudad>.html
    sitio/accesibilidad.html
    sitio/creditos.html
"""

import hashlib
import html
import io
import json
import os
import re
import shutil
import wave

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENIDO = os.path.join(BASE, "contenido")
SITIO = os.path.join(BASE, "sitio")
FOTOS = os.path.join(SITIO, "assets", "fotos")
AUDIO_SRC = os.path.join(BASE, "audio")
AUDIO_DST = os.path.join(SITIO, "audio")
EXT_AUDIO = (".mp3", ".wav", ".ogg", ".opus", ".m4a")

SITIO_URL = os.environ.get("LEGADO_URL", "").strip().rstrip("/")
CIUDADES = [
    ("avila", "Ávila"),
    ("alcala-de-henares", "Alcalá de Henares"),
    ("cordoba", "Córdoba"),
    ("merida", "Mérida"),
    ("salamanca", "Salamanca"),
    ("santiago-de-compostela", "Santiago de Compostela"),
    ("segovia", "Segovia"),
    ("toledo", "Toledo"),
]

PENDIENTES = [
    {
        "id": "baeza",
        "nombre": "Baeza",
        "provincia": "Jaén",
        "comunidad": "Andalucía",
        "unesco": "2003",
        "texto": "Conjunto renacentista de palacios y plazas en la provincia de Jaén.",
        "lat": "37.9938",
        "lon": "-3.4700",
    },
    {
        "id": "caceres",
        "nombre": "Cáceres",
        "provincia": "Cáceres",
        "comunidad": "Extremadura",
        "unesco": "1986",
        "texto": "Ciudad medieval de torres, piedra y murallas casi intactas.",
        "lat": "39.4716",
        "lon": "-6.3710",
    },
    {
        "id": "cuenca",
        "nombre": "Cuenca",
        "provincia": "Cuenca",
        "comunidad": "Castilla-La Mancha",
        "unesco": "1996",
        "texto": "Casas colgadas sobre la hoz del Huécar y casco histórico en cuesta.",
        "lat": "40.0704",
        "lon": "-2.1374",
    },
    {
        "id": "eivissa",
        "nombre": "Eivissa",
        "provincia": "Illes Balears",
        "comunidad": "Illes Balears",
        "unesco": "1999",
        "texto": "Dalt Vila, la ciudad fortificada que domina el puerto de Ibiza.",
        "lat": "38.9089",
        "lon": "1.4326",
    },
    {
        "id": "la-laguna",
        "nombre": "San Cristóbal de La Laguna",
        "provincia": "Santa Cruz de Tenerife",
        "comunidad": "Canarias",
        "unesco": "1999",
        "texto": "Primera ciudad universitaria sin murallas, con trazado renacentista.",
        "lat": "28.4853",
        "lon": "-16.3167",
    },
    {
        "id": "tarragona",
        "nombre": "Tarragona",
        "provincia": "Tarragona",
        "comunidad": "Cataluña",
        "unesco": "2000",
        "texto": "Tarraco romana: anfiteatro, circo y murallas junto al mar.",
        "lat": "41.1189",
        "lon": "1.2445",
    },
    {
        "id": "ubeda",
        "nombre": "Úbeda",
        "provincia": "Jaén",
        "comunidad": "Andalucía",
        "unesco": "2003",
        "texto": "Plazas y palacios renacentistas en el corazón de Jaén.",
        "lat": "38.0116",
        "lon": "-3.3702",
    },
]

WMO = {
    0: "despejado",
    1: "mayormente despejado",
    2: "parcialmente nublado",
    3: "nublado",
    45: "niebla",
    48: "niebla con escarcha",
    51: "llovizna ligera",
    53: "llovizna moderada",
    55: "llovizna intensa",
    61: "lluvia ligera",
    63: "lluvia moderada",
    65: "lluvia intensa",
    71: "nieve ligera",
    73: "nieve moderada",
    75: "nieve intensa",
    80: "chubascos ligeros",
    81: "chubascos moderados",
    82: "chubascos fuertes",
    95: "tormenta",
    96: "tormenta con granizo",
}


# ---------------------------------------------------------------- utilidades
def e(texto):
    return html.escape(texto or "", quote=True)


def leer(ruta):
    return io.open(ruta, encoding="utf-8").read()


def escribir(ruta, texto):
    io.open(ruta, "w", encoding="utf-8", newline="\n").write(texto)


def sin_md(texto):
    texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto or "")
    texto = re.sub(r"`(.+?)`", r"\1", texto)
    return texto.strip()


def md(texto):
    """Escapa y convierte el Markdown en línea que usan las fichas."""
    texto = e(texto)
    texto = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" rel="noopener">\1</a>',
        texto,
    )
    texto = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"`([^`]+)`", r"<code>\1</code>", texto)
    return texto


def mayuscula(texto):
    texto = (texto or "").strip()
    if not texto:
        return texto
    return texto[0].upper() + texto[1:]


# ------------------------------------------------------------------ parser
def separar_frontmatter(texto):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", texto, re.S)
    datos = {}
    for linea in m.group(1).splitlines():
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            datos[clave.strip()] = valor.strip()
    return datos, texto[m.end():]


def separar_secciones(cuerpo):
    cabeceras = list(re.finditer(r"^## (\d+)\. (.+)$", cuerpo, re.M))
    secciones = {}
    for i, cab in enumerate(cabeceras):
        inicio = cab.end()
        fin = cabeceras[i + 1].start() if i + 1 < len(cabeceras) else len(cuerpo)
        secciones[int(cab.group(1))] = (cab.group(2).strip(), cuerpo[inicio:fin])
    return secciones


def lista_puntos(bloque):
    puntos, actual = [], None
    for cruda in bloque.splitlines():
        linea = cruda.rstrip()
        if linea.startswith("- "):
            if actual:
                puntos.append(actual)
            actual = linea[2:].strip()
        elif linea.startswith("  ") and actual and linea.strip():
            actual += " " + linea.strip()
        elif not linea.strip():
            if actual:
                puntos.append(actual)
                actual = None
        else:
            if actual:
                puntos.append(actual)
                actual = None
    if actual:
        puntos.append(actual)
    return puntos


def pares_puntos(bloque):
    salida = []
    for punto in lista_puntos(bloque):
        m = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", punto)
        if m:
            salida.append((m.group(1).strip(), sin_md(m.group(2))))
        else:
            salida.append((None, sin_md(punto)))
    return salida


def parrafos_negrita(bloque):
    pares, clave = [], None
    for cruda in bloque.splitlines():
        linea = cruda.rstrip()
        if not linea.strip() or linea.startswith("|") or linea.startswith("> "):
            continue
        m = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", linea)
        if m:
            clave = m.group(1).strip()
            pares.append([clave, sin_md(m.group(2))])
        elif clave:
            pares[-1][1] += " " + sin_md(linea)
    return {k: v for k, v in pares}


def tabla(bloque):
    filas, cabecera = [], None
    for linea in bloque.splitlines():
        if not linea.strip().startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in celdas):
            continue
        if cabecera is None:
            cabecera = celdas
            continue
        filas.append(dict(zip(cabecera, celdas)))
    return filas


def texto_citas(bloque):
    lineas = [l.lstrip("> ").strip() for l in bloque.splitlines() if l.startswith(">")]
    return " ".join(x for x in lineas if x)


def texto_libre(bloque):
    """Párrafos y notas fuera de tablas y listas."""
    trozos = []
    for cruda in bloque.splitlines():
        linea = cruda.strip()
        if not linea or linea.startswith("|") or linea.startswith("###"):
            continue
        if linea.startswith(">"):
            continue
        trozos.append(linea)
    texto = " ".join(trozos)
    return re.sub(r"\s+", " ", texto).strip()


def paradas_detalle(bloque):
    partes = re.split(r"^### ", bloque, flags=re.M)[1:]
    salida = []
    for parte in partes:
        primera, _, resto = parte.partition("\n")
        m = re.match(r"(\d+)\.\s*(.+)", primera.strip())
        if not m:
            continue
        campos = {}
        for clave, valor in pares_puntos(resto):
            if clave:
                campos[clave] = valor
        salida.append({"n": int(m.group(1)), "nombre": m.group(2).strip(), "campos": campos})
    return salida


def fuentes(bloque):
    salida = []
    for punto in lista_puntos(bloque):
        m = re.match(r"^(.*?)\s*:\s*(https?://\S+)$", punto)
        if m:
            salida.append({"titulo": sin_md(m.group(1)).strip(), "url": m.group(2)})
        else:
            m = re.match(r"^(.*?)\s*(https?://\S+)$", punto)
            if m:
                salida.append({"titulo": sin_md(m.group(1)).strip() or m.group(2), "url": m.group(2)})
    return salida


def extension_foto(city_id, n):
    carpeta = os.path.join(FOTOS, city_id)
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        if os.path.exists(os.path.join(carpeta, f"{n:02d}{ext}")):
            return f"{n:02d}{ext}"
    return None


def dimensiones_foto(ruta):
    try:
        from PIL import Image  # opcional: solo para reservar el espacio exacto

        with Image.open(ruta) as im:
            return im.size
    except Exception:
        return (1200, 800)


def duracion_wav(ruta):
    try:
        with wave.open(ruta) as w:
            return w.getnframes() / float(w.getframerate())
    except Exception:
        return None


def duracion_audio(ruta):
    """Duración en segundos.

    Para MP3 se usa el WAV de origen con el mismo nombre si sigue disponible;
    así la ficha conserva la duración aunque el archivo publicado sea MP3.
    """
    if not ruta:
        return None
    if ruta.lower().endswith(".wav"):
        return duracion_wav(ruta)
    if ruta.lower().endswith(".mp3"):
        return duracion_wav(os.path.splitext(ruta)[0] + ".wav")
    return None


def mmss(segundos):
    segundos = int(round(segundos))
    return f"{segundos // 60}:{segundos % 60:02d}"


def enlaces_fotos():
    """Devuelve {(ciudad, archivo): url de la ficha en Commons}."""
    ruta = os.path.join(BASE, "creditos-fotos.md")
    if not os.path.exists(ruta):
        return {}
    salida, ciudad = {}, None
    for linea in leer(ruta).splitlines():
        if linea.startswith("## "):
            ciudad = linea[3:].strip()
        elif linea.startswith("| ") and "http" in linea:
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if len(celdas) >= 5 and celdas[0] != "Uso":
                salida[(ciudad, celdas[1])] = celdas[4]
    return salida


# ------------------------------------------------------------------- datos
def cargar_ciudad(city_id, nombre, guiones, enlaces):
    fm, cuerpo = separar_frontmatter(leer(os.path.join(CONTENIDO, city_id + ".md")))
    sec = separar_secciones(cuerpo)

    ficha_txt = sec[1][1]
    lineas = ficha_txt.splitlines()
    intro, en_lista = [], False
    for linea in lineas:
        if linea.startswith("- "):
            en_lista = True
        if not en_lista and linea.strip():
            intro.append(linea.strip())
    resumen = re.sub(r"\s+", " ", " ".join(intro)).strip()
    datos = dict(pares_puntos(ficha_txt))

    accesibilidad = [
        {
            "campo": f.get("Campo", ""),
            "valor": f.get("Valor", ""),
            "fuente": f.get("Fuente", ""),
            "estado": f.get("Estado", ""),
        }
        for f in tabla(sec[2][1])
        if f.get("Campo") and f.get("Campo") != "Campo"
    ]
    accesibilidad_nota = texto_libre(sec[2][1])

    ruta_txt = sec[3][1]
    ruta = parrafos_negrita(ruta_txt)
    tabla_paradas = tabla(ruta_txt)
    detalles = {p["n"]: p for p in paradas_detalle(sec[4][1])}

    paradas = []
    for fila in tabla_paradas:
        try:
            n = int(fila.get("#", "0"))
        except ValueError:
            continue
        coords = fila.get("Coordenadas", "")
        lat = lon = None
        m = re.match(r"(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)", coords)
        if m:
            lat, lon = m.group(1), m.group(2)
        detalle = detalles.get(n, {"nombre": fila.get("Parada", ""), "campos": {}})
        parada = {
            "n": n,
            "nombre": fila.get("Parada", detalle["nombre"]),
            "tiempo": fila.get("Tiempo", ""),
            "acceso": fila.get("Acceso", ""),
            "estado": fila.get("Estado", ""),
            "lat": lat,
            "lon": lon,
            "detalle": detalle["campos"],
        }
        audio = next((g for g in guiones if g["city"] == city_id and g["index"] == n), None)
        if audio:
            nombre_audio = archivo_audio(city_id, n)
            ruta_audio = (
                os.path.join(AUDIO_SRC, city_id, nombre_audio)
                if nombre_audio
                else None
            )
            segundos = duracion_audio(ruta_audio) if ruta_audio else None
            parada["audio"] = {
                "titulo": audio["title"],
                "texto": audio["text"],
                "archivo": (
                    f"audio/{city_id}/{nombre_audio}"
                    if nombre_audio
                    else f"audio/{city_id}/{n:02d}{EXT_AUDIO[0]}"
                ),
                "duracion": mmss(segundos) if segundos is not None else "",
                "tamano": (
                    f"{os.path.getsize(ruta_audio) / 1048576:.1f} MB".replace(".", ",")
                    if ruta_audio and os.path.exists(ruta_audio)
                    else ""
                ),
            }
        paradas.append(parada)

    clima_pares = {}
    for clave, valor in pares_puntos(sec[6][1]):
        if clave:
            clima_pares[clave] = valor
    m_fuente = re.search(r"\*\*Fuente:\*\*\s*(.+)", sec[6][1])
    clima = {
        "ahora": clima_pares.get("Ahora", ""),
        "hoy": clima_pares.get("Hoy", ""),
        "manana": clima_pares.get("Mañana", ""),
        "pasado": clima_pares.get("Pasado", ""),
        "fuente": sin_md(m_fuente.group(1)) if m_fuente else "",
        "nota": texto_citas(sec[6][1]),
    }

    emergencias = tabla(sec[7][1])
    emergencias = [f for f in emergencias if f.get("Categoría") and f.get("Nombre")]
    nota_emergencias = texto_libre(sec[7][1])
    nota_emergencias = re.sub(r"^\*\*(Nota|Aviso):\*\*\s*", "", nota_emergencias)

    parking_filas = tabla(sec[8][1])
    parking = {
        "intro": texto_libre(sec[8][1]).split("**Nota:**")[0].split("**Aviso:**")[0].strip(),
        "filas": [
            f for f in parking_filas
            if f.get("Nombre") and f.get("Nombre") not in ("Sin datos OSM",)
        ],
        "nota": (
            texto_libre(sec[8][1]).split("**Nota:**")[-1].split("**Aviso:**")[-1].strip()
            if ("**Nota:**" in sec[8][1] or "**Aviso:**" in sec[8][1])
            else ""
        ),
    }

    transporte = {
        "filas": [f for f in tabla(sec[9][1]) if f.get("Modo")],
        "notas": [t for t in pares_puntos(sec[9][1]) if t[1]],
    }

    fotos = []
    idx_foto = 0
    for fila in tabla(sec[10][1]):
        if not fila.get("Archivo"):
            continue
        idx_foto += 1
        archivo = fila["Archivo"]
        ext = extension_foto(city_id, idx_foto)
        autor = fila.get("Autor", "")
        licencia = fila.get("Licencia", "")
        ruta_foto = f"assets/fotos/{city_id}/{ext}" if ext else None
        ancho, alto = (
            dimensiones_foto(os.path.join(SITIO, ruta_foto))
            if ruta_foto
            else (1200, 800)
        )
        fotos.append(
            {
                "uso": fila.get("Uso", ""),
                "archivo": archivo,
                "autor": autor,
                "licencia": licencia,
                "alt": fila.get("Alt", "") or fila.get("Uso", ""),
                "ruta": ruta_foto,
                "ancho": ancho,
                "alto": alto,
                "enlace": enlaces.get((nombre, archivo), ""),
                "credito": f"Fotografía: {autor}, {licencia}, Wikimedia Commons",
            }
        )

    checklist = []
    if 12 in sec:
        checklist = [
            sin_md(m.group(1)).strip()
            for m in re.finditer(r"^-\s*\[[ xX]\]\s*(.+)$", sec[12][1], re.M)
            if m.group(1).strip()
        ]

    fichas = {"intro": "", "fuentes": "", "filas": [], "notas": []}
    if 13 in sec:
        bloque = sec[13][1]
        m_fuentes = re.search(r"\*\*Fuentes:\*\*\s*(.+)", bloque)
        fichas["fuentes"] = m_fuentes.group(1).strip() if m_fuentes else ""
        fichas["intro"] = texto_libre(bloque.split("**Fuentes:**")[0])
        fichas["filas"] = [
            f for f in tabla(bloque) if f.get("Monumento")
        ]
        if "**Notas:**" in bloque:
            fichas["notas"] = [
                n for n in lista_puntos(bloque.split("**Notas:**", 1)[1]) if n
            ]

    return {
        "id": city_id,
        "nombre": fm.get("nombre", nombre),
        "provincia": fm.get("provincia", ""),
        "comunidad": fm.get("comunidad", ""),
        "unesco": fm.get("unesco_desde", ""),
        "lat": fm.get("lat", ""),
        "lon": fm.get("lon", ""),
        "resumen": resumen,
        "frase": re.split(r"(?<=[.!?])\s", resumen)[0] if resumen else "",
        "datos": datos,
        "accesibilidad": accesibilidad,
        "accesibilidad_nota": accesibilidad_nota,
        "ruta": ruta,
        "paradas": paradas,
        "clima": clima,
        "emergencias": emergencias,
        "nota_emergencias": nota_emergencias,
        "parking": parking,
        "transporte": transporte,
        "fotos": fotos,
        "fuentes": fuentes(sec[11][1]),
        "checklist": checklist,
        "fichas": fichas,
        "audio": [g for g in guiones if g["city"] == city_id],
    }


# ------------------------------------------------------------------ render
def logo_en_linea():
    """Devuelve el lockup SVG con la clase que aplica el tamaño de cabecera."""
    with io.open(
        os.path.join(SITIO, "assets", "logo.svg"), encoding="utf-8"
    ) as archivo:
        svg = archivo.read().strip()
    return svg.replace(
        "<svg ",
        '<svg class="marca__logo" focusable="false" ',
        1,
    )


def cabecera(pagina, prefijo=""):
    def activo(clave):
        return ' aria-current="page"' if pagina == clave else ""

    return f"""<a class="salto" href="#contenido">Saltar al contenido</a>
<header class="cabecera">
  <div class="contenedor cabecera__interior">
    <a class="marca" href="{prefijo}index.html">
      {logo_en_linea()}
    </a>
    <nav class="nav" aria-label="Navegación principal">
      <a href="{prefijo}index.html#ciudades"{activo('ciudades')}>Ciudades</a>
      <a href="{prefijo}accesibilidad.html"{activo('accesibilidad')}>Accesibilidad</a>
      <a href="{prefijo}creditos.html"{activo('creditos')}>Créditos</a>
    </nav>
    <a class="boton-112" href="tel:112">
      <span class="boton-112__texto">Emergencias</span>
      <span class="boton-112__num">112</span>
    </a>
  </div>
</header>"""


def pie(prefijo=""):
    return f"""<footer class="pie">
  <div class="contenedor pie__interior">
    <div>
      <p class="pie__marca">Legado a Tu Paso</p>
      <p class="pie__claim">Turismo accesible en ciudades Patrimonio.
      Descúbrelas sin barreras.</p>
    </div>
    <nav class="pie__nav" aria-label="Enlaces del pie">
      <a href="{prefijo}index.html#ciudades">Ciudades</a>
      <a href="{prefijo}accesibilidad.html">Accesibilidad</a>
      <a href="{prefijo}verificacion.html">Verificación</a>
      <a href="{prefijo}creditos.html">Créditos y licencias</a>
    </nav>
    <div class="pie__app">
      <p class="pie__app-titulo">Llévala en el móvil</p>
      <button type="button" class="boton boton--claro" id="instalar-app" hidden>
        Instalar la app
      </button>
      <p class="pie__app-ayuda" id="instalar-ayuda" hidden></p>
      <p class="pie__conexion" id="estado-conexion" role="status" aria-live="polite">
        Comprobando la conexión…
      </p>
    </div>
    <div class="pie__aviso">
      <p><strong>Información orientativa.</strong> Los datos de accesibilidad están
      pendientes de verificación en sitio. Responsable: Natalia Blázquez Herrero.
      Fuentes oficiales consultadas entre el 2 y el 4 de noviembre de 2026.</p>
      <p>Fotos de Wikimedia Commons con autor y licencia. Audio provisional
      generado con voz sintética.</p>
    </div>
  </div>
</footer>"""


_SELLOS = {}


def sello_asset(nombre):
    """Versión corta basada en mtime y tamaño, para invalidar la caché."""
    if nombre not in _SELLOS:
        try:
            st = os.stat(os.path.join(SITIO, "assets", nombre))
            _SELLOS[nombre] = f"{int(st.st_mtime):x}{st.st_size:x}"
        except OSError:
            _SELLOS[nombre] = "0"
    return _SELLOS[nombre]


def documento(titulo, descripcion, cuerpo, pagina, prefijo="", extra_head="",
              leaflet=False, ruta="", imagen="assets/social/og.png",
              noindex=False):
    assets_leaflet = ""
    if leaflet:
        assets_leaflet = (
            f'<link rel="stylesheet" href="{prefijo}assets/leaflet/leaflet.css'
            f'?v={sello_asset("leaflet/leaflet.css")}">\n'
            f'<script src="{prefijo}assets/leaflet/leaflet.js'
            f'?v={sello_asset("leaflet/leaflet.js")}" defer></script>'
        )
    url = f"{SITIO_URL}/{ruta}" if SITIO_URL and ruta else ""
    imagen_url = f"{SITIO_URL}/{imagen}" if SITIO_URL else imagen
    canonical = f'<link rel="canonical" href="{e(url)}">' if url else ""
    og_url = f'<meta property="og:url" content="{e(url)}">' if url else ""
    robots = (
        '<meta name="robots" content="noindex,nofollow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<meta name="theme-color" content="#FAF9F7">
<meta name="color-scheme" content="light">
<meta name="application-name" content="Legado a Tu Paso">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Legado">
{robots}
{canonical}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Legado a Tu Paso">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
{og_url}
<meta property="og:image" content="{e(imagen_url)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Legado a Tu Paso: turismo accesible en ciudades Patrimonio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(titulo)}">
<meta name="twitter:description" content="{e(descripcion)}">
<meta name="twitter:image" content="{e(imagen_url)}">
<link rel="icon" href="{prefijo}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{prefijo}favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{prefijo}assets/iconos/apple-touch-icon.png">
<link rel="manifest" href="{prefijo}manifest.webmanifest">
<link rel="preload" href="{prefijo}assets/fuente/atkinson-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefijo}assets/fuente/literata-600-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefijo}assets/estilos.css?v={sello_asset('estilos.css')}">
{assets_leaflet}
{extra_head}
</head>
<body>
{cabecera(pagina, prefijo)}
<p class="aviso-conexion" id="aviso-conexion" role="status" hidden>
  Sin conexión. Las guías descargadas y sus audios siguen disponibles; el mapa
  y el tiempo no se actualizan.
</p>
<main id="contenido">
{cuerpo}
</main>
{pie(prefijo)}
<script src="{prefijo}assets/app.js?v={sello_asset('app.js')}" defer></script>
</body>
</html>
"""


def migas(ciudad):
    return f"""<nav class="migas contenedor" aria-label="Migas de pan">
  <ol>
    <li><a href="index.html">Inicio</a></li>
    <li><a href="index.html#ciudades">Ciudades</a></li>
    <li aria-current="page">{e(ciudad['nombre'])}</li>
  </ol>
</nav>"""


def chips_datos(ciudad):
    piezas = []
    for clave in ("Tiempo recomendado", "Mejor momento"):
        if ciudad["datos"].get(clave):
            piezas.append(
                f'<div class="dato"><dt>{e(clave)}</dt>'
                f'<dd>{md(mayuscula(ciudad["datos"][clave]))}</dd></div>'
            )
    return f'<dl class="datos-clave">{"".join(piezas)}</dl>'


def aviso_ciudad(ciudad):
    texto = ciudad["datos"].get(
        "Aviso",
        "Información orientativa. Pendiente de verificación en sitio.",
    )
    return f"""<aside class="aviso" aria-label="Aviso sobre la información">
  <p><strong>Antes de viajar.</strong> {md(mayuscula(texto))}</p>
  <p><strong>Verificación en sitio pendiente.</strong> Responsable: Natalia
  Blázquez Herrero.</p>
</aside>"""


def indice_secciones(ciudad):
    enlaces = [
        ("descarga", "Sin conexión"),
        ("ruta", "Ruta y paradas"),
        ("accesibilidad", "Accesibilidad"),
        ("clima", "Clima"),
        ("emergencias", "Emergencias"),
        ("aparcamiento", "Aparcamiento"),
        ("transporte", "Transporte"),
        ("fotos", "Fotos"),
        ("fuentes", "Fuentes"),
    ]
    if ciudad.get("fichas", {}).get("filas"):
        enlaces.insert(1, ("fichas", "Fichas de monumento"))
    items = "".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in enlaces)
    return f"""<nav class="indice" aria-label="Secciones de esta guía">
  <h2 class="indice__titulo">En esta guía</h2>
  <ul>{items}</ul>
</nav>"""


def bloque_ruta(ciudad):
    ruta = ciudad["ruta"]
    base = ruta.get("Ruta base", "")
    m = re.match(r"([\d.,]+\s*km[^,.;]*)", base)
    distancia = m.group(1) if m else base
    datos = [
        ("Distancia", distancia),
        ("Superficie", ruta.get("Superficie", "")),
        ("Desnivel", ruta.get("Desnivel", "")),
    ]
    filas = "".join(
        f'<div class="dato"><dt>{e(k)}</dt><dd>{md(mayuscula(v))}</dd></div>'
        for k, v in datos
        if v
    )
    variante = ""
    for clave, valor in ruta.items():
        if clave.startswith("Variante") or clave.startswith("En total"):
            variante += f"<p><strong>{e(clave)}:</strong> {md(mayuscula(valor))}</p>"
    alternativa = (
        f'<div class="alternativa"><h3>Alternativa de acceso</h3>'
        f'<p>{md(mayuscula(ruta.get("Alternativa", "")))}</p></div>'
        if ruta.get("Alternativa")
        else ""
    )
    return f"""<section id="ruta" class="seccion" aria-labelledby="t-ruta">
  <h2 id="t-ruta">Ruta y paradas</h2>
  <p class="entradilla">{e(ruta.get("Ruta base", ""))}</p>
  <dl class="datos-clave">{filas}</dl>
  {variante}
  {alternativa}
  {bloque_mapa(ciudad)}
</section>"""


def bloque_mapa(ciudad):
    puntos = [
        f'<li><span class="mapa__num">{p["n"]}</span>'
        f'<a href="https://www.openstreetmap.org/?mlat={p["lat"]}&amp;mlon={p["lon"]}#map=19/{p["lat"]}/{p["lon"]}"'
        f' rel="noopener">{e(p["nombre"])}</a>'
        f'<span class="mapa__coords">{e(p["lat"])}, {e(p["lon"])}</span></li>'
        for p in ciudad["paradas"]
        if p["lat"] and p["lon"]
    ]
    datos = {
        "centro": [float(ciudad["lat"]), float(ciudad["lon"])],
        "paradas": [
            {
                "n": p["n"],
                "nombre": p["nombre"],
                "lat": float(p["lat"]),
                "lon": float(p["lon"]),
            }
            for p in ciudad["paradas"]
            if p["lat"] and p["lon"]
        ],
    }
    datos_json = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    destino = f'{ciudad["lat"]},{ciudad["lon"]}'
    return f"""<div class="mapa" role="group" aria-labelledby="t-mapa">
  <h3 id="t-mapa">Mapa de la ruta</h3>
  <p class="mapa__nota">Mapa interactivo con Leaflet y cartografía de
  OpenStreetMap. Las paradas están numeradas en el mismo orden que el recorrido.
  Los marcadores son una referencia visual; la lista de abajo es la alternativa
  navegable, con coordenadas y enlaces al mapa.</p>
  <div class="mapa-marco">
    <div class="mapa-leaflet" id="mapa-ruta" role="region"
         aria-label="Mapa del recorrido por {e(ciudad['nombre'])}"></div>
  </div>
  <p class="mapa__leyenda"><span class="punto-mapa" aria-hidden="true"></span>
  Paradas de la ruta, en orden.</p>
  <ol class="mapa__lista">{"".join(puntos)}</ol>
  <p class="mapa__acciones">
    <a class="boton boton--secundario" href="https://www.google.com/maps/dir/?api=1&amp;destination={destino}" rel="noopener">
      Indicaciones en Google Maps</a>
    <a class="boton boton--secundario" href="https://www.openstreetmap.org/directions?to={destino}#map=15/{ciudad['lat']}/{ciudad['lon']}" rel="noopener">
      Indicaciones en OpenStreetMap</a>
  </p>
  <p class="mapa__letra">La cartografía puede no reflejar obras recientes. Para la
  accesibilidad, vale la lista de paradas y la ficha de cada una.</p>
</div>
<script type="application/json" id="mapa-ruta-datos">{datos_json}</script>"""


def bloque_paradas(ciudad):
    salida = []
    for p in ciudad["paradas"]:
        detalle = p["detalle"]
        campos = []
        for clave in ("Qué es", "Por qué importa", "Acceso"):
            if detalle.get(clave):
                campos.append(
                    f'<div class="parada__campo"><h4>{e(clave)}</h4>'
                    f'<p>{md(mayuscula(detalle[clave]))}</p></div>'
                )
        for clave in ("Alternativa", "Aseo adaptado"):
            if detalle.get(clave):
                campos.append(
                    f'<div class="parada__campo"><h4>{e(clave)}</h4>'
                    f'<p>{md(mayuscula(detalle[clave]))}</p></div>'
                )
        audio = p.get("audio")
        bloque_audio = ""
        if audio:
            meta_audio = " · ".join(
                parte
                for parte in (
                    audio["duracion"],
                    audio["tamano"],
                    "voz sintética provisional",
                )
                if parte
            )
            bloque_audio = f"""<div class="audio">
  <p class="audio__titulo">Audio de la parada</p>
  <audio controls preload="none" src="{audio['archivo']}"
         aria-label="Audio de la parada {p['n']}: {e(p['nombre'])}">
    Tu navegador no reproduce audio. Puedes <a href="{audio['archivo']}">descargar el archivo</a>.
  </audio>
  <p class="audio__meta">{meta_audio}</p>
  <details class="transcripcion">
    <summary>Leer la transcripción</summary>
    <p>{e(audio['texto'])}</p>
  </details>
  <p class="audio__descarga"><a href="{audio['archivo']}" download>Descargar audio</a></p>
</div>"""
        coords = ""
        if p["lat"]:
            coords = (
                f'<div><dt>Coordenadas</dt><dd>'
                f'<a href="https://www.openstreetmap.org/?mlat={p["lat"]}&amp;mlon={p["lon"]}#map=19/{p["lat"]}/{p["lon"]}"'
                f' rel="noopener">{e(p["lat"])}, {e(p["lon"])}</a></dd></div>'
            )
        salida.append(f"""<article class="parada" id="p{p['n']}">
  <header class="parada__cabecera">
    <p class="parada__numero" aria-hidden="true">{p['n']:02d}</p>
    <h3 class="parada__titulo"><span class="sr-only">Parada {p['n']}: </span>{e(p['nombre'])}</h3>
  </header>
  <dl class="parada__datos">
    <div><dt>Tiempo</dt><dd>{e(p['tiempo'])}</dd></div>
    <div><dt>Acceso</dt><dd>{e(p['acceso'])}</dd></div>
    {coords}
  </dl>
  <div class="parada__texto">{''.join(campos)}</div>
  {bloque_audio}
</article>""")
    return "".join(salida)


CORTOS = {"112", "061", "062", "080", "085", "091", "092"}


def celda_telefono(valor, estado, solo_verificados):
    """Enlaza teléfonos. En urgencias solo publica números contrastados."""
    partes = [p.strip() for p in re.split(r"\s*[·/]\s*", valor) if p.strip()]
    enlaces, ocultos = [], 0
    for parte in partes:
        digitos = re.sub(r"\D", "", parte)
        if not digitos:
            continue
        if (
            not solo_verificados
            or estado == "verificado"
            or (len(digitos) == 3 and digitos in CORTOS)
        ):
            enlaces.append(f'<a href="tel:{digitos}">{e(parte)}</a>')
        else:
            ocultos += 1
    if ocultos:
        enlaces.append('<span class="marca-estado">local por confirmar</span>')
    return " · ".join(enlaces) or "—"


def celda_enlace(valor):
    valor = (valor or "").strip()
    if not valor or valor == "—":
        return e(valor)
    if valor.startswith("http://") or valor.startswith("https://"):
        url, texto = valor, re.sub(r"^https?://(www\.)?", "", valor).rstrip("/")
    else:
        url, texto = "https://" + valor, valor
    return f'<a href="{e(url)}" rel="noopener">{e(texto)}</a>'


PISTA_TABLA = (
    '<p class="pista-tabla" aria-hidden="true" hidden>Las tablas de esta página '
    "se desplazan en horizontal: desliza o usa las flechas del teclado.</p>"
)


def audios_publicados(city_id):
    """Devuelve {número de parada: archivo} con un solo formato por audio.

    Se publica el primer formato disponible según EXT_AUDIO: MP3 antes que WAV,
    para no duplicar el peso de los audios en el sitio.
    """
    carpeta = os.path.join(AUDIO_SRC, city_id)
    elegidos = {}
    if not os.path.isdir(carpeta):
        return elegidos

    for nombre in os.listdir(carpeta):
        base, ext = os.path.splitext(nombre)
        ext = ext.lower()
        if not base.isdigit() or ext not in EXT_AUDIO:
            continue
        numero = int(base)
        actual = elegidos.get(numero)
        if actual is None:
            elegidos[numero] = nombre
            continue
        prioridad_actual = EXT_AUDIO.index(os.path.splitext(actual)[1].lower())
        if EXT_AUDIO.index(ext) < prioridad_actual:
            elegidos[numero] = nombre

    return elegidos


def archivo_audio(city_id, n):
    """Nombre del audio de una parada; MP3 si existe, si no WAV."""
    return audios_publicados(city_id).get(n)


def tabla_html(filas, columnas, clases="", etiqueta="Tabla de datos",
               solo_verificados=False):
    if not filas:
        return ""
    cab = "".join(f"<th scope=\"col\">{e(c)}</th>" for c in columnas.values())
    cuerpo = ""
    for fila in filas:
        estado_fila = (fila.get("Estado") or "").strip()
        celdas = []
        for clave in columnas:
            valor = fila.get(clave, "") or ""
            if clave == "Teléfono":
                celdas.append(
                    f"<td>{celda_telefono(valor, estado_fila, solo_verificados)}</td>"
                )
            elif clave == "Contacto" and re.fullmatch(r"[\d\s+·/]+", valor):
                celdas.append(
                    f"<td>{celda_telefono(valor, estado_fila, False)}</td>"
                )
            elif clave == "Enlace":
                celdas.append(f"<td>{celda_enlace(valor)}</td>")
            elif clave == "Estado":
                if valor and valor != "verificado":
                    celdas.append(
                        f'<td><span class="marca-estado">{e(valor)}</span></td>'
                    )
                else:
                    celdas.append(f"<td>{e(valor)}</td>")
            else:
                celdas.append(f"<td>{md(valor)}</td>")
        cuerpo += "<tr>" + "".join(celdas) + "</tr>"
    return f"""<div class="tabla-envoltorio" tabindex="0" role="region" aria-label="{e(etiqueta)}">
  <table class="{clases}">
    <caption class="sr-only">{e(etiqueta)}</caption>
    <thead><tr>{cab}</tr></thead>
    <tbody>{cuerpo}</tbody>
  </table>
</div>
{PISTA_TABLA}"""


def bloque_accesibilidad(ciudad):
    filas = ciudad["accesibilidad"]
    tabla_filas = [
        {
            "Campo": f.get("campo", ""),
            "Valor": f.get("valor", ""),
            "Fuente": f.get("fuente", ""),
            "Estado": f.get("estado", ""),
        }
        for f in filas
    ]
    nota = ciudad.get("accesibilidad_nota", "")
    nota_html = f'  <p class="nota">{md(nota)}</p>\n' if nota else ""
    return f"""<section id="accesibilidad" class="seccion" aria-labelledby="t-acc">
  <h2 id="t-acc">Accesibilidad</h2>
  <p class="entradilla">Datos recogidos de fuentes oficiales y de OpenStreetMap.
  La columna «Estado» indica si el dato está verificado en sitio.</p>
  {tabla_html(tabla_filas, {'Campo':'Campo','Valor':'Valor','Fuente':'Fuente','Estado':'Estado'}, etiqueta='Accesibilidad en ' + ciudad['nombre'])}
{nota_html}</section>"""


def bloque_fichas(ciudad):
    fichas = ciudad.get("fichas") or {}
    if not fichas.get("filas"):
        return ""
    columnas = {
        "Monumento": "Monumento",
        "Ámbito": "Ámbito",
        "Dato": "Dato",
        "Valor": "Valor",
        "Fuente": "Fuente y fecha",
        "Estado": "Estado",
    }
    notas = "".join(f"<li>{md(n)}</li>" for n in fichas.get("notas", []))
    return f"""<section id="fichas" class="seccion" aria-labelledby="t-fichas">
  <h2 id="t-fichas">Fichas de monumento</h2>
  {f'<p class="entradilla">{md(fichas["intro"])}</p>' if fichas.get("intro") else ''}
  {f'<p class="fichas__fuentes">{md(fichas["fuentes"])}</p>' if fichas.get("fuentes") else ''}
  {tabla_html(fichas["filas"], columnas, etiqueta='Fichas de monumento de ' + ciudad['nombre'])}
  {f'<div class="nota fichas__notas"><h3>Notas de la ficha</h3><ul>{notas}</ul></div>' if notas else ''}
</section>"""


def bloque_clima(ciudad):
    clima = ciudad["clima"]
    filas = "".join(
        f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>'
        for k, v in (
            ("Ahora", clima["ahora"]),
            ("Hoy", clima["hoy"]),
            ("Mañana", clima["manana"]),
            ("Pasado mañana", clima["pasado"]),
        )
        if v
    )
    fuente = md(clima["fuente"]) or "Open-Meteo."
    if not fuente.endswith((".", "!", "?")):
        fuente += "."
    return f"""<section id="clima" class="seccion" aria-labelledby="t-clima">
  <h2 id="t-clima">Clima</h2>
  <div class="panel" id="clima-panel" data-lat="{e(ciudad['lat'])}" data-lon="{e(ciudad['lon'])}" data-ciudad="{e(ciudad['nombre'])}">
    <p class="panel__fuente">{fuente}</p>
    <dl class="clima">{filas}</dl>
    <p id="clima-estado" class="panel__estado" role="status"></p>
    <p class="panel__acciones">
      <button class="boton boton--secundario" type="button" id="clima-actualizar">
        Actualizar el tiempo ahora
      </button>
    </p>
    <p class="panel__letra">El tiempo se consulta a Open-Meteo al abrir la
    página y se actualiza cada 5 minutos. La consulta se envía desde tu
    navegador; no se guardan datos personales.</p>
  </div>
  {f'<p class="nota">{md(clima["nota"])}</p>' if clima["nota"] else ''}
</section>"""


def bloque_emergencias(ciudad):
    return f"""<section id="emergencias" class="seccion" aria-labelledby="t-emerg">
  <h2 id="t-emerg">Emergencias</h2>
  <div class="emergencia">
    <p class="emergencia__etiqueta">Emergencias · 24 horas</p>
    <a class="emergencia__tel" href="tel:112">112</a>
    <p>Gratuito desde cualquier teléfono. Funciona sin datos y sin geolocalización.
    Si no puedes hablar, intenta enviar un mensaje o pedir ayuda a alguien cerca.</p>
  </div>
  {tabla_html([
      {'Categoría': f.get('Categoría',''), 'Nombre': f.get('Nombre',''),
       'Teléfono': f.get('Teléfono',''), 'Dirección': f.get('Dirección','') or '—',
       'Estado': f.get('Estado','')}
      for f in ciudad['emergencias']
  ], {'Categoría':'Categoría','Nombre':'Nombre','Teléfono':'Teléfono','Dirección':'Dirección','Estado':'Estado'}, etiqueta='Teléfonos de emergencia de ' + ciudad['nombre'], solo_verificados=True)}
  {f'<p class="nota">{md(mayuscula(ciudad["nota_emergencias"]))}</p>' if ciudad['nota_emergencias'] else ''}
</section>"""


def bloque_aparcamiento(ciudad):
    columnas = {
        "Nombre": "Nombre",
        "Coordenadas": "Coordenadas",
        "Plazas": "Plazas",
        "PMR": "Plazas PMR",
        "Coste": "Coste",
        "Tipo": "Tipo / superficie",
        "Estado": "Estado",
    }
    filas = [
        {
            "Nombre": f.get("Nombre", ""),
            "Coordenadas": f.get("Coordenadas", ""),
            "Plazas": f.get("Plazas", ""),
            "PMR": f.get("PMR", ""),
            "Coste": f.get("Coste", ""),
            "Tipo": f.get("Tipo") or f.get("Superficie", ""),
            "Estado": f.get("Estado", ""),
        }
        for f in ciudad["parking"]["filas"]
    ]
    if filas:
        cuerpo = tabla_html(filas, columnas, etiqueta="Aparcamientos de " + ciudad["nombre"])
    else:
        cuerpo = ('<p class="vacio">No hay datos de aparcamiento adaptado en '
                  'OpenStreetMap para esta ciudad. No inventamos plazas: consulta '
                  'la web municipal de movilidad antes de viajar.</p>')
    return f"""<section id="aparcamiento" class="seccion" aria-labelledby="t-park">
  <h2 id="t-park">Aparcamiento accesible</h2>
  {f'<p class="entradilla">{md(ciudad["parking"]["intro"])}</p>' if ciudad['parking']['intro'] else ''}
  {cuerpo}
  {f'<p class="nota">{md(mayuscula(ciudad["parking"]["nota"]))}</p>' if ciudad['parking']['nota'] else ''}
</section>"""


def bloque_transporte(ciudad):
    columnas = {
        "Modo": "Modo",
        "Operador": "Operador",
        "Accesibilidad": "Accesibilidad",
        "Contacto": "Contacto",
        "Enlace": "Enlace",
        "Tiempo real": "Tiempo real",
    }
    cuerpo = tabla_html(
        ciudad["transporte"]["filas"],
        columnas,
        etiqueta="Transporte accesible en " + ciudad["nombre"],
    )
    notas = "".join(
        f'<p><strong>{e(k)}:</strong> {md(mayuscula(v))}</p>'
        for k, v in ciudad["transporte"]["notas"]
        if k
    )
    return f"""<section id="transporte" class="seccion" aria-labelledby="t-trans">
  <h2 id="t-trans">Transporte accesible</h2>
  {cuerpo}
  <div class="nota">{notas}</div>
</section>"""


def bloque_fotos(ciudad):
    figuras = []
    for f in ciudad["fotos"]:
        if not f["ruta"]:
            continue
        credito = (
            f"Fotografía: {e(f['autor'])}, {e(f['licencia'])}, "
        )
        if f["enlace"]:
            credito += (
                f'<a href="{e(f["enlace"])}" rel="noopener">'
                "Wikimedia Commons</a>"
            )
        else:
            credito += "Wikimedia Commons"
        figuras.append(f"""<figure class="foto">
  <img src="{f['ruta']}" alt="{e(f['alt'])}" loading="lazy" decoding="async"
       width="{f['ancho']}" height="{f['alto']}">
  <figcaption>
    <span class="foto__uso">{e(f['uso'])}</span>
    <span class="foto__credito">{credito}</span>
  </figcaption>
</figure>""")
    return f"""<section id="fotos" class="seccion" aria-labelledby="t-fotos">
  <h2 id="t-fotos">Fotos</h2>
  <p class="entradilla">Imágenes de Wikimedia Commons con licencia libre. El
  crédito aparece bajo cada foto y en la página de <a href="creditos.html">créditos</a>.</p>
  <div class="galeria">{''.join(figuras)}</div>
</section>"""


def bloque_fuentes(ciudad):
    items = "".join(
        f'<li><a href="{e(f["url"])}" rel="noopener">{e(f["titulo"])}</a></li>'
        for f in ciudad["fuentes"]
    )
    return f"""<section id="fuentes" class="seccion" aria-labelledby="t-fuentes">
  <h2 id="t-fuentes">Fuentes</h2>
  <ul class="fuentes">{items}</ul>
</section>"""


def tamano_recurso(ruta):
    """Tamaño de un recurso del sitio, con respaldo en la carpeta audio/."""
    candidatos = [os.path.join(SITIO, ruta)]
    if ruta.startswith("audio/"):
        candidatos.append(os.path.join(AUDIO_SRC, ruta[len("audio/"):]))
    for candidato in candidatos:
        if os.path.exists(candidato):
            return os.path.getsize(candidato)
    return 0


def bloque_descarga(ciudad):
    """Panel para guardar fotos y audios de una ciudad sin conexión."""
    urls, vistos, total = [], set(), 0
    for foto in ciudad["fotos"]:
        ruta = foto.get("ruta")
        if ruta and ruta not in vistos:
            vistos.add(ruta)
            urls.append(ruta)
            total += tamano_recurso(ruta)
    for parada in ciudad["paradas"]:
        audio = parada.get("audio")
        ruta = audio.get("archivo") if audio else None
        if ruta and ruta not in vistos:
            vistos.add(ruta)
            urls.append(ruta)
            total += tamano_recurso(ruta)
    if not urls:
        return ""

    datos = json.dumps(
        {"ciudad": ciudad["id"], "urls": urls}, ensure_ascii=False
    ).replace("</", "<\\/")
    megas = f"{total / 1048576:.1f}".replace(".", ",")
    return f"""<section id="descarga" class="seccion descarga" aria-labelledby="t-descarga">
  <h2 id="t-descarga">Esta guía sin conexión</h2>
  <p class="descarga__intro">Guarda las fotos y los audios de
  {e(ciudad['nombre'])} ({megas} MB) para consultarlos sin datos. El mapa, el
  tiempo y los enlaces externos necesitan conexión.</p>
  <div class="descarga__acciones">
    <button type="button" class="boton boton--primario" id="descargar-ciudad">
      Descargar esta ciudad
    </button>
    <button type="button" class="boton boton--secundario" id="borrar-descarga" hidden>
      Borrar la descarga
    </button>
  </div>
  <p class="descarga__estado" id="descarga-estado" role="status" aria-live="polite">
    Comprobando si esta guía ya está guardada…
  </p>
  <progress class="descarga__progreso" id="descarga-progreso" max="100"
            value="0" aria-label="Progreso de la descarga" hidden>0 %</progress>
  <p class="descarga__nota">Las fotos y los audios se guardan en este
  dispositivo. Puedes borrarlos cuando quieras con el botón «Borrar la
  descarga».</p>
  <script type="application/json" id="descarga-datos">{datos}</script>
</section>"""


def pagina_ciudad(ciudad):
    titulo = f"{ciudad['nombre']} — guía accesible | Legado a Tu Paso"
    descripcion = (
        f"Guía de turismo accesible en {ciudad['nombre']}: ruta con {len(ciudad['paradas'])} "
        "paradas, audio, clima, emergencias, aparcamiento y transporte."
    )
    cuerpo = f"""{migas(ciudad)}
<article class="ficha contenedor">
  <header class="ficha__cabecera">
    <p class="eyebrow">{e(ciudad['comunidad'])} · Patrimonio de la Humanidad desde {e(ciudad['unesco'])}</p>
    <h1>{e(ciudad['nombre'])}</h1>
    <p class="entradilla grande">{e(ciudad['resumen'])}</p>
    {chips_datos(ciudad)}
  </header>
  {aviso_ciudad(ciudad)}
  {indice_secciones(ciudad)}
  {bloque_descarga(ciudad)}
  {bloque_ruta(ciudad)}
  <div class="paradas-lista">
    <h2 class="sr-only">Paradas de la ruta</h2>
    {bloque_paradas(ciudad)}
  </div>
  {bloque_accesibilidad(ciudad)}
  {bloque_fichas(ciudad)}
  {bloque_clima(ciudad)}
  {bloque_emergencias(ciudad)}
  {bloque_aparcamiento(ciudad)}
  {bloque_transporte(ciudad)}
  {bloque_fotos(ciudad)}
  {bloque_fuentes(ciudad)}
</article>"""
    return documento(titulo, descripcion, cuerpo, "ciudades", leaflet=True,
                     ruta=ciudad["id"] + ".html")


def tarjeta_ciudad(ciudad):
    primera = ciudad["fotos"][0] if ciudad["fotos"] else None
    foto = primera["ruta"] if primera and primera["ruta"] else None
    alt = primera["alt"] if primera else ""
    imagen = (
        f'<img class="tarjeta__foto" src="{foto}" alt="{e(alt)}" loading="lazy" decoding="async" width="{primera["ancho"]}" height="{primera["alto"]}">'
        if foto
        else '<div class="tarjeta__foto tarjeta__foto--vacia" aria-hidden="true"></div>'
    )
    buscable = f"{ciudad['nombre']} {ciudad['provincia']} {ciudad['comunidad']}".lower()
    return f"""<li class="rejilla__item" data-completa="1" data-buscable="{e(buscable)}"
    data-lat="{e(ciudad['lat'])}" data-lon="{e(ciudad['lon'])}">
  <a class="tarjeta" href="{ciudad['id']}.html">
    {imagen}
    <div class="tarjeta__cuerpo">
      <p class="etiqueta etiqueta--completa">Guía completa</p>
      <h3 class="tarjeta__titulo">{e(ciudad['nombre'])}</h3>
      <p class="tarjeta__meta">{e(ciudad['comunidad'])} · UNESCO {e(ciudad['unesco'])}</p>
      <p class="tarjeta__tiempo" hidden></p>
      <p class="tarjeta__texto">{e(ciudad['frase'])}</p>
      <p class="tarjeta__cta">Ver la guía</p>
    </div>
  </a>
</li>"""


def tarjeta_pendiente(c):
    buscable = f"{c['nombre']} {c['provincia']} {c['comunidad']}".lower()
    return f"""<li class="rejilla__item" data-completa="0" data-buscable="{e(buscable)}"
    data-lat="{e(c['lat'])}" data-lon="{e(c['lon'])}">
  <div class="tarjeta tarjeta--pronto">
    <div class="tarjeta__foto tarjeta__foto--vacia" aria-hidden="true"></div>
    <div class="tarjeta__cuerpo">
      <p class="etiqueta etiqueta--pronto">Próximamente</p>
      <h3 class="tarjeta__titulo">{e(c['nombre'])}</h3>
      <p class="tarjeta__meta">{e(c['comunidad'])} · UNESCO {e(c['unesco'])}</p>
      <p class="tarjeta__tiempo" hidden></p>
      <p class="tarjeta__texto">{e(c['texto'])}</p>
      <p class="tarjeta__cta tarjeta__cta--apagada">Guía en preparación</p>
    </div>
  </div>
</li>"""


def pagina_inicio(ciudades):
    tarjetas = "".join(tarjeta_ciudad(c) for c in ciudades) + "".join(
        tarjeta_pendiente(c) for c in PENDIENTES
    )
    total_paradas = sum(len(c["paradas"]) for c in ciudades)
    datos_mapa = [
        {
            "nombre": c["nombre"],
            "comunidad": c["comunidad"],
            "lat": float(c["lat"]),
            "lon": float(c["lon"]),
            "url": c["id"] + ".html",
            "completa": True,
        }
        for c in ciudades
    ] + [
        {
            "nombre": c["nombre"],
            "comunidad": c["comunidad"],
            "lat": float(c["lat"]),
            "lon": float(c["lon"]),
            "url": "",
            "completa": False,
        }
        for c in PENDIENTES
    ]
    datos_mapa_json = json.dumps(datos_mapa, ensure_ascii=False).replace("</", "<\\/")
    cuerpo = f"""<section class="hero">
  <div class="contenedor">
    <p class="eyebrow">Ciudades Patrimonio de la Humanidad</p>
    <h1>Turismo accesible en ciudades Patrimonio</h1>
    <p class="hero__claim">Descúbrelas sin barreras.</p>
    <p class="hero__intro">Guías para recorrer las ciudades patrimonio de España
    con información clara sobre accesibilidad, rutas, audio, clima, emergencias,
    aparcamiento y transporte. Sin promesas que no podamos sostener.</p>
    <div class="hero__acciones">
      <a class="boton boton--primario" href="#ciudades">Ver las ciudades</a>
      <a class="boton boton--secundario" href="accesibilidad.html">Cómo funciona el sitio</a>
    </div>
  </div>
</section>

<section class="cifras" aria-label="El proyecto en cifras">
  <div class="contenedor cifras__interior">
    <div class="cifra"><strong>{len(ciudades)}</strong><span>guías completas</span></div>
    <div class="cifra"><strong>{total_paradas}</strong><span>paradas con audio</span></div>
    <div class="cifra"><strong>{len(ciudades) + len(PENDIENTES)}</strong><span>ciudades en el catálogo</span></div>
  </div>
</section>

<section id="mapa-general" class="seccion contenedor" aria-labelledby="t-mapa-general">
  <div class="seccion__cabecera">
    <h2 id="t-mapa-general">Las 15 ciudades en el mapa</h2>
    <p>El mapa sitúa las guías completas y las que están en preparación. La
    lista de abajo es la alternativa textual: abre cada ficha sin usar el
    mapa.</p>
  </div>
  <div class="mapa-marco mapa-marco--general">
    <div class="mapa-leaflet" id="mapa-ciudades" role="region"
         aria-label="Mapa de las 15 ciudades del catálogo"></div>
  </div>
  <ul class="leyenda-mapa">
    <li><span class="punto-mapa" aria-hidden="true"></span> Guía completa</li>
    <li><span class="punto-mapa punto-mapa--pronto" aria-hidden="true"></span> Próximamente</li>
  </ul>
  <p class="mapa__nota">Cartografía de OpenStreetMap con Leaflet. La lista de
  ciudades que aparece justo debajo es la alternativa textual, con la misma
  información y sin necesidad de usar el mapa.</p>
</section>
<script type="application/json" id="mapa-ciudades-datos">{datos_mapa_json}</script>

<section id="ciudades" class="seccion contenedor" aria-labelledby="t-ciudades">
  <div class="seccion__cabecera">
    <h2 id="t-ciudades">Las 15 ciudades</h2>
    <p>Ocho tienen guía completa. Las otras siete se incorporan en la siguiente
    fase, con el mismo nivel de detalle.</p>
  </div>

  <div class="buscador">
    <label for="buscar">Buscar ciudad, provincia o comunidad</label>
    <input type="search" id="buscar" name="buscar" autocomplete="off"
           placeholder="Ejemplo: Córdoba, Galicia, Jaén">
  </div>

  <div class="filtros" role="group" aria-label="Filtrar por contenido">
    <button type="button" class="chip" data-filtro="todas" aria-pressed="true">Todas (15)</button>
    <button type="button" class="chip" data-filtro="completas" aria-pressed="false">Guía completa ({len(ciudades)})</button>
    <button type="button" class="chip" data-filtro="pendientes" aria-pressed="false">Próximamente ({len(PENDIENTES)})</button>
  </div>

  <p class="resultado" id="resultado" role="status">15 ciudades.</p>
  <p class="tiempo-nota" id="tiempo-estado" role="status">El tiempo actual de
  cada ciudad se carga automáticamente al abrir la página.</p>
  <ul class="rejilla" id="rejilla">{tarjetas}</ul>
  <p class="vacio" id="sin-resultados" hidden>No hay ciudades que coincidan con
  la búsqueda. Prueba con otra palabra.</p>
</section>

<section class="seccion seccion--papel" aria-labelledby="t-como">
  <div class="contenedor">
    <h2 id="t-como">Cómo funciona cada guía</h2>
    <ol class="pasos">
      <li>
        <h3>Elige la ciudad y la ruta</h3>
        <p>Distancia, desnivel, superficie y una alternativa de acceso cuando
        el recorrido completo no es viable.</p>
      </li>
      <li>
        <h3>Escucha o lee cada parada</h3>
        <p>Cada parada tiene audio y transcripción. Nada depende solo del oído ni
        solo de la vista.</p>
      </li>
      <li>
        <h3>Comprueba antes de viajar</h3>
        <p>Clima, emergencias, aparcamiento y transporte, con la fuente y la fecha
        de cada dato.</p>
      </li>
    </ol>
  </div>
</section>

<section class="seccion contenedor" aria-labelledby="t-compromiso">
  <div class="compromiso">
    <h2 id="t-compromiso">Lo que este sitio no hace</h2>
    <ul>
      <li>No dice que un lugar es accesible sin una verificación en sitio.</li>
      <li>No inventa plazas de aparcamiento ni teléfonos locales.</li>
      <li>No promete tiempo real donde no hay una API oficial.</li>
    </ul>
    <p>Cuando un dato está pendiente, lo dice. Esa es la diferencia entre una guía
    útil y un folleto.</p>
  </div>
</section>"""

    return documento(
        "Legado a Tu Paso — Turismo accesible en ciudades Patrimonio",
        "Guías de turismo accesible en las Ciudades Patrimonio de la Humanidad de "
        "España: rutas, audio, clima, emergencias, aparcamiento y transporte.",
        cuerpo,
        "ciudades",
        leaflet=True,
        ruta="index.html",
    )


def pagina_accesibilidad():
    cuerpo = """<div class="contenedor pagina">
  <p class="eyebrow">Compromiso</p>
  <h1>Accesibilidad de este sitio</h1>
  <p class="entradilla grande">El sitio está diseñado para cumplir WCAG 2.2 nivel AA.
  Su estado es <strong>parcialmente conforme</strong>: las comprobaciones
  automáticas están hechas y las manuales son favorables, pero falta una auditoría
  externa y la verificación en sitio de los datos de las guías.</p>

  <section class="seccion" aria-labelledby="t-estado">
    <h2 id="t-estado">Estado de conformidad</h2>
    <dl class="datos-clave">
      <div class="dato"><dt>Referencia</dt><dd>WCAG 2.2 nivel AA</dd></div>
      <div class="dato"><dt>Estado</dt><dd>Parcialmente conforme</dd></div>
      <div class="dato"><dt>Última revisión</dt><dd>7 de noviembre de 2026</dd></div>
      <div class="dato"><dt>Auditoría externa</dt><dd>Pendiente</dd></div>
    </dl>
    <p><strong>Parcialmente conforme</strong> significa que el sitio cumple la
    mayoría de los criterios, pero no todos están comprobados por una persona
    externa o quedan limitaciones documentadas más abajo. No usamos la palabra
    «conforme» ni mostramos un sello que no tengamos.</p>
  </section>

  <section class="seccion" aria-labelledby="t-hecho">
    <h2 id="t-hecho">Lo que ya está resuelto</h2>
    <ul class="lista-check">
      <li>Estructura semántica con un solo <code>h1</code> por página y jerarquía de
      encabezados.</li>
      <li>Enlace «Saltar al contenido» y navegación operable con teclado.</li>
      <li>Foco visible en todos los controles.</li>
      <li>Contraste mínimo de 4,5:1 en texto normal y 3:1 en texto grande.</li>
      <li>Textos alternativos vacíos en imágenes decorativas y crédito visible.</li>
      <li>Transcripción escrita de todos los audios. Ningún audio se reproduce solo.</li>
      <li>Respeto de <code>prefers-reduced-motion</code> y de <code>prefers-contrast</code>.</li>
      <li>Formularios con etiqueta visible y mensajes de estado anunciados.</li>
      <li>El 112 está siempre a un toque desde la cabecera.</li>
      <li>Funciona a 200 % de zoom y en pantallas de 320 px de ancho.</li>
    </ul>
  </section>

  <section class="seccion" aria-labelledby="t-comprobado">
    <h2 id="t-comprobado">Qué se ha comprobado y cómo</h2>
    <div class="tabla-envoltorio" tabindex="0" role="region" aria-label="Comprobaciones de accesibilidad realizadas">
      <table>
        <caption class="sr-only">Comprobaciones automáticas y manuales del sitio</caption>
        <thead>
          <tr><th scope="col">Comprobación</th><th scope="col">Método</th><th scope="col">Resultado</th></tr>
        </thead>
        <tbody>
          <tr><td>Estructura, ids y anclas</td><td>Auditor propio (<code>revisar_sitio.py</code>)</td><td>13 páginas, 0 problemas</td></tr>
          <tr><td>Contraste, nombres accesibles y semántica</td><td>Lighthouse automático</td><td>Puntuación máxima en las páginas revisadas</td></tr>
          <tr><td>Teclado, foco y «saltar al contenido»</td><td>Revisión manual</td><td>Recorrido completo sin ratón</td></tr>
          <tr><td>Zoom al 200 % y 320 px de ancho</td><td>Revisión manual</td><td>Sin contenido cortado</td></tr>
          <tr><td>Modo de contraste y movimiento reducido</td><td>Revisión manual</td><td>Estilos alternativos activos</td></tr>
          <tr><td>Datos de accesibilidad de las guías</td><td>Verificación en sitio</td><td>Pendiente (ver abajo)</td></tr>
        </tbody>
      </table>
    </div>
    <p>La revisión manual la ha hecho el propio equipo, no una persona externa.
    Por eso el estado es parcialmente conforme y no conforme.</p>
  </section>

  <section class="seccion" aria-labelledby="t-pendiente">
    <h2 id="t-pendiente">Limitaciones conocidas</h2>
    <ul class="lista-check lista-check--aviso">
      <li><strong>Mapa interactivo:</strong> Leaflet con cartografía de
      OpenStreetMap, sin clave de API. La misma ruta está siempre en texto, con
      coordenadas y enlaces de indicaciones.</li>
      <li><strong>Fotos:</strong> seleccionadas por título y licencia, sin revisión
      visual humana todavía.</li>
      <li><strong>Audio:</strong> la versión publicada usa voz sintética provisional.
      La versión final será voz humana.</li>
      <li><strong>Datos de accesibilidad:</strong> marcados como pendientes hasta la
      verificación en sitio, a cargo de Natalia Blázquez Herrero. El
      <a href="verificacion.html">plan de verificación</a> reúne lo que falta por
      comprobar en cada ciudad y permite descargar los datos en CSV para el
      trabajo de campo.</li>
      <li><strong>Canal de contacto:</strong> pendiente de definir antes de la
      publicación.</li>
      <li><strong>Auditoría externa:</strong> pendiente. Hasta que se haga, este
      sitio no se presenta como certificado.</li>
    </ul>
  </section>

  <section class="seccion" aria-labelledby="t-campo">
    <h2 id="t-campo">Materiales de verificación</h2>
    <p>La accesibilidad de los monumentos y las calles no se puede prometer desde
    un despacho. Estos documentos sirven para comprobarla sobre el terreno y
    dejar constancia de lo que sigue pendiente:</p>
    <ul class="fuentes">
      <li><a href="verificacion.html">Plan de verificación en sitio</a> —
      imprimible, una página por ciudad.</li>
      <li><a href="verificacion/datos-accesibilidad.csv" download>datos-accesibilidad.csv</a>
      — los 96 datos publicados que hay que confirmar.</li>
      <li><a href="verificacion/tareas.csv" download>tareas.csv</a> — las 69 tareas
      pendientes de las ocho ciudades.</li>
      <li><a href="verificacion/segovia-monumentos.csv" download>segovia-monumentos.csv</a>
      — 46 datos de las fichas oficiales de Segovia.</li>
      <li><a href="verificacion/guia-de-campo.md" download>guia-de-campo.md</a> y
      <a href="verificacion/plantilla-ficha-campo.md" download>plantilla-ficha-campo.md</a>
      — método de medición y ficha imprimible.</li>
    </ul>
    <p class="nota">Mientras no haya fecha, medida y firma, un dato sigue en estado
    <code>pendiente</code>. No se retira el aviso por haber consultado una web.</p>
  </section>

  <section class="seccion" aria-labelledby="t-usar">
    <h2 id="t-usar">Cómo usar la guía con lector de pantalla</h2>
    <p>Cada ciudad tiene un índice de secciones al principio. Los audios son
    controles nativos del navegador: se pueden pausar, retroceder y descargar. La
    transcripción está justo debajo y se abre con el botón «Leer la
    transcripción».</p>
    <p>Los enlaces de coordenadas abren OpenStreetMap. Los teléfonos de emergencia
    son enlaces <code>tel:</code> y funcionan en móvil.</p>
  </section>

  <section class="seccion" aria-labelledby="t-tecnica">
    <h2 id="t-tecnica">Ficha técnica</h2>
    <dl class="datos-clave">
      <div class="dato"><dt>Referencia</dt><dd>WCAG 2.2 nivel AA</dd></div>
      <div class="dato"><dt>Estado</dt><dd>Parcialmente conforme</dd></div>
      <div class="dato"><dt>Sitio</dt><dd>HTML estático, sin rastreo ni cookies</dd></div>
      <div class="dato"><dt>Tipografía</dt><dd>Atkinson Hyperlegible y Literata, licencia OFL</dd></div>
      <div class="dato"><dt>Última revisión</dt><dd>7 de noviembre de 2026</dd></div>
    </dl>
  </section>
</div>"""
    return documento(
        "Accesibilidad del sitio | Legado a Tu Paso",
        "Medidas de accesibilidad del sitio, limitaciones conocidas y ficha técnica.",
        cuerpo,
        "accesibilidad",
        ruta="accesibilidad.html",
    )


def bloque_verificacion(ciudad):
    """Ficha imprimible con los datos que hay que comprobar en el sitio."""
    filas = []
    for a in ciudad["accesibilidad"]:
        estado = a["estado"] or ""
        if estado and estado != "verificado":
            marca = f'<span class="marca-estado">{e(estado)}</span>'
        else:
            marca = e(estado) or "—"
        filas.append(
            "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>"
            '<td class="celda-casilla"><span class="casilla" aria-hidden="true"></span>'
            '<span class="sr-only">Por comprobar: {}</span></td></tr>'.format(
                e(a["campo"]),
                md(a["valor"]) or "—",
                e(a["fuente"]) or "—",
                marca,
                e(a["campo"]),
            )
        )
    tareas = "".join(
        '<li><span class="casilla" aria-hidden="true"></span>'
        f"{md(t)}</li>"
        for t in ciudad["checklist"]
    )
    meta = (
        f"{len(ciudad['paradas'])} paradas · "
        f"{len(ciudad['accesibilidad'])} datos de accesibilidad · "
        f"{len(ciudad['parking']['filas'])} aparcamientos publicados · "
        f"{len(ciudad['checklist'])} tareas"
    )
    return f"""<article class="ficha-verificacion" id="{ciudad['id']}"
     aria-labelledby="v-{ciudad['id']}">
  <header class="ficha-verificacion__cabecera">
    <p class="eyebrow">{e(ciudad['comunidad'])}</p>
    <h2 id="v-{ciudad['id']}">{e(ciudad['nombre'])}</h2>
    <p class="ficha-verificacion__meta">{meta}</p>
  </header>

  <h3>Datos publicados que hay que confirmar</h3>
  <div class="tabla-envoltorio" tabindex="0" role="region"
       aria-label="Datos de accesibilidad de {e(ciudad['nombre'])}">
    <table>
      <caption class="sr-only">Datos de accesibilidad de {e(ciudad['nombre'])}:
      valor publicado, fuente, estado y casilla para marcar la comprobación.</caption>
      <thead>
        <tr>
          <th scope="col">Campo</th>
          <th scope="col">Valor publicado</th>
          <th scope="col">Fuente</th>
          <th scope="col">Estado</th>
          <th scope="col" class="celda-casilla">Comprobado</th>
        </tr>
      </thead>
      <tbody>{"".join(filas)}</tbody>
    </table>
  </div>
  {PISTA_TABLA}

  <h3>Tareas de esta ciudad</h3>
  <ul class="lista-casillas">{tareas}</ul>

  <div class="firma">
    <p class="firma__campo">
      <span class="linea-firma"></span>
      <span class="firma__etiqueta">Nombre y firma</span>
    </p>
    <p class="firma__campo">
      <span class="linea-firma"></span>
      <span class="firma__etiqueta">Fecha de la visita</span>
    </p>
    <p class="firma__campo">
      <span class="linea-firma"></span>
      <span class="firma__etiqueta">Resultado (correcto, corregido o pendiente)</span>
    </p>
  </div>
</article>"""


def pagina_verificacion(ciudades):
    total_pendientes = sum(
        1
        for c in ciudades
        for a in c["accesibilidad"]
        if a["estado"] and a["estado"] != "verificado"
    )
    total_tareas = sum(len(c["checklist"]) for c in ciudades)
    filas_resumen = "".join(
        '<tr><td><a href="#{0}">{1}</a></td><td>{2}</td><td>{3}</td>'
        "<td>{4}</td><td>{5}</td></tr>".format(
            c["id"],
            e(c["nombre"]),
            len(c["paradas"]),
            len(c["accesibilidad"]),
            sum(
                1
                for a in c["accesibilidad"]
                if a["estado"] and a["estado"] != "verificado"
            ),
            len(c["checklist"]),
        )
        for c in ciudades
    )
    bloques = "".join(bloque_verificacion(c) for c in ciudades)
    cuerpo = f"""<div class="contenedor pagina">
  <p class="eyebrow">Verificación</p>
  <h1>Plan de verificación en sitio</h1>
  <p class="entradilla grande">Las ocho guías están publicadas como borrador. Esta
  página reúne, ciudad por ciudad, los datos que hay que confirmar sobre el
  terreno y las tareas pendientes, para llevarla impresa y firmarla.</p>

  <dl class="datos-clave">
    <div class="dato"><dt>Responsable</dt><dd>Natalia Blázquez Herrero</dd></div>
    <div class="dato"><dt>Estado</dt><dd>Pendiente, no completada</dd></div>
    <div class="dato"><dt>Fecha límite</dt><dd>2 de diciembre de 2026</dd></div>
    <div class="dato"><dt>Ciudades</dt><dd>{len(ciudades)}</dd></div>
    <div class="dato"><dt>Datos por confirmar</dt><dd>{total_pendientes}</dd></div>
    <div class="dato"><dt>Tareas</dt><dd>{total_tareas}</dd></div>
  </dl>

  <p class="hero__acciones">
    <button class="boton boton--primario" type="button" id="imprimir">
      Imprimir el plan completo
    </button>
    <a class="boton boton--secundario" href="accesibilidad.html">
      Cómo se ha construido el sitio
    </a>
  </p>

  <section class="seccion" aria-labelledby="t-resumen">
    <h2 id="t-resumen">Resumen por ciudad</h2>
    <div class="tabla-envoltorio" tabindex="0" role="region"
         aria-label="Resumen de la verificación por ciudad">
      <table>
        <caption class="sr-only">Paradas, datos de accesibilidad, datos
        pendientes y tareas de cada ciudad.</caption>
        <thead>
          <tr>
            <th scope="col">Ciudad</th>
            <th scope="col">Paradas</th>
            <th scope="col">Datos</th>
            <th scope="col">Pendientes</th>
            <th scope="col">Tareas</th>
          </tr>
        </thead>
        <tbody>{filas_resumen}</tbody>
      </table>
    </div>
    {PISTA_TABLA}
  </section>

  <section class="seccion" aria-labelledby="t-metodo">
    <h2 id="t-metodo">Cómo registrar la visita</h2>
    <ol class="lista-numerada">
      <li>Imprime el plan: cada ciudad empieza en una página nueva.</li>
      <li>Recorre la ruta publicada en el mismo orden y comprueba las paradas.</li>
      <li>Marca cada dato solo si lo has visto o lo has confirmado con una fuente
      oficial. Si no, se queda como pendiente.</li>
      <li>Anota en la ficha cualquier diferencia entre lo publicado y lo que
      encuentres, aunque parezca menor.</li>
      <li>Firma al terminar cada ciudad y avisa de los cambios para corregir el
      contenido antes de retirar los avisos de borrador.</li>
    </ol>
    <p class="aviso-inline"><strong>Regla del proyecto:</strong> ningún dato se
    cambia por suposición. Sin fuente o sin comprobación, se mantiene el estado
    pendiente.</p>
  </section>

  <section class="seccion" aria-labelledby="t-descargas">
    <h2 id="t-descargas">Datos para llevar al campo</h2>
    <p>Los mismos datos de esta página, en CSV para abrir con Excel o con una
    hoja de cálculo. Cada fila tiene casillas de fecha, resultado y notas para
    rellenar durante la visita.</p>
    <ul class="fuentes">
      <li><a href="verificacion/datos-accesibilidad.csv" download>datos-accesibilidad.csv</a>
      — los 96 datos publicados que hay que confirmar.</li>
      <li><a href="verificacion/tareas.csv" download>tareas.csv</a>
      — las tareas pendientes de las ocho ciudades.</li>
      <li><a href="verificacion/segovia-monumentos.csv" download>segovia-monumentos.csv</a>
      — 46 datos de las fichas oficiales de la catedral y el acueducto.</li>
      <li><a href="verificacion/guia-de-campo.md" download>guia-de-campo.md</a>
      — método, material, cómo medir y cómo rellenar los CSV.</li>
      <li><a href="verificacion/plantilla-ficha-campo.md" download>plantilla-ficha-campo.md</a>
      — ficha imprimible para una parada.</li>
    </ul>
    <p class="nota">Los archivos van en UTF-8 con BOM y separador «;» para que
    Excel en español los abra directamente. El estado de partida siempre es
    <code>pendiente</code>.</p>
  </section>

  {bloques}
</div>"""
    return documento(
        "Plan de verificación en sitio | Legado a Tu Paso",
        "Plan imprimible para verificar en el terreno la accesibilidad, las "
        "emergencias, el aparcamiento y el transporte de las ocho ciudades.",
        cuerpo,
        "verificacion",
        ruta="verificacion.html",
    )


def pagina_creditos(ciudades):
    bloques = []
    for c in ciudades:
        filas = []
        for f in c["fotos"]:
            archivo = e(f["archivo"])
            if f["enlace"]:
                archivo = (
                    f'<a href="{e(f["enlace"])}" rel="noopener">{archivo}</a>'
                )
            filas.append(
                f"""<tr>
  <td>{e(f['uso'])}</td>
  <td>{archivo}</td>
  <td>{e(f['autor'])}</td>
  <td>{e(f['licencia'])}</td>
</tr>"""
            )
        filas = "".join(filas)
        bloques.append(f"""<section class="seccion" aria-labelledby="cr-{c['id']}">
  <h2 id="cr-{c['id']}">{e(c['nombre'])}</h2>
  <div class="tabla-envoltorio" tabindex="0" role="region" aria-label="Créditos de {e(c['nombre'])}">
    <table>
      <caption class="sr-only">Fotografías de {e(c['nombre'])}</caption>
      <thead><tr><th scope="col">Uso</th><th scope="col">Archivo en Commons</th>
      <th scope="col">Autoría</th><th scope="col">Licencia</th></tr></thead>
      <tbody>{filas}</tbody>
    </table>
  </div>
  {PISTA_TABLA}
</section>""")

    cuerpo = f"""<div class="contenedor pagina">
  <p class="eyebrow">Transparencia</p>
  <h1>Créditos y licencias</h1>
  <p class="entradilla grande">Todo lo que no es nuestro está atribuido. Si eres
  autor de una imagen y quieres corregir el crédito, escríbenos cuando el canal de
  contacto esté publicado.</p>

  <section class="seccion" aria-labelledby="t-fotos">
    <h2 id="t-fotos">Fotografías</h2>
    <p>Todas proceden de Wikimedia Commons con licencia libre (CC0, dominio
    público, CC BY o CC BY-SA). El crédito aparece también bajo cada imagen.</p>
  </section>
  {''.join(bloques)}

  <section class="seccion" aria-labelledby="t-audio">
    <h2 id="t-audio">Audio</h2>
    <p>Los 64 audios provisionales se generaron con la voz sintética Microsoft
    Helena (es-ES) a partir de guiones propios. Se sustituirán por locución
    humana. La transcripción de cada audio es nuestra.</p>
  </section>

  <section class="seccion" aria-labelledby="t-datos">
    <h2 id="t-datos">Datos y cartografía</h2>
    <ul class="fuentes">
      <li>Clima: <a href="https://open-meteo.com/" rel="noopener">Open-Meteo</a>,
      consultado desde el navegador, con
      <a href="https://www.aemet.es/" rel="noopener">AEMET</a> como referencia
      oficial.</li>
      <li>Coordenadas y aparcamientos:
      <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a>,
      datos de sus colaboradores (ODbL).</li>
      <li>Mapas: <a href="https://leafletjs.com/" rel="noopener">Leaflet</a> 1.9.4
      (licencia BSD de 2 cláusulas), alojado en el propio sitio, con teselas de
      OpenStreetMap. La atribución aparece dentro de cada mapa.</li>
      <li>Fotografías:
      <a href="https://commons.wikimedia.org/" rel="noopener">Wikimedia Commons</a>.</li>
      <li>Tipografías: Atkinson Hyperlegible (Braille Institute) para el texto
      y la interfaz, y Literata (TypeTogether) para titulares y marca. Ambas se
      autoalojan con la
      <a href="https://openfontlicense.org/" rel="noopener">SIL Open Font License</a>;
      las licencias completas están en <code>assets/fuente/</code>.</li>
    </ul>
  </section>

  <section class="seccion" aria-labelledby="t-marca">
    <h2 id="t-marca">Marca</h2>
    <p>El logotipo, el emblema y el favicon son propios. El nombre del logotipo
    se ha convertido a trazos a partir de Literata, así que se reproduce igual
    aunque la fuente no esté instalada. Archivos:
    <code>logo.svg</code>, <code>logo-claro.svg</code>,
    <code>logo-emblema.svg</code>, <code>logo-emblema-claro.svg</code> y
    <code>favicon.svg</code>.</p>
  </section>

  <section class="seccion" aria-labelledby="t-privacidad">
    <h2 id="t-privacidad">Privacidad</h2>
    <p>El sitio no usa cookies, analítica ni píxeles de seguimiento. No hay
    cuentas ni formularios que envíen datos a un servidor propio.</p>
    <p>El navegador hace dos peticiones a terceros: Open-Meteo, para el tiempo, y
    las teselas de OpenStreetMap, para los mapas. Como en cualquier petición web,
    esos servicios reciben la IP y el agente del navegador y se rigen por sus
    propias políticas. No se les envía nada más. El audio, las fuentes y las
    imágenes se sirven desde este mismo sitio.</p>
  </section>

  <section class="seccion" aria-labelledby="t-aviso">
    <h2 id="t-aviso">Aviso</h2>
    <p>La información de accesibilidad es orientativa y está pendiente de
    verificación en sitio. No sustituye la confirmación con el establecimiento ni
    con el ayuntamiento correspondiente.</p>
  </section>
</div>"""

    return documento(
        "Créditos y licencias | Legado a Tu Paso",
        "Autoría y licencias de las fotografías, los audios y los datos del proyecto.",
        cuerpo,
        "creditos",
        ruta="creditos.html",
    )


def pagina_404():
    cuerpo = """<div class="contenedor pagina">
  <p class="eyebrow">Error 404</p>
  <h1>Esta página no existe</h1>
  <p class="entradilla grande">Puede que el enlace esté mal escrito o que la
  página ya no esté disponible. El resto del sitio sigue en pie: elige una
  ciudad o vuelve al inicio.</p>
  <p class="hero__acciones">
    <a class="boton boton--primario" href="index.html">Volver al inicio</a>
    <a class="boton boton--secundario" href="index.html#ciudades">Ver las 15 ciudades</a>
  </p>
  <section class="seccion" aria-labelledby="t-404">
    <h2 id="t-404">Enlaces útiles</h2>
    <ul class="fuentes">
      <li><a href="accesibilidad.html">Accesibilidad del sitio</a></li>
      <li><a href="verificacion.html">Plan de verificación en sitio</a></li>
      <li><a href="creditos.html">Créditos y licencias</a></li>
    </ul>
    <p class="nota">Si has llegado desde un enlace de una guía, prueba a buscar la
    ciudad en el catálogo de la portada.</p>
  </section>
</div>"""
    return documento(
        "Página no encontrada | Legado a Tu Paso",
        "La página solicitada no existe. Vuelve al catálogo de ciudades "
        "Patrimonio de la Humanidad.",
        cuerpo,
        "404",
        ruta="404.html",
        noindex=True,
    )


def escribir_manifest():
    iconos = [
        {
            "src": "assets/iconos/icono-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any",
        },
        {
            "src": "assets/iconos/icono-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any",
        },
        {
            "src": "assets/iconos/icono-maskable-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable",
        },
    ]
    manifest = {
        "id": "./",
        "name": "Legado a Tu Paso",
        "short_name": "Legado",
        "description": "Turismo accesible en ciudades Patrimonio. Descúbrelas sin barreras.",
        "lang": "es",
        "dir": "ltr",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "display_override": ["standalone", "minimal-ui"],
        "background_color": "#FAF9F7",
        "theme_color": "#FAF9F7",
        "categories": ["travel", "navigation", "education"],
        "icons": iconos,
        "shortcuts": [
            {
                "name": "Ciudades",
                "short_name": "Ciudades",
                "description": "Catálogo de ciudades Patrimonio",
                "url": "./index.html#ciudades",
                "icons": [iconos[0]],
            },
            {
                "name": "Verificación",
                "short_name": "Verificación",
                "description": "Estado de los datos de accesibilidad",
                "url": "./verificacion.html",
                "icons": [iconos[0]],
            },
            {
                "name": "Ávila",
                "short_name": "Ávila",
                "description": "Guía accesible de Ávila",
                "url": "./avila.html",
                "icons": [iconos[0]],
            },
        ],
        "screenshots": [
            {
                "src": "assets/capturas/app-inicio.png",
                "sizes": "390x844",
                "type": "image/png",
                "form_factor": "narrow",
                "label": "Portada de Legado a Tu Paso en el móvil",
            },
            {
                "src": "assets/capturas/app-guia.png",
                "sizes": "390x844",
                "type": "image/png",
                "form_factor": "narrow",
                "label": "Guía de una ciudad con ruta, audio y descarga sin conexión",
            },
            {
                "src": "assets/capturas/app-escritorio.png",
                "sizes": "1280x800",
                "type": "image/png",
                "form_factor": "wide",
                "label": "Catálogo de ciudades en escritorio",
            },
        ],
    }
    escribir(
        os.path.join(SITIO, "manifest.webmanifest"),
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )


def lista_precache(ciudades):
    """Cáscara de la app: páginas, estilos, fuentes, logos e iconos."""
    paginas = ["index.html"]
    paginas += [ciudad["id"] + ".html" for ciudad in ciudades]
    paginas += ["accesibilidad.html", "verificacion.html", "creditos.html", "404.html"]
    assets = [
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
    ]
    fuentes = []
    carpeta_fuentes = os.path.join(SITIO, "assets", "fuente")
    if os.path.isdir(carpeta_fuentes):
        fuentes = [
            "assets/fuente/" + nombre
            for nombre in sorted(os.listdir(carpeta_fuentes))
            if nombre.endswith(".woff2")
        ]
    iconos = []
    carpeta_iconos = os.path.join(SITIO, "assets", "iconos")
    if os.path.isdir(carpeta_iconos):
        iconos = [
            "assets/iconos/" + nombre
            for nombre in sorted(os.listdir(carpeta_iconos))
            if nombre.endswith(".png")
        ]
    rutas = paginas + assets + fuentes + iconos
    return [ruta for ruta in rutas if os.path.exists(os.path.join(SITIO, ruta))]


def version_shell(rutas):
    """Huella del contenido para que el service worker se actualice."""
    huella = hashlib.sha1()
    for ruta in sorted(rutas):
        huella.update(ruta.encode("utf-8"))
        with open(os.path.join(SITIO, ruta), "rb") as archivo:
            for bloque in iter(lambda: archivo.read(65536), b""):
                huella.update(bloque)
    return huella.hexdigest()[:12]


def escribir_sw(ciudades):
    rutas = lista_precache(ciudades)
    plantilla = leer(os.path.join(BASE, "herramientas", "sw.js"))
    version = hashlib.sha1(
        (plantilla + "|" + version_shell(rutas)).encode("utf-8")
    ).hexdigest()[:12]
    salida = plantilla.replace("__VERSION__", version).replace(
        "__PRECACHE__",
        json.dumps(rutas, ensure_ascii=False, indent=2),
    )
    escribir(os.path.join(SITIO, "sw.js"), salida)


def escribir_robots():
    lineas = [
        "User-agent: *",
        "Allow: /",
        "",
    ]
    if SITIO_URL:
        lineas.append(f"Sitemap: {SITIO_URL}/sitemap.xml")
    else:
        lineas.append("# Sitemap: pendiente de dominio definitivo")
    escribir(os.path.join(SITIO, "robots.txt"), "\n".join(lineas) + "\n")


def escribir_sitemap(ciudades):
    ruta = os.path.join(SITIO, "sitemap.xml")
    if not SITIO_URL:
        # Sin dominio no se publica un sitemap con URL falsas o antiguas.
        if os.path.exists(ruta):
            os.remove(ruta)
        return
    rutas = (
        ["index.html"]
        + [c["id"] + ".html" for c in ciudades]
        + ["accesibilidad.html", "verificacion.html", "creditos.html"]
    )
    items = "".join(
        f"  <url><loc>{e(SITIO_URL)}/{e(ruta)}</loc>"
        f"<lastmod>2026-11-07</lastmod></url>\n"
        for ruta in rutas
    )
    escribir(
        os.path.join(SITIO, "sitemap.xml"),
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{items}</urlset>\n",
    )


# -------------------------------------------------------------------- main
def main():
    os.makedirs(SITIO, exist_ok=True)
    guiones = json.load(io.open(os.path.join(AUDIO_SRC, "scripts.json"), encoding="utf-8"))
    enlaces = enlaces_fotos()

    ciudades = [cargar_ciudad(cid, nombre, guiones, enlaces) for cid, nombre in CIUDADES]

    escribir(os.path.join(SITIO, "index.html"), pagina_inicio(ciudades))
    for ciudad in ciudades:
        escribir(os.path.join(SITIO, ciudad["id"] + ".html"), pagina_ciudad(ciudad))
    escribir(os.path.join(SITIO, "accesibilidad.html"), pagina_accesibilidad())
    escribir(os.path.join(SITIO, "verificacion.html"), pagina_verificacion(ciudades))
    escribir(os.path.join(SITIO, "creditos.html"), pagina_creditos(ciudades))
    escribir(os.path.join(SITIO, "404.html"), pagina_404())
    escribir_manifest()
    escribir_sw(ciudades)
    escribir_robots()
    escribir_sitemap(ciudades)

    # Copia de los audios (solo el formato publicado y si falta o cambia)
    copiados = 0
    for city_id, _ in CIUDADES:
        origen = os.path.join(AUDIO_SRC, city_id)
        destino = os.path.join(AUDIO_DST, city_id)
        os.makedirs(destino, exist_ok=True)
        elegidos = audios_publicados(city_id)
        publicados = set(elegidos.values())
        for nombre in sorted(publicados):
            src = os.path.join(origen, nombre)
            dst = os.path.join(destino, nombre)
            if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
                shutil.copy2(src, dst)
                copiados += 1
        # Retira versiones antiguas del mismo audio (por ejemplo, WAV si ya hay MP3).
        for nombre in os.listdir(destino):
            if nombre.lower().endswith(EXT_AUDIO) and nombre not in publicados:
                os.remove(os.path.join(destino, nombre))

    # El JSON que se publica apunta al formato que realmente se sirve.
    guiones_sitio = json.load(
        io.open(os.path.join(AUDIO_SRC, "scripts.json"), encoding="utf-8")
    )
    for guion in guiones_sitio:
        nombre = audios_publicados(guion["city"]).get(guion["index"])
        if nombre:
            guion["file"] = f"audio/{guion['city']}/{nombre}"
    with io.open(
        os.path.join(AUDIO_DST, "scripts.json"), "w", encoding="utf-8"
    ) as archivo:
        json.dump(guiones_sitio, archivo, ensure_ascii=False, indent=1)

    print(f"Páginas generadas: {len(ciudades) + 5}")
    print(f"Audios copiados: {copiados}")
    for ciudad in ciudades:
        print(
            f"  {ciudad['nombre']:24} {len(ciudad['paradas'])} paradas "
            f"{len(ciudad['fotos'])} fotos"
        )

    import generar_verificacion

    generar_verificacion.generar(ciudades)


if __name__ == "__main__":
    main()
