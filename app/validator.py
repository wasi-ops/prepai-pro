EXPECTED_KEYS = [
    "candidate_summary",
    "matching_skills",
    "missing_skills",
    "job_match_score",
    "strengths",
    "improvement_suggestions",
    "recommended_learning_topics"
]


def validate_required_keys(parsed_result):
    missing_keys = []

    for key in EXPECTED_KEYS:
        if key not in parsed_result:
            missing_keys.append(key)

    if missing_keys:
        return False, missing_keys

    return True, []


def validate_job_match_score(parsed_result):
    score = parsed_result.get("job_match_score")

    if not isinstance(score, (int, float)):
        return False, "job_match_score must be a number."

    if score < 0 or score > 100:
        return False, "job_match_score must be between 0 and 100."

    return True, "Score is valid."


def validate_list_fields(parsed_result):
    list_fields = [
        "matching_skills",
        "missing_skills",
        "strengths",
        "improvement_suggestions",
        "recommended_learning_topics"
    ]

    errors = []

    for field in list_fields:
        if not isinstance(parsed_result.get(field), list):
            errors.append(f"{field} must be a list.")

    if errors:
        return False, errors

    return True, []


def validate_resume_analysis(parsed_result):
    if parsed_result is None:
        return False, ["No parsed result found."]

    are_keys_valid, missing_keys = validate_required_keys(parsed_result)

    if not are_keys_valid:
        return False, [f"Missing keys: {missing_keys}"]

    is_score_valid, score_message = validate_job_match_score(parsed_result)

    if not is_score_valid:
        return False, [score_message]

    are_lists_valid, list_errors = validate_list_fields(parsed_result)

    if not are_lists_valid:
        return False, list_errors

    return True, ["Validation successful."]

INTERVIEW_EXPECTED_KEYS = [
    "technical_questions",
    "project_questions",
    "behavioral_questions",
    "missing_skill_questions"
]


def validate_interview_questions(parsed_result):
    if parsed_result is None:
        return False, ["No parsed result found."]

    missing_keys = []

    for key in INTERVIEW_EXPECTED_KEYS:
        if key not in parsed_result:
            missing_keys.append(key)

    if missing_keys:
        return False, [f"Missing keys: {missing_keys}"]

    for key in INTERVIEW_EXPECTED_KEYS:
        if not isinstance(parsed_result[key], list):
            return False, [f"{key} must be a list."]

    return True, ["Interview questions validation successful."]


ANSWER_EVALUATION_EXPECTED_KEYS = [
    "overall_score",
    "technical_correctness_score",
    "clarity_score",
    "relevance_score",
    "depth_score",
    "feedback",
    "strengths",
    "weaknesses",
    "improved_answer",
    "next_practice_topics"
]


def validate_score_field(parsed_result, field_name):
    score = parsed_result.get(field_name)

    if not isinstance(score, (int, float)):
        return False, f"{field_name} must be a number."

    if score < 0 or score > 100:
        return False, f"{field_name} must be between 0 and 100."

    return True, f"{field_name} is valid."


def validate_answer_evaluation(parsed_result):
    if parsed_result is None:
        return False, ["No parsed result found."]

    missing_keys = []

    for key in ANSWER_EVALUATION_EXPECTED_KEYS:
        if key not in parsed_result:
            missing_keys.append(key)

    if missing_keys:
        return False, [f"Missing keys: {missing_keys}"]

    score_fields = [
        "overall_score",
        "technical_correctness_score",
        "clarity_score",
        "relevance_score",
        "depth_score"
    ]

    for field in score_fields:
        is_score_valid, score_message = validate_score_field(parsed_result, field)

        if not is_score_valid:
            return False, [score_message]

    list_fields = [
        "strengths",
        "weaknesses",
        "next_practice_topics"
    ]

    for field in list_fields:
        if not isinstance(parsed_result.get(field), list):
            return False, [f"{field} must be a list."]

    if not isinstance(parsed_result.get("feedback"), str):
        return False, ["feedback must be a string."]

    if not isinstance(parsed_result.get("improved_answer"), str):
        return False, ["improved_answer must be a string."]

    return True, ["Rubric-based answer evaluation validation successful."]