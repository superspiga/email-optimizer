# Email Optimizer - Agente AI per l'analisi intelligente delle email

Un agente AI avanzato che legge, analizza e prioritizza le tue email da diversi account, identificando mittenti, contesto e azioni richieste.

## 🎯 Funzionalità

- **Multi-account**: Supporto per più account email (Gmail, Outlook, IMAP)
- **Classificazione intelligente**: Identifica automaticamente il tipo di mittente (cliente, partner, fornitore, amico, etc.)
- **Analisi del contesto**: Comprende il contesto e l'urgenza di ogni email
- **Analisi thread**: Analizza le conversazioni precedenti per continuità
- **Prioritizzazione**: Suggerisce quali email richiedono risposta urgente
- **Estrazione task**: Identifica azioni richieste non completate
- **AI-Powered**: Utilizza Claude AI per analisi semantica avanzata

## 🚀 Installazione

```bash
# Clona il repository
git clone <repository-url>
cd email-optimizer

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Configura variabili d'ambiente
cp .env.example .env
# Modifica .env con le tue credenziali
```

## ⚙️ Configurazione

### 1. API Key Claude
Ottieni una API key da [Anthropic Console](https://console.anthropic.com/)

### 2. Configurazione Email
Aggiungi i tuoi account email nel file `.env`:

```env
# Claude AI API
ANTHROPIC_API_KEY=your-api-key-here

# Account Email (puoi configurarne multipli)
EMAIL_ACCOUNTS='[
    {
        "name": "Gmail Personale",
        "type": "gmail",
        "email": "tuo@gmail.com",
        "credentials": "path/to/credentials.json"
    },
    {
        "name": "Email Lavoro",
        "type": "imap",
        "host": "imap.example.com",
        "port": 993,
        "email": "tuo@lavoro.com",
        "password": "your-password"
    }
]'
```

### 3. Classificazione Mittenti
Personalizza le categorie nel file `config/sender_categories.json`

## 📖 Utilizzo

### Analisi base
```python
from src.email_analyzer import EmailAnalyzer

analyzer = EmailAnalyzer()
results = analyzer.analyze_all_accounts()

for email_analysis in results:
    print(f"Da: {email_analysis.sender}")
    print(f"Categoria: {email_analysis.sender_category}")
    print(f"Priorità: {email_analysis.priority}")
    print(f"Task da fare: {email_analysis.pending_tasks}")
```

### Analisi con prioritizzazione
```python
# Ottieni solo email ad alta priorità
high_priority = analyzer.get_high_priority_emails()

# Ottieni task non completati
pending_tasks = analyzer.extract_all_pending_tasks()
```

## 🏗️ Architettura

```
email-optimizer/
├── src/
│   ├── email_reader/       # Connessione e lettura email
│   ├── ai_agent/          # Agente AI per analisi
│   ├── models/            # Modelli dati
│   └── utils/             # Utility
├── config/                # File di configurazione
├── tests/                 # Test unitari
└── examples/              # Esempi d'uso
```

## 🔒 Privacy e Sicurezza

- Le email vengono processate localmente
- Le chiamate API a Claude sono crittografate
- Le credenziali email sono memorizzate solo localmente
- Nessun dato viene condiviso con terze parti

## 📝 Licenza

MIT License

## 🤝 Contributi

Contributi, issues e feature requests sono benvenuti!
