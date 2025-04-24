from datetime import datetime


def parse(date: str):
    """
    Parse date fields
    """
    if date:
        # date can be 0000-12-30T00:00:00Z in certain cases, like postedDate in the comment CMS-2009-0058-DRAFT-2645
        if date.startswith("0000"):  
            # this mimics the behavior from regulations.gov's website,
            date = date.replace("0000", "2000")
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return None
