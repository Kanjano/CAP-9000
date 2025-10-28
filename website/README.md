# 🔴 CAP 9000 - Official Website

Landing page ufficiale per CAP 9000 - Cognitive Assistance Program

## 🌐 Live Site

**URL:** https://cap9000.netlify.app

## 📁 Struttura

```
website/
├── index.html              # Landing page
├── netlify.toml           # Configurazione Netlify
├── README.md              # Questo file
├── assets/
│   ├── icon.svg          # Icona HAL SVG
│   └── icon.png          # Icona HAL PNG
└── downloads/
    ├── CAP-9000-macOS-v1.0.0.dmg        # 748 KB
    ├── CAP-9000-Windows-v1.0.0.zip      # 396 KB
    └── installer_wizard.sh               # 8 KB
```

## 🚀 Deploy su Netlify

### Metodo 1: Netlify CLI

```bash
# Installa Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd website
netlify deploy --prod
```

### Metodo 2: Netlify Dashboard

1. Vai su https://app.netlify.com
2. Click "Add new site" > "Deploy manually"
3. Trascina cartella `website/`
4. Deploy automatico!

### Metodo 3: GitHub + Netlify (Raccomandato)

1. Push su GitHub
2. Connetti repository a Netlify
3. Deploy automatico ad ogni push

## 📦 Download Disponibili

| File | Dimensione | Piattaforma |
|------|------------|-------------|
| CAP-9000-macOS-v1.0.0.dmg | 748 KB | macOS 10.15+ |
| CAP-9000-Windows-v1.0.0.zip | 396 KB | Windows 10+ |
| installer_wizard.sh | 8 KB | macOS/Linux |

## 🎨 Features Landing Page

- ✅ Design HAL 9000 autentico
- ✅ Occhio rosso animato
- ✅ Download diretti installer
- ✅ Multi-lingua (EN/IT)
- ✅ Responsive design
- ✅ Contact section
- ✅ Features showcase

## 🔧 Configurazione Netlify

Il file `netlify.toml` configura:

- **Publish directory**: `.` (root)
- **Redirects**: SPA routing
- **Headers**: Security headers
- **Downloads**: Cache e attachment headers

## 📊 Analytics (Opzionale)

Per aggiungere analytics, modifica `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>

<!-- Cloudflare Web Analytics -->
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' 
        data-cf-beacon='{"token": "TOKEN"}'></script>
```

## 🌍 Custom Domain

Per usare dominio personalizzato:

1. Netlify Dashboard > Domain settings
2. Add custom domain
3. Configura DNS:
   - Type: CNAME
   - Name: cap9000 (o www)
   - Value: [your-site].netlify.app

## 📝 Aggiornamento Installer

Per aggiornare gli installer:

```bash
# 1. Crea nuovi installer
./create_installers.sh

# 2. Copia in website/downloads/
cp ~/Desktop/CAP-9000-*.* website/downloads/

# 3. Aggiorna versione in index.html

# 4. Deploy
cd website
netlify deploy --prod
```

## 🔗 Link Utili

- **Repository**: https://github.com/antoniocangiano/cap9000
- **Netlify**: https://cap9000.netlify.app
- **Email**: antonio.web2music@gmail.com

## 📄 License

MIT License - © 2025 Antonio Cangiano
