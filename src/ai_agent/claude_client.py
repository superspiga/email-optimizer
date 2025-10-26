"""
Client per interazione con Claude API
"""

import os
import logging
from typing import Optional, Dict, Any
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Client per Claude AI API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        temperature: float = 0.3
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY non configurata")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def analyze(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Analizza con Claude

        Args:
            prompt: Prompt utente
            system_prompt: System prompt (opzionale)

        Returns:
            Risposta di Claude
        """
        try:
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            kwargs: Dict[str, Any] = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.client.messages.create(**kwargs)

            # Estrai il testo dalla risposta
            if response.content and len(response.content) > 0:
                return response.content[0].text

            return ""

        except Exception as e:
            logger.error(f"Errore chiamata Claude API: {e}")
            raise

    def analyze_batch(
        self,
        prompts: list[str],
        system_prompt: Optional[str] = None
    ) -> list[str]:
        """
        Analizza multipli prompt (sequenziale)

        Args:
            prompts: Lista di prompt
            system_prompt: System prompt comune

        Returns:
            Lista di risposte
        """
        results = []
        for prompt in prompts:
            try:
                result = self.analyze(prompt, system_prompt)
                results.append(result)
            except Exception as e:
                logger.error(f"Errore batch analysis: {e}")
                results.append("")

        return results
