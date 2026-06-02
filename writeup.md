# Campus Pathfinder: Project Write-up

# Streamlit App:
https://campus-pathfinder.streamlit.app/

# Github Repo Link:
https://github.com/Sikander-Hayat-Khan/Campus-Pathfinder.git

### Why this problem? What made you pick it? How did you discover it was worth solving?
University administrations are consistently overwhelmed by a massive influx of student support queries, ranging from simple password resets to critical registration roadblocks and deadline-driven fee issues. I noticed that manual sorting and routing of these tickets take administrative staff days to clear out, frustrating students—especially during high-stress periods like exam weeks or course enrollment windows. It was worth solving because response delays directly impact students' academic activities, and a large portion of the workload involves routing simple, structured data.

### Who is the user?
There are two primary personas:
1. **The Student (End-User):** Needs a quick, efficient way to report an issue without worrying about "who" they need to contact. 
2. **University Support Staff (Admin):** Receives triaged, properly categorized tickets that include generated summaries and drafted email responses, saving them manual processing time.

### Architecture: How does the agent work? What decisions does it make autonomously?
The app uses a hybrid architecture blending deterministic routing with LLM-powered context extraction (via Groq/Llama).
- **Classification Generation:** A custom LLM prompt evaluates the student’s natural language input, locking it cleanly into predefined categories while assigning a confidence score.
- **State Machine / Feedback Loop:** The application evaluates the extracted category against a database of required fields. If data is missing (e.g. no student ID for a fee issue), it halts and asks the user contextual follow-up questions autonomously to populate the missing data cache.
- **Urgency Generation:** Contextual cues (e.g. "My exam is in 10 minutes") are parsed by another LLM step to classify the priority as low, medium, or high.
- **Final Output:** The system synthesizes the memory dict into a formatted summary and an automated email draft that support staff can send with one click.

### What does it escalate?
The routing engine evaluates tickets and flags them as `Escalated` (meaning they require immediate human review) under two conditions:
1. **High Urgency:** The LLM detects an explicitly urgent timeline (e.g. an exam starting shortly).
2. **Low Confidence (< 70%):** The LLM isn't completely confident about its classification, ensuring confusing or complex edge cases aren't misrouted into auto-queues.
Everything else gets standard `Auto Routed` status.

### What did you learn?
1. **Prompt Engineering & Enforced Schemas:** Simply asking an LLM for classification isn't enough; it must be explicitly restricted to valid categories in the prompt text, and its response heavily sanitized before JSON parsing to avoid edge-case hallucinations. 
2. **State Management in Streamlit:** Storing memory states across user-interaction reruns (`st.session_state`) was critical to achieving multi-turn interactions (asking for missing fields before finalizing the ticket). 
3. **Decoupling Logic:** Separating the application strictly into a `Core/` logical package and an `LLM/` agent package greatly simplified unit testing and iteration, avoiding a massive, unmaintainable root script.
