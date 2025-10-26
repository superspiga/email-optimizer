#!/usr/bin/env python3
"""Test semplice modello Claude"""

import sys
import os

# Aggiungi il path corrente
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dotenv import load_dotenv
    from anthropic import Anthropic
except ImportError as e:
    print(f"❌ Errore import: {e}")
    print("\n💡 Soluzione: Attiva l'ambiente virtuale:")
    print("   source venv/bin/activate  # Mac/Linux")
    print("   venv\\Scripts\\activate     # Windows")
    sys.exit(1)

# Carica .env
load_dotenv()

# Verifica API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ANTHROPIC_API_KEY non trovata")
    print("\n💡 Verifica il file .env")
    sys.exit(1)

print(f"✅ API Key trovata: {api_key[:20]}...")

# Test modelli
modelli = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

client = Anthropic(api_key=api_key)

print("\n🧪 Test modelli...\n")

funzionante = None

for modello in modelli:
    try:
        print(f"Provo {modello}... ", end="", flush=True)

        response = client.messages.create(
            model=modello,
            max_tokens=10,
            messages=[{"role": "user", "content": "ciao"}]
        )

        print("✅ FUNZIONA!")
        funzionante = modello
        break

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print("❌ 404 (non disponibile)")
        elif "401" in error_msg:
            print("❌ 401 (API key invalida)")
            print("\n⚠️  Verifica la tua API key su https://console.anthropic.com/")
            sys.exit(1)
        elif "403" in error_msg:
            print("❌ 403 (accesso negato)")
        else:
            print(f"❌ Errore: {error_msg[:60]}")

if funzionante:
    print(f"\n🎯 MODELLO DA USARE: {funzionante}")
    print(f"\n📝 Modifica il file .env:")
    print(f"   AI_MODEL={funzionante}")
    print("\n✅ Poi rilancia: python main.py")
else:
    print("\n❌ Nessun modello funziona!")
    print("\n🔍 Possibili cause:")
    print("   1. Account Anthropic senza billing configurato")
    print("   2. API key senza accesso ai modelli")
    print("   3. Crediti esauriti")
    print("\n💡 Verifica: https://console.anthropic.com/settings/billing")
