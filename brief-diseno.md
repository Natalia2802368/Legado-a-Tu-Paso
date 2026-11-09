# Brief de diseño: Legado a Tu Paso — v1.7

## 1. Contexto

Web app mobile-first de turismo inclusivo para las Ciudades Patrimonio de la
Humanidad de España, instalable como PWA y empaquetable como app nativa para iOS
y Android. El público es diverso: personas con discapacidad física, visual,
auditiva o cognitiva, personas mayores, familias con carritos, personas con
lesiones temporales y sus acompañantes.

La app debe transmitir **confianza, calma y rigor**, no urgencia comercial. La
accesibilidad es el producto, no una capa decorativa. La experiencia debe
funcionar igual de bien en el navegador, instalada desde la pantalla de inicio y
dentro de la app nativa, también sin conexión.

## 2. Objetivo

Que una persona entienda en menos de un minuto si puede visitar una ciudad, qué
ruta le conviene y dónde resolver sus necesidades prácticas, sin sentirse
abrumada ni engañada.

## 3. Idea central

**“El patrimonio se vive a tu paso.”**

## 4. Mensajes

1. Quince ciudades, una historia común.
2. Rutas que se adaptan a tu ritmo.
3. Información verificada, con fuente y fecha.
4. Voces e historias en cada parada.
5. Lo práctico también importa: clima, emergencias, parking y transporte.
6. Llévatela en el móvil: se instala y conserva las guías descargadas sin
   conexión.

## 5. Marca

### Paleta de marca

| Token | Color | Uso | Contraste sobre `#FAF9F7` |
| --- | --- | --- | --- |
| `--bg` | `#FAF9F7` | Fondo principal | — |
| `--surface` | `#F7F6F4` | Tarjetas y bloques | — |
| `--ink` | `#30160D` | Texto principal | 16,01:1 |
| `--primary` | `#5E2E1B` | Botones y enlaces | 10,60:1 |
| `--accent` | `#592411` | Detalles y estados | 11,84:1 |
| `--muted` | `#8D9094` | Solo texto grande o iconos | 3,05:1 |
| `--border` | `#C6C8CB` | Líneas y separadores | 1,59:1 |

Reglas:
- `--muted` no se usa para texto normal.
- `--border` no se usa para texto.
- Ningún estado se comunica solo con color.

### Tipografía

- **Titulares y marca:** Literata 600, una serif editorial de TypeTogether.
- **Texto e interfaz:** Atkinson Hyperlegible 400/700, del Braille Institute.
- **Licencia:** ambas SIL Open Font License, autoalojadas en WOFF2 con
  subconjuntos latin y latin-ext. No hay dependencia de fuentes instaladas.
- **Mínimos:** 16 px en cuerpo, 1,5 de interlineado, 200 % de zoom sin pérdida.
- **Pesos:** Literata solo se sirve en 600; Atkinson en 400 y 700.

### Logo

La marca está cerrada y vectorizada:

- **Emblema:** círculo en tinta `#30160D` con una puerta recortada abierta por
  abajo. La misma forma aparece en el favicon sobre una teja redondeada.
- **Wordmark:** «Legado» en Literata 700 (tinta) y «a Tu Paso» en Literata 400
  (teja), convertidos a trazos. El SVG no depende de la fuente instalada.
- **Archivos:** `sitio/assets/logo.svg` (lockup horizontal),
  `sitio/assets/logo-claro.svg` (para fondos oscuros),
  `sitio/assets/logo-emblema.svg`, `sitio/assets/logo-emblema-claro.svg` y
  `sitio/assets/favicon.svg` (icono cuadrado). La hoja de marca interna está en
  `marca.html`.
- **Uso en cabecera:** el lockup se inserta en línea a 40 px de alto (36 px en
  pantallas menores de 380 px), dentro de un enlace de 44 px de alto.
- **Modo de alto contraste:** los trazos pasan a `CanvasText` y la máscara del
  emblema conserva el recorte.
- **Generación:** `python herramientas/crear_marca.py` reconstruye logo,
  emblema, favicon y subconjuntos de Literata desde la fuente variable.

### Iconos de app y pantallas de inicio

- **PWA:** `icono-192.png`, `icono-512.png`, `icono-maskable-512.png` (fondo
  tinta completo, emblema dentro de la zona segura) y `apple-touch-icon.png`.
  El maskable no lleva esquinas transparentes.
- **Tiendas:** `assets/icon-only.png` (1024×1024, sin esquinas redondeadas: la
  tienda aplica su máscara), `icon-foreground.png` e `icon-background.png` para
  el icono adaptativo de Android.
- **Pantallas de inicio:** `assets/splash.png` (fondo papel, emblema tinta) y
  `splash-dark.png` (fondo tinta, emblema papel), 2732×2732.
- **Regla:** el emblema nunca se estira, se rota ni se separa del círculo. En
  iOS el icono se muestra ya redondeado por el sistema; no se añade un borde
  extra.
- **Generación:** `python herramientas/crear_iconos.py` produce los iconos PWA,
  el ICO y las fuentes nativas. `@capacitor/assets` genera después las tallas de
  cada plataforma.

## 6. Principios de diseño

1. **Claridad antes que elegancia.** Si hay que elegir, gana la comprensión.
2. **La accesibilidad se ve.** Los datos de acceso están en la ficha, no escondidos.
3. **Una cosa por pantalla.** Especialmente en ruta y emergencias.
4. **Confianza visible.** Fuente, fecha y estado en cada dato práctico.
5. **Alternativa siempre.** Mapa → lista. Audio → transcripción. Icono → texto.
6. **Sin oscuros patrones.** Nada de registro obligatorio, urgencia falsa ni
   geolocalización forzada.

## 7. Pantallas

| Pantalla | Contenido clave |
| --- | --- |
| Inicio | Propuesta de valor, buscador, ciudades destacadas, acceso a emergencias |
| Catálogo | 15 ciudades, filtros por necesidad y provincia |
| Ficha de ciudad | Resumen, patrimonio, accesibilidad, fuentes, CTA de ruta |
| Ruta | Paradas, mapa/lista, distancia, superficie, pendiente, descanso |
| Parada | Qué es, acceso, audio, transcripción, alternativa táctil |
| Práctico | Clima, emergencias, parking y transporte |
| Emergencias | 112 destacado, directorio por categoría, teléfonos |
| Parking | Lista y mapa, plazas PMR, dimensiones, horario, coste |
| Transporte | Modos, adaptaciones, contacto, enlace oficial |
| Audio | Player grande, transcripción, velocidad, posición |
| Verificación | Plan de campo por ciudad, datos por confirmar, tareas y firma; versión impresa A4 |
| Sellos | Colección, progreso, compartir |
| Instalar app | Botón en el pie, instrucción para iOS y confirmación de app instalada |
| Descarga sin conexión | Tamaño, botón de descarga, progreso, estado guardado, borrado y reintento |
| Sin conexión | Banda superior, estado en el pie y explicación de qué sigue funcionando |
| App nativa | Misma interfaz dentro de Capacitor; sin panel de descarga porque el contenido va incluido |
| Estados | Vacío, error, sin conexión, sin permiso, dato pendiente |

## 8. Componentes

- **Barra de confianza:** “Fuente: Ayuntamiento de Ávila · Verificado el 2/11/2026”.
- **Badge de estado:** verificado, pendiente, desactualizado, descartado.
- **Tarjeta de clima:** icono + texto + temperatura + “Actualizado a las 20:45”.
- **Botonera de emergencia:** 112 como acción principal, 44×44 px mínimo.
- **Ficha de accesibilidad:** iconos con etiqueta textual, no solo símbolos.
- **Lista de paradas:** equivalente textual del mapa.
- **Player de audio:** controles grandes, transcripción desplegable.
- **Aviso de dato pendiente:** “Estamos verificando este dato. Confirma con la
  oficina de turismo.”
- **Ficha de verificación:** tabla de datos publicados, casillas para marcar y
  líneas de firma; en impresión, una ciudad por página.
- **Panel de descarga:** título, tamaño en MB, botón primario, barra de progreso,
  estado en `role="status"` y botón secundario para borrar. Nunca descarga solo:
  siempre lo inicia la persona.
- **Aviso de conexión:** banda fina bajo la cabecera, texto claro y cierre
  automático al volver la red; no tapa el contenido ni el foco.
- **Botón de instalación:** discreto en el pie, con el mismo lenguaje que el
  resto de botones; en iOS se sustituye por una instrucción breve, no por un
  botón inerte.

## 9. Accesibilidad

- WCAG 2.2 AA.
- Navegación completa por teclado y foco visible.
- Contraste mínimo 4,5:1 en texto normal y 3:1 en texto grande.
- Áreas táctiles de 44×44 px.
- Texto ampliable al 200 % sin scroll horizontal.
- `prefers-reduced-motion` respetado.
- Alternativa textual a mapas, iconos, audio y vídeo.
- Transcripción y subtítulos.
- Lectura fácil para contenidos clave.
- Formularios con etiquetas persistentes y errores claros.
- El módulo de emergencias funciona sin geolocalización y con datos cacheados.
- Leaflet con teselas de OpenStreetMap: el mapa se carga sin clave ni cookies de
  terceros; la lista textual no depende del mapa. Los marcadores del mapa de
  portada son decorativos y la lista de ciudades es la alternativa operable.
- **Áreas seguras:** `viewport-fit=cover` y `env(safe-area-inset-*)` en
  contenedores, cabecera, pie y banda de conexión para no quedar bajo el notch ni
  la barra de gestos.
- **Modo instalado:** la app se comprueba con `display-mode: standalone`; no se
  muestra el botón de instalar cuando ya está instalada.
- **Sin conexión:** el estado nunca se comunica solo por color; se anuncia en
  `role="status"` y se explica qué queda disponible.
- **Progreso:** `<progress>` nativo con etiqueta accesible y porcentaje textual;
  el estado se anuncia sin robar el foco.
- **App nativa:** se respetan las barras del sistema y el tamaño táctil; el panel
  de descarga no aparece porque el contenido ya está incluido.

## 10. Entregables

| Pieza | Formato | Fecha | Estado |
| --- | --- | --- | --- |
| Sistema visual: color, tipografía, espaciado, iconos, componentes | Figma + tokens | Semana 1 | Implementado en CSS y `marca.html` |
| Pantallas móvil 390×844 y escritorio 1440 | Figma | Semana 1-2 | Implementado y revisado a 320, 390 y 785 px |
| Prototipo navegable del flujo descubrir → ruta → parada → sello | Figma | Semana 2 | Implementado como sitio estático |
| Pantallas de práctico: clima, emergencias, parking, transporte | Figma | Semana 2 | Implementado en las 8 fichas |
| Anotaciones de accesibilidad y estados | Figma | Semana 2 | Implementado: estados, avisos y foco visible |
| Handoff: especificaciones, assets y textos alt | Figma + exportables | Semana 3 | Assets en `sitio/assets/`, textos alt en el generador |
| Logotipo, emblema, favicon e iconos de instalación | SVG + PNG + ICO | — | Hecho y verificado |
| Tarjeta social 1200×630 | PNG | — | Hecho (`sitio/assets/social/og.png`) |
| Hoja de marca interna | HTML | — | Hecho (`marca.html`) |
| Iconos y splash para las tiendas | PNG 1024×1024 y 2732×2732 | — | Hecho (`assets/`); falta generar tallas con `@capacitor/assets` |
| Capturas de la app para el manifiesto | PNG 390×844 y 1280×800 | — | Hecho (`sitio/assets/capturas/`) |
| Interfaz de instalación, descarga y sin conexión | HTML + CSS + JS | — | Hecho y probado en navegador de escritorio |
| Prueba visual en iPhone y Android reales | Dispositivo | Antes de tiendas | Pendiente |

## 11. Tono y referencias

- **Personalidad:** cercano, culto, sereno, riguroso.
- **Sí:** aire, fotografía protagonista, tipografía legible, lenguaje directo.
- **No:** folleto turístico, dorados institucionales, saturación, tecnicismos,
  falsa urgencia.
- **Referencias:** editoriales de viajes con fotografía amplia y texto sereno;
  guías de patrimonio con datos y fuentes visibles. Evitar folletos con dorados
  institucionales, mayúsculas sostenidas y falsa urgencia.

## 12. Restricciones

- Mobile-first y responsive; misma interfaz en web, PWA instalada y app nativa.
- Áreas seguras de iOS y Android respetadas; sin contenido bajo el notch.
- La instalación y la descarga son opcionales: nunca bloquean la lectura.
- Leaflet + OpenStreetMap, sin API key, con atribución y alternativa textual.
- Audio con transcripción.
- Fotos libres con crédito.
- Contenido en español.
- Sin registro obligatorio.
- Plazo: 4 semanas.
- Logo y tipografía: definidos en la sección 5.
- Materiales de Stitch: solo referencia de interacción; no se adoptaron su
  paleta, su tipografía ni sus afirmaciones acústicas o AAA (ver
  `materiales/LEEME.md`).

## 13. Aprobación

- Rondas: 2.
- Aprueba: responsable del proyecto (por confirmar antes de publicar).
- Criterios:
  - Se entiende sin explicación previa.
  - La accesibilidad está visible y no requiere buscar.
  - El flujo de emergencia está a un toque.
  - Ningún dato práctico carece de fuente/fecha.
  - La interfaz funciona con teclado, lector de pantalla y zoom.
  - La instalación y la descarga se entienden sin explicación previa.
  - Sin conexión, se distingue lo disponible de lo que necesita red.

## 14. No incluye

- Creación de marca desde cero.
- Producción de fotografía.
- Producción de audio.
- Desarrollo frontend.
- Cartografía propia.
