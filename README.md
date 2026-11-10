# Legado a Tu Paso

**Turismo accesible en ciudades Patrimonio. Descúbrelas sin barreras.**

Aplicación web instalable (PWA) y base de app nativa para iOS y Android que
ayuda a preparar una visita a las Ciudades Patrimonio de la Humanidad de España:
qué se puede visitar, cómo llegar, qué barreras existen, qué recursos de acceso
hay y qué hacer si surge una emergencia.

El proyecto no promete accesibilidad: la documenta con fuente, fecha y estado de
verificación. **Ningún dato se presenta como verificado hasta que se comprueba
en el lugar.**

- **Versión del documento:** 1.9
- **Fecha:** 10 de noviembre de 2026
- **Entrega objetivo de la PWA:** 2 de diciembre de 2026
- **Estado:** web y PWA terminadas; empaquetado nativo preparado y pendiente de
  compilar; publicación pendiente de datos legales y verificación en sitio

## Estado actual

| Pieza | Estado |
| --- | --- |
| Catálogo de 15 ciudades | Listo: 8 guías completas y 7 fichas «Próximamente» |
| Guías completas | Ávila, Alcalá de Henares, Córdoba, Mérida, Salamanca, Santiago de Compostela, Segovia y Toledo |
| Fotos | 64 WebP publicadas, con autor y licencia en `creditos.html` |
| Audio | 64 MP3 provisionales de voz sintética, con transcripción y descarga |
| Mapas | Leaflet + OpenStreetMap, con alternativa textual y coordenadas |
| Clima | Open-Meteo, actualización cada 5 minutos y aviso sin conexión |
| Accesibilidad | Datos normalizados a `pendiente`; verificación en sitio pendiente |
| PWA | Instalable, con cáscara precargada de 35 archivos y descarga por ciudad |
| Sin conexión | Páginas, fotos y audio disponibles; mapa y clima explicados |
| App nativa | Configuración de Capacitor lista; proyectos Android/iOS sin generar |
| Publicación | Lista técnica y documentación; faltan dominio, aviso legal y contacto |

## Cifras del sitio publicado

| Concepto | Valor |
| --- | --- |
| Páginas generadas | 13 (portada, 8 guías, accesibilidad, verificación, créditos y 404) |
| Archivos en la cáscara del service worker | 35 |
| Fotos publicadas | 64 WebP · 14,1 MB |
| Audios publicados | 64 MP3 mono 64 kbps · 16,2 MB |
| Peso total de `sitio/` | 31,6 MB |
| Audios WAV de origen | 64 · 88,9 MB, no se publican |
| Descarga de una ciudad | 3,3–4,1 MB (fotos + audio) |

Los WAV se conservan en `audio/` como fuente de las grabaciones y para regenerar
los MP3. La web solo copia el formato publicado, de modo que no se duplica el
peso.

## Estructura del proyecto

| Ruta | Contenido |
| --- | --- |
| `contenido/` | Fuente Markdown de las 8 guías y de la plantilla de ciudad |
| `sitio/` | Sitio estático generado: es lo que se publica y lo que empaqueta Capacitor |
| `audio/` | WAV de origen, MP3 publicados y `scripts.json` con los textos |
| `fotos-originales/` | Fotos de origen; no se publican |
| `verificacion/` | CSV de accesibilidad, tareas y guía de campo |
| `herramientas/` | Generadores, revisión, service worker y utilidades de marca |
| `publicacion/` | Instrucciones de hosting, comprobaciones y guía de app móvil |
| `assets/` | Iconos y splash de origen para Capacitor |
| `capturas/` | Capturas internas de revisión; no se publican |

## Ver el sitio en local

```powershell
cd C:\Users\Admin\Documents\Legado-a-Tu-Paso
python -m http.server 8010 --directory sitio
```

Abrir <http://127.0.0.1:8010>. El service worker funciona en `localhost` o
`127.0.0.1`; para probar la instalación en un móvil hace falta HTTPS.

## Regenerar el sitio

```powershell
cd C:\Users\Admin\Documents\Legado-a-Tu-Paso
python herramientas\crear_iconos.py
python herramientas\generar_sitio.py
python herramientas\revisar_sitio.py
```

Orden obligatorio: los iconos se generan antes que el sitio y la revisión se
ejecuta al final. `revisar_sitio.py` comprueba páginas, recursos, manifiesto,
iconos, capturas, atajos, versión del service worker y cada archivo precargado.

### Dominio público

Sin variable de entorno, el sitio funciona pero no publica URL canónicas ni
sitemap. Para la versión definitiva:

```powershell
$env:LEGADO_URL = "https://www.ejemplo.es"
python herramientas\crear_iconos.py
python herramientas\generar_sitio.py
```

Con `LEGADO_URL` se añaden `canonical`, `og:url`, la imagen social absoluta,
`sitemap.xml` y la línea `Sitemap:` de `robots.txt`.

## Audio

- **Formato publicado:** MP3 mono, 22.050 Hz, 64 kbps.
- **Formato fuente:** WAV mono, 22.050 Hz, 16 bits.
- **Voz:** Microsoft Helena (es-ES), generada el 2/11/2026. Es una versión
  provisional; la producción final usa voz humana y los guiones de cada ficha.
- **Duración:** los 64 MP3 conservan la duración de su WAV de origen (diferencia
  máxima comprobada: 0,001 s).
- **Textos:** `audio/scripts.json` apunta a los MP3 publicados.
- **Conversión:** `python herramientas/convertir_audio.py` regenera los MP3 desde
  los WAV (requiere `ffmpeg` en el PATH o `--ffmpeg`). Usa `--forzar` para
  reconvertir todo.
- **Inventario y duraciones:** `audio/README.md`.

El generador elige un solo formato por parada, con prioridad MP3, copia solo ese
archivo a `sitio/audio/`, retira versiones antiguas y reescribe
`sitio/audio/scripts.json` con las rutas publicadas.

## Accesibilidad y verificación

Estados admitidos: `verificado`, `pendiente`, `desactualizado` y `descartado`.
«Fuente oficial» describe el origen del dato, no un estado de verificación.

- **Responsable de la verificación en sitio:** Natalia Blázquez Herrero.
- **Fecha límite:** 2 de diciembre de 2026.
- **Situación:** todos los datos están en `pendiente`.
- **Material de campo:** `verificacion/datos-accesibilidad.csv` (96 filas),
  `verificacion/tareas.csv` (69 filas) y
  `verificacion/segovia-monumentos.csv` (46 filas).
- **Guía:** `verificacion/guia-de-campo.md` y
  `verificacion/plantilla-ficha-campo.md`.
- **Página pública:** `sitio/verificacion.html`, con descarga de los CSV.

No se debe cambiar un estado a `verificado` sin la comprobación firmada. Tampoco
se inventan teléfonos, plazas de aparcamiento PMR, medidas ni pendientes.

## PWA y app móvil

La misma carpeta `sitio/` es la web, la PWA instalable y el contenido de la app
nativa. No hay dos bases de código.

- **PWA:** manifiesto con iconos 192/512 y maskable, tres atajos y tres capturas;
  service worker con precarga versionada, HTML network-first con caída a caché,
  estáticos cache-first y caché de medios persistente.
- **Sin conexión:** las 13 páginas y la interfaz están precargadas. Cada guía
  permite descargar sus fotos y audios, muestra progreso y tamaño, y permite
  borrarlos. El audio guardado responde a peticiones `Range` con `206`.
- **Instalación:** botón en el pie en navegadores compatibles e instrucciones de
  Compartir → Añadir a pantalla de inicio en iPhone y iPad.
- **App nativa:** Capacitor 8, identificador `es.legadoatupaso.app`, `webDir`
  apuntando a `sitio/` e iconos/splash de origen en `assets/`.

La compilación nativa requiere Node 22+, JDK 21, Android Studio Otter o
posterior y, para iOS, macOS con Xcode 26+. En este equipo no están disponibles.
La guía completa, incluida la publicación en tiendas, está en
`publicacion/APP-MOVIL.md`.

## Comprobaciones realizadas

- **Auditoría del generador:** 13 páginas, manifiesto y service worker correctos;
  0 problemas.
- **Audio:** 64 MP3 presentes, sin archivos WAV publicados; duración conservada.
- **Lighthouse:** 1,0 en accesibilidad, buenas prácticas y SEO en portada, Ávila,
  verificación, accesibilidad y créditos.
- **Desbordamiento horizontal:** sin incidencias a 320, 390 y 785 px en portada,
  Ávila, verificación, accesibilidad, créditos y 404.
- **Sin conexión:** recarga servida desde el service worker, foto en caché,
  audio con `Range` `206` y sin errores de consola.
- **Fallo 502:** la página guardada sustituye al error cuando la red no devuelve
  una respuesta válida.

Las comprobaciones son locales. Antes de publicar hay que repetirlas en la URL
real con HTTPS; la lista está en `publicacion/COMPROBACION-PUBLICACION.md`.

## Pendientes y bloqueos

| Pendiente | Responsable o dependencia |
| --- | --- |
| Verificación en sitio de los datos de accesibilidad | Natalia Blázquez Herrero |
| Grabación con voz humana | Producción de audio |
| Revisión visual de las 64 fotos | Revisión humana |
| Aviso legal, privacidad y canal de contacto | Datos del cliente |
| Dominio definitivo y HTTPS | Decisión de publicación |
| Aparcamiento accesible en Mérida; datos parciales en Alcalá, Córdoba y Segovia | Fuentes municipales |
| Compilar Android e iOS y publicar en tiendas | Node 22+, JDK 21, Android SDK, macOS/Xcode y cuentas |

## Documentos de referencia

- `prd.md` — requisitos de producto y alcance.
- `brief-diseno.md` — identidad, diseño y restricciones de experiencia.
- `publicacion/LEEME.md` — cómo publicar el sitio y tipos MIME.
- `publicacion/COMPROBACION-PUBLICACION.md` — lista previa a abrir al público.
- `publicacion/APP-MOVIL.md` — PWA, Capacitor y tiendas.
- `audio/README.md` — inventario de los 64 audios.
- `creditos-fotos.md` — autores y licencias de las fotografías.

## Licencia y uso

Proyecto privado. El código no se distribuye con una licencia de reutilización
abierta (`UNLICENSED` en `package.json`). Las fotografías conservan la licencia
indicada en `creditos.html` y en `creditos-fotos.md`; las tipografías Atkinson
Hyperlegible y Literata se usan bajo SIL Open Font License, incluida en
`sitio/assets/fuente/`.
