import streamlit as st
import json

from LLM.classifier import classify_request
from LLM.urgency import determine_urgency
from Core.router import should_escalate, route

from database import (init_db, save_ticket)

from Core.memory import initialize_memory
from Core.missing_fields import find_missing_fields
from LLM.question_generator import get_question

from LLM.summary import generate_summary
from LLM.email_generator import generate_email

# Session State Initialization

if "memory" not in st.session_state:
    st.session_state.memory = initialize_memory()

if "current_field" not in st.session_state:
    st.session_state.current_field = None

if "original_request" not in st.session_state:
    st.session_state.original_request = None

if "ticket_completed" not in st.session_state:
    st.session_state.ticket_completed = False

# Database Initialization

init_db()

# UI

st.title("Campus Pathfinder - Student Support Triage Agent")

# PHASE 1 - INITIAL REQUEST

if st.session_state.current_field is None and not st.session_state.ticket_completed:
    request = st.text_area("Describe your issue")

    if st.button("Submit Request"):

        if not request.strip():
            st.error("Please describe your issue before submitting.")

        else:
            st.session_state.original_request = request

            try:
                classification_response = classify_request(request)

                classification = json.loads(classification_response)

            except Exception as e:
                st.error(f"Classification failed: {e}")
                st.stop()

            st.session_state.memory["category"] = classification["category"]

            st.session_state.memory["confidence"] = classification["confidence"]

            # category = classification["category"]

            # st.session_state.memory["category"] = category

            missing = find_missing_fields(classification["category"],st.session_state.memory)

            if missing:
                st.session_state.current_field = missing[0]
                st.rerun()

            else:
                st.session_state.current_field = "PROCESS_TICKET"
                st.rerun()

# PHASE 2 - COLLECT MISSING INFORMATION

elif (st.session_state.current_field and st.session_state.current_field != "PROCESS_TICKET"):
    field = st.session_state.current_field

    st.warning(get_question(field))

    answer = st.text_input("Your Response")

    if st.button("Submit Information"):
        if not answer.strip():
            st.error("Please provide the requested information.")

        else:
            st.session_state.memory[field] = answer
            missing = find_missing_fields(st.session_state.memory["category"], st.session_state.memory)

            if missing:
                st.session_state.current_field = missing[0]

            else:
                st.session_state.current_field = "PROCESS_TICKET"
            st.rerun()

# PHASE 3 - PROCESS TICKET

elif st.session_state.current_field == "PROCESS_TICKET":
    request = st.session_state.original_request

    try:
        urgency_response = determine_urgency(request)

        urgency = json.loads(urgency_response)

    except Exception as e:
        st.error(f"Urgency determination failed: {e}")
        st.stop()
    
    category = st.session_state.memory["category"] 
    
    confidence = st.session_state.memory["confidence"]

    # confidence = 0.90

    # category = st.session_state.memory["category"]

    department = route(category)

    escalate = should_escalate(confidence, urgency["urgency"])

    status = ("Escalated" if escalate else "Auto Routed")

    summary = generate_summary(st.session_state.memory)

    email = generate_email(department, summary)

    save_ticket(request, category, urgency["urgency"], confidence, department, summary, email, status)

    st.success("Ticket Created Successfully")

    st.write("Category:", category)

    st.write("Urgency:", urgency["urgency"])

    st.write("Department:", department)

    st.write("Status:", status)

    st.subheader("Generated Ticket Summary")

    st.write(summary)

    st.subheader("Generated Email Draft")

    st.write(email)

    if escalate: 
        st.warning( "This ticket has been escalated for human review." )

    st.session_state.ticket_completed = True

# PHASE 4 - RESET

if st.session_state.ticket_completed:
    st.divider()

    if st.button("Create New Ticket"):
        st.session_state.memory = initialize_memory()

        st.session_state.current_field = None

        st.session_state.original_request = None

        st.session_state.ticket_completed = False

        st.rerun()