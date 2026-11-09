# Guía de trabajo de campo

**Proyecto:** Legado a Tu Paso
**Responsable de verificación:** Natalia Blázquez Herrero
**Fecha límite:** 2 de diciembre de 2026
**Estado:** pendiente, no completada

Esta guía explica cómo convertir los datos publicados como `pendiente` en datos
`verificado`. La regla es sencilla: **solo se marca lo que se ha visto o medido**.
Tener una fuente oficial no cambia el estado: la fuente se anota en su columna y
el dato sigue `pendiente` hasta la inspección. Si hay dudas, se queda pendiente y
se anota la duda.

## 1. Qué hay que verificar

| Archivo | Contenido | Filas |
| --- | --- | --- |
| `datos-accesibilidad.csv` | Los datos de accesibilidad publicados en las 8 guías | 96 |
| `tareas.csv` | Las tareas pendientes de cada ciudad | 69 |
| `segovia-monumentos.csv` | Fichas oficiales de la catedral y el acueducto de Segovia | 46 |

Los tres están en `verificacion/` y también en `sitio/verificacion/` para
descargarlos desde el plan de verificación. Se abren con Excel, LibreOffice o
Google Sheets. Usan UTF-8 con BOM y separador `;`.

El plan imprimible tiene 10 páginas A4: portada, método y una página por ciudad.
Sirve para llevar al campo, pero el CSV es el que se entrega relleno.

## 2. Antes de salir

1. Imprime el plan desde `sitio/verificacion.html` con el botón **Imprimir el
   plan completo**.
2. Descarga los tres CSV y comprueba que abren bien.
3. Revisa la ruta publicada de cada ciudad y anota las paradas que vas a visitar.
4. Confirma horarios y acceso con el monumento u oficina de turismo. No des por
   hecho que una puerta secundaria está abierta.
5. Para Segovia, puedes consultar antes el [Gemelo Digital
   municipal](https://segovia.es/area/obras-servicios-e-infraestructuras-municipales/gemelo-digital-de-segovia)
   para perfiles de elevación y geometrías de edificios. No lo uses como prueba
   del pavimento, de los obstáculos ni del estado de conservación: el protocolo
   municipal no garantiza la ausencia de errores ni la actualización permanente.
   Si reutilizas sus datos, cita «Origen de los datos: Ayuntamiento de Segovia»
   y la fecha de actualización.
6. Prepara el material:
   - cinta métrica de 5 m y, si es posible, medidor láser;
   - nivel de burbuja o app de inclinación;
   - linterna para zonas de penumbra;
   - cámara o móvil con ubicación desactivada para las fotos;
   - plan impreso, lápiz y tabla de apoyo;
   - teléfono cargado y el 112 identificado.
7. Si vas a comprobar bucles magnéticos, lleva un receptor compatible o pide al
   recinto que lo demuestre. No se marca «sí» por ver el cartel.

## 3. Qué significa cada estado

| Estado | Cuándo se usa |
| --- | --- |
| `pendiente` | No se ha comprobado, o la comprobación no es concluyente. Es el estado de partida. |
| `verificado` | Se ha visto o medido en sitio, con fecha y persona. |
| `desactualizado` | Se verificó hace más de 12 meses o el recinto ha cambiado. |
| `descartado` | El dato ya no aplica (por ejemplo, una parada retirada). Se explica en notas. |

Para pasar una fila a `verificado` hacen falta **tres cosas**:

1. el resultado observado, escrito en la columna `resultado`;
2. la fecha de la visita, en `fecha_visita` (formato `AAAA-MM-DD`);
3. el nombre de quien lo comprueba, en `notas` o en la ficha firmada.

Si el valor publicado era incorrecto, se escribe el valor correcto en
`resultado` y se avisa para corregir el contenido. No se cambia el CSV y se deja
la web como estaba.

## 4. Cómo medir

- **Pendiente de rampa:** divide la altura salvada entre la longitud horizontal
  y multiplica por 100. Una rampa de 9 cm en 50 cm da un 18 %, no el 24,9 % que
  figura en la ficha de la catedral. Mide la longitud real, no la de la base.
- **Ancho de paso:** mide la luz libre entre la hoja abierta y el marco, no el
  ancho total de la puerta.
- **Escalones:** altura de contrahuella y profundidad de huella. Anota si hay
  franja antideslizante y contraste de borde.
- **Giro en silla:** comprueba si se puede girar 360° sin salir del espacio. Si
  no cabe, mide el diámetro libre.
- **Mostradores:** altura y si se puede aproximar de frente. Un mostrador alto
  puede tener una parte baja usable; compruébalo.
- **Aseos:** puerta, giro, barras de apoyo, altura del inodoro y del lavabo,
  espacio lateral de transferencia. Si no hay aseo adaptado, se dice.
- **Bucle magnético:** comprueba que está encendido y que se oye con el receptor.
  Un cartel no es una prueba.
- **Iluminación:** si no hay luxómetro, describe zonas de penumbra, reflejos y
  cambios bruscos de luz. No inventes valores.
- **Superficie:** distingue losetas lisas, empedrado irregular, adoquín, tierra y
  zonas con resbalones por lluvia.
- **Recorrido:** valora la continuidad. Un acceso bueno no sirve si el itinerario
  siguiente tiene escalones sin alternativa.

## 5. Fotos y privacidad

- Haz una foto general del acceso y otra del detalle que se mide.
- No fotografíes personas identificables sin permiso. Si aparecen, difumina o
  descarta la foto.
- Nombra los archivos así: `ciudad-parada-detalle-AAAAMMDD.jpg`.
- No subas fotos de campo a la web sin revisar encuadre, derechos y vigencia.
- Las fotos actuales de Wikimedia Commons siguen pendientes de revisión visual
  humana; no las sustituyas sin actualizar el crédito.

## 6. Cómo rellenar el CSV

Columnas de `datos-accesibilidad.csv`:

| Columna | Qué escribir |
| --- | --- |
| `valor_publicado` | No se toca: es lo que dice la web hoy. |
| `fuente` | No se toca: es la fuente con la que se publicó. |
| `estado` | `verificado`, `pendiente`, `desactualizado` o `descartado`. |
| `fecha_visita` | `AAAA-MM-DD`. |
| `resultado` | Lo observado, con unidades. Si coincide, `Confirmado`. |
| `notas` | Diferencias, dudas, nombre de quien comprueba. |

Columnas de `tareas.csv`: mismas reglas, más `resultado` para decir si la tarea
se completó, no aplica o sigue pendiente.

Columnas de `segovia-monumentos.csv`: mismas reglas. `fecha_inspeccion_ficha`
dice `no indicada` porque las fichas oficiales no la traen; no la inventes.

## 7. Después de la visita

1. Pasa los datos del papel al CSV el mismo día, mientras recuerdas las medidas.
2. Revisa que no haya filas `verificado` sin fecha ni resultado.
3. Entrega los tres CSV y las fichas firmadas.
4. Avisa de las contradicciones: sobre todo la rampa de la catedral, las obras de
   la Puerta del Perdón, las plazas PMR y los teléfonos locales.
5. El contenido se corrige en `contenido/*.md`, se regenera el sitio y se
   vuelve a imprimir el plan.
6. Los avisos de «pendiente de verificación» solo se retiran cuando los datos
   críticos de esa ciudad estén verificados y firmados.

## 8. Criterios para no publicar

No se publica como accesible, ni se retira el aviso, si:

- no hay fecha de visita;
- la medida es una estimación sin instrumento;
- solo se ha consultado una web o un folleto, sin ver el espacio;
- la persona que comprueba no puede confirmar el uso real (por ejemplo, un aseo
  cerrado con llave);
- hay una contradicción sin resolver.

En esos casos se mantiene `pendiente` y se explica por qué en `notas`.

## 9. Contacto y escalado

- Responsable de la verificación: **Natalia Blázquez Herrero**.
- Contacto directo del proyecto: pendiente de definir antes de publicar.
- Incidencias de accesibilidad del sitio web: se registran en la página
  `accesibilidad.html`, que también está pendiente de un canal de contacto.

## 10. Entrega

La entrega se considera completa cuando:

- los tres CSV están rellenos y sin filas `verificado` incompletas;
- las fichas impresas están firmadas y fechadas;
- las contradicciones están señaladas;
- el proyecto ha corregido el contenido y ha regenerado el sitio;
- el plan de verificación se ha vuelto a imprimir y revisar.
