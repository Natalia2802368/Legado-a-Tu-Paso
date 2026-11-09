# Paquete de publicación

El sitio que se publica es **el contenido de `sitio/`**. No hay backend, base de
datos ni proceso de build en el servidor: son HTML, CSS, JavaScript, imágenes,
fuentes, audio y CSV.

## Qué hay aquí

| Archivo | Para qué |
| --- | --- |
| `netlify.toml` | Netlify o Cloudflare Pages: publicar la carpeta `sitio/`. |
| `htaccess.txt` | Apache 2.4: copiar como `sitio/.htaccess`. |
| `nginx.conf` | Nginx: incluir en el bloque `server`. |
| `COMPROBACION-PUBLICACION.md` | Lista de comprobaciones antes de abrir al público. |
| `APP-MOVIL.md` | PWA, empaquetado con Capacitor y publicación en App Store y Google Play. |

Las cabeceras de seguridad y caché para Netlify y Cloudflare Pages están en
`sitio/_headers`.

## Antes de generar la versión final

1. Define el dominio público y pásalo al generador:

   ```powershell
   cd C:\Users\Admin\Documents\Legado-a-Tu-Paso
   $env:LEGADO_URL = "https://www.ejemplo.es"
   python herramientas\crear_iconos.py
   python herramientas\generar_sitio.py
   ```

   Con `LEGADO_URL`, el generador añade `canonical`, `og:url`, la imagen social
   absoluta, `sitemap.xml` y la línea `Sitemap:` de `robots.txt`. Sin dominio, el
   sitio funciona igual, pero no se publica sitemap ni URL canónica.

2. Confirma que el dominio y el certificado HTTPS están activos.

3. Revisa el aviso legal y el canal de contacto. Sin ellos no se debe publicar
   una web de un proyecto identificable en España. Están pendientes de que el
   cliente facilite los datos.

## Subida

- **Netlify / Cloudflare Pages:** conecta el repositorio o sube `sitio/` como
  directorio de publicación. `netlify.toml` ya indica `publish = "sitio"`.
- **Apache:** sube el contenido de `sitio/` y copia `htaccess.txt` como
  `.htaccess` en la raíz publicada.
- **Nginx:** sube `sitio/` y adapta `nginx.conf` al bloque del dominio.
- **GitHub Pages:** sube `sitio/` a la rama de publicación. No hay `_headers`
  ni `.htaccess`; las cabeceras de seguridad no se pueden aplicar desde el
  propio repositorio. Si la seguridad es requisito, usa Cloudflare delante.

## PWA y app nativa

El contenido de `sitio/` es a la vez la web, la PWA instalable y la app nativa:

- **PWA:** se publica con el resto del sitio. Necesita HTTPS, `sw.js` en la raíz
  y `manifest.webmanifest`. No requiere tiendas ni cuenta de usuario.
- **Caché del service worker:** `sw.js` debe servirse con `Cache-Control:
  no-cache` (o `max-age=0, must-revalidate`). Las cabeceras de `sitio/_headers`,
  `htaccess.txt` y `nginx.conf` ya lo incluyen. Si el hosting cachea `sw.js`
  durante días, las actualizaciones tardan en llegar.
- **App nativa:** se empaqueta con Capacitor desde el mismo `sitio/`. Requiere
  Node 22+, JDK 21, Android SDK y, para iOS, macOS con Xcode 26+. La guía
  completa está en `APP-MOVIL.md`.
- **Antes de tiendas:** aviso legal y política de privacidad publicados, audio
  convertido a Opus/MP3 y prueba en dispositivos reales con VoiceOver y TalkBack.

## Tipos MIME imprescindibles

| Extensión | Tipo |
| --- | --- |
| `.html` | `text/html; charset=utf-8` |
| `.css` | `text/css` |
| `.js` | `text/javascript` |
| `.webp` | `image/webp` |
| `.svg` | `image/svg+xml` |
| `.woff2` | `font/woff2` |
| `.wav` | `audio/wav` |
| `.mp3` | `audio/mpeg` |
| `.webmanifest` | `application/manifest+json` |
| `.xml` | `application/xml` |
| `.csv` | `text/csv; charset=utf-8` |

## Lo que no se publica

- `contenido/`, `audio/` (fuente), `fotos-originales/`, `materiales/`,
  `herramientas/`, `verificacion/` (los Markdown internos) y `capturas/`.
- Los CSV, la guía de campo y la plantilla de ficha sí se publican, pero solo
  los de `sitio/verificacion/`. Los Markdown internos de `verificacion/` no se
  publican directamente.
- Las fotos originales no se publican: solo los WebP de `sitio/assets/fotos/`.
- `marca.html` es interno y no forma parte de las páginas publicadas.
