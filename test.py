import scholarly
import requests

# Search Google Scholar and refine results using CrossRef API
def search_papers_combined(query, num_results=5):
    # Step 1: Search Google Scholar
    search_query = scholarly.search_pubs(query)

    for i in range(num_results):
        try:
            pub = next(search_query)
            title = pub.get('bib', {}).get('title', None)
            
            if title:
                # Step 2: Search CrossRef by title
                crossref_url = "https://api.crossref.org/works"
                params = {
                    "query.bibliographic": title,
                    "rows": 1,
                }
                response = requests.get(crossref_url, params=params)
                
                if response.status_code == 200:
                    crossref_data = response.json()
                    if crossref_data['message']['items']:
                        item = crossref_data['message']['items'][0]
                        doi = item.get('DOI', 'No DOI available')
                        crossref_title = item.get('title', ["No title available"])[0]
                        url = f"https://doi.org/{doi}"

                        print(f"Title: {crossref_title}\nDOI: {doi}\nLink: {url}\n")

                else:
                    print(f"Error: Received status code {response.status_code} from CrossRef API")

        except StopIteration:
            print("No more results found.")
            break

# Example usage
search_papers_combined("machine learning and cancer", num_results=3)
