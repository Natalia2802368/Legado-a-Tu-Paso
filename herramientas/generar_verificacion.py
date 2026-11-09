# -*- coding: utf-8 -*-
"""Genera los CSV de verificación en sitio a partir de contenido/*.md.

Salida:
    verificacion/datos-accesibilidad.csv     datos publicados que hay que confirmar
    verificacion/tareas.csv                  tareas por ciudad
    verificacion/segovia-monumentos.csv      fichas oficiales de catedral y acueducto
    sitio/verificacion/*.csv                 copia descargable desde la web

Uso:
    python herramientas/generar_verificacion.py

Los CSV van en UTF-8 con BOM y separador «;» para que Excel en español los abra
directamente. No se inventa ningún dato: el estado de partida es «pendiente».
"""

import csv
import io
import json
import os
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENIDO = os.path.join(BASE, "contenido")
SITIO = os.path.join(BASE, "sitio")
VERIFICACION = os.path.join(BASE, "verificacion")
VERIFICACION_SITIO = os.path.join(SITIO, "verificacion")
SEGOVIA_FICHAS = os.path.join(
    BASE,
    "materiales",
    "files-2",
    "segovia_fichas_accesibilidad_catedral_acueducto.csv",
)

RESPONSABLE = "Natalia Blázquez Herrero"
FECHA_LIMITE = "2026-12-02"

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


def escribir_csv(ruta, cabecera, filas):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with io.open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo, delimiter=";", lineterminator="\r\n")
        escritor.writerow(cabecera)
        for fila in filas:
            escritor.writerow([fila.get(columna, "") for columna in cabecera])
    print(f"{os.path.relpath(ruta, BASE):48} {len(filas)} filas")


def filas_accesibilidad(ciudades):
    salida = []
    for ciudad in ciudades:
        for dato in ciudad["accesibilidad"]:
            salida.append(
                {
                    "ciudad_id": ciudad["id"],
                    "ciudad": ciudad["nombre"],
                    "comunidad": ciudad["comunidad"],
                    "campo": dato["campo"],
                    "valor_publicado": dato["valor"],
                    "fuente": dato["fuente"],
                    "estado": dato["estado"] or "pendiente",
                    "responsable": RESPONSABLE,
                    "fecha_limite": FECHA_LIMITE,
                    "fecha_visita": "",
                    "resultado": "",
                    "notas": "",
                }
            )
    return salida


def filas_tareas(ciudades):
    salida = []
    for ciudad in ciudades:
        for numero, tarea in enumerate(ciudad["checklist"], 1):
            salida.append(
                {
                    "ciudad_id": ciudad["id"],
                    "ciudad": ciudad["nombre"],
                    "numero": numero,
                    "tarea": tarea,
                    "estado": "pendiente",
                    "responsable": RESPONSABLE,
                    "fecha_limite": FECHA_LIMITE,
                    "fecha_visita": "",
                    "resultado": "",
                    "notas": "",
                }
            )
    return salida


def filas_segovia():
    if not os.path.exists(SEGOVIA_FICHAS):
        print("Aviso: no está el CSV de fichas de Segovia; se omite.")
        return []
    with io.open(SEGOVIA_FICHAS, encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        salida = []
        for fila in lector:
            salida.append(
                {
                    "id": fila.get("id", ""),
                    "monumento": fila.get("monumento", ""),
                    "ambito": fila.get("ambito", ""),
                    "elemento": fila.get("elemento", ""),
                    "valor": fila.get("valor", ""),
                    "unidad": fila.get("unidad", ""),
                    "tipo_dato": fila.get("tipo_dato", ""),
                    "observacion": fila.get("observacion", ""),
                    "fuente_url": fila.get("fuente_url", ""),
                    "fecha_consulta": fila.get("fecha_consulta", ""),
                    "fecha_inspeccion_ficha": fila.get(
                        "fecha_inspeccion_ficha", "no indicada"
                    ),
                    "estado": "pendiente",
                    "responsable": RESPONSABLE,
                    "fecha_limite": FECHA_LIMITE,
                    "fecha_visita": "",
                    "resultado": "",
                    "notas": "",
                }
            )
    return salida


def generar(ciudades=None, publicar=True):
    if ciudades is None:
        import generar_sitio

        guiones = json.load(
            io.open(
                os.path.join(BASE, "audio", "scripts.json"), encoding="utf-8"
            )
        )
        enlaces = generar_sitio.enlaces_fotos()
        ciudades = [
            generar_sitio.cargar_ciudad(cid, nombre, guiones, enlaces)
            for cid, nombre in CIUDADES
        ]

    destinos = [VERIFICACION]
    if publicar:
        destinos.append(VERIFICACION_SITIO)

    datos = [
        (
            "datos-accesibilidad.csv",
            [
                "ciudad_id",
                "ciudad",
                "comunidad",
                "campo",
                "valor_publicado",
                "fuente",
                "estado",
                "responsable",
                "fecha_limite",
                "fecha_visita",
                "resultado",
                "notas",
            ],
            filas_accesibilidad(ciudades),
        ),
        (
            "tareas.csv",
            [
                "ciudad_id",
                "ciudad",
                "numero",
                "tarea",
                "estado",
                "responsable",
                "fecha_limite",
                "fecha_visita",
                "resultado",
                "notas",
            ],
            filas_tareas(ciudades),
        ),
        (
            "segovia-monumentos.csv",
            [
                "id",
                "monumento",
                "ambito",
                "elemento",
                "valor",
                "unidad",
                "tipo_dato",
                "observacion",
                "fuente_url",
                "fecha_consulta",
                "fecha_inspeccion_ficha",
                "estado",
                "responsable",
                "fecha_limite",
                "fecha_visita",
                "resultado",
                "notas",
            ],
            filas_segovia(),
        ),
    ]

    for destino in destinos:
        for nombre, cabecera, filas in datos:
            escribir_csv(os.path.join(destino, nombre), cabecera, filas)

    if publicar:
        # La guía y la plantilla también se descargan desde el plan.
        os.makedirs(VERIFICACION_SITIO, exist_ok=True)
        for nombre in ("guia-de-campo.md", "plantilla-ficha-campo.md"):
            origen = os.path.join(VERIFICACION, nombre)
            if os.path.exists(origen):
                shutil.copy2(origen, os.path.join(VERIFICACION_SITIO, nombre))
                print(f"sitio/verificacion/{nombre:28} copiado")

    print(
        f"Total: {sum(len(f) for _, _, f in datos)} filas · "
        f"responsable: {RESPONSABLE} · límite: {FECHA_LIMITE}"
    )


if __name__ == "__main__":
    generar()
