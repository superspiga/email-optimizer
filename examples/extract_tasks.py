"""
Esempio: Estrazione task pendenti
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config_loader import ConfigLoader
from src.email_reader.email_factory import EmailReaderFactory
from src.ai_agent.email_analyzer import EmailAnalyzer


def main():
    """Esempio estrazione task"""

    print("✅ Email Optimizer - Estrazione Task\n")

    # Setup
    config = ConfigLoader()
    accounts = config.load_email_accounts()
    readers = EmailReaderFactory.create_readers_from_config(accounts)
    analyzer = EmailAnalyzer(readers=readers)

    # Analizza
    print("⏳ Analisi email in corso...\n")
    report = analyzer.analyze_all_accounts(days=7)

    # Estrai tutti i task
    tasks = report.all_pending_tasks

    print(f"📋 Trovati {len(tasks)} task pendenti\n")

    # Raggruppa per priorità
    critical = [t for t in tasks if t.priority.value == "critica"]
    high = [t for t in tasks if t.priority.value == "alta"]
    medium = [t for t in tasks if t.priority.value == "media"]

    print(f"🔴 Critici: {len(critical)}")
    print(f"🟡 Alta priorità: {len(high)}")
    print(f"🟢 Media priorità: {len(medium)}")

    # Mostra task critici
    if critical:
        print("\n🚨 TASK CRITICI:\n")
        for task in critical:
            print(f"• {task.description}")
            if task.deadline:
                print(f"  Scadenza: {task.deadline.strftime('%Y-%m-%d')}")
            print(f"  Contesto: {task.context[:100]}...")
            print()

    # Mostra task con scadenza
    tasks_with_deadline = [t for t in tasks if t.deadline]
    tasks_with_deadline.sort(key=lambda t: t.deadline)

    if tasks_with_deadline:
        print("\n📅 TASK CON SCADENZA:\n")
        for task in tasks_with_deadline[:10]:
            print(f"• [{task.deadline.strftime('%Y-%m-%d')}] {task.description}")


if __name__ == "__main__":
    main()
