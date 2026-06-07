ROLE_PLATFORM_ADMIN = "platform_admin"
ROLE_ORG_ADMIN = "org_admin"
ROLE_FINANCE_MANAGER = "finance_manager"
ROLE_APPROVER = "approver"
ROLE_AUDITOR = "auditor"
ROLE_EMPLOYEE = "employee"

ALL_ROLES = {
    ROLE_PLATFORM_ADMIN,
    ROLE_ORG_ADMIN,
    ROLE_FINANCE_MANAGER,
    ROLE_APPROVER,
    ROLE_AUDITOR,
    ROLE_EMPLOYEE,
}

ADMIN_ROLES = {ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN}
FINANCE_WRITE_ROLES = {ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN, ROLE_FINANCE_MANAGER}
APPROVAL_ROLES = {ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN, ROLE_FINANCE_MANAGER, ROLE_APPROVER}
ORG_READ_ROLES = {ROLE_PLATFORM_ADMIN, ROLE_ORG_ADMIN, ROLE_FINANCE_MANAGER, ROLE_APPROVER, ROLE_AUDITOR}

ROLE_ALIASES = {
    "admin": ROLE_ORG_ADMIN,
    "auditor": ROLE_AUDITOR,
    "approver": ROLE_APPROVER,
    "employee": ROLE_EMPLOYEE,
    "finance_admin": ROLE_FINANCE_MANAGER,
    "finance_manager": ROLE_FINANCE_MANAGER,
    "org_admin": ROLE_ORG_ADMIN,
    "platform_admin": ROLE_PLATFORM_ADMIN,
    "user": ROLE_EMPLOYEE,
}


def normalize_role(raw_role: str | None) -> str:
    if not raw_role:
        return ROLE_EMPLOYEE
    return ROLE_ALIASES.get(raw_role.strip().lower(), ROLE_EMPLOYEE)


def derive_highest_role(roles: list[str] | set[str] | tuple[str, ...]) -> str:
    normalized = {normalize_role(role) for role in roles}
    for role in (
        ROLE_PLATFORM_ADMIN,
        ROLE_ORG_ADMIN,
        ROLE_FINANCE_MANAGER,
        ROLE_APPROVER,
        ROLE_AUDITOR,
        ROLE_EMPLOYEE,
    ):
        if role in normalized:
            return role
    return ROLE_EMPLOYEE
