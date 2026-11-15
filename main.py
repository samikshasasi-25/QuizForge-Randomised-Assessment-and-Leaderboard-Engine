
import random
import json
import os
from datetime import datetime

# ==========================================
# QUIZFORGE - RANDOMISED ASSESSMENT ENGINE
# ==========================================

SCORE_FILE = "quizforge_scores.json"

CORRECT_MARKS = 4
WRONG_MARKS = 1

# ==========================================
# 1. QUESTION BANK
# ==========================================

question_bank = [

    # PYTHON
    {"id": 1, "question": "What is a Python list?",
     "options": {"A": "Loop", "B": "Collection", "C": "Function", "D": "Class"},
     "answer": "B", "topic": "Python", "difficulty": "Easy"},

    {"id": 2, "question": "Which keyword defines a function?",
     "options": {"A": "func", "B": "define", "C": "def", "D": "method"},
     "answer": "C", "topic": "Python", "difficulty": "Easy"},

    {"id": 3, "question": "Which data type stores key-value pairs?",
     "options": {"A": "List", "B": "Tuple", "C": "Dictionary", "D": "Set"},
     "answer": "C", "topic": "Python", "difficulty": "Medium"},

    {"id": 4, "question": "What is the output of 5 // 2?",
     "options": {"A": "2.5", "B": "2", "C": "3", "D": "1"},
     "answer": "B", "topic": "Python", "difficulty": "Medium"},

    {"id": 5, "question": "Which data type is immutable?",
     "options": {"A": "List", "B": "Dictionary", "C": "Set", "D": "Tuple"},
     "answer": "D", "topic": "Python", "difficulty": "Hard"},

    # JAVA
    {"id": 6, "question": "Which keyword creates an object in Java?",
     "options": {"A": "class", "B": "new", "C": "this", "D": "void"},
     "answer": "B", "topic": "Java", "difficulty": "Easy"},

    {"id": 7, "question": "Which method is the entry point of a Java program?",
     "options": {"A": "start()", "B": "run()", "C": "main()", "D": "init()"},
     "answer": "C", "topic": "Java", "difficulty": "Easy"},

    {"id": 8, "question": "Which data type stores true or false?",
     "options": {"A": "int", "B": "char", "C": "boolean", "D": "String"},
     "answer": "C", "topic": "Java", "difficulty": "Easy"},

    {"id": 9, "question": "Which keyword supports class inheritance?",
     "options": {"A": "extends", "B": "imports", "C": "package", "D": "static"},
     "answer": "A", "topic": "Java", "difficulty": "Medium"},

    {"id": 10, "question": "Java bytecode is executed by which component?",
     "options": {"A": "JVM", "B": "HTML", "C": "SQL", "D": "BIOS"},
     "answer": "A", "topic": "Java", "difficulty": "Hard"},

    # C PROGRAMMING
    {"id": 11, "question": "Which function displays output in C?",
     "options": {"A": "input()", "B": "print()", "C": "printf()", "D": "display()"},
     "answer": "C", "topic": "C Programming", "difficulty": "Easy"},

    {"id": 12, "question": "Which symbol terminates a C statement?",
     "options": {"A": ".", "B": ";", "C": ":", "D": ","},
     "answer": "B", "topic": "C Programming", "difficulty": "Easy"},

    {"id": 13, "question": "Which header file contains printf()?",
     "options": {"A": "stdlib.h", "B": "math.h", "C": "stdio.h", "D": "string.h"},
     "answer": "C", "topic": "C Programming", "difficulty": "Medium"},

    {"id": 14, "question": "Which loop executes at least once?",
     "options": {"A": "for", "B": "while", "C": "do-while", "D": "if"},
     "answer": "C", "topic": "C Programming", "difficulty": "Medium"},

    {"id": 15, "question": "Array indexing in C starts from?",
     "options": {"A": "0", "B": "1", "C": "-1", "D": "2"},
     "answer": "A", "topic": "C Programming", "difficulty": "Easy"},

    # DATA STRUCTURES
    {"id": 16, "question": "Which data structure follows FIFO?",
     "options": {"A": "Stack", "B": "Queue", "C": "Tree", "D": "Graph"},
     "answer": "B", "topic": "Data Structures", "difficulty": "Easy"},

    {"id": 17, "question": "Which data structure follows LIFO?",
     "options": {"A": "Queue", "B": "Array", "C": "Stack", "D": "Graph"},
     "answer": "C", "topic": "Data Structures", "difficulty": "Easy"},

    {"id": 18, "question": "Which structure consists of nodes and links?",
     "options": {"A": "Linked List", "B": "Integer", "C": "String", "D": "Float"},
     "answer": "A", "topic": "Data Structures", "difficulty": "Medium"},

    {"id": 19, "question": "Which structure represents hierarchical data?",
     "options": {"A": "Queue", "B": "Tree", "C": "Stack", "D": "Array"},
     "answer": "B", "topic": "Data Structures", "difficulty": "Medium"},

    {"id": 20, "question": "Which tree traversal visits the root first?",
     "options": {"A": "Inorder", "B": "Postorder", "C": "Preorder", "D": "None"},
     "answer": "C", "topic": "Data Structures", "difficulty": "Hard"},

    # ALGORITHMS
    {"id": 21, "question": "Which algorithm finds an element in a sorted array efficiently?",
     "options": {"A": "Linear Search", "B": "Binary Search", "C": "Bubble Sort", "D": "Selection Sort"},
     "answer": "B", "topic": "Algorithms", "difficulty": "Easy"},

    {"id": 22, "question": "Which sorting algorithm repeatedly swaps adjacent elements?",
     "options": {"A": "Bubble Sort", "B": "Merge Sort", "C": "Quick Sort", "D": "Heap Sort"},
     "answer": "A", "topic": "Algorithms", "difficulty": "Easy"},

    {"id": 23, "question": "What is the time complexity of linear search in the worst case?",
     "options": {"A": "O(1)", "B": "O(log n)", "C": "O(n)", "D": "O(n²)"},
     "answer": "C", "topic": "Algorithms", "difficulty": "Medium"},

    {"id": 24, "question": "Which algorithm uses divide and conquer?",
     "options": {"A": "Linear Search", "B": "Merge Sort", "C": "Bubble Sort", "D": "Insertion Sort"},
     "answer": "B", "topic": "Algorithms", "difficulty": "Medium"},

    {"id": 25, "question": "What is the average time complexity of Quick Sort?",
     "options": {"A": "O(n)", "B": "O(n log n)", "C": "O(n²)", "D": "O(1)"},
     "answer": "B", "topic": "Algorithms", "difficulty": "Hard"},

    # DBMS
    {"id": 26, "question": "Which SQL command retrieves data?",
     "options": {"A": "GET", "B": "OPEN", "C": "SELECT", "D": "UPDATE"},
     "answer": "C", "topic": "DBMS", "difficulty": "Easy"},

    {"id": 27, "question": "Which key uniquely identifies a row?",
     "options": {"A": "Foreign Key", "B": "Primary Key", "C": "Duplicate Key", "D": "Common Key"},
     "answer": "B", "topic": "DBMS", "difficulty": "Easy"},

    {"id": 28, "question": "What does DBMS stand for?",
     "options": {"A": "Database Management System", "B": "Data Backup Server", "C": "Digital Base System", "D": "Database Memory Service"},
     "answer": "A", "topic": "DBMS", "difficulty": "Medium"},

    {"id": 29, "question": "Which join returns matching rows from both tables?",
     "options": {"A": "INNER JOIN", "B": "CROSS JOIN", "C": "FULL JOIN", "D": "SELF JOIN"},
     "answer": "A", "topic": "DBMS", "difficulty": "Medium"},

    {"id": 30, "question": "Which normal form removes partial dependency?",
     "options": {"A": "1NF", "B": "2NF", "C": "3NF", "D": "BCNF"},
     "answer": "B", "topic": "DBMS", "difficulty": "Hard"},

    # OPERATING SYSTEMS
    {"id": 31, "question": "Which is an example of an operating system?",
     "options": {"A": "Python", "B": "Linux", "C": "MySQL", "D": "HTML"},
     "answer": "B", "topic": "Operating Systems", "difficulty": "Easy"},

    {"id": 32, "question": "Which part manages hardware resources?",
     "options": {"A": "Kernel", "B": "Browser", "C": "Compiler", "D": "Editor"},
     "answer": "A", "topic": "Operating Systems", "difficulty": "Easy"},

    {"id": 33, "question": "What is multitasking?",
     "options": {"A": "Running multiple tasks", "B": "Deleting files", "C": "Formatting disks", "D": "Installing software"},
     "answer": "A", "topic": "Operating Systems", "difficulty": "Medium"},

    {"id": 34, "question": "Which scheduling algorithm uses time slices?",
     "options": {"A": "FCFS", "B": "SJF", "C": "Round Robin", "D": "Priority only"},
     "answer": "C", "topic": "Operating Systems", "difficulty": "Medium"},

    {"id": 35, "question": "Which condition is necessary for deadlock?",
     "options": {"A": "Mutual Exclusion", "B": "Compilation", "C": "Sorting", "D": "Indexing"},
     "answer": "A", "topic": "Operating Systems", "difficulty": "Hard"},

    # COMPUTER NETWORKS
    {"id": 36, "question": "What does LAN stand for?",
     "options": {"A": "Local Area Network", "B": "Large Access Node", "C": "Long Area Number", "D": "Local Access Name"},
     "answer": "A", "topic": "Computer Networks", "difficulty": "Easy"},

    {"id": 37, "question": "Which device connects different networks?",
     "options": {"A": "Keyboard", "B": "Router", "C": "Monitor", "D": "Printer"},
     "answer": "B", "topic": "Computer Networks", "difficulty": "Easy"},

    {"id": 38, "question": "What does HTTP stand for?",
     "options": {"A": "HyperText Transfer Protocol", "B": "High Transfer Text Program", "C": "Hyper Terminal Transfer Process", "D": "Host Text Transfer Protocol"},
     "answer": "A", "topic": "Computer Networks", "difficulty": "Medium"},

    {"id": 39, "question": "Which protocol is used to send emails?",
     "options": {"A": "FTP", "B": "SMTP", "C": "HTTP", "D": "IP"},
     "answer": "B", "topic": "Computer Networks", "difficulty": "Medium"},

    {"id": 40, "question": "How many layers are in the OSI model?",
     "options": {"A": "4", "B": "5", "C": "7", "D": "8"},
     "answer": "C", "topic": "Computer Networks", "difficulty": "Hard"},

    # APTITUDE
    {"id": 41, "question": "What is 20% of 200?",
     "options": {"A": "20", "B": "30", "C": "40", "D": "50"},
     "answer": "C", "topic": "Aptitude", "difficulty": "Easy"},

    {"id": 42, "question": "What is the average of 10, 20 and 30?",
     "options": {"A": "10", "B": "20", "C": "30", "D": "60"},
     "answer": "B", "topic": "Aptitude", "difficulty": "Easy"},

    {"id": 43, "question": "A train travels 60 km in one hour. What is its speed?",
     "options": {"A": "30 km/h", "B": "40 km/h", "C": "60 km/h", "D": "90 km/h"},
     "answer": "C", "topic": "Aptitude", "difficulty": "Medium"},

    {"id": 44, "question": "What is the simple interest on Rs. 1000 at 10% for 2 years?",
     "options": {"A": "100", "B": "150", "C": "200", "D": "300"},
     "answer": "C", "topic": "Aptitude", "difficulty": "Medium"},

    {"id": 45, "question": "If 5 workers finish a task in 10 days, how many worker-days are required?",
     "options": {"A": "15", "B": "25", "C": "50", "D": "100"},
     "answer": "C", "topic": "Aptitude", "difficulty": "Hard"},

    # LOGICAL REASONING
    {"id": 46, "question": "Find the next number: 2, 4, 6, 8, ?",
     "options": {"A": "9", "B": "10", "C": "12", "D": "14"},
     "answer": "B", "topic": "Logical Reasoning", "difficulty": "Easy"},

    {"id": 47, "question": "Which one is different?",
     "options": {"A": "Apple", "B": "Mango", "C": "Carrot", "D": "Banana"},
     "answer": "C", "topic": "Logical Reasoning", "difficulty": "Easy"},

    {"id": 48, "question": "Find the next letter: A, C, E, G, ?",
     "options": {"A": "H", "B": "I", "C": "J", "D": "K"},
     "answer": "B", "topic": "Logical Reasoning", "difficulty": "Medium"},

    {"id": 49, "question": "If CAT is coded as DBU, how is DOG coded?",
     "options": {"A": "EPH", "B": "CNG", "C": "FQI", "D": "EOG"},
     "answer": "A", "topic": "Logical Reasoning", "difficulty": "Medium"},

    {"id": 50, "question": "A is taller than B. B is taller than C. Who is shortest?",
     "options": {"A": "A", "B": "B", "C": "C", "D": "Cannot determine"},
     "answer": "C", "topic": "Logical Reasoning", "difficulty": "Hard"}
]


# ==========================================
# 2. LOAD AND SAVE RESULTS
# ==========================================

def load_results():
    if not os.path.exists(SCORE_FILE):
        return []

    try:
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        print("Warning: Results file could not be read.")
        return []


def save_results(results):
    with open(SCORE_FILE, "w") as file:
        json.dump(results, file, indent=4)


# ==========================================
# 3. DISPLAY AVAILABLE TOPICS
# ==========================================

def get_topics():
    return sorted(set(q["topic"] for q in question_bank))


def view_topics():
    print("\n========== AVAILABLE TOPICS ==========")

    for index, topic in enumerate(get_topics(), 1):
        count = sum(1 for q in question_bank if q["topic"] == topic)
        print(f"{index}. {topic} ({count} questions)")


# ==========================================
# 4. VIEW QUESTION BANK
# ==========================================

def view_question_bank():
    view_topics()

    topic = input("\nEnter topic name (or ALL): ").strip()

    if topic.upper() == "ALL":
        selected = question_bank
    else:
        selected = [
            q for q in question_bank
            if q["topic"].lower() == topic.lower()
        ]

    if not selected:
        print("Topic not found!")
        return

    print("\n========== QUESTION BANK ==========")

    for q in selected:
        print(f"\nID: {q['id']} | Topic: {q['topic']} | Difficulty: {q['difficulty']}")
        print(q["question"])

        for letter, option in q["options"].items():
            print(f"{letter}. {option}")


# ==========================================
# 5. SELECT TOPIC AND QUESTION COUNT
# ==========================================

def select_topic():
    topics = get_topics()
    view_topics()

    try:
        choice = int(input("\nSelect topic number: "))

        if choice < 1 or choice > len(topics):
            print("Invalid topic selection!")
            return None

        return topics[choice - 1]

    except ValueError:
        print("Please enter a valid number!")
        return None


def select_question_count(available_count):
    while True:
        try:
            count = int(input(
                f"How many questions do you want? (1-{available_count}): "
            ))

            if count < 1:
                print("Please enter at least 1 question.")

            elif count > available_count:
                print(f"Only {available_count} questions are available.")

            else:
                return count

        except ValueError:
            print("Please enter a valid whole number.")


# ==========================================
# 6. START NEW QUIZ
# ==========================================

def start_quiz():
    name = input("\nEnter student name: ").strip()

    if not name:
        print("Student name cannot be empty!")
        return

    topic = select_topic()

    if topic is None:
        return

    available = [q for q in question_bank if q["topic"] == topic]

    print(f"\nAvailable questions: {len(available)}")

    count = select_question_count(len(available))

    quiz = random.sample(available, count)

    score = 0
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    review = []

    print("\n====================================")
    print("             QUIZFORGE")
    print("====================================")
    print("Student:", name)
    print("Topic:", topic)
    print("Questions:", count)
    print("Correct: +4 | Wrong: -1 | Skipped: 0")
    print("Enter S to skip a question.")
    print("====================================")

    for index, q in enumerate(quiz, 1):

        print(f"\nQuestion {index}/{count}")
        print(f"[{q['difficulty']}] {q['question']}")

        for letter, option in q["options"].items():
            print(f"{letter}. {option}")

        while True:
            answer = input("Your answer (A/B/C/D/S): ").strip().upper()

            if answer in ["A", "B", "C", "D", "S"]:
                break

            print("Invalid input! Enter A, B, C, D or S.")

        if answer == "S":
            status = "Unanswered"
            marks = 0
            selected_text = "Not answered"
            unanswered_count += 1

        elif answer == q["answer"]:
            status = "Correct"
            marks = CORRECT_MARKS
            score += marks
            correct_count += 1
            selected_text = q["options"][answer]

        else:
            status = "Incorrect"
            marks = -WRONG_MARKS
            score += marks
            wrong_count += 1
            selected_text = q["options"][answer]

        review.append({
            "question": q["question"],
            "selected_answer": selected_text,
            "correct_answer": q["options"][q["answer"]],
            "selected_option": answer,
            "correct_option": q["answer"],
            "status": status,
            "marks": marks
        })

    # ======================================
    # 7. FINAL RESULT
    # ======================================

    maximum_marks = count * CORRECT_MARKS
    percentage = (score / maximum_marks) * 100
    accuracy = (correct_count / count) * 100

    print("\n====================================")
    print("             FINAL RESULT")
    print("====================================")
    print("Student:", name)
    print("Topic:", topic)
    print("Score:", score, "/", maximum_marks)
    print(f"Score Percentage: {percentage:.2f}%")
    print(f"Accuracy: {accuracy:.2f}%")
    print("Correct:", correct_count)
    print("Incorrect:", wrong_count)
    print("Unanswered:", unanswered_count)

    # ======================================
    # 8. COMPLETE ANSWER REVIEW
    # ======================================

    print("\n========== ANSWER REVIEW ==========")

    for index, item in enumerate(review, 1):
        print(f"\nQ{index}. {item['question']}")
        print("Your answer:", item["selected_answer"])
        print("Correct answer:", item["correct_answer"])
        print("Status:", item["status"])

        if item["marks"] > 0:
            print("Marks awarded: +", item["marks"])
        else:
            print("Marks awarded:", item["marks"])

    # ======================================
    # 9. SAVE RESULT
    # ======================================

    results = load_results()

    result = {
        "name": name,
        "topic": topic,
        "score": score,
        "total_questions": count,
        "correct": correct_count,
        "incorrect": wrong_count,
        "unanswered": unanswered_count,
        "percentage": round(percentage, 2),
        "accuracy": round(accuracy, 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    results.append(result)
    save_results(results)

    print("\nYour result has been saved successfully!")


# ==========================================
# 10. TOPIC-WISE LEADERBOARD
# ==========================================

def view_leaderboard():
    results = load_results()

    if not results:
        print("\nNo quiz results available yet.")
        return

    topic = select_topic()

    if topic is None:
        return

    topic_results = [
        r for r in results
        if r["topic"] == topic
    ]

    if not topic_results:
        print("\nNo scores available for this topic.")
        return

    topic_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    print(f"\n========== {topic.upper()} LEADERBOARD ==========")
    print(f"{'Rank':<8}{'Name':<20}{'Score':<12}{'Questions':<12}")
    print("-" * 52)

    previous_score = None
    rank = 0

    for index, student in enumerate(topic_results[:5], 1):

        if student["score"] != previous_score:
            rank = index

        print(
            f"{rank:<8}"
            f"{student['name']:<20}"
            f"{student['score']:<12}"
            f"{student['total_questions']:<12}"
        )

        previous_score = student["score"]


# ==========================================
# 11. VIEW STUDENT RESULTS
# ==========================================

def view_my_results():
    results = load_results()

    name = input("\nEnter your student name: ").strip()

    if not name:
        print("Please enter a name.")
        return

    student_results = [
        r for r in results
        if r["name"].strip().casefold() == name.casefold()
    ]

    if not student_results:
        print("No results found for this student.")
        return

    print(f"\n========== RESULTS FOR {name.upper()} ==========")

    for index, result in enumerate(student_results, 1):
        print(f"\nQuiz {index}")
        print("Topic:", result["topic"])
        print("Score:", result["score"])
        print("Questions:", result["total_questions"])
        print("Correct:", result["correct"])
        print("Incorrect:", result["incorrect"])
        print("Unanswered:", result["unanswered"])
        print("Percentage:", result["percentage"], "%")
        print("Date:", result["date"])


# ==========================================
# 12. MAIN MENU
# ==========================================

def main():

    while True:

        print("\n")
        print("=" * 45)
        print("                 QUIZFORGE")
        print("       Randomised Assessment Engine")
        print("=" * 45)

        print("1. Start New Quiz")
        print("2. View Available Topics")
        print("3. View Question Bank")
        print("4. View Leaderboard")
        print("5. View My Quiz Results")
        print("6. Exit")

        print("=" * 45)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            start_quiz()

        elif choice == "2":
            view_topics()

        elif choice == "3":
            view_question_bank()

        elif choice == "4":
            view_leaderboard()

        elif choice == "5":
            view_my_results()

        elif choice == "6":
            print("\nThank you for using QuizForge!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice! Please select between 1 and 6.")


# ==========================================
# 13. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    main()
