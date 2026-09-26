# Pixelverso Studio — Sitio Web

**Tu mundo, en cuadros · Concepción, Chile**

---

## ¿Qué es este proyecto?

Sitio web de e-commerce para **Pixelverso Studio**, tienda de cuadros personalizados impresos en bastidor de madera MDF artesanal. Los clientes eligen categoría, tamaño y orientación, y confirman su pedido directo por WhatsApp.

---

## Tecnologías

- **Un solo archivo HTML** (`index.html`) con CSS y JS embebidos — sin frameworks, sin build
- Google Fonts: Bebas Neue + Rajdhani
- Lottie CDN (fallback automático a videos MP4 si no existen los JSON)
- LocalStorage para persistencia del carrito
- WhatsApp API (`wa.me`) para envío de pedidos

---

## Estructura de carpetas

```
project/
├── index.html          → todo el sitio (HTML + CSS + JS embebido)
├── data/
│   └── productos.json  → catálogo de productos (editable)
├── images/
│   ├── logo.png
│   ├── banner-cta.png
│   ├── bg-hero-texture.png
│   └── cat-*.png       → imágenes de las 18 categorías
├── videos/
│   └── 0X_pixelito-*.mp4  → animaciones de Pixelito
├── animations/         → Lottie JSON (opcional, fallback a videos)
└── uploads/            → carpeta para fotos personalizadas (uso futuro)
```

---

## Producto

- **Material:** Bastidor MDF artesanal con impresión UV
- **Tamaños:** 40×30 cm · 80×60 cm
- **Multipanel:** tríptico 3 × 25×70 cm · cuádruple 4 × 25×70 cm (una sola medida, sin elegir tamaño)
- **Orientación:** Vertical u horizontal
- **Fijación:** Cola fría de madera (sin clavos ni taladros)
- **Envío:** Retiro local · Delivery en Concepción · Blue Express / Starken a todo Chile

---

## Las 22 categorías

Anime · Videojuegos · Dragon Ball Z · Marvel · DC · Música · Autos · Pokémon · Mafia · Enamorados · Cuadros familiares · Stranger Things · The Last of Us · John Wick · Nintendo · Cristiana · Collage · Espacio personalizado · Deportes · Películas · **Arte abstracto** · **Infantil**

---

## Funcionalidades principales

- Hero slider (2 slides, autoplay 5 s)
- 18 secciones de categorías con scroll horizontal y flechas prev/next
- Vista previa 3D interactiva con tilt por mouse/touch
- Carrito sidebar con persistencia en localStorage
- Envío de pedido formateado directo a WhatsApp (+56 9 3273 4706)
- Formulario de personalización con drag & drop de imagen
- Panel de Tweaks: Vibe / Energy / Density (persiste en localStorage)
- Scroll reveal con IntersectionObserver
- Responsive (mobile / tablet / desktop)

---

## Cómo agregar productos al catálogo

### Estructura de imágenes
Cada producto tiene **3 archivos** guardados en su carpeta de categoría:

```
images/
├── anime/
│   ├── anime-01-mockup-40x30.jpg  ← mockup tamaño pequeño (modal al elegir 40x30)
│   ├── anime-01-mockup-80x60.jpg  ← mockup tamaño grande (card + modal por defecto)
│   ├── anime-01-art.jpg           ← obra sola sin bastidor (aparece al hover)
│   ├── anime-02-mockup-40x30.jpg
│   ├── anime-02-mockup-80x60.jpg
│   └── anime-02-art.jpg
├── dragonball/
├── marvel/
└── ...  (18 categorías)
```

### Comportamiento visual por archivo

| Archivo | Dónde se usa |
|---|---|
| `mockup-80x60.jpg` | Card del catálogo (siempre visible) · Modal cuando se elige 80×60 |
| `mockup-40x30.jpg` | Modal cuando se elige 40×30 cm |
| `art.jpg` | Al pasar el mouse sobre la card (crossfade) |

### Agregar un producto nuevo

1. Pon los 3 archivos en `images/<categoria>/`
2. Descomenta el bloque en `data/productos.json` y completa `nombre` y `orientacion`
3. Guarda — el sitio carga el JSON en runtime

```json
{
  "id": "anime-01",
  "nombre": "Eren Titán",
  "mockup40":    "images/anime/anime-01-mockup-40x30.jpg",
  "mockup80":    "images/anime/anime-01-mockup-80x60.jpg",
  "art":         "images/anime/anime-01-art.jpg",
  "categoria":   "Anime",
  "orientacion": "vertical"
}
```

---

### Cuadros multipanel (trípticos / cuádruples)

Usan **una sola imagen** (el mockup en la pared) guardada como `images/<cat>/<cat>-NN-mockup-80x60.jpg`, así cumplen la regla "producto válido = tiene mockup-80x60" y la renumeración normal. En `productos.json` llevan:

```json
{ "id": "anime-08", "nombre": "Naruto, Sakura y Sasuke — Equipo 7",
  "mockup40": "images/anime/anime-08-mockup-80x60.jpg", "mockup80": "…mismo…", "art": "…mismo…",
  "categoria": "Anime", "orientacion": "horizontal",
  "formato": "triptico", "medida": "3 × 25×70 cm", "origen": "NARUTO 2.png" }
```

La web muestra la etiqueta **▥ Tríptico** en la card y, en la vista previa, un solo botón con la medida (el carrito y WhatsApp usan esa medida).

- `importar_multipanel.py` — importa desde `Downloads\CUADROS TRIPLES` (lista de archivos → categoría/nombre adentro del script; salta los ya importados por `origen`).
- `renumerar.py <cats…>` / `--todas` — deja las carpetas sin huecos y actualiza **a la vez** archivos, `productos.json` e `index.html` (el hero usa rutas fijas como `anime-04`). Verifica al final que todas las rutas existan.

## Deploy a producción

```powershell
cd C:\Users\elbol\PROYECTOS\pixelverso
git add index.html data/productos.json
git commit -m "..."
git push origin main
firebase login:use gerssoneduardol@gmail.com   # ⚠️ NO respetadoresdocentes: esa cuenta no tiene acceso
firebase use pixelverso-studio-cl
firebase deploy --only hosting
```

### ⚠️ Ojo: hay DOS proyectos Firebase de Pixelverso

Ambos responden y sirven el mismo sitio, lo que hace muy fácil desplegar al equivocado y creer que "no se aplicó el cambio":

| Proyecto Firebase | URL | Último deploy detectado |
|---|---|---|
| `pixelverso-studio-cl` | https://pixelverso-studio-cl.web.app | 24 jun 2026, 20:17 ← **más reciente** |
| `pixelverso-studio` | https://pixelverso-studio.web.app | 24 jun 2026, 15:16 |

**El `.firebaserc` de esta carpeta apunta a `pixelverso-studio-cl`**, y es el que tiene el deploy más nuevo — así que ese es el bueno. Ten presente que `CLAUDE.md` decía `pixelverso-studio` (sin `-cl`), que es el proyecto antiguo.

Si un deploy "no se ve reflejado", lo primero a revisar es a cuál de los dos se subió.

---

## Contacto / Redes

- **WhatsApp:** +56 9 3273 4706
- **Instagram:** @pixelverso.studio
- **Ubicación:** Concepción, Chile

---

## Historial de cambios

### v1.5 — 2026-09-26 · Trípticos y categorías nuevas
- 24 cuadros multipanel (23 trípticos 3 × 25×70 cm + 1 cuádruple 4 × 25×70 cm) repartidos en sus categorías
- Categorías nuevas: **Arte abstracto** (10) e **Infantil** (2), con portada, menú del footer y `CAT_SLUG_MAP`
- Campo `formato`/`medida` en `productos.json`; card con etiqueta ▥ Tríptico y vista previa con medida fija
- Renumeración sin huecos de anime, pokemon y videojuegos (referencias del hero actualizadas)
- Textos de la web mencionan los trípticos

### v1.0 — 2026-05-10 · Construcción inicial
- Sitio construido desde cero como single-file HTML
- 18 categorías con scroll horizontal
- Carrito funcional con WhatsApp
- Hero slider 2 slides
- Visualizador 3D con 4 ambientes

### v1.1 — 2026-05-10 · Tweaks panel + mockups
- Panel de Tweaks: Vibe (Cyber Neon / Sunset Otaku / Mono Coleccionista), Energy (Zen / Studio / Arcade), Density (Cinema / Studio / Mercado)
- Mockups por categoría auto-generados con CSS scenes (sin imágenes externas)
- Hover crossfade: mockup → obra sola
- Vista previa 3D corregida (bug listeners en DOM)
- Tamaño cambia escala visual del cuadro en el modal
- Foto personalizada abre el mismo modal con orientación auto-detectada

### v1.4 — 2026-05-10 · Mockup por tamaño en vista previa
- Esquema de 3 archivos: `mockup-40x30`, `mockup-80x60` y `art`
- Card del catálogo → siempre muestra `mockup-80x60` (más impacto visual)
- Modal vista previa → al elegir 40×30 cambia a `mockup-40x30`, al elegir 80×60 cambia a `mockup-80x60`
- Hover de card → crossfade a `art.jpg` (obra sola)
- `productos.json` actualizado con campos `mockup40`, `mockup80`, `art`

### v1.3 — 2026-05-10 · Sistema de catálogo con carpetas por categoría
- 18 carpetas creadas en `images/<categoria>/`
- `productos.json`: nuevo esquema con `imagenMockup` (obra en bastidor) e `imagenArt` (obra sola)
- JS: función `_renderCategoriasFromJSON()` — cuando subes productos al JSON, aparecen automáticamente en sus categorías en el sitio
- Hover de card: muestra `imagenArt`; card y modal usan `imagenMockup`
- Repo subido a GitHub: [github.com/Gerssitochaskia/pixelverso](https://github.com/Gerssitochaskia/pixelverso)

### v1.2 — 2026-05-10 · Ajustes de contenido y UI
- **Trust bar:** textos actualizados a bastidor artesanal, ultra HD, cola fría de madera, retiro/delivery/envío
- **Eliminadas** las 5 estrellas y "480 reseñas verificadas" (sin reseñas reales aún)
- **Eliminado** video Pixelito flotante del hero (descontextualizado)
- **Eliminada** sección hexagonal "Mezcla universos" (no aplica al producto actual)
- **Logo** con border-radius circular en navbar
- **Contenedor** más ancho (1480px) con menos padding lateral para aprovechar los bordes
- **Envíos:** 3 opciones — Retiro en local (gratis) / Delivery Concepción / Blue Express + Starken todo Chile
- **3 pasos** de personalización: sin referencias a lienzo/metalizado, actualizado a madera MDF
- **Video** en sección "Clientes reales" cambiado de Pixelito triste → Pixelito héroe
- **Footer:** iconos SVG reales de Instagram, Facebook y WhatsApp (eliminado Twitter)
- **Wood frame** más delgado (padding 2.5%) para simular vinilo sobre MDF sin marco grueso
- **3D tilt** más amplio: 45°/35° (antes 22°/18°)
- **Cuadro 80×60** no se sale del frame en el visualizador
- **Carrito:** opciones de entrega actualizadas (Retiro local / Delivery / Blue Express + Starken)
