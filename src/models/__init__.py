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
    Priority,
    AnalysisReport
)

__all__ = [
    "EmailMessage",
    "EmailThread",
    "EmailAccount",
    "SenderCategory",
    "EmailAnalysis",
    "PendingTask",
    "Priority",
    "AnalysisReport"
]
