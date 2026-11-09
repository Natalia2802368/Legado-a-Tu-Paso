# Comprobación antes de publicar

Lista de comprobaciones para abrir el sitio al público sin romper la promesa del
proyecto: **ningún dato de accesibilidad se presenta como verificado sin estarlo**.

Marcar cada casilla solo cuando se haya comprobado en la URL real, no en local.

## 1. Dominio, HTTPS y canónicas

- [ ] El dominio definitivo está decidido y escrito (ej. `https://www.ejemplo.es`).
- [ ] El certificado HTTPS es válido y no da avisos. La versión HTTP redirige 301
      a HTTPS.
- [ ] El dominio sin `www` y con `www` apuntan al mismo sitio (uno redirige al
      otro).
- [ ] El sitio se ha generado con `LEGADO_URL`:

      ```powershell
      $env:LEGADO_URL = "https://www.ejemplo.es"
      python herramientas\crear_iconos.py
      python herramientas\generar_sitio.py
      ```

- [ ] Cada página tiene `<link rel="canonical">` con la URL absoluta correcta.
- [ ] `og:url` y `og:image` son absolutos y apuntan al dominio real.
- [ ] `sitio/sitemap.xml` existe y lista las 12 páginas indexables (sin `404.html`).
- [ ] `sitio/robots.txt` incluye `Sitemap: https://…/sitemap.xml`.
- [ ] `404.html` responde con código 404 real (no 200) desde el servidor.
- [ ] Las rutas sin `.html` (`/segovia`) funcionan o redirigen; no dan 404.

## 2. Cabeceras y tipos MIME

- [ ] `Content-Type: text/html; charset=utf-8` en todas las páginas.
- [ ] `.webmanifest` se sirve como `application/manifest+json`.
- [ ] `.woff2` se sirve como `font/woff2`.
- [ ] `.webp` se sirve como `image/webp`.
- [ ] `.wav` se sirve como `audio/wav`.
- [ ] `.svg` se sirve como `image/svg+xml`.
- [ ] `.xml` se sirve como `application/xml`.
- [ ] `.csv` se sirve como `text/csv; charset=utf-8` y se abre con Excel.
- [ ] `X-Content-Type-Options: nosniff` está presente.
- [ ] `Referrer-Policy: strict-origin-when-cross-origin` está presente.
- [ ] `Content-Security-Policy` está presente y **no rompe** mapas, clima, fuentes
      ni audio. Comprobar la consola del navegador en `/segovia.html` y en
      `/index.html`.
- [ ] Si se activa HSTS, el sitio funciona en HTTPS en todas sus rutas antes de
      enviar la cabecera.

## 3. Rendimiento y caché

- [ ] `html` se sirve con `Cache-Control: public, max-age=0, must-revalidate`.
- [ ] CSS, JS y fuentes llevan hash o `?v=` y caché larga.
- [ ] Las fotos llevan caché de 30 días y el audio de 7 días.
- [ ] `gzip` o `br` está activo para HTML, CSS, JS, SVG y XML.
- [ ] La portada pesa menos de 1,5 MB en la primera carga (sin contar el mapa si
      se carga después).

### PWA y service worker

- [ ] El sitio se sirve por HTTPS (o `http://127.0.0.1` en local); sin HTTPS el
      service worker no se registra.
- [ ] `/sw.js` responde 200 con `Cache-Control: no-cache` o
      `max-age=0, must-revalidate`, no con caché de días.
- [ ] `/manifest.webmanifest` responde 200 como `application/manifest+json`.
- [ ] Tras la primera visita, `legado-shell-…` contiene las 13 páginas, CSS, JS,
      fuentes, logos, iconos, manifiesto y Leaflet (35 archivos).
- [ ] Al recargar sin conexión, la página y la navegación siguen funcionando.
- [ ] Si el servidor o un proxy devuelve `502`, la página guardada sigue
      apareciendo en lugar del error.
- [ ] «Descargar esta ciudad» guarda todas las fotos y audios, muestra progreso y
      termina con «Guía guardada en este dispositivo».
- [ ] «Borrar la descarga» elimina los medios y vuelve a pedir red.
- [ ] Una petición `Range` a un audio guardado responde `206` con
      `Content-Range` y `Accept-Ranges: bytes`.
- [ ] El navegador ofrece instalar la app; en iOS aparece la instrucción de
      Compartir → Añadir a pantalla de inicio.
- [ ] Al publicar una versión nueva, cambia el nombre de `legado-shell-…`, se
      borra la cáscara anterior y **se conserva** `legado-media-v1`.
- [ ] Si el sistema borra la caché, la app lo explica y permite volver a
      descargar sin romper la página.

## 4. Audio y contenido multimedia

- [ ] Los 64 audios responden 200 y se pueden reproducir y descargar.
- [ ] El servidor admite peticiones `Range` en `/audio/*` (para buscar dentro del
      audio). Probar con un reproductor que permita arrastrar.
- [ ] Ningún audio se reproduce automáticamente.
- [ ] Cada audio tiene su transcripción en la misma página.
- [ ] Si se sustituye el TTS por voz humana, los nombres de archivo y los
      créditos siguen siendo correctos.

## 5. Imágenes, iconos y redes sociales

- [ ] `/assets/social/og.png` responde 200 y mide 1200×630.
- [ ] El validador de tarjetas sociales (por ejemplo, el depurador de Facebook o
      el de LinkedIn) muestra título, descripción e imagen.
- [ ] `/favicon.ico` y `/assets/favicon.svg` responden 200.
- [ ] `manifest.webmanifest` responde 200 y el navegador ofrece instalar el sitio.
- [ ] Los iconos 192 y 512 y el maskable se ven bien en la instalación.
- [ ] Ninguna imagen publicada tiene datos EXIF con ubicación o autor privado.

## 6. Legal y contacto

- [ ] Aviso legal con titular, NIF y domicilio, o los datos que correspondan.
- [ ] Política de privacidad coherente con el uso real (sin cookies, Open-Meteo y
      OSM como terceros).
- [ ] Canal de contacto accesible (correo o formulario) y dirección publicada.
- [ ] Si hay formulario, cumple RGPD: finalidad, base jurídica y derechos.
- [ ] Declaración de accesibilidad con fecha y canal para reportar barreras.
- [ ] Texto de licencia de fotos y audios revisado por quien publica.

> **Bloqueo actual:** el proyecto no ha recibido los datos legales ni el canal de
> contacto. Sin ellos no se debe publicar una web identificable en España.

## 7. Contenido y promesas

- [ ] Ninguna página dice que un lugar «es accesible» sin estado `verificado`.
- [ ] El aviso de «pendiente de verificación» sigue visible en las 8 guías.
- [ ] Los datos de Segovia siguen marcados como consulta de ficha oficial, no como
      inspección propia.
- [ ] No hay teléfonos, plazas PMR ni medidas inventadas.
- [ ] La fecha de revisión de la página de accesibilidad es la real.
- [ ] Los enlaces externos abren bien y no han cambiado de destino.

## 8. Accesibilidad del sitio publicado

- [ ] Lighthouse (o axe) da 100 en accesibilidad en portada, una ciudad,
      accesibilidad, verificación y créditos.
- [ ] Se puede recorrer toda la portada solo con teclado, con foco visible.
- [ ] «Saltar al contenido» aparece al primer <kbd>Tab</kbd>.
- [ ] A 200 % de zoom no hay contenido cortado ni desplazamiento horizontal.
- [ ] Con `prefers-reduced-motion`, no hay animaciones molestas.
- [ ] Con modo de contraste alto o `forced-colors`, los controles se distinguen.
- [ ] El mapa tiene alternativa en texto con coordenadas.
- [ ] El clima se anuncia con `aria-live` sin interrumpir.
- [ ] El 112 es un enlace `tel:` visible en cabecera y en cada guía.
- [ ] Un lector de pantalla (NVDA o VoiceOver) lee el índice y las paradas en
      orden lógico.

## 9. Después de publicar

- [ ] Enviar `sitemap.xml` a Google Search Console y a Bing Webmaster Tools.
- [ ] Comprobar que la página 404 se muestra al pedir una URL inexistente.
- [ ] Vigilar los errores 404 y de CSP en los registros del servidor.
- [ ] Programar una revisión de enlaces externos y de datos cada 6 meses.
- [ ] Programar la sustitución del TTS por voz humana.
- [ ] Programar la verificación en sitio de Natalia Blázquez Herrero antes del
      2 de diciembre de 2026.
- [ ] Retirar el aviso de «pendiente» solo con los CSV rellenos y firmados.
- [ ] Guardar una copia del sitio publicado y de los CSV entregados.

## 10. App nativa y tiendas

Solo cuando existan cuentas y entorno de compilación. Guía completa en
`APP-MOVIL.md`.

- [ ] Node 22+, JDK 21, Android Studio Otter o posterior y, para iOS, macOS con
      Xcode 26+.
- [ ] `npm install`, `npm run cap:add:android` / `cap:add:ios` y `npm run assets`
      ejecutados sin errores.
- [ ] Iconos y splash generados desde `assets/`; el icono de tienda mide
      1024×1024 y no lleva esquinas transparentes.
- [ ] `npm run cap:sync` copia el `sitio/` actualizado y el binario abre sin red.
- [ ] El panel «Descargar esta ciudad» está oculto en la app nativa.
- [ ] Audio, mapa y clima funcionan en un Android real y en un iPhone real.
- [ ] VoiceOver y TalkBack recorren cabecera, índice, paradas, audio y
      emergencias en orden lógico.
- [ ] El 112 abre el marcador en ambos sistemas.
- [ ] Audio convertido a Opus o MP3 y tamaño del binario medido antes de subir.
- [ ] Política de privacidad en una URL estable y enlace desde la ficha de
      tienda.
- [ ] Aviso legal y canal de contacto publicados en la web.
- [ ] Ficha de Google Play: descripción, categoría, capturas, icono y gráfico de
      cabecera; formulario de seguridad de datos.
- [ ] Ficha de App Store: descripción, palabras clave, capturas, icono y
      clasificación de contenido.
- [ ] Claves de firma guardadas con copia de seguridad; versión y número de
      compilación incrementados.
- [ ] Ningún dato de accesibilidad se presenta como verificado sin la firma de
      Natalia Blázquez Herrero.

## Cómo revertir

El sitio es estático. Si algo falla tras publicar:

1. Mantener la versión anterior de `sitio/` en el servidor o en el hosting.
2. Volver a subir esa versión.
3. No cambiar los datos de accesibilidad para «arreglar» una página: el problema
   suele ser de cabeceras, rutas o caché.
