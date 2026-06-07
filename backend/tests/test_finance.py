from tests.conftest import get_client


def _auth_header(client, role: str = "org_admin") -> dict[str, str]:
    response = client.post(
        "/api/auth/dev-login",
        json={"email": f"{role}@example.com", "display_name": role.title(), "role": role},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_budget_expense_and_approve() -> None:
    client = get_client()
    admin_headers = _auth_header(client, "org_admin")

    categories = client.get("/api/finance/categories", headers=admin_headers)
    assert categories.status_code == 200
    category_id = categories.json()["data"][0]["id"]

    budget = client.post(
        "/api/finance/budgets",
        headers=admin_headers,
        json={
            "name": "June Travel",
            "category_id": category_id,
            "currency": "INR",
            "amount": "10000.00",
            "start_date": "2026-06-01",
            "end_date": "2026-06-30",
            "alert_threshold_percent": 80,
        },
    )
    assert budget.status_code == 200
    budget_id = budget.json()["data"]["id"]

    employee_headers = _auth_header(client, "employee")
    expense = client.post(
        "/api/finance/expenses",
        headers=employee_headers,
        json={
            "title": "Taxi from airport",
            "vendor_name": "City Cabs",
            "invoice_number": "TX-001",
            "category_id": category_id,
            "budget_id": budget_id,
            "currency": "INR",
            "amount": "1250.00",
            "expense_date": "2026-06-05",
            "description": "Travel expense",
        },
    )
    assert expense.status_code == 200
    expense_id = expense.json()["data"]["id"]
    assert expense.json()["data"]["status"] == "submitted"

    approved = client.post(
        f"/api/finance/expenses/{expense_id}/approve",
        headers=admin_headers,
        json={"comment": "Looks good"},
    )
    assert approved.status_code == 200
    assert approved.json()["data"]["status"] == "approved"
