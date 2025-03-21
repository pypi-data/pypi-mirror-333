from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = []
admin_url = settings.DRY['ADMIN_URL_PATH']


if settings.OIDC['ENABLED']:
    import mozilla_django_oidc as oidc

    urlpatterns += [
        path('oidc/', include('mozilla_django_oidc.urls')),
        path(
            'login/',
            oidc.urls.OIDCAuthenticateClass.as_view(),
            name='login',
        ),
        path('logout/', oidc.views.OIDCLogoutView.as_view(), name='logout'),
    ]

if settings.DEBUG:
    import debug_toolbar
    from django.views import defaults as view_defaults

    kwargs = {'exception': Exception()}
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # This allows the error pages to be debugged during development, just
        # visit these url in browser to see what these error pages look like.
        path('400/', view_defaults.bad_request, kwargs),
        path('403/', view_defaults.permission_denied, kwargs),
        path('404/', view_defaults.page_not_found, kwargs),
        path('500/', view_defaults.server_error),
    ]

urlpatterns += [
    # Django Hijack
    path('hijack/', include('hijack.urls'))
]

admin_urlpatterns = [
    # Django Admin
    path(admin_url, admin.site.urls)
]

urlpatterns = (
    urlpatterns
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + admin_urlpatterns
)
