import random

import numpy as np


class student:

    def __init__(self, email, grade, age, name, teacher):
        self.email = email
        self.grade = grade
        self.age = age
        self.name = name
        self.teacher = teacher
        self.assignment = 0
        self.slots = []
        self.enrichment_preference = {
            0: "waitlist"
        }

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Grade: {self.grade}\n"
                f"Enrichments Assigned: {self.enrichment_preference[self.assignment]}\n"
                f"Possible Days: {self.slots}\n"
                f"Rankings: {self.enrichment_preference}")

    def retrieve_assignment(self):
        return self.enrichment_preference[self.assignment]

    def assign_preference(self, rank, enrichment_program):
        self.enrichment_preference[rank] = enrichment_program

    def randomize_assignment(self):
        self.assignment = random.randint(0, np.max([x for x in self.enrichment_preference.keys()]))

