import streamlit as st
import json
from classifier import classify_request
from urgency import determine_urgency
from router import should_escalate, route
from database import init_db, save_ticket

# Initialize database
init_db()

# Page title
st.title("Campus Pathfinder - Student Support Triage Agent")

# User input
request = st.text_area("Describe your issue")

# Submit button
if st.button("Submit"):

    # Validate input
    if not request.strip():
        st.error("Please describe your issue before submitting.")

    else:
        st.write("Analyzing...")

        # Classification Agent
        classification_response = classify_request(request)

        classification = json.loads(classification_response)

        # Urgency Agent
        urgency_response = determine_urgency(request)

        urgency = json.loads(urgency_response)

        # Escalation Decision
        escalate = should_escalate(classification["confidence"], urgency["urgency"])

        # Routing Decision
        department = route(classification["category"])

        # Ticket Status
        status = ("Escalated" if escalate else "Auto Routed")

        # Save Ticket
        save_ticket(request, classification["category"], urgency["urgency"], status)

        # Display Results
        st.success("Ticket Created Successfully")

        st.write("Category:", classification["category"])

        st.write("Confidence:", classification["confidence"])

        st.write("Urgency:", urgency["urgency"])

        st.write("Department:", department)

        st.write("Status:", status)