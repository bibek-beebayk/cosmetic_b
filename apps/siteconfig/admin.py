from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import Banner, NavItem, SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(SingletonModelAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


@admin.register(NavItem)
class NavItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["title", "link", "active", "parent", "order"]
    list_editable = ["active", "order"]
