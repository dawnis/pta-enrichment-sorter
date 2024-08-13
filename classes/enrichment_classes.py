from .utilities import clean_enrichment_name

class student:

    def __init__(self, email, grade, age, name, teacher):
        self.email = email
        self.grade = grade
        self.age = age
        self.name = name
        self.teacher = teacher
        self.enrichment_preference = {
            1: None
        }

    def assign_preference(self, rank, enrichment_program):
        self.enrichment_preference[rank] = enrichment_program

class enrichment:
    def __init__(self, enrichment_name, min_size=8, max_size=12, waitlist_size=4):
        # defaults are minimum 8 students and max 12
        self.name = clean_enrichment_name(enrichment_name)
        self.min_size = min_size
        self.max_size = max_size
        self.waitlist_size = waitlist_size