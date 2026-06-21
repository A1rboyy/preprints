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

import re


CONTRACTION_PATTERN = re.compile(
    r"\b(?:"
    r"ain't|aren't|can't|couldn't|didn't|doesn't|don't|hadn't|hasn't|haven't|"
    r"he'd|he'll|he's|I'd|I'll|I'm|I've|isn't|it's|let's|mightn't|mustn't|"
    r"shan't|she'd|she'll|she's|shouldn't|that's|there's|they'd|they'll|"
    r"they're|they've|wasn't|we'd|we'll|we're|we've|weren't|what's|where's|"
    r"who's|won't|wouldn't|you'd|you'll|you're|you've|n't|'re|'ve|'ll|'d|'m"
    r")\b",
    re.IGNORECASE
)

SIGNPOSTING_PATTERN = re.compile(
    r"\b("
    r"in this (section|paper|chapter|study|work)\s+we\b|"
    r"in the following (section|chapter)\b|"
    r"the remainder of this (paper|article|chapter)\b|"
    r"this (section|paper|chapter)\s+(describes|presents|discusses|introduces|outlines)\b|"
    r"in this section\b|"
    r"we (first|next|then|begin by)\b"
    r")",
    re.IGNORECASE
)


VAGUE_VERBS = [
    "provide", "provides", "provided", "providing",
    "enable", "enables", "enabled", "enabling",
    "allow", "allows", "allowed", "allowing"
]

VAGUE_VERB_PATTERN = re.compile(
    r"\b("
    r"provide|provides|provided|providing|"
    r"enable|enables|enabled|enabling|"
    r"allow|allows|allowed|allowing"
    r")\b",
    re.IGNORECASE
)

parsed_data = [] 
for file in tqdm(json_files):
    with open(file, "r") as f:
        parsed_data.append(json.load(f))

## Uses 

rows = []

for paper in tqdm(parsed_data):

    metadata = paper.get("metadata", {})
    text = paper.get("text", "")

    # Skip empty texts
    if not text or len(text.strip()) == 0:
        continue

    vague_verb_matches = VAGUE_VERB_PATTERN.findall(text)

    num_vague_verbs = len(vague_verb_matches)
    uses_vague_verbs = num_vague_verbs > 0

    # Writing style checks
    has_contractions = bool(CONTRACTION_PATTERN.search(text))
    has_exclamation_marks = "!" in text
    has_signposting = bool(SIGNPOSTING_PATTERN.search(text))

    row = {
        "biorxiv_doi": metadata.get("biorxiv_doi"),
        "published_doi": metadata.get("published_doi"),
        "title": metadata.get("preprint_title"),

        # Readability metrics
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "gunning_fog": textstat.gunning_fog(text),

        # Writing tips as flags
        "uses_contractions": has_contractions,
        "uses_exclamation_marks": has_exclamation_marks,
        "uses_signposting_phrases": has_signposting,

        # Vague verbs
        "uses_vague_verbs": uses_vague_verbs,
        "num_vague_verbs": num_vague_verbs
    }

    rows.append(row)

# Create dataframe
df_scores = pd.DataFrame(rows)

# Save as CSV
output_path = "rules_with_scores.csv"
df_scores.to_csv(output_path, index=False)

print(f"Saved {len(df_scores)} rows to {output_path}")
print(df_scores.head())