
# 🐦 Analyse de Sentiments Twitter/X - INFO0909 - Système Multi-Agents

🤖 Ce projet implémente un système multi-agents pour l'analyse de sentiments de tweets en français, en utilisant [SPADE](https://pypi.org/project/spade/) 🌟<br>
📚 Il a été développé dans le cadre de l'unité d'enseignement INFO0909 - Systèmes Multi-Agents 🎓<br>
👥 Les auteurs sont :
- [Alexandre COLLIGNON](https://github.com/Stoupy51)
- [Axelle GARRAT](https://github.com/akselZ)


## 🏗️ Architecture
Le système est composé de 5 agents qui communiquent entre eux :

1. **CrawlerAgent**: 🔍 Collecte les tweets via l'API Twitter (twscrape), puis les envoie au **CleanerAgent** si les tweets ne sont pas déjà dans la base de données.
2. **CleanerAgent**: 🧹 Nettoie et prétraite les tweets selon les options choisies, puis l'envoie au **LabellerAgent**
3. **LabellerAgent**: 🤔 Analyse le sentiment des tweets via un modèle LLM (Llama), puis l'envoie au **DatabaseAgent**
4. **DatabaseAgent**: 💾 Stocke les résultats dans une base de données JSON. Si aucun tweet n'a été reçu en 10 secondes, l'agent **SVMAgent** est notifié.
5. **SVMAgent**: 📊 Entraine un SVM sur les tweets analysés et les labels associés. Puis affiche l'accuracy du modèle.


## ⚙️ Configuration
La configuration du système se fait via le fichier `config.py` qui contient plusieurs classes de configuration :

- `CrawlerConfig`: 🔍 Configuration de la collecte des tweets `(compte Twitter, nombre max de tweets, requête de recherche)`
- `CleanerConfig`: 🧹 Options de nettoyage des textes `(suppression des liens, caractères spéciaux, accents, mise en minuscule, stopwords)`
- `LabellerConfig`: 🎯 Configuration du modèle d'analyse de sentiments `(labels, URL de l'API, modèle, prompt)`
- `SVMConfig`: 📈 Paramètres pour la classification SVM `(nombre max de features, type de kernel, taille du test set, random state)`
- `DatabaseConfig`: 💽 Configuration de la base de données `(création d'une nouvelle base au démarrage, fichier)`
- `Agents`: 🔑 Identifiants et mots de passe des agents SPADE `(crawler, cleaner, database, labeller, svm)`


## 📋 Prérequis
- Python 3.8 ou plus 🐍
- Ollama (pour le modèle LLM) 🦙

## 🚀 Installation

1. 📥 Cloner le repository (`git clone https://github.com/Stoupy51/INFO0909_SMA` par exemple)
2. 📦 Installer les dépendances (`pip install -r requirements.txt`, ou juste `python main.py` qui installera les dépendances manquantes)
