import os
import json
import pandas as pd

from text_features import calculate_text_features
from openalex import fetch_openalex_data
from structure_features import calculate_structure_features

JSON_FOLDER = "data/final_data/json"
XML_FOLDER = "data/final_data/xml"

results = []

for file in os.listdir(JSON_FOLDER):

    if not file.endswith(".json"):
        continue

    path = os.path.join(JSON_FOLDER, file)

    print(f"\nProcessing: {file}")

    with open(path, "r", encoding="utf-8") as f:

        data = json.load(f)

    text = data.get("text", "")

    if not text:
        print("Skipped: no text")
        continue

    # ======================
    # Qualitätsfilter
    # ======================

    word_count = len(text.split())

    if word_count < 1000:
        print("Skipped: too short")
        continue

    if word_count > 30000:
        print("Skipped: too long")
        continue

    # ======================
    # Text Features
    # ======================

    features = calculate_text_features(text)

    # ======================
    # Struktur Features
    # ======================

    features["figure_count"] = len(
        data.get("figures", [])
    )

    features["table_count"] = len(
        data.get("tables", [])
    )

    xml_file = file.replace(
        ".json",
        ".xml"
    )

    xml_path = os.path.join(
        XML_FOLDER,
        xml_file
    )

    structure_features = (
        calculate_structure_features(
            xml_path
        )
    )

    features.update(
        structure_features
    )

    # ======================
    # Metadaten
    # ======================

    metadata = data.get("metadata", {})

    pub_metadata = metadata.get(
        "pub_metadata",
        {}
    )

    doi = metadata.get("doi")

    features["doi"] = doi

    features["preprint_date"] = (
        pub_metadata.get("preprint_date")
    )

    features["preprint_category"] = (
        pub_metadata.get("preprint_category")
    )

    features["published_doi"] = (
        pub_metadata.get("published_doi")
    )

    features["published_flag"] = (
        1
        if pub_metadata.get("published_doi")
        else 0
    )

    # ======================
    # OpenAlex
    # ======================

    if doi:

        print("Fetching OpenAlex data...")

        openalex_data = fetch_openalex_data(
            doi
        )

        if openalex_data:

            features.update(
                openalex_data
            )

        else:

            print(
                "No OpenAlex data found."
            )

    # ======================
    # Datensatz erweitern
    # ======================

    results.append(features)

# ======================
# EXPORT
# ======================

df = pd.DataFrame(results)

os.makedirs(
    "output",
    exist_ok=True
)

df.to_csv(
    "output/full_dataset.csv",
    sep=";",
    index=False
)

print("\nDone.")
print(df.head())

print("\nDataset Shape:")
print(df.shape)