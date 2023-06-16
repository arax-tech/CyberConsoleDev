from django.contrib import admin
from django.urls import path, include
from company.views import  LogView

admin.site.site_header = 'BroadBand9'
admin.site.site_title = 'Admin'
admin.site.index_title = 'CyberConsole'

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path("api/company/", include("company.urls")),
    path("api/client/", include("client.urls")),
    path("api/team/", include("team.urls")),

    path("api/logs/", LogView.as_view(), name="logs"),
    path("api/log/store/", LogView.as_view(), name="log_store"),
    path("api/log/delete/<id>/", LogView.as_view(), name="log_delete"),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
