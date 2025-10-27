#!/usr/bin/env python3
"""
Genera icone PNG da SVG per CAP 9000
Richiede: pip install cairosvg pillow
"""

import os
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
    import io
except ImportError:
    print("Installing required packages...")
    os.system("pip install cairosvg pillow")
    import cairosvg
    from PIL import Image
    import io

# Dimensioni richieste
SIZES = [16, 32, 48, 64, 128, 256, 512, 1024]

# Directory
ICONS_DIR = Path("build-resources/icons")
ICONS_DIR.mkdir(parents=True, exist_ok=True)

SVG_FILE = Path("frontend/public/icon.svg")

def generate_png(size):
    """Genera PNG da SVG"""
    output_file = ICONS_DIR / f"icon-{size}x{size}.png"
    
    print(f"Generating {size}x{size}...")
    
    # Converti SVG in PNG
    png_data = cairosvg.svg2png(
        url=str(SVG_FILE),
        output_width=size,
        output_height=size
    )
    
    # Salva
    with open(output_file, 'wb') as f:
        f.write(png_data)
    
    print(f"  ✓ Saved: {output_file}")

def generate_ico():
    """Genera ICO per Windows (multi-size)"""
    print("\nGenerating Windows ICO...")
    
    # Carica tutte le dimensioni
    images = []
    for size in [16, 32, 48, 64, 128, 256]:
        png_file = ICONS_DIR / f"icon-{size}x{size}.png"
        if png_file.exists():
            img = Image.open(png_file)
            images.append(img)
    
    if images:
        ico_file = ICONS_DIR / "icon.ico"
        images[0].save(
            ico_file,
            format='ICO',
            sizes=[(img.width, img.height) for img in images]
        )
        print(f"  ✓ Saved: {ico_file}")

def generate_icns():
    """Genera ICNS per macOS"""
    print("\nGenerating macOS ICNS...")
    
    iconset_dir = ICONS_DIR / "icon.iconset"
    iconset_dir.mkdir(exist_ok=True)
    
    # Mappa dimensioni per iconset
    iconset_map = {
        16: ["icon_16x16.png"],
        32: ["icon_16x16@2x.png", "icon_32x32.png"],
        64: ["icon_32x32@2x.png"],
        128: ["icon_128x128.png"],
        256: ["icon_128x128@2x.png", "icon_256x256.png"],
        512: ["icon_256x256@2x.png", "icon_512x512.png"],
        1024: ["icon_512x512@2x.png"]
    }
    
    for size, names in iconset_map.items():
        src = ICONS_DIR / f"icon-{size}x{size}.png"
        if src.exists():
            for name in names:
                dst = iconset_dir / name
                Image.open(src).save(dst)
                print(f"  ✓ Created: {name}")
    
    # Converti in icns (solo su macOS)
    if os.system("which iconutil > /dev/null 2>&1") == 0:
        icns_file = ICONS_DIR / "icon.icns"
        os.system(f"iconutil -c icns {iconset_dir} -o {icns_file}")
        print(f"  ✓ Saved: {icns_file}")
    else:
        print("  ⚠ iconutil not found (macOS only), skipping ICNS generation")

def main():
    print("=" * 50)
    print("CAP 9000 Icon Generator")
    print("=" * 50)
    print()
    
    if not SVG_FILE.exists():
        print(f"✗ Error: {SVG_FILE} not found")
        return
    
    # Genera PNG
    for size in SIZES:
        generate_png(size)
    
    # Genera ICO
    generate_ico()
    
    # Genera ICNS
    generate_icns()
    
    print()
    print("=" * 50)
    print("✓ Icon generation completed!")
    print("=" * 50)
    print()
    print(f"Icons saved in: {ICONS_DIR.absolute()}")
    print()
    print("Files generated:")
    for f in sorted(ICONS_DIR.glob("*")):
        if f.is_file():
            size_mb = f.stat().st_size / 1024
            print(f"  • {f.name} ({size_mb:.1f} KB)")

if __name__ == "__main__":
    main()
