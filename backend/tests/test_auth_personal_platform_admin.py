from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

import pytest

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.user_service import (
    MICROSOFT_CONSUMER_TENANT_ID,
    PLATFORM_PERSONAL_ADMIN_ORG_NAME,
    PLATFORM_PERSONAL_ADMIN_TENANT_ID,
    sync_user_context_from_claims,
)


def _consumer_payload(email: str) -> dict:
    now = datetime.now(UTC)
    return {
        "tid": MICROSOFT_CONSUMER_TENANT_ID,
        "sub": f"sub-{email}",
        "email": email,
        "preferred_username": email,
        "name": "Platform Owner",
        "iss": f"https://login.microsoftonline.com/{MICROSOFT_CONSUMER_TENANT_ID}/v2.0",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "sid": f"sid-{email}",
    }


def test_personal_platform_admin_uses_internal_platform_org(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PLATFORM_ADMIN_EMAILS", "owner@outlook.com")
    get_settings.cache_clear()

    with SessionLocal() as db:
        context = sync_user_context_from_claims(
            db,
            _consumer_payload("owner@outlook.com"),
            session_fingerprint="fingerprint-owner",
            session_identifier="session-owner",
            auth_provider="entra",
            user_agent="pytest",
        )

    assert context.user.platform_role == "platform_admin"
    assert context.organization.tenant_id == PLATFORM_PERSONAL_ADMIN_TENANT_ID
    assert context.organization.name == PLATFORM_PERSONAL_ADMIN_ORG_NAME
    assert context.membership.role == "org_admin"


def test_personal_non_admin_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PLATFORM_ADMIN_EMAILS", raising=False)
    get_settings.cache_clear()

    with SessionLocal() as db:
        with pytest.raises(ValueError, match="Personal Microsoft accounts are only allowed"):
            sync_user_context_from_claims(
                db,
                _consumer_payload("someone@outlook.com"),
                session_fingerprint="fingerprint-user",
                session_identifier="session-user",
                auth_provider="entra",
                user_agent="pytest",
            )

    os.environ.pop("PLATFORM_ADMIN_EMAILS", None)
    get_settings.cache_clear()
