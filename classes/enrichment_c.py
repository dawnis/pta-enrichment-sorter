import re

def gen_waitlist():
    """Generates a dummy class called waitlist"""
    # return enrichment("1st, 2nd, 3rd, 4th, 5th graders: waitlist (Sundays, $00)", min_size=0, max_size=1000)
    return enrichment("Sundays, waitlist (1st, 2nd, 3rd, 4th, 5th graders, $00)", min_size=0, max_size=1000)

class enrichment:
    def __init__(self, enrichment_name, min_size=8, max_size=12):
        # defaults are minimum 8 students and max 12
        self.name = clean_enrichment_name(enrichment_name)
        self.min_size = min_size
        self.max_size = max_size
        self.timeslot = regex_timeslot(enrichment_name)
        self.gradelevel = regex_grades(enrichment_name)

    def __str__(self):
        return (f"{self.name}")

    def __repr__(self):
        return (f"{self.name}")

def clean_enrichment_name(enrichment_raw):
    """Cleans up enrichment name string"""
    #enrichment_name_pattern = r':\s*(.*?)\s*\('
    enrichment_name_pattern = r',\s*(.*?)\s*\('
    rematch = re.search(enrichment_name_pattern, enrichment_raw)
    return rematch.group(1)

def regex_grades(enrichment_raw):
    """Gets the grade levels from the raw enrichment name"""
    grade_pattern = r'(?:K|\d+(?:st|nd|rd|th))'
    grade_strings =  re.findall(grade_pattern, enrichment_raw)
    return [g[0] for g in grade_strings]

def regex_timeslot(enrichment_raw):
    """Pulls the meeting day from the enrichment title"""
    # weekday_pattern = "(?i)(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
    weekday_pattern = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"
    matches = re.findall(weekday_pattern, enrichment_raw)
    return matches[0]


