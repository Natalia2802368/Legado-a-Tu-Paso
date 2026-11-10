# PRD: Legado a Tu Paso — v1.7

**Producto:** aplicación web instalable (PWA) y app para iOS y Android de turismo
inclusivo en Ciudades Patrimonio de la Humanidad de España.  
**Versión:** 1.7  
**Fecha:** 10 de noviembre de 2026  
**Lanzamiento objetivo:** PWA el 2 de diciembre de 2026; apps nativas cuando haya
cuentas de tienda y toolchain.  
**Estado:** implementado como web y PWA; empaquetado nativo preparado y pendiente
de compilar; publicación pendiente de datos legales y verificación en sitio

## 1. Resumen

Legado a Tu Paso ayuda a personas con necesidades de accesibilidad —y a cualquiera
que viaje con ellas— a descubrir una ciudad patrimonio, entender qué la hace
única, seguir una ruta adaptada, escuchar su historia y resolver lo práctico:
clima, emergencias, aparcamiento accesible y transporte.

La app no es un folleto turístico. Es una herramienta de confianza: cada dato de
accesibilidad debe tener fuente, fecha y estado de verificación.

## 2. Problema

La información turística suele ser genérica y no responde a las preguntas que
determinan si una visita es posible: ¿hay rampas?, ¿cuánto pesa la pendiente?,
¿dónde aparco?, ¿puedo entrar con silla?, ¿hay aseo adaptado?, ¿qué hago si
necesito ayuda? La información está dispersa, desactualizada o mezcla promesas
comerciales con datos verificables.

## 3. Objetivos

- Permitir el flujo completo: descubrir → elegir ciudad → consultar accesibilidad
  → recorrer → escuchar → obtener sello.
- Concentrar información práctica y de emergencia en el mismo lugar.
- Publicar 8 ciudades con contenido completo y audio, y 15 en el catálogo.
- Medir activación, finalización de rutas, uso de audio y consultas prácticas.
- No afirmar accesibilidad sin fuente y verificación.

## 4. No objetivos

- Reservas, pagos o venta de entradas.
- Contenido generado por usuarios.
- Reescribir la app en React Native o Flutter: se usa la misma web con Capacitor.
- Publicar en App Store y Google Play sin cuentas de desarrollador ni toolchain
  nativo.
- Multiidioma en el MVP.
- Realidad aumentada.
- Cuentas y sincronización entre dispositivos.
- Canje físico de recompensas.
- Ocupación de aparcamientos en vivo.
- Disponibilidad de camas, agentes o farmacias en tiempo real.

## 5. Personas

| Persona | Necesidad | Qué valora |
| --- | --- | --- |
| Persona con movilidad reducida | Saber si puede entrar y recorrer | Rampas, pendientes, distancias, aseos |
| Persona ciega o con baja visión | Orientarse y entender el entorno | Audio, braille, texto alternativo |
| Persona sorda | Acceder a la información | Transcripciones, lengua de signos |
| Persona con discapacidad cognitiva | Entender sin sobrecarga | Lectura fácil, pasos claros |
| Persona mayor | Caminar sin riesgo | Descanso, sombra, letra grande |
| Familia con carrito | Circular sin obstáculos | Superficie, ascensores, aseos |
| Persona con lesión temporal | Adaptar la visita | Alternativas y rutas cortas |
| Cuidador o acompañante | Planificar por dos | Información práctica y emergencias |

## 6. Alcance

### Catálogo
15 ciudades patrimonio. Todas con ficha básica.

### Contenido completo y audio (8)
Ávila, Alcalá de Henares, Córdoba, Mérida, Salamanca, Santiago de Compostela,
Segovia y Toledo.

### Módulo práctico
- Clima actual y previsión.
- Emergencias.
- Aparcamiento accesible.
- Transporte accesible.
- Hora local.

### Distribución
- **PWA instalable:** el mismo sitio se instala desde el navegador, sin tiendas
  ni cuenta de usuario. Es el entregable inmediato.
- **Uso sin conexión:** la cáscara (páginas, estilos, fuentes, logos y mapas
  Leaflet) se precarga; cada ciudad se puede descargar con sus fotos y audios.
- **App nativa:** el mismo `sitio/` se empaqueta con Capacitor 8 para Android e
  iOS, con identificador `es.legadoatupaso.app`. La compilación y la publicación
  en tiendas quedan supeditadas a las cuentas y al entorno de compilación.
- **Una sola base de código:** no hay versiones separadas de contenido ni de
  diseño entre web, PWA y app nativa.

## 7. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación |
| --- | --- | --- | --- |
| RF-01 | Catálogo de ciudades | Must | Veo las 15 ciudades y puedo filtrar por necesidad, provincia y nombre. |
| RF-02 | Ficha de ciudad | Must | Incluye resumen, valor patrimonial, accesibilidad, fuente, fecha y CTA de ruta. |
| RF-03 | Ruta adaptada | Must | Cada ciudad completa tiene una ruta con paradas ordenadas, distancia, duración, superficie, pendiente, escalones, descanso y aseos. |
| RF-04 | Mapa y lista | Must | Leaflet con teselas de OpenStreetMap muestra ruta y marcadores; una lista textual equivalente funciona sin mapa. |
| RF-05 | Audio | Must | Play, pausa, avance, retroceso, velocidad, transcripción y memoria de posición. |
| RF-06 | Sellos inclusivos | Must | Se obtienen al completar parada/ruta, escuchar o marcar manualmente; no dependen de GPS. |
| RF-07 | Perfil de accesibilidad | Should | Puedo guardar necesidades en el dispositivo y filtrar con ellas. |
| RF-08 | Clima | Must | Temperatura, sensación, viento, humedad, previsión 3 días, hora de actualización y estado de error. Carga automática al abrir y refresco cada 5 minutos. |
| RF-09 | Emergencias | Must | 112 visible en todas las pantallas; directorio por categoría; teléfonos enlazables; contenido cacheado. |
| RF-10 | Aparcamiento accesible | Must | Lista y mapa con plazas PMR, dirección, coordenadas, número, dimensiones, transferencia, horario, coste y distancia. |
| RF-11 | Transporte accesible | Must | Modos, adaptaciones, contacto y enlace oficial; indicador de tiempo real solo si existe API. |
| RF-12 | Hora local | Could | Reloj con zona horaria de la ciudad. |
| RF-13 | Confianza | Must | Cada dato muestra fuente, fecha y estado: verificado, pendiente, desactualizado o descartado. |
| RF-14 | Compartir | Should | Comparto ciudad, ruta o sello con enlace o hoja nativa. |
| RF-15 | Analítica y consentimiento | Must | Eventos solo tras consentimiento; geolocalización opcional. |
| RF-16 | Instalación PWA | Must | El navegador ofrece instalar la app; en iOS se explica Compartir → Añadir a pantalla de inicio. La app instalada abre en modo `standalone`. |
| RF-17 | Uso sin conexión | Must | Tras una primera visita, las 13 páginas y la navegación funcionan sin red. Cada ciudad se descarga con sus fotos y audios, muestra progreso, permite borrarla y recuerda su estado. |
| RF-18 | Audio sin conexión | Must | El audio descargado se reproduce y se puede buscar sin red mediante respuestas `206` a peticiones `Range`. |
| RF-19 | App nativa | Should | El mismo sitio se empaqueta con Capacitor para Android e iOS; la app nativa incluye todo el contenido y oculta la descarga por ciudad. |

### Reglas de los datos prácticos

- **Clima:** AEMET OpenData como fuente oficial; Open-Meteo como respaldo. No
  llamarlo “en directo”: es la última observación o previsión disponible.
- **Emergencias:** directorio verificado + 112. No prometer disponibilidad en
  tiempo real.
- **Aparcamientos:** dato estático verificado. La ocupación en vivo solo si el
  ayuntamiento publica una API.
- **Transporte:** información estática + enlace oficial. Llegadas en vivo solo
  con GTFS-RT.
- **Farmacias:** teléfono y enlace al colegio oficial; no hacer scraping de
  guardias sin autorización.

## 8. Requisitos no funcionales

- **Accesibilidad:** WCAG 2.2 AA; teclado, foco visible, contraste, texto al
  200 %, movimiento reducido, alternativas a audio y mapa.
- **Rendimiento:** LCP < 2,5 s en 4G; CLS < 0,1; INP < 200 ms. Mapas y audio bajo
  demanda.
- **Privacidad:** sin cuenta obligatoria; progreso y perfil en local;
  consentimiento previo para analítica y terceros; geolocalización opcional.
- **Disponibilidad:** el contenido de emergencias debe funcionar con el último
  dato cacheado.
- **Compatibilidad:** últimas dos versiones de Chrome, Safari, Firefox y Edge;
  iOS y Android actuales. La app nativa usa Capacitor 8 (Android SDK 36, mínimo
  24; iOS 15 o posterior).
- **Instalabilidad:** manifiesto válido, iconos 192/512 y maskable, service
  worker con HTTPS y pantalla de inicio. Sin instalación forzada: la web sigue
  funcionando si el navegador no la admite.
- **Sin conexión:** cáscara precargada y caché de medios persistente e
  independiente de la versión del service worker. El mapa, el tiempo y los
  enlaces externos quedan fuera de la caché y se explican como no disponibles.
- **Almacenamiento:** la descarga de una ciudad ronda 3,3–4,1 MB con los MP3
  actuales; se solicita almacenamiento persistente y se avisa si el sistema
  borra la caché. La app nativa incluye el contenido, no lo descarga.
- **Empaquetado nativo:** `webDir` apunta a `sitio/`; iconos, splash y metadatos
  se generan desde `assets/`. El sitio publica MP3 mono de 64 kbps y pesa
  31,6 MB; los WAV de origen (88,9 MB) no se empaquetan.
- **SEO:** fichas indexables, metadatos, URLs limpias y sitemap.
- **Seguridad:** HTTPS, sin secretos en cliente, claves restringidas por dominio;
  `sw.js` se sirve sin caché larga y la CSP no bloquea el service worker.
- **Contenido:** español; revisión editorial y verificación en sitio.

## 9. Flujos

1. **Descubrir:** inicio → catálogo → filtro → ficha → ruta.
2. **Recorrer:** ruta → parada → audio/transcripción → siguiente → sello.
3. **Resolver:** ficha → práctico → clima / emergencias / parking / transporte.
4. **Emergencia:** cualquier pantalla → 112 → llamada.
5. **Volver:** progreso guardado → continuar ruta.

## 10. Estados y errores

- Sin permiso de ubicación: mapa y lista funcionan; se explica cómo activarlo.
- Sin GPS o señal imprecisa: selección manual de ciudad/parada.
- Audio no disponible: transcripción y reintento.
- Sin conexión: la cáscara y las guías descargadas siguen disponibles, con sus
  fotos y audios; clima, mapa y enlaces externos no. Una banda superior y el pie
  explican qué funciona y qué no.
- Instalación no disponible: se mantiene la web completa y la descarga de audio
  por parada; se explica la limitación sin bloquear el contenido.
- Descarga interrumpida: se conserva lo descargado, se indica cuántos archivos
  faltan y se ofrece reintentar o borrar.
- App nativa sin conexión: todo el contenido va incluido; solo se pierden clima,
  mapa y enlaces externos.
- API de clima caída: último dato con hora y aviso.
- Leaflet u OpenStreetMap no cargan: se mantiene la lista textual, las
  coordenadas y los enlaces de indicaciones.
- Sin datos de parking: enlace al mapa oficial y aviso.
- Sin datos de transporte: enlace a la app oficial.
- Colección vacía: explicación de cómo conseguir el primer sello.

## 11. Métricas

| Métrica | Definición | Objetivo inicial |
| --- | --- | --- |
| Activación | Ficha → ruta iniciada | ≥ 25 % |
| Finalización | Rutas terminadas / iniciadas | ≥ 40 % |
| Audio | Rutas con audio reproducido | ≥ 30 % |
| Sellos | Sellos por sesión activa | ≥ 1 |
| Práctico | Fichas con clic en clima, parking o transporte | ≥ 20 % |
| Emergencias | Aperturas del panel / sesiones | Medir, sin objetivo |
| Retorno | Usuarios que vuelven en 7 días | ≥ 10 % |
| Calidad | Datos con fuente y fecha | 100 % |
| Frescura | Datos verificados hace < 90 días | ≥ 90 % |

## 12. Modelo de datos

### Ciudad
`id`, `nombre`, `provincia`, `comunidad`, `unesco_desde`, `lat`, `lon`,
`timezone`, `resumen`, `accesibilidad_resumen`, `fuente_principal`,
`verificado_en`.

### Parada
`id`, `orden`, `nombre`, `lat`, `lon`, `descripcion`, `acceso`, `superficie`,
`pendiente`, `escalones`, `aseo`, `descanso`, `audio`, `transcripcion`,
`alternativas`, `fuente`, `estado`.

### Emergencia
`categoria`, `nombre`, `telefono`, `direccion`, `horario`, `fuente`,
`verificado_en`.

### Aparcamiento
`nombre`, `direccion`, `lat`, `lon`, `plazas_pmr`, `dimensiones`,
`transferencia`, `horario`, `coste`, `distancia_ruta`, `superficie`, `fuente`,
`estado`.

### Transporte
`modo`, `operador`, `accesibilidad`, `contacto`, `url_oficial`, `tiempo_real`,
`fuente`, `verificado_en`.

### Clima
`proveedor`, `lat`, `lon`, `timezone`, `actualizado_en`.

### Foto
`url`, `autor`, `licencia`, `licencia_url`, `origen_url`, `alt`, `estado`.

## 13. Mapas

- Leaflet 1.9.4 se sirve desde el propio sitio (BSD-2); las teselas vienen de
  OpenStreetMap. No hay clave de API, cookies de terceros ni cuenta de
  facturación.
- La atribución de OpenStreetMap es visible dentro de cada mapa y en la página
  de créditos.
- El uso de teselas públicas debe respetar la política de uso razonable. Si el
  tráfico crece, hay que contratar un proveedor o autoalojar las teselas.
- El contenido de OpenStreetMap se puede cachear según su licencia ODbL, pero
  las teselas públicas no se deben precargar de forma masiva.
- OpenStreetMap no garantiza rutas sin escalones. La accesibilidad es dato
  propio y verificado aparte.
- Toda ruta y todo aparcamiento necesitan lista textual equivalente. En la
  portada, la lista de ciudades es la alternativa operable al mapa.
- El mapa de portada usa marcadores decorativos no enfocables; el mapa de cada
  ruta usa marcadores numerados con nombre accesible.
- Google Maps y OpenStreetMap se usan solo como enlaces de indicaciones, nunca
  como fuente de accesibilidad.

### Plan de verificación en sitio

`verificacion.html` es la herramienta de campo: reúne por ciudad los datos
publicados con su fuente y estado, las tareas del checklist y un bloque de firma.
Se imprime en A4, con una página por ciudad (10 páginas en total). Su función es
registrar la comprobación, no cambiarla: ningún dato pasa a `verificado`
sin firma ni fuente.

## 14. Contenido y verificación

### Jerarquía de fuentes
1. Ayuntamiento y oficina de turismo.
2. Junta/Comunidad y Turespaña/Spain.info.
3. Guías oficiales de accesibilidad.
4. Entidades de personas con discapacidad.
5. OpenStreetMap y Google Maps como pistas, nunca como verdad final.

### Estados
- `verificado`: comprobado en sitio. En los teléfonos de emergencia, contrastado
  con la fuente oficial.
- `pendiente`: dato de fuente oficial, web o visita, todavía sin comprobación en
  sitio; no se publica como accesible.
- `desactualizado`: más de 12 meses sin revisar.
- `descartado`: dato retirado; no se muestra como vigente.

No existe un estado `fuente_oficial`: la fuente se anota en su columna y el dato
sigue en `pendiente` hasta la visita.

### Fotos
- Solo dominio público, CC0, CC BY o CC BY-SA.
- Crédito visible con autor, licencia y enlace.
- Revisión visual obligatoria: encuadre, personas identificables, vigencia.
- Texto alternativo descriptivo.

## 15. Plan de 4 semanas (Plan A)

| Semana | Entregable |
| --- | --- |
| 1 | Modelo, sistema de diseño, Ávila completa y 3 fichas básicas |
| 2 | 4 ciudades restantes, rutas y mapa; parking/transporte de 4 piloto |
| 3 | Audio de las 8, emergencias, clima, sellos y transcripciones |
| 4 | Auditoría de accesibilidad, revisión de contenido, publicación |

**Ruta crítica:** contenido verificado de emergencias, parking y transporte. Si no
está listo, se publica con 4 ciudades completas y el resto como “próximamente”.

### Estado a 10 de noviembre de 2026

| Entregable | Estado |
| --- | --- |
| Modelo y sistema de diseño | Hecho; emblema vectorial definitivo y tipografías OFL autoalojadas |
| 8 fichas completas | Hecho, en estado `borrador` |
| Fichas de monumento | Segovia: catedral y acueducto con 46 datos de ficha oficial, todos `pendiente` |
| Rutas con coordenadas reales | Hecho (Nominatim) |
| Clima con fuente y hora | Hecho (Open-Meteo); carga automática y refresco cada 5 minutos |
| Directorio de emergencias | Parcial: 112 y números nacionales; locales `pendiente` |
| Aparcamiento PMR | Parcial: OSM; Mérida sin datos y Alcalá, Córdoba y Segovia con datos parciales |
| Transporte | Parcial: operador y contacto; flota sin confirmar |
| 64 guiones de audio | Hecho |
| 64 audios TTS provisionales | Hecho: MP3 mono 64 kbps, 22.050 Hz; WAV de origen conservados sin publicar |
| Grabación con voz humana | Pendiente |
| Verificación en sitio | Asignada a Natalia Blázquez Herrero; pendiente; plan imprimible, guía de campo y CSV en `verificacion/` |
| App web implementada | Hecho: sitio estático de 13 páginas en `sitio/`, con 404, manifest y robots |
| PWA instalable | Hecho: manifiesto con atajos y capturas, iconos, service worker y registro condicionado en Capacitor |
| Modo sin conexión | Hecho: cáscara de 35 archivos precargada, descarga de fotos y audios por ciudad con progreso y borrado |
| Audio sin conexión | Hecho: caché persistente y respuestas `Range` con `206`, probadas en local |
| App nativa con Capacitor | Preparada: `package.json`, `capacitor.config.json`, iconos y splash; sin compilar por falta de toolchain |
| Cuentas y publicación en tiendas | Pendiente: Google Play, Apple Developer, firma y fichas de tienda |
| Mapas | Hecho: Leaflet 1.9.4 + OpenStreetMap, sin clave; marcadores visuales y lista textual operable |
| Logo y tipografía de marca | Hecho: logo, emblema y favicon SVG propios; Literata 600 + Atkinson Hyperlegible 400/700 |
| Iconos de instalación y tarjeta social | Hecho: PNG 192/512, maskable, apple-touch, ICO y OG 1200×630 |
| Paquete de publicación | Hecho: Netlify, Apache, Nginx, cabeceras CSP y lista de comprobación |
| Aviso legal, privacidad y contacto | Pendiente: faltan los datos del titular y el canal |
| Dominio, HTTPS y sitemap | Pendiente: sin dominio definitivo; el generador acepta `LEGADO_URL` |
| Auditoría externa de accesibilidad | Pendiente |
| Materiales de referencia | Revisados; qué se adoptó y qué no, en `materiales/LEEME.md` |
| Contexto municipal de Segovia | Hecho: Plan Integral y Gemelo Digital citados con sus límites, sin atribuirles verificación en sitio |

**Bloqueos de lanzamiento:** sin aviso legal, privacidad y contacto no se publica
una web identificable en España. La verificación en sitio y la voz humana siguen
abiertas. El plan de publicación está en
`publicacion/COMPROBACION-PUBLICACION.md`.

## 16. Criterios de lanzamiento

- [x] 15 fichas, 8 completas.
- [x] 8 rutas con paradas y datos de acceso.
- [x] Audio y transcripción en las 8.
- [ ] Emergencias con 112 y directorio local.
- [x] Clima con fuente y hora, carga automática y refresco.
- [x] Mapa Leaflet + lista textual en portada y en las 8 rutas.
- [x] Marca aplicada: logotipo SVG, emblema, favicon y tipografías autoalojadas.
- [ ] Parking y transporte de 4 ciudades piloto verificados.
- [ ] Plan de verificación impreso y firmado para las 8 ciudades.
- [ ] Sin errores P0/P1.
- [ ] WCAG 2.2 AA verificado por una persona externa.
- [x] PWA instalable con manifiesto, iconos y service worker.
- [x] Cáscara y guías descargadas funcionan sin conexión, con audio `Range`.
- [ ] Prueba de la PWA en un iPhone y un Android reales.
- [ ] App nativa compilada y probada en dispositivos reales.
- [ ] Fichas, capturas y política de privacidad para App Store y Google Play.
- [ ] Analítica y consentimiento (decisión actual: no hay analítica ni cookies).
- [x] Aviso de información orientativa y fecha de verificación.

## 17. Riesgos

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| Datos de accesibilidad falsos o desactualizados | Alto | Fuente, fecha y verificación en sitio |
| Teléfonos de emergencia incorrectos | Muy alto | Confirmación con ayuntamiento y 112 |
| 8 ciudades en 4 semanas | Alto | Plan A: 4 completas + 4 básicas |
| Fotos inadecuadas | Medio | Revisión visual y licencias |
| Teselas de OpenStreetMap no disponibles o uso excesivo | Medio | Lista textual siempre; proveedor o autoalojado si crece el tráfico |
| Falta de API de transporte | Medio | Enlace oficial; tiempo real en fase 2 |
| Audio sin grabar | Medio | Guiones listos; TTS como respaldo |
| Service worker obsoleto o caché corrupta | Medio | Versión calculada por contenido, cáscara y medios en cachés separadas, borrado por ciudad |
| Caché borrada por el sistema | Medio | Aviso claro y descarga repetible; almacenamiento persistente cuando se inicia la descarga |
| App nativa demasiado pesada | Medio | Audio ya convertido a MP3 de 64 kbps; medir el binario tras `cap sync` |
| Rechazo en tiendas por privacidad o contenido | Medio | Política de privacidad, aviso legal y declaración de accesibilidad antes de enviar |
| Sin cuentas o Mac para compilar | Alto | PWA como entregable inmediato; empaquetado preparado para un equipo o CI con el entorno completo |

## 18. Preguntas abiertas

1. ~~¿Voz humana o sintética para los 8 audios?~~ Resuelto: TTS provisional +
   guiones para voz humana.
2. ~~¿Logo y tipografía definitivos?~~ Resuelto: logotipo vectorial propio y
   Literata 600 + Atkinson Hyperlegible, ambas OFL y autoalojadas.
3. ~~¿Quién verifica en sitio accesibilidad, teléfonos y parking?~~ Resuelto:
   Natalia Blázquez Herrero, pendiente de ejecución.
4. ~~¿Hay clave de Google Maps y presupuesto?~~ Resuelto: no hay clave; se usa
   Leaflet + OpenStreetMap.
5. ¿Se integra GTFS-RT en alguna ciudad?
6. ¿Se publican las 15 fichas o solo 8?
7. ~~¿Web, PWA o app nativa?~~ Resuelto: PWA ya y app nativa con Capacitor
   cuando existan cuentas y toolchain; una sola base de código.
8. ¿Cuándo se abren las cuentas de Google Play y Apple Developer, y quién asume
   su coste y la firma de las apps?
9. ¿El identificador `es.legadoatupaso.app` se mantiene o se cambia a un dominio
   propio antes de la primera publicación en tiendas? No se puede cambiar después.
