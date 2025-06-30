from django.db import models
from tinymce.models import HTMLField


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    cover_image = models.ImageField(upload_to="blog_covers/", null=True, blank=True)
    content = HTMLField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["-created_at"]  # Newest first


class BlogSection(models.Model):
    blog = models.ForeignKey(Blog, related_name="sections", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = HTMLField()
    image = models.ImageField(upload_to="blog_sections/", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} - {self.blog.title}"
