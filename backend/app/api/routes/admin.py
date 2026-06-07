from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.rbac import ROLE_ORG_ADMIN, ROLE_PLATFORM_ADMIN
from app.core.security import require_role
from app.db.session import get_db
from app.schemas.auth import MembershipOut, MembershipRoleUpdateRequest, OrganizationOut, SessionOut
from app.schemas.common import APIEnvelope
from app.services.user_service import list_memberships, list_sessions, revoke_session, update_membership_role

router = APIRouter()


@router.get("/organization", response_model=APIEnvelope[OrganizationOut])
def get_current_organization(principal=Depends(require_role(ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN))) -> APIEnvelope[OrganizationOut]:
    return APIEnvelope(
        data=OrganizationOut(
            id=principal.organization_id,
            tenant_id=principal.tenant_id or "",
            name=principal.organization_name,
            slug=principal.organization_slug,
            default_currency=principal.default_currency,
        )
    )


@router.get("/members", response_model=APIEnvelope[list[MembershipOut]])
def members(
    principal=Depends(require_role(ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN)),
    db: Session = Depends(get_db),
) -> APIEnvelope[list[MembershipOut]]:
    return APIEnvelope(data=[MembershipOut.model_validate(item) for item in list_memberships(db, principal.organization_id)])


@router.patch("/members/{membership_id}", response_model=APIEnvelope[MembershipOut])
def update_role(
    membership_id: str,
    payload: MembershipRoleUpdateRequest,
    principal=Depends(require_role(ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN)),
    db: Session = Depends(get_db),
) -> APIEnvelope[MembershipOut]:
    membership = update_membership_role(db, membership_id, payload.role)
    if membership is None or membership.organization_id != principal.organization_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")
    return APIEnvelope(data=MembershipOut.model_validate(membership))


@router.get("/sessions", response_model=APIEnvelope[list[SessionOut]])
def sessions(
    principal=Depends(require_role(ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN)),
    db: Session = Depends(get_db),
) -> APIEnvelope[list[SessionOut]]:
    return APIEnvelope(data=[SessionOut.model_validate(item) for item in list_sessions(db, principal.organization_id)])


@router.post("/sessions/{session_id}/revoke", response_model=APIEnvelope[SessionOut])
def revoke(
    session_id: str,
    principal=Depends(require_role(ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN)),
    db: Session = Depends(get_db),
) -> APIEnvelope[SessionOut]:
    session = revoke_session(db, session_id)
    if session is None or session.organization_id != principal.organization_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return APIEnvelope(data=SessionOut.model_validate(session))
