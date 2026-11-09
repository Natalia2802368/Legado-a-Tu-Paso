# App para iOS y Android

Legado a Tu Paso se distribuye de dos formas con el mismo contenido:

1. **PWA instalable** desde el navegador, disponible ya y sin tiendas.
2. **App nativa con Capacitor** para App Store y Google Play, cuando existan las
   cuentas de desarrollador y el equipo de compilación.

No hay dos bases de código: el sitio de `sitio/` es la app. Capacitor lo empaqueta
en un WebView nativo y añade los iconos, la pantalla de inicio y los metadatos de
cada tienda.

## Estado actual

| Pieza | Estado |
| --- | --- |
| PWA instalable | Lista: manifiesto, iconos, service worker y modo sin conexión |
| Cáscara sin conexión | Lista: 13 páginas, CSS, JS, fuentes, logos y Leaflet (35 archivos) |
| Descarga por ciudad | Lista: fotos y audios bajo demanda, con progreso y borrado |
| Audio sin conexión | Listo: caché persistente con soporte de peticiones `Range` |
| Configuración de Capacitor | Lista: `package.json`, `capacitor.config.json`, iconos y splash |
| Proyecto Android | Pendiente: hace falta Node 22+, JDK 21 y Android Studio |
| Proyecto iOS | Pendiente: hace falta un Mac con Xcode 26+ |
| Cuentas de tienda | Pendientes: Google Play y Apple Developer |
| Firma y publicación | Pendiente: claves, fichas de tienda y revisión |

En este equipo **no se pueden compilar los binarios**: no hay Node, el Java
instalado es 8, no hay Android SDK y Windows no puede compilar iOS. Los archivos
de configuración quedan preparados para hacerlo en un equipo con el entorno
completo o en un servicio de integración continua.

## Qué funciona ya en la PWA

- **Instalar:** en Chrome, Edge, Samsung Internet y navegadores compatibles
  aparece el botón «Instalar la app» en el pie. En iPhone y iPad se muestra la
  instrucción de Compartir → Añadir a pantalla de inicio.
- **Sin conexión:** al abrir la app una vez se guarda la cáscara. Las páginas,
  el índice, la verificación, los créditos y los estilos siguen disponibles.
- **Descargar una ciudad:** cada guía tiene el bloque «Esta guía sin conexión».
  Guarda sus fotos y sus audios, muestra el progreso y permite borrarlos. El
  tamaño se indica antes de descargar (unos 12–15 MB por ciudad con los WAV
  actuales).
- **Audio:** se reproduce y se puede buscar dentro del archivo aunque no haya
  conexión, porque el service worker responde a las peticiones `Range` desde la
  caché.
- **Mapa y tiempo:** necesitan conexión. La app lo explica y mantiene el texto,
  la lista de paradas y el audio utilizables sin red.
- **Almacenamiento:** el navegador puede pedir permiso para conservar los datos.
  La app solicita almacenamiento persistente al iniciar una descarga. Si el
  sistema borra la caché por falta de espacio, la guía se puede volver a
  descargar.

La PWA no necesita cuentas de tienda ni Mac. Es la vía inmediata para probar en
un móvil real y para enseñar el proyecto antes del 2 de diciembre.

## Requisitos para compilar la app nativa

| Herramienta | Versión mínima | Para qué |
| --- | --- | --- |
| Node.js | 22 | CLI de Capacitor y dependencias |
| npm | Incluido con Node | Instalar paquetes |
| JDK | 21 | Compilar Android |
| Android Studio | Otter 2025.2.1 o posterior | SDK, emulador y firma Android |
| Xcode | 26 o posterior | Compilar y firmar iOS (solo macOS) |
| CocoaPods | Versión compatible con Xcode 26 | Dependencias iOS |
| Cuenta Google Play | Alta única | Publicar en Android |
| Apple Developer Program | Suscripción anual | Publicar en iOS |

Capacitor 8 trabaja con Android SDK 36 y iOS 15 o posterior. Antes de comprar
cuentas, confirma los requisitos vigentes en la documentación oficial de
Capacitor y de cada tienda.

## Compilar Android

En un equipo Windows, macOS o Linux con Node 22+, JDK 21 y Android Studio:

```powershell
cd C:\Users\Admin\Documents\Legado-a-Tu-Paso

# 1. Generar el sitio actualizado
python herramientas\crear_iconos.py
python herramientas\generar_sitio.py

# 2. Instalar dependencias de Capacitor
npm install

# 3. Crear el proyecto Android (solo la primera vez)
npm run cap:add:android

# 4. Generar iconos y pantallas de inicio de la marca
npm run assets

# 5. Copiar el sitio y actualizar dependencias nativas
npm run cap:sync

# 6. Abrir Android Studio
npm run cap:open:android
```

En Android Studio:

1. Espera a que Gradle sincronice.
2. Prueba en un emulador y en un móvil real.
3. Genera un **Android App Bundle** firmado (`Build > Generate Signed Bundle`).
4. Sube el `.aab` a Google Play Console.

Para volver a compilar después de cambiar contenido o estilos, basta con:

```powershell
python herramientas\generar_sitio.py
npm run cap:sync
```

## Compilar iOS

Necesitas un Mac con Xcode 26 o posterior. En el Mac:

```bash
cd /ruta/a/Legado-a-Tu-Paso
python3 herramientas/crear_iconos.py
python3 herramientas/generar_sitio.py
npm install
npm run cap:add:ios      # solo la primera vez
npm run assets
npm run cap:sync
npm run cap:open:ios
```

En Xcode:

1. Selecciona el equipo de firma.
2. Comprueba el identificador `es.legadoatupaso.app`.
3. Prueba en un iPhone real; el simulador no valida bien el audio, la vibración
   ni el comportamiento del notch.
4. Archiva (`Product > Archive`) y sube a App Store Connect.

Si no hay un Mac, se puede usar un servicio de integración continua con macOS
para generar el archivo de Xcode, pero la firma y la subida siguen necesitando
una cuenta de Apple.

## Identidad de la app

- **Nombre:** Legado a Tu Paso.
- **Identificador:** `es.legadoatupaso.app`.
- **Esquema web:** `https` en Android.
- **Iconos y splash:** `assets/icon-only.png`, `icon-foreground.png`,
  `icon-background.png`, `splash.png` y `splash-dark.png`, generados por
  `herramientas/crear_iconos.py`.
- **Color de fondo:** papel `#FAF9F7`; tinta `#30160D`; teja `#5E2E1B`.

El identificador se puede cambiar antes de la primera publicación, pero no
después: la tienda lo usa para reconocer la app. Si el proyecto consigue un
dominio definitivo, valora usar un identificador basado en ese dominio antes de
subir la primera versión.

## Tamaño y audio

Capacitor copia **todo** `sitio/` dentro de la app. Hoy son unos 104 MB, de los
cuales 89 MB son los 64 WAV provisionales. Esto es aceptable para una prueba
interna, pero conviene reducirlo antes de publicar:

- convertir los WAV a Opus o MP3 mono de 64 kbps (la voz se entiende bien y el
  peso baja aproximadamente 10 veces);
- regenerar el sitio y comprobar que los reproductores usan el nuevo formato;
- volver a ejecutar `npm run cap:sync` y medir el tamaño del binario.

La descarga por ciudad de la PWA no cambia el tamaño del binario nativo: en la
app nativa todos los audios ya van incluidos. El bloque «Descargar esta ciudad»
se oculta automáticamente dentro de Capacitor.

## Actualizaciones

- **PWA:** el service worker descarga una versión nueva cuando cambia el
  contenido. La app avisa de que hay conexión o no, pero no fuerza una recarga.
- **App nativa:** no se usa actualización en caliente. Cada cambio de contenido
  requiere regenerar, `npm run cap:sync`, compilar y subir una versión nueva a la
  tienda. Para cambios pequeños, la revisión suele ser rápida; para cambios de
  contenido grande, planifica la fecha.

## Publicación en las tiendas

Antes de enviar la primera versión:

- [ ] Cuenta de Google Play creada y verificada.
- [ ] Apple Developer Program activo y equipo de firma configurado.
- [ ] Política de privacidad publicada en una URL estable. La app no usa cookies
      ni rastreo, pero sí consulta Open-Meteo y OpenStreetMap; hay que explicarlo.
- [ ] Aviso legal y canal de contacto publicados en la web.
- [ ] Ficha de tienda: nombre, descripción breve y larga, categoría, palabras
      clave, capturas de móvil y tableta, icono de 1024 × 1024 y gráfico de
      cabecera.
- [ ] Clasificación de contenido y formulario de seguridad de datos.
- [ ] Declaración de accesibilidad: la app tiene textos alternativos, audio,
      navegación por teclado y estados de foco; las fotos y los datos de
      accesibilidad siguen el mismo régimen de verificación que la web.
- [ ] Prueba en un dispositivo real con VoiceOver y TalkBack.
- [ ] Datos de accesibilidad: **ninguno se presenta como verificado** hasta que
      Natalia Blázquez Herrero firme la comprobación en sitio.
- [ ] Versión y número de compilación incrementados.
- [ ] Claves de firma guardadas en un lugar seguro y con copia de seguridad.

Google Play y App Store revisan el contenido y la privacidad. Una app de turismo
puede publicarse sin backend, pero necesita una URL de política de privacidad y
un medio de contacto.

## Qué no se puede hacer en este equipo

- Compilar Android: faltan Node 22+, JDK 21 y Android SDK.
- Compilar iOS: hace falta macOS con Xcode 26+.
- Firmar y subir a las tiendas: faltan las cuentas y las claves.
- Probar audio en un iPhone real: no hay dispositivo conectado.

Mientras tanto, la PWA se puede instalar y probar en cualquier móvil con un
navegador actualizado. Es el entregable inmediato y la base que se empaquetará
después.

## Comprobaciones rápidas de la PWA

1. Abrir la web con HTTPS (o `http://127.0.0.1` en local) y esperar a que cargue.
2. En el pie debe aparecer «Instalar la app» o la instrucción de iPhone.
3. Abrir una guía y pulsar «Descargar esta ciudad». Debe mostrar progreso y
   terminar con «Guía guardada en este dispositivo».
4. Activar el modo avión, cerrar la app y volver a abrirla desde el icono. La
   guía descargada, sus fotos y sus audios deben seguir funcionando.
5. Comprobar que el mapa y el tiempo muestran un aviso comprensible sin
   conexión, sin romper el resto de la página.
6. Borrar la descarga y comprobar que las fotos y audios vuelven a pedir red.
