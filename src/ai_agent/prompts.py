"""
Prompt templates per l'agente AI
"""


SYSTEM_PROMPT = """Sei un assistente AI esperto nell'analisi di email aziendali e personali.
Il tuo compito è analizzare email per aiutare l'utente a gestire meglio la sua casella di posta.

Devi essere:
- Preciso nell'identificare il tipo di mittente e il contesto
- Attento nell'identificare azioni richieste e scadenze
- Obiettivo nel determinare le priorità
- Conciso ma completo nelle tue analisi

Rispondi sempre in formato JSON valido."""


EMAIL_ANALYSIS_PROMPT = """Analizza questa email e fornisci un'analisi completa in formato JSON.

**EMAIL:**
Da: {sender} ({sender_name})
A: {recipients}
Oggetto: {subject}
Data: {date}
Account: {account_name}

Corpo:
{body}

---

Fornisci l'analisi in questo formato JSON:

{{
  "sender_category": "<cliente|partner|fornitore|collega|amico|marketing|spam|altro>",
  "sender_category_confidence": <0.0-1.0>,
  "context_summary": "<breve riassunto del contenuto in 1-2 frasi>",
  "key_points": ["<punto chiave 1>", "<punto chiave 2>", ...],
  "sentiment": "<positivo|neutro|negativo>",
  "tone": "<formale|informale|urgente|amichevole|professionale>",
  "priority": "<critica|alta|media|bassa|minima>",
  "priority_score": <0.0-1.0>,
  "requires_response": <true|false>,
  "response_urgency": "<immediata|entro_giorno|entro_settimana|nessuna>",
  "action_required": <true|false>,
  "pending_tasks": [
    {{
      "description": "<descrizione del task>",
      "deadline": "<YYYY-MM-DD o null>",
      "priority": "<critica|alta|media|bassa|minima>",
      "context": "<contesto del task>"
    }}
  ],
  "suggested_actions": ["<azione suggerita 1>", "<azione suggerita 2>"],
  "response_suggestions": "<suggerimenti per la risposta se necessaria>"
}}

Considera:
1. **Categoria mittente**: Analizza il dominio, il contenuto, il tono per classificare
2. **Priorità**: Valuta urgenza, importanza del mittente, presenza di scadenze
3. **Task**: Identifica richieste esplicite (es. "puoi inviarmi...", "per favore conferma...")
4. **Deadline**: Cerca date o riferimenti temporali (es. "entro venerdì", "urgente")

Rispondi SOLO con il JSON, senza altro testo."""


THREAD_ANALYSIS_PROMPT = """Analizza questo thread di email per fornire contesto aggiuntivo.

**THREAD:**
{thread_messages}

---

Fornisci un'analisi del thread in formato JSON:

{{
  "thread_summary": "<riassunto della conversazione>",
  "conversation_flow": "<breve descrizione del flusso della conversazione>",
  "open_questions": ["<domanda 1>", "<domanda 2>"],
  "pending_from_user": ["<azione pendente 1>", "<azione pendente 2>"],
  "last_action_required": "<ultima azione richiesta all'utente, se presente>"
}}

Concentrati su:
1. Identificare se ci sono richieste fatte all'utente che non hanno ricevuto risposta
2. Domande senza risposta
3. Impegni presi dall'utente non ancora mantenuti

Rispondi SOLO con il JSON."""


BATCH_PRIORITIZATION_PROMPT = """Data questa lista di email già analizzate, determina l'ordine di priorità globale.

**EMAIL DA PRIORITIZZARE:**
{email_summaries}

---

Fornisci una lista ordinata in formato JSON:

{{
  "priority_order": [
    {{
      "email_id": "<id>",
      "rank": <1-N>,
      "reason": "<motivo della priorità>"
    }}
  ],
  "urgent_count": <numero di email urgenti>,
  "recommendations": ["<raccomandazione generale 1>", "<raccomandazione 2>"]
}}

Criteri di prioritizzazione:
1. Email da clienti con richieste urgenti
2. Email con scadenze imminenti
3. Email da partner/colleghi su progetti in corso
4. Email che richiedono conferme
5. Email informative ma importanti
6. Email marketing/newsletter

Rispondi SOLO con il JSON."""


TASK_EXTRACTION_PROMPT = """Estrai tutti i task e le azioni richieste da questo set di email.

**EMAIL:**
{emails_content}

---

Fornisci una lista completa di task in formato JSON:

{{
  "tasks": [
    {{
      "description": "<descrizione task>",
      "source_email_id": "<id email>",
      "sender": "<mittente>",
      "deadline": "<YYYY-MM-DD o null>",
      "priority": "<critica|alta|media|bassa|minima>",
      "estimated_effort": "<veloce|medio|lungo>",
      "context": "<contesto completo>"
    }}
  ],
  "task_count": <numero totale task>,
  "high_priority_count": <numero task alta priorità>,
  "tasks_with_deadline": <numero task con scadenza>
}}

Cerca pattern come:
- "puoi", "potresti", "per favore"
- "devi", "è necessario", "richiesto"
- "conferma", "invia", "prepara"
- Riferimenti a date/scadenze

Rispondi SOLO con il JSON."""
