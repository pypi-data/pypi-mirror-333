import argparse
from pubmed_fetcher.fetcher import PubMedFetcher

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed articles and filter pharmaceutical/biotech authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("--max", type=int, default=10, help="Maximum number of results")
    parser.add_argument("--output", type=str, default="pubmed_results.csv", help="Output CSV file name")

    args = parser.parse_args()

    fetcher = PubMedFetcher()
    papers = fetcher.fetch_papers(args.query, args.max)
    
    if not papers:
        print("No results found.")
        return
    
    filtered_papers = fetcher.filter_pharma_authors(papers)
    fetcher.save_to_csv(filtered_papers, args.output)

if __name__== "_main_":
    main()