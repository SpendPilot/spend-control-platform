from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_dev_access_token, get_current_principal
from app.db.session import get_db
from app.models import Organization, OrganizationMembership, UserSession
from app.schemas.auth import AuthProfileOut, AuthResponse, DevLoginRequest
from app.schemas.common import APIEnvelope
from app.services.user_service import get_user_from_principal, sync_user_context_from_claims

router = APIRouter()


@router.get("/me", response_model=APIEnvelope[AuthProfileOut])
def me(principal=Depends(get_current_principal), db: Session = Depends(get_db)) -> APIEnvelope[AuthProfileOut]:
    user = get_user_from_principal(db, principal.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    organization = db.query(Organization).filter(Organization.id == principal.organization_id).first()
    membership = db.query(OrganizationMembership).filter(OrganizationMembership.id == principal.membership_id).first()
    session = db.query(UserSession).filter(UserSession.id == principal.session_id).first()
    if organization is None or membership is None or session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session context not found")
    return APIEnvelope(
        data=AuthProfileOut(
            user=user,
            organization=organization,
            membership=membership,
            session=session,
            effective_role=principal.role,
        )
    )


@router.post("/dev-login", response_model=APIEnvelope[AuthResponse])
def dev_login(payload: DevLoginRequest, db: Session = Depends(get_db)) -> APIEnvelope[AuthResponse]:
    settings = get_settings()
    if settings.auth_mode != "dev-local":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dev login is disabled")

    email = payload.email or settings.dev_auth_default_email
    display_name = payload.display_name or settings.dev_auth_default_name
    role = payload.role or settings.dev_auth_default_role
    claims = {
        "oid": f"dev-{email}",
        "tid": "local-dev-tenant",
        "preferred_username": email,
        "email": email,
        "name": display_name,
        "roles": [role],
        "sid": f"dev-session-{email}",
    }
    auth_context = sync_user_context_from_claims(
        db,
        claims,
        session_fingerprint=f"dev-session-{email}",
        session_identifier=f"dev-session-{email}",
        auth_provider="dev-local",
        user_agent="developer",
    )
    token = create_dev_access_token(email, display_name, role)
    return APIEnvelope(
        data=AuthResponse(
            access_token=token,
            profile=AuthProfileOut(
                user=auth_context.user,
                organization=auth_context.organization,
                membership=auth_context.membership,
                session=auth_context.session,
                effective_role=auth_context.membership.role,
            ),
        )
    )
