import random

import numpy as np
from classes.enrichment_c import gen_waitlist


class student:

    def __init__(self, email, grade, age, name, teacher):
        self.email = email
        self.grade = grade
        self.age = age
        self.name = name
        self.teacher = teacher
        self.assignment = {}
        self.enrichment_preference = {
            0: gen_waitlist()
        }

    def __str__(self):
        enrichments_assigned = "\n".join([
            self.enrichment_preference[self.assignment[x]].name for x in self.assignment.keys()
        ])

        possible_days = ", ".join(self.assignment.keys())

        return (f"Name: {self.name}\n"
                f"Grade: {self.grade}\n"
                f"Enrichments Assigned: {enrichments_assigned}\n"
                f"Possible Days: {possible_days}\n"
                f"Rankings: {self.enrichment_preference}")

    def assign_preference(self, rank, enrichment_program):
        """Enrichment program is an enrichment class object"""
        self.enrichment_preference[rank] = enrichment_program

    def randomize_assignment(self, alpha=None):
        for day in self.assignment.keys():
            if (alpha is None) or (random.random() < alpha):
                valid_prefs = dict(filter(lambda e: day in e[1].timeslot, self.enrichment_preference.items()))
                valid_prefs.update({0: self.enrichment_preference[0]})
                pref_list = [x for x in valid_prefs.keys()]
                self.assignment[day] = random.choice(pref_list)

        return

