"""
Test debate modes with YOUR physics course
Run: python backend/test_with_course.py
"""

# ✅ AJOUTE CES LIGNES AU DÉBUT
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Maintenant l'import marche
from debate import get_ai_response

# ===== TON COURS DE PHYSIQUE =====
# REMPLACE CE TEXTE PAR TON COURS RÉEL
PHYSICS_COURSE = """
La mécanique classique est l'étude du mouvement des objets sous l'influence des forces.

**Les trois lois de Newton:**
1. Première loi (inertie): Un objet au repos reste au repos, un objet en mouvement reste en mouvement sauf si une force externe agit
2. Deuxième loi: F = ma (Force = masse × accélération)
3. Troisième loi: À chaque action correspond une réaction égale et opposée

**Le travail et l'énergie:**
- Travail (W) = Force × Distance × cos(angle)
- Énergie cinétique = 1/2 × m × v²
- Énergie potentielle = m × g × h

**Conservation de l'énergie:**
L'énergie totale d'un système isolé reste constante. Elle se transforme entre formes potentielle et cinétique.
"""

def test_mode(mode_name, student_answer):
    """
    Test one mode with a student answer
    
    Args:
        mode_name: "socrate", "contradicteur", or "jury"
        student_answer: What the student said
    """
    print(f"\n{'='*70}")
    print(f"TEST: Mode {mode_name.upper()}")
    print(f"{'='*70}")
    print(f"📚 Cours: {PHYSICS_COURSE[:100]}...")
    print(f"👨‍🎓 Étudiant dit: {student_answer}")
    print(f"\n🤖 Réponse IA:\n")
    
    # Get response (streaming)
    full_response = ""
    for token in get_ai_response(PHYSICS_COURSE, mode_name, [], student_answer):
        print(token, end="", flush=True)
        full_response += token
    
    print(f"\n\n✅ Réponse reçue ({len(full_response)} caractères)")
    return full_response

def main():
    """Run all tests"""
    
    print("🧪 TEST DES 3 MODES AVEC TON COURS DE PHYSIQUE\n")
    
    # Test 1: Socrate mode
    print("TEST 1/3: MODE SOCRATE")
    response1 = test_mode(
        "socrate",
        "Je pense que la force est la même chose que l'énergie"
    )
    
    input("\n⏸️  Appuie sur Entrée pour continuer...")
    
    # Test 2: Contradicteur mode
    print("\n\nTEST 2/3: MODE CONTRADICTEUR")
    response2 = test_mode(
        "contradicteur",
        "D'après Newton, si je pousse une table, la table me pousse pas"
    )
    
    input("\n⏸️  Appuie sur Entrée pour continuer...")
    
    # Test 3: Jury mode
    print("\n\nTEST 3/3: MODE JURY")
    response3 = test_mode(
        "jury",
        "L'énergie cinétique d'une voiture qui roule à 100 km/h c'est m×g×h"
    )
    
    # Summary
    print("\n" + "="*70)
    print("✅ TOUS LES TESTS COMPLÉTÉS!")
    print("="*70)
    print(f"✓ Mode Socrate: {len(response1)} caractères")
    print(f"✓ Mode Contradicteur: {len(response2)} caractères")
    print(f"✓ Mode Jury: {len(response3)} caractères")
    print("\n🎉 Le backend fonctionne!")

if __name__ == "__main__":
    main()