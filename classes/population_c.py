import random
import pandas as pd
import numpy as np
import copy

from .enrichment_c import enrichment, gen_waitlist


class population:

    def __init__(self, student_list, enrichments):
        self.students = student_list
        self.enrichment = enrichments

        #add waitlist into the list of enrichments
        self.enrichment.update({"waitlist": gen_waitlist()})
        self.penalty_history = []

        #for each student, check if they signed up for grade appropriate enrichments. Flag if there is a problem
        for x in self.students:
            invalid_ranks = []
            for (r, e) in x.enrichment_preference.items():
                if e.name == 'waitlist':
                    continue

                if x.grade not in e.gradelevel:
                    invalid_ranks.append(r)

            for rank in invalid_ranks:
                print(f"Warning! {x.name} (grade {x.grade} signed up for {x.enrichment_preference[rank].name} (grades {x.enrichment_preference[rank].gradelevel}) -- preference is removed")
                del x.enrichment_preference[rank]

            if len(invalid_ranks) > 0:
                remaining_names = [x.name if x.name != 'waitlist' else '' for (r, x) in x.enrichment_preference.items()]
                print(f"Remaining preferences are {", ".join(remaining_names)}")

        #for each student, add a waitlist assignment for each day they can go to enrichment
        for x in self.students:
            for (r, e) in x.enrichment_preference.items():
                if e.name != 'waitlist':
                    x.assignment.update({e.timeslot: 0})

        for x in self.students:
            x.randomize_assignment()

    def produce_class_assignment_sheet(self):
        """Outputs current assignments for student population"""
        student_rows = []
        for student in self.students:
            for (k, v) in student.assignment.items():
                student_rows.append({
                    "Name": student.name,
                    "Grade": student.grade,
                    "Email": student.email,
                    "Teacher": student.teacher,
                    "Enrichment": str(student.enrichment_preference[v]),
                    "Day": k,
                    "Ranking": v,
                    "Num Classes Requested": student.num_classes
                })

        worksheet = pd.DataFrame(student_rows)

        # Get students that are waitlist only
        wdf_filt = pd.DataFrame([x.name for x in self.get_waitlist_only()], columns = ["Name"])

        waitlist = pd.merge(wdf_filt, worksheet, on=['Name'], how='left')

        worksheet_filt = worksheet.query("Enrichment != 'waitlist'").copy()

        return pd.concat([worksheet_filt, waitlist], axis=0)

    def report_multi_asignments(self):
        """Reports any students with multiple assignments"""
        for student in self.students:
            preferences = [x for (k, x) in student.assignment.items()]
            num_assignments = np.sum(list(map(lambda x: x != 0, preferences)))
            if num_assignments > 1:
                print(student)
                print("\n")
        return

    def report_invalid_preferences(self):
        """Reports any students with no possible assignments"""
        for student in self.students:
            preferences = [x for (k, x) in student.assignment.items()]
            if len(preferences) == 0:
                print(student)
                print("\n")
        return

    def display_student(self, student_name):
        student_lookup = filter(lambda x: x.name.lower().startswith(student_name.lower()), self.students)
        for s in student_lookup:
            print(s)
            student = s
        return student

    def get_waitlist_only(self):
        """Returns a list of students who are only assigned to waitlist"""
        s = []
        for student in self.students:
            preferences = [x for (k, x) in student.assignment.items()]
            if np.sum(preferences) == 0:
                s.append(student)
        return s

    def display_current_waitlist(self):
        waitlist = self.get_waitlist_only()
        for student in waitlist:
            print(student)
            print("\n")
        return

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
            s.randomize_assignment(mut_prob)
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
                        "class_name": str(s.enrichment_preference[r]),
                        "ranking": r
                    })
        agg = pd.DataFrame(ers)
        agg_c =  agg.groupby(['class_name', 'ranking'])["name"].count()
        agg_c_pvt =  agg_c.unstack().fillna(0)
        agg_c_pvt["total"] = agg_c_pvt.sum(axis=1)
        return agg_c_pvt.sort_values(by=["total"], ascending=False)

    def enrichment_limits(self):
        """Computes dataframe with min/max size for each enrichment class to aid in computing penalty"""
        e_frame = []
        for (k, e) in self.enrichment.items():
            e_frame.append(
                {"enrichment": e.name,
                 "min": e.min_size,
                 "max": e.max_size
                 }
            )
        return pd.DataFrame(e_frame)

    def class_counts(self, student_list):

        class_assignment_list = []

        for s in student_list:
            for (day, rank) in s.assignment.items():
                class_assignment_list.append(
                    {"enrichment": str(s.enrichment_preference[rank]), "name": s.name}
                )
        counter_df = pd.DataFrame(class_assignment_list)

        #need to filter out students assigned to any class for waitlisted population
        waitlist = counter_df.query("enrichment == 'waitlist'").copy()
        nonwaitlist = counter_df.query("enrichment != 'waitlist'").copy()
        waitlist_only = pd.DataFrame(set(waitlist.name) - set(nonwaitlist.name), columns = ['name'])

        waitlist_filt = pd.merge(waitlist,
                                 waitlist_only,
                                 on = ['name'],
                                 how = 'inner').drop_duplicates().copy()

        counter_df_filt = pd.concat([nonwaitlist, waitlist_filt], axis=0)


        edf_count = counter_df_filt.groupby(["enrichment"])["name"].nunique()
        return edf_count.reset_index()

    def compute_penalty(self, student_list):
        """Computes current cost structure of genome
        -- cost of a ranked choice is rank - 1
        -- there is a penalty of +class max per each student over the class maximum
        -- there is a penalty of +5 per each student missing from the class minimum
        -- each student waitlisted gets a penalty of last ranked + 1
        """

        # g = self.genome(student_list)

        #1st compute penalty associated with each choice
        choice_score = self.rank_choice_penalty(student_list)

        #compute scores for determining if class size bounds (min or max) are violated
        edf_count = self.class_counts(student_list)
        e_limits = self.enrichment_limits()
        edf_counts = pd.merge(edf_count, e_limits, on=['enrichment'], how='outer')
        edf_counts = edf_counts.fillna(0)

        #compute a penalty for each student on wait list
        waitlist_penalty =  len(self.get_waitlist_only())**2

        class_size_penalty = 0
        for (idxx, row) in edf_counts.iterrows():
            if row['name'] > row['max']:
                class_size_penalty += 10 * (row['name'] - row['max'])
            elif row['name'] < row['min']:
                class_size_penalty += (row['min'] - row['name']) * 10
            elif row['enrichment'] != 'waitlist':
                class_size_penalty += 4*(row['max'] - row['name']) #add a flat penalty for each unfilled spot

        return choice_score + class_size_penalty + waitlist_penalty


    def rank_choice_penalty(self, student_list):
        """Computes the summed average penalty for each student's ranking, skipping zeros"""
        penalty = 0
        for student in student_list:
            preferences = [x for (k, x) in student.assignment.items()]

            rank_penalty = np.min(preferences) - 1
            zeros_penalty = np.sum(preferences == 0) / 2
            # if np.sum(preferences) == 0:
            #     continue
            # else:
            #     filt_prefs = filter(lambda a: a != 0, preferences)
            #     penalty += np.mean([x-1 for x in filt_prefs])

            penalty += rank_penalty + zeros_penalty

        return penalty
