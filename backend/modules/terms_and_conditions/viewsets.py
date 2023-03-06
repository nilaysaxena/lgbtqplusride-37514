from rest_framework import authentication
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser
from .models import TermAndCondition
from .serializers import TermAndConditionSerializer
from rest_framework import viewsets


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class TermAndConditionViewSet(viewsets.ModelViewSet):
    serializer_class = TermAndConditionSerializer
    permission_classes = [IsAdminUser | ReadOnly]  # Makes it Read-only unless admin
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    http_method_names = ['get']

    # This query will only return a single (if it exists) T&C string, and that will be 
    # the most recently updated one that *also* has an active flag. You must set at least
    # one T&C object to active for this to work.
    def get_queryset(self):
        qry_type = self.request.query_params.get('type', 'DEFAULT')
        qry = TermAndCondition.objects.filter(is_active=True, type=qry_type).order_by('-updated_at')[0:1]
        return qry
