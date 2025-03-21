from django.test import TestCase

from byuhbll_django_dry.models import UserMixin


class UserMixinTests(TestCase):
    def test_basic_usage(self):
        class Group:
            def __init__(self, name):
                self.name = name

        class Groups:
            def __init__(self, *groups):
                self.groups = groups

            def all(self):
                return self.groups

        class MockUser(UserMixin):
            def __init__(self, username, groups):
                self.username = username
                self.groups = groups

        username = 'testusername'
        admin_group_name = 'Admin'
        ta_group_name = 'TA'
        librarian_group_name = 'SubjectLibrarian'

        u = MockUser(username, Groups(Group(admin_group_name), Group(ta_group_name)))

        self.assertEqual(u.net_id, username)
        self.assertTrue(u.in_group(admin_group_name))
        self.assertTrue(u.in_group(ta_group_name))
        self.assertFalse(u.in_group(librarian_group_name))
