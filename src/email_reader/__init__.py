"""
Modulo per lettura email da diversi provider
"""

from .base_reader import BaseEmailReader
from .imap_reader import IMAPEmailReader
from .gmail_reader import GmailEmailReader
from .email_factory import EmailReaderFactory

__all__ = [
    "BaseEmailReader",
    "IMAPEmailReader",
    "GmailEmailReader",
    "EmailReaderFactory"
]
