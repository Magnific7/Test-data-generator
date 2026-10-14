from fastapi import APIRouter
from app.api.schemas.requests import GenerateInvoiceRequest
from app.generators.invoices import generate_invoice_records


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
