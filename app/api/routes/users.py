from fastapi import APIRouter
from app.api.schemas.requests import GenerateUserRequest
from app.generators.users import generate_user_records


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("")
def generate_users(request: GenerateUserRequest):
    users = generate_user_records(request.count, request.scenario.value)

    return {
        "count": len(users),
        "scenario": request.scenario,
        "data": users
    }
