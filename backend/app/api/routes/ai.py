from fastapi import APIRouter, Depends

from app.core.security import get_current_principal
from app.schemas.common import APIEnvelope
from app.schemas.documents import DocumentAnalysisResult, TextAnalyzeRequest
from app.services.document_service import DocumentService

router = APIRouter()
document_service = DocumentService()


@router.post("/analyze", response_model=APIEnvelope[DocumentAnalysisResult])
def analyze_text(
    payload: TextAnalyzeRequest,
    _principal=Depends(get_current_principal),
) -> APIEnvelope[DocumentAnalysisResult]:
    return APIEnvelope(data=document_service.analyze_text(payload.text, payload.metadata))
