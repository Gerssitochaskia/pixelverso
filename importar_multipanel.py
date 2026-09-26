"""
Agrega cuadros multipanel (trípticos 3 × 25×70 cm y cuádruples 4 × 25×70 cm) al catálogo.

- Cada producto usa UNA imagen (el mockup en la pared) guardada como
  images/<cat>/<cat>-NN-mockup-80x60.jpg, así sigue las reglas del catálogo
  (producto válido = tiene mockup-80x60) y la renumeración existente.
- En productos.json lleva "formato" y "medida"; la web muestra esa medida
  en vez de 40×30 / 80×60.

    python importar_multipanel.py            (se puede correr de nuevo: salta los ya importados)
"""

import json
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent
ORIGEN = Path(r"C:\Users\elbol\Downloads\CUADROS TRIPLES")
JSON = RAIZ / "data" / "productos.json"

TRIPTICO = ("triptico", "3 × 25×70 cm")
CUADRUPLE = ("cuadruple", "4 × 25×70 cm")

# archivo, carpeta, categoría (como en productos.json), nombre, tags, formato
ITEMS = [
    ("ChatGPT Image 30 ago 2026, 00_35_02.png", "familia", "Cuadros familiares",
     "Familia — Papá, Hija, Hijo y Mamá (4 piezas)", "familia papa mama hijo hija blanco y negro retrato cuadruple", CUADRUPLE),
    ("COLOCOLO.png", "deportes", "Deportes",
     "Colo-Colo — Tríptico Escudo", "colo colo colocolo escudo futbol chile triptico", TRIPTICO),
    ("Create_abstract_art_frames_20260925234941.jpg", "abstracto", "Arte abstracto",
     "Árbol de la Vida Arcoíris", "arbol de la vida arcoiris acuarela colores decoracion triptico", TRIPTICO),
    ("Create_art_from_three_frames_20260925235355.jpg", "abstracto", "Arte abstracto",
     "París de Noche — Torre Eiffel", "paris torre eiffel ciudad noche luces decoracion triptico", TRIPTICO),
    ("Create_art_without_text_20260926145403.jpg", "abstracto", "Arte abstracto",
     "Plantas Boho", "plantas boho minimalista hojas terracota decoracion triptico", TRIPTICO),
    ("Create_three_frames_from_image_20260926145349.jpg", "infantil", "Infantil",
     "Idol K-Pop — Escenario", "kpop k-pop idol cantante niña infantil animacion triptico", TRIPTICO),
    ("Creating_abstract_art_frames_20260925234745.jpg", "abstracto", "Arte abstracto",
     "Abstracto Fluido Multicolor", "abstracto fluido multicolor tinta alcohol decoracion triptico", TRIPTICO),
    ("Creating_abstract_art_frames_20260925234802.jpg", "abstracto", "Arte abstracto",
     "Abstracto Ondas Violeta y Oro", "abstracto ondas violeta morado dorado lujo decoracion triptico", TRIPTICO),
    ("Creating_bird_art_frames_20260925235406.jpg", "abstracto", "Arte abstracto",
     "Pájaros al Atardecer", "pajaros aves siluetas atardecer naturaleza decoracion triptico", TRIPTICO),
    ("Creating_three_frames_from_image_20260926145357.jpg", "infantil", "Infantil",
     "Trío K-Pop — Idols", "kpop k-pop idols trio niñas infantil animacion triptico", TRIPTICO),
    ("FAMILIA.jpeg", "familia", "Cuadros familiares",
     "Familia — Hijo, Papá y Mamá", "familia papa mama hijo blanco y negro retrato triptico", TRIPTICO),
    ("FAMILIA2.png", "familia", "Cuadros familiares",
     "Familia — Hijo, Papá y Mamá II", "familia papa mama hijo blanco y negro retrato triptico", TRIPTICO),
    ("familia3.png", "familia", "Cuadros familiares",
     "Familia — Mamá, Hija y Papá", "familia papa mama hija blanco y negro retrato triptico", TRIPTICO),
    ("Family_of_lions_in_frames_20260925234814.jpg", "abstracto", "Arte abstracto",
     "Familia de Leones — Sabana", "leones leon familia sabana animales atardecer decoracion triptico", TRIPTICO),
    ("GTA 1.png", "videojuegos", "Videojuegos",
     "GTA VI — Jason y Lucia", "gta 6 vi grand theft auto jason lucia videojuego triptico", TRIPTICO),
    ("GTA2.jpeg", "videojuegos", "Videojuegos",
     "GTA VI — Acción", "gta 6 vi grand theft auto accion videojuego triptico", TRIPTICO),
    ("Modify_frames_into_art_20260926145410.jpg", "abstracto", "Arte abstracto",
     "Aves — Petirrojo, Chochín y Martín Pescador", "aves pajaros petirrojo martin pescador naturaleza decoracion triptico", TRIPTICO),
    ("Modify_three_frames_into_art_20260925235402.jpg", "abstracto", "Arte abstracto",
     "Árbol Dorado — Lujo", "arbol dorado oro lujo ciervo paisaje decoracion triptico", TRIPTICO),
    ("NARUTO 2.png", "anime", "Anime",
     "Naruto, Sakura y Sasuke — Equipo 7", "naruto sakura sasuke equipo 7 anime triptico", TRIPTICO),
    ("NARUTO3.png", "anime", "Anime",
     "Naruto, Sasuke y Kakashi", "naruto sasuke kakashi uzumaki uchiha hatake anime triptico", TRIPTICO),
    ("POKEMON 2.jpeg", "pokemon", "Pokemon",
     "Iniciales de Kanto — Bulbasaur, Charmander y Squirtle", "pokemon bulbasaur charmander squirtle iniciales kanto triptico", TRIPTICO),
    ("POKEMON3.jpeg", "pokemon", "Pokemon",
     "Gengar Ramen", "pokemon gengar ramen japones rosado triptico", TRIPTICO),
    ("RONALDO.jpeg", "deportes", "Deportes",
     "Cristiano Ronaldo — Tríptico Estadio", "cristiano ronaldo cr7 estadio futbol triptico", TRIPTICO),
    ("Updating_panels_with_street_art_20260926145339.jpg", "abstracto", "Arte abstracto",
     "Arte Urbano — Street Art", "arte urbano street art graffiti corona retrato decoracion triptico", TRIPTICO),
]


def siguiente_numero(carpeta: Path, cat: str) -> int:
    usados = [int(p.name.split("-")[1]) for p in carpeta.glob(f"{cat}-*-mockup-80x60.jpg")
              if p.name.split("-")[1].isdigit()]
    return max(usados, default=0) + 1


def main():
    with open(JSON, encoding="utf-8-sig") as f:
        data = json.load(f)
    productos = data["productos"]
    ya = {p.get("origen") for p in productos if p.get("origen")}

    for archivo, cat, categoria, nombre, tags, (formato, medida) in ITEMS:
        if archivo in ya:
            print(f"· ya importado: {nombre}")
            continue
        carpeta = RAIZ / "images" / cat
        carpeta.mkdir(parents=True, exist_ok=True)
        n = siguiente_numero(carpeta, cat)
        pid = f"{cat}-{n:02d}"
        ruta = f"images/{cat}/{pid}-mockup-80x60.jpg"
        with Image.open(ORIGEN / archivo) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((1600, 1600))
            im.save(RAIZ / ruta, "JPEG", quality=86, optimize=True)
        productos.append({
            "id": pid, "nombre": nombre, "tags": tags,
            "mockup40": ruta, "mockup80": ruta, "art": ruta,
            "categoria": categoria, "orientacion": "horizontal",
            "formato": formato, "medida": medida, "origen": archivo,
        })
        print(f"✔ {pid}: {nombre} ({medida})")

    with open(JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Imagen de portada para las categorías nuevas (regla del catálogo)
    for cat in ("abstracto", "infantil"):
        portada = RAIZ / "images" / f"cat-{cat}.png"
        primera = sorted((RAIZ / "images" / cat).glob("*-mockup-80x60.jpg"))
        if not portada.exists() and primera:
            with Image.open(primera[0]) as im:
                im.thumbnail((900, 900))
                im.save(portada, "PNG", optimize=True)
            print(f"✔ portada {portada.name}")


if __name__ == "__main__":
    main()
