from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.user_service import (
    MICROSOFT_CONSUMER_TENANT_ID,
    PERSONAL_ACCOUNT_TENANT_PREFIX,
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


def test_personal_account_bootstraps_isolated_workspace(monkeypatch) -> None:
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
    assert context.organization.tenant_id.startswith(f"{PERSONAL_ACCOUNT_TENANT_PREFIX}:")
    assert context.organization.name == "Platform Owner Workspace"
    assert context.membership.role == "org_admin"


def test_personal_accounts_do_not_share_the_consumer_tenant_workspace(monkeypatch) -> None:
    monkeypatch.delenv("PLATFORM_ADMIN_EMAILS", raising=False)
    get_settings.cache_clear()

    with SessionLocal() as db:
        first = sync_user_context_from_claims(
            db,
            _consumer_payload("someone@outlook.com"),
            session_fingerprint="fingerprint-user-1",
            session_identifier="session-user-1",
            auth_provider="entra",
            user_agent="pytest",
        )
        first_org_id = first.organization.id
        first_tenant_id = first.organization.tenant_id
        first_role = first.membership.role
        second = sync_user_context_from_claims(
            db,
            _consumer_payload("another@outlook.com"),
            session_fingerprint="fingerprint-user-2",
            session_identifier="session-user-2",
            auth_provider="entra",
            user_agent="pytest",
        )
        second_org_id = second.organization.id
        second_tenant_id = second.organization.tenant_id
        second_role = second.membership.role

    assert first_org_id != second_org_id
    assert first_tenant_id != second_tenant_id
    assert first_role == "org_admin"
    assert second_role == "org_admin"

    os.environ.pop("PLATFORM_ADMIN_EMAILS", None)
    get_settings.cache_clear()
