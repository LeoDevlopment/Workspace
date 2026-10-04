from enum import StrEnum


class Perm(StrEnum):
    # Пользователи
    USERS_VIEW_OWN = "users.view_own"
    USERS_VIEW_COLLEAGUES = "users.view_colleagues"
    USERS_VIEW_ALL = "users.view_all"
    USERS_VIEW_FIRED = "users.view_fired"
    USERS_CREATE = "users.create"
    USERS_EDIT = "users.edit"
    USERS_DELETE = "users.delete"
    USERS_CHANGE_STATUS = "users.change_status"
    USERS_CHANGE_WORKPLACE = "users.change_workplace"
    USERS_CHANGE_POSITION = "users.change_position"
    USERS_MAKE_CARD_PUBLIC = "users.make_card_public"
    USERS_MANAGE_ROLES = "users.manage_roles"
    USERS_MANAGE_PERMISSIONS = "users.manage_permissions"

    # Роли
    ROLES_VIEW = "roles.view"
    ROLES_CREATE = "roles.create"
    ROLES_EDIT = "roles.edit"
    ROLES_DELETE = "roles.delete"
    ROLES_MANAGE_PERMISSIONS = "roles.manage_permissions"

    # Должности
    POSITIONS_VIEW = "positions.view"
    POSITIONS_CREATE = "positions.create"
    POSITIONS_EDIT = "positions.edit"
    POSITIONS_DELETE = "positions.delete"

    # Места работы
    WORKPLACES_VIEW = "workplaces.view"
    WORKPLACES_CREATE = "workplaces.create"
    WORKPLACES_EDIT = "workplaces.edit"
    WORKPLACES_DELETE = "workplaces.delete"
    WORKPLACES_ASSIGN_USERS = "workplaces.assign_users"
    WORKPLACES_UPLOAD_PHOTO = "workplaces.upload_photo"

    # Документы
    DOCUMENTS_VIEW_OWN = "documents.view_own"
    DOCUMENTS_VIEW_WORKPLACE = "documents.view_workplace"
    DOCUMENTS_VIEW_ALL = "documents.view_all"
    DOCUMENTS_UPLOAD_USER = "documents.upload_user"
    DOCUMENTS_UPLOAD_WORKPLACE = "documents.upload_workplace"
    DOCUMENTS_DELETE = "documents.delete"
    DOCUMENTS_GRANT_ACCESS = "documents.grant_access"

    # Оценки
    RATINGS_VIEW = "ratings.view"
    RATINGS_CREATE = "ratings.create"
    RATINGS_EDIT = "ratings.edit"

    # Комментарии
    COMMENTS_VIEW = "comments.view"
    COMMENTS_CREATE = "comments.create"
    COMMENTS_EDIT = "comments.edit"
    COMMENTS_DELETE = "comments.delete"

    # Дашборд и резерв
    DASHBOARD_VIEW = "dashboard.view"
    DASHBOARD_VIEW_ARCHIVE = "dashboard.view_archive"
    PERSONNEL_RESERVE_VIEW = "personnel_reserve.view"

    # Аудит
    AUDIT_VIEW = "audit.view"


# Права, которые получает системная роль user
DEFAULT_USER_PERMISSIONS: set[Perm] = {
    Perm.USERS_VIEW_OWN,
    Perm.USERS_VIEW_COLLEAGUES,
    Perm.DOCUMENTS_VIEW_OWN,
}

# Права роли user, которые нельзя расширять через кастомные роли по умолчанию
SYSTEM_ROLE_ADMIN = "admin"
SYSTEM_ROLE_USER = "user"