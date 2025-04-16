import re


def get_docket_id(document_id: str):
    # a regex that matches the last -xxxx of a document id
    pattern = r"-\d+$"

    return re.sub(pattern, "", document_id)


def create(document_attributes: dict):
    docket_id = document_attributes.get("docketId", get_docket_id(document_attributes.get("documentId")))
    return {
        "data": {
            "id": docket_id,
            "type": "dockets",
            "attributes": {
                "agencyId": document_attributes.get("agencyId"),
                "docketType": f"Dummy ({document_attributes.get('documentType')})",  # as far as i know these can be any of the following: `Rule`, `Other`, and `Notice`
                "modifyDate": document_attributes.get("modifyDate"),
                "title": document_attributes.get("title"),
            },
            "links": {"self": f"https://api.regulations.gov/v4/dockets/{docket_id}"},
        }
    }
