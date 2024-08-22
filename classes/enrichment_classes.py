import random
from .utilities import clean_enrichment_name

class population:

    def __init__(self, student_list, enrichments):
        self.students = student_list
        self.enrichments = enrichment

        for x in self.students:
            x.randomize_assignment()

        self.genome = [x.assignment for x in self.students]

    def compute_penalty(self):
        """Computes current cost structure of genome
        -- cost of a ranked choice is rank - 1
        -- there is a penalty of +class max per each student over the class maximum
        -- there is a penalty of +5 per each student missing from the class minimum
        -- each student waitlisted gets a penalty of last ranked + 1
        """

class student:

    def __init__(self, email, grade, age, name, teacher):
        self.email = email
        self.grade = grade
        self.age = age
        self.name = name
        self.teacher = teacher
        self.assignment = 0
        self.enrichment_preference = {
            0: "waitlist"
        }

    def assign_preference(self, rank, enrichment_program):
        self.enrichment_preference[rank] = enrichment_program

    def randomize_assignment(self):
        self.assignment = random.randint(0, len(self.enrichment_preference.keys()) - 1)

class enrichment:
    def __init__(self, enrichment_name, min_size=8, max_size=12, waitlist_size=4):
        # defaults are minimum 8 students and max 12
        self.name = clean_enrichment_name(enrichment_name)
        self.min_size = min_size
        self.max_size = max_size
        self.waitlist_size = waitlist_size