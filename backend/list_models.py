import os
from dotenv import load_dotenv
from groq import Groq

# Charger le fichier .env
load_dotenv('.env')

# Initialiser Groq
api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=api_key)

print("📋 Modèles disponibles chez Groq :\n")

try:
    models = client.models.list()
    for model in models.data:
        print(f"✅ {model.id}")
except Exception as e:
    print(f"❌ Erreur : {e}")