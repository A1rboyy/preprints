import os
import pandas as pd

from pdf_parser import extract_text_from_pdf
from text_features import calculate_text_features
from structure_features import calculate_structure_features
from openalex import fetch_openalex_data

PDF_FOLDER = "data/pdfs"

results = []

for file in os.listdir(PDF_FOLDER):

    if file.endswith(".pdf") and not file.startswith("._"):

        path = os.path.join(PDF_FOLDER, file)

        print(f"\nProcessing: {file}")

        # PDF Text extrahieren
        text = extract_text_from_pdf(path)

        # einfache Qualitätsfilter
        word_count = len(text.split())

        if word_count < 1000:
            print("Skipped: too short")
            continue

        if word_count > 30000:
            print("Skipped: too long")
            continue

        # Text Features berechnen
        features = calculate_text_features(text)
        structure_features = calculate_structure_features(text)

        features.update(structure_features)

        # DOI aus Dateiname
        doi = file.replace(".pdf", "")
        doi = doi.replace("_", "/")

        features["doi"] = doi
        features["file"] = file

        # OpenAlex Daten abrufen
        print("Fetching OpenAlex data...")

        openalex_data = fetch_openalex_data(doi)

        if openalex_data:

            features.update(openalex_data)

        else:

            print("No OpenAlex data found.")

        # Ergebnisse speichern
        results.append(features)

# ==========================================
# EXPORT
# ==========================================

df = pd.DataFrame(results)

os.makedirs("output", exist_ok=True)

df.to_csv(
    "output/full_dataset.csv",
    index=False,
    sep=";"
)

print("\nDone.")
print(df.head())