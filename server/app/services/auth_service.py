from app.schemas.auth import LoginRequest
from app.schemas.user import UserResponse


DEMO_USERS = {
    "admin@talentmatch.com": {
        "id": "1",
        "name": "Admin User",
        "role": "admin",
        "permissions": [
            "create:job",
            "edit:job",
            "delete:job",
            "view:all_jobs",
            "view:all_candidates",
            "edit:candidate",
            "configure:ai",
            "view:analytics",
        ],
    },
    "recruiter@company.com": {
        "id": "2",
        "name": "Recruiter User",
        "role": "recruiter",
        "permissions": [
            "create:job",
            "edit:job",
            "view:all_jobs",
            "view:all_candidates",
            "score:candidate",
        ],
    },
    "hiring@techcorp.com": {
        "id": "3",
        "name": "Hiring Manager",
        "role": "hiring_manager",
        "permissions": [
            "view:all_jobs",
            "view:all_candidates",
            "score:candidate",
        ],
    },
    "candidate@example.com": {
        "id": "4",
        "name": "Candidate User",
        "role": "candidate",
        "permissions": [],
    },
}


def authenticate_demo_user(email: str, password: str) -> UserResponse | None:
    """Development-only authentication: any non-empty password is accepted."""
    if not password:
        return None

    user_data = DEMO_USERS.get(email.lower())
    if user_data is None:
        return None

    return UserResponse(
        id=user_data["id"],
        email=email.lower(),
        name=user_data["name"],
        role=user_data["role"],
        permissions=user_data["permissions"],
    )
