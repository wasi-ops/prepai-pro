import json
import os

from utils import save_text_file
from prompts import (
    build_resume_analysis_prompt,
    build_interview_questions_prompt,
    build_answer_evaluation_prompt
)
from llm_service import call_llm
from parser import parse_json_response
from validator import (
    validate_resume_analysis,
    validate_interview_questions,
    validate_answer_evaluation
)


HISTORY_FILE_PATH = "outputs/practice_history.json"


def get_multiline_input(title):
    print(f"\nEnter {title}:")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines)


def get_analysis_mode():
    print("\nChoose analysis mode:")
    print("1. basic")
    print("2. detailed")
    print("3. strict")
    print("4. mentor")

    mode = input("Enter mode: ").strip().lower()

    allowed_modes = ["basic", "detailed", "strict", "mentor"]

    if mode not in allowed_modes:
        print("Invalid mode selected. Using mentor mode by default.")
        return "mentor"

    return mode


def save_json_result(result, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print(f"\nJSON result saved to {file_path}")


def load_json_file(file_path, default_value):
    if not os.path.exists(file_path):
        return default_value

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print(f"Warning: {file_path} is not valid JSON. Starting fresh.")
        return default_value


def print_analysis(parsed_result):
    print("\nPrepAI Pro - Resume Analysis")
    print("============================\n")

    print("Candidate Summary:")
    print(parsed_result["candidate_summary"])

    print("\nJob Match Score:")
    print(parsed_result["job_match_score"])

    print("\nMatching Skills:")
    for skill in parsed_result["matching_skills"]:
        print("-", skill)

    print("\nMissing Skills:")
    for skill in parsed_result["missing_skills"]:
        print("-", skill)

    print("\nStrengths:")
    for strength in parsed_result["strengths"]:
        print("-", strength)

    print("\nImprovement Suggestions:")
    for suggestion in parsed_result["improvement_suggestions"]:
        print("-", suggestion)

    print("\nRecommended Learning Topics:")
    for topic in parsed_result["recommended_learning_topics"]:
        print("-", topic)


def create_text_summary(parsed_result):
    summary = f"""
PrepAI Pro - Resume Analysis Summary

Candidate Summary:
{parsed_result["candidate_summary"]}

Job Match Score:
{parsed_result["job_match_score"]}

Missing Skills:
{", ".join(parsed_result["missing_skills"])}

Recommended Learning Topics:
{", ".join(parsed_result["recommended_learning_topics"])}
"""
    return summary


def print_interview_questions(parsed_questions):
    print("\nPrepAI Pro - Interview Questions")
    print("================================\n")

    print("Technical Questions:")
    for question in parsed_questions["technical_questions"]:
        print("-", question)

    print("\nProject-Based Questions:")
    for question in parsed_questions["project_questions"]:
        print("-", question)

    print("\nBehavioral Questions:")
    for question in parsed_questions["behavioral_questions"]:
        print("-", question)

    print("\nMissing Skill Questions:")
    for question in parsed_questions["missing_skill_questions"]:
        print("-", question)


def create_interview_questions_summary(parsed_questions):
    summary = "PrepAI Pro - Interview Questions\n\n"

    summary += "Technical Questions:\n"
    for question in parsed_questions["technical_questions"]:
        summary += f"- {question}\n"

    summary += "\nProject-Based Questions:\n"
    for question in parsed_questions["project_questions"]:
        summary += f"- {question}\n"

    summary += "\nBehavioral Questions:\n"
    for question in parsed_questions["behavioral_questions"]:
        summary += f"- {question}\n"

    summary += "\nMissing Skill Questions:\n"
    for question in parsed_questions["missing_skill_questions"]:
        summary += f"- {question}\n"

    return summary


def collect_all_questions(parsed_questions):
    all_questions = []

    for question in parsed_questions["technical_questions"]:
        all_questions.append({
            "category": "Technical",
            "question": question
        })

    for question in parsed_questions["project_questions"]:
        all_questions.append({
            "category": "Project",
            "question": question
        })

    for question in parsed_questions["behavioral_questions"]:
        all_questions.append({
            "category": "Behavioral",
            "question": question
        })

    for question in parsed_questions["missing_skill_questions"]:
        all_questions.append({
            "category": "Missing Skill",
            "question": question
        })

    return all_questions


def display_numbered_questions(all_questions):
    print("\nAvailable Interview Questions")
    print("=============================\n")

    for index, question_item in enumerate(all_questions, start=1):
        category = question_item["category"]
        question = question_item["question"]

        print(f"{index}. [{category}] {question}")


def select_question(all_questions):
    while True:
        try:
            choice = int(input("\nEnter question number, or 0 to stop practice: "))

            if choice == 0:
                return None

            if 1 <= choice <= len(all_questions):
                selected_question = all_questions[choice - 1]
                return selected_question

            print("Invalid number. Please choose a valid question number.")

        except ValueError:
            print("Please enter a number only.")


def print_answer_evaluation(parsed_evaluation):
    print("\nPrepAI Pro - Rubric-Based Answer Evaluation")
    print("===========================================\n")

    print("Overall Score:")
    print(parsed_evaluation["overall_score"])

    print("\nTechnical Correctness Score:")
    print(parsed_evaluation["technical_correctness_score"])

    print("\nClarity Score:")
    print(parsed_evaluation["clarity_score"])

    print("\nRelevance Score:")
    print(parsed_evaluation["relevance_score"])

    print("\nDepth Score:")
    print(parsed_evaluation["depth_score"])

    print("\nFeedback:")
    print(parsed_evaluation["feedback"])

    print("\nStrengths:")
    for strength in parsed_evaluation["strengths"]:
        print("-", strength)

    print("\nWeaknesses:")
    for weakness in parsed_evaluation["weaknesses"]:
        print("-", weakness)

    print("\nImproved Answer:")
    print(parsed_evaluation["improved_answer"])

    print("\nNext Practice Topics:")
    for topic in parsed_evaluation["next_practice_topics"]:
        print("-", topic)


def create_practice_session_summary(practice_result):
    summary = "PrepAI Pro - Interview Practice Session\n\n"

    summary += f"Question Category: {practice_result['category']}\n\n"

    summary += "Question:\n"
    summary += practice_result["question"] + "\n\n"

    summary += "User Answer:\n"
    summary += practice_result["user_answer"] + "\n\n"

    evaluation = practice_result["evaluation"]

    summary += "Evaluation:\n"
    summary += f"Overall Score: {evaluation['overall_score']}\n"
    summary += f"Technical Correctness: {evaluation['technical_correctness_score']}\n"
    summary += f"Clarity: {evaluation['clarity_score']}\n"
    summary += f"Relevance: {evaluation['relevance_score']}\n"
    summary += f"Depth: {evaluation['depth_score']}\n\n"

    summary += "Feedback:\n"
    summary += evaluation["feedback"] + "\n\n"

    summary += "Strengths:\n"
    for strength in evaluation["strengths"]:
        summary += f"- {strength}\n"

    summary += "\nWeaknesses:\n"
    for weakness in evaluation["weaknesses"]:
        summary += f"- {weakness}\n"

    summary += "\nImproved Answer:\n"
    summary += evaluation["improved_answer"] + "\n\n"

    summary += "Next Practice Topics:\n"
    for topic in evaluation["next_practice_topics"]:
        summary += f"- {topic}\n"

    return summary


def append_practice_history(practice_result):
    practice_history = load_json_file(HISTORY_FILE_PATH, [])

    if not isinstance(practice_history, list):
        practice_history = []

    practice_history.append(practice_result)

    save_json_result(practice_history, HISTORY_FILE_PATH)

    return practice_history


def calculate_score_summary(practice_history):
    if not practice_history:
        return {
            "total_attempts": 0,
            "average_overall_score": None,
            "highest_score": None,
            "lowest_score": None,
            "best_area": None,
            "weakest_area": None
        }

    valid_evaluations = []

    for practice_result in practice_history:
        evaluation = practice_result.get("evaluation", {})

        if isinstance(evaluation.get("overall_score"), (int, float)):
            valid_evaluations.append(evaluation)

    if not valid_evaluations:
        return {
            "total_attempts": 0,
            "average_overall_score": None,
            "highest_score": None,
            "lowest_score": None,
            "best_area": None,
            "weakest_area": None
        }

    overall_scores = [
        evaluation["overall_score"]
        for evaluation in valid_evaluations
    ]

    score_fields = {
        "technical_correctness": "technical_correctness_score",
        "clarity": "clarity_score",
        "relevance": "relevance_score",
        "depth": "depth_score"
    }

    average_area_scores = {}

    for area_name, field_name in score_fields.items():
        scores = [
            evaluation[field_name]
            for evaluation in valid_evaluations
            if isinstance(evaluation.get(field_name), (int, float))
        ]

        if scores:
            average_area_scores[area_name] = round(sum(scores) / len(scores), 2)

    best_area = max(
        average_area_scores,
        key=average_area_scores.get
    )

    weakest_area = min(
        average_area_scores,
        key=average_area_scores.get
    )

    score_summary = {
        "total_attempts": len(valid_evaluations),
        "average_overall_score": round(sum(overall_scores) / len(overall_scores), 2),
        "highest_score": max(overall_scores),
        "lowest_score": min(overall_scores),
        "average_area_scores": average_area_scores,
        "best_area": best_area,
        "weakest_area": weakest_area
    }

    return score_summary


def print_score_summary(score_summary):
    print("\nPrepAI Pro - Practice Score Summary")
    print("===================================\n")

    print("Total Attempts:")
    print(score_summary["total_attempts"])

    print("\nAverage Overall Score:")
    print(score_summary["average_overall_score"])

    print("\nHighest Score:")
    print(score_summary["highest_score"])

    print("\nLowest Score:")
    print(score_summary["lowest_score"])

    print("\nBest Area:")
    print(score_summary["best_area"])

    print("\nWeakest Area:")
    print(score_summary["weakest_area"])

    if score_summary.get("average_area_scores"):
        print("\nAverage Area Scores:")
        for area, score in score_summary["average_area_scores"].items():
            print(f"- {area}: {score}")


def create_score_summary_text(score_summary):
    summary = "PrepAI Pro - Practice Score Summary\n\n"

    summary += f"Total Attempts: {score_summary['total_attempts']}\n"
    summary += f"Average Overall Score: {score_summary['average_overall_score']}\n"
    summary += f"Highest Score: {score_summary['highest_score']}\n"
    summary += f"Lowest Score: {score_summary['lowest_score']}\n"
    summary += f"Best Area: {score_summary['best_area']}\n"
    summary += f"Weakest Area: {score_summary['weakest_area']}\n\n"

    if score_summary.get("average_area_scores"):
        summary += "Average Area Scores:\n"

        for area, score in score_summary["average_area_scores"].items():
            summary += f"- {area}: {score}\n"

    return summary


def run_resume_analysis(resume_text, job_description, mode):
    prompt = build_resume_analysis_prompt(
        resume_text,
        job_description,
        mode=mode
    )

    ai_output = call_llm(prompt)

    if ai_output is None:
        print("No resume analysis received.")
        return None

    parsed_result = parse_json_response(ai_output)

    is_valid, validation_messages = validate_resume_analysis(parsed_result)

    print("\nResume Analysis Validation Result:")
    for message in validation_messages:
        print("-", message)

    if not is_valid:
        print("Resume analysis failed validation.")
        return None

    print_analysis(parsed_result)

    save_json_result(
        parsed_result,
        "outputs/interactive_resume_analysis.json"
    )

    text_summary = create_text_summary(parsed_result)

    save_text_file(
        "outputs/interactive_summary.txt",
        text_summary
    )

    return parsed_result


def run_interview_question_generation(resume_text, job_description):
    interview_prompt = build_interview_questions_prompt(
        resume_text,
        job_description
    )

    interview_ai_output = call_llm(interview_prompt)

    if interview_ai_output is None:
        print("No interview questions received.")
        return None

    parsed_questions = parse_json_response(interview_ai_output)

    are_questions_valid, question_validation_messages = validate_interview_questions(
        parsed_questions
    )

    print("\nInterview Questions Validation Result:")
    for message in question_validation_messages:
        print("-", message)

    if not are_questions_valid:
        print("Interview questions failed validation.")
        return None

    print_interview_questions(parsed_questions)

    save_json_result(
        parsed_questions,
        "outputs/interview_questions.json"
    )

    interview_summary = create_interview_questions_summary(parsed_questions)

    save_text_file(
        "outputs/interview_questions.txt",
        interview_summary
    )

    return parsed_questions


def run_answer_evaluation(question_to_answer, user_answer, resume_text, job_description):
    answer_evaluation_prompt = build_answer_evaluation_prompt(
        question_to_answer,
        user_answer,
        resume_text,
        job_description
    )

    answer_ai_output = call_llm(answer_evaluation_prompt)

    if answer_ai_output is None:
        print("No answer evaluation received.")
        return None

    parsed_evaluation = parse_json_response(answer_ai_output)

    is_answer_valid, answer_validation_messages = validate_answer_evaluation(
        parsed_evaluation
    )

    print("\nAnswer Evaluation Validation Result:")
    for message in answer_validation_messages:
        print("-", message)

    if not is_answer_valid:
        print("Answer evaluation failed validation.")
        return None

    print_answer_evaluation(parsed_evaluation)

    return parsed_evaluation


def run_practice_session(parsed_questions, resume_text, job_description):
    all_questions = collect_all_questions(parsed_questions)

    if not all_questions:
        print("No questions available for practice.")
        return

    while True:
        display_numbered_questions(all_questions)

        selected_question_item = select_question(all_questions)

        if selected_question_item is None:
            print("Practice session stopped.")
            break

        question_to_answer = selected_question_item["question"]
        question_category = selected_question_item["category"]

        print("\nSelected Question:")
        print(question_to_answer)

        user_answer = get_multiline_input("your interview answer")

        parsed_evaluation = run_answer_evaluation(
            question_to_answer,
            user_answer,
            resume_text,
            job_description
        )

        if parsed_evaluation is None:
            print("Skipping this practice attempt because evaluation failed.")
            continue

        practice_result = {
            "category": question_category,
            "question": question_to_answer,
            "user_answer": user_answer,
            "evaluation": parsed_evaluation
        }

        practice_history = append_practice_history(practice_result)

        save_json_result(
            practice_result,
            "outputs/latest_practice_session_result.json"
        )

        practice_summary = create_practice_session_summary(practice_result)

        save_text_file(
            "outputs/latest_practice_session_summary.txt",
            practice_summary
        )

        score_summary = calculate_score_summary(practice_history)

        print_score_summary(score_summary)

        save_json_result(
            score_summary,
            "outputs/practice_score_summary.json"
        )

        score_summary_text = create_score_summary_text(score_summary)

        save_text_file(
            "outputs/practice_score_summary.txt",
            score_summary_text
        )

        continue_choice = input("\nDo you want to practice another question? yes/no: ")
        continue_choice = continue_choice.strip().lower()

        if continue_choice not in ["yes", "y"]:
            print("Practice session completed.")
            break


def main():
    print("Welcome to PrepAI Pro")
    print("=====================")

    os.makedirs("outputs", exist_ok=True)

    resume_text = get_multiline_input("resume text")

    job_description = get_multiline_input("job description")

    mode = get_analysis_mode()

    parsed_analysis = run_resume_analysis(
        resume_text,
        job_description,
        mode
    )

    if parsed_analysis is None:
        return

    parsed_questions = run_interview_question_generation(
        resume_text,
        job_description
    )

    if parsed_questions is None:
        return

    run_practice_session(
        parsed_questions,
        resume_text,
        job_description
    )

    print("\nPrepAI Pro finished successfully.")


if __name__ == "__main__":
    main()