"""
Classe base per lettori email
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta

from ..models import EmailMessage, EmailThread, EmailAccount


class BaseEmailReader(ABC):
    """Classe astratta base per tutti i lettori email"""

    def __init__(self, account: EmailAccount):
        self.account = account

    @abstractmethod
    def connect(self) -> bool:
        """Connessione all'account email"""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnessione dall'account"""
        pass

    @abstractmethod
    def fetch_emails(
        self,
        folder: str = "INBOX",
        limit: Optional[int] = None,
        since_date: Optional[datetime] = None,
        unread_only: bool = False
    ) -> List[EmailMessage]:
        """
        Recupera email dall'account

        Args:
            folder: Cartella da cui leggere (default INBOX)
            limit: Numero massimo di email da recuperare
            since_date: Recupera solo email da questa data
            unread_only: Recupera solo email non lette

        Returns:
            Lista di EmailMessage
        """
        pass

    @abstractmethod
    def get_thread(self, thread_id: str) -> Optional[EmailThread]:
        """
        Recupera un thread completo di email

        Args:
            thread_id: ID del thread

        Returns:
            EmailThread o None se non trovato
        """
        pass

    @abstractmethod
    def mark_as_read(self, email_id: str) -> bool:
        """Marca email come letta"""
        pass

    def get_recent_emails(self, days: int = 7) -> List[EmailMessage]:
        """
        Recupera email recenti

        Args:
            days: Numero di giorni di storico

        Returns:
            Lista di email recenti
        """
        since = datetime.now() - timedelta(days=days)
        return self.fetch_emails(since_date=since)
