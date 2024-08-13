import re
from .enrichment_classes import student

def clean_enrichment_name(enrichment_raw):
    """Cleans up enrichment name string"""
    enrichment_name_pattern = r':\s*(.*?)\s*\('
    rematch = re.search(enrichment_name_pattern, enrichment_raw)
    return rematch.group(1)

def process_registration_form(df_csv):
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
                s.assign_preference(ranking+1, clean_enrichment_name(preference))

        student_list.append(s)

    return student_list