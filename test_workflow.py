import json
from LLM.classifier import classify_request
from LLM.urgency import determine_urgency
from Core.router import should_escalate, route
from Core.memory import initialize_memory
from Core.missing_fields import find_missing_fields
from LLM.summary import generate_summary
from LLM.email_generator import generate_email

def test_workflow():
    print("="*50)
    print("🚀 TESTING CAMPUS PATHFINDER WORKFLOW 🚀")
    print("="*50)

    # 1. Test Classifier
    print("\n[1] Testing Classifier...")
    test_request = "I cannot log into the student portal and I forgot my password."
    print(f"Request: {test_request}")
    classification_response = classify_request(test_request)
    classification = json.loads(classification_response)
    print(f"Result: {classification}")

    # 2. Test Urgency
    print("\n[2] Testing Urgency...")
    urgency_response = determine_urgency(test_request)
    print("Raw urgency response:", repr(urgency_response))
    urgency = json.loads(urgency_response)
    print(f"Result: {urgency}")

    # 3. Test Router & Escalation
    print("\n[3] Testing Router & Escalation...")
    category = classification.get("category", "other")
    conf = classification.get("confidence", 0.0)
    urg = urgency.get("urgency", "low")
    
    escalate = should_escalate(conf, urg)
    department = route(category)
    print(f"Escalate: {escalate}")
    print(f"Department: {department}")

    # 4. Test Memory Components
    print("\n[4] Testing Memory Components...")
    memory = initialize_memory()
    memory["category"] = category
    memory["confidence"] = conf
    memory["urgency"] = urg
    # Simulating partially filled memory
    memory["student_id"] = "BSE-123"
    print(f"Memory initialized: {memory}")

    # 5. Test Missing Field Detection
    print("\n[5] Testing Missing Field Detection...")
    missing = find_missing_fields(category, memory)
    print(f"Missing Fields for '{category}': {missing}")

    # 6. Simulate fulfilling missing fields (e.g. through question agent)
    print("\n[.] Simulating user providing missing fields...")
    memory["error_message"] = "Invalid Password"
    missing_after = find_missing_fields(category, memory)
    print(f"Missing Fields now: {missing_after}")

    # 7. Test Summary Generator
    print("\n[6] Testing Summary Generator...")
    summary = generate_summary(memory)
    print(f"Generated Summary:\n{summary}\n")

    # 8. Test Email Generator
    print("\n[7] Testing Email Generator...")
    email = generate_email(department, summary)
    print(f"Generated Email:\n{email}\n")

    print("\n✅ Workflow test complete!")

if __name__ == "__main__":
    test_workflow()
