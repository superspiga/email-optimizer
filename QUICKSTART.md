# Quick Start - Esegui Email Optimizer in 5 minuti

## 1️⃣ Installa Dipendenze

```bash
# Crea ambiente virtuale
python3 -m venv venv

# Attiva ambiente
source venv/bin/activate  # Mac/Linux
# oppure
venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt
```

## 2️⃣ Ottieni API Key Claude

1. Vai su: https://console.anthropic.com/
2. Fai login o registrati
3. Vai su "API Keys"
4. Clicca "Create Key"
5. Copia la chiave (inizia con `sk-ant-`)

## 3️⃣ Configura Account Email

### Opzione A: Gmail con IMAP (PIÙ VELOCE)

**Genera App Password:**
1. Vai su: https://myaccount.google.com/security
2. Abilita "Verifica in due passaggi" se non attiva
3. Cerca "Password per le app"
4. Seleziona "Posta" e "Computer Mac/Windows"
5. Copia la password di 16 caratteri

### Opzione B: Altri provider IMAP

**Gmail:** `imap.gmail.com:993`
**Outlook:** `outlook.office365.com:993`
**Yahoo:** `imap.mail.yahoo.com:993`

## 4️⃣ Crea File .env

Crea file `.env` nella root del progetto:

```env
# API Claude
ANTHROPIC_API_KEY=sk-ant-la-tua-chiave-qui

# Account Email
EMAIL_ACCOUNTS='[
    {
        "name": "Il Mio Gmail",
        "type": "imap",
        "host": "imap.gmail.com",
        "port": 993,
        "email": "tuo@gmail.com",
        "password": "la-tua-app-password-qui",
        "use_ssl": true
    }
]'

# Configurazione (opzionale)
MAX_EMAILS_PER_RUN=10
DAYS_TO_ANALYZE=3
LOG_LEVEL=INFO
```

## 5️⃣ Esegui!

```bash
python main.py
```

## 🎯 Esempio Completo

```bash
# 1. Attiva ambiente
source venv/bin/activate

# 2. Verifica configurazione
cat .env

# 3. Esegui
python main.py

# Vedrai output tipo:
# 🤖 Email Optimizer - Avvio...
# ✓ Configurazione caricata
# ✓ Trovati 1 account email
# ✓ Readers email pronti
# ✓ Claude AI client inizializzato
# 📧 Inizio analisi email...
```

## ⚡ Test Rapido (Solo 5 Email)

Per testare velocemente senza analizzare troppe email:

```bash
# Modifica .env
MAX_EMAILS_PER_RUN=5
DAYS_TO_ANALYZE=1

# Esegui
python main.py
```

## 🐛 Problemi Comuni

### Errore: "ANTHROPIC_API_KEY non configurata"
- Verifica che `.env` esista nella root
- Verifica che la chiave inizi con `sk-ant-`

### Errore: "Authentication failed"
- Gmail: Usa "App Password", NON la password normale
- Verifica email e password corrette
- Verifica che IMAP sia abilitato nelle impostazioni email

### Errore: "No module named 'anthropic'"
```bash
pip install -r requirements.txt
```

## 📊 Dopo l'esecuzione

I risultati vengono mostrati a schermo con:
- 📧 Numero email analizzate
- 🚨 Email urgenti
- ✅ Task da fare
- ⭐ Top email prioritarie

I log sono salvati in: `logs/email_optimizer.log`

## 🔥 Esempi Avanzati

```bash
# Solo email urgenti
python examples/prioritize_emails.py

# Estrai tutti i task
python examples/extract_tasks.py

# Esempio base
python examples/basic_usage.py
```

## 💡 Tips

1. **Prima esecuzione**: Usa `MAX_EMAILS_PER_RUN=5` per test
2. **Costi API**: Ogni email costa ~$0.01-0.03 con Claude
3. **Velocità**: ~2-5 secondi per email
4. **Privacy**: Tutto locale, nessun dato condiviso

## ✅ Checklist Setup

- [ ] Python 3.9+ installato
- [ ] Ambiente virtuale creato e attivato
- [ ] Dipendenze installate (`pip install -r requirements.txt`)
- [ ] API Key Claude ottenuta
- [ ] App Password Gmail generata (o credenziali email)
- [ ] File `.env` creato e configurato
- [ ] Eseguito `python main.py` con successo!
