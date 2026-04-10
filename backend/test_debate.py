import groq
import os
from debate import PROMPTS # Importation cruciale

# Remplacez par votre vraie clé ou assurez-vous qu'elle est en variable d'environnement
client = groq.Groq(api_key="GROQ_API_KEY")

def test_contradicteur():
    cours_exemple = "Le cycle de Krebs se déroule dans la mitochondrie et produit de l'ATP."
    user_input = "Le cycle de Krebs sert uniquement à fabriquer de l'énergie immédiatement."
    
    # Préparation du prompt
    system_prompt = PROMPTS['contradicteur'].format(content=cours_exemple)
    
    completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile", # <--- Nouveau modèle à jour
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    )
    
    print("\n--- RÉPONSE DU CONTRADICTEUR ---")
    print(completion.choices[0].message.content)
    print("--------------------------------\n")

if __name__ == "__main__":
    test_contradicteur()