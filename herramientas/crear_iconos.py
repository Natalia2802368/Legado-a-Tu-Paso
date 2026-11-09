# -*- coding: utf-8 -*-
"""Genera los iconos PNG y el favicon.ico a partir del emblema de la marca.

Uso:
    python herramientas/crear_iconos.py

Salida:
    sitio/assets/iconos/icono-192.png
    sitio/assets/iconos/icono-512.png
    sitio/assets/iconos/icono-maskable-512.png
    sitio/assets/iconos/apple-touch-icon.png
    sitio/favicon.ico
    assets/icon-only.png, icon-foreground.png, icon-background.png
    assets/splash.png, assets/splash-dark.png   (fuentes de Capacitor)
"""

import os

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONOS = os.path.join(BASE, "sitio", "assets", "iconos")
SITIO = os.path.join(BASE, "sitio")
ASSETS_NATIVOS = os.path.join(BASE, "assets")

TINTA = "#30160D"
PAPEL = "#FAF9F7"
ESCALA = 4


def icono_redondeado(tamano):
    lado = tamano * ESCALA
    imagen = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rounded_rectangle(
        [0, 0, lado - 1, lado - 1],
        radius=14 * lado / 64.0,
        fill=TINTA,
    )
    factor = lado / 64.0
    dibujo.rectangle(
        [22 * factor, 34 * factor, 42 * factor, 64 * factor], fill=PAPEL
    )
    dibujo.ellipse(
        [22 * factor, 24 * factor, 42 * factor, 44 * factor], fill=PAPEL
    )
    return imagen.resize((tamano, tamano), Image.Resampling.LANCZOS)


def icono_maskable(tamano):
    lado = tamano * ESCALA
    imagen = Image.new("RGBA", (lado, lado), TINTA)
    dibujo = ImageDraw.Draw(imagen)
    factor = lado / 64.0

    def punto(x, y):
        # La puerta se reduce al 72 % y se centra en la zona segura del icono.
        return (
            lado / 2 + (x - 32) * 0.72 * factor,
            lado / 2 + (y - 32) * 0.72 * factor,
        )

    x0, y0 = punto(22, 34)
    x1, y1 = punto(42, 64)
    dibujo.rectangle([x0, y0, x1, y1], fill=PAPEL)
    x0, y0 = punto(22, 24)
    x1, y1 = punto(42, 44)
    dibujo.ellipse([x0, y0, x1, y1], fill=PAPEL)
    return imagen.resize((tamano, tamano), Image.Resampling.LANCZOS)


def dibujar_emblema(dibujo, lado, color, escala=1.0):
    """Dibuja la puerta y el arco centrados en un lienzo cuadrado."""
    factor = lado / 64.0

    def punto(x, y):
        return (
            lado / 2 + (x - 32) * escala * factor,
            lado / 2 + (y - 44) * escala * factor,
        )

    x0, y0 = punto(22, 34)
    x1, y1 = punto(42, 64)
    dibujo.rectangle([x0, y0, x1, y1], fill=color)
    x0, y0 = punto(22, 24)
    x1, y1 = punto(42, 44)
    dibujo.ellipse([x0, y0, x1, y1], fill=color)


def icono_para_tienda(tamano):
    """Icono sin esquinas redondeadas: la tienda aplica su propia máscara."""
    imagen = Image.new("RGBA", (tamano, tamano), TINTA)
    dibujar_emblema(ImageDraw.Draw(imagen), tamano, PAPEL, 0.78)
    return imagen


def primer_plano_icono(tamano):
    imagen = Image.new("RGBA", (tamano, tamano), (0, 0, 0, 0))
    dibujar_emblema(ImageDraw.Draw(imagen), tamano, PAPEL, 0.62)
    return imagen


def fondo_icono(tamano):
    return Image.new("RGBA", (tamano, tamano), TINTA)


def pantalla_inicio(tamano, fondo, color):
    imagen = Image.new("RGBA", (tamano, tamano), fondo)
    dibujar_emblema(ImageDraw.Draw(imagen), tamano, color, 0.55)
    return imagen


def guardar_en(carpeta, imagen, nombre):
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)
    imagen.save(ruta, "PNG", optimize=True)
    print(f"{nombre:32} {imagen.size[0]}x{imagen.size[1]} · {os.path.getsize(ruta)} bytes")


def guardar(imagen, nombre):
    guardar_en(ICONOS, imagen, nombre)


def main():
    guardar(icono_redondeado(192), "icono-192.png")
    guardar(icono_redondeado(512), "icono-512.png")
    guardar(icono_maskable(512), "icono-maskable-512.png")
    guardar(icono_maskable(180), "apple-touch-icon.png")

    # Fuentes para @capacitor/assets (iconos y pantallas de inicio nativos).
    guardar_en(ASSETS_NATIVOS, icono_para_tienda(1024), "icon-only.png")
    guardar_en(ASSETS_NATIVOS, primer_plano_icono(1024), "icon-foreground.png")
    guardar_en(ASSETS_NATIVOS, fondo_icono(1024), "icon-background.png")
    guardar_en(
        ASSETS_NATIVOS,
        pantalla_inicio(2732, PAPEL, TINTA),
        "splash.png",
    )
    guardar_en(
        ASSETS_NATIVOS,
        pantalla_inicio(2732, TINTA, PAPEL),
        "splash-dark.png",
    )

    # ICO multirresolución a partir del icono redondeado.
    base = icono_redondeado(256)
    ruta_ico = os.path.join(SITIO, "favicon.ico")
    base.save(
        ruta_ico,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    print(f"favicon.ico                      {os.path.getsize(ruta_ico)} bytes")


if __name__ == "__main__":
    main()
