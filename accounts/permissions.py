from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManager(BasePermission):
    message = 'Only Motorpool Managers can perform this action.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_manager
        )

class IsAuditor(BasePermission):
    message = 'Access restricted to Auditors only.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_auditor
        )

class IsManagerOrAuditor(BasePermission):
    message = 'Access restricted to Managers and Auditors only.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_manager:
            return True
        if user.is_auditor and request.method in SAFE_METHODS:
            return True
        return False

class IsManagerOrReadOnly(BasePermission):
    message = 'Only Motorpool Managers can modify records.'

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_manager

class IsOwnerOrManager(BasePermission):
    message = 'You do not have permission to access this record.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_manager:
            return True
        if request.method in SAFE_METHODS:
            return obj.requested_by == request.user
        return False

class CanViewCosts(BasePermission):
    message = 'Financial data is restricted to Motorpool Managers only.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.can_view_costs
        )