from parser import detect_and_extract, summarize_course

# ======================
# LOAD FILE
# ======================
with open("mon_cours.pdf", "rb") as f:
    file_bytes = f.read()

# ======================
# EXTRACT TEXT
# ======================
text = detect_and_extract(file_bytes, "application/pdf")

print("\n=== TEXTE EXTRAIT ===\n")
print(text[:500])

# ======================
# AI SUMMARY
# ======================
summary = summarize_course(text)

print("\n=== RÉSUMÉ IA ===\n")
print(summary)