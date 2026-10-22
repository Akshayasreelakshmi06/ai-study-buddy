import os
import json

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
)

# ---------- MIDNIGHT INDIGO THEME ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0B1020, #11172B, #17152F);
        color: #F1F5F9;
    }
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stSidebar"] {
        background: #0D1325;
        border-right: 1px solid #28304A;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }
    h1, h2, h3 {
        color: #F8FAFC !important;
    }
    p, label, .stMarkdown {
        color: #D7DEEE;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #151D33 !important;
        color: #F8FAFC !important;
        border: 1px solid #394466 !important;
        border-radius: 10px !important;
    }
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1.1rem;
        font-weight: 600;
    }
    [data-testid="stExpander"], [data-testid="stForm"] {
        background: #182038;
        border: 1px solid #303B5C;
        border-radius: 14px;
    }
    hr {
        border-color: #303B5C;
    }
    a {
        color: #A5B4FC !important;
    }
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- API SETUP ----------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL = "gemini-3.5-flash-lite"


# ---------- STUDY PROGRESS TRACKING ----------
if "topics_studied" not in st.session_state:
    st.session_state.topics_studied = []

if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []

if "notes_created_count" not in st.session_state:
    st.session_state.notes_created_count = 0

if "flashcards_reviewed" not in st.session_state:
    st.session_state.flashcards_reviewed = 0


# ---------- SESSION STATE ----------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "study_notes" not in st.session_state:
    st.session_state.study_notes = ""

if "notes_topic" not in st.session_state:
    st.session_state.notes_topic = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("📚 Study Buddy")
    st.caption("Your personal AI learning space")
    st.divider()

    
    page = st.radio(
    "NAVIGATION",
    [   
        "📊 Study Progress",
        "🏠 Home",
        "💡 Explain a Topic",
        "📝 Study Notes",
        "🎯 Take a Quiz",
        "🃏 Revision Flashcards",
        "📅 Personal Study Planner",
        "💬 Chat with AI",
    ],
)

    st.divider()
    st.caption("Learn something new every day ✨")

# ---------- HEADER ----------
st.markdown(
    """
    <div style="
        background: linear-gradient(120deg, #252B50, #433078, #252B50);
        padding: 18px 24px;
        border-radius: 16px;
        border: 1px solid #393B68;
        margin-bottom: 24px;
    ">
        <h1 style="color: #FFFFFF; margin: 0;">📚 AI Study Buddy</h1>
        <p style="color: #E0E7FF; margin: 8px 0 0 0;">
            Your learning companion for explanations, revision notes,
            quizzes, and AI-powered conversations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


def generate_text(prompt):
    """Send a prompt to Gemini and return its response."""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    if not response.text:
        raise ValueError("The AI returned an empty response.")

    return response.text.strip()


def show_error(error):
    st.error("Something went wrong. Please try again.")
    st.caption(f"Technical details: {error}")
    
def record_topic(topic):
    """Save a topic once in the current session."""
    topic = topic.strip()
    if topic and topic not in st.session_state.topics_studied:
        st.session_state.topics_studied.append(topic)


def update_flashcard_review_count():
    """Count flashcards marked as reviewed."""
    st.session_state.flashcards_reviewed = sum(
        1
        for key in st.session_state
        if key.startswith("flashcard_reviewed_")
        and st.session_state[key] is True
    )



# ---------- HOME ----------
if page == "🏠 Home":
    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #252B50, #433078, #252B50);
            padding: 28px;
            border-radius: 18px;
            border: 1px solid #55518B;
            margin-bottom: 12px;
        ">
            <p style="color: #C4B5FD; font-size: 13px; margin-bottom: 8px;">
                ✦ YOUR PERSONAL AI LEARNING SPACE
            </p>
            <h1 style="color: #FFFFFF; margin: 0;">
                Welcome to AI Study Buddy 👋
            </h1>
            <p style="color: #E0E7FF; font-size: 17px; margin-top: 12px;">
                Learn smarter, revise faster, and feel confident in every subject.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("✨ What would you like to learn today?")

    col1, col2 = st.columns(2)

    with col1:
        st.info("💡 **Understand concepts**\n\nLearn difficult topics in simple language.")
        st.info("📝 **Create revision notes**\n\nGenerate organized notes for studying.")

    with col2:
        st.info("🎯 **Test your knowledge**\n\nPractice with a five-question quiz.")
        st.info("💬 **Ask questions**\n\nChat with AI to clear your doubts.")

    st.markdown("### Quick start")
    quick_topic = st.text_input(
        "Enter a topic to learn",
        placeholder="Example: Python functions",
        key="home_topic",
    )
    quick_level = st.selectbox(
        "Your learning level",
        ["Beginner", "Intermediate", "Advanced"],
        key="home_level",
    )

    if st.button("Explain my topic", type="primary"):
        if not quick_topic.strip():
            st.warning("Please enter a topic first.")
        else:
            try:
                with st.spinner("Preparing your explanation..."):
                    result = generate_text(
                        f"Explain {quick_topic} to a {quick_level} learner. "
                        "Use simple language, an example, and three key takeaways."
                    )
                st.markdown("### Your explanation")
                st.markdown(result)
                record_topic(quick_topic)
            except Exception as error:
                show_error(error)


# ---------- TOPIC EXPLAINER ----------
elif page == "💡 Explain a Topic":
    st.subheader("💡 AI Topic Explainer")
    topic = st.text_input(
        "What do you want to understand?",
        placeholder="Example: Machine learning",
        key="explain_topic",
    )
    level = st.selectbox(
        "Choose your level",
        ["Beginner", "Intermediate", "Advanced"],
        key="explain_level",
    )

    if st.button("Explain topic", type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            try:
                with st.spinner("Creating your explanation..."):
                    result = generate_text(
                        f"Explain {topic} to a {level} learner. "
                        "Use clear headings, simple language, a practical example, "
                        "and three key takeaways. Include code if relevant."
                    )
                st.markdown(result)
                record_topic(topic)
            except Exception as error:
                show_error(error)


# ---------- STUDY NOTES ----------
elif page == "📝 Study Notes":
    st.subheader("📝 Study Notes Generator")
    notes_topic = st.text_input(
        "Topic for your notes",
        placeholder="Example: Python lists",
        key="notes_topic_input",
    )
    notes_level = st.selectbox(
        "Choose your level",
        ["Beginner", "Intermediate", "Advanced"],
        key="notes_level",
    )
    notes_length = st.selectbox(
        "Notes length",
        ["Quick revision", "Detailed notes", "Exam preparation"],
        key="notes_length",
    )

    if st.button("Generate study notes", type="primary"):
        if not notes_topic.strip():
            st.warning("Please enter a topic.")
        else:
            prompt = f"""
Create {notes_length.lower()} about {notes_topic}
for a {notes_level} learner.

Include:
- A clear title
- Definition and important concepts
- Key points in bullet lists
- Examples where useful
- Common mistakes or misconceptions
- A short revision summary

For exam preparation, include likely questions to practise.
Use accurate information and easy-to-understand language.
"""
            try:
                with st.spinner("Preparing your study notes..."):
                    st.session_state.study_notes = generate_text(prompt)
                    st.session_state.notes_topic = notes_topic
                    st.session_state.notes_created_count += 1
                    record_topic(notes_topic)
            except Exception as error:
                show_error(error)

    if st.session_state.study_notes:
        st.divider()
        st.markdown(f"### Notes: {st.session_state.notes_topic or 'Your topic'}")
        st.markdown(st.session_state.study_notes)
        st.download_button(
            label="⬇️ Download study notes",
            data=st.session_state.study_notes,
            file_name="ai_study_notes.txt",
            mime="text/plain",
        )


# ---------- QUIZ ----------
elif page == "🎯 Take a Quiz":
    st.subheader("🎯 Test Your Knowledge")
    quiz_topic_input = st.text_input(
        "Quiz topic",
        placeholder="Example: Python loops",
        key="quiz_topic_input",
    )
    quiz_level = st.selectbox(
        "Quiz difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        key="quiz_level",
    )

    if st.button("Generate quiz", type="primary"):
        if not quiz_topic_input.strip():
            st.warning("Please enter a topic.")
        else:
            prompt = f"""
Create exactly 5 multiple-choice questions about {quiz_topic_input}
for a {quiz_level} learner.

Return ONLY a valid JSON array. Do not use Markdown fences.
Each item must contain:
"question": question text,
"options": an array of exactly 4 answer choices,
"answer": exact text of the correct option,
"explanation": a short explanation.

Every answer must exactly match one of its options.
"""
            try:
                with st.spinner("Generating your quiz..."):
                    raw_text = generate_text(prompt)

                if raw_text.startswith("```"):
                    raw_text = raw_text.removeprefix("```json")
                    raw_text = raw_text.removeprefix("```")
                    raw_text = raw_text.removesuffix("```").strip()

                questions = json.loads(raw_text)

                if not isinstance(questions, list) or len(questions) != 5:
                    raise ValueError("The AI did not return exactly five questions.")

                for question in questions:
                    if (
                        not isinstance(question, dict)
                        or not isinstance(question.get("options"), list)
                        or len(question["options"]) != 4
                        or question.get("answer") not in question["options"]
                    ):
                        raise ValueError("A quiz question has an invalid format.")

                st.session_state.quiz = questions
                st.session_state.quiz_topic = quiz_topic_input
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []

            except json.JSONDecodeError:
                st.error("The AI returned an invalid quiz format. Please try again.")
            except Exception as error:
                show_error(error)

    if st.session_state.quiz:
        st.markdown(f"### Quiz: {st.session_state.quiz_topic}")

        with st.form("quiz_form"):
            answers = []

            for i, question in enumerate(st.session_state.quiz):
                st.markdown(f"**Q{i + 1}. {question['question']}**")
                selected = st.radio(
                    "Choose one answer",
                    question["options"],
                    index=None,
                    key=f"answer_{i}",
                )
                answers.append((question, selected))

            submitted = st.form_submit_button("Submit answers")

        if submitted:
            score = sum(
                1 for question, selected in answers
                if selected == question["answer"]
            )
            st.session_state.quiz_submitted = True
            st.session_state.quiz_score = score
            st.session_state.quiz_history.append({
                "topic": st.session_state.quiz_topic,
                "score": score,
                "total": len(st.session_state.quiz),
            })
            record_topic(st.session_state.quiz_topic)
            st.session_state.quiz_answers = [
                selected for question, selected in answers
            ]

        if st.session_state.get("quiz_submitted", False):
            score = st.session_state.quiz_score
            st.subheader(f"🏆 Your score: {score}/5")

            for i, question in enumerate(st.session_state.quiz):
                selected = st.session_state.quiz_answers[i]
                if selected == question["answer"]:
                    st.success(f"Q{i + 1}: Correct!")
                else:
                    st.error(f"Q{i + 1}: Incorrect or unanswered.")

                st.write(f"**Correct answer:** {question['answer']}")
                st.write(f"**Explanation:** {question['explanation']}")



# ---------- REVISION FLASHCARDS ----------
elif page == "🃏 Revision Flashcards":
    st.subheader("🃏 AI Revision Flashcards")
    st.write("Turn any topic into quick question-and-answer cards for revision.")

    topic = st.text_input(
        "Enter your topic",
        placeholder="e.g. Python functions, DBMS, Computer Networks",
        key="flashcard_topic",
    )

    number_of_cards = st.selectbox(
        "Number of flashcards",
        [5, 10, 15],
        key="flashcard_count",
    )

    if st.button("✨ Generate Flashcards"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            prompt = f"""
Create exactly {number_of_cards} useful revision flashcards
for the topic: {topic}

The learner is a college student.
Keep answers accurate, clear, and easy to revise.
Each card must contain one question and its answer.

Return ONLY a valid JSON array in this format:
[
  {{"question": "What is ...?", "answer": "..."}},
  {{"question": "Why is ...?", "answer": "..."}}
]

Do not include Markdown code fences or extra text.
"""
            try:
                import json

                with st.spinner("Creating your flashcards..."):
                    response = generate_text(prompt)

                cleaned_response = response.strip()
                if cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response.split("\n", 1)[1]
                    if cleaned_response.rstrip().endswith("```"):
                        cleaned_response = cleaned_response.rstrip()[:-3].strip()

                cards = json.loads(cleaned_response)

                if not isinstance(cards, list) or not cards:
                    st.error("The AI returned an unexpected format. Please try again.")
                elif not all(
                    isinstance(card, dict)
                    and "question" in card
                    and "answer" in card
                    for card in cards
                ):
                    st.error("Some flashcards were incomplete. Please try again.")
                else:
                    for key in list(st.session_state.keys()):
                        if key.startswith("flashcard_reviewed_"):
                            del st.session_state[key]
                    st.session_state.flashcards_reviewed = 0
                    st.session_state.flashcards = cards
                    st.success(f"Generated {len(cards)} flashcards!")

            except Exception as error:
                st.error("Couldn't generate flashcards. Please try again.")
                st.caption(f"Technical details: {error}")

    if st.session_state.get("flashcards"):
        st.markdown("### Your revision cards")

        
        for index, card in enumerate(st.session_state.flashcards, start=1):
            with st.expander(f"Card {index}: {card['question']}"):
                st.markdown("**Answer**")
                st.write(card["answer"])

                st.checkbox(
                    "Mark as reviewed",
                    key=f"flashcard_reviewed_{index}",
                    on_change=update_flashcard_review_count,
                )


        flashcard_text = "\n\n".join(
            f"Card {index}\nQuestion: {card['question']}\nAnswer: {card['answer']}"
            for index, card in enumerate(st.session_state.flashcards, start=1)
        )

        st.download_button(
            "⬇️ Download Flashcards",
            data=flashcard_text,
            file_name="revision_flashcards.txt",
            mime="text/plain",
        )


# ---------- PERSONAL STUDY PLANNER ----------
elif page == "📅 Personal Study Planner":
    st.subheader("📅 Personal Study Planner")
    st.write("Create a study timetable based on your exam and available time.")

    subjects = st.text_area(
        "Enter your subjects and topics",
        placeholder="Python: Functions, OOP\nDBMS: SQL, Normalization\nDAA: Sorting, Graphs",
        key="planner_subjects",
    )

    exam_date = st.date_input(
        "Exam date",
        min_value=__import__("datetime").date.today(),
        key="planner_exam_date",
    )

    daily_hours = st.slider(
        "Available study hours per day",
        min_value=1,
        max_value=12,
        value=3,
        key="planner_daily_hours",
    )

    study_style = st.selectbox(
        "Study preference",
        [
            "Balanced study",
            "Focus on difficult subjects",
            "Revision and practice",
        ],
        key="planner_study_style",
    )

    if st.button("✨ Generate My Study Plan", type="primary"):
        if not subjects.strip():
            st.warning("Please enter your subjects first.")
        else:
            prompt = f"""
Create a realistic study timetable for a college student.

Subjects and topics:
{subjects}

Exam date: {exam_date}
Available hours per day: {daily_hours}
Study preference: {study_style}

Instructions:
- Calculate the days remaining until the exam.
- Make a day-by-day timetable.
- Distribute time across the listed subjects.
- Include short breaks, practice questions, and revision.
- Keep the daily workload within the available study hours.
- Use clear headings and a readable table.
- Do not invent additional subjects.
"""

            try:
                with st.spinner("Creating your study plan..."):
                    plan = generate_text(prompt)

                st.session_state["personal_study_plan"] = plan

            except Exception as error:
                show_error(error)

    if st.session_state.get("personal_study_plan"):
        st.markdown("### 📚 Your Study Timetable")
        st.markdown(st.session_state["personal_study_plan"])

        st.download_button(
            "⬇️ Download Study Plan",
            data=st.session_state["personal_study_plan"],
            file_name="personal_study_plan.txt",
            mime="text/plain",
        )


# ---------- STUDY PROGRESS DASHBOARD ----------
elif page == "📊 Study Progress":
    st.subheader("📊 Your Study Progress")
    st.write("Track your learning activity in this session.")

    topics = st.session_state.topics_studied
    quiz_history = st.session_state.quiz_history

    total_quizzes = len(quiz_history)
    average_score = (
        sum(item["score"] / item["total"] * 100 for item in quiz_history)
        / total_quizzes
        if total_quizzes else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("📚 Topics studied", len(set(topics)))
    col2.metric("🎯 Quizzes completed", total_quizzes)
    col3.metric("🏆 Average quiz score", f"{average_score:.1f}%")

    st.divider()

    st.markdown("### 📖 Topics you've studied")
    if topics:
        for topic in sorted(set(topics)):
            st.write(f"• {topic}")
    else:
        st.info("Your studied topics will appear here as tracking is added.")

    st.markdown("### 🎯 Quiz performance")
    if quiz_history:
        for index, item in enumerate(quiz_history, start=1):
            percentage = item["score"] / item["total"] * 100
            st.write(
                f"**{index}. {item['topic']}** — "
                f"{item['score']}/{item['total']} ({percentage:.0f}%)"
            )
            st.progress(percentage / 100)
    else:
        st.info("Complete a quiz to start building your performance history.")

    st.divider()

    st.markdown("### 📝 Other learning activity")
    col1, col2 = st.columns(2)
    col1.metric(
        "Notes generated",
        st.session_state.notes_created_count
    )
    col2.metric(
        "Flashcards reviewed",
        st.session_state.flashcards_reviewed
    )
