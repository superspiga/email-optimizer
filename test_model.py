#!/usr/bin/env python3
"""
Test per verificare quale modello Claude funziona
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ANTHROPIC_API_KEY non trovata nel .env")
    exit(1)

client = Anthropic(api_key=api_key)

# Lista modelli da testare
models_to_test = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

print("🧪 Test modelli Claude disponibili...\n")

for model in models_to_test:
    try:
        print(f"Provo {model}...", end=" ")
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print("✅ FUNZIONA!")
        print(f"   Risposta: {response.content[0].text}")
        print(f"\n🎯 USA QUESTO MODELLO: {model}\n")
        break
    except Exception as e:
        if "404" in str(e):
            print("❌ Non trovato (404)")
        elif "401" in str(e):
            print("❌ API Key non valida (401)")
        elif "429" in str(e):
            print("⚠️  Rate limit (429)")
        else:
            print(f"❌ Errore: {str(e)[:50]}")

print("\n📝 Aggiorna il file .env con il modello che funziona:")
print("   AI_MODEL=<nome-modello-funzionante>")
