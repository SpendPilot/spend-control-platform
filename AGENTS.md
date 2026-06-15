PROJECT_NAME: SpendPilot

You are a professional prompt engineer, senior full-stack software engineer, DevOps engineer, cloud engineer, database engineer, Azure SaaS engineer, product architect, and refactoring engineer.

I need you to refactor my existing original SpendPilot project into a complete business payment operations platform.

Very important current project status:

* This is still the original SpendPilot repository.
* I have NOT yet run the repo-splitting phases.
* I have NOT yet run the CI/CD refactor phases.
* I have NOT yet run the Terraform/Helm/GitOps restructuring phases.
* I will run those prompts only after this product/application refactor is completed.
* Therefore, do NOT assume the repo is already split.
* Do NOT split the repo in this run.
* Do NOT move the app into multiple repos in this run.
* Do NOT redesign Terraform, Helm, GitOps, or CI/CD unless absolutely required to keep the current app build working.
* Keep the current project structure compatible with future repo-splitting and CI/CD refactor prompts.

Current SpendPilot context:

* SpendPilot already exists.
* It is a multi-tenant SaaS application.
* It already has authentication.
* It already has tenant/company behavior.
* The first person who logs into a tenant/company becomes org_owner.
* This first-user org_owner logic is already built.
* Do not break the first-user org_owner logic.
* The project may already have bill upload, document extraction, Azure Document Intelligence, AI features, dashboards, policies/rules, approvals, or expense features.
* Reuse working code where possible.
* Refactor weak or outdated code safely.
* Remove redundant code only after replacement is validated.
* Do not delete secrets, environment files, production configs, Terraform state, kubeconfigs, certificates, or unknown sensitive files.
* Do not run destructive database migrations without explicit approval.
* Do not run terraform apply.

AI context and multi-agent requirements:
This project already has AI context files somewhere in the repository. You must find them, read them, use them, and update them properly.

Before changing application code:

1. Search the repository for AI/context files and agent instruction files.
2. Look for files/folders such as:

   * AI_CONTEXT.md
   * CURRENT_STATE.md
   * TARGET_ARCHITECTURE.md
   * DECISIONS.md
   * REFACTOR_PLAN.md
   * RISK_REGISTER.md
   * MIGRATION_CHECKLIST.md
   * CLEANUP_STRATEGY.md
   * SERVICE_BOUNDARIES.md
   * SERVICE_SPLIT_READINESS.md
   * REPO_SPLIT_PLAN.md
   * CLEANUP_PLAN.md
   * CLEANUP_REPORT.md
   * FINAL_REFACTOR_SUMMARY.md
   * FINAL_FOLDER_STRUCTURE.md
   * FINAL_OPERATIONS_GUIDE.md
   * AGENTS.md
   * CONTRIBUTING.md
   * docs/
   * .ai/
   * ai-context/
   * .codex/
   * .cursor/
   * any project memory or architecture notes
3. Create or update AI_CONTEXT_INDEX.md if it does not exist.
4. AI_CONTEXT_INDEX.md must list:

   * all discovered context files
   * purpose of each context file
   * which file is the source of truth for architecture
   * which file is the source of truth for current implementation state
   * which file tracks decisions
   * which file tracks cleanup
   * which file tracks risks
   * which file future agents should read first
5. Do not blindly overwrite existing context files.
6. Preserve useful historical decisions.
7. Add date-stamped notes when updating context.
8. If multiple context files conflict, document the conflict in DECISIONS.md or RISK_REGISTER.md before choosing a direction.
9. Keep context concise but useful. Do not dump huge code blocks into context files.
10. Future agents should be able to continue the project by reading the context files.

AI context best practices to follow:

* Maintain a clear source-of-truth hierarchy.
* Keep product decisions separate from implementation notes.
* Keep architecture decisions separate from task checklists.
* Keep cleanup decisions traceable.
* Use ADR-style decision notes when making major choices.
* Keep CURRENT_STATE.md updated after each phase.
* Keep IMPLEMENTATION_CHECKLIST.md updated with completed and pending tasks.
* Keep RISK_REGISTER.md updated with blockers and dangerous areas.
* Keep CLEANUP_REFOCUS_PLAN.md updated before deleting anything.
* Keep FINAL_* reports only for completed validated work.
* Do not mark work complete unless validated or clearly documented as unvalidated.
* Support multiple agents by documenting what was changed, what remains, and what should not be touched.

Multi-agent coordination rules:

* Before starting a phase, read AI_CONTEXT_INDEX.md and CURRENT_STATE.md.
* Before modifying a major area, check whether another context file describes that area.
* After finishing a phase, update CURRENT_STATE.md, IMPLEMENTATION_CHECKLIST.md, and relevant decision/cleanup docs.
* If a task is partially done, clearly mark it as PARTIAL.
* If something is unsafe to change, mark it as REVIEW.
* If something is removed, document why and where references were checked.
* Do not leave ambiguous TODOs without owner/context.
* Do not create duplicate competing context files unless needed.
* Prefer updating existing context files over creating many random docs.

New product direction:
SpendPilot must become a centralized business payment operations platform for companies.

The company has two main types of costs:

1. Recurring monthly costs
   These are costs that must be paid every month or on a fixed schedule.

Examples:

* software subscriptions
* infrastructure costs
* physical infrastructure costs
* rent
* utilities
* internet
* SaaS tools
* maintenance contracts
* cloud bills
* office recurring payments

2. Variable expenses
   These are expenses that vary every month and are usually submitted by employees or department heads.

Examples:

* travel
* food
* utilities
* maintenance
* office supplies
* team-specific expenses
* one-time purchases

SpendPilot should help the company:

* track recurring expenses
* track variable expenses
* upload bills
* extract bill details
* manage approvals
* manage company budget
* manage department budgets
* manage spend limits
* prioritize payments
* understand weekly and monthly cash outflow
* understand which payments are urgent
* understand which bills can wait
* understand whether paying everything now will hurt cash flow
* manage departments and department heads
* provide AI insights about cash flow, spending, budget usage, profit/loss if revenue data exists, and payment suggestions

Default departments:

* IT
* Marketing
* HR

Use only these three default departments for now.

If the existing project already has departments, adapt or migrate safely to support these default departments.
Prefer a flexible departments table instead of hardcoding department behavior everywhere.

Core roles:

1. org_owner
2. dept_head
3. employee

Role behavior:

* First user in a tenant/company is org_owner. This already exists. Preserve it.
* Every user who logs in after the org_owner should become employee by default.
* On first login, an employee must choose their department from IT, Marketing, or HR.
* After choosing department, the employee can access employee-level features.
* org_owner can later promote one employee from each department to dept_head.
* dept_head is not a separate database role like it_head, marketing_head, or hr_head unless the existing app strongly requires that.
* Prefer role = dept_head with department_id.
* In the UI, display department heads as IT Head, Marketing Head, or HR Head based on their department.
* A department should have only one active dept_head unless the existing code already supports multiple department heads safely.
* org_owner can demote a dept_head back to employee.
* org_owner can remove/deactivate users.
* org_owner can change a user’s department.
* dept_head can only access their own department data.
* employee can only access their own data and limited department budget information.
* org_owner can access all company/tenant data.
* All backend queries must be tenant-scoped.
* Cross-tenant data access must be impossible.

Do not create a new_user role for this version.
The final behavior should be:

* first user = org_owner
* all later users = employee
* employee must choose department on first login
* org_owner may promote employee to dept_head later

Main org_owner tabs/pages:

1. Dashboard
   Purpose:
   Company-wide dashboard with graphs, statistics, and complete expense analysis.

Must show:

* total spend this month
* recurring spend this month
* variable spend this month
* pending approvals
* approved expenses
* rejected expenses
* company budget used
* company budget remaining
* department-wise spend
* category-wise spend
* recurring vs variable chart
* monthly spend trend graph
* upcoming payment summary
* cash outflow this week
* cash outflow this month

2. Expenses
   Purpose:
   Show all company expenses.

This page must have two clear sections:

A. Recurring Expenses

* created by org_owner
* org_owner can create recurring expense
* org_owner can edit recurring expense
* org_owner can pause/delete recurring expense
* org_owner can upload/link bills to recurring expenses if useful
* recurring expenses should have vendor, category, amount, billing cycle, due date, next due date, priority, and status

B. Variable Expenses

* submitted by employees or department heads by uploading bills
* variable expenses go through approval workflow
* org_owner can approve or reject variable expenses forwarded by dept_head
* show submitter, department, category, vendor, amount, bill, extraction status, approval state, and comments

3. Spend Limits
   Purpose:
   Business spend limits for employees, departments, and categories.

This replaces the generic policy/rules idea with simple business-friendly limits.

Must support:

* per-employee monthly request limit
* per-department monthly limit
* per-category limit
* max single expense amount
* approval threshold amount
* allowed categories
* recurring expense creation restriction
* variable expense approval rules

Examples:

* Travel above ₹10,000 requires org_owner approval.
* Food above ₹2,000 requires dept_head review.
* Employees cannot submit more than ₹25,000 per month.
* Only org_owner can directly create recurring expenses.
* dept_head must request org_owner approval for recurring expenses.

4. Payment Priority / Cash Outflow
   Purpose:
   Help org_owner decide what to pay first.

Must show:

* how much cash will go out this week
* how much cash will go out this month
* urgent payments
* overdue payments
* recurring bills due soon
* approved variable expenses waiting for payment
* bills that can wait
* whether paying everything now will hurt the company monthly budget
* vendor payments that may block operations

Payment priority categories:

* Pay now
* Pay this week
* Can wait
* Needs review
* Blocked

Priority ranking should consider:

* due date
* recurring vs variable type
* vendor importance
* business criticality
* department
* amount
* approval status
* budget availability
* overdue status

5. AI Insights
   Purpose:
   AI chatbot/assistant for finance and cash-flow insights.

AI should answer:

* How is my cash flow this month?
* Are we overspending?
* Which department is spending the most?
* Which recurring payments are coming soon?
* Which payments are urgent?
* Which bills can wait?
* Will paying all pending bills hurt this month’s budget?
* Are we likely to exceed the company budget?
* Which expenses should I review first?
* Are we in profit or loss if revenue data exists?

AI rules:

* Use only current tenant/company data.
* Never expose another tenant’s data.
* Do not invent financial facts.
* Clearly say when data is missing.
* Do not give legal or tax advice as fact.
* Ground responses in expenses, bills, budgets, departments, approvals, and payment priorities.
* Provide practical suggestions.
* Store AI chat history only tenant-scoped and user-scoped.
* Avoid sending secrets, raw tokens, private config, or unnecessary PII to AI services.

6. Budgets
   Purpose:
   Allow org_owner to manage budgets.

Must support:

* company monthly budget
* IT department monthly budget
* Marketing department monthly budget
* HR department monthly budget
* budget used
* budget remaining
* budget exceeded warning
* budget history
* edit/update budget

Important:

* org_owner sets the total company monthly budget.
* org_owner also sets individual department budgets.
* dept_head and employee can only view the budget for their own department.

7. Bills Library
   Purpose:
   Show all uploaded bills with filters.

Filters:

* date range
* department
* employee
* category
* recurring/variable
* approval status
* vendor
* amount range
* extraction status
* payment status

Each bill should show:

* uploaded file
* extracted fields
* linked expense
* submitter
* department
* approval state
* created date
* updated date

8. Manage Departments & Users
   Purpose:
   Allow org_owner to manage users, departments, and department heads.

Must show:

* departments: IT, Marketing, HR
* department budget summary
* current department head
* users by department
* all employees
* promote employee to dept_head
* demote dept_head to employee
* change user department
* remove/deactivate user
* user role
* user status

Rules:

* Every user after org_owner starts as employee.
* Employee chooses department on first login.
* org_owner can promote one employee from each department to dept_head.
* org_owner can remove or deactivate users.
* dept_head is scoped only to assigned department.

9. Profile
   Purpose:
   Org owner profile/settings.

Must show:

* name
* email
* company/tenant name
* role
* preferences
* profile update if supported

Main dept_head tabs/pages:

1. Department Dashboard
   Purpose:
   Show only the department-specific dashboard.

Must show:

* department monthly budget set by org_owner
* used budget
* remaining budget
* pending employee expense requests
* approved expenses
* rejected expenses
* forwarded-to-org-owner expenses
* recurring expense requests
* variable expenses
* category-wise department spend
* monthly trend graph
* upcoming department payments if applicable

2. Expense Upload & Review
   Purpose:
   Dept_head can request recurring expenses and review employee variable expenses.

This page must have two sections:

A. Recurring Expense Request
Flow:

* dept_head cannot directly create recurring expenses.
* dept_head can request org_owner approval for a recurring expense.
* request includes vendor, amount, category, billing cycle, reason, and optional bill.
* org_owner approves or rejects the recurring expense request.
* if org_owner approves it, it becomes an approved recurring expense or approved recurring expense record for that department.
* dept_head can see request status.

Statuses:

* pending with org_owner
* approved by org_owner
* rejected by org_owner

B. Variable Expense Review
Flow:

* employees submit variable expenses to their department.
* dept_head reviews employee variable expense requests.
* dept_head can reject the request.
* dept_head can forward the request to org_owner for final approval.
* dept_head should see full status.

Statuses:

* pending with dept_head
* rejected by dept_head
* forwarded to org_owner
* approved by org_owner
* rejected by org_owner
* paid if payment tracking exists

Important:

* dept_head does not perform final approval/payment by default.
* Final approval should normally belong to org_owner.
* If existing app already has different approval rules, adapt carefully and document the decision.

3. Department Profile
   Purpose:
   Show department details.

Must show:

* department name
* department head
* assigned users
* monthly budget
* used budget
* remaining budget
* department categories if any

Main employee flow/pages:

Employee first-login onboarding:

* After login, employee must choose department: IT, Marketing, or HR.
* After choosing department, employee is assigned that department.
* Employee remains role employee.
* Employee cannot become dept_head by themselves.
* Only org_owner can promote employee to dept_head.

1. Department Budget
   Purpose:
   Show employee their own department budget summary.

Must show:

* department budget
* used amount
* remaining amount
* simple graph/statistics
* employee must not see other departments

2. Upload Variable Expense
   Purpose:
   Employee can upload variable expenses only.

Rules:

* employee can only upload variable expenses
* employee cannot request recurring expenses
* employee cannot create recurring expenses
* employee uploads bill and submits request to dept_head
* employee can see request status

Variable expense examples:

* travel
* food
* maintenance
* utilities
* office supplies
* one-time team expenses

Form fields:

* category
* vendor
* amount
* expense date
* description/reason
* bill/document upload
* department auto-filled
* submitter auto-filled

Employee-visible statuses:

* pending with dept_head
* rejected by dept_head
* forwarded to org_owner
* approved by org_owner
* rejected by org_owner
* paid if payment tracking exists

3. Profile
   Purpose:
   Show employee profile.

Must show:

* name
* email
* department
* role
* submitted expense count
* pending/approved/rejected summary if useful

Data model requirements:
Design or update models safely based on existing code.

Suggested entities:

* tenants
* users
* departments
* expense_categories
* recurring_expenses
* recurring_expense_requests
* variable_expenses
* bills
* bill_extractions
* approvals
* approval_comments
* spend_limits
* budgets
* payment_priorities
* vendors
* ai_chat_sessions
* ai_chat_messages
* audit_events

User:

* id
* tenant_id
* auth_provider_subject / entra_id / provider_user_id if applicable
* email
* name
* role: org_owner/dept_head/employee
* department_id nullable
* onboarding_completed boolean
* status active/inactive
* created_at
* updated_at

Department:

* id
* tenant_id
* name
* description
* department_head_user_id nullable
* created_at
* updated_at

RecurringExpense:

* id
* tenant_id
* department_id nullable
* vendor_id nullable
* name
* category
* amount
* billing_cycle monthly/quarterly/yearly/custom
* due_day
* next_due_date
* priority
* criticality
* status active/paused/deleted
* created_by
* created_at
* updated_at

RecurringExpenseRequest:

* id
* tenant_id
* department_id
* requested_by
* vendor
* name
* category
* estimated_amount
* billing_cycle
* reason
* bill_id nullable
* status pending/approved/rejected
* approved_by nullable
* approved_at nullable
* rejection_reason nullable
* created_at
* updated_at

VariableExpense:

* id
* tenant_id
* department_id
* submitted_by
* vendor_id nullable
* category
* amount
* expense_date
* description
* bill_id
* status pending_dept_head/rejected_by_dept_head/forwarded_to_org_owner/approved_by_org_owner/rejected_by_org_owner/paid
* dept_head_reviewer_id nullable
* org_owner_approver_id nullable
* rejection_reason nullable
* created_at
* updated_at

Bill:

* id
* tenant_id
* uploaded_by
* department_id
* file_url/path/reference
* original_filename
* mime_type
* extraction_status
* linked_expense_type recurring_request/recurring_expense/variable_expense
* linked_expense_id nullable
* created_at
* updated_at

BillExtraction:

* id
* bill_id
* tenant_id
* vendor_name
* invoice_number
* invoice_date
* total_amount
* tax_amount
* currency
* extracted_line_items JSON if supported
* confidence_score
* raw_extraction JSON if safe
* created_at

SpendLimit:

* id
* tenant_id
* department_id nullable
* user_id nullable
* category nullable
* max_single_expense_amount
* monthly_limit
* requires_approval_above_amount
* created_by
* active
* created_at
* updated_at

Budget:

* id
* tenant_id
* scope company/department
* department_id nullable
* month
* year
* amount
* used_amount calculated or materialized
* created_by
* created_at
* updated_at

PaymentPriority:

* id
* tenant_id
* expense_type recurring/variable
* expense_id
* priority pay_now/pay_this_week/can_wait/needs_review/blocked
* reason
* due_date
* estimated_cash_out_date
* created_at
* updated_at

Approval:

* id
* tenant_id
* target_type recurring_request/variable_expense
* target_id
* requested_by
* approver_id
* status pending/forwarded/approved/rejected
* comments
* decided_at
* created_at

Vendor:

* id
* tenant_id
* name
* category
* criticality low/medium/high/critical
* contact_info optional
* created_at
* updated_at

AIChatSession:

* id
* tenant_id
* user_id
* title
* created_at
* updated_at

AIChatMessage:

* id
* tenant_id
* session_id
* role user/assistant/system
* content
* grounded_context JSON if safe
* created_at

AuditEvent:

* id
* tenant_id
* actor_user_id
* action
* target_type
* target_id
* metadata JSON
* created_at

Backend/API requirements:

Auth/current user:

* get current user
* get current user role/access
* preserve first-user org_owner behavior
* default later users to employee
* first-login employee department selection
* complete employee onboarding
* role-based access checks

Departments/users:

* ensure default departments exist: IT, Marketing, HR
* list departments
* update department
* list users
* list users by department
* promote employee to dept_head
* demote dept_head to employee
* change user department
* remove/deactivate user
* get department profile

Budgets:

* create/update company monthly budget
* create/update department monthly budget
* get company budget dashboard
* get department budget dashboard
* get budget usage

Recurring expenses:

* create recurring expense by org_owner
* update recurring expense by org_owner
* pause/delete recurring expense by org_owner
* list recurring expenses
* create recurring expense request by dept_head
* approve/reject recurring expense request by org_owner

Variable expenses:

* upload variable expense by employee
* upload variable expense by dept_head if allowed
* list own variable expenses
* list department variable expenses for dept_head
* dept_head reject variable expense
* dept_head forward variable expense to org_owner
* org_owner approve/reject variable expense
* list all variable expenses for org_owner

Bills:

* upload bill
* process bill extraction if document extraction exists
* list bills with filters
* get bill details
* link bill to recurring/variable expense

Spend limits:

* create spend limit
* update spend limit
* list spend limits
* evaluate expense against spend limits before submission/approval

Payment priority:

* calculate weekly cash outflow
* calculate monthly cash outflow
* rank payments
* show urgent payments
* show bills that can wait
* show payments blocking operations
* show budget impact before approving/paying

AI:

* ask AI finance assistant
* get AI chat history
* generate dashboard insights
* generate cash-flow suggestions

Audit:

* log sensitive actions
* list audit events for org_owner

Frontend requirements:

Routing:

* org_owner sees org_owner layout.
* dept_head sees dept_head layout for their department.
* employee sees employee layout.
* employee without department assignment sees first-login department selection page.
* unauthorized access redirects to a safe page.
* all pages enforce role, department, and tenant access.

Org owner navigation:

1. Dashboard
2. Expenses
3. Spend Limits
4. Payment Priority
5. AI Insights
6. Budgets
7. Bills Library
8. Manage Departments & Users
9. Profile

Dept head navigation:

1. Department Dashboard
2. Expense Upload & Review
3. Department Profile

Employee navigation:

1. Department Budget
2. Upload Variable Expense
3. Profile

UI requirements:

* dashboard cards
* charts/graphs for spend trends
* recurring vs variable chart
* department-wise spend chart
* category-wise spend chart
* budget progress bars
* approval status badges
* filters for bills and expenses
* upload forms
* review/approve/reject actions
* clear empty states
* loading states
* error states
* role-based buttons/actions

Document extraction requirements:
If existing bill/document extraction exists:

* reuse it
* connect extracted fields to Bill and Expense models
* show extraction status
* show extracted vendor, invoice number, date, total amount, tax amount, line items if available
* allow review/edit of extracted fields if feasible
* do not remove working extraction code

If document extraction does not exist:

* create a clean abstraction/stub for later integration
* do not hardcode Azure credentials

Implementation order for this product refactor:

Phase -1: AI context discovery and multi-agent setup

1. Search the full repository for existing AI context and agent instruction files.
2. Read all discovered context files before changing code.
3. Create or update AI_CONTEXT_INDEX.md.
4. Create or update CURRENT_STATE.md.
5. Create or update IMPLEMENTATION_CHECKLIST.md.
6. Create or update RISK_REGISTER.md.
7. Create or update DECISIONS.md.
8. Document that this repo has not yet gone through repo-splitting/CICD/infra refactor.
9. Document that this product refactor must remain compatible with future repo split.
10. Do not change application code in this phase unless needed to inspect/build.

Phase 0: Context and current-state scan

1. Read AI_CONTEXT_INDEX.md and all source-of-truth context docs.
2. Scan frontend, backend, services, database, routes, env vars, tests, and deployment files.
3. Identify current auth/tenant logic.
4. Identify current first-user org_owner logic.
5. Identify current bill upload/document extraction logic.
6. Identify current expense/budget/rule/approval logic.
7. Create PRODUCT_REFOCUS_PLAN.md.
8. Create CURRENT_FEATURE_MAP.md.
9. Update IMPLEMENTATION_CHECKLIST.md.
10. Do not delete anything.

Phase 1: Identity, roles, and department onboarding

1. Preserve current authentication.
2. Preserve first-user org_owner logic.
3. Add/update roles: org_owner, dept_head, employee.
4. Ensure users after org_owner default to employee.
5. Add first-login department selection for employees.
6. Add department assignment model.
7. Seed or ensure default departments: IT, Marketing, HR.
8. Add org_owner ability to promote/demote dept_head.
9. Add role-based access middleware/guards.
10. Add tenant-scoped authorization checks.
11. Add tests if possible.
12. Update CURRENT_STATE.md, IMPLEMENTATION_CHECKLIST.md, DECISIONS.md, and RISK_REGISTER.md.

Phase 2: Data model and migrations

1. Add/update models for departments, users, recurring expenses, recurring expense requests, variable expenses, bills, bill extractions, approvals, budgets, spend limits, vendors, payment priorities, AI chat, and audit events.
2. Preserve reusable existing models.
3. Create safe migrations.
4. Do not run destructive migrations automatically.
5. Document migration steps in DATA_MODEL_CHANGELOG.md.
6. Update AI context files after the phase.

Phase 3: Backend APIs

1. Implement current-user and department selection APIs.
2. Implement department/user management APIs.
3. Implement budget APIs.
4. Implement recurring expense APIs.
5. Implement recurring expense request APIs.
6. Implement variable expense APIs.
7. Implement approval workflow APIs.
8. Implement bill library APIs.
9. Implement spend limit APIs.
10. Implement payment priority APIs.
11. Implement AI assistant APIs.
12. Implement audit logging.
13. Add/update backend tests.
14. Update AI context files after the phase.

Phase 4: Frontend role-based layouts

1. Implement role-based routing.
2. Implement employee first-login department selection.
3. Implement org_owner layout/navigation.
4. Implement dept_head layout/navigation.
5. Implement employee layout/navigation.
6. Protect pages by role, department, and tenant.
7. Update AI context files after the phase.

Phase 5: Org owner features

1. Build org_owner dashboard.
2. Build expenses page with recurring and variable sections.
3. Build spend limits page.
4. Build payment priority/cash outflow page.
5. Build AI insights page.
6. Build budgets page.
7. Build bills library page.
8. Build manage departments/users page.
9. Build org_owner profile page.
10. Update AI context files after the phase.

Phase 6: Dept head features

1. Build department dashboard.
2. Build expense upload/review page.
3. Implement recurring expense request flow.
4. Implement employee variable expense review flow.
5. Implement reject/forward-to-org-owner flow.
6. Build department profile page.
7. Update AI context files after the phase.

Phase 7: Employee features

1. Build employee department budget view.
2. Build variable expense upload page.
3. Show request status lifecycle.
4. Build employee profile page.
5. Update AI context files after the phase.

Phase 8: Document extraction integration

1. Connect existing document extraction to bill upload.
2. Store extracted bill data.
3. Show extraction status.
4. Allow review/edit if feasible.
5. Link bills to recurring requests, recurring expenses, or variable expenses.
6. Add tests/mocks.
7. Update AI context files after the phase.

Phase 9: Payment priority and cash flow logic

1. Calculate weekly cash outflow.
2. Calculate monthly cash outflow.
3. Rank payments by urgency.
4. Identify bills that can wait.
5. Identify payments blocking operations.
6. Show budget impact before approving/paying.
7. Add tests.
8. Update AI context files after the phase.

Phase 10: AI insights

1. Ground AI responses in tenant data.
2. Add prompt/context builder.
3. Add cash-flow summary.
4. Add budget usage summary.
5. Add department spend summary.
6. Add urgent payment explanation.
7. Add practical suggestions.
8. Add tests/mocks.
9. Update AI context files after the phase.

Phase 11: Cleanup

1. Identify old redundant files, pages, APIs, models, docs, and workflows.
2. Create CLEANUP_REFOCUS_PLAN.md.
3. Classify each item as KEEP / MOVE / MERGE / DELETE / REVIEW.
4. Search references before deleting.
5. Remove only safe DELETE items.
6. Do not remove auth/tenant/org_owner logic unless replacement is validated.
7. Do not remove document extraction code if still useful.
8. Do not remove deployment files unless replaced.
9. Create FINAL_CLEANUP_REPORT.md.
10. Update AI context files after the phase.

Phase 12: Validation
Run or document:

* frontend install
* frontend lint/typecheck
* frontend tests
* frontend build
* backend install
* backend tests
* service-level tests if applicable
* API tests
* database migration validation
* auth tests
* role access tests
* tenant isolation tests
* first-user org_owner tests
* employee default-role tests
* employee department selection tests
* dept_head promotion tests
* bill upload tests
* document extraction tests/mocks
* approval workflow tests
* budget calculation tests
* payment priority tests
* AI assistant tests/mocks
* Docker builds if applicable
* current deployment compatibility if affected
* repository-wide search for removed paths
* repository-wide search for stale old feature names
* AI context consistency check

Phase 13: Final documentation
Create/update:

1. FINAL_PRODUCT_SUMMARY.md
2. FINAL_FEATURE_MAP.md
3. FINAL_ROLE_ACCESS_MATRIX.md
4. FINAL_API_MAP.md
5. FINAL_DATA_MODEL.md
6. FINAL_OPERATIONS_GUIDE.md
7. FINAL_CLEANUP_REPORT.md
8. FINAL_AI_CONTEXT_HANDOFF.md

FINAL_AI_CONTEXT_HANDOFF.md must include:

* source-of-truth context files
* completed phases
* incomplete phases
* files changed
* risky areas
* known bugs
* validation results
* next recommended prompt
* whether the project is ready for later repo-splitting/CICD/infra refactor prompts

Final output:
At the end, summarize:

1. What changed.
2. What existing functionality was preserved.
3. What org_owner features were added.
4. What dept_head features were added.
5. What employee behavior was added.
6. What document extraction integration was preserved or added.
7. What AI context files were found and updated.
8. What was cleaned up.
9. What was validated.
10. What could not be validated.
11. What files remain under REVIEW.
12. Whether the project is ready for the later repo-splitting/CICD/infra refactor prompts.
13. The next safest step.

For this first Codex run:
Execute only Phase -1, Phase 0, and Phase 1.
Do not implement all features yet.
Do not delete old files yet.
Do not split the repo.
Do not modify Terraform, Helm, GitOps, or CI/CD unless required for documentation only.
Focus on AI context discovery, current-state scan, product refocus planning, preserving first-user org_owner logic, role logic, department onboarding, access control design, and safe implementation checklist.


<!-- Future refactor note:
Do not execute repo split, Terraform, Helm, GitOps, or CI/CD restructure during the current product refactor.

After the product refactor is validated and committed, run the separate repository/platform restructure prompt.

The current priority is:
1. preserve existing auth and first-user org_owner logic
2. implement SpendPilot business payment operations features
3. validate product behavior
4. update AI context files
5. cleanup only product-level redundant files -->