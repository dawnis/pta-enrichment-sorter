from .enrichment_classes import student

def process_registration_form(df_csv):
    """Returns a list of student from the registration form"""
    student_list = []
    for (idx, row) in df_csv.iterrows():
        student_list.append(
            student(
                row["Email Address"],
                row["Child's Grade"],
                row["Child's Age"],
                " ".join([row["Student's First Name"], row["Student's Last Name"]]),
                row["Child's Teacher"]
            )
        )

    #TODO: make second pass to get class prefs
    return student_list