from fastapi import APIRouter
from app.api.schemas.requests import GenerateInvoiceRequest, GenerateMixedInvoiceRequest
from app.generators.invoices import generate_invoice_records, generate_mixed_invoice_records


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

@router.post("")
def generate_invoices(request: GenerateInvoiceRequest):
    invoices = generate_invoice_records(request.count, request.scenario.value)

    return {
        "count": len(invoices),
        "scenario": request.scenario,
        "data": invoices
    }


@router.post("/mixed")
def generate_mixed_invoices(request: GenerateMixedInvoiceRequest):
    scenario_counts = {scenario.value: count for scenario, count in request.scenarios.items()}
    invoices = generate_mixed_invoice_records(scenario_counts)

    return {
        "count": len(invoices),
        "scenarios": scenario_counts,
        "data": invoices
    }
