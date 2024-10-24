from transformers import pipeline

# Charger le pipeline de classification des sentiments avec un modèle multilingue
analyse_sentiments = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Texte en français à analyser
texte = " pierrepribetich gros mensonge   c est juste un amendement  qui ne change rien \u00e0 la suite   juste un coup d \u00e9p\u00e9e dans l eau  le gouvernement barnier fera passer la reforme et vous le savez  mentir  manipuler aussi   l oeuvre d une vie politique qu est l\u00e0 votre   "

# Analyser le sentiment
resultat = analyse_sentiments(texte)

# Afficher le résultat
print(resultat)