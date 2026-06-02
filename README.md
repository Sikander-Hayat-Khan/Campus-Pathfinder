# Campus Pathfinder

Campus Pathfinder is an AI-powered student support triage agent designed to streamline university helpdesks and student services by automating the initial intake and triage workflow. Built with Streamlit and powered by Groq LLMs (Llama 3), it drastically reduces manual administrative ticketing overhead while ensuring critical student issues are handled promptly.

## 🚀 Features

- **Automated Issue Classification**: Uses LLMs to categorize student requests into predefined buckets (`login_issue`, `registration_issue`, `fee_issue`, `exam_issue`, `other`).
- **Urgency Detection**: Automatically scores the urgency of a request (`low`, `medium`, `high`) based on the context (e.g., an exam starting in 10 minutes).
- **Smart Follow-ups**: Detects missing fields depending on the issue category (e.g., a fee issue requires a student ID and an amount) and autonomously prompts the user to provide them before finalizing the ticket.
- **Intelligent Routing & Escalation**: Maps issues directly to the concerned department (IT, Registrar, Finance, Examination). Escalates tickets requiring human review based on confidence scores or high urgency.
- **Drafts & Summaries**: Automatically generates a concise briefing of the ticket and drafts a professional response email for the support staff.

## 📁 Project Structure

```text
Campus_Pathfinder/
├── Core/                  # Business logic (deterministic)
│   ├── memory.py          # State/memory management definitions
│   ├── router.py          # Escalation and routing logic
│   ├── missing_fields.py  # Validation for missing ticket fields
│   └── required_fields.py # Constants for required inputs per category
│
├── LLM/                   # AI Agent logic and integrations
│   ├── classifier.py      # Category and confidence prediction
│   ├── urgency.py         # Urgency detection agent
│   ├── summary.py         # Ticket summary agent
│   ├── email_generator.py # Agent to generate support emails
│   ├── question_generator.py # Prompts for missing fields
│   └── prompts.py         # Centralized prompt templates
│
├── app.py                 # Main Streamlit web application
├── database.py            # SQLite database initialization and queries
├── test_workflow.py       # E2E pipeline test script
├── writeup.md             # Project write-up and FAQs
├── requirements.txt       # Project dependencies
└── tickets.db             # Local SQLite database
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sikander-Hayat-Khan/Campus-Pathfinder.git
   cd Campus-Pathfinder
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the Application:**
   ```bash
   python -m streamlit run app.py
   ```
   Open your browser to `http://localhost:8501`.

## 🧠 Workflows

1. **Phase 1: Initial Request** - Student submits a description of their issue.
2. **Phase 2: Missing Information** - Agent requests follow-ups if strictly required constraints aren't met.
3. **Phase 3: Processing** - Generates Urgency, routes to department, decides on escalation, creates summaries and emails.
4. **Phase 4: Save** - Writes to the `tickets.db` database.