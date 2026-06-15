"""Add payment operations core models

Revision ID: 20260615_0003
Revises: 20260615_0002
Create Date: 2026-06-15 00:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260615_0003"
down_revision = "20260615_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "vendors",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("criticality", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("contact_info", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("organization_id", "name", name="uq_vendor_name"),
    )
    op.create_index("ix_vendors_organization_id", "vendors", ["organization_id"], unique=False)

    op.create_table(
        "recurring_expenses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("department_id", sa.String(length=36), sa.ForeignKey("departments.id"), nullable=True),
        sa.Column("vendor_id", sa.String(length=36), sa.ForeignKey("vendors.id"), nullable=True),
        sa.Column("bill_document_id", sa.String(length=36), sa.ForeignKey("documents.id"), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="INR"),
        sa.Column("billing_cycle", sa.String(length=30), nullable=False, server_default="monthly"),
        sa.Column("due_day", sa.Integer(), nullable=True),
        sa.Column("next_due_date", sa.Date(), nullable=True),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="pay_this_week"),
        sa.Column("criticality", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("created_by_user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_recurring_expenses_organization_id", "recurring_expenses", ["organization_id"], unique=False)

    op.create_table(
        "recurring_expense_requests",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("department_id", sa.String(length=36), sa.ForeignKey("departments.id"), nullable=False),
        sa.Column("requested_by_user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("vendor_name", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("estimated_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="INR"),
        sa.Column("billing_cycle", sa.String(length=30), nullable=False, server_default="monthly"),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("bill_document_id", sa.String(length=36), sa.ForeignKey("documents.id"), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("approved_by_user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_recurring_expense_requests_organization_id", "recurring_expense_requests", ["organization_id"], unique=False)

    op.create_table(
        "spend_limits",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("department_id", sa.String(length=36), sa.ForeignKey("departments.id"), nullable=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("max_single_expense_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("monthly_limit", sa.Numeric(12, 2), nullable=True),
        sa.Column("requires_approval_above_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("allowed_categories_json", sa.JSON(), nullable=True),
        sa.Column("recurring_creation_restricted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("variable_requires_org_owner", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_by_user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_spend_limits_organization_id", "spend_limits", ["organization_id"], unique=False)

    op.create_table(
        "payment_priorities",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("expense_type", sa.String(length=20), nullable=False),
        sa.Column("expense_id", sa.String(length=36), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("estimated_cash_out_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_payment_priorities_organization_id", "payment_priorities", ["organization_id"], unique=False)
    op.create_index("ix_payment_priorities_expense_id", "payment_priorities", ["expense_id"], unique=False)

    op.create_table(
        "ai_chat_sessions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_ai_chat_sessions_organization_id", "ai_chat_sessions", ["organization_id"], unique=False)

    op.create_table(
        "ai_chat_messages",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("ai_chat_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("grounded_context_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_ai_chat_messages_organization_id", "ai_chat_messages", ["organization_id"], unique=False)

    op.add_column("budgets", sa.Column("department_id", sa.String(length=36), nullable=True))
    op.add_column("budgets", sa.Column("scope", sa.String(length=20), nullable=False, server_default="company"))
    op.add_column("budgets", sa.Column("month", sa.Integer(), nullable=True))
    op.add_column("budgets", sa.Column("year", sa.Integer(), nullable=True))
    op.create_index("ix_budgets_department_id", "budgets", ["department_id"], unique=False)
    op.create_foreign_key("fk_budgets_department_id_departments", "budgets", "departments", ["department_id"], ["id"])

    op.add_column("expenses", sa.Column("department_id", sa.String(length=36), nullable=True))
    op.add_column("expenses", sa.Column("vendor_id", sa.String(length=36), nullable=True))
    op.add_column("expenses", sa.Column("expense_type", sa.String(length=20), nullable=False, server_default="variable"))
    op.add_column("expenses", sa.Column("dept_head_reviewer_user_id", sa.String(length=36), nullable=True))
    op.add_column("expenses", sa.Column("org_owner_approver_user_id", sa.String(length=36), nullable=True))
    op.add_column("expenses", sa.Column("rejection_reason", sa.Text(), nullable=True))
    op.add_column("expenses", sa.Column("payment_status", sa.String(length=20), nullable=False, server_default="unpaid"))
    op.create_index("ix_expenses_department_id", "expenses", ["department_id"], unique=False)
    op.create_index("ix_expenses_vendor_id", "expenses", ["vendor_id"], unique=False)
    op.create_index("ix_expenses_dept_head_reviewer_user_id", "expenses", ["dept_head_reviewer_user_id"], unique=False)
    op.create_index("ix_expenses_org_owner_approver_user_id", "expenses", ["org_owner_approver_user_id"], unique=False)
    op.create_foreign_key("fk_expenses_department_id_departments", "expenses", "departments", ["department_id"], ["id"])
    op.create_foreign_key("fk_expenses_vendor_id_vendors", "expenses", "vendors", ["vendor_id"], ["id"])
    op.create_foreign_key("fk_expenses_dept_head_reviewer_user_id_users", "expenses", "users", ["dept_head_reviewer_user_id"], ["id"])
    op.create_foreign_key("fk_expenses_org_owner_approver_user_id_users", "expenses", "users", ["org_owner_approver_user_id"], ["id"])

    op.add_column("documents", sa.Column("department_id", sa.String(length=36), nullable=True))
    op.add_column("documents", sa.Column("linked_expense_type", sa.String(length=30), nullable=True))
    op.add_column("documents", sa.Column("linked_expense_id", sa.String(length=36), nullable=True))
    op.create_index("ix_documents_department_id", "documents", ["department_id"], unique=False)
    op.create_foreign_key("fk_documents_department_id_departments", "documents", "departments", ["department_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("fk_documents_department_id_departments", "documents", type_="foreignkey")
    op.drop_index("ix_documents_department_id", table_name="documents")
    op.drop_column("documents", "linked_expense_id")
    op.drop_column("documents", "linked_expense_type")
    op.drop_column("documents", "department_id")

    op.drop_constraint("fk_expenses_org_owner_approver_user_id_users", "expenses", type_="foreignkey")
    op.drop_constraint("fk_expenses_dept_head_reviewer_user_id_users", "expenses", type_="foreignkey")
    op.drop_constraint("fk_expenses_vendor_id_vendors", "expenses", type_="foreignkey")
    op.drop_constraint("fk_expenses_department_id_departments", "expenses", type_="foreignkey")
    op.drop_index("ix_expenses_org_owner_approver_user_id", table_name="expenses")
    op.drop_index("ix_expenses_dept_head_reviewer_user_id", table_name="expenses")
    op.drop_index("ix_expenses_vendor_id", table_name="expenses")
    op.drop_index("ix_expenses_department_id", table_name="expenses")
    op.drop_column("expenses", "payment_status")
    op.drop_column("expenses", "rejection_reason")
    op.drop_column("expenses", "org_owner_approver_user_id")
    op.drop_column("expenses", "dept_head_reviewer_user_id")
    op.drop_column("expenses", "expense_type")
    op.drop_column("expenses", "vendor_id")
    op.drop_column("expenses", "department_id")

    op.drop_constraint("fk_budgets_department_id_departments", "budgets", type_="foreignkey")
    op.drop_index("ix_budgets_department_id", table_name="budgets")
    op.drop_column("budgets", "year")
    op.drop_column("budgets", "month")
    op.drop_column("budgets", "scope")
    op.drop_column("budgets", "department_id")

    op.drop_index("ix_ai_chat_messages_organization_id", table_name="ai_chat_messages")
    op.drop_table("ai_chat_messages")
    op.drop_index("ix_ai_chat_sessions_organization_id", table_name="ai_chat_sessions")
    op.drop_table("ai_chat_sessions")
    op.drop_index("ix_payment_priorities_expense_id", table_name="payment_priorities")
    op.drop_index("ix_payment_priorities_organization_id", table_name="payment_priorities")
    op.drop_table("payment_priorities")
    op.drop_index("ix_spend_limits_organization_id", table_name="spend_limits")
    op.drop_table("spend_limits")
    op.drop_index("ix_recurring_expense_requests_organization_id", table_name="recurring_expense_requests")
    op.drop_table("recurring_expense_requests")
    op.drop_index("ix_recurring_expenses_organization_id", table_name="recurring_expenses")
    op.drop_table("recurring_expenses")
    op.drop_index("ix_vendors_organization_id", table_name="vendors")
    op.drop_table("vendors")
