"""
Configurazione logging
"""

import logging
import os
from pathlib import Path
from rich.logging import RichHandler


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "logs/email_optimizer.log",
    use_rich: bool = True
) -> None:
    """
    Configura logging per l'applicazione

    Args:
        log_level: Livello di log (DEBUG, INFO, WARNING, ERROR)
        log_file: Path del file di log
        use_rich: Usa Rich per output colorato nel terminale
    """

    # Crea directory logs se non esiste
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configura logger root
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Rimuovi handler esistenti
    logger.handlers.clear()

    # Handler per file
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Handler per console
    if use_rich:
        console_handler = RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=False
        )
    else:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)

    console_handler.setLevel(getattr(logging, log_level.upper()))
    logger.addHandler(console_handler)

    logger.info("Logging configurato correttamente")
