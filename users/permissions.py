from rest_framework import permissions

class IsModer(permissions.BasePermission):
    """Доступ для модераторов"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moders").exists()


class IsModerOrOwner(permissions.BasePermission):
    """Разрешает доступ модераторам или владельцам объекта"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Moders").exists():
            return True
        return IsOwner().has_object_permission(request, view, obj)


class IsOwner(permissions.BasePermission):
    """Разрешает доступ только владельцу курса"""
    def has_object_permission(self, request, view, obj):
        # Для курсов
        if hasattr(obj, "owner_course"):
            return obj.owner_course == request.user
        # Для уроков
        elif hasattr(obj, "owner_lesson"):
            return obj.owner == request.user
        return False
