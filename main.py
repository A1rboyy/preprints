import json
import csv
import requests
import time
import os

API_URL = "https://api.semanticscholar.org/graph/v1/paper/DOI:{}"


def get_citation_count(doi: str) -> int:
    params = {"fields": "citationCount"}
    
    response = requests.get(API_URL.format(doi), params=params)
    
    if response.status_code != 200:
        print(f"Failed for {doi}: {response.status_code}")
        return None

    data = response.json()
    return data.get("citationCount", None)


def load_existing_dois(csv_path: str) -> set:
    """Read already processed DOIs from CSV"""
    processed = set()

    if not os.path.exists(csv_path):
        return processed

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            doi = row["doi"]
            citation_count = row["citation_count"]

            # only skip if we actually have a result
            if citation_count not in ("", "None", None):
                processed.add(doi)

    return processed


def process_metadata(json_path: str, output_csv: str):
    with open(json_path, "r") as f:
        metadata = json.load(f)

    articles = metadata["articles"]

    processed_dois = load_existing_dois(output_csv)

    # open in append mode
    file_exists = os.path.exists(output_csv)

    with open(output_csv, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # write header only if file is new
        if not file_exists:
            writer.writerow(["doi_type", "doi", "title", "citation_count"])

        for article in articles:
            title = article["preprint_title"]

            dois = [
                ("biorxiv_doi", article.get("biorxiv_doi")),
                ("published_doi", article.get("published_doi"))
            ]

            for doi_type, doi in dois:
                if not doi or doi in processed_dois:
                    continue

                citation_count = get_citation_count(doi)

                writer.writerow([doi_type, doi, title, citation_count])
                processed_dois.add(doi)

                print(f"{doi_type}: {doi} -> {citation_count}")

                time.sleep(1)


if __name__ == "__main__":
    process_metadata("SampleData/metadata.json", "citations.csv")