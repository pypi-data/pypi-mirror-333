import requests
import csv
from typing import List, Dict

# Base URL for PubMed API
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

class PubMedFetcher:
    """Class to fetch research papers from PubMed based on a query."""

    @staticmethod
    def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[str]:
        """Fetches paper IDs from PubMed based on the search query."""
        params = {
            "db": "pubmed",  # Specify database
            "term": query,  # Search term
            "retmode": "json",  # Response format
            "retmax": max_results  # Maximum results
        }
        response = requests.get(PUBMED_API_URL, params=params)
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

    @staticmethod
    def get_paper_details(paper_id: str) -> Dict[str, str]:
        """Fetches details of a paper using its PubMed ID."""
        return {
            "PubmedID": paper_id,
            "Title": "Sample Paper Title",  # Placeholder title
            "Publication Date": "2025-01-01",  # Placeholder date
            "Non-academic Author(s)": "Dr. John Doe",  # Example author
            "Company Affiliation(s)": "XYZ Biotech",  # Example company
            "Corresponding Author Email": "johndoe@xyzbiotech.com"  # Example email
        }

    @staticmethod
    def save_to_csv(results: List[Dict[str, str]], filename: str):
        """Saves paper details to a CSV file."""
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
