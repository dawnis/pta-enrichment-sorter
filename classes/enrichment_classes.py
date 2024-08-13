import re

class student:

    def __init__(self, email, grade, age, name, parent, teacher):
        self.email = email
        self.grade = grade
        self.age = age
        self.name = name
        self.parent = parent
        self.teacher = teacher
        self.enrichment_preference = {
            1: None,
            2: None,
            3: None
        }

    def assign_preference(self, rank, enrichment_program):
        self.enrichment_preference[rank] = enrichment_program

class enrichment:
    def __init__(self, enrichment_name, min_size=8, max_size=12, waitlist_size=4):
        # defaults are minimum 8 students and max 12
        enrichment_name_pattern = r':\s*(.*?)\s*\('
        rematch = re.search(enrichment_name_pattern, enrichment_name)
        self.raw_name = enrichment_name
        self.name = rematch.group(1)
        self.min_size = min_size
        self.max_size = max_size
        self.waitlist_size = waitlist_size