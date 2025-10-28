# 🚀 CAP 9000 - Deploy su Netlify

Guida step-by-step per pubblicare CAP 9000 su Netlify.

---

## 📋 Prerequisiti

- ✅ Account Netlify (gratuito): https://app.netlify.com/signup
- ✅ Account GitHub (opzionale ma raccomandato)
- ✅ Installer creati nella cartella `website/downloads/`

---

## 🎯 Metodo 1: Deploy Manuale (Più Veloce)

### **Step 1: Prepara i File**

I file sono già pronti in `website/`:

```
website/
├── index.html                           ✅
├── netlify.toml                         ✅
├── assets/
│   ├── icon.svg                         ✅
│   └── icon.png                         ✅
└── downloads/
    ├── CAP-9000-macOS-v1.0.0.dmg       ✅
    ├── CAP-9000-Windows-v1.0.0.zip     ✅
    └── installer_wizard.sh              ✅
```

### **Step 2: Deploy su Netlify**

1. **Vai su Netlify:**
   - https://app.netlify.com

2. **Login/Signup:**
   - Usa GitHub, GitLab, Bitbucket o Email

3. **Deploy Manuale:**
   - Click "Add new site"
   - Click "Deploy manually"
   - Trascina la cartella `website/` nella zona di drop
   - Attendi upload (30 secondi - 2 minuti)

4. **Sito Live!**
   - URL temporaneo: `https://random-name-12345.netlify.app`
   - Puoi cambiare il nome in: Site settings > Change site name

### **Step 3: Cambia Nome Sito**

1. Site settings > Site details
2. Click "Change site name"
3. Inserisci: `cap9000`
4. Save
5. **Nuovo URL:** `https://cap9000.netlify.app` 🎉

---

## 🎯 Metodo 2: Deploy da GitHub (Raccomandato)

### **Step 1: Crea Repository GitHub**

```bash
# 1. Vai su github.com
# 2. Click "New repository"
# 3. Nome: cap9000-website
# 4. Public
# 5. Create repository
```

### **Step 2: Push Codice su GitHub**

```bash
# Nella cartella del progetto
cd /Users/antoniocangiano/Desktop/CascadeProjects/windsurf-project

# Aggiungi remote GitHub
git remote add origin https://github.com/antoniocangiano/cap9000-website.git

# Push tutto
git add -A
git commit -m "feat: Website completo con installer scaricabili"
git push -u origin main
```

### **Step 3: Connetti Netlify a GitHub**

1. **Netlify Dashboard:**
   - https://app.netlify.com

2. **New Site from Git:**
   - Click "Add new site"
   - Click "Import an existing project"
   - Click "GitHub"

3. **Autorizza GitHub:**
   - Autorizza Netlify ad accedere ai tuoi repo

4. **Seleziona Repository:**
   - Cerca: `cap9000-website`
   - Click sul repository

5. **Configura Build:**
   - **Branch to deploy:** `main`
   - **Base directory:** `website`
   - **Build command:** (lascia vuoto)
   - **Publish directory:** `.` (punto)
   - Click "Deploy site"

6. **Deploy Automatico:**
   - Netlify fa deploy automaticamente
   - Attendi 1-2 minuti
   - Sito live! 🎉

### **Step 4: Deploy Automatici**

Ora ogni volta che fai push su GitHub:

```bash
# Modifica qualcosa
vim website/index.html

# Commit e push
git add -A
git commit -m "Update landing page"
git push

# Netlify fa deploy automaticamente! 🚀
```

---

## 🎯 Metodo 3: Netlify CLI (Per Developer)

### **Step 1: Installa Netlify CLI**

```bash
npm install -g netlify-cli
```

### **Step 2: Login**

```bash
netlify login
# Si apre browser per autorizzazione
```

### **Step 3: Deploy**

```bash
# Vai nella cartella website
cd website

# Deploy di test
netlify deploy

# Deploy production
netlify deploy --prod
```

### **Step 4: Link al Sito**

```bash
# Collega cartella a sito Netlify esistente
netlify link

# Oppure crea nuovo sito
netlify init
```

---

## 🔗 URL Repository GitHub

**Per creare il repository:**

1. Vai su: https://github.com/new
2. Nome repository: `cap9000-website`
3. Descrizione: `Official website for CAP 9000 - Cognitive Assistance Program`
4. Public
5. Create repository

**Comandi per push:**

```bash
cd /Users/antoniocangiano/Desktop/CascadeProjects/windsurf-project

# Aggiungi remote
git remote add origin https://github.com/antoniocangiano/cap9000-website.git

# Push
git branch -M main
git push -u origin main
```

**URL finale repository:**
```
https://github.com/antoniocangiano/cap9000-website
```

---

## 🌐 URL Sito Finale

Dopo il deploy, il sito sarà disponibile su:

```
https://cap9000.netlify.app
```

**Download diretti:**
- macOS: `https://cap9000.netlify.app/downloads/CAP-9000-macOS-v1.0.0.dmg`
- Windows: `https://cap9000.netlify.app/downloads/CAP-9000-Windows-v1.0.0.zip`
- Wizard: `https://cap9000.netlify.app/downloads/installer_wizard.sh`

---

## ⚙️ Configurazione Avanzata

### **Custom Domain**

1. Netlify Dashboard > Domain settings
2. Add custom domain
3. Inserisci: `cap9000.com`
4. Configura DNS:
   ```
   Type: CNAME
   Name: @
   Value: cap9000.netlify.app
   ```

### **HTTPS**

- ✅ Automatico con Netlify
- ✅ Let's Encrypt gratuito
- ✅ Rinnovo automatico

### **Analytics**

Netlify Analytics (opzionale, $9/mese):
- Site settings > Analytics
- Enable Netlify Analytics

Oppure usa Google Analytics gratuito.

---

## 🔧 Troubleshooting

### **Problema: File non trovati**

```bash
# Verifica struttura
cd website
ls -la

# Deve contenere:
# - index.html
# - netlify.toml
# - assets/
# - downloads/
```

### **Problema: Download non funzionano**

Verifica che i file siano in `website/downloads/`:

```bash
ls -lh website/downloads/
# Deve mostrare:
# CAP-9000-macOS-v1.0.0.dmg
# CAP-9000-Windows-v1.0.0.zip
# installer_wizard.sh
```

### **Problema: Deploy fallisce**

1. Verifica `netlify.toml` presente
2. Verifica `index.html` presente
3. Controlla logs in Netlify Dashboard

---

## 📊 Statistiche Deploy

| Metodo | Tempo | Difficoltà | Auto-Deploy |
|--------|-------|------------|-------------|
| **Manuale** | 2 min | ⭐ | ❌ |
| **GitHub** | 5 min | ⭐⭐ | ✅ |
| **CLI** | 3 min | ⭐⭐⭐ | ✅ |

**Raccomandato:** Metodo GitHub per deploy automatici.

---

## 📝 Checklist Pre-Deploy

- [ ] Installer creati in `website/downloads/`
- [ ] `index.html` aggiornato con link corretti
- [ ] `netlify.toml` presente
- [ ] Icone in `website/assets/`
- [ ] Test locale: `python3 -m http.server 8000`
- [ ] Verifica download funzionanti
- [ ] Account Netlify creato
- [ ] (Opzionale) Repository GitHub creato

---

## 🎉 Deploy Completato!

Dopo il deploy, condividi:

- 🌐 Website: `https://cap9000.netlify.app`
- 📦 GitHub: `https://github.com/antoniocangiano/cap9000-website`
- 📧 Email: antonio.web2music@gmail.com

---

<div align="center">

**CAP 9000** - Cognitive Assistance Program

*"I am putting myself to the fullest possible use."*

© 2025 Antonio Cangiano

</div>
