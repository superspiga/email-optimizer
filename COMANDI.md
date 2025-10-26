# 🚀 Comandi per Eseguire Email Optimizer

## Metodo 1: Setup Automatico (CONSIGLIATO) ⚡

### Mac/Linux:
```bash
# 1. Setup automatico
chmod +x setup.sh
./setup.sh

# 2. Modifica .env con le tue credenziali
nano .env

# 3. Esegui
source venv/bin/activate
python main.py
```

### Windows:
```cmd
# 1. Setup automatico
setup.bat

# 2. Modifica .env con le tue credenziali
notepad .env

# 3. Esegui
venv\Scripts\activate
python main.py
```

---

## Metodo 2: Setup Manuale 🔧

### Mac/Linux:
```bash
# 1. Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Crea file .env
cp .env.example .env
nano .env  # Modifica con le tue credenziali

# 4. Esegui
python main.py
```

### Windows:
```cmd
# 1. Crea ambiente virtuale
python -m venv venv
venv\Scripts\activate

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Crea file .env
copy .env.example .env
notepad .env  # Modifica con le tue credenziali

# 4. Esegui
python main.py
```

---

## 🔑 Credenziali Necessarie

### 1. Claude API Key
```
Vai su: https://console.anthropic.com/
→ API Keys → Create Key
→ Copia la chiave (inizia con sk-ant-)
```

### 2. Gmail App Password
```
Vai su: https://myaccount.google.com/security
→ Verifica in due passaggi (attivala se non attiva)
→ Password per le app → Posta → Computer
→ Copia la password di 16 caratteri
```

### 3. Configura .env
```env
ANTHROPIC_API_KEY=sk-ant-la-tua-chiave

EMAIL_ACCOUNTS='[
    {
        "name": "Gmail",
        "type": "imap",
        "host": "imap.gmail.com",
        "port": 993,
        "email": "tuo@gmail.com",
        "password": "la-tua-app-password",
        "use_ssl": true
    }
]'
```

---

## ▶️ Eseguire il Programma

### Esecuzione Base:
```bash
# Attiva ambiente (se non già attivo)
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Esegui
python main.py
```

### Test con Poche Email:
```bash
# Modifica .env prima:
# MAX_EMAILS_PER_RUN=5
# DAYS_TO_ANALYZE=1

python main.py
```

### Esempi Specifici:
```bash
# Solo email urgenti
python examples/prioritize_emails.py

# Estrai task
python examples/extract_tasks.py

# Esempio base
python examples/basic_usage.py
```

---

## 🐛 Troubleshooting

### Errore: "command not found: python3"
```bash
# Prova con:
python --version

# Se non funziona, installa Python:
# Mac: brew install python3
# Ubuntu: sudo apt install python3
# Windows: https://python.org/downloads
```

### Errore: "No module named 'anthropic'"
```bash
# Riattiva ambiente e reinstalla:
source venv/bin/activate
pip install -r requirements.txt
```

### Errore: "Authentication failed"
```bash
# Gmail: Usa App Password, NON la password normale
# Verifica che IMAP sia abilitato in Gmail Settings
```

### Verificare Configurazione:
```bash
# Controlla che .env esista
cat .env

# Verifica log
cat logs/email_optimizer.log
```

---

## 📊 Cosa Aspettarsi

L'esecuzione richiede circa **2-5 secondi per email**.

Output esempio:
```
🤖 Email Optimizer - Avvio...
✓ Configurazione caricata
✓ Trovati 1 account email
✓ Readers email pronti
✓ Claude AI client inizializzato

📧 Inizio analisi email...

📊 Statistiche Generali
  • Email analizzate: 10
  • Account: Gmail Personale

⚡ Distribuzione Priorità
  • alta: 3
  • media: 5
  • bassa: 2

🚨 Email che richiedono risposta urgente: 2
✅ Task Pendenti: 5
```

---

## 💰 Costi

Con Claude Sonnet 3.5:
- **~$0.01-0.03** per email
- **10 email** = ~$0.20
- **100 email** = ~$2.00

---

## ⏹️ Fermare/Uscire

```bash
# Disattiva ambiente virtuale
deactivate

# Per chiudere, premi CTRL+C durante l'esecuzione
```

---

## 🔄 Esecuzioni Successive

Una volta configurato, le prossime volte:

```bash
# 1. Vai nella directory
cd email-optimizer

# 2. Attiva ambiente
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3. Esegui
python main.py
```

Fatto! 🎉
