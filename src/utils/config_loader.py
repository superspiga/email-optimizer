"""
Caricamento configurazione
"""

import os
import json
import logging
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv

from ..models import EmailAccount

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Caricatore configurazione da environment e file"""

    def __init__(self, env_file: str = ".env"):
        # Carica variabili d'ambiente
        load_dotenv(env_file)

        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.ai_model = os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.3"))

        self.max_emails_per_run = int(os.getenv("MAX_EMAILS_PER_RUN", "50"))
        self.days_to_analyze = int(os.getenv("DAYS_TO_ANALYZE", "7"))

        self.use_cache = os.getenv("USE_CACHE", "true").lower() == "true"
        self.cache_expiry_hours = int(os.getenv("CACHE_EXPIRY_HOURS", "24"))

        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/email_optimizer.log")

    def load_email_accounts(self) -> List[EmailAccount]:
        """
        Carica configurazione account email

        Returns:
            Lista di EmailAccount
        """
        accounts_json = os.getenv("EMAIL_ACCOUNTS", "[]")

        try:
            accounts_data = json.loads(accounts_json)
            accounts = []

            for acc_data in accounts_data:
                account = EmailAccount(
                    name=acc_data["name"],
                    type=acc_data["type"],
                    email=acc_data["email"],
                    host=acc_data.get("host"),
                    port=acc_data.get("port"),
                    password=acc_data.get("password"),
                    credentials_file=acc_data.get("credentials_file"),
                    use_ssl=acc_data.get("use_ssl", True)
                )
                accounts.append(account)

            logger.info(f"Caricati {len(accounts)} account email")
            return accounts

        except Exception as e:
            logger.error(f"Errore caricamento account: {e}")
            return []

    def load_sender_categories(self) -> dict:
        """
        Carica configurazione categorie mittenti

        Returns:
            Dictionary con configurazione categorie
        """
        config_path = Path("config/sender_categories.json")

        if not config_path.exists():
            logger.warning("File categorie mittenti non trovato")
            return {}

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Errore caricamento categorie: {e}")
            return {}

    def validate_config(self) -> bool:
        """
        Valida configurazione

        Returns:
            True se configurazione valida
        """
        if not self.anthropic_api_key:
            logger.error("ANTHROPIC_API_KEY non configurata")
            return False

        accounts = self.load_email_accounts()
        if not accounts:
            logger.error("Nessun account email configurato")
            return False

        return True
