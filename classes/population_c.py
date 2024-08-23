import random
import pandas as pd
import numpy as np
import copy

from .enrichment_c import enrichment

class population:

    def __init__(self, student_list, enrichments):
        self.students = student_list
        self.enrichment = enrichments
        self.mutation_probability = 0.10
        self.penalty_history = []

        for x in self.students:
            x.randomize_assignment()

    def set_mutation_prob(self):
        """returns the mutation rate for each round of evolution"""
        n = len(self.students)
        alpha = [(x+1)/n for x in range(20)]
        return random.choice(alpha)


    def genome(self, student_list):
        """returns current genome for population"""
        return [x.assignment for x in student_list]

    def evolve(self, number_steps):
        f = self.compute_penalty(self.students)
        self.penalty_history = [f]
        reporting_steps = np.round(number_steps/10)

        for x in range(number_steps):
            m = self.set_mutation_prob()
            s_old = copy.deepcopy(self.students)

            self.mutate(m)
            f_prime = self.compute_penalty(self.students)

            if f_prime < f:
                f = f_prime
            else:
                self.students = s_old

            self.penalty_history.append(f)

            if np.mod(x, reporting_steps) == 0:
                print(f"Step {x}, mutation_rate: {m}, computed penalty: {self.compute_penalty(self.students)}")

        return

    def mutate(self, mut_prob):
        for s in self.students:
            if random.random() < mut_prob:
                s.randomize_assignment()
        return

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

    def class_counts(self, student_list):
        enrichment_choices = [
            {"enrichment": s.retrieve_assignment()} for s in student_list
        ]

        enrichment__counter_df = pd.DataFrame(enrichment_choices)
        edf_count = enrichment__counter_df.groupby("enrichment")["enrichment"].count()
        return edf_count

    def compute_penalty(self, student_list):
        """Computes current cost structure of genome
        -- cost of a ranked choice is rank - 1
        -- there is a penalty of +class max per each student over the class maximum
        -- there is a penalty of +5 per each student missing from the class minimum
        -- each student waitlisted gets a penalty of last ranked + 1
        """

        g = self.genome(student_list)

        #1st compute penalty associated with each choice
        choice_score = np.sum([x-1 if x > 0 else 0 for x in g])

        #class exceed maximum score
        edf_count = self.class_counts(student_list)

        #compute a penalty for each student on wait list
        waitlist_penalty =  np.sum([x==0 for x in g])**2

        class_size_penalty = 0

        for e in edf_count.index:
            if edf_count[e] > 12:
                class_size_penalty += 10 * (edf_count[e] - 12)
            elif edf_count[e] < 8:
                class_size_penalty += (8 - edf_count[e]) * 10

        return choice_score + class_size_penalty + waitlist_penalty
