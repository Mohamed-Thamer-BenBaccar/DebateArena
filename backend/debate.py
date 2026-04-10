# backend/debate.py
# Ce fichier contient toute la logique IA de DebateArena
import os
from groq import Groq
from dotenv import load_dotenv
# Charger les variables d'environnement depuis .env
load_dotenv()
# Créer le client Groq UNE SEULE FOIS (pas à chaque appel)
# C'est plus efficace que de le recréer à chaque message
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
# Dictionnaire qui contiendra les 3 prompts système
# Chaque prompt sera ajouté dans les étapes suivantes
PROMPTS = {
    "contradicteur": "Tu es un contradicteur. Voici le cours : {content}",
    "socrate": "Tu es Socrate. Voici le cours : {content}",
    "jury": "Tu es le jury. Voici le cours : {content}"
}

# Ajouter dans debate.py, après les PROMPTS :
def get_ai_response(content, mode, history, message):
    '''
    Appelle Groq et yield les tokens un par un (streaming).
    Paramètres :
    - content : str — résumé du cours (fourni par M3 via M1)
    - mode : str — 'contradicteur', 'socrate' ou 'jury'
    - history : list — historique [{role:'user'|'assistant', content:'...'}]
    - message : str — le nouveau message de l'étudiant
    Retourne : generator qui yield des strings (tokens)
    '''
    # ÉTAPE 1 : Sélectionner le bon prompt et injecter le contenu du cours
    if mode not in PROMPTS:
        mode = 'contradicteur' # mode par défaut si mode inconnu
    system_prompt = PROMPTS[mode].format(content=content[:3000])
    # content[:3000] : on limite à 3000 caractères pour rester
    # dans la limite de tokens et garder des réponses rapides
    # ÉTAPE 2 : Construire la liste de messages complète
    # Groq a besoin de : [system] + [historique] + [nouveau message]
    messages = []
    messages.append({'role': 'system', 'content': system_prompt})
    # Ajouter l'historique de la conversation (pour la mémoire du débat)
    messages.extend(history) # history est déjà au bon format
    # Ajouter le nouveau message de l'étudiant
    messages.append({'role': 'user', 'content': message})
    # ÉTAPE 3 : Appeler Groq avec stream=True
    stream = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=messages,
        stream=True, # activer le streaming
        max_tokens=300, # max 300 tokens » 200-220 mots
        temperature=0.7, # 0=déterministe, 1=créatif. 0.7 = bon équilibre
    )
    # ÉTAPE 4 : Yield chaque token reçu
    for chunk in stream:
        # chunk.choices[0].delta.content : le token (peut être None en début/fin)
        token = chunk.choices[0].delta.content
        if token is not None: # ignorer les chunks None (début et fin de stream)
            yield token # envoyer le token au appelant (M1/FastAPI)
# --- TEST STANDALONE ---
if __name__ == '__main__':
    print('Test streaming get_ai_response...')
    
cours = 'Newton : F=ma, inertie, action-réaction'
print('Réponse (token par token) :')
for token in get_ai_response(
content=cours,
mode='contradicteur',
history=[],
message='La force est proportionnelle à la masse'
):
    print(token, end='', flush=True) # flush=True pour voir immédiatement
print() # nouvelle ligne à la fin

# Ajouter dans debate.py, après PROMPTS = {} :
PROMPTS['contradicteur'] = '''Tu es un adversaire intellectuel rigoureux.
Le cours sur lequel tu vas débattre est le suivant :
---
{content}
---
Tes règles ABSOLUES que tu ne peux JAMAIS enfreindre :
RÈGLE 1 : Tu CONTREDIS toujours l'affirmation de l'étudiant, même si elle est correcte.
Si l'étudiant a raison, tu trouves une nuance, une limite, une exception.
RÈGLE 2 : Tu cherches les IMPRÉCISIONS, les GÉNÉRALISATIONS abusives, les RACCOURCIS.
Exemple : 'toujours' ou 'jamais' sont presque toujours faux.
RÈGLE 3 : Tu ne donnes JAMAIS la réponse correcte directement.
Tu forces l'étudiant à réfléchir par lui-même.
RÈGLE 4 : Tu termines TOUJOURS par exactement UNE seule question.
Jamais deux questions. Jamais zéro question.
RÈGLE 5 : Tu restes STRICTEMENT dans le contexte du cours fourni entre ---.
Si l'étudiant sort du sujet, tu le ramènes poliment vers le cours.
RÈGLE 6 : Longueur de réponse : 2 à 4 phrases + 1 question. Jamais plus long.
'''
# --- TEST IMMÉDIAT ---
# Ajouter ce code TEMPORAIREMENT sous le prompt pour tester :
if __name__ == '__main__':
    cours_test = 'Les lois de Newton : 1) Inertie 2) F=ma 3) Action-réaction'
    system = PROMPTS['contradicteur'].format(content=cours_test)
    r = client.chat.completions.create(
    model='llama-3.3-70b-versatile',
    messages=[
    {'role': 'system', 'content': system},
    {'role': 'user', 'content': 'La force est égale à la masse fois l accélération'}
    ],
    max_tokens=200
    )
    print('=== TEST CONTRADICTEUR ===')
    print(r.choices[0].message.content)

# Test rapide au lancement
if __name__ == '__main__':
    print('debate.py chargé avec succès')
print(f'Client Groq prêt : {client is not None}')

PROMPTS['socrate'] = '''Tu es Socrate, le philosophe grec de l'Antiquité.
Le cours sur lequel porte le dialogue est :
---
{content}
---
Ta méthode — la maïeutique — consiste à faire accoucher l'étudiant de la vérité
par des questions, jamais en lui donnant la réponse.
Tes règles ABSOLUES :
RÈGLE 1 : Tu réponds UNIQUEMENT par une question. Jamais une affirmation.
Si tu te surprends à affirmer quelque chose, reformule en question.
RÈGLE 2 : Tu n utilises JAMAIS les mots : 'Exact', 'Correct', 'Bravo', 'Bien',
'Tout à fait', 'Effectivement', 'En effet'. Ces mots sont interdits.
RÈGLE 3 : Tu ne confirmes JAMAIS si une réponse est correcte ou incorrecte.
Tu continues toujours à questionner.
RÈGLE 4 : Si l'étudiant dit 'je ne sais pas' ou est bloqué depuis 2 échanges,
tu reformules ta question différemment ou tu poses une question plus simple.
RÈGLE 5 : Longueur : 1 à 2 phrases maximum. Toujours une question.
RÈGLE 6 : Tu restes dans le contexte du cours fourni.
'''
# Test Socrate :
if __name__ == '__main__':
    cours_test = 'Les lois de Newton...'
    system = PROMPTS['socrate'].format(content=cours_test)
    # Test 1 : réponse correcte
    msgs = [{'role':'system','content':system},
    {'role':'user','content':'Newton a défini 3 lois du mouvement'}]
    r = client.chat.completions.create(model='llama-3.3-70b-versatile',
    messages=msgs, max_tokens=100)
    print('=== SOCRATE — Réponse correcte ===')
    print(r.choices[0].message.content)
    # Test 2 : je ne sais pas
    msgs.append({'role':'assistant','content': r.choices[0].message.content})
    msgs.append({'role':'user','content':'je ne sais pas'})
    r2 = client.chat.completions.create(model='llama-3.3-70b-versatile',
    messages=msgs, max_tokens=100)
    print('=== SOCRATE — Je ne sais pas ===')
    print(r2.choices[0].message.content)

PROMPTS['jury'] = '''Tu es un jury d'examen universitaire strict, juste et précis.
Le cours évalué est :
---
{content}
---
Pour CHAQUE réponse de l'étudiant, tu dois TOUJOURS :
FORMAT OBLIGATOIRE — respecter exactement cet ordre :
Ligne 1 : [NOTE: X/10] ¬ X est un entier entre 0 et 10
Ligne 2 : Une seule phrase de justification de la note.
Ligne 3 : (ligne vide)
Ligne 4 : Question suivante : [ta question tirée du cours]
Barème précis :
10/10 = Réponse parfaite, complète, sans aucune imprécision.
8/10 = Bonne réponse avec une légère omission ou imprécision.
6/10 = Réponse partiellement correcte, éléments importants manquants.
4/10 = Quelques éléments corrects mais incompréhension globale.
2/10 = Presque tout faux, une seule idée correcte.
0/10 = Réponse complètement fausse ou hors sujet.
RÈGLE ABSOLUE : Commence TOUJOURS par [NOTE: X/10] sur la première ligne.
Ne commence JAMAIS par autre chose.
'''
# Test Jury :
if __name__ == '__main__':
    cours_test = 'Newton : F=ma, inertie, action-réaction'
    system = PROMPTS['jury'].format(content=cours_test)
    for reponse, attendu in [
    ('F=ma signifie que la force est le produit de la masse et de l accélération', '8-10'),
    ('Newton a fait des trucs avec des pommes', '1-3'),
    ]:
        r = client.chat.completions.create(model='llama-3.3-70b-versatile',
    messages=[{'role':'system','content':system},
    {'role':'user','content':reponse}], max_tokens=200)
    rep = r.choices[0].message.content
    print(f'=== Réponse : {reponse[:40]}... ===')
    print(rep)
    print(f'(Attendu : {attendu}/10)')
    print()

cours = 'Newton : F=ma, inertie, action-réaction'
history = [] # historique vide au début
# Tour 1
msg1 = 'La force est le produit de la masse et de l accélération'
print(f'Étudiant : {msg1}')
rep1 = ''
for token in get_ai_response(cours, 'contradicteur', history, msg1):
    rep1 += token
print(token, end='', flush=True)
print()
# Ajouter les 2 messages à l'historique pour le tour suivant
history.append({'role': 'user', 'content': msg1})
history.append({'role': 'assistant', 'content': rep1})
# Tour 2 — l'IA doit se souvenir du tour 1
msg2 = 'Mais l accélération peut être négative non ?'
print(f'Étudiant : {msg2}')
for token in get_ai_response(cours, 'contradicteur', history, msg2):
    print(token, end='', flush=True)
print()