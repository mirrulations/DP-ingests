from datetime import datetime


# Function to parse date fields
def parse(date: str):
    if date:
        if date.startswith(
            "0000"
        ):  # date can be 0000-12-30T00:00:00Z in certain cases, like postedDate in the comment CMS-2009-0058-DRAFT-2645
            date = date.replace(
                "0000", "2000"
            )  # this is the behavior from regulations.gov's website,
            # i believe this may be because the comment was withdrawn...
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return None
