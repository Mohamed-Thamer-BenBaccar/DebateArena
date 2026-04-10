from parser import detect_and_extract, summarize_course

with open("mon_cours.pdf", "rb") as f:
    data = f.read()

print("\n=== TEXTE EXTRAIT ===\n")

text = detect_and_extract(data, "application/pdf")
print(text[:500])

print("\n=== RÉSUMÉ IA ===\n")

summary = summarize_course(text)
print(summary)