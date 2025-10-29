# 🚀 Deploy CAP 9000 Landing Page su Netlify

## 📋 Prerequisiti

- Account Netlify (gratuito): https://app.netlify.com/signup
- Repository GitHub: https://github.com/Kanjano/CAP-9000

---

## 🎯 Metodo 1: Deploy Automatico da GitHub (RACCOMANDATO)

### **Passo 1: Login Netlify**
1. Vai su https://app.netlify.com
2. Login con GitHub

### **Passo 2: Nuovo Sito**
1. Click su **"Add new site"** → **"Import an existing project"**
2. Seleziona **"Deploy with GitHub"**
3. Autorizza Netlify ad accedere a GitHub

### **Passo 3: Seleziona Repository**
1. Cerca **"CAP-9000"** o **"Kanjano/CAP-9000"**
2. Click sul repository

### **Passo 4: Configurazione Build**
```
Build settings:
├─ Base directory: website
├─ Build command: (lascia vuoto - sito statico)
├─ Publish directory: . (punto)
└─ Branch: main
```

**IMPORTANTE:** Imposta **Base directory** a `website`

### **Passo 5: Deploy**
1. Click **"Deploy site"**
2. Attendi 1-2 minuti
3. Sito live! 🎉

### **Passo 6: Custom Domain (Opzionale)**
```
1. Site settings → Domain management
2. Add custom domain
3. Configura DNS secondo istruzioni Netlify
```

---

## 🎯 Metodo 2: Deploy Manuale (Drag & Drop)

### **Passo 1: Prepara File**
```bash
cd /Users/antoniocangiano/Desktop/CascadeProjects/windsurf-project
zip -r website-deploy.zip website/
```

### **Passo 2: Deploy**
1. Vai su https://app.netlify.com/drop
2. Drag & drop `website-deploy.zip`
3. Attendi upload
4. Sito live! 🎉

---

## 📁 Struttura Deploy

```
website/                    # Base directory Netlify
├── index.html             # Landing page
├── netlify.toml          # Config Netlify (già presente)
├── downloads/            # Installer
│   ├── CAP-9000-macOS-v1.1.0.dmg
│   ├── CAP-9000-Windows-v1.1.0.zip
│   └── installer_wizard.sh
└── assets/               # Risorse (se presenti)
```

---

## ⚙️ Configurazione netlify.toml

Il file `website/netlify.toml` è già configurato:

```toml
[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/downloads/*"
  [headers.values]
    Content-Disposition = "attachment"
    Cache-Control = "public, max-age=31536000"
```

**Features:**
- ✅ SPA routing (redirects)
- ✅ Security headers
- ✅ Download headers per installer
- ✅ Cache 1 anno per downloads

---

## 🔄 Deploy Automatico (CI/CD)

Netlify rileva automaticamente push su GitHub:

```
1. Fai modifiche locali
2. git add -A
3. git commit -m "update"
4. git push origin main
5. Netlify auto-deploy! 🚀
```

**Tempo deploy:** ~30 secondi

---

## 🌐 URL Sito

Dopo il deploy riceverai:

```
URL temporaneo: https://random-name-123.netlify.app
Custom domain: https://cap9000.netlify.app (configurabile)
```

---

## 📊 Monitoraggio

**Netlify Dashboard:**
- Deploy status
- Build logs
- Analytics
- Forms (se aggiungi)
- Functions (se aggiungi)

---

## 🔧 Troubleshooting

### **Problema: 404 su downloads**
```
Soluzione: Verifica che downloads/ sia committato su GitHub
```

### **Problema: Build fallito**
```
Soluzione: 
1. Verifica Base directory: website
2. Publish directory: .
3. Build command: vuoto (sito statico)
```

### **Problema: Headers non applicati**
```
Soluzione: Verifica netlify.toml in website/
```

---

## ✅ Checklist Deploy

- [ ] Account Netlify creato
- [ ] Repository GitHub collegato
- [ ] Base directory: `website`
- [ ] Publish directory: `.`
- [ ] Build command: vuoto
- [ ] netlify.toml presente
- [ ] Installer in downloads/
- [ ] Deploy completato
- [ ] Sito accessibile
- [ ] Downloads funzionanti

---

## 🚀 Deploy Rapido (Comandi)

```bash
# 1. Verifica file
cd /Users/antoniocangiano/Desktop/CascadeProjects/windsurf-project
ls website/
ls website/downloads/

# 2. Commit e push
git add -A
git commit -m "deploy: Landing page ready"
git push origin main

# 3. Vai su Netlify e configura
# https://app.netlify.com
```

---

## 📝 Note

- **Gratuito:** Piano free Netlify sufficiente
- **Bandwidth:** 100GB/mese free
- **Build:** 300 minuti/mese free
- **SSL:** Certificato HTTPS automatico
- **CDN:** Global CDN incluso

---

## 🎯 Prossimi Passi

1. Deploy su Netlify
2. Configura custom domain (opzionale)
3. Aggiungi analytics (opzionale)
4. Configura form contatti (opzionale)

---

**URL Utili:**
- Netlify: https://app.netlify.com
- Docs: https://docs.netlify.com
- Support: https://answers.netlify.com

**Buon deploy! 🚀**
