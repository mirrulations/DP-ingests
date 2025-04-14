import re


def get_docket_id(document_id: str):
    # a regex that matches the last -xxxx of a document id
    pattern = r"-\d+$"

    return re.sub(pattern, "", document_id)


def create(document: dict):
    docket_id = document.get("docketId", get_docket_id(document.get("documentId")))
    return {
        "data": {
            "id": docket_id,
            "type": "dockets",
            "attributes": {
                "agencyId": document.get("agencyId"),
                "docketType": f"Dummy ({document.get('documentType')})",  # as far as i know these can be any of the following: `Rule`, `Other`, and `Notice`
                "modifyDate": document.get("modifyDate"),
                "title": document.get("title"),
            },
            "links": {"self": f"https://api.regulations.gov/v4/dockets/{docket_id}"},
        }
    }
