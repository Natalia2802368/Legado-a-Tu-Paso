# -*- coding: utf-8 -*-
"""Convierte los WAV de audio/ al MP3 que publica el sitio.

Uso:
    python herramientas/convertir_audio.py
    python herramientas/convertir_audio.py --ffmpeg "C:\\ruta\\ffmpeg.exe"
    python herramientas/convertir_audio.py --forzar

Formato de salida: MP3 mono, 22.050 Hz, 64 kbps, sin metadatos. Los WAV se
conservan como fuente. Después de convertir, ejecutar generar_sitio.py para
copiar los MP3 y actualizar las duraciones y los tamaños de las fichas.
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(BASE, "audio")


def buscar_ffmpeg(ruta):
    if ruta:
        if os.path.isfile(ruta):
            return os.path.abspath(ruta)
        encontrado = shutil.which(ruta)
        if encontrado:
            return encontrado
        return None
    return shutil.which("ffmpeg")


def convertir(ffmpeg, wav, mp3):
    orden = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        wav,
        "-ac",
        "1",
        "-ar",
        "22050",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        "64k",
        "-map_metadata",
        "-1",
        "-id3v2_version",
        "3",
        mp3,
    ]
    subprocess.run(orden, check=True)


def megas(rutas):
    return sum(os.path.getsize(r) for r in rutas) / 1048576


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ffmpeg",
        help="Ruta a ffmpeg.exe. Si se omite, se busca en PATH.",
    )
    parser.add_argument(
        "--forzar",
        action="store_true",
        help="Vuelve a convertir aunque el MP3 sea más reciente que el WAV.",
    )
    args = parser.parse_args()

    ffmpeg = buscar_ffmpeg(args.ffmpeg)
    if not ffmpeg:
        print(
            "No se encuentra ffmpeg. Instálalo o indica la ruta con "
            "--ffmpeg \"C:\\ruta\\ffmpeg.exe\".",
            file=sys.stderr,
        )
        return 1

    wavs = sorted(glob.glob(os.path.join(AUDIO, "*", "*.wav")))
    if not wavs:
        print("No hay archivos WAV en audio/.", file=sys.stderr)
        return 1

    convertidos = 0
    omitidos = 0
    for wav in wavs:
        mp3 = os.path.splitext(wav)[0] + ".mp3"
        if (
            not args.forzar
            and os.path.exists(mp3)
            and os.path.getmtime(mp3) >= os.path.getmtime(wav)
        ):
            omitidos += 1
            continue
        try:
            convertir(ffmpeg, wav, mp3)
        except subprocess.CalledProcessError:
            print("Error al convertir: %s" % wav, file=sys.stderr)
            return 1
        convertidos += 1
        print("convertido: %s" % os.path.relpath(mp3, BASE))

    mp3s = sorted(glob.glob(os.path.join(AUDIO, "*", "*.mp3")))
    print(
        "WAV: %d (%.1f MB) · MP3: %d (%.1f MB) · convertidos: %d · omitidos: %d"
        % (len(wavs), megas(wavs), len(mp3s), megas(mp3s), convertidos, omitidos)
    )
    if convertidos:
        print("Ahora ejecuta: python herramientas/generar_sitio.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
