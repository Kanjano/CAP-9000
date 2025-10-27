#!/bin/bash
# Script per creare installer CAP 9000 per macOS e Windows

set -e

echo "========================================"
echo "CAP 9000 - Installer Creator"
echo "========================================"
echo ""

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
DESKTOP_DIR="$HOME/Desktop"

# Crea directory dist
mkdir -p "$DIST_DIR"

echo -e "${YELLOW}[1/5]${NC} Building frontend..."
cd "$PROJECT_DIR/frontend"
npm run build
cd "$PROJECT_DIR"
echo -e "${GREEN}✓${NC} Frontend built"
echo ""

echo -e "${YELLOW}[2/5]${NC} Creating macOS installer package..."

# Crea struttura app macOS
APP_NAME="CAP 9000"
APP_DIR="$DIST_DIR/$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Copia file applicazione
cp -r frontend/dist "$RESOURCES_DIR/"
cp -r *.py "$RESOURCES_DIR/" 2>/dev/null || true
cp requirements.txt "$RESOURCES_DIR/" 2>/dev/null || true
cp -r local_docs "$RESOURCES_DIR/" 2>/dev/null || true
cp download_docs.py "$RESOURCES_DIR/" 2>/dev/null || true
cp build-resources/icons/icon.svg "$RESOURCES_DIR/icon.svg"

# Crea script di avvio
cat > "$MACOS_DIR/CAP9000" << 'EOF'
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$DIR/../Resources"

# Avvia Flask backend
cd "$RESOURCES_DIR"
python3 app.py &
FLASK_PID=$!

# Attendi che Flask sia pronto
sleep 3

# Apri frontend nel browser
open "http://localhost:5001"

# Attendi che l'utente chiuda
wait $FLASK_PID
EOF

chmod +x "$MACOS_DIR/CAP9000"

# Crea Info.plist
cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>CAP9000</string>
    <key>CFBundleIdentifier</key>
    <string>com.antoniocangiano.cap9000</string>
    <key>CFBundleName</key>
    <string>CAP 9000</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleIconFile</key>
    <string>icon</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo -e "${GREEN}✓${NC} macOS app created: $APP_DIR"
echo ""

echo -e "${YELLOW}[3/5]${NC} Creating macOS DMG..."
DMG_NAME="CAP-9000-macOS-v1.0.0.dmg"
hdiutil create -volname "CAP 9000" -srcfolder "$APP_DIR" -ov -format UDZO "$DIST_DIR/$DMG_NAME"
echo -e "${GREEN}✓${NC} DMG created: $DMG_NAME"
echo ""

echo -e "${YELLOW}[4/5]${NC} Creating Windows installer package..."
WIN_DIR="$DIST_DIR/CAP-9000-Windows"
mkdir -p "$WIN_DIR"

# Copia file
cp -r frontend/dist "$WIN_DIR/"
cp -r *.py "$WIN_DIR/" 2>/dev/null || true
cp requirements.txt "$WIN_DIR/" 2>/dev/null || true
cp -r local_docs "$WIN_DIR/" 2>/dev/null || true
cp download_docs.py "$WIN_DIR/" 2>/dev/null || true
cp build-resources/icons/icon.svg "$WIN_DIR/"

# Crea script di avvio Windows
cat > "$WIN_DIR/CAP9000.bat" << 'EOF'
@echo off
cd /d %~dp0
start /B python app.py
timeout /t 3 /nobreak > nul
start http://localhost:5001
EOF

# Crea README per Windows
cat > "$WIN_DIR/README.txt" << 'EOF'
CAP 9000 - Cognitive Assistance Program
========================================

INSTALLAZIONE:
1. Installa Python 3.9+: https://www.python.org/downloads/
2. Installa Ollama: https://ollama.ai/download
3. Apri terminale in questa cartella
4. Esegui: pip install -r requirements.txt
5. Esegui: ollama pull codellama
6. Doppio click su CAP9000.bat

SUPPORTO:
antonio.web2music@gmail.com
EOF

# Crea ZIP per Windows
cd "$DIST_DIR"
ZIP_NAME="CAP-9000-Windows-v1.0.0.zip"
zip -r "$ZIP_NAME" "CAP-9000-Windows"
rm -rf "CAP-9000-Windows"
cd "$PROJECT_DIR"

echo -e "${GREEN}✓${NC} Windows package created: $ZIP_NAME"
echo ""

echo -e "${YELLOW}[5/5]${NC} Copying installers to Desktop..."
cp "$DIST_DIR/$DMG_NAME" "$DESKTOP_DIR/"
cp "$DIST_DIR/$ZIP_NAME" "$DESKTOP_DIR/"

echo -e "${GREEN}✓${NC} Installers copied to Desktop"
echo ""

echo "========================================"
echo -e "${GREEN}✓ BUILD COMPLETED!${NC}"
echo "========================================"
echo ""
echo "Installers created:"
echo "  • macOS: $DESKTOP_DIR/$DMG_NAME"
echo "  • Windows: $DESKTOP_DIR/$ZIP_NAME"
echo ""
echo "Installer size:"
du -h "$DESKTOP_DIR/$DMG_NAME" 2>/dev/null || echo "  • macOS: N/A"
du -h "$DESKTOP_DIR/$ZIP_NAME" 2>/dev/null || echo "  • Windows: N/A"
echo ""
