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


path_to_json = 'team4/json'
json_files = [path_to_json+"/"+pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

import re



RULES = {
    # 1. contractions
    """
    Dont use contractions in papers. Write more formally: do not use contractions.
    """
    "contractions": re.compile(r"\b(?:"
        r"ain't|aren't|can't|couldn't|didn't|doesn't|don't|hadn't|hasn't|haven't|"
        r"isn't|it's|let's|mustn't|shan't|shouldn't|that's|there's|they're|"
        r"we're|weren't|won't|wouldn't|i'm|i've|i'd|i'll|he's|she's|you're|you've|you'll"
        r")\b", re.IGNORECASE),

    # 2. exclamation marks (no regex needed, but keep consistent)
    """
    Do not use exclamation marks (ever!).
    """

    "exclamation": re.compile(r"!"),

    # 3. signposting phrases

    """
    Avoid writing: “In this section we do the following…”. Just do the following.
    """

    "signposting": re.compile(
        r"\b(in this (section|paper|chapter)\s+we\b|"
        r"in the following (section|chapter)\b|"
        r"the remainder of this (paper|article|chapter)\b|"
        r"this (section|paper|chapter)\s+(describes|presents|discusses|introduces|outlines)\b)",
        re.IGNORECASE
    ),

    # 4. vague verbs (core ones from article)

    """
    Try to avoid vague words like “provides”, “enables”, “allows”, etc. These dont tell us anything about the mechanism. 
    How does the method/data provide/enable/allow? This is a general tip to make your science writing more precise.
    """

    "vague_verbs": re.compile(
        r"\b(provide|provides|provided|providing|"
        r"enable|enables|enabled|enabling|"
        r"allow|allows|allowed|allowing)\b",
        re.IGNORECASE
    ),

    # 5. "allows to" mistake

    """
    Another common error that I fix is the use of “allows to”. For example, I am often fixing sentences like “a learned warping field allows to model human deformations”. 
    “Allows to model” is wrong. A simple rewrite is “a learned warping field models human deformations” or “a learned warping field allows the method to model human deformations,” or 
    “a learned warping field makes it possible to model human deformations.” There are several meanings for the verb “allow” but the one being used here is “to give (someone) permission to
    do (something)”. The use here is missing the “someone”. In my second example, the “someone” is “the method”. 
    Whenever you find yourself wanting to write “allows to”, ask yourself “allows who to what?” Or, better yet, don’t use this. It is not precise. 
    It is not like our code is giving permission to “warping fields” to “model deformations”.
    """

    "allows_to": re.compile(r"\ballows?\s+to\b", re.IGNORECASE),

    # 6. aim to constructions

    """
    Similarly, one of the things I correct most is “we aim to exploit” or similar. Just write “we exploit”. Be direct. Say what you did.
    """

    "aim_to": re.compile(r"\baim(?:s|ed|ing)?\s+to\b", re.IGNORECASE),

    # 7. overuse of "we"

    """
    In general, people use “we” way too much in papers. They write “First we do x and then we do y.” when they mean that the “method” does x and then y. 
    If “we” do it, it means the authors did it by hand.
    """

    "we": re.compile(r"\bwe\b", re.IGNORECASE),

    # 8. hedging words

    """
    Avoid saying things passively. People often write “We can compute the X with Y.” What they mean is “We compute X with Y”. Saying you “can” do it means that you didn’t really do it but maybe could have. 
    If you did it, say you did it. If you didn’t do it, why are you writing this? Same goes for sentences like “The loss can be written as follows:”.
    Be more direct. “The loss is:”. Get rid of all the extra words and words that indicate that you are unsure or hesitant. Be definitive.
    """

    "hedging": re.compile(r"\b(can|could|may|might)\b", re.IGNORECASE),

    # 9. "to that end"

    """
    People over use “to that end”. When you use it, the “end” has to be really clear. In 80–90% of the cases, the end is not clear.
    """

    "to_that_end": re.compile(r"\bto that end\b", re.IGNORECASE),

    # 10. chatgpt-style words

    """
    A dead giveaway that you use ChatGPT is the presence of words like delve and showcase.
    I never want to see the word “showcase” to describe results. Results are there to evaluate your method not to sell it to someone. 
    We are not selling fancy watches! You, as a scientist, should be impartial. You made a hypothesis that your method would be better than the SOTA. 
    Your results are there to test this hypothesis in a dispassionate manner.
    """

    "chatgpt_words": re.compile(
        r"\b(delve|delves|delved|delving|showcase|showcases|showcased|showcasing)\b",
        re.IGNORECASE
    ),

    # 11. absolute claims

    """
    Also avoid terms like “paramount importance” — this literally means “more important than anything else”.
    That’s tough to support. Words like “unique” are similarly dangerous. These words leave no wiggle room — if you use them, you’re asking for a fight!
    """

    "absolute_words": re.compile(
        r"\b(unique|paramount|always|never)\b",
        re.IGNORECASE
    ),

    # 12. comparative vagueness

    """
    I often see people write things like “our work is more accurate” or “our method is more robust.” Or they write If you use the word “more,” 
    then you have to tell us more than what? That is, “our work is more accurate than the baseline”. The same applies to the use of “better” — better than what? Be explicit.
    """

    "comparatives": re.compile(r"\b(more|better)\b", re.IGNORECASE),

    # 13. passive voice (approx)

    """
    Avoid saying things passively. People often write “We can compute the X with Y.” What they mean is “We compute X with Y”. Saying you “can” do it means that you didn’t really do it but maybe could have. 
    If you did it, say you did it. If you didn’t do it, why are you writing this? Same goes for sentences like “The loss can be written as follows:”.
    Be more direct. “The loss is:”. Get rid of all the extra words and words that indicate that you are unsure or hesitant. Be definitive.
    
    Derived from Rule 8
    """

    "passive": re.compile(r"\b(is|was|were|are|been|be|being)\s+\w+ed\b", re.IGNORECASE),
}

def compute_rule_features(text, num_words):
    features = {}

    for name, pattern in RULES.items():
        matches = pattern.findall(text)

        features[f"num_{name}"] = len(matches)
        features[f"{name}_per_1000"] = (len(matches) / num_words * 1000) if num_words > 0 else 0
        features[f"uses_{name}"] = len(matches) > 0

    return features

parsed_data = [] 
for file in tqdm(json_files):
    with open(file, "r", encoding="utf-8") as f:
        parsed_data.append(json.load(f))

rows = []

for paper in tqdm(parsed_data):
    metadata = paper.get("metadata", {})
    text = paper.get("text", "")

    if not text or len(text.strip()) == 0:
        continue

    num_words = len(text.split())

    rule_features = compute_rule_features(text, num_words)

    row = {
        "biorxiv_doi": metadata.get("biorxiv_doi"),
        "published_doi": metadata.get("published_doi"),
        "title": metadata.get("preprint_title"),

        # readability
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "gunning_fog": textstat.gunning_fog(text),

        # merge rule features
        **rule_features
    }

    rows.append(row)

# Create dataframe
df_scores = pd.DataFrame(rows)

# Save as CSV
output_path = "rules_with_scores.csv"
df_scores.to_csv(output_path, index=False)

print(f"Saved {len(df_scores)} rows to {output_path}")
print(df_scores.head())