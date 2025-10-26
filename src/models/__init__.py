"""
Modelli dati per Email Optimizer
"""

from .email_models import (
    EmailMessage,
    EmailThread,
    EmailAccount,
    SenderCategory,
    EmailAnalysis,
    PendingTask,
    Priority
)

__all__ = [
    "EmailMessage",
    "EmailThread",
    "EmailAccount",
    "SenderCategory",
    "EmailAnalysis",
    "PendingTask",
    "Priority"
]
