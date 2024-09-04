from .enrichment_c import clean_enrichment_name
from .student_c import student

def process_registration_form(df_csv, enrichment_dict):
    """Returns a list of student from the registration form"""
    student_list = []
    for (idx, row) in df_csv.iterrows():
        s = student(
            row["Email Address"],
            row["Child's Grade"],
            row["Child's Age"],
            " ".join([row["Student's First Name"], row["Student's Last Name"]]),
            row["Child's Teacher"] )

        for ranking in range(4):
            if ranking == 0:
                str = '1st'
            elif ranking == 1:
                str = '2nd'
            elif ranking == 2:
                str = '3rd'
            else:
                str = f"{ranking+1}th"

            preference = row[f"Rank your child's {str} choice of classes"]

            if preference == preference:
                enrichment_name = clean_enrichment_name(preference)
                s.assign_preference(ranking + 1, enrichment_dict[enrichment_name])

        student_list.append(s)

    return student_list