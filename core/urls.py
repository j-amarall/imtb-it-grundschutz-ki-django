from django.contrib import admin
from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts
    path("accounts/", include("accounts.urls")),

    # Core pages
    path("", core_views.home, name="home"),
    path("chat/", core_views.chat, name="chat"),
    path("chat/clear/", core_views.clear_chat, name="chat_clear"),
    path("impressum/", core_views.impressum, name="impressum"),
    path("datenschutz/", core_views.datenschutz, name="datenschutz"),
]
