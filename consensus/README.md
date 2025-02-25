
# 🤖 Système de Consensus - INFO0909 - Systèmes Multi-Agents

🔍 Ce projet implémente un système multi-agents pour la détection de textes générés par IA en utilisant des mécanismes de consensus, construit avec [AutoGen](https://pypi.org/project/autogen-core/) 🌟<br>
📚 Il a été développé dans le cadre de l'unité d'enseignement INFO0909 - Systèmes Multi-Agents 🎓<br>
👥 Les auteurs sont :
- [Alexandre COLLIGNON](https://github.com/Stoupy51)
- [Axelle GARRAT](https://github.com/akselZ)

## 📋 Prérequis
- Python 3.12 ou plus 🐍
- [Ollama (pour le modèle LLM)](https://ollama.com/) 🦙

## 🚀 Installation & Démarrage

1. 📥 Cloner le repository
2. 📦 Installer les dépendances (`pip install -r requirements.txt`: optionnel, le main.py installera les dépendances manquantes)
3. 🚀 Démarrer le système avec `python main.py`

## 🏗️ Architecture
Le système est composé de plusieurs agents qui communiquent pour atteindre un consensus sur la nature d'un texte (généré par IA ou non) :

1. **PresidentAgent**: 🎯 Coordonne les votes et agrège les résultats en utilisant différents mécanismes de consensus
2. **BERT Agent**: 🧠 Utilise le modèle BERT pour la classification
3. **Ollama Agent**: 🦙 Utilise le modèle LLaMA via Ollama pour les prédictions
4. **Random Agent**: 🎲 Fait des prédictions aléatoires comme référence

## 🗳️ Mécanismes de Consensus

Le système implémente trois méthodes de vote :

1. **Vote Majoritaire**: Décision basée sur la majorité simple des votes des agents
2. **Vote de Borda**: Vote basé sur les préférences où les agents classent leurs prédictions
3. **PAXOS**: Protocole de consensus distribué

## ⚙️ Configuration
La configuration du système se fait via le fichier `config.py` qui contient plusieurs composants clés :

- Chemins et configurations des modèles
- Emplacement et paramètres du dataset
- Paramètres de communication des agents
- Paramètres des mécanismes de vote

## 📊 Dataset
Le projet utilise le dataset [AI Vs Human Text](https://www.kaggle.com/datasets/shanegerami/ai-vs-human-text) (5% des données car 487235 lignes est trop grand) de Kaggle pour l'entraînement et l'évaluation.

