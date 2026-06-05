PROMPT_MODES = {
    "basic": "Give a simple beginner-friendly resume analysis.",
    "detailed": "Give a detailed resume analysis with practical improvement suggestions.",
    "strict": "Act like a strict technical recruiter and be honest about weaknesses.",
    "mentor": "Act like a supportive AI mentor and explain how the candidate can improve step by step."
}


def build_resume_analysis_prompt(resume_text, job_description, mode="mentor"):
    analysis_style = PROMPT_MODES.get(mode, PROMPT_MODES["mentor"])

    prompt = f"""
You are PrepAI Pro, an AI career assistant.

Your task is to compare a candidate resume with a job description.

Analysis Style:
{analysis_style}

Rules:
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations outside JSON.
- Be realistic and practical.
- Do not invent skills that are not present in the resume.
- If a skill is required in the job description but missing from the resume, include it in missing_skills.
- job_match_score must be a number between 0 and 100.

Use this exact JSON structure:

{{
  "candidate_summary": "",
  "matching_skills": [],
  "missing_skills": [],
  "job_match_score": 0,
  "strengths": [],
  "improvement_suggestions": [],
  "recommended_learning_topics": []
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""
    return prompt
def build_interview_questions_prompt(resume_text, job_description):
    prompt = f"""
You are PrepAI Pro, an AI interview preparation assistant.

Your task is to generate interview questions based on the candidate resume and job description.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations outside JSON.

Rules:
- Questions should be realistic for a Junior GenAI Engineer role.
- Questions should be based on the resume and job description.
- Include questions about missing skills also.
- Keep questions clear and practical.

Use this exact JSON structure:

{{
  "technical_questions": [],
  "project_questions": [],
  "behavioral_questions": [],
  "missing_skill_questions": []
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""
    return prompt

def build_answer_evaluation_prompt(question, user_answer, resume_text, job_description):
    prompt = f"""
You are PrepAI Pro, an AI interview coach.

Your task is to evaluate the candidate's interview answer using a clear scoring rubric.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations outside JSON.

Evaluation Rubric:
1. technical_correctness_score:
   - Is the answer technically correct?
   - Does it explain the concept accurately?

2. clarity_score:
   - Is the answer easy to understand?
   - Is it well structured?

3. relevance_score:
   - Does the answer directly answer the interview question?
   - Is it relevant to the target job role?

4. depth_score:
   - Does the answer have enough detail?
   - Does it include examples or practical understanding?

5. overall_score:
   - Give a final score between 0 and 100 based on all the above.

Rules:
- All scores must be numbers between 0 and 100.
- Be honest but helpful.
- Feedback should be practical.
- Improved answer should be interview-ready.
- Consider the resume and job description while evaluating.
- Do not give fake praise.
- If the answer is weak, clearly explain what is missing.

Use this exact JSON structure:

{{
  "overall_score": 0,
  "technical_correctness_score": 0,
  "clarity_score": 0,
  "relevance_score": 0,
  "depth_score": 0,
  "feedback": "",
  "strengths": [],
  "weaknesses": [],
  "improved_answer": "",
  "next_practice_topics": []
}}

Interview Question:
{question}

Candidate Answer:
{user_answer}

Resume:
{resume_text}

Job Description:
{job_description}
"""
    return prompt