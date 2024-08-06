import requests
from bs4 import BeautifulSoup
import json

# URL de base
base_url = "https://www.agenceecofin.com"

# URLs des pages
page_1_url = "https://www.agenceecofin.com/a-la-une/recherche-article?filterTitle=&submit.x=0&submit.y=0&filterTousLesFils=Tous&filterCategories=Sous-rubrique&filterLDateFrom=&filterDateTo=&option=com_dmk2articlesfilter&view=articles&filterFrench=French&Itemid=269&userSearch=1&layout=#dmk2articlesfilter_results"
page_2_url = base_url + "/a-la-une/recherche-article/articles?submit_x=0&submit_y=0&filterTousLesFils=Tous&filterCategories=Sous-rubrique&filterFrench=French&userSearch=1&testlimitstart=7"

# Fonction pour récupérer les liens des articles d'une page donnée
def obtenir_liens_articles(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    h3_tags = soup.find_all('h3', class_='r')
    return [base_url + h3.find('a')['href'] for h3 in h3_tags if h3.find('a') and h3.find('a').get('href')]

# Fonction pour extraire le contenu d'un article
def obtenir_contenu_article(lien):
    response = requests.get(lien)
    page_soup = BeautifulSoup(response.content, 'html.parser')
    
    h1_tag = page_soup.find('h1', class_='itemTitle')
    titre = h1_tag.text.strip() if h1_tag else 'No title'
    
    p_tags = page_soup.find_all('p', class_='texte textearticle')
    paragraphes = [p.text.strip() for p in p_tags]

    return {
        'titre': titre,
        'paragraphes': paragraphes,
        'lien': lien
    }

# Liste pour stocker les données des articles
data = []

# Récupérer les liens des articles des deux pages
liens_articles = obtenir_liens_articles(page_1_url) + obtenir_liens_articles(page_2_url)

# Extraire le contenu des articles et les ajouter à la liste des données
for lien in liens_articles:
    data.append(obtenir_contenu_article(lien))

# Enregistrer les données dans un fichier JSON
with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Les données ont été enregistrées dans 'articles.json'.")
