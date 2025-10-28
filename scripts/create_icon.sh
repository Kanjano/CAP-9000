#!/bin/bash
# Crea icona PNG da SVG per macOS

# Verifica se qlmanage è disponibile (macOS)
if command -v qlmanage &> /dev/null; then
    # Usa qlmanage per convertire SVG in PNG
    qlmanage -t -s 512 -o build-resources/icons/ frontend/public/icon.svg
    
    # Rinomina il file generato
    mv build-resources/icons/icon.svg.png build-resources/icons/icon.png 2>/dev/null || true
    
    echo "✓ Icona PNG creata: build-resources/icons/icon.png"
elif command -v convert &> /dev/null; then
    # Usa ImageMagick se disponibile
    convert -background none -size 512x512 frontend/public/icon.svg build-resources/icons/icon.png
    echo "✓ Icona PNG creata con ImageMagick"
else
    echo "⚠ Nessun tool di conversione disponibile"
    echo "Installa ImageMagick: brew install imagemagick"
fi
