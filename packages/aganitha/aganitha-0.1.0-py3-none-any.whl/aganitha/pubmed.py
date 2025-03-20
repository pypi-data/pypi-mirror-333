
import requests
import xml.etree.ElementTree as ET
import csv

# Define a list of pharmaceutical/biotech keywords
pharma_keywords = ['pharmaceutical', 'biotech', 'biotechnology', 'pharma', 'biopharma', 'biomedical']

# Function to search PubMed and fetch results
def search_pubmed(query, debug=False):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'xml',
    }
    
    if debug:
        print(f"Searching PubMed with query: {query}")
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        pmids = [id.text for id in root.findall('.//Id')]
        if debug:
            print(f"Found {len(pmids)} articles")
        if not pmids:
            print("No results found.")
            return []
        return pmids
    else:
        print(f"Error fetching data from PubMed. Status code: {response.status_code}")
        return []

# Function to fetch article details using PMIDs
def fetch_article_details(pmids, debug=False):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': ','.join(pmids),
        'retmode': 'xml',
    }
    
    if debug:
        print(f"Fetching details for PMIDs: {pmids}")
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        articles = []
        for article in root.findall('.//PubmedArticle'):
            pubmed_id = article.find('.//PubmedData/ArticleIdList/ArticleId').text
            title = article.find('.//ArticleTitle').text
            pub_date = article.find('.//PubDate/Year').text if article.find('.//PubDate/Year') is not None else 'N/A'
            authors = article.findall('.//Author')
            
            non_academic_authors = []
            company_affiliations = []
            corresponding_author_email = ''
            
            for author in authors:
                last_name = author.find('.//LastName').text if author.find('.//LastName') is not None else ''
                fore_name = author.find('.//ForeName').text if author.find('.//ForeName') is not None else ''
                affiliation = author.find('.//Affiliation')
                
                if affiliation is not None:
                    affiliation_text = affiliation.text.lower()
                    if any(keyword in affiliation_text for keyword in pharma_keywords):
                        company_affiliations.append(affiliation.text)
                    else:
                        non_academic_authors.append(f"{fore_name} {last_name}")
                
                # Get email of corresponding author (if available)
                if author.find('.//Email') is not None:
                    corresponding_author_email = author.find('.//Email').text

            if non_academic_authors or company_affiliations:
                articles.append({
                    'PubmedID': pubmed_id,
                    'Title': title,
                    'Publication Date': pub_date,
                    'Non-academic Author(s)': ', '.join(non_academic_authors),
                    'Company Affiliation(s)': ', '.join(company_affiliations),
                    'Corresponding Author Email': corresponding_author_email,
                })
        return articles
    else:
        print(f"Error fetching article details. Status code: {response.status_code}")
        return []

# Function to save the results in a CSV file
def save_to_csv(articles, filename="pubmed_results.csv"):
    fieldnames = ['PubmedID', 'Title', 'Publication Date', 'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
    print(f"Results saved to {filename}")
