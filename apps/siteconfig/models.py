from django.db import models
from solo.models import SingletonModel


class SiteConfig(SingletonModel):
    site_name = models.CharField(max_length=255, verbose_name="Site Name")
    site_description = models.TextField(verbose_name="Site Description", blank=True, null=True)
    site_logo = models.ImageField(upload_to='siteconfig/', verbose_name="Site Logo", blank=True, null=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name


class Banner(models.Model):
    title = models.CharField(max_length=255, verbose_name="Banner Title")
    image = models.ImageField(upload_to='banners/', verbose_name="Banner Image")
    link = models.CharField(verbose_name="Banner Link", blank=True, null=True, max_length=255)
    active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        ordering = ['-id']
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title
