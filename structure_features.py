import xml.etree.ElementTree as ET

def calculate_structure_features(xml_path):

    features = {}

    try:

        tree = ET.parse(xml_path)

        root = tree.getroot()

        # Sections zählen
        sections = len(
            root.findall(".//sec")
        )

        # References zählen
        references = len(
            root.findall(".//ref")
        )

        features["section_count"] = sections
        features["reference_count"] = references

    except Exception as e:

        print(
            f"XML Error: {xml_path} -> {e}"
        )

        features["section_count"] = None
        features["reference_count"] = None

    return features