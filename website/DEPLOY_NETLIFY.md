# 🚀 Deploy CAP 9000 su Netlify

## ✅ Stato Attuale

Il sito è **pronto per il deploy** su Netlify con tutte le modifiche più recenti:

- ✅ Design Material stilizzato per HAL 9000
- ✅ Landing page multilingua (IT/EN)
- ✅ Link GitHub corretto: `https://github.com/Kanjano/CAP-9000`
- ✅ Configurazione Netlify (`netlify.toml`)
- ✅ Installer disponibili in `/downloads`

## 📁 Struttura Website

```
website/
├── index.html              # Landing page principale
├── netlify.toml           # Configurazione Netlify
├── assets/
│   ├── icon.png           # Icona CAP 9000
│   └── icon.svg           # Icona vettoriale
└── downloads/
    ├── CAP 9000 Code Assistant-1.0.0-arm64.dmg (96 MB)
    ├── CAP 9000 Code Assistant-1.0.0-arm64-mac.zip (93 MB)
    └── installer_wizard.sh
```

## 🎨 Modifiche Recenti

### Design HAL 9000 Material
- Struttura a 3 layer (outer, middle, inner)
- Riflesso luminoso per effetto glass
- Animazione pulse fluida
- Ombre soft e stratificate

## 🌐 Deploy su Netlify

### Opzione 1: Deploy Manuale (Drag & Drop)

1. Vai su [Netlify](https://app.netlify.com/)
2. Clicca su **"Add new site"** → **"Deploy manually"**
3. Trascina la cartella `website/` nell'area di upload
4. Netlify farà automaticamente il deploy

### Opzione 2: Deploy da Git (Consigliato)

1. Vai su [Netlify](https://app.netlify.com/)
2. Clicca su **"Add new site"** → **"Import an existing project"**
3. Connetti il repository GitHub: `Kanjano/CAP-9000`
4. Configura:
   - **Base directory**: `website`
   - **Build command**: (lascia vuoto)
   - **Publish directory**: `.` (punto)
5. Clicca su **"Deploy site"**

### Opzione 3: Netlify CLI

```bash
# Installa Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy dalla cartella website
cd website
netlify deploy --prod
```

## ⚙️ Configurazione Netlify

Il file `netlify.toml` include:

```toml
[build]
  publish = "."
  
# Redirect per SPA
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# Security headers
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"

# Cache per downloads
[[headers]]
  for = "/downloads/*"
  [headers.values]
    Content-Disposition = "attachment"
    Cache-Control = "public, max-age=31536000"
```

## 🔗 URL Personalizzato (Opzionale)

Dopo il deploy, puoi configurare un dominio personalizzato:

1. Vai su **Site settings** → **Domain management**
2. Clicca su **"Add custom domain"**
3. Segui le istruzioni per configurare DNS

Esempio: `cap9000.netlify.app` → `cap9000.yourdomain.com`

## ✨ Features della Landing Page

- **Multilingua**: Rilevamento automatico IT/EN
- **HAL 9000 Eye**: Design Material con animazione pulse
- **Responsive**: Ottimizzato per mobile e desktop
- **SEO Ready**: Meta tags e descrizioni
- **Performance**: Nessuna dipendenza esterna pesante
- **Open Source**: Link diretto a GitHub

## 📊 Dimensioni File

- `index.html`: ~31 KB
- `icon.png`: ~80 KB
- `icon.svg`: ~2 KB
- **Totale website** (senza downloads): ~113 KB
- **Con installer**: ~190 MB

## 🎯 Prossimi Passi

1. ✅ Deploy su Netlify
2. ⏳ Configurare dominio personalizzato (opzionale)
3. ⏳ Aggiungere Google Analytics (opzionale)
4. ⏳ Configurare form di contatto Netlify (opzionale)

## 📝 Note

- Gli installer in `/downloads` sono file grandi (~90-96 MB ciascuno)
- Netlify ha un limite di 100 MB per file in deploy gratuito
- Considera di hostare gli installer su GitHub Releases se necessario

## 🔒 Sicurezza

Headers di sicurezza già configurati:
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

---

**Pronto per il deploy!** 🚀

Creato: 7 Novembre 2025
