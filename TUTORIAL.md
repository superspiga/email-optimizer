# Tutorial: Configurazione Email Optimizer

Guida completa per configurare e utilizzare Email Optimizer.

## 1. Installazione

### Prerequisiti
- Python 3.9 o superiore
- pip installato
- Account Claude AI (API key)
- Account email da analizzare

### Passi

```bash
# Clona il repository
git clone <url>
cd email-optimizer

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt
```

## 2. Configurazione Claude AI

1. Vai su [https://console.anthropic.com/](https://console.anthropic.com/)
2. Crea un account se non ne hai uno
3. Vai su "API Keys"
4. Genera una nuova API key
5. Copia la chiave (inizia con `sk-ant-...`)

## 3. Configurazione Account Email

### Opzione A: Gmail (Consigliato)

**Passo 1: Abilita Gmail API**

1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto
3. Abilita "Gmail API"
4. Vai su "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Tipo applicazione: "Desktop app"
6. Scarica il file JSON delle credenziali
7. Salva come `credentials/gmail_credentials.json`

**Passo 2: Configura .env**

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here

EMAIL_ACCOUNTS='[
    {
        "name": "Gmail Personale",
        "type": "gmail",
        "email": "tuo@gmail.com",
        "credentials_file": "credentials/gmail_credentials.json"
    }
]'
```

### Opzione B: IMAP (Gmail, Outlook, etc.)

**Per Gmail:**

1. Vai su [myaccount.google.com/security](https://myaccount.google.com/security)
2. Abilita "2-Step Verification"
3. Vai su "App passwords"
4. Genera password per "Mail"
5. Copia la password generata

**Configurazione .env:**

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here

EMAIL_ACCOUNTS='[
    {
        "name": "Gmail IMAP",
        "type": "imap",
        "host": "imap.gmail.com",
        "port": 993,
        "email": "tuo@gmail.com",
        "password": "your-app-password-here",
        "use_ssl": true
    }
]'
```

**Per Outlook:**

```env
EMAIL_ACCOUNTS='[
    {
        "name": "Outlook",
        "type": "imap",
        "host": "outlook.office365.com",
        "port": 993,
        "email": "tuo@outlook.com",
        "password": "your-password",
        "use_ssl": true
    }
]'
```

## 4. Configurazione Completa

Crea file `.env` nella root del progetto:

```env
# Claude AI
ANTHROPIC_API_KEY=sk-ant-your-key-here
AI_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.3

# Account Email (puoi averne multipli)
EMAIL_ACCOUNTS='[
    {
        "name": "Gmail Lavoro",
        "type": "gmail",
        "email": "lavoro@gmail.com",
        "credentials_file": "credentials/gmail_credentials.json"
    },
    {
        "name": "Email Personale",
        "type": "imap",
        "host": "imap.gmail.com",
        "port": 993,
        "email": "personale@gmail.com",
        "password": "app-password-here",
        "use_ssl": true
    }
]'

# Configurazione analisi
MAX_EMAILS_PER_RUN=50
DAYS_TO_ANALYZE=7

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/email_optimizer.log
```

## 5. Primo Utilizzo

### Test di base

```bash
python main.py
```

Questo:
1. Connette agli account configurati
2. Recupera email degli ultimi 7 giorni
3. Analizza ogni email con Claude AI
4. Mostra report dettagliato

### Personalizza categorie mittenti

Modifica `config/sender_categories.json` per personalizzare:

```json
{
  "categories": [
    {
      "name": "cliente",
      "keywords": ["ordine", "preventivo", "acquisto"],
      "domains": ["clienteimportante.com"],
      "priority_weight": 0.9
    }
  ]
}
```

## 6. Utilizzo Avanzato

### Esempio: Solo email urgenti

```python
from src.email_analyzer import EmailAnalyzer

analyzer = EmailAnalyzer()
report = analyzer.analyze_all_accounts(days=3)

for email in report.urgent_responses_needed:
    print(f"URGENTE: {email.subject}")
    print(f"  Azioni: {email.suggested_actions}")
```

### Esempio: Estrai tutti i task

```python
report = analyzer.analyze_all_accounts()

for task in report.all_pending_tasks:
    if task.priority.value == "critica":
        print(f"⚠️ {task.description}")
        print(f"   Scadenza: {task.deadline}")
```

## 7. Risoluzione Problemi

### Errore: "ANTHROPIC_API_KEY non configurata"
- Verifica che il file `.env` esista
- Verifica che la chiave sia corretta
- La chiave deve iniziare con `sk-ant-`

### Errore connessione Gmail
- Verifica che Gmail API sia abilitata
- Verifica che il file credentials sia nel path corretto
- Al primo accesso si aprirà browser per autorizzazione

### Errore connessione IMAP
- Verifica host e porta corretti
- Per Gmail usa "App Password", non password normale
- Verifica che IMAP sia abilitato nelle impostazioni email

## 8. Best Practices

1. **Non committare credenziali**: `.env` e `credentials/` sono in `.gitignore`
2. **Limita email per test**: Usa `MAX_EMAILS_PER_RUN=10` per test
3. **Monitora costi API**: Claude ha limiti di rate e costi
4. **Backup configurazioni**: Salva configurazioni personalizzate

## 9. Prossimi Passi

- Esplora `examples/` per casi d'uso specifici
- Personalizza prompt in `src/ai_agent/prompts.py`
- Integra con task manager/calendario
- Crea automazioni con cron/scheduler

## Supporto

Per problemi o domande:
- Controlla i log in `logs/email_optimizer.log`
- Leggi documentazione API: [docs.anthropic.com](https://docs.anthropic.com)
- Apri issue su GitHub
