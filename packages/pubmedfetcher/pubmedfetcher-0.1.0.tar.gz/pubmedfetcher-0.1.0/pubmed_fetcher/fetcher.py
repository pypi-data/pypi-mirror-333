import requests
import pandas as pd

class PubMedFetcher:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        self.db = "pubmed"
    
    def fetch_papers(self, query, max_results=10):
        """Fetches PubMed articles based on a user query."""
        params = {
            "db": self.db,
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        paper_ids = data.get("esearchresult", {}).get("idlist", [])
        return self.fetch_details(paper_ids)
    
    def fetch_details(self, paper_ids):
        """Fetches details of given paper IDs."""
        if not paper_ids:
            return []
        
        params = {
            "db": self.db,
            "id": ",".join(paper_ids),
            "retmode": "json"
        }
        
        response = requests.get(self.details_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        papers = []
        for paper_id in paper_ids:
            summary = data.get("result", {}).get(paper_id, {})
            title = summary.get("title", "N/A")
            authors = summary.get("authors", [])
            affiliation = summary.get("source", "N/A")
            
            papers.append({
                "id": paper_id,
                "title": title,
                "authors": authors,
                "affiliation": affiliation
            })
        
        return papers

    def filter_pharma_authors(self, papers):
        """Filters papers with authors affiliated with pharmaceutical or biotech companies."""
        pharma_keywords = ["pharma", "biotech", "laboratory", "research institute"]
        
        filtered_papers = []
        for paper in papers:
            for author in paper["authors"]:
                if any(keyword in str(author).lower() for keyword in pharma_keywords):
                    filtered_papers.append(paper)
                    break
        
        return filtered_papers

    def save_to_csv(self, papers, filename="pubmed_results.csv"):
        """Saves paper data to a CSV file."""
        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")