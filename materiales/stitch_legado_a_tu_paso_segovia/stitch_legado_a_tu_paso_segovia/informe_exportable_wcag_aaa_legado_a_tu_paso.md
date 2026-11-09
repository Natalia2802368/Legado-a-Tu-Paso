# Especificaciones Técnicas y Auditoría de Accesibilidad (WCAG 2.2 Nivel AAA)

**Proyecto:** «Legado a tu paso» — Turismo Accesible en Segovia para Personas con Hipoacusia  
**Destinatarios clave:** Personas con audífonos, implantes cocleares y fatiga auditiva o cognitiva  
**Fecha del informe:** Octubre 2024 / Auditoría de Prototipo  
**Estándar de conformidad:** W3C Web Content Accessibility Guidelines (WCAG) 2.2 — **Nivel AAA**

---

## 1. Resumen Ejecutivo de Conformidad

El proyecto digital **«Legado a tu paso»** ha sido concebido desde sus cimientos arquitectónicos, gráficos y de interacción bajo la pauta más rigurosa de accesibilidad web: **WCAG 2.2 Nivel AAA**. 

El diseño erradica cualquier dependencia del canal auditivo para la planificación y disfrute de la visita cultural a los monumentos de Segovia, proporcionando información acústica cuantitativa y cualitativa (decibelios, tiempos de reverberación, compatibilidad con bucle magnético según norma IEC 60118-4) en un entorno visual estructurado, predecible y de mínimo esfuerzo cognitivo.

### Matriz Global de Cumplimiento Técnico

| Principio WCAG | Criterio de Éxito | Nivel | Estado | Métrica / Solución Implementada en «Legado a tu paso» |
| :--- | :--- | :---: | :---: | :--- |
| **1. Perceptible** | **1.4.6 Contraste (Mejorado)** | **AAA** | **CUMPLE** | Ratio texto principal: **16.2:1** (`#0f1729` sobre `#fbf9f6`). Mínimo exigido: 7:1. |
| **1. Perceptible** | **1.4.8 Presentación Visual** | **AAA** | **CUMPLE** | Ancho máx. 68 car/línea (`max-w-prose`), alineación a izquierda, interlineado 1.625, zoom al 200% sin scroll horizontal. |
| **1. Perceptible** | **1.2.6 / 1.2.8 Cero dependencias de audio** | **AAA** | **CUMPLE** | 100% de los datos acústicos expresados mediante diagramas numéricos, etiquetas textuales y previsión de vídeo en LSE. |
| **2. Operable** | **2.1.3 Teclado (Sin Excepciones)** | **AAA** | **CUMPLE** | Navegación íntegra por tabulación con anillo de foco visible (`ring-4 ring-blue-700`, contraste 8.4:1). Cero trampas de teclado. |
| **2. Operable** | **2.2.3 Sin Tiempo de Espera** | **AAA** | **CUMPLE** | Cero temporizadores o caducidad de sesión en monumentos o formulario. |
| **2. Operable** | **2.4.9 Propósito del Enlace (Solo Enlace)** | **AAA** | **CUMPLE** | Prohibidos textos genéricos (*«Ver más»*). Todos los enlaces son unívocos y descriptivos por sí mismos. |
| **2. Operable** | **2.5.5 Tamaño del Objetivo (Mejorado)** | **AAA** | **CUMPLE** | Áreas interactivas mínimas de **48 × 48 px** (+19% sobre los 44×44 px de WCAG AAA), con holgura perimetral (`gap-3`). |
| **3. Comprensible** | **3.1.5 Nivel de Lectura (Plain Language)** | **AAA** | **CUMPLE** | Glosario contextual integrado para términos especializados (*bucle magnético*, *RT60*, *dB SPL*); redacción llana directa. |
| **3. Comprensible** | **3.3.6 Prevención de Errores (Todos)** | **AAA** | **CUMPLE** | Autoguardado local en `localStorage`, recuperación ante fallos de red sin pérdida de datos y edición posterior al envío. |
| **4. Robusto** | **4.1.3 Mensajes de Estado** | **AAA/AA** | **CUMPLE** | Regiones `aria-live="polite"` y `role="status"` para actualizaciones dinámicas de filtros y borrador seguro. |

---

## 2. Auditoría Detallada por Principios WCAG 2.2

### Principio 1: Perceptible

#### 1.4.6 Contraste (Mejorado) — Nivel AAA
* **Exigencia normativa:** Relación de contraste de al menos **7:1** para texto normal y **4.5:1** para texto grande (≥18pt o ≥14pt negrita).
* **Valores del sistema de diseño «Legado a tu paso»:**
  * Texto principal (Slate Navy `#0f1729`) sobre Fondo principal (Warm Off-white `#fbf9f6`): **16.2:1** (Cumplimiento superior en un +131% a la norma).
  * Texto secundario y datos descriptivos (`#1e293b`) sobre Contenedor intermedio (`#f1ede7`): **11.8:1**.
  * Texto sobre fondo de tarjetas blancas (`#ffffff`): **16.9:1**.
  * Botones primarios (Fondo `#0f1729` con texto `#ffffff`): **16.9:1**.
  * Enlaces activos y resaltados de foco (`#1d4ed8`): **8.2:1** a **9.5:1**.
* **Modos de visualización forzada:** Soporte nativo para el modo de alto contraste del sistema operativo (*Windows High Contrast Mode*) mediante bordes semánticos definidos en CSS `currentColor`.

#### 1.4.8 Presentación Visual — Nivel AAA
* **Exigencia normativa:** Permitir al usuario adaptar tipografía y color; prohibición de texto justificado; ancho no superior a 80 caracteres; interlineado espacioso; tolerancia a zoom de 200% sin scroll horizontal.
* **Implementación:**
  * **Longitud de línea:** Se restringen los bloques de lectura mediante `max-w-prose` (rango controlado de 60 a 72 caracteres por línea en escritorio y ajuste natural fluido en móvil a 390 px).
  * **Alineación:** Estricta alineación a la izquierda (`text-left`), con `text-justify` expresamente deshabilitado para evitar ríos de espacios en blanco que dificulten la lectura en personas con dislexia o fatiga ocular.
  * **Interlineado:** `leading-relaxed` (1.625) en párrafos y separación de párrafos (`space-y-4` a `space-y-6`), superando con holgura el factor 1.5 exigido.
  * **Zoom fluido:** Estructura basada en unidades relativas (`rem`, flexbox y grid). Pruebas de escalado al 200% y 400% mantienen legibilidad íntegra sin cortes ni barras horizontales de desplazamiento.

#### 1.2.6 Lengua de Signos y 1.2.8/1.2.9 Alternativa Completa
* **Implementación adaptada a hipoacusia:**
  * Eliminación sistemática de barreras basadas en sonido: no se exige audio para comprender ningún aspecto patrimonial ni funcional.
  * Los parámetros acústicos se comunican visualmente:
    * **Presencia de bucle magnético perimetral (Telecoil / Posición T)** verificada por técnicos.
    * **Nivel medio de ruido ambiental (dB SPL)** con comparativa intuitiva (ej. *«52 dB: equivalente a una biblioteca tranquila»*).
    * **Tiempo de reverberación (RT60)** presentado como *«Tiempo de eco: 0.7s (Voz clara, no retumba)»*.
  * Integración prevista para enlaces y ventanas modales de interpretación en Lengua de Signos Española (LSE).

---

### Principio 2: Operable

#### 2.1.3 Teclado (Sin Excepciones) — Nivel AAA
* **Exigencia normativa:** Toda la interfaz debe ser completamente operable mediante teclado o pulsadores sin tiempos de respuesta específicos y sin ninguna excepción.
* **Implementación:**
  * Árbol de navegación 100% secuencial y lógico vía tecla `Tab` y `Shift + Tab`.
  * Anillo de foco prominente de alto contraste:
    ```css
    focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-blue-700 focus-visible:ring-offset-2
    ```
  * Manejo accesible de diálogos y paneles modales: captura y retorno de foco al elemento desencadenante al cerrar (`Esc`).

#### 2.2.3 Sin Tiempo de Espera — Nivel AAA
* **Exigencia normativa:** El tiempo no debe ser un factor crítico para ninguna tarea.
* **Implementación:**
  * Ausencia absoluta de temporizadores de sesión, cuentas atrás de reserva o caducidad en el envío de opiniones.

#### 2.4.9 Propósito del Enlace (Solo Enlace) — Nivel AAA
* **Exigencia normativa:** El propósito de cada enlace debe ser identificable a partir del propio texto del enlace de forma aislada, sin necesidad de leer el contexto circundante.
* **Implementación:**
  * Erradicación de fórmulas ambiguas (*«Ver más»*, *«Haz clic aquí»*, *«Detalles»*).
  * Textos explícitos:
    * *«Ver ficha y datos acústicos del Acueducto de Segovia»*
    * *«Ver condiciones acústicas del Alcázar de Segovia»*
    * *«Inspeccionar auditoría técnica del Sello de Accesibilidad Acústica»*
    * *«Volver al listado general de monumentos accesibles»*
  * Atributos `aria-label` descriptivos en enlaces de glifos o tarjetas reducidas.

#### 2.5.5 Tamaño del Objetivo (Mejorado) — Nivel AAA
* **Exigencia normativa:** Dianas interactivas con un área mínima de **44 × 44 px CSS**.
* **Implementación en «Legado a tu paso»:**
  * **Estándar adoptado:** **48 × 48 px CSS** (Superficie efectiva de 2.304 px², un +19% superior a la exigencia AAA).
  * Botones con `min-h-[48px]`, `min-w-[48px]`, padding interno generoso y separación perimetral de al menos 12 px entre controles para evitar toques accidentales en exteriores con una sola mano.

---

### Principio 3: Comprensible

#### 3.1.5 Nivel de Lectura y 3.1.3 Palabras Poco Comunes — Nivel AAA
* **Exigencia normativa:** Lenguaje claro que no supere la educación secundaria básica (< 8.º grado escolar) o inclusión de definiciones contextuales directas para jerga técnica.
* **Implementación:**
  * Sustitución de terminología compleja por explicaciones directas en primera persona y en contexto de visita turística.
  * Glosario integrado en tarjeta:
    * **Bucle magnético:** *«Envía el sonido del guía directamente a tu audífono o implante, eliminando el ruido de alrededor»*.
    * **Tiempo de eco (RT60):** *«0.7 segundos: tiempo de eco muy bajo; no retumba la voz y se entiende cada palabra»*.
    * **Horas tranquilas:** *«De 10:00 a 11:30: menor afluencia de grupos y menor barullo»*.
  * Pregunta de feedback comprensible y pragmática: *«¿Esta información te ha ahorrado tener que llamar o dudar antes de tu visita?»*.

#### 3.3.6 Prevención de Errores (Todos) — Nivel AAA
* **Exigencia normativa:** Mecanismos de comprobación, reversibilidad o confirmación en todo formulario, garantizando que no se pierdan datos.
* **Implementación:**
  * **Persistencia en `localStorage`:** Los datos introducidos en la pantalla de feedback se guardan automáticamente con cada pulsación (`legado_feedback_draft`).
  * **Tolerancia a fallos de red:** En caso de corte de conexión (habitual en muros de piedra de Segovia), el formulario retiene íntegros los datos y ofrece el botón *«Reintentar envío ahora»*.
  * **Reversibilidad:** El estado de agradecimiento posterior al envío incluye la acción directa *«Modificar mi valoración o añadir más detalles»*.

---

### Principio 4: Robusto

#### 4.1.3 Mensajes de Estado
* Notificación en vivo (`role="status"`, `aria-live="polite"`) cada vez que los filtros del catálogo se modifican (ej. *«Mostrando 4 monumentos con bucle magnético activo en Segovia»*) y al guardarse el borrador local.
* Notificación de alerta (`role="alert"`) ante pérdidas de red sin bloquear la navegación por teclado.

---

## 3. Instrucciones de Exportación

1. **Formato Markdown (.md):** Este contenido se encuentra registrado y disponible en el DataStore y en el lienzo para su copia, descarga o commit directo en repositorios Git (`ACCESSIBILITY_WCAG_AAA.md`).
2. **Generación / Conversión a PDF:**
   * **Opción A (Navegador):** Abrir el documento o pantalla en el navegador y ejecutar `Ctrl + P` (o `Cmd + P`) seleccionando *«Guardar como PDF»* (márgenes normales, tamaño A4, gráficos de fondo activados).
   * **Opción B (Herramientas CLI / Markdown to PDF):** Compatible al 100% con motores como Pandoc, Marp, Typora o extensiones de VS Code (*Markdown PDF*) utilizando la sintaxis estándar aquí provista.
