## DATA354_Chatbot

Ce dépôt contient une application Streamlit qui implémente la génération augmentée par récupération (RAG) en utilisant l'API Gemini Pro.

### Gemini Pro RAG App

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/your-username/gemini-pro-rag-app.git
    cd gemini-pro-rag-app
    ```

2. Installez les dépendances requises :
    ```bash
    pip install -r requirements.txt
    ```

3. Configurez les variables d'environnement :
    - Créez un fichier `.env` à la racine du projet et ajoutez votre clé API Google :
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```


## Application Structure



  # `scraping.py`

Ce script Python est conçu pour extraire des articles à partir du site Web de l'Agence Ecofin en utilisant le web scraping. Il récupère les liens des articles à partir de deux pages de résultats de recherche (les 12 articles les plus récents), puis extrait les titres et les paragraphes de chaque article. Les données extraites sont ensuite enregistrées dans un fichier JSON.

### Fonctionnalités

- **Récupération des liens d'articles** : 
  - Utilise BeautifulSoup pour analyser les pages web et extraire les liens des articles à partir des balises `<h3>` avec la classe `"r"`.

- **Extraction du contenu des articles** :
  - Pour chaque lien d'article récupéré, le script télécharge le contenu de la page et en extrait le titre (balise `<h1>` avec la classe `"itemTitle"`) et les paragraphes (balises `<p>` avec la classe `"texte textearticle"`).

- **Enregistrement des données** :
  - Les informations extraites (titre, paragraphes, et lien de l'article) sont stockées dans un fichier JSON nommé `articles.json`.

### Structure du Code

- **`base_url`** : URL de base du site web de l'Agence Ecofin.
- **`page_1_url` et `page_2_url`** : URLs des pages contenant les articles à extraire.
- **`obtenir_liens_articles(page_url)`** : Fonction pour récupérer les liens des articles à partir d'une page donnée.
- **`obtenir_contenu_article(lien)`** : Fonction pour extraire le titre et les paragraphes d'un article en utilisant son lien.
- **`data`** : Liste pour stocker les données des articles extraits.
- **Enregistrement des données** : Les données extraites sont enregistrées dans un fichier `articles.json`.







## `rag.py`

Ce script est une application Streamlit qui utilise la technologie RAG (Retrieval-Augmented Generation) pour répondre aux questions sur les articles extraits du site de l'Agence Ecofin. Il intègre le modèle Gemini Pro de LangChain pour fournir des réponses détaillées basées sur un contexte préchargé ou des réponses générales pour des questions fréquentes.

### Fonctionnalités

- **Chargement des Variables d'Environnement** :
  - Utilise `dotenv` pour charger les variables d'environnement, telles que la clé API de Google.

- **Chargement et Traitement du Texte** :
  - La fonction `load_text_from_json(json_path)` lit un fichier JSON contenant les articles et extrait le texte à partir des titres et des paragraphes des articles.
  
- **Initialisation de l'Index Vectoriel** :
  - La fonction `initialize_vector_index(text)` crée un index vectoriel à partir du texte extrait en utilisant des embeddings de Google Generative AI et le stockage vectoriel Chroma.

- **Génération de Réponses** :
  - La fonction `get_response(question)` répond aux questions des utilisateurs en utilisant le modèle Gemini Pro. Elle vérifie d'abord si la question est une question générale prédéfinie avant de récupérer les documents pertinents pour générer une réponse basée sur le contexte.

- **Interface Utilisateur** :
  - L'application Streamlit offre une interface pour poser des questions sur les articles. Elle gère l'historique des conversations et affiche les réponses du bot.

### Structure du Code

- **`load_text_from_json(json_path)`** :
  - Fonction pour lire un fichier JSON et extraire le texte des articles.

- **`initialize_vector_index(text)`** :
  - Fonction pour initialiser un index vectoriel à partir du texte extrait en utilisant des embeddings et Chroma.

- **`get_response(question)`** :
  - Fonction pour obtenir une réponse à une question en utilisant le modèle Gemini Pro. La fonction vérifie d'abord les réponses générales avant d'interroger le modèle sur le contexte fourni.

- **Streamlit Configuration** :
  - Configure l'application Streamlit avec un titre de page, une icône, et un état initial de la barre latérale. Gère également l'historique des chats et le nettoyage de l'historique via l'interface utilisateur.




### Instructions d'Utilisation

1. **Exécuter le script** :








- **`.env`**:
  - Environment variables file.
  - **Note**: Ce fichier n'est pas inclus dans le dépôt et doit être créé par l'utilisateur.
  - Ajoutez votre clé API Google dans ce fichier:
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```
















    

## Usage
Lancer d'abord le fichier scraping.py afin de générer le fichier "articles.json" 
.Pour exécuter l'application, utilisez la commande suivante:
```bash
streamlit run rag.py
