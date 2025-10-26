"""
Esempio: Prioritizzazione email
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config_loader import ConfigLoader
from src.email_reader.email_factory import EmailReaderFactory
from src.ai_agent.email_analyzer import EmailAnalyzer


def main():
    """Esempio prioritizzazione"""

    print("⚡ Email Optimizer - Prioritizzazione\n")

    # Setup
    config = ConfigLoader()
    accounts = config.load_email_accounts()
    readers = EmailReaderFactory.create_readers_from_config(accounts)
    analyzer = EmailAnalyzer(readers=readers)

    # Analizza
    print("⏳ Analisi email in corso...\n")
    report = analyzer.analyze_all_accounts(days=5, max_emails=30)

    # Email urgenti
    urgent = report.urgent_responses_needed

    print(f"🚨 {len(urgent)} email richiedono risposta urgente\n")

    # Mostra dettagli
    for i, email in enumerate(urgent, 1):
        print(f"{i}. [{email.priority.value.upper()}] {email.subject}")
        print(f"   Da: {email.sender_name or email.sender}")
        print(f"   Categoria: {email.sender_category.value}")
        print(f"   Urgenza risposta: {email.response_urgency}")
        print(f"   Riassunto: {email.context_summary}")

        if email.suggested_actions:
            print(f"   Azioni suggerite:")
            for action in email.suggested_actions:
                print(f"     • {action}")

        print()

    # Statistiche per categoria mittente
    print("\n📊 Email per categoria mittente:\n")
    for category, count in sorted(
        report.by_category.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"  • {category}: {count}")


if __name__ == "__main__":
    main()
