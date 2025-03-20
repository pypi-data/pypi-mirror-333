# main.py
import argparse
from aganitha.pubmed import search_pubmed, fetch_article_details, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Search PubMed and fetch articles with pharma/biotech authors.")
    
    # Add the argument for the query and other options
    parser.add_argument('query', type=str, help="Search query for PubMed")
    parser.add_argument('-d', '--debug', action='store_true', help="Print debug information")
    parser.add_argument('-f', '--for-file', type=str, help="Specify the filename to save the results")
    
    args = parser.parse_args()

    # Step 1: Search PubMed for the query
    pmids = search_pubmed(args.query, debug=args.debug)
    
    if pmids:
        # Step 2: Fetch article details for the found PMIDs
        articles = fetch_article_details(pmids, debug=args.debug)
        
        if articles:
            # Step 3: Save the results to a CSV file or print them
            if args.for_file:
                save_to_csv(articles, filename=args.for_file)
            else:
                print(f"Found {len(articles)} relevant articles:")
                for article in articles:
                    print(article)
        else:
            print("No articles found with non-academic affiliations or pharma/biotech companies.")
    else:
        print("No results found for your query.")

if __name__ == "__main__":
    main()
