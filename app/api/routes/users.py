from fastapi import APIRouter
from app.api.schemas.requests import GenerateUserRequest, GenerateMixedUserRequest
from app.generators.users import generate_user_records, generate_mixed_user_records


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


@router.post("/mixed")
def generate_mixed_users(request: GenerateMixedUserRequest):
    scenario_counts = {scenario.value: count for scenario, count in request.scenarios.items()}
    users = generate_mixed_user_records(scenario_counts)

    return {
        "count": len(users),
        "scenarios": scenario_counts,
        "data": users
    }
