from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_principal
from app.db.session import get_db
from app.schemas.common import APIEnvelope
from app.schemas.finance import (
    BudgetCreateRequest,
    BudgetOut,
    DashboardOut,
    ExpenseActionRequest,
    ExpenseCategoryOut,
    ExpenseCreateRequest,
    ExpenseOut,
)
from app.services.finance_service import FinanceService

router = APIRouter()
finance_service = FinanceService()


@router.get("/dashboard", response_model=APIEnvelope[DashboardOut])
def dashboard(principal=Depends(get_current_principal), db: Session = Depends(get_db)) -> APIEnvelope[DashboardOut]:
    return APIEnvelope(data=finance_service.build_dashboard(db, principal))


@router.get("/categories", response_model=APIEnvelope[list[ExpenseCategoryOut]])
def categories(principal=Depends(get_current_principal), db: Session = Depends(get_db)) -> APIEnvelope[list[ExpenseCategoryOut]]:
    return APIEnvelope(
        data=[ExpenseCategoryOut.model_validate(category) for category in finance_service.list_categories(db, principal)]
    )


@router.get("/budgets", response_model=APIEnvelope[list[BudgetOut]])
def budgets(principal=Depends(get_current_principal), db: Session = Depends(get_db)) -> APIEnvelope[list[BudgetOut]]:
    items = []
    for budget in finance_service.list_budgets(db, principal):
        spent_amount = finance_service._budget_consumed(budget)
        items.append(
            BudgetOut(
                id=budget.id,
                name=budget.name,
                currency=budget.currency,
                amount=budget.amount,
                start_date=budget.start_date,
                end_date=budget.end_date,
                alert_threshold_percent=budget.alert_threshold_percent,
                status=budget.status,
                category=ExpenseCategoryOut.model_validate(budget.category) if budget.category else None,
                spent_amount=spent_amount,
                created_at=budget.created_at,
                updated_at=budget.updated_at,
            )
        )
    return APIEnvelope(data=items)


@router.post("/budgets", response_model=APIEnvelope[BudgetOut])
def create_budget(
    payload: BudgetCreateRequest,
    principal=Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> APIEnvelope[BudgetOut]:
    budget = finance_service.create_budget(db, principal, payload)
    return APIEnvelope(
        data=BudgetOut(
            id=budget.id,
            name=budget.name,
            currency=budget.currency,
            amount=budget.amount,
            start_date=budget.start_date,
            end_date=budget.end_date,
            alert_threshold_percent=budget.alert_threshold_percent,
            status=budget.status,
            category=ExpenseCategoryOut.model_validate(budget.category) if budget.category else None,
            spent_amount=0,
            created_at=budget.created_at,
            updated_at=budget.updated_at,
        )
    )


@router.get("/expenses", response_model=APIEnvelope[list[ExpenseOut]])
def expenses(principal=Depends(get_current_principal), db: Session = Depends(get_db)) -> APIEnvelope[list[ExpenseOut]]:
    return APIEnvelope(data=[_to_expense_out(item) for item in finance_service.list_expenses(db, principal)])


@router.post("/expenses", response_model=APIEnvelope[ExpenseOut])
def create_expense(
    payload: ExpenseCreateRequest,
    principal=Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> APIEnvelope[ExpenseOut]:
    return APIEnvelope(data=_to_expense_out(finance_service.create_expense(db, principal, payload)))


@router.get("/expenses/{expense_id}", response_model=APIEnvelope[ExpenseOut])
def get_expense(
    expense_id: str,
    principal=Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> APIEnvelope[ExpenseOut]:
    return APIEnvelope(data=_to_expense_out(finance_service.get_expense(db, principal, expense_id)))


@router.post("/expenses/{expense_id}/approve", response_model=APIEnvelope[ExpenseOut])
def approve_expense(
    expense_id: str,
    payload: ExpenseActionRequest,
    principal=Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> APIEnvelope[ExpenseOut]:
    return APIEnvelope(data=_to_expense_out(finance_service.approve_expense(db, principal, expense_id, payload, "approve")))


@router.post("/expenses/{expense_id}/reject", response_model=APIEnvelope[ExpenseOut])
def reject_expense(
    expense_id: str,
    payload: ExpenseActionRequest,
    principal=Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> APIEnvelope[ExpenseOut]:
    return APIEnvelope(data=_to_expense_out(finance_service.approve_expense(db, principal, expense_id, payload, "reject")))


def _to_expense_out(expense) -> ExpenseOut:
    return ExpenseOut(
        id=expense.id,
        title=expense.title,
        vendor_name=expense.vendor_name,
        invoice_number=expense.invoice_number,
        currency=expense.currency,
        amount=expense.amount,
        expense_date=expense.expense_date,
        status=expense.status,
        policy_status=expense.policy_status,
        description=expense.description,
        ai_summary=expense.ai_summary,
        ai_risk_level=expense.ai_risk_level,
        budget_id=expense.budget_id,
        category=ExpenseCategoryOut.model_validate(expense.category) if expense.category else None,
        documents=[
            {
                "id": document.id,
                "filename": document.filename,
                "status": document.status,
                "created_at": document.created_at,
            }
            for document in expense.documents
        ],
        approvals=[item for item in expense.approvals],
        submitted_by_user_id=expense.submitted_by_user_id,
        created_at=expense.created_at,
        updated_at=expense.updated_at,
    )
