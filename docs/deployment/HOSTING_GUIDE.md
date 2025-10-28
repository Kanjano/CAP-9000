# 🌐 CAP 9000 - Guida Hosting Gratuito Landing Page

Guida per pubblicare la landing page di CAP 9000 su hosting gratuito.

---

## 🎯 Opzioni Hosting Gratuito

### **1. GitHub Pages** (Raccomandato) ⭐

**Pro:**
- ✅ Gratuito illimitato
- ✅ HTTPS automatico
- ✅ Custom domain supportato
- ✅ Deploy automatico da Git
- ✅ CDN globale

**Contro:**
- ⚠️ Solo siti statici
- ⚠️ Limite 1GB storage

**Setup:**

```bash
# 1. Crea repository GitHub
# Vai su github.com e crea nuovo repo "cap9000-website"

# 2. Inizializza Git nella cartella landing
cd /path/to/project
git init
git add landing-page.html
git commit -m "Initial commit"

# 3. Aggiungi remote e push
git remote add origin https://github.com/TUO_USERNAME/cap9000-website.git
git branch -M main
git push -u origin main

# 4. Abilita GitHub Pages
# Vai su: Settings > Pages
# Source: main branch
# Folder: / (root)
# Save

# 5. Il sito sarà disponibile su:
# https://TUO_USERNAME.github.io/cap9000-website/landing-page.html
```

**Custom Domain:**
```bash
# Aggiungi file CNAME nella root
echo "cap9000.tuodominio.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push

# Configura DNS:
# Type: CNAME
# Name: cap9000
# Value: TUO_USERNAME.github.io
```

---

### **2. Netlify** ⭐⭐

**Pro:**
- ✅ Gratuito illimitato
- ✅ Deploy automatico
- ✅ HTTPS automatico
- ✅ Custom domain gratuito
- ✅ Form handling
- ✅ Redirects e headers

**Contro:**
- ⚠️ Limite 100GB bandwidth/mese

**Setup:**

```bash
# 1. Crea account su netlify.com

# 2. Installa Netlify CLI
npm install -g netlify-cli

# 3. Login
netlify login

# 4. Deploy
cd /path/to/project
netlify deploy

# 5. Scegli opzioni:
# - Create new site
# - Team: tuo account
# - Site name: cap9000
# - Publish directory: . (current)

# 6. Deploy production
netlify deploy --prod

# Sito disponibile su:
# https://cap9000.netlify.app
```

**Configurazione netlify.toml:**
```toml
[build]
  publish = "."

[[redirects]]
  from = "/"
  to = "/landing-page.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
```

---

### **3. Vercel** ⭐⭐

**Pro:**
- ✅ Gratuito illimitato
- ✅ Deploy automatico
- ✅ HTTPS automatico
- ✅ Edge network globale
- ✅ Analytics

**Contro:**
- ⚠️ Limite 100GB bandwidth/mese

**Setup:**

```bash
# 1. Crea account su vercel.com

# 2. Installa Vercel CLI
npm install -g vercel

# 3. Login
vercel login

# 4. Deploy
cd /path/to/project
vercel

# Sito disponibile su:
# https://cap9000.vercel.app
```

---

### **4. Cloudflare Pages** ⭐⭐⭐

**Pro:**
- ✅ Gratuito illimitato
- ✅ Bandwidth illimitato
- ✅ HTTPS automatico
- ✅ CDN globale velocissimo
- ✅ Deploy automatico

**Contro:**
- ⚠️ Limite 500 build/mese

**Setup:**

```bash
# 1. Crea account su pages.cloudflare.com

# 2. Connect Git repository
# - Autorizza GitHub
# - Seleziona repository
# - Configure build:
#   - Build command: (vuoto)
#   - Build output: /
#   - Root directory: /

# 3. Deploy automatico ad ogni push

# Sito disponibile su:
# https://cap9000.pages.dev
```

---

### **5. Render** ⭐

**Pro:**
- ✅ Gratuito
- ✅ HTTPS automatico
- ✅ Deploy automatico

**Contro:**
- ⚠️ Limite 100GB bandwidth/mese
- ⚠️ Sleep dopo inattività

**Setup:**

```bash
# 1. Crea account su render.com

# 2. New Static Site
# - Connect repository
# - Build command: (vuoto)
# - Publish directory: .

# Sito disponibile su:
# https://cap9000.onrender.com
```

---

## 🎯 Raccomandazione

### **Per CAP 9000:**

**Opzione Migliore: Cloudflare Pages** ⭐⭐⭐

**Perché:**
- ✅ Bandwidth illimitato (importante per download installer)
- ✅ CDN velocissimo globale
- ✅ Gratuito per sempre
- ✅ Deploy automatico
- ✅ HTTPS incluso

**Setup Rapido:**

```bash
# 1. Push su GitHub
cd /path/to/project
git init
git add landing-page.html
git add build-resources/icons/
git commit -m "Landing page CAP 9000"
git remote add origin https://github.com/antoniocangiano/cap9000-website.git
git push -u origin main

# 2. Vai su pages.cloudflare.com
# 3. Connect GitHub
# 4. Seleziona repository
# 5. Deploy!

# URL finale:
# https://cap9000.pages.dev
# o custom: https://cap9000.com
```

---

## 📁 Struttura Repository per Hosting

```
cap9000-website/
├── index.html                  # Rinomina landing-page.html
├── assets/
│   ├── icon.svg               # Icona HAL
│   └── icon.png               # Icona PNG
├── downloads/
│   ├── CAP-9000-macOS-v1.0.0.dmg
│   └── CAP-9000-Windows-v1.0.0.zip
├── README.md
└── CNAME                      # Per custom domain
```

**Prepara file:**

```bash
# Crea struttura
mkdir -p cap9000-website/assets
mkdir -p cap9000-website/downloads

# Copia file
cp landing-page.html cap9000-website/index.html
cp build-resources/icons/icon.svg cap9000-website/assets/
cp build-resources/icons/icon.png cap9000-website/assets/
cp ~/Desktop/CAP-9000-macOS-v1.0.0.dmg cap9000-website/downloads/
cp ~/Desktop/CAP-9000-Windows-v1.0.0.zip cap9000-website/downloads/

# Aggiorna link in index.html
# Cambia:
# <button>Download macOS</button>
# Con:
# <a href="downloads/CAP-9000-macOS-v1.0.0.dmg" download>Download macOS</a>
```

---

## 🔗 Link Download Funzionanti

**Aggiorna landing-page.html:**

```html
<!-- Download Buttons -->
<div class="download-buttons">
    <a href="downloads/CAP-9000-macOS-v1.0.0.dmg" 
       download 
       class="download-btn">
        <span class="btn-icon">🍎</span>
        Download macOS
        <span class="btn-size">(748 KB)</span>
    </a>
    
    <a href="downloads/CAP-9000-Windows-v1.0.0.zip" 
       download 
       class="download-btn">
        <span class="btn-icon">🪟</span>
        Download Windows
        <span class="btn-size">(396 KB)</span>
    </a>
</div>

<!-- Installer Wizard -->
<div class="wizard-section">
    <h3>Installation Wizard</h3>
    <p>Include download automatico LLM e documentazioni</p>
    <a href="downloads/installer_wizard.sh" 
       download 
       class="download-btn wizard-btn">
        🧙‍♂️ Download Wizard (macOS/Linux)
    </a>
</div>
```

---

## 📊 Analytics (Opzionale)

### **Google Analytics:**

```html
<!-- Aggiungi in <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### **Cloudflare Web Analytics:**

```html
<!-- Aggiungi prima di </body> -->
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' 
        data-cf-beacon='{"token": "TUO_TOKEN"}'></script>
```

---

## 🚀 Deploy Automatico

### **GitHub Actions per Cloudflare Pages:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Publish to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: cap9000
          directory: .
```

---

## 📝 Checklist Pre-Deploy

- [ ] Rinomina `landing-page.html` in `index.html`
- [ ] Copia icone in `assets/`
- [ ] Copia installer in `downloads/`
- [ ] Aggiorna link download
- [ ] Aggiungi dimensioni file
- [ ] Test locale: `python3 -m http.server 8000`
- [ ] Verifica link funzionanti
- [ ] Push su GitHub
- [ ] Deploy su hosting
- [ ] Test sito live
- [ ] Verifica download funzionanti
- [ ] Aggiungi analytics (opzionale)
- [ ] Configura custom domain (opzionale)

---

## 🎯 URL Finale

Dopo il deploy, il sito sarà disponibile su:

- **Cloudflare Pages**: `https://cap9000.pages.dev`
- **GitHub Pages**: `https://antoniocangiano.github.io/cap9000-website/`
- **Netlify**: `https://cap9000.netlify.app`
- **Vercel**: `https://cap9000.vercel.app`

**Custom Domain** (opzionale):
- `https://cap9000.com`
- `https://www.cap9000.com`

---

## 📞 Support

Per problemi di hosting:
- Email: antonio.web2music@gmail.com
- GitHub Issues: repository del sito

---

<div align="center">

**CAP 9000** - Cognitive Assistance Program

© 2025 Antonio Cangiano

</div>
