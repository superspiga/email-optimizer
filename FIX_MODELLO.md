# 🔧 FIX MODELLO CLAUDE

Il modello `claude-3-5-sonnet-20241022` non è disponibile.

## ✅ SOLUZIONE RAPIDA

Apri il file `.env` e aggiungi/modifica questa riga:

```env
AI_MODEL=claude-3-5-sonnet-20241022
```

## Modelli Disponibili

Se anche questo non funziona, prova in ordine:

```env
# Opzione 1: Claude 3.5 Sonnet (Ottobre 2024)
AI_MODEL=claude-3-5-sonnet-20241022

# Opzione 2: Claude 3.5 Sonnet (Giugno 2024) - PIÙ STABILE
AI_MODEL=claude-3-5-sonnet-20240620

# Opzione 3: Claude 3 Opus (più potente ma costoso)
AI_MODEL=claude-3-opus-20240229

# Opzione 4: Claude 3 Sonnet (economico)
AI_MODEL=claude-3-sonnet-20240229
```

## 🎯 File .env Completo Corretto

```env
# Claude AI
ANTHROPIC_API_KEY=sk-ant-la-tua-chiave-qui
AI_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.3

# Account Email
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

# Configurazione
MAX_EMAILS_PER_RUN=5
DAYS_TO_ANALYZE=1
LOG_LEVEL=INFO
LOG_FILE=logs/email_optimizer.log
```

## Poi rilancia:

```bash
python main.py
```
