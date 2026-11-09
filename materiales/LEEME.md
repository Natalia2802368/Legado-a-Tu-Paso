# Materiales de referencia

Carpeta interna: **no se publica** en `sitio/`. Última revisión: 8 de noviembre
de 2026.

Regla de entrada: un material no es una fuente hasta que se comprueba. Solo pasa
a la web lo que tiene fuente, fecha y estado; las inferencias se quedan fuera o
se marcan como tales. Esta carpeta conserva el rastro de lo consultado para que
cualquier dato publicado se pueda auditar.

## 1. Inventario y decisión

| Material | Qué contiene | Decisión | Dónde se nota |
| --- | --- | --- | --- |
| `files/ia_turismo_accesible_espana.csv` y `.pdf` | 17 fichas sobre IA y turismo accesible en España: proyectos, contratación pública, un evento, un prototipo, una política, publicaciones, datos sin verificar e hipótesis. | **Contexto, no contenido.** No se publica ninguna afirmación de este informe. La conclusión que sí se adopta es metodológica: casi todo está «declarado por la entidad» y no se localizaron evaluaciones independientes, así que no se usan asistentes de IA para inventar o completar datos de accesibilidad. | README, decisión «Datos e IA». |
| `files-2/segovia_verificacion_afirmaciones.csv` | 14 afirmaciones sobre Segovia con resultado, evidencia, URL, nota y fecha de consulta (4/11/2026). | **Sí, como evidencia.** Se usaron las partes confirmadas y se conservaron las contradicciones. No se usó la fecha del Plan Integral (no consta) ni se publicó como hecho la inferencia sobre el Gemelo Digital. | `contenido/segovia.md`, sección 13 y notas. |
| `files-2/segovia_fichas_accesibilidad_catedral_acueducto.csv` | 46 filas con medidas y estados de las fichas oficiales de Turismo de Segovia para la catedral y el acueducto. Ninguna ficha indica fecha de inspección. | **Sí, con estado `pendiente`.** Se condensaron en 23 filas publicadas; las 46 quedan en el CSV de campo para medir en sitio. No se ha promovido ninguna a `verificado`. | `contenido/segovia.md`, sección 13, y `verificacion/segovia-monumentos.csv`. |
| `files-2/segovia_verificacion_fuentes.pdf` | Recopilación de fuentes y capturas del trabajo de verificación. | **Archivo de evidencia.** No se republica: solo se enlazan las fuentes originales. | No aparece en la web. |
| `stitch_legado_a_tu_paso_segovia/` | Prototipos visuales, pantallas y dos informes que se autodeclaran WCAG 2.2 AAA, centrados en Segovia y en hipoacusia. | **No adoptado en bloque.** Se aprovecharon criterios de interacción ya implementados y comprobados; se rechazó el resto. | Ver apartado 3. |
| `documentos_Plan_Integral_de_Accesibilidad_de_Segovia_a13d906c.pdf` y su copia comprimida | Presentación municipal de 90 páginas del Plan Integral de Accesibilidad. | **Contexto.** Se confirma que el plan existe, quién lo financió y qué ámbitos cubre. No se usan barreras, actuaciones ni importes concretos porque están en imágenes y planos no legibles; el documento no lleva fecha. | `contenido/segovia.md`, párrafo «Marco municipal». |
| `Acuerdo JGL 170.2026.pdf` | Acuerdo de la Junta de Gobierno Local de 2/7/2026 que aprueba el protocolo de datos cartográficos y del Gemelo Digital (exp. 314/2026/PG1000). | **Contexto legal.** No cambia el contenido público porque el sitio no reutiliza datos GIS municipales. Se usa para describir el Gemelo Digital y sus límites. | `verificacion/guia-de-campo.md`, apartado 2. |
| `Protocolo General Para la Disposición de Datos Cartograficos Municipales y del Gemelo Digital de Segovia.pdf` | Texto del protocolo: datos abiertos, datos restringidos, condiciones de reutilización y exclusión de responsabilidad. | **Contexto legal.** Mismas condiciones y cautelas que el acuerdo. | `verificacion/guia-de-campo.md`, apartado 2. |

## 2. Qué se ha integrado exactamente

- **Segovia, marco municipal:** párrafo en el apartado 2 de
  `contenido/segovia.md`. Dice que el Ayuntamiento publica un resumen del Plan
  Integral, sin fecha, y que no se localizaron el plan completo ni los planos.
  El Gemelo Digital sirve para perfiles de elevación y medición de edificios,
  pero su protocolo no garantiza ausencia de errores ni actualización
  permanente.
- **Segovia, fichas de monumento:** 23 filas publicadas en el apartado 13, con
  fuente, fecha de consulta y estado `pendiente`. Las notas conservan la
  contradicción de la rampa de la catedral, las obras de la Puerta del Perdón,
  la falta de fecha de inspección y la decisión de no publicar datos acústicos
  sin medir.
- **Guía de campo:** aviso para usar el Gemelo Digital solo como preparación y
  para citar «Origen de los datos: Ayuntamiento de Segovia» y la fecha de
  actualización si se reutilizan sus datos.
- **Generador:** el apartado 2 de una ciudad admite ahora una nota de texto
  libre después de la tabla de accesibilidad (`accesibilidad_nota`). Solo
  Segovia la usa por ahora.
- **README:** decisión «Datos e IA» y referencia a esta carpeta.

## 3. Qué se ha rechazado y por qué

Del paquete de Stitch no se copió código ni se adoptó su sistema de diseño:

- **Paleta y tipografía:** proponía azul marino, ámbar y crema, y Source Serif 4.
  El proyecto ya decidió papel `#FAF9F7`, tinta `#30160D`, teja `#5E2E1B`,
  Literata 600 y Atkinson Hyperlegible. Cambiarlas rompería la marca y los
  contrastes ya comprobados.
- **Conformidad AAA autodeclarada:** los informes afirman cumplimiento WCAG 2.2
  AAA sin evidencia de auditoría externa. La web declara un objetivo AA y un
  estado «parcialmente conforme», que es lo que se puede sostener.
- **Datos acústicos:** decibelios, RT60, «bucle magnético verificado por
  técnicos» y horas valle no tienen medición ni fuente en el material. No se
  publican. La ficha de Segovia lo dice expresamente.
- **Formulario de feedback y vídeo en LSE:** no hay backend, canal de contacto
  ni vídeos grabados. Publicar la interfaz sin el servicio sería una promesa
  vacía.
- **Alcance:** el material reduce el proyecto a Segovia y a hipoacusia. El
  catálogo real cubre 15 ciudades y distintas necesidades de accesibilidad.
- **Capturas y HTML:** sirven como referencia visual, no como base de código.
  No se han copiado al sitio.

Del informe de IA no se ha usado ningún dato público: las fichas mezclan
declaraciones comerciales, proyectos sin evaluación y datos marcados como «sin
verificar». Se conserva como contexto para justificar la regla de verificación
humana.

Del Plan Integral no se han usado cifras, barreras ni presupuestos: el texto
extraíble es un índice y los planos están en imágenes. Tampoco se le asigna una
fecha que el documento no indica.

## 4. Cómo incorporar material nuevo

1. Identifica autoría, entidad, fecha, URL canónica y tipo de documento
   (fuente primaria, secundaria, marketing o inferencia).
2. Comprueba la afirmación y anota el resultado exacto: confirmado, confirmado
   parcialmente, no verificable o inferencia.
3. Si es un dato de accesibilidad, se queda en `pendiente` hasta la inspección
   en sitio. Una web, un folleto o un PDF no convierten un dato en verificado.
4. Si se adopta, actualiza el contenido y el generador; si no, déjalo anotado
   aquí con el motivo.
5. No copies parámetros de seguimiento (`utm_*`), imágenes sin licencia ni PDFs
   de terceros. Enlaza la fuente original y conserva la fecha de consulta.

## 5. Atribuciones que hay que respetar

- **Datos GIS del Ayuntamiento de Segovia (si se reutilizan):** «Origen de los
  datos: Ayuntamiento de Segovia», logotipo municipal y fecha de la última
  actualización. No se puede insinuar que el Ayuntamiento avala el proyecto.
  Los datos abiertos se pueden usar sin solicitud; los restringidos requieren
  solicitud, informe técnico y resolución de Alcaldía.
- **OpenStreetMap:** © OpenStreetMap contributors, ODbL.
- **Open-Meteo:** atribución visible en el bloque de clima.
- **Fotos:** autor, licencia y enlace a Wikimedia Commons en la página de
  créditos.
- **Tipografías:** Literata y Atkinson Hyperlegible, SIL Open Font License.

## 6. Estado

Revisión cerrada el 8/11/2026. No queda material sin decidir. Los PDFs y CSV se
conservan como evidencia interna; la web solo publica datos con fuente, fecha y
estado, y mantiene `pendiente` todo lo que no se ha comprobado en sitio.
