from types import SimpleNamespace

from django.contrib.auth import get_user_model, models as auth_models
from django.test import TestCase

from byuhbll_django_dry.permissions import (
    HasAPIGroupPermission,
    RealmHasAny,
    RealmHasRoles,
    ResourceHasAny,
    ResourceHasRoles,
)


class HasAPIGroupPermissionTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create(username='testuser')
        self.api_group, _ = auth_models.Group.objects.get_or_create(name='API')

    def tearDown(self):
        self.User.objects.all().delete()

    def test_default_has_permission_success(self):
        self.user.groups.add(self.api_group)
        request = SimpleNamespace(method='GET', user=self.user)
        view = SimpleNamespace()
        self.assertTrue(HasAPIGroupPermission().has_permission(request, view))

    def test_default_has_permission_failure(self):
        request = SimpleNamespace(method='GET', user=self.user)
        view = SimpleNamespace()
        self.assertFalse(HasAPIGroupPermission().has_permission(request, view))


class TokenPermissionTests(TestCase):
    def setUp(self):
        self.auth = SimpleNamespace(
            payload={
                'resource_access': {'byuhbll_django_dry': {'roles': ['API', 'ADMIN']}},
                'realm_access': {'roles': ['basic-access', 'student']},
            }
        )
        self.request = SimpleNamespace(method='GET', auth=self.auth)

    def test_resource_has_roles_success(self):
        view = SimpleNamespace(resource_roles=['API', 'ADMIN'])
        self.assertTrue(ResourceHasRoles().has_permission(self.request, view))

    def test_resource_has_roles_failure(self):
        view = SimpleNamespace(resource_roles=['ADMIN', 'SUPERUSER'])
        self.assertFalse(ResourceHasRoles().has_permission(self.request, view))

    def test_resource_has_any_success(self):
        view = SimpleNamespace(resource_roles=['ADMIN', 'SUPERUSER'])
        self.assertTrue(ResourceHasAny().has_permission(self.request, view))

    def test_resource_has_any_failure(self):
        view = SimpleNamespace(resource_roles=['SUPERUSER'])
        self.assertFalse(ResourceHasAny().has_permission(self.request, view))

    def test_realm_has_roles_success(self):
        view = SimpleNamespace(realm_roles=['basic-access', 'student'])
        self.assertTrue(RealmHasRoles().has_permission(self.request, view))

    def test_realm_has_roles_failure(self):
        view = SimpleNamespace(realm_roles=['student', 'admin'])
        self.assertFalse(RealmHasRoles().has_permission(self.request, view))

    def test_realm_has_any_success(self):
        view = SimpleNamespace(realm_roles=['student', 'admin'])
        self.assertTrue(RealmHasAny().has_permission(self.request, view))

    def test_realm_has_any_failure(self):
        view = SimpleNamespace(realm_roles=['admin'])
        self.assertFalse(RealmHasAny().has_permission(self.request, view))

    def test_no_payload_failure(self):
        auth = SimpleNamespace(payload={})
        self.request = SimpleNamespace(method='GET', auth=auth)
        self.assertFalse(ResourceHasRoles().has_permission(self.request, None))

    def test_no_resource_access_roles_failure(self):
        self.request.auth.payload.pop('resource_access')
        self.assertFalse(ResourceHasRoles().has_permission(self.request, self.auth))

    def test_no_realm_access_roles_failure(self):
        self.request.auth.payload.pop('realm_access')
        self.assertFalse(RealmHasRoles().has_permission(self.request, self.auth))
