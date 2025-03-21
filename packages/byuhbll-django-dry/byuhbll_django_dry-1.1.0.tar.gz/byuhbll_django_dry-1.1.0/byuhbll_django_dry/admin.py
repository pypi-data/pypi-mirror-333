"""Custom admin actions and mixins."""

import csv
import functools

from django.http import HttpResponse


def admin_action(func):
    """Decorator for identifying admin action methods."""

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)

    wrapped.short_description = wrapped.__doc__
    return wrapped


class ExportActionMixin:
    export_data_filename = 'data.csv'

    @admin_action
    def export_data(self, request, queryset):
        """Export selected data"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            f'attachment; filename="{self.export_data_filename}"'
        )

        fields = getattr(self, 'export_fields', self.list_display)

        writer = csv.writer(response)
        # write header row
        writer.writerow([i for i in fields])
        # write data rows
        for item in queryset:
            values = [getattr(item, name, None) for name in fields]
            writer.writerow([v() if callable(v) else v for v in values])

        return response
