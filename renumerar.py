"""
Renumera categorías sin huecos (01, 02, 03…) y actualiza TODO lo que apunta a los archivos:
nombres en images/<cat>/, ids y rutas en data/productos.json y referencias en index.html.

    python renumerar.py anime deportes familia          (categorías = nombre de carpeta)
    python renumerar.py --todas
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
TIPOS = ("mockup-40x30", "mockup-80x60", "art")


def renumerar(cat: str, data: dict, html: str) -> str:
    carpeta = RAIZ / "images" / cat
    numeros = sorted({int(m.group(1)) for p in carpeta.glob(f"{cat}-*.jpg")
                      if (m := re.match(rf"{cat}-(\d+)-", p.name))})
    sin_80 = [n for n in numeros if not (carpeta / f"{cat}-{n:02d}-mockup-80x60.jpg").exists()]
    if sin_80:
        print(f"  ⚠ {cat}: sin mockup-80x60 (no válidos, se dejan fuera de la numeración): {sin_80}")
    validos = [n for n in numeros if n not in sin_80]
    mapa = {viejo: nuevo for nuevo, viejo in enumerate(validos, 1) if viejo != nuevo}
    if not mapa:
        print(f"  {cat}: ya está sin huecos ({len(validos)} productos)")
        return html

    # 1) archivos, en dos pasos para no pisar nombres
    for viejo in mapa:
        for t in TIPOS:
            f = carpeta / f"{cat}-{viejo:02d}-{t}.jpg"
            if f.exists():
                f.rename(carpeta / f"__tmp-{viejo:02d}-{t}.jpg")
    for viejo, nuevo in mapa.items():
        for t in TIPOS:
            f = carpeta / f"__tmp-{viejo:02d}-{t}.jpg"
            if f.exists():
                f.rename(carpeta / f"{cat}-{nuevo:02d}-{t}.jpg")

    # 2) productos.json e index.html (reemplazo por marcador para evitar cadenas 02→03→04)
    def cambiar(texto: str) -> str:
        for viejo in mapa:
            texto = texto.replace(f"{cat}-{viejo:02d}-", f"@@{cat}@{viejo:02d}-").replace(f'"{cat}-{viejo:02d}"', f'"@@{cat}@{viejo:02d}"')
        for viejo, nuevo in mapa.items():
            texto = texto.replace(f"@@{cat}@{viejo:02d}", f"{cat}-{nuevo:02d}")
        return texto

    for p in data["productos"]:
        for k in ("id", "mockup40", "mockup80", "art"):
            if isinstance(p.get(k), str):
                p[k] = cambiar(f'"{p[k]}"' if k == "id" else p[k]).strip('"')
    print(f"  {cat}: " + ", ".join(f"{v:02d}→{n:02d}" for v, n in mapa.items()))
    return cambiar(html)


def main():
    cats = sys.argv[1:]
    if cats == ["--todas"]:
        cats = [d.name for d in (RAIZ / "images").iterdir() if d.is_dir() and d.name != "mockups"]
    rjson, rhtml = RAIZ / "data" / "productos.json", RAIZ / "index.html"
    data = json.loads(rjson.read_text(encoding="utf-8-sig"))
    html = rhtml.read_text(encoding="utf-8")
    for cat in cats:
        html = renumerar(cat, data, html)
    rjson.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    rhtml.write_text(html, encoding="utf-8")
    # verificación: cada ruta del JSON debe existir
    faltan = [p[k] for p in data["productos"] for k in ("mockup40", "mockup80", "art")
              if p.get(k) and not (RAIZ / p[k]).exists()]
    print("✔ todas las rutas del JSON existen" if not faltan else f"⚠ rutas que no existen: {faltan[:10]}")


if __name__ == "__main__":
    main()
