"""Revisa el HTML generado en sitio/ antes de publicar.

Comprueba, en cada página:
  - un solo h1 y presencia de <title>
  - ids únicos
  - que cada aria-labelledby apunte a un id existente
  - anclas internas y archivos enlazados existentes
  - recursos (imágenes, audio, scripts) existentes, ignorando ?v=...
  - que todas las imágenes tengan atributo alt
  - que el manifiesto y el service worker estén generados y sus recursos existan

Uso:
    python herramientas/revisar_sitio.py
"""

import glob
import html.parser
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = os.path.join(BASE, "sitio")


class Auditor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.hrefs = []
        self.srcs = []
        self.aria = []
        self.imgs = []
        self.h1 = 0
        self.title = None
        self._en_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag in ("img", "audio", "source", "script") and "src" in a:
            self.srcs.append(a["src"])
        if "aria-labelledby" in a:
            self.aria.extend(a["aria-labelledby"].split())
        if tag == "img":
            self.imgs.append(a.get("alt"))
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._en_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._en_title = False

    def handle_data(self, data):
        if self._en_title and self.title is None:
            self.title = data.strip()


def revisar(ruta):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    p = Auditor()
    p.feed(texto)
    problemas = []

    if p.h1 != 1:
        problemas.append(f"h1={p.h1}")
    if not p.title:
        problemas.append("sin title")

    duplicados = sorted({i for i in p.ids if p.ids.count(i) > 1})
    if duplicados:
        problemas.append("ids duplicados: %s" % ", ".join(duplicados[:5]))

    for destino in p.aria:
        if destino not in p.ids:
            problemas.append(f"aria-labelledby roto: {destino}")

    for href in p.hrefs:
        if href.startswith("#") and len(href) > 1:
            if href[1:] not in p.ids:
                problemas.append(f"ancla rota: {href}")
        elif href.startswith(("http://", "https://", "tel:", "mailto:")):
            continue
        else:
            fichero = href.split("#")[0].split("?")[0]
            if fichero and not os.path.exists(os.path.join(SITIO, fichero)):
                problemas.append(f"archivo enlazado inexistente: {href}")

    for src in p.srcs:
        if not src or src.startswith(("http://", "https://")):
            continue
        fichero = src.split("?")[0].split("#")[0]
        if not os.path.exists(os.path.join(SITIO, fichero)):
            problemas.append(f"recurso inexistente: {src}")

    if any(alt is None for alt in p.imgs):
        problemas.append("img sin atributo alt")

    return problemas


def ruta_local(url):
    """Convierte una URL relativa del manifiesto en una ruta de sitio/."""
    limpia = (url or "").split("?")[0].split("#")[0]
    if limpia.startswith("./"):
        limpia = limpia[2:]
    return limpia


def revisar_manifest():
    ruta = os.path.join(SITIO, "manifest.webmanifest")
    if not os.path.exists(ruta):
        return ["manifest.webmanifest ausente"]

    try:
        with open(ruta, encoding="utf-8") as archivo:
            manifest = json.load(archivo)
    except (ValueError, OSError) as error:
        return [f"manifest.webmanifest inválido: {error}"]

    problemas = []
    for clave in ("name", "short_name", "start_url", "scope", "display", "icons"):
        if not manifest.get(clave):
            problemas.append(f"manifest sin {clave}")

    iconos = manifest.get("icons") or []
    if not any(i.get("sizes") == "512x512" for i in iconos):
        problemas.append("manifest sin icono 512x512")
    if not any(i.get("purpose") == "maskable" for i in iconos):
        problemas.append("manifest sin icono maskable")

    recursos = list(iconos)
    recursos += manifest.get("screenshots") or []
    for corto in manifest.get("shortcuts") or []:
        recursos += corto.get("icons") or []
        destino = ruta_local(corto.get("url"))
        if destino and not os.path.exists(os.path.join(SITIO, destino)):
            problemas.append(f"atajo sin destino: {corto.get('url')}")

    for recurso in recursos:
        destino = ruta_local(recurso.get("src"))
        if destino and not os.path.exists(os.path.join(SITIO, destino)):
            problemas.append(f"icono o captura ausente: {recurso.get('src')}")

    return problemas


def revisar_sw():
    ruta = os.path.join(SITIO, "sw.js")
    if not os.path.exists(ruta):
        return ["sw.js ausente"]

    with open(ruta, encoding="utf-8") as archivo:
        texto = archivo.read()

    problemas = []
    if "__VERSION__" in texto or "__PRECACHE__" in texto:
        problemas.append("sw.js sin generar (quedan marcadores)")

    version = re.search(r'const VERSION = "([^"]+)"', texto)
    if not version or not version.group(1):
        problemas.append("sw.js sin versión")

    precache = re.search(r"const PRECACHE = (\[.*?\]);", texto, re.S)
    if not precache:
        return problemas + ["sw.js sin lista PRECACHE"]

    try:
        rutas = json.loads(precache.group(1))
    except ValueError:
        return problemas + ["PRECACHE no es JSON válido"]

    if len(rutas) < 20:
        problemas.append(f"PRECACHE demasiado corto: {len(rutas)} archivos")
    for destino in rutas:
        if not os.path.exists(os.path.join(SITIO, ruta_local(destino))):
            problemas.append(f"precache ausente: {destino}")

    return problemas


def main():
    paginas = sorted(glob.glob(os.path.join(SITIO, "*.html")))
    if not paginas:
        print("No hay páginas en sitio/. Ejecuta antes generar_sitio.py.")
        return 1

    fallos = 0
    for ruta in paginas:
        nombre = os.path.basename(ruta)
        problemas = revisar(ruta)
        print(f"{nombre:<32} {'OK' if not problemas else '; '.join(problemas[:6])}")
        fallos += len(problemas)

    for nombre, revision in (
        ("manifest.webmanifest", revisar_manifest()),
        ("sw.js", revisar_sw()),
    ):
        print(f"{nombre:<32} {'OK' if not revision else '; '.join(revision[:6])}")
        fallos += len(revision)

    print()
    print(f"páginas: {len(paginas)} · problemas: {fallos}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
