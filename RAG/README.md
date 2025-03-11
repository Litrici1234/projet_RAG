# Agent Conversationnel Spécialisé avec RAG

##  Description du Projet
Ce projet implémente un agent conversationnel spécialisé basé sur la technique de **Retrieval-Augmented Generation (RAG)**. Il utilise un modèle de langage (LLM) open-source de **Hugging Face** et exploite des **articles scrapés** pour enrichir ses réponses.

L'architecture du projet repose sur trois étapes principales :
1. **Scraping des articles** : Extraction des articles via un script dédié.
2. **Traitement RAG** : Intégration des documents scrapés dans un pipeline RAG.
3. **Déploiement de l'agent** : Déploiement de l'agent conversationnel capable de répondre en s'appuyant sur les articles collectés.

---

##  Installation et Configuration
### 1️⃣ Cloner le projet
 lien :  https://github.com/Litrici1234/projet_RAG


### 2️⃣ Installer les dépendances
Utilisez un environnement virtuel (optionnel mais recommandé) :

Installez les bibliothèques requises :
```bash
pip install -r requirements.txt
```

### 3️⃣ Obtenir une clé API Hugging Face
Le modèle LLM utilisé provient de **Hugging Face**, nécessitant une clé API.
- Créez un compte sur Hugging Face
- Générez une **Access Token** dans votre profil.
- Ajoutez-la comme variable d'environnement
 
---

##  Exécution du Projet
### 1️⃣ Scraper les Articles
Lancez le notebook dédié au scraping : Scrap_articles.ipynb

Ce script stocke les articles scrapés dans le dossier **Data_articles/** sous forme pdf.
Data_articles est accessible via le lien : https://drive.google.com/drive/folders/168vCKBqkhAYq6QQxOWQRK-0xtRNWsB1v?usp=sharing
### 2️⃣ Construire l'Agent Conversationnel
Exécutez le fichier Python de construction de l'agent :
```bash
streamlit run Gen_AI.py
```
Cela charge les documents scrapés et entraîne le modèle RAG.

L’agent est maintenant accessible en local via une interface Streamlit.

---

## Structure du Projet
```
/
│── Data_articles/         # Articles scrapés
│── Gen AI data354.ipynb.ipynb  # Notebook de scraping
│── Gen_AI.py    # Construction de l'agent RAG
│── requirements.txt       # Bibliothèques nécessaires
│── README.md              # Documentation du projet
```

---



Pour toute question ou suggestion, vous pouvez me contacter sur LinkedIn : https://www.linkedin.com/in/litricia-momo-temfack-205aaa246/.

utilisez python3.11


