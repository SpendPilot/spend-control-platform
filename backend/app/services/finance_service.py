from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.core.rbac import APPROVAL_ROLES, FINANCE_WRITE_ROLES, ORG_READ_ROLES
from app.core.security import AuthenticatedPrincipal
from app.models import Budget, Document, Expense, ExpenseApproval, ExpenseCategory
from app.schemas.finance import (
    BudgetCreateRequest,
    DashboardOut,
    ExpenseActionRequest,
    ExpenseCreateRequest,
)
from app.services.audit_service import create_audit_event


class FinanceService:
    def list_categories(self, db: Session, principal: AuthenticatedPrincipal) -> list[ExpenseCategory]:
        return (
            db.query(ExpenseCategory)
            .filter(ExpenseCategory.organization_id == principal.organization_id)
            .order_by(ExpenseCategory.name.asc())
            .all()
        )

    def list_budgets(self, db: Session, principal: AuthenticatedPrincipal) -> list[Budget]:
        return (
            db.query(Budget)
            .options(joinedload(Budget.category), joinedload(Budget.expenses))
            .filter(Budget.organization_id == principal.organization_id)
            .order_by(Budget.start_date.desc(), Budget.name.asc())
            .all()
        )

    def create_budget(self, db: Session, principal: AuthenticatedPrincipal, payload: BudgetCreateRequest) -> Budget:
        if principal.role not in FINANCE_WRITE_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")

        category_id = self._validate_category(db, principal, payload.category_id) if payload.category_id else None
        budget = Budget(
            organization_id=principal.organization_id,
            category_id=category_id,
            name=payload.name,
            currency=payload.currency,
            amount=payload.amount,
            start_date=payload.start_date,
            end_date=payload.end_date,
            alert_threshold_percent=payload.alert_threshold_percent,
        )
        db.add(budget)
        db.commit()
        db.refresh(budget)
        create_audit_event(
            db,
            organization_id=principal.organization_id,
            actor_user_id=principal.user_id,
            resource_type="budget",
            resource_id=budget.id,
            action="created",
            details={"name": budget.name, "amount": str(budget.amount)},
        )
        return budget

    def list_expenses(self, db: Session, principal: AuthenticatedPrincipal) -> list[Expense]:
        query = (
            db.query(Expense)
            .options(
                joinedload(Expense.category),
                joinedload(Expense.budget),
                joinedload(Expense.documents),
                joinedload(Expense.approvals),
            )
            .filter(Expense.organization_id == principal.organization_id)
            .order_by(Expense.created_at.desc())
        )
        if principal.role not in ORG_READ_ROLES:
            query = query.filter(Expense.submitted_by_user_id == principal.user_id)
        return query.all()

    def get_expense(self, db: Session, principal: AuthenticatedPrincipal, expense_id: str) -> Expense:
        expense = (
            db.query(Expense)
            .options(
                joinedload(Expense.category),
                joinedload(Expense.budget),
                joinedload(Expense.documents).joinedload(Document.scans),
                joinedload(Expense.approvals),
            )
            .filter(Expense.id == expense_id, Expense.organization_id == principal.organization_id)
            .first()
        )
        if expense is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        if principal.role not in ORG_READ_ROLES and expense.submitted_by_user_id != principal.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return expense

    def create_expense(self, db: Session, principal: AuthenticatedPrincipal, payload: ExpenseCreateRequest) -> Expense:
        category_id = self._validate_category(db, principal, payload.category_id) if payload.category_id else None
        budget = self._validate_budget(db, principal, payload.budget_id) if payload.budget_id else None

        expense = Expense(
            organization_id=principal.organization_id,
            submitted_by_user_id=principal.user_id,
            budget_id=budget.id if budget else None,
            category_id=category_id,
            title=payload.title,
            vendor_name=payload.vendor_name,
            invoice_number=payload.invoice_number,
            currency=payload.currency,
            amount=payload.amount,
            expense_date=payload.expense_date,
            description=payload.description,
            status="approved" if principal.role in FINANCE_WRITE_ROLES else "submitted",
            policy_status="approved" if principal.role in FINANCE_WRITE_ROLES else "needs_review",
            ai_summary=payload.ai_summary,
            ai_risk_level=payload.ai_risk_level,
        )
        db.add(expense)
        db.flush()

        if payload.document_id:
            document = (
                db.query(Document)
                .filter(
                    Document.id == payload.document_id,
                    Document.organization_id == principal.organization_id,
                )
                .first()
            )
            if document is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
            document.expense_id = expense.id

        db.commit()
        db.refresh(expense)
        create_audit_event(
            db,
            organization_id=principal.organization_id,
            actor_user_id=principal.user_id,
            resource_type="expense",
            resource_id=expense.id,
            action="created",
            details={"title": expense.title, "amount": str(expense.amount)},
        )
        return expense

    def approve_expense(
        self,
        db: Session,
        principal: AuthenticatedPrincipal,
        expense_id: str,
        payload: ExpenseActionRequest,
        action: str,
    ) -> Expense:
        if principal.role not in APPROVAL_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        expense = self.get_expense(db, principal, expense_id)
        expense.status = "approved" if action == "approve" else "rejected"
        expense.policy_status = "approved" if action == "approve" else "rejected"
        approval = ExpenseApproval(
            expense_id=expense.id,
            approver_user_id=principal.user_id,
            action=action,
            comment=payload.comment,
        )
        db.add(approval)
        db.commit()
        db.refresh(expense)
        create_audit_event(
            db,
            organization_id=principal.organization_id,
            actor_user_id=principal.user_id,
            resource_type="expense",
            resource_id=expense.id,
            action=action,
            details={"comment": payload.comment},
        )
        return expense

    def build_dashboard(self, db: Session, principal: AuthenticatedPrincipal) -> DashboardOut:
        expenses_query = db.query(Expense).filter(Expense.organization_id == principal.organization_id)
        if principal.role not in ORG_READ_ROLES:
            expenses_query = expenses_query.filter(Expense.submitted_by_user_id == principal.user_id)

        expenses = expenses_query.all()
        pending_approvals = sum(1 for expense in expenses if expense.status == "submitted")
        total_spend = sum((expense.amount for expense in expenses if expense.status == "approved"), Decimal("0"))
        draft_spend = sum((expense.amount for expense in expenses if expense.status == "submitted"), Decimal("0"))

        budgets = self.list_budgets(db, principal)
        budget_cards = []
        for budget in budgets:
            consumed = self._budget_consumed(budget)
            utilization = float((consumed / budget.amount) * Decimal("100")) if budget.amount else 0.0
            budget_cards.append(
                {
                    "budget_id": budget.id,
                    "name": budget.name,
                    "limit_amount": budget.amount,
                    "consumed_amount": consumed,
                    "utilization_percent": round(utilization, 2),
                    "threshold_percent": budget.alert_threshold_percent,
                }
            )

        category_totals = (
            db.query(ExpenseCategory.name, func.coalesce(func.sum(Expense.amount), 0))
            .join(Expense, Expense.category_id == ExpenseCategory.id)
            .filter(Expense.organization_id == principal.organization_id, Expense.status == "approved")
            .group_by(ExpenseCategory.name)
            .order_by(func.sum(Expense.amount).desc())
            .all()
        )

        return DashboardOut(
            organization_name=principal.organization_name,
            role=principal.role,
            total_expenses=len(expenses),
            approved_spend=total_spend,
            submitted_spend=draft_spend,
            pending_approvals=pending_approvals,
            budgets=budget_cards,
            category_breakdown=[
                {"category": category_name, "amount": Decimal(str(amount))}
                for category_name, amount in category_totals
            ],
        )

    def _budget_consumed(self, budget: Budget) -> Decimal:
        return sum(
            (
                expense.amount
                for expense in budget.expenses
                if expense.status == "approved"
                and budget.start_date <= expense.expense_date <= budget.end_date
            ),
            Decimal("0"),
        )

    def _validate_category(self, db: Session, principal: AuthenticatedPrincipal, category_id: str) -> str:
        category = (
            db.query(ExpenseCategory)
            .filter(
                ExpenseCategory.id == category_id,
                ExpenseCategory.organization_id == principal.organization_id,
            )
            .first()
        )
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense category not found")
        return category.id

    def _validate_budget(self, db: Session, principal: AuthenticatedPrincipal, budget_id: str) -> Budget:
        budget = (
            db.query(Budget)
            .filter(Budget.id == budget_id, Budget.organization_id == principal.organization_id)
            .first()
        )
        if budget is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
        return budget
