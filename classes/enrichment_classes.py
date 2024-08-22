import random
import pandas as pd
import numpy as np
from .utilities import clean_enrichment_name

class population:

    def __init__(self, student_list, enrichments):
        self.students = student_list
        self.enrichments = enrichment
        self.mutation_probability = 0.10
        self.penalty_history = []

        for x in self.students:
            x.randomize_assignment()


    def genome(self):
        """returns current genome for population"""
        return [x.assignment for x in self.students]

    def evolve(self, number_steps):
        f = self.compute_penalty()
        self.penalty_history = [f]
        for x in range(number_steps):
            s_old = self.students.copy()
            self.mutate()
            f_prime = self.compute_penalty()

            if f_prime >= f:
                self.students = s_old
            else:
                f = f_prime

            self.penalty_history.append(f)
            if np.mod(x, 100) == 0:
                print(f"Penalty of: {f}")

        return f

    def mutate(self):
        for s in self.students:
            if random.random() < self.mutation_probability:
                s.randomize_assignment()

    def enrichment_ranking_summary(self):
        """Returns a summary of how many students ranked each class 1st, 2nd, etc.
        Have options for either waitlist only or all"""

        ers = []
        for s in self.students:
            for r in s.enrichment_preference.keys():
                if r != 0:
                    ers.append ({
                        "name": s.name,
                        "class_name": s.enrichment_preference[r],
                        "ranking": r
                    })
        agg = pd.DataFrame(ers)
        agg_c =  agg.groupby(['class_name', 'ranking'])["name"].count()
        agg_c_pvt =  agg_c.unstack().fillna(0)
        agg_c_pvt["total"] = agg_c_pvt.sum(axis=1)
        return agg_c_pvt.sort_values(by=["total"], ascending=False)

    def class_counts(self):
        enrichment_choices = [
            {"enrichment": s.retrieve_assignment()} for s in self.students
        ]

        enrichment__counter_df = pd.DataFrame(enrichment_choices)
        edf_count = enrichment__counter_df.groupby("enrichment")["enrichment"].count()
        return edf_count

    def compute_penalty(self):
        """Computes current cost structure of genome
        -- cost of a ranked choice is rank - 1
        -- there is a penalty of +class max per each student over the class maximum
        -- there is a penalty of +5 per each student missing from the class minimum
        -- each student waitlisted gets a penalty of last ranked + 1
        """

        #1st compute penalty associated with each choice
        choice_score = np.sum([4 if x == 0 else x-1 for x in self.genome()])

        #class exceed maximum score
        edf_count = self.class_counts()

        class_size_penalty = 0

        for e in edf_count.index:
            if edf_count[e] > 12:
                class_size_penalty += 5 * (edf_count[e] - 12)
            elif edf_count[e] < 8:
                class_size_penalty += (8 - edf_count[e]) * 5

        return choice_score + class_size_penalty

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

    def retrieve_assignment(self):
        return self.enrichment_preference[self.assignment]

    def assign_preference(self, rank, enrichment_program):
        self.enrichment_preference[rank] = enrichment_program

    def randomize_assignment(self):
        self.assignment = random.randint(0, len(self.enrichment_preference.keys()) - 1)

class enrichment:
    def __init__(self, enrichment_name, min_size=8, max_size=12):
        # defaults are minimum 8 students and max 12
        self.name = clean_enrichment_name(enrichment_name)
        self.min_size = min_size
        self.max_size = max_size