# 🔐 Code Signing per CAP 9000

## ❌ Problema
macOS blocca app non firmate con errore:
```
"CAP 9000 Code Assistant" è danneggiato e non può essere aperto.
Dovresti spostarlo nel Cestino.
```

## ✅ Soluzioni

### Per Utenti Finali (WORKAROUND)

#### Metodo 1: Rimuovi Quarantena (Più Veloce)
```bash
xattr -cr "/Applications/CAP 9000 Code Assistant.app"
```

#### Metodo 2: Apri con Tasto Destro
1. Tasto destro sull'app → **"Apri"**
2. Click **"Apri"** nel dialog di sicurezza
3. Conferma ancora **"Apri"**

#### Metodo 3: Impostazioni Sistema
1. **Sistema** → **Privacy e Sicurezza**
2. Scorri fino a "Consenti app scaricate da:"
3. Click **"Apri comunque"** accanto a CAP 9000

---

### Per Sviluppatori (SOLUZIONE PERMANENTE)

## 🎯 Code Signing con Apple Developer Certificate

### Prerequisiti
1. **Apple Developer Account** ($99/anno)
   - https://developer.apple.com/programs/

2. **Developer ID Application Certificate**
   - Keychain Access → Certificate Assistant → Request Certificate
   - Upload su Apple Developer Portal
   - Download e installa certificato

### Configurazione electron-builder

**frontend/package.json:**
```json
{
  "build": {
    "appId": "com.kanjano.cap9000",
    "productName": "CAP 9000 Code Assistant",
    "mac": {
      "category": "public.app-category.developer-tools",
      "target": ["dmg", "zip"],
      "icon": "assets/icon.icns",
      "hardenedRuntime": true,
      "gatekeeperAssess": false,
      "entitlements": "build/entitlements.mac.plist",
      "entitlementsInherit": "build/entitlements.mac.plist",
      "identity": "Developer ID Application: Your Name (TEAM_ID)"
    },
    "dmg": {
      "sign": true
    },
    "afterSign": "scripts/notarize.js"
  }
}
```

### Entitlements File

**frontend/build/entitlements.mac.plist:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
</dict>
</plist>
```

### Notarization Script

**frontend/scripts/notarize.js:**
```javascript
const { notarize } = require('@electron/notarize');

exports.default = async function notarizing(context) {
  const { electronPlatformName, appOutDir } = context;
  if (electronPlatformName !== 'darwin') {
    return;
  }

  const appName = context.packager.appInfo.productFilename;

  return await notarize({
    appBundleId: 'com.kanjano.cap9000',
    appPath: `${appOutDir}/${appName}.app`,
    appleId: process.env.APPLE_ID,
    appleIdPassword: process.env.APPLE_APP_SPECIFIC_PASSWORD,
    teamId: process.env.APPLE_TEAM_ID
  });
};
```

### Environment Variables
```bash
export APPLE_ID="your-apple-id@email.com"
export APPLE_APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
export APPLE_TEAM_ID="YOUR_TEAM_ID"
export CSC_LINK="/path/to/certificate.p12"
export CSC_KEY_PASSWORD="certificate-password"
```

### Build con Firma
```bash
npm install --save-dev @electron/notarize
npm run package:mac
```

---

## 🆓 Alternative Gratuite

### Ad-hoc Signing (Senza Developer Account)
```bash
# Firma locale (non distribuibile)
codesign --deep --force --sign - "CAP 9000 Code Assistant.app"
```

### Self-Signed Certificate
```bash
# Crea certificato self-signed
security create-keychain -p password build.keychain
security default-keychain -s build.keychain
security unlock-keychain -p password build.keychain

# Firma app
codesign --deep --force --sign "Developer ID Application" \
  "CAP 9000 Code Assistant.app"
```

**⚠️ NOTA:** Certificati self-signed richiedono comunque workaround utente.

---

## 📝 Documentazione Utente

Aggiungi al README e website:

### Installazione macOS
```markdown
### ⚠️ Avviso Sicurezza macOS

Al primo avvio, macOS potrebbe bloccare l'app. Questo è normale per app non distribuite tramite App Store.

**Soluzione Rapida:**
```bash
xattr -cr "/Applications/CAP 9000 Code Assistant.app"
```

**Oppure:**
1. Tasto destro sull'app → "Apri"
2. Conferma "Apri" nel dialog
```

---

## 🎯 Roadmap

- [ ] Ottenere Apple Developer Account
- [ ] Configurare Code Signing
- [ ] Implementare Notarization
- [ ] Automatizzare processo in CI/CD
- [ ] Distribuire app firmata

**Status Attuale:** App non firmata - richiede workaround utente
**Target:** App firmata e notarizzata per distribuzione seamless
