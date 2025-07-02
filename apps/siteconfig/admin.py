from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import SiteConfig, Banner


@admin.register(SiteConfig)
class SiteConfigAdmin(SingletonModelAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass
