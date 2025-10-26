"""
Test per modelli dati
"""

import pytest
from datetime import datetime
from src.models import (
    EmailMessage,
    EmailAccount,
    Priority,
    SenderCategory,
    PendingTask
)


def test_email_message_creation():
    """Test creazione EmailMessage"""
    email = EmailMessage(
        id="123",
        account_name="Test",
        sender="test@example.com",
        recipients=["recipient@example.com"],
        subject="Test Subject",
        body="Test body",
        date=datetime.now()
    )

    assert email.id == "123"
    assert email.sender == "test@example.com"
    assert email.subject == "Test Subject"


def test_priority_enum():
    """Test Priority enum"""
    assert Priority.CRITICAL.value == "critica"
    assert Priority.HIGH.value == "alta"
    assert Priority.MEDIUM.value == "media"


def test_sender_category_enum():
    """Test SenderCategory enum"""
    assert SenderCategory.CLIENT.value == "cliente"
    assert SenderCategory.PARTNER.value == "partner"
    assert SenderCategory.FRIEND.value == "amico"


def test_pending_task_creation():
    """Test creazione PendingTask"""
    task = PendingTask(
        description="Inviare documento",
        priority=Priority.HIGH,
        mentioned_in_email_id="123",
        context="Email dal cliente"
    )

    assert task.description == "Inviare documento"
    assert task.priority == Priority.HIGH
    assert task.is_completed == False


def test_email_account_validation():
    """Test validazione EmailAccount"""
    account = EmailAccount(
        name="Test",
        type="gmail",
        email="valid@example.com"
    )

    assert account.email == "valid@example.com"
    assert account.use_ssl == True  # default


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
