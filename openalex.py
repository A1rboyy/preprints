import requests
import time


CURRENT_YEAR = 2026

def fetch_openalex_data(doi):

    url = f"https://api.openalex.org/works/https://doi.org/{doi}"

    try:

        response = requests.get(url)

        if response.status_code != 200:

            print(f"Error {response.status_code} for DOI: {doi}")

            return None

        data = response.json()

        citation_count = data.get("cited_by_count", 0)

        publication_year = data.get("publication_year")

        # Citations per year berechnen
        if publication_year:

            citations_per_year = (
                citation_count /
                (CURRENT_YEAR - publication_year + 1)
            )

        else:

            citations_per_year = None

        # Journal extrahieren
        journal_name = (
            data.get("primary_location", {})
                .get("source", {})
                .get("display_name")
        )

        # Published Flag
        published_flag = 1 if journal_name else 0

        return {

            "citation_count":
                citation_count,

            "publication_year":
                publication_year,

            "citations_per_year":
                round(citations_per_year, 2)
                if citations_per_year else None,

            "journal_name":
                journal_name,

            "published_flag":
                published_flag,

            "is_open_access":
                data.get("open_access", {})
                    .get("is_oa"),

            "type":
                data.get("type"),

            "openalex_id":
                data.get("id")
        }

    except Exception as e:

        print("OpenAlex Error:", e)

        return None

    finally:

        time.sleep(0.1)


