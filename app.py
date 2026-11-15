
import random
import streamlit as st
from datetime import datetime

# Import the existing QuizForge question bank and functions
from main import (
    question_bank,
    SCORE_FILE,
    CORRECT_MARKS,
    WRONG_MARKS,
    load_results,
    save_results
)

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="QuizForge",
    page_icon="📝",
    layout="wide"
)

st.title("📝 QuizForge")
st.subheader("Randomised Assessment and Leaderboard Engine")

st.write(
    "Practice placement-related questions, "
    "test your knowledge and track your performance."
)

st.divider()

# ==========================================
# 2. INITIALISE SESSION STATE
# ==========================================

defaults = {
    "quiz_active": False,
    "quiz_completed": False,
    "quiz_questions": [],
    "remaining_questions": [],
    "current_question": 0,
    "review": [],
    "score": 0,
    "correct": 0,
    "incorrect": 0,
    "unanswered": 0,
    "student_name": "",
    "selected_topic": "",
    "quiz_mode": "Normal",
    "current_level": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# 3. GET AVAILABLE TOPICS
# ==========================================

topics = sorted(set(q["topic"] for q in question_bank))


# ==========================================
# 4. ADAPTIVE QUESTION SELECTION
# ==========================================

difficulty_levels = ["Easy", "Medium", "Hard"]


def select_adaptive_question(remaining, target_level):

    target = difficulty_levels[target_level]

    matching = [
        q for q in remaining
        if q["difficulty"] == target
    ]

    if matching:
        return random.choice(matching)

    nearest_distance = min(
        abs(
            difficulty_levels.index(q["difficulty"])
            - target_level
        )
        for q in remaining
    )

    nearest = [
        q for q in remaining
        if abs(
            difficulty_levels.index(q["difficulty"])
            - target_level
        ) == nearest_distance
    ]

    return random.choice(nearest)


# ==========================================
# 5. START QUIZ
# ==========================================

def start_quiz(name, topic, count, mode):

    available = [
        q for q in question_bank
        if q["topic"] == topic
    ]

    st.session_state.student_name = name
    st.session_state.selected_topic = topic
    st.session_state.quiz_mode = mode

    st.session_state.review = []
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.incorrect = 0
    st.session_state.unanswered = 0
    st.session_state.current_question = 0

    if mode == "Normal":

        selected = random.sample(available, count)

        st.session_state.quiz_questions = selected
        st.session_state.remaining_questions = []

    else:

        remaining = available.copy()

        first = random.choice(remaining)
        remaining.remove(first)

        st.session_state.quiz_questions = [first]
        st.session_state.remaining_questions = remaining

        st.session_state.current_level = (
            difficulty_levels.index(first["difficulty"])
        )

    st.session_state.quiz_active = True
    st.session_state.quiz_completed = False


# ==========================================
# 6. SAVE FINAL RESULT
# ==========================================

def finish_quiz():

    review = st.session_state.review

    count = len(review)

    score = st.session_state.score

    maximum_marks = count * CORRECT_MARKS

    percentage = (score / maximum_marks) * 100

    accuracy = (
        st.session_state.correct / count
    ) * 100

    result = {
        "name": st.session_state.student_name,
        "topic": st.session_state.selected_topic,
        "mode": st.session_state.quiz_mode,
        "score": score,
        "total_questions": count,
        "correct": st.session_state.correct,
        "incorrect": st.session_state.incorrect,
        "unanswered": st.session_state.unanswered,
        "percentage": round(percentage, 2),
        "accuracy": round(accuracy, 2),
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    results = load_results()
    results.append(result)
    save_results(results)

    st.session_state.quiz_completed = True
    st.session_state.quiz_active = False


# ==========================================
# 7. PROCESS ANSWER
# ==========================================

def submit_answer(answer):

    index = st.session_state.current_question

    q = st.session_state.quiz_questions[index]

    if answer == "Skip":

        status = "Unanswered"
        marks = 0
        selected_text = "Not answered"

        st.session_state.unanswered += 1

    else:

        selected_option = answer[0]

        selected_text = q["options"][selected_option]

        if selected_option == q["answer"]:

            status = "Correct"
            marks = CORRECT_MARKS

            st.session_state.correct += 1
            st.session_state.score += marks

        else:

            status = "Incorrect"
            marks = -WRONG_MARKS

            st.session_state.incorrect += 1
            st.session_state.score += marks

    # Store answer review

    st.session_state.review.append({

        "question": q["question"],
        "selected_answer": selected_text,
        "correct_answer": q["options"][q["answer"]],
        "status": status,
        "marks": marks,
        "difficulty": q["difficulty"]

    })

    # Update difficulty in adaptive mode

    if st.session_state.quiz_mode == "Adaptive":

        if status == "Correct":

            st.session_state.current_level = min(
                st.session_state.current_level + 1,
                2
            )

        elif status == "Incorrect":

            st.session_state.current_level = max(
                st.session_state.current_level - 1,
                0
            )

    # Move to next question

    if index + 1 < len(st.session_state.quiz_questions):

        st.session_state.current_question += 1

        if st.session_state.quiz_mode == "Adaptive":

            remaining = st.session_state.remaining_questions

            next_question = select_adaptive_question(
                remaining,
                st.session_state.current_level
            )

            remaining.remove(next_question)

            st.session_state.quiz_questions.append(
                next_question
            )

    else:

        finish_quiz()


# ==========================================
# 8. NAVIGATION
# ==========================================

quiz_tab, bank_tab, leaderboard_tab, results_tab, report_tab = st.tabs([
    "🎯 Take Quiz",
    "📚 Question Bank",
    "🏆 Leaderboard",
    "📊 My Results",
    "📈 Performance Report"
])


# ==========================================
# 9. QUIZ SECTION
# ==========================================

with quiz_tab:

    st.header("Start Your Quiz")

    if not st.session_state.quiz_active and not st.session_state.quiz_completed:

        with st.form("quiz_setup"):

            name = st.text_input("Enter your name")

            topic = st.selectbox(
                "Select a topic",
                topics
            )

            available_count = sum(
                1 for q in question_bank
                if q["topic"] == topic
            )

            count = st.number_input(
                "Number of questions",
                min_value=1,
                max_value=available_count,
                value=min(5, available_count)
            )

            mode = st.radio(
                "Select quiz mode",
                ["Normal", "Adaptive"],
                horizontal=True
            )

            start_button = st.form_submit_button(
                "Start Quiz",
                use_container_width=True
            )

        if start_button:

            if not name.strip():

                st.error("Please enter your name.")

            else:

                start_quiz(
                    name.strip(),
                    topic,
                    int(count),
                    mode
                )

                st.rerun()

    # Display active quiz

    if st.session_state.quiz_active:

        index = st.session_state.current_question

        total = len(st.session_state.quiz_questions)

        q = st.session_state.quiz_questions[index]

        st.progress((index + 1) / total)

        st.write(
            f"Question {index + 1} of {total}"
        )

        st.caption(
            f"Topic: {st.session_state.selected_topic} | "
            f"Mode: {st.session_state.quiz_mode}"
        )

        st.info(
            f"Difficulty: {q['difficulty']}"
        )

        st.subheader(q["question"])

        choices = [
            f"{letter}. {option}"
            for letter, option in q["options"].items()
        ]

        answer = st.radio(
            "Choose your answer:",
            choices + ["Skip"],
            key=f"answer_{index}"
        )

        if st.button(
            "Submit Answer",
            use_container_width=True
        ):

            submit_answer(answer)
            st.rerun()

    # Display final score

    if st.session_state.quiz_completed:

        st.success("Quiz completed successfully!")

        count = len(st.session_state.review)

        maximum_marks = count * CORRECT_MARKS

        percentage = (
            st.session_state.score / maximum_marks
        ) * 100

        accuracy = (
            st.session_state.correct / count
        ) * 100

        st.subheader("Your Final Result")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Score",
            f"{st.session_state.score}/{maximum_marks}"
        )

        col2.metric(
            "Score Percentage",
            f"{percentage:.2f}%"
        )

        col3.metric(
            "Accuracy",
            f"{accuracy:.2f}%"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Correct", st.session_state.correct)
        col2.metric("Incorrect", st.session_state.incorrect)
        col3.metric("Skipped", st.session_state.unanswered)

        st.divider()

        st.subheader("Answer Review")

        for i, item in enumerate(st.session_state.review, 1):

            with st.expander(f"Question {i}: {item['status']}"):

                st.write(item["question"])

                st.write(
                    "Your answer:",
                    item["selected_answer"]
                )

                st.write(
                    "Correct answer:",
                    item["correct_answer"]
                )

                st.write(
                    "Difficulty:",
                    item["difficulty"]
                )

                st.write(
                    "Marks:",
                    item["marks"]
                )

        if st.button("Start Another Quiz"):

            st.session_state.quiz_completed = False
            st.session_state.quiz_active = False

            st.rerun()


# ==========================================
# 10. QUESTION BANK
# ==========================================

with bank_tab:

    st.header("Question Bank")

    selected_topic = st.selectbox(
        "Choose a topic to explore",
        ["All Topics"] + topics,
        key="bank_topic"
    )

    if selected_topic == "All Topics":

        filtered_questions = question_bank

    else:

        filtered_questions = [
            q for q in question_bank
            if q["topic"] == selected_topic
        ]

    st.write(
        f"Total questions: {len(filtered_questions)}"
    )

    for q in filtered_questions:

        with st.expander(
            f"Q{q['id']}. {q['question']}"
        ):

            st.write("Topic:", q["topic"])
            st.write("Difficulty:", q["difficulty"])

            for letter, option in q["options"].items():

                st.write(f"{letter}. {option}")


# ==========================================
# 11. LEADERBOARD
# ==========================================

with leaderboard_tab:

    st.header("🏆 Topic-wise Leaderboard")

    selected_topic = st.selectbox(
        "Select topic",
        topics,
        key="leaderboard_topic"
    )

    results = load_results()

    topic_results = [
        r for r in results
        if r["topic"] == selected_topic
    ]

    topic_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    if topic_results:

        st.dataframe(
            [
                {
                    "Rank": i,
                    "Name": r["name"],
                    "Score": r["score"],
                    "Questions": r["total_questions"],
                    "Mode": r.get("mode", "Normal")
                }
                for i, r in enumerate(topic_results[:5], 1)
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No scores available for this topic yet.")


# ==========================================
# 12. STUDENT RESULTS
# ==========================================

with results_tab:

    st.header("My Quiz Results")

    student_name = st.text_input(
        "Enter student name",
        key="results_name"
    )

    if st.button("View My Results"):

        results = load_results()

        student_results = [
            r for r in results
            if r["name"].strip().casefold()
            == student_name.strip().casefold()
        ]

        if not student_name.strip():

            st.warning("Please enter your name.")

        elif student_results:

            st.success(
                f"Found {len(student_results)} quiz attempts."
            )

            st.dataframe(
                student_results,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("No results found.")


# ==========================================
# 13. TOPIC-WISE PERFORMANCE REPORT
# ==========================================

with report_tab:

    st.header("Topic-wise Performance Report")

    student_name = st.text_input(
        "Enter student name",
        key="report_name"
    )

    if st.button("Generate Report"):

        results = load_results()

        student_results = [
            r for r in results
            if r["name"].strip().casefold()
            == student_name.strip().casefold()
        ]

        if not student_name.strip():

            st.warning("Please enter your name.")

        elif not student_results:

            st.warning("No results found for this student.")

        else:

            performance = {}

            for result in student_results:

                topic = result["topic"]

                if topic not in performance:

                    performance[topic] = {
                        "Attempts": 0,
                        "Questions": 0,
                        "Correct": 0,
                        "Incorrect": 0,
                        "Unanswered": 0,
                        "Score": 0
                    }

                data = performance[topic]

                data["Attempts"] += 1
                data["Questions"] += result["total_questions"]
                data["Correct"] += result["correct"]
                data["Incorrect"] += result["incorrect"]
                data["Unanswered"] += result["unanswered"]
                data["Score"] += result["score"]

            for topic, data in performance.items():

                accuracy = (
                    data["Correct"] / data["Questions"]
                ) * 100

                percentage = (
                    data["Score"] /
                    (data["Questions"] * CORRECT_MARKS)
                ) * 100

                st.subheader(topic)

                col1, col2, col3 = st.columns(3)

                col1.metric("Attempts", data["Attempts"])

                col2.metric(
                    "Correct Answers",
                    data["Correct"]
                )

                col3.metric(
                    "Accuracy",
                    f"{accuracy:.2f}%"
                )

                st.write(
                    f"Score: {data['Score']} / "
                    f"{data['Questions'] * CORRECT_MARKS}"
                )

                st.write(
                    f"Score Percentage: {percentage:.2f}%"
                )

                st.divider()


# ==========================================
# END OF QUIZFORGE STREAMLIT APPLICATION
# ==========================================

st.caption("QuizForge | Randomised Assessment Engine")
