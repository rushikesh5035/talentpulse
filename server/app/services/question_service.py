from app.schemas.question import QuestionGenerateRequest


def _unique_skills(skills: list[str]) -> list[str]:
    """Strip whitespace and deduplicate skills case-insensitively, preserving order."""
    unique: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        normalized = skill.strip()
        key = normalized.casefold()

        if normalized and key not in seen:
            seen.add(key)
            unique.append(normalized)

    return unique


def generate_questions(request: QuestionGenerateRequest) -> list[str]:
    """Generate deterministic template questions, prioritizing shared skills.

    The job description is accepted as context for future AI generation. This
    template implementation currently uses only the supplied skill lists.
    """
    base_templates = [
        "Tell us about your experience with {skill}.",
        "Describe a challenging project where you used {skill}.",
        "How do you approach debugging issues involving {skill}?",
        "What best practices do you follow when using {skill}?",
    ]

    job_skills = _unique_skills(request.job_skills)
    candidate_skills = _unique_skills(request.candidate_skills)

    job_skill_keys = {skill.casefold() for skill in job_skills}
    overlap = [
        skill for skill in candidate_skills 
        if skill.casefold() in job_skill_keys
    ]

    overlap_keys = {skill.casefold() for skill in overlap}
    remaining_skills = [
        skill
        for skill in job_skills + candidate_skills
        if skill.casefold() not in overlap_keys
    ]

    prioritized_skills = _unique_skills(overlap + remaining_skills)

    questions: list[str] = []
    for skill in prioritized_skills:
        for template in base_templates:
            questions.append(template.format(skill=skill))
            if len(questions) == 6:
                return questions

    general_questions = [
        "What interests you about this position?",
        "Describe a technical decision you made and the trade-offs you considered.",
        "How do you approach learning an unfamiliar technology?",
    ]

    questions.extend(general_questions[: 6 - len(questions)])
    return questions