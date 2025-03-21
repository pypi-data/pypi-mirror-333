"""Model mixins for common fields and methods."""


class UserMixin:
    @property
    def net_id(self):
        return self.username

    def in_group(self, group_name):
        return any(g.name == group_name for g in self.groups.all())
