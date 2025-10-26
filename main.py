#!/usr/bin/env python3
"""
Email Optimizer - Agente AI per analisi intelligente email

Script principale per eseguire l'analisi delle email
"""

import sys
from pathlib import Path

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.logger import setup_logging
from src.utils.config_loader import ConfigLoader
from src.email_reader.email_factory import EmailReaderFactory
from src.ai_agent.email_analyzer import EmailAnalyzer
from src.ai_agent.claude_client import ClaudeClient

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress


def print_report_summary(report, console: Console):
    """Stampa riassunto del report"""

    # Header
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]📧 Email Optimizer - Report Analisi[/bold cyan]",
        border_style="cyan"
    ))

    # Statistiche generali
    console.print(f"\n[bold]📊 Statistiche Generali[/bold]")
    console.print(f"  • Email analizzate: [cyan]{report.total_emails_analyzed}[/cyan]")
    console.print(f"  • Account: [cyan]{', '.join(report.accounts_analyzed)}[/cyan]")

    # Priorità
    console.print(f"\n[bold]⚡ Distribuzione Priorità[/bold]")
    for priority, count in report.by_priority.items():
        console.print(f"  • {priority}: [yellow]{count}[/yellow]")

    # Categorie
    console.print(f"\n[bold]📁 Categorie Mittenti[/bold]")
    for category, count in report.by_category.items():
        console.print(f"  • {category}: [yellow]{count}[/yellow]")

    # Email urgenti
    if report.urgent_responses_needed:
        console.print(f"\n[bold red]🚨 Email che richiedono risposta urgente: {len(report.urgent_responses_needed)}[/bold red]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Da", style="cyan", width=25)
        table.add_column("Oggetto", style="white", width=40)
        table.add_column("Priorità", justify="center")
        table.add_column("Urgenza", justify="center")

        for analysis in report.urgent_responses_needed[:10]:  # Top 10
            priority_color = "red" if analysis.priority.value == "critica" else "yellow"
            table.add_row(
                f"{analysis.sender_name or analysis.sender}",
                analysis.subject[:37] + "..." if len(analysis.subject) > 40 else analysis.subject,
                f"[{priority_color}]{analysis.priority.value}[/{priority_color}]",
                analysis.response_urgency
            )

        console.print(table)

    # Task pendenti
    if report.all_pending_tasks:
        console.print(f"\n[bold]✅ Task Pendenti: {len(report.all_pending_tasks)}[/bold]")

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Task", style="white", width=50)
        table.add_column("Priorità", justify="center", width=10)
        table.add_column("Scadenza", justify="center", width=12)

        for task in report.all_pending_tasks[:15]:  # Top 15
            priority_color = "red" if task.priority.value == "critica" else "yellow" if task.priority.value == "alta" else "white"
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "N/A"

            table.add_row(
                task.description[:47] + "..." if len(task.description) > 50 else task.description,
                f"[{priority_color}]{task.priority.value}[/{priority_color}]",
                deadline_str
            )

        console.print(table)

    # Email ad alta priorità
    if report.high_priority_emails:
        console.print(f"\n[bold]⭐ Email Alta Priorità: {len(report.high_priority_emails)}[/bold]")

        for i, analysis in enumerate(report.high_priority_emails[:5], 1):
            console.print(f"\n[bold cyan]{i}. {analysis.subject}[/bold cyan]")
            console.print(f"   Da: {analysis.sender_name or analysis.sender} ([italic]{analysis.sender_category.value}[/italic])")
            console.print(f"   Priorità: [yellow]{analysis.priority.value}[/yellow] (score: {analysis.priority_score:.2f})")
            console.print(f"   Riassunto: {analysis.context_summary}")

            if analysis.suggested_actions:
                console.print(f"   Azioni suggerite:")
                for action in analysis.suggested_actions:
                    console.print(f"     • {action}")


def main():
    """Funzione principale"""

    console = Console()

    console.print("\n[bold cyan]🤖 Email Optimizer - Avvio...[/bold cyan]\n")

    # Carica configurazione
    config = ConfigLoader()

    # Setup logging
    setup_logging(
        log_level=config.log_level,
        log_file=config.log_file
    )

    # Valida configurazione
    if not config.validate_config():
        console.print("[bold red]❌ Configurazione non valida. Verifica .env[/bold red]")
        return 1

    console.print("[green]✓[/green] Configurazione caricata")

    # Carica account email
    accounts = config.load_email_accounts()
    if not accounts:
        console.print("[bold red]❌ Nessun account email configurato[/bold red]")
        return 1

    console.print(f"[green]✓[/green] Trovati {len(accounts)} account email")

    # Crea readers
    readers = EmailReaderFactory.create_readers_from_config(accounts)
    console.print(f"[green]✓[/green] Readers email pronti")

    # Crea Claude client
    claude_client = ClaudeClient(
        api_key=config.anthropic_api_key,
        model=config.ai_model,
        max_tokens=config.max_tokens,
        temperature=config.temperature
    )
    console.print(f"[green]✓[/green] Claude AI client inizializzato")

    # Crea analyzer
    analyzer = EmailAnalyzer(
        readers=readers,
        claude_client=claude_client,
        config=config
    )

    console.print("\n[bold]📧 Inizio analisi email...[/bold]\n")

    # Analizza email
    try:
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Analisi in corso...",
                total=None
            )

            report = analyzer.analyze_all_accounts(
                days=config.days_to_analyze,
                max_emails=config.max_emails_per_run
            )

            progress.update(task, completed=True)

        # Stampa report
        print_report_summary(report, console)

        console.print("\n[bold green]✅ Analisi completata![/bold green]\n")

        return 0

    except Exception as e:
        console.print(f"\n[bold red]❌ Errore durante l'analisi: {e}[/bold red]\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
