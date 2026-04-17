from datetime import datetime


# Function to parse date fields (regulations.gov ISO-Z and Federal Register date-only)
def parse(date: str):
    if not date:
        return None
    # date can be 0000-12-30T00:00:00Z in certain cases, like postedDate in the comment CMS-2009-0058-DRAFT-2645
    if date.startswith("0000"):
        date = date.replace("0000", "2000")
    if len(date) == 10 and date[4] == "-" and date[7] == "-":
        return datetime.strptime(date, "%Y-%m-%d")
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
