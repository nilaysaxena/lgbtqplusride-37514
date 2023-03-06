from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsCustomAuthenticated(BasePermission):
    def has_permission(self, request, view):
        authenticate = False
        if request.user and request.user.is_authenticated:
            if request.user.is_rider or request.user.is_driver:
                if not request.user.is_mission_statement_accepted:
                    raise PermissionDenied('Mission Statement not Accepted')

                if not request.user.is_payment_terms_accepted:
                    raise PermissionDenied('Payment Terms not Accepted')
                authenticate = True
        return authenticate
