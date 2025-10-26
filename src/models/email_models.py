"""
Modelli dati per email e analisi
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class Priority(str, Enum):
    """Livelli di priorità"""
    CRITICAL = "critica"
    HIGH = "alta"
    MEDIUM = "media"
    LOW = "bassa"
    MINIMAL = "minima"


class SenderCategory(str, Enum):
    """Categorie di mittenti"""
    CLIENT = "cliente"
    PARTNER = "partner"
    SUPPLIER = "fornitore"
    COLLEAGUE = "collega"
    FRIEND = "amico"
    MARKETING = "marketing"
    SPAM = "spam"
    OTHER = "altro"


class EmailAccount(BaseModel):
    """Configurazione account email"""
    name: str
    type: str  # gmail, imap, outlook
    email: EmailStr
    host: Optional[str] = None
    port: Optional[int] = None
    password: Optional[str] = None
    credentials_file: Optional[str] = None
    use_ssl: bool = True


class EmailMessage(BaseModel):
    """Messaggio email"""
    id: str
    account_name: str
    sender: EmailStr
    sender_name: Optional[str] = None
    recipients: List[EmailStr]
    cc: List[EmailStr] = Field(default_factory=list)
    subject: str
    body: str
    html_body: Optional[str] = None
    date: datetime
    thread_id: Optional[str] = None
    in_reply_to: Optional[str] = None
    references: List[str] = Field(default_factory=list)
    attachments: List[str] = Field(default_factory=list)
    is_read: bool = False
    raw_headers: Optional[Dict[str, Any]] = None


class EmailThread(BaseModel):
    """Thread di conversazione email"""
    thread_id: str
    subject: str
    messages: List[EmailMessage]
    participants: List[EmailStr]
    start_date: datetime
    last_date: datetime
    message_count: int


class PendingTask(BaseModel):
    """Task/azione richiesta"""
    description: str
    deadline: Optional[datetime] = None
    priority: Priority
    mentioned_in_email_id: str
    context: str
    is_completed: bool = False
    extracted_at: datetime = Field(default_factory=datetime.now)


class EmailAnalysis(BaseModel):
    """Analisi completa di un'email"""
    email_id: str
    sender: EmailStr
    sender_name: Optional[str] = None
    subject: str
    date: datetime

    # Classificazione
    sender_category: SenderCategory
    sender_category_confidence: float = Field(ge=0.0, le=1.0)

    # Contesto e analisi
    context_summary: str
    key_points: List[str] = Field(default_factory=list)
    sentiment: str  # positivo, neutro, negativo
    tone: str  # formale, informale, urgente, etc.

    # Prioritizzazione
    priority: Priority
    priority_score: float = Field(ge=0.0, le=1.0)
    requires_response: bool
    response_urgency: str  # immediata, entro_giorno, entro_settimana, nessuna

    # Thread analysis
    thread_id: Optional[str] = None
    thread_context: Optional[str] = None
    previous_messages_count: int = 0

    # Task extraction
    pending_tasks: List[PendingTask] = Field(default_factory=list)
    action_required: bool

    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.now)
    ai_model_used: str = "claude-3-5-sonnet"

    # Suggerimenti
    suggested_actions: List[str] = Field(default_factory=list)
    response_suggestions: Optional[str] = None


class AnalysisReport(BaseModel):
    """Report completo di analisi"""
    generated_at: datetime = Field(default_factory=datetime.now)
    total_emails_analyzed: int
    accounts_analyzed: List[str]

    # Statistiche
    by_priority: Dict[Priority, int] = Field(default_factory=dict)
    by_category: Dict[SenderCategory, int] = Field(default_factory=dict)

    # Email analizzate
    analyses: List[EmailAnalysis]

    # Task aggregati
    all_pending_tasks: List[PendingTask] = Field(default_factory=list)

    # Top priority emails
    high_priority_emails: List[EmailAnalysis] = Field(default_factory=list)

    # Richieste di risposta urgente
    urgent_responses_needed: List[EmailAnalysis] = Field(default_factory=list)
