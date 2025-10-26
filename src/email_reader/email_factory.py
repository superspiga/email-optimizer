"""
Factory per creare lettori email
"""

import logging
from typing import Optional

from .base_reader import BaseEmailReader
from .imap_reader import IMAPEmailReader
from .gmail_reader import GmailEmailReader
from ..models import EmailAccount

logger = logging.getLogger(__name__)


class EmailReaderFactory:
    """Factory per creare il lettore email appropriato"""

    @staticmethod
    def create_reader(account: EmailAccount) -> Optional[BaseEmailReader]:
        """
        Crea il lettore appropriato per il tipo di account

        Args:
            account: Configurazione account

        Returns:
            Istanza del lettore appropriato o None se tipo non supportato
        """
        account_type = account.type.lower()

        if account_type == "gmail":
            return GmailEmailReader(account)

        elif account_type in ["imap", "outlook", "other"]:
            return IMAPEmailReader(account)

        else:
            logger.error(f"Tipo account non supportato: {account_type}")
            return None

    @staticmethod
    def create_readers_from_config(accounts: list[EmailAccount]) -> list[BaseEmailReader]:
        """
        Crea lettori per tutti gli account configurati

        Args:
            accounts: Lista di configurazioni account

        Returns:
            Lista di lettori email
        """
        readers = []

        for account in accounts:
            reader = EmailReaderFactory.create_reader(account)
            if reader:
                readers.append(reader)
            else:
                logger.warning(f"Impossibile creare reader per {account.name}")

        return readers
