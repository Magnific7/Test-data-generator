from fastapi import APIRouter, HTTPException
from app.api.schemas.requests import GenerateDataRequest
from app.generators.users import generate_user_records


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("")
def generate_users(request: GenerateDataRequest):
    try:
        users = generate_user_records(request.count, request.scenario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "count": len(users),
        "scenario": request.scenario,
        "data": users
    }