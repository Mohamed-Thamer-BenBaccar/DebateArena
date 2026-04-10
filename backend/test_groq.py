# backend/test_groq.py
import os
import time
from groq import Groq
from dotenv import load_dotenv
# Charger les variables du fichier .env
load_dotenv()
# Créer le client Groq avec la clé API
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
print('Envoi de la requête à Groq...')
debut = time.time()
# Premier appel simple
response = client.chat.completions.create(
model='llama-3.3-70b-versatile', # nom exact du modèle
messages=[
{'role': 'user', 'content': 'Dis bonjour en une phrase courte'}
],
max_tokens=50 # limiter pour ce test
)
fin = time.time()
latence = round((fin - debut) * 1000) # en millisecondes
print(f'Réponse : {response.choices[0].message.content}')
print(f'Latence : {latence}ms')
print(f'Modèle : {response.model}')
print(f'Tokens : {response.usage.total_tokens}')