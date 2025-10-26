"""
Esempio base di utilizzo di Email Optimizer
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config_loader import ConfigLoader
from src.email_reader.email_factory import EmailReaderFactory
from src.ai_agent.email_analyzer import EmailAnalyzer


def main():
    """Esempio base"""

    print("📧 Email Optimizer - Esempio Base\n")

    # 1. Carica configurazione
    config = ConfigLoader()
    accounts = config.load_email_accounts()

    print(f"✓ Caricati {len(accounts)} account")

    # 2. Crea readers
    readers = EmailReaderFactory.create_readers_from_config(accounts)

    # 3. Crea analyzer
    analyzer = EmailAnalyzer(readers=readers)

    # 4. Analizza email (ultimi 3 giorni)
    print("\n⏳ Analisi in corso...\n")

    report = analyzer.analyze_all_accounts(
        days=3,
        max_emails=20
    )

    # 5. Mostra risultati
    print(f"📊 Email analizzate: {report.total_emails_analyzed}")
    print(f"🚨 Email urgenti: {len(report.urgent_responses_needed)}")
    print(f"✅ Task pendenti: {len(report.all_pending_tasks)}")

    # 6. Mostra top 5 email prioritarie
    print("\n⭐ Top 5 Email Prioritarie:\n")

    for i, analysis in enumerate(report.high_priority_emails[:5], 1):
        print(f"{i}. {analysis.subject}")
        print(f"   Da: {analysis.sender}")
        print(f"   Categoria: {analysis.sender_category.value}")
        print(f"   Priorità: {analysis.priority.value}")
        print(f"   Richiede risposta: {'Sì' if analysis.requires_response else 'No'}")
        print()


if __name__ == "__main__":
    main()
