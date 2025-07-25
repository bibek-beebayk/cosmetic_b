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
    

class NavItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Nav Item Title")
    link = models.CharField(verbose_name="Nav Item Link", blank=True, null=True, max_length=255)
    active = models.BooleanField(default=True, verbose_name="Is Active")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['order']

    class Meta:
        ordering = ['-id']
        verbose_name = "Nav Item"
        verbose_name_plural = "Nav Items"

    def __str__(self):
        return self.title
    
    def get_children(self):
        return NavItem.objects.filter(parent=self).order_by('order')
