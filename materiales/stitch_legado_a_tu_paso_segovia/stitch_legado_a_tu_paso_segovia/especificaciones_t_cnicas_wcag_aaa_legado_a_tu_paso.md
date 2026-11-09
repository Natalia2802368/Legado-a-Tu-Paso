# Especificaciones Técnicas de Accesibilidad (WCAG 2.2 Nivel AAA)
## Proyecto: «Legado a tu paso» — Turismo Accesible en Segovia para Personas con Hipoacusia

Este documento recoge la auditoría técnica, criterios de éxito e implementación de diseño y código para garantizar la conformidad con las pautas **WCAG 2.2 nivel AAA**, con foco prioritario en usuarios con audífonos, implantes cocleares y fatiga cognitiva/visual.

---

### 1. Principio: Perceptible

#### 1.4.6 Contraste (Mejorado) — Nivel AAA
* **Requisito WCAG**: La presentación visual de texto e imágenes de texto tiene una relación de contraste de al menos **7:1**, excepto textos grandes (al menos 18pt o 14pt negrita) que deben tener al menos **4.5:1**.
* **Implementación en «Legado a tu paso»**:
  - Color de texto principal (`#0f1729`) sobre fondo de superficie (`#fbf9f6`): **Contraste 16.2:1** (Supera ampliamente el 7:1 exigido).
  - Texto secundario y etiquetas (`#1e293b` sobre `#f1ede7` / `#ffffff`): **Contraste 9.4:1 a 14.1:1**.
  - Acentos interactivos primarios (`#1d4ed8` / `#0f1729` sobre contenedor claro): mínimo **8.2:1**.
  - Todos los estados interactivos (foco, selección, hover) mantienen la ratio > 7:1.

#### 1.4.8 Presentación Visual — Nivel AAA
* **Requisito WCAG**:
  1. El usuario puede seleccionar colores de fondo y primer plano.
  2. El ancho del texto no supera los **80 caracteres** o glifos por línea.
  3. El texto no está justificado (alineación a la izquierda).
  4. Interlineado de al menos 1.5 en párrafos, y espaciado entre párrafos de al menos 1.5 veces el interlineado.
  5. El texto se puede ampliar al 200% sin barras de desplazamiento horizontal.
* **Implementación**:
  - Regla tipográfica: `max-w-prose` (máximo 65–72 caracteres por línea).
  - Alineación estricta a la izquierda (`text-left`), prohibición de `text-justify`.
  - Leading adaptado: `leading-relaxed` (1.625) y espaciado de bloques con márgenes rítmicos (`space-y-4`).
  - Layouts responsivos y fluidos en Tailwind con rems; soporte de zoom al 200% y 400% sin scroll horizontal ni solapamiento.

#### 1.2.6 Lengua de Signos (Grabada) y 1.2.8 / 1.2.9 Alternativa Completa — Nivel AAA
* **Implementación para Hipoacusia**:
  - Ausencia deliberada de requisitos de audio: ninguna interacción depende de alertas sonoras o llamadas telefónicas.
  - Alternativa visual integral para cualquier dato acústico: la información de reverberación y ruido ambiental se traduce a decibelios numéricos, bandas de frecuencia y gráficos SVG etiquetados, además de insignias textuales explícitas (*«Bucle magnético activo»*, *«Horas valle recomendadas»*).
  - Compatibilidad prevista para glosas y vídeo en LSE (Lengua de Signos Española) embebido con reproductor accesible.

---

### 2. Principio: Operable

#### 2.1.3 Teclado (Sin Excepciones) — Nivel AAA
* **Requisito WCAG**: Toda la funcionalidad del contenido se puede operar a través de una interfaz de teclado sin requerir tiempos específicos para las pulsaciones.
* **Implementación**:
  - Navegación completa por tabulación (`tabindex="0"` lógico en botones, enlaces, tarjetas clicables y switches).
  - Indicador de foco visible de alto contraste: `focus-visible:ring-4 focus-visible:ring-blue-600 focus-visible:ring-offset-2`.
  - Atajos y orden de foco secuencial idéntico al orden visual.
  - Sin trampas de teclado (*no keyboard traps*) en diálogos ni modales.

#### 2.2.3 Sin Tiempo de Espera — Nivel AAA
* **Requisito WCAG**: El tiempo no es parte esencial de ningún evento ni actividad.
* **Implementación**:
  - Ninguna sesión caduca durante la consulta de monumentos o el envío de feedback.
  - El borrador de feedback se guarda de manera automática y persistente en `localStorage`. El usuario no pierde sus datos por pausas o pérdida de conectividad.

#### 2.2.4 Interrupciones aplazables — Nivel AAA
* **Implementación**:
  - Cero pop-ups o notificaciones espontáneas invasivas. Las alertas de estado sólo se emiten en respuesta a una acción explícita del usuario.

#### 2.4.9 Propósito del Enlace (Solo Enlace) — Nivel AAA
* **Requisito WCAG**: Existe un mecanismo disponible para permitir que el propósito de cada enlace se identifique a partir del propio texto del enlace.
* **Implementación**:
  - Eliminación de textos genéricos tipo *"Ver más"* o *"Haga clic aquí"*.
  - Enlaces unívocos y descriptivos: *"Ver datos acústicos del Alcázar de Segovia"*, *"Inspeccionar certificado del sello de accesibilidad"*, *"Volver al listado general de monumentos"*.
  - Atributos `aria-label` descriptivos en todos los botones de iconos complementarios.

#### 2.5.5 Tamaño del Objetivo (Mejorado) — Nivel AAA
* **Requisito WCAG**: El tamaño del objetivo táctil o clicable tiene un área mínima de **44 × 44 píxeles CSS** (WCAG 2.2 criterio 2.5.8 solicita 24x24 px, pero AAA requiere 44x44 px o equivalente con holgura suficiente).
* **Implementación**:
  - Todos los botones, toggles de filtro y enlaces principales cuentan con `min-h-[48px]` y `min-w-[48px]` con área de toque despejada sin solapamiento de dianas.

---

### 3. Principio: Comprensible

#### 3.1.3 Palabras Poco Comunes y 3.1.5 Nivel de Lectura — Nivel AAA
* **Requisito WCAG**: El texto claro no requiere un nivel de lectura superior a la educación secundaria inferior, o se proporcionan aclaraciones para jerga especializada.
* **Implementación**:
  - Glosario contextual accesible para términos técnicos auditivos: explicaciones directas para conceptos como *"Bucle de inducción magnética (posición T)"*, *"Tiempo de reverberación (RT60)"* y *"dB SPL"*.
  - Redacción en lenguaje claro (*Plain Language* / Lectura Facilitada) validada en las pantallas de feedback (*«¿Esto te ha ahorrado llamar o dudar?»*).

#### 3.2.5 Cambios a Petición — Nivel AAA
* **Requisito WCAG**: Los cambios de contexto se inician únicamente mediante solicitud del usuario o existe un mecanismo para desactivarlos.
* **Implementación**:
  - La selección de filtros o la alternancia de pestañas no recarga la página ni desplaza inesperadamente el scroll.
  - La navegación se gestiona con avisos de región en vivo (`aria-live="polite"`).

#### 3.3.5 Ayuda Contextual y 3.3.6 Prevención de Errores (Todos) — Nivel AAA
* **Requisito WCAG**: Proporcionar ayuda contextual para la introducción de datos y validaciones reversibles.
* **Implementación**:
  - Pantalla de feedback con guardado preventivo local: ante fallos de conexión, se muestra de inmediato el estado con el botón *"Reintentar envío ahora"* y confirmación de *"Borrador seguro guardado localmente"*.
  - Opciones de confirmación y revisión previas al envío definitivo.

---

### 4. Principio: Robusto

#### 4.1.3 Mensajes de Estado (WCAG 2.1 / 2.2)
* **Implementación**:
  - Regiones `role="status"` y `aria-live="polite"` para notificar cambios en el filtrado de monumentos (ej.: *"4 monumentos encontrados con bucle magnético"*).
  - Alerta en vivo accesible (`role="alert"`) para situaciones de error de red sin bloquear el foco del teclado.

---

### Resumen de Cumplimiento Técnico

| Criterio WCAG 2.2 AAA | Estado en «Legado a tu paso» | Detalle técnico |
| :--- | :---: | :--- |
| **1.4.6 Contraste mejorado (7:1)** | **CUMPLE (16.2:1)** | Slate navy `#0f1729` sobre warm off-white `#fbf9f6` |
| **1.4.8 Presentación visual** | **CUMPLE** | Máx. 70 car/línea, `text-left`, zoom 200% sin scroll horizontal |
| **2.1.3 Teclado sin excepciones** | **CUMPLE** | Navegación 100% interactiva por teclado con `focus-visible` destacado |
| **2.2.3 Sin tiempo límite** | **CUMPLE** | Sin temporizadores ni expiración de sesión |
| **2.4.9 Propósito del enlace** | **CUMPLE** | Textos y `aria-label` autosuficientes y unívocos |
| **2.5.5 Área de toque (44×44px)** | **CUMPLE** | Dianas táctiles de mínimo 48×48px con padding seguro |
| **3.1.5 Lectura comprensible** | **CUMPLE** | Lenguaje claro y definición visual de prótesis/términos acústicos |
| **3.3.6 Prevención de errores** | **CUMPLE** | Autoguardado local + persistencia de borrador offline |
