from django.contrib import admin
from django.urls import path

class LogAdminSite(admin.AdminSite):
    def get_urls(self):
        custom_urls = []
        admin_urls = super().get_urls()
        return custom_urls + admin_urls


admin_site = LogAdminSite()
