from enum import StrEnum


class UserStatusCode(StrEnum):
    EMPLOYED = "employed"
    FIRED = "fired"
    VACATION = "vacation"
    SICK = "sick"


class OwnerType(StrEnum):
    USER = "user"
    WORKPLACE = "workplace"


class SubjectType(StrEnum):
    USER = "user"
    ROLE = "role"


class PermissionEffect(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


class DashboardPeriodStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"