from django.db import models
from tinymce.models import HTMLField

from apps.siteconfig.models import NavItem


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = HTMLField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        related_name="subcategories",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="category_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        
        if not NavItem.objects.filter(title=self.name).exists():
            navitem = NavItem.objects.create(
                title=self.name, link=f"/products/?category={self.slug}"
            )

            if self.parent:
                navitem.parent = NavItem.objects.get(title=self.parent.name)
                navitem.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        NavItem.objects.filter(title=self.name).delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = HTMLField(blank=True, null=True)
    logo = models.ImageField(upload_to="brand_logos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = HTMLField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        Brand, related_name="products", on_delete=models.CASCADE, null=True, blank=True
    )
    ingredients = HTMLField(blank=True, null=True)
    how_to_use = HTMLField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        ratings = self.reviews.values_list("rating", flat=True)
        if ratings:
            return sum(ratings) / len(ratings)
        return 0

    @classmethod
    def get_new_arrivals(cls, limit=4):
        return cls.objects.order_by("-created_at")[:limit]

    @classmethod
    def get_best_sellers(cls, limit=4):
        # TODO: Implement logic to determine best sellers, e.g., based on sales data
        return cls.objects.order_by("-stock")[:limit]

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    image = models.ImageField(upload_to="product_variants/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.product.name}"

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        unique_together = ("product", "name")
        ordering = ["name"]


class ProductShade(models.Model):
    product = models.ForeignKey(
        Product, related_name="shades", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    hex_code = models.CharField(
        max_length=7, help_text="Hex color code (e.g., #FFFFFF)"
    )
    image = models.ImageField(upload_to="product_shades/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.product.name}"

    class Meta:
        verbose_name = "Product Shade"
        verbose_name_plural = "Product Shades"
        unique_together = ("product", "name")
        ordering = ["name"]


class ProductProperty(models.Model):
    product = models.ForeignKey(
        Product, related_name="properties", on_delete=models.CASCADE
    )
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = "Product Property"
        verbose_name_plural = "Product Properties"
        unique_together = ("product", "key")
        ordering = ["key"]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="product_images/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["-is_main", "id"]
        # unique_together = ("product", "is_main")


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        ordering = ["-created_at"]
