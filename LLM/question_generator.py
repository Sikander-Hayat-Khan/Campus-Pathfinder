QUESTIONS = {

    "student_id":
    "Please provide your student ID.",

    "error_message":
    "What error message do you see?",

    "course_code":
    "Please provide the course code.",

    "amount":
    "What amount is involved?"
}


def get_question(field):

    return QUESTIONS.get(
        field,
        "Please provide additional information."
    )