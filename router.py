def should_escalate(confidence, urgency):

    if confidence < 0.70:
        return True

    if urgency == "high":
        return True

    return False