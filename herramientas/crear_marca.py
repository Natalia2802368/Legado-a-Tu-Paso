"""Genera la identidad vectorial y las fuentes web de Legado a Tu Paso.

Salidas:
  sitio/assets/logo.svg            lockup horizontal (emblema + wordmark)
  sitio/assets/logo-claro.svg      lockup para fondos oscuros
  sitio/assets/logo-emblema.svg    emblema suelto
  sitio/assets/logo-emblema-claro.svg  emblema para fondos oscuros
  sitio/assets/favicon.svg         icono cuadrado para pestañas
  sitio/assets/fuente/literata-latin.woff2
  sitio/assets/fuente/literata-latin-ext.woff2
  sitio/assets/fuente/OFL-Literata.txt

El wordmark se convierte a trazos desde la Literata variable, así que el logo
no depende de que la fuente esté instalada.

Uso:
    python herramientas/crear_marca.py
"""

import io
import math
import os
import sys

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(BASE, "herramientas", "fuentes", "Literata-Variable.ttf")
OFL = os.path.join(BASE, "herramientas", "fuentes", "OFL-Literata.txt")
ASSETS = os.path.join(BASE, "sitio", "assets")
FUENTES = os.path.join(ASSETS, "fuente")

TINTA = "#30160D"
TEJA = "#5E2E1B"
PAPEL = "#FAF9F7"
TEJA_CLARO = "#E8D9CE"

TAM_TEXTO = 30
OPSZ_TEXTO = 20
ALTO = 64
CENTRO = ALTO / 2
EMBLEMA = 56
HUECO = 13

LATIN = (
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
    "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,"
    "U+2212,U+2215,U+FEFF,U+FFFD"
)
LATIN_EXT = (
    "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,"
    "U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,"
    "U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF"
)


def instancia(peso, opsz=OPSZ_TEXTO):
    fuente = TTFont(FUENTE)
    return instantiateVariableFont(
        fuente, {"wght": peso, "opsz": opsz}, inplace=False
    )


def contorno(texto, peso, tamano, x, linea_base, opsz=OPSZ_TEXTO):
    """Devuelve el trazado SVG de un texto y el ancho avanzado."""
    fuente = instancia(peso, opsz)
    glifos = fuente.getGlyphSet()
    orden = fuente.getGlyphOrder()
    datos = io.BytesIO()
    fuente.save(datos)

    cara = hb.Face(datos.getvalue())
    hb_fuente = hb.Font(cara)
    buffer = hb.Buffer()
    buffer.add_str(texto)
    buffer.guess_segment_properties()
    hb.shape(hb_fuente, buffer, {"kern": True, "liga": True})

    escala = tamano / fuente["head"].unitsPerEm
    partes = []
    for info, pos in zip(buffer.glyph_infos, buffer.glyph_positions):
        nombre = orden[info.codepoint]
        pluma = SVGPathPen(glifos, ntos=lambda v: f"{v:.2f}")
        transformacion = (
            escala,
            0,
            0,
            -escala,
            x + pos.x_offset * escala,
            linea_base - pos.y_offset * escala,
        )
        glifos[nombre].draw(TransformPen(pluma, transformacion))
        partes.append(pluma.getCommands())
        x += pos.x_advance * escala
    return "".join(partes), x


def ancho_espacio(peso=400, tamano=TAM_TEXTO):
    fuente = instancia(peso)
    return fuente["hmtx"]["space"][0] * tamano / fuente["head"].unitsPerEm


def svg_logo(nombre, color_fuerte, color_suave, sufijo=""):
    cap = instancia(700)["OS/2"].sCapHeight
    linea_base = CENTRO + cap * TAM_TEXTO / 1000 / 2
    x_texto = EMBLEMA + HUECO
    d_fuerte, fin = contorno("Legado", 700, TAM_TEXTO, x_texto, linea_base)
    inicio_suave = fin + ancho_espacio(400) + 0.8
    d_suave, fin = contorno("a Tu Paso", 400, TAM_TEXTO, inicio_suave, linea_base)
    ancho = math.ceil(fin + 2)

    mascara = (
        f'<mask id="logo-arco{sufijo}" maskUnits="userSpaceOnUse" '
        f'x="0" y="0" width="{EMBLEMA}" height="{ALTO}">'
        f'<rect width="{EMBLEMA}" height="{ALTO}" fill="#fff"/>'
        f'<path d="M18 64V34a10 10 0 0 1 20 0v30z" fill="#000"/>'
        f"</mask>"
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {ALTO}" '
        f'width="{ancho}" height="{ALTO}" role="img" '
        f'aria-labelledby="logo-titulo{sufijo}">\n'
        f'<title id="logo-titulo{sufijo}">Legado a Tu Paso</title>\n'
        f'<desc>Emblema con un arco de acceso y el nombre de la marca.</desc>\n'
        f"{mascara}\n"
        f'<circle class="logo__emblema" cx="28" cy="32" r="28" '
        f'fill="{color_fuerte}" mask="url(#logo-arco{sufijo})"/>\n'
        f'<path class="logo__texto" fill="{color_fuerte}" d="{d_fuerte}"/>\n'
        f'<path class="logo__texto-suave" fill="{color_suave}" d="{d_suave}"/>\n'
        f"</svg>\n"
    )
    with io.open(os.path.join(ASSETS, nombre), "w", encoding="utf-8") as f:
        f.write(svg)
    print(nombre, ancho, "x", ALTO, "·", len(svg), "bytes")


def svg_emblema(nombre, color, sufijo=""):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-labelledby="emblema-titulo{sufijo}">
<title id="emblema-titulo{sufijo}">Emblema de Legado a Tu Paso</title>
<desc>Un arco de acceso recortado sobre un círculo.</desc>
<mask id="emblema-arco{sufijo}" maskUnits="userSpaceOnUse" x="0" y="0" width="64" height="64">
  <rect width="64" height="64" fill="#fff"/>
  <path d="M22 64V34a10 10 0 0 1 20 0v30z" fill="#000"/>
</mask>
<circle cx="32" cy="32" r="28" fill="{color}" mask="url(#emblema-arco{sufijo})"/>
</svg>
"""
    with io.open(os.path.join(ASSETS, nombre), "w", encoding="utf-8") as f:
        f.write(svg)
    print(nombre, len(svg), "bytes")


def svg_favicon():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
<rect width="64" height="64" rx="14" fill="{TINTA}"/>
<path d="M22 64V34a10 10 0 0 1 20 0v30z" fill="{PAPEL}"/>
</svg>
"""
    with io.open(os.path.join(ASSETS, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("favicon.svg", len(svg), "bytes")


def unicode_desde(texto):
    valores = set()
    for trozo in texto.split(","):
        trozo = trozo.strip().replace("U+", "")
        if "-" in trozo:
            a, b = trozo.split("-")
            valores.update(range(int(a, 16), int(b, 16) + 1))
        else:
            valores.add(int(trozo, 16))
    return sorted(valores)


def subconjunto(nombre, rangos, peso=None, opsz=28):
    fuente = TTFont(FUENTE)
    if peso is not None:
        fuente = instantiateVariableFont(
            fuente, {"wght": peso, "opsz": opsz}, inplace=False
        )
    opciones = Options()
    opciones.name_IDs = ["*"]
    opciones.name_languages = ["*"]
    opciones.layout_features = ["kern", "liga", "calt"]
    opciones.glyph_names = False
    opciones.ignore_missing_unicodes = True
    sub = Subsetter(options=opciones)
    sub.populate(unicodes=unicode_desde(rangos))
    sub.subset(fuente)
    fuente.flavor = "woff2"
    destino = os.path.join(FUENTES, nombre)
    fuente.save(destino)
    print(nombre, os.path.getsize(destino), "bytes")


def main():
    os.makedirs(FUENTES, exist_ok=True)
    svg_logo("logo.svg", TINTA, TEJA)
    svg_logo("logo-claro.svg", PAPEL, TEJA_CLARO, "-claro")
    svg_emblema("logo-emblema.svg", TINTA)
    svg_emblema("logo-emblema-claro.svg", PAPEL, "-claro")
    svg_favicon()
    subconjunto("literata-600-latin.woff2", LATIN, peso=600)
    subconjunto("literata-600-latin-ext.woff2", LATIN_EXT, peso=600)
    with io.open(OFL, "rb") as origen, io.open(
        os.path.join(FUENTES, "OFL-Literata.txt"), "wb"
    ) as destino:
        destino.write(origen.read())
    print("OFL-Literata.txt copiado")


if __name__ == "__main__":
    sys.exit(main())
