import os, json
import pandas as pd
import matplotlib
from tqdm.auto import trange, tqdm
import textstat


## Gunning Fox = More complex text has a higher score. A score of 12 means that the text is understandable by a 12th grader. 
# A score of 8 means that the text is understandable by an 8th grader. A score of 20 means that the text is very complex and may be difficult for most people to understand.


# flesch_kincaid_grade = The Flesch-Kincaid Grade Level is a readability test designed to
# indicate how difficult a passage in English is to understand. It uses the total number of words, sentences, 
# and syllables in the text to calculate a grade level. A score of 8.0 means that the text is understandable by an 8th grader, while a score of 12.0 means that it is understandable by a 12th grader.


## flesch_reading_ease = The Flesch Reading Ease score is a readability test designed 
# to indicate how difficult a passage in English is to understand. It uses the total number of words,
#  sentences, and syllables in the text to calculate a score. A higher score indicates that the text is easier
#  to read, while a lower score indicates that it is more difficult. For example, a score of 90-100 means that the text is very easy to read, while a score of 0-30 means that it is very difficult to read.


path_to_json = 'SampleData/output'
json_files = [path_to_json+"/"+pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]


parsed_data = [] 
for file in tqdm(json_files):
    with open(file, "r") as f:
        parsed_data.append(json.load(f))


rows = []

for paper in tqdm(parsed_data):

    metadata = paper.get("metadata", {})
    text = paper.get("text", "")

    # Skip empty texts
    if not text or len(text.strip()) == 0:
        continue

    row = {
        "biorxiv_doi": metadata.get("biorxiv_doi"),
        "published_doi": metadata.get("published_doi"),
        "title": metadata.get("preprint_title"),

        # Readability metrics
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "gunning_fog": textstat.gunning_fog(text),
    }

    rows.append(row)

# Create dataframe
df_scores = pd.DataFrame(rows)

# Save as CSV
output_path = "readability_scores.csv"
df_scores.to_csv(output_path, index=False)

print(f"Saved {len(df_scores)} rows to {output_path}")
print(df_scores.head())