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
- **Orientación:** Vertical u horizontal
- **Fijación:** Cola fría de madera (sin clavos ni taladros)
- **Envío:** Retiro local · Delivery en Concepción · Blue Express / Starken a todo Chile

---

## Las 18 categorías

Anime · Videojuegos · Dragon Ball Z · Marvel · DC · Música · Autos · Pokémon · Mafia · Enamorados · Cuadros familiares · Stranger Things · The Last of Us · John Wick · Nintendo · Cristiana · Collage · Espacio personalizado

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
Cada producto tiene **dos fotos** guardadas en su carpeta de categoría:

```
images/
├── anime/
│   ├── anime-01-mockup.jpg   ← obra en bastidor (se ve en la card)
│   ├── anime-01-art.jpg      ← obra sola (se ve al hover)
│   ├── anime-02-mockup.jpg
│   └── anime-02-art.jpg
├── dragonball/
├── marvel/
└── ...  (18 categorías)
```

### Agregar un producto nuevo

1. Pon las dos fotos en `images/<categoria>/` con la convención de nombre
2. Descomenta (o copia) el bloque correspondiente en `data/productos.json`
3. Completa `nombre` y `orientacion` (`vertical` o `horizontal`)
4. Guarda — el sitio carga el JSON en runtime, sin recompilar nada

```json
{
  "id": "anime-01",
  "nombre": "Eren Titán",
  "imagenMockup": "images/anime/anime-01-mockup.jpg",
  "imagenArt":    "images/anime/anime-01-art.jpg",
  "categoria":    "Anime",
  "orientacion":  "vertical"
}
```

> **Convención de nombres:** `<categoria>-<número>-mockup.jpg` y `<categoria>-<número>-art.jpg`
> Ejemplo: `dragonball-03-mockup.jpg` + `dragonball-03-art.jpg`

---

## Contacto / Redes

- **WhatsApp:** +56 9 3273 4706
- **Instagram:** @pixelverso.studio
- **Ubicación:** Concepción, Chile

---

## Historial de cambios

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
