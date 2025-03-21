"""Permissions classes"""

import logging
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import BasePermission

from .utils import deep_get

logger = logging.getLogger(__name__)


class HasAPIGroupPermission(BasePermission):
    """
    API permissions class that grants permission if the authenticated user is
    in a specific django auth group.

    The functionality of this permissions class can be customized by adding a
    `required_groups` attribute to the API view. This attribute should be a
    dict with a mapping from HTTP methods as the keys to a list of django auth
    group names that have permission for that method. For example:

        class MyAPIView(APIView):
            ...
            required_groups = {
                'GET': ['GetPeopleGroup', 'HeadPeopleGroup'],
                'POST': ['SecretPostGroup'],
            }
            ...

    By default the 'API' group is granted permission to all HTTP methods.
    """

    def has_permission(self, request, view):
        """Override"""
        required_groups_mapping = getattr(view, 'required_groups', {})
        required_groups = required_groups_mapping.get(request.method, ['API'])
        return request.user.groups.filter(name__in=required_groups).count() > 0


class PermissionABC(type(BasePermission), type(ABC)):
    """
    Since BasePermission and ABC have two separate metaclasses, we create
    a single metaclass that inherits from both metaclasses
    """


class TokenHasRole(BasePermission, ABC, metaclass=PermissionABC):
    """
    This class is to be subclassed and its inteface implemented
    in order to check roles provided in an APIView (or subclass)
    against the roles found in a JWT token.
    """

    @property
    @abstractmethod
    def role_attribute_name(self):
        """
        Each Permission that implements TokenHasRole needs to specify the
        name of the attribute where roles are stored.
        """

    @abstractmethod
    def get_roles_from_token(self, token_payload):
        """
        Extract the pertinent roles provided in the JWT
        """

    @abstractmethod
    def has_required_roles(self, provided_roles, required_roles):
        """
        Checks to see if the client has the necessary roles required to access
        the APIView
        """

    def get_roles(self, view):
        """
        Get the list of roles from the APIView
        """
        try:
            return getattr(view, self.role_attribute_name)
        except AttributeError as e:
            raise ImproperlyConfigured(
                f'{type(self).__name__} requires the view to define the '
                f'{self.role_attribute_name} attribute'
            ) from e

    def has_permission(self, request, view):
        """
        Override of BasePermission.has_permission that checks if the roles
        provided in the token (a JWT) are sufficient to allow access to the
        APIView.
        """
        if not request.auth or not request.auth.payload:
            return False

        roles = self.get_roles_from_token(request.auth.payload)

        if not roles:
            return False

        required_roles = self.get_roles(view)
        has_roles = self.has_required_roles(roles, required_roles)
        return has_roles


class RequiredRolesMixin:
    """
    Subclass this mixin to authorize a client only if they have
    ALL the required roles.
    """

    def has_required_roles(self, provided_roles, required_roles):
        provided = set(provided_roles)
        required = set(required_roles)

        return required.issubset(provided)


class AnyRoleMixin:
    """
    Subclass this mixin to authorize a client who has ANY of the
    required roles.
    """

    def has_required_roles(self, provided_roles, required_roles):
        provided = set(provided_roles)
        required = set(required_roles)

        return provided & required


class ResourceHasRoles(RequiredRolesMixin, TokenHasRole):
    """
    Permission that requires all resource roles specified in the
    APIView be found in the JWT.

    The resource roles are expected to be found in the JWT in the keypath
    resource_access.{aud}.roles (where aud is the token audience,
    as specified in the simple_jwt settings).

    APIViews that use this Permission will need to add an attribute
    named `resource_roles` which contains a list of roles.
    """

    @property
    def role_attribute_name(self):
        return 'resource_roles'

    def get_roles_from_token(self, token_payload):
        slug = settings.DRY['PROJECT_SLUG']
        return deep_get(token_payload, f'resource_access.{slug}.roles')


class RealmHasRoles(RequiredRolesMixin, TokenHasRole):
    """
    Permission that requires all realm roles specified in the
    APIView be found in the JWT.

    The realm roles are expected to be found in the JWT by the keypath
    of 'realm_access.roles'.

    APIViews that use this Permission will need to add an attribute
    named `realm_roles` which contains a list of the required roles.
    """

    @property
    def role_attribute_name(self):
        return 'realm_roles'

    def get_roles_from_token(self, token_payload):
        return deep_get(token_payload, 'realm_access.roles')


class ResourceHasAny(AnyRoleMixin, ResourceHasRoles):
    """
    Subclass of ResourceHasRoles, but only requires at least one resouce
    role specified in the APIView be present in the JWT, rather than all
    of them.
    """


class RealmHasAny(AnyRoleMixin, RealmHasRoles):
    """
    Subclass of ResourceHasRoles, but only requires at least one realm role
    specified in the APIView be present in the JWT, rather than all of them.
    """
