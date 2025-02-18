import requests

def download_wikidata_sparql_csv(query, file_path):
    url = 'https://query.wikidata.org/sparql'
    
    response = requests.get(url, params={'query': query}, headers={'Accept': 'text/csv'})
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True
    else:
        print(f"Error: Failed to retrieve data. Status code {response.status_code}")
        return False