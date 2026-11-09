# Modelo de ficha de ciudad

Usa este modelo para cada ciudad. Sustituye los campos y elimina las notas que no
apliquen. No publiques una ficha con datos sin fuente ni con estado `pendiente`.

## Frontmatter

```yaml
---
id: nombre-ciudad
nombre: Nombre oficial
provincia: Provincia
comunidad: Comunidad autónoma
unesco_desde: 1985
lat: 40.000000
lon: -4.000000
timezone: Europe/Madrid
estado: borrador | revisado | publicado
fuente_principal: URL oficial
verificado_en: AAAA-MM-DD
---
```

## 1. Ficha

- **Titular:** `# Ciudad — una frase que la resuma`.
- **Por qué es patrimonio:** 60–90 palabras.
- **Tiempo recomendado:** ruta base y visita completa.
- **Mejor momento:** mañana/tarde, sombra, calor, aglomeración.
- **Accesibilidad en una frase:** qué puede esperar una persona con movilidad
  reducida, baja visión, discapacidad auditiva o cognitiva.
- **Aviso:** información orientativa, fuentes oficiales, fecha y pendiente de
  verificación en sitio.

## 2. Accesibilidad

| Campo | Valor | Fuente | Estado |
| --- | --- | --- | --- |
| Superficie predominante | Adoquín, losas, asfalto, tierra | | verificado / pendiente / desactualizado / descartado |
| Pendiente | Llana, moderada, fuerte | | |
| Escalones | Sí/No, número y alternativa | | |
| Aseos adaptados | Ubicación | | |
| Plazas PMR | Número y ubicación | | |
| Bucle magnético | Sí/No | | |
| Braille | Sí/No | | |
| Lengua de signos | Sí/No | | |
| Lectura fácil | Sí/No | | |
| Audioguía | Sí/No e idiomas | | |
| Perro de asistencia | Permitido | | |
| Descanso | Bancos y sombra | | |

## 3. Ruta

**Ruta base:** X,X km aproximados (estimación sobre mapa), duración, N paradas.  
**Superficie:**  
**Desnivel:**  
**Alternativa:** tramos no aptos y recorrido sustitutivo.

| # | Parada | Coordenadas | Tiempo | Acceso | Audio | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | lat, lon | | | Sí | pendiente |

## 4. Paradas

Repetir un bloque por parada.

### 1. Nombre de la parada

- **Qué es:** 40–60 palabras.
- **Por qué importa:** 30–50 palabras.
- **Acceso:** entrada, rampa, elevador, escalones.
- **Aseo adaptado:**
- **Alternativa:** maqueta, braille, vídeo, texto.
- **Estado:** `pendiente`; verificar en sitio.

## 5. Guiones de audio

> Formato: 40–60 segundos con ritmo pausado (unas 65–100 palabras). Voz
> humana, frases cortas. La transcripción se publica siempre junto al audio.

**1. Nombre de la parada**

> “Guion en segunda persona, presente, frases cortas. Di qué se ve, por qué
> importa y qué debe saber una persona con discapacidad antes de entrar.”

## 6. Clima

**Fuente:** Open-Meteo, consulta del AAAA-MM-DD a las HH:MM.  
**Producción:** AEMET OpenData y avisos oficiales.

- **Ahora:** temperatura; sensación; estado del cielo; viento; humedad.
- **Hoy:** mínima y máxima.
- **Mañana:** mínima y máxima.
- **Pasado:** mínima y máxima.

> Nota estacional: calor, hielo, lluvia o viento, y su efecto en el firme.

## 7. Emergencias

| Categoría | Nombre | Teléfono | Dirección | Fuente | Estado |
| --- | --- | --- | --- | --- | --- |
| General | Emergencias | 112 | — | UE | verificado |
| Policía Nacional | Policía Nacional | 091 | — | Ministerio del Interior | verificado |
| Guardia Civil | Guardia Civil | 062 | — | Guardia Civil | verificado |
| Emergencias sanitarias | | | — | | verificado |
| Bomberos | | 080 | — | | verificado |
| Policía Local | | 092 | — | Ayuntamiento | pendiente |
| Hospital | | — | | | pendiente |
| Farmacias | Colegio Oficial de Farmacéuticos | — | — | | pendiente |

**Nota:** solo se publican teléfonos locales confirmados. El 112 y los números
nacionales funcionan siempre.

## 8. Aparcamiento accesible

Datos de OpenStreetMap (Overpass, AAAA-MM-DD). **No verificados.**

| Nombre | Coordenadas | Plazas | PMR | Coste | Tipo | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | pendiente |

**Nota:** si no hay datos suficientes, no se inventan plazas: se muestra un aviso
y el enlace al mapa oficial.

## 9. Transporte accesible

| Modo | Operador | Accesibilidad | Contacto | Enlace | Tiempo real |
| --- | --- | --- | --- | --- | --- |
| Autobús urbano | | Confirmar flota con rampa | | | No |
| Tren | Renfe | Andenes adaptados; asistencia Atendo | 912 320 320 | renfe.com | Sí, en app |
| Taxi | | Confirmar vehículo adaptado | | — | No |

## 10. Fotos

| Uso | Archivo | Autor | Licencia |
| --- | --- | --- | --- |
| | | | |

Crédito visible: **“Fotografía: [autor], [licencia], Wikimedia Commons”**, con
enlace a la ficha del archivo. Ver `creditos-fotos.md`.

## 11. Fuentes

- Ayuntamiento:
- Turismo oficial:
- Organismo de patrimonio:
- Renfe:
- Open-Meteo:
- OpenStreetMap / Overpass:
- Wikimedia Commons:

## 12. Checklist

- [ ] Textos revisados y sin afirmaciones sin fuente.
- [ ] Coordenadas comprobadas.
- [ ] Accesibilidad verificada en sitio.
- [ ] Teléfonos y horarios confirmados.
- [ ] Aparcamientos con titularidad y dimensiones.
- [ ] Transporte con contacto oficial.
- [ ] Fotos revisadas y con crédito.
- [ ] Audio grabado y transcrito.
- [ ] Fecha de verificación visible.
