from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ExpenseCategoryOut(BaseModel):
    id: str
    code: str
    name: str
    description: str | None

    model_config = {"from_attributes": True}


class BudgetCreateRequest(BaseModel):
    name: str
    category_id: str | None = None
    currency: str = "INR"
    amount: Decimal
    start_date: date
    end_date: date
    alert_threshold_percent: int = 80


class BudgetOut(BaseModel):
    id: str
    name: str
    currency: str
    amount: Decimal
    start_date: date
    end_date: date
    alert_threshold_percent: int
    status: str
    category: ExpenseCategoryOut | None = None
    spent_amount: Decimal = Decimal("0")
    created_at: datetime
    updated_at: datetime


class ExpenseApprovalOut(BaseModel):
    id: str
    approver_user_id: str
    action: str
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ExpenseCreateRequest(BaseModel):
    title: str
    vendor_name: str | None = None
    invoice_number: str | None = None
    category_id: str | None = None
    budget_id: str | None = None
    document_id: str | None = None
    currency: str = "INR"
    amount: Decimal
    expense_date: date
    description: str | None = None
    ai_summary: str | None = None
    ai_risk_level: str | None = None


class ExpenseActionRequest(BaseModel):
    comment: str | None = None


class ExpenseDocumentOut(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime


class ExpenseOut(BaseModel):
    id: str
    title: str
    vendor_name: str | None
    invoice_number: str | None
    currency: str
    amount: Decimal
    expense_date: date
    status: str
    policy_status: str
    description: str | None
    ai_summary: str | None
    ai_risk_level: str | None
    budget_id: str | None
    category: ExpenseCategoryOut | None
    documents: list[ExpenseDocumentOut] = Field(default_factory=list)
    approvals: list[ExpenseApprovalOut] = Field(default_factory=list)
    submitted_by_user_id: str
    created_at: datetime
    updated_at: datetime


class BudgetCardOut(BaseModel):
    budget_id: str
    name: str
    limit_amount: Decimal
    consumed_amount: Decimal
    utilization_percent: float
    threshold_percent: int


class CategorySpendOut(BaseModel):
    category: str
    amount: Decimal


class DashboardOut(BaseModel):
    organization_name: str
    role: str
    total_expenses: int
    approved_spend: Decimal
    submitted_spend: Decimal
    pending_approvals: int
    budgets: list[BudgetCardOut]
    category_breakdown: list[CategorySpendOut]
