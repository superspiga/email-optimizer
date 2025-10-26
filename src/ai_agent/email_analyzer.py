"""
Analizzatore email principale che coordina tutto
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from collections import defaultdict

from .claude_client import ClaudeClient
from .prompts import (
    SYSTEM_PROMPT,
    EMAIL_ANALYSIS_PROMPT,
    THREAD_ANALYSIS_PROMPT,
    TASK_EXTRACTION_PROMPT,
    BATCH_PRIORITIZATION_PROMPT
)
from ..models import (
    EmailMessage,
    EmailThread,
    EmailAnalysis,
    PendingTask,
    Priority,
    SenderCategory,
    AnalysisReport
)
from ..email_reader import BaseEmailReader
from ..utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class EmailAnalyzer:
    """Analizzatore principale di email con AI"""

    def __init__(
        self,
        readers: Optional[List[BaseEmailReader]] = None,
        claude_client: Optional[ClaudeClient] = None,
        config: Optional[ConfigLoader] = None
    ):
        self.readers = readers or []
        self.claude_client = claude_client or ClaudeClient()
        self.config = config or ConfigLoader()

    def analyze_email(
        self,
        email: EmailMessage,
        thread: Optional[EmailThread] = None
    ) -> EmailAnalysis:
        """
        Analizza una singola email

        Args:
            email: Email da analizzare
            thread: Thread opzionale per contesto

        Returns:
            Analisi completa dell'email
        """
        logger.info(f"Analizzando email: {email.subject}")

        try:
            # Prepara prompt per analisi email
            prompt = EMAIL_ANALYSIS_PROMPT.format(
                sender=email.sender,
                sender_name=email.sender_name or "N/A",
                recipients=", ".join(email.recipients),
                subject=email.subject,
                date=email.date.isoformat(),
                account_name=email.account_name,
                body=email.body[:5000]  # Limita lunghezza
            )

            # Chiamata a Claude
            response = self.claude_client.analyze(prompt, SYSTEM_PROMPT)

            # Parse risposta JSON
            analysis_data = json.loads(response)

            # Analisi thread se disponibile
            thread_context = None
            if thread and len(thread.messages) > 1:
                thread_context = self._analyze_thread(thread)

            # Converti task in oggetti PendingTask
            pending_tasks = []
            for task_data in analysis_data.get("pending_tasks", []):
                deadline = None
                if task_data.get("deadline"):
                    try:
                        deadline = datetime.fromisoformat(task_data["deadline"])
                    except:
                        pass

                task = PendingTask(
                    description=task_data["description"],
                    deadline=deadline,
                    priority=Priority(task_data["priority"]),
                    mentioned_in_email_id=email.id,
                    context=task_data.get("context", ""),
                    is_completed=False
                )
                pending_tasks.append(task)

            # Crea EmailAnalysis
            analysis = EmailAnalysis(
                email_id=email.id,
                sender=email.sender,
                sender_name=email.sender_name,
                subject=email.subject,
                date=email.date,
                sender_category=SenderCategory(analysis_data["sender_category"]),
                sender_category_confidence=analysis_data["sender_category_confidence"],
                context_summary=analysis_data["context_summary"],
                key_points=analysis_data.get("key_points", []),
                sentiment=analysis_data["sentiment"],
                tone=analysis_data["tone"],
                priority=Priority(analysis_data["priority"]),
                priority_score=analysis_data["priority_score"],
                requires_response=analysis_data["requires_response"],
                response_urgency=analysis_data["response_urgency"],
                thread_id=email.thread_id,
                thread_context=thread_context,
                previous_messages_count=len(thread.messages) - 1 if thread else 0,
                pending_tasks=pending_tasks,
                action_required=analysis_data["action_required"],
                suggested_actions=analysis_data.get("suggested_actions", []),
                response_suggestions=analysis_data.get("response_suggestions")
            )

            return analysis

        except Exception as e:
            logger.error(f"Errore analisi email {email.id}: {e}")
            # Ritorna analisi base in caso di errore
            return self._create_fallback_analysis(email)

    def _analyze_thread(self, thread: EmailThread) -> str:
        """Analizza un thread per contesto aggiuntivo"""
        try:
            # Prepara riassunto messaggi thread
            thread_messages = []
            for msg in thread.messages[-5:]:  # Ultimi 5 messaggi
                thread_messages.append(
                    f"Da: {msg.sender}\n"
                    f"Data: {msg.date}\n"
                    f"Oggetto: {msg.subject}\n"
                    f"Corpo: {msg.body[:500]}\n"
                )

            prompt = THREAD_ANALYSIS_PROMPT.format(
                thread_messages="\n---\n".join(thread_messages)
            )

            response = self.claude_client.analyze(prompt, SYSTEM_PROMPT)
            thread_data = json.loads(response)

            return thread_data.get("thread_summary", "")

        except Exception as e:
            logger.error(f"Errore analisi thread: {e}")
            return ""

    def analyze_all_accounts(
        self,
        days: int = 7,
        max_emails: int = 50
    ) -> AnalysisReport:
        """
        Analizza email da tutti gli account configurati

        Args:
            days: Giorni di storico da analizzare
            max_emails: Numero massimo di email per account

        Returns:
            Report completo di analisi
        """
        all_analyses = []
        accounts_analyzed = []

        for reader in self.readers:
            try:
                # Connetti
                if not reader.connect():
                    logger.error(f"Impossibile connettersi a {reader.account.name}")
                    continue

                logger.info(f"Recupero email da {reader.account.name}")

                # Recupera email
                emails = reader.get_recent_emails(days=days)
                if max_emails:
                    emails = emails[:max_emails]

                logger.info(f"Trovate {len(emails)} email da analizzare")

                # Analizza ogni email
                for email in emails:
                    # Recupera thread se disponibile
                    thread = None
                    if email.thread_id:
                        thread = reader.get_thread(email.thread_id)

                    # Analizza
                    analysis = self.analyze_email(email, thread)
                    all_analyses.append(analysis)

                accounts_analyzed.append(reader.account.name)

                # Disconnetti
                reader.disconnect()

            except Exception as e:
                logger.error(f"Errore analisi account {reader.account.name}: {e}")
                continue

        # Crea statistiche
        by_priority = defaultdict(int)
        by_category = defaultdict(int)
        all_tasks = []
        high_priority = []
        urgent_responses = []

        for analysis in all_analyses:
            by_priority[analysis.priority] += 1
            by_category[analysis.sender_category] += 1
            all_tasks.extend(analysis.pending_tasks)

            if analysis.priority in [Priority.CRITICAL, Priority.HIGH]:
                high_priority.append(analysis)

            if analysis.requires_response and analysis.response_urgency in ["immediata", "entro_giorno"]:
                urgent_responses.append(analysis)

        # Ordina per priorità
        high_priority.sort(key=lambda x: x.priority_score, reverse=True)
        urgent_responses.sort(key=lambda x: x.priority_score, reverse=True)

        return AnalysisReport(
            total_emails_analyzed=len(all_analyses),
            accounts_analyzed=accounts_analyzed,
            by_priority=dict(by_priority),
            by_category=dict(by_category),
            analyses=all_analyses,
            all_pending_tasks=all_tasks,
            high_priority_emails=high_priority,
            urgent_responses_needed=urgent_responses
        )

    def get_high_priority_emails(
        self,
        min_priority: Priority = Priority.HIGH
    ) -> List[EmailAnalysis]:
        """
        Ottieni solo email ad alta priorità

        Args:
            min_priority: Priorità minima

        Returns:
            Lista di email ad alta priorità
        """
        # Nota: richiede prima di fare analyze_all_accounts
        # Questa è una funzione helper per filtrare
        pass

    def extract_all_pending_tasks(
        self,
        analyses: List[EmailAnalysis]
    ) -> List[PendingTask]:
        """
        Estrai tutti i task pendenti dalle analisi

        Args:
            analyses: Lista di analisi email

        Returns:
            Lista di task pendenti ordinati per priorità
        """
        all_tasks = []
        for analysis in analyses:
            all_tasks.extend(analysis.pending_tasks)

        # Ordina per priorità e deadline
        all_tasks.sort(
            key=lambda t: (
                0 if t.priority == Priority.CRITICAL else
                1 if t.priority == Priority.HIGH else
                2 if t.priority == Priority.MEDIUM else 3,
                t.deadline or datetime.max
            )
        )

        return all_tasks

    def _create_fallback_analysis(self, email: EmailMessage) -> EmailAnalysis:
        """Crea analisi di fallback in caso di errore"""
        return EmailAnalysis(
            email_id=email.id,
            sender=email.sender,
            sender_name=email.sender_name,
            subject=email.subject,
            date=email.date,
            sender_category=SenderCategory.OTHER,
            sender_category_confidence=0.5,
            context_summary="Analisi non disponibile",
            sentiment="neutro",
            tone="formale",
            priority=Priority.MEDIUM,
            priority_score=0.5,
            requires_response=False,
            response_urgency="nessuna",
            action_required=False
        )
