import re

def calculate_structure_features(text):

    features = {}

    # Figure Count
    figures = len(
        re.findall(r"figure|fig\\.", text.lower())
    )

    # Table Count
    tables = len(
        re.findall(r"table", text.lower())
    )

    # Section Count
    sections = len(
        re.findall(
            r"\\n[A-Z][A-Z\\s]{3,}\\n",
            text
        )
    )

    # Reference Count
    references = len(
        re.findall(r"\\[[0-9]+\\]", text)
    )

    features["figure_count"] = figures
    features["table_count"] = tables
    features["section_count"] = sections
    features["reference_count"] = references

    return features