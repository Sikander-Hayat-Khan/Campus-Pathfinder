def should_escalate(confidence, urgency):

    if confidence < 0.70:
        return True

    if urgency == "high":
        return True

    return False

def route(category):
    mapping = {
        "login_issue": "IT Department",
        "registration_issue": "Registrar Office",
        "fee_issue": "Finance Office",
        "exam_issue": "Examination Office"
    }
    return mapping.get(category, "General Support")

def route(category):

    mapping = {

        "login_issue":
        "IT Department",

        "registration_issue":
        "Registrar Office",

        "fee_issue":
        "Finance Office",

        "exam_issue":
        "Examination Office"
    }

    return mapping.get(category, "General Support")