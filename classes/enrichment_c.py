import re


class enrichment:
    def __init__(self, enrichment_name, min_size=8, max_size=12):
        # defaults are minimum 8 students and max 12
        self.name = clean_enrichment_name(enrichment_name)
        self.min_size = min_size
        self.max_size = max_size
        self.timeslot = regex_timeslot(enrichment_name)
        self.gradelevel = regex_grades(enrichment_name)


def clean_enrichment_name(enrichment_raw):
    """Cleans up enrichment name string"""
    enrichment_name_pattern = r':\s*(.*?)\s*\('
    rematch = re.search(enrichment_name_pattern, enrichment_raw)
    return rematch.group(1)

def regex_grades(enrichment_raw):
    """Gets the grade levels from the raw enrichment name"""
    grade_pattern = r'^(.*?) graders\s?:'
    gmatch = re.search(grade_pattern, enrichment_raw)
    return [x.strip() for x in gmatch.group(1).split(",")]

def regex_timeslot(enrichment_raw):
    """Pulls the meeting day from the enrichment title"""
    weekday_pattern = "(?i)(?:Monday|Tuesday|Wednesday|Thursday|Friday)"
    matches = re.findall(weekday_pattern, enrichment_raw)
    return matches[0]


