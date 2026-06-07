from tests.conftest import get_client


def _auth_header(client) -> dict[str, str]:
    response = client.post(
        "/api/auth/dev-login",
        json={"email": "reviewer@example.com", "display_name": "Reviewer", "role": "employee"},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_upload_scan_extract_and_fetch_document() -> None:
    client = get_client()
    headers = _auth_header(client)

    upload = client.post(
        "/api/documents/upload",
        headers=headers,
        files={"file": ("contract.txt", b"This contract contains indemnity and termination clauses.", "text/plain")},
    )
    assert upload.status_code == 200
    document_id = upload.json()["data"]["document"]["id"]

    scan = client.post(f"/api/documents/{document_id}/scan", headers=headers)
    assert scan.status_code == 200
    assert scan.json()["data"]["risk_level"] in {"medium", "high"}

    extracted = client.post(f"/api/documents/{document_id}/extract-expense", headers=headers)
    assert extracted.status_code == 200
    assert extracted.json()["data"]["provider_status"] in {"fallback", "azure-ai-foundry", "azure-document-intelligence"}

    latest = client.get(f"/api/documents/{document_id}/scan-result", headers=headers)
    assert latest.status_code == 200
    assert latest.json()["data"]["document_id"] == document_id
