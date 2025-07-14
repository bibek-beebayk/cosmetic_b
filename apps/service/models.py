from django.contrib.auth import get_user_model
from django.db import models
from tinymce.models import HTMLField

User = get_user_model()


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = HTMLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    image = models.ImageField(upload_to="services/")

    def __str__(self):
        return self.name


class Staff(models.Model):

    ROLES = [("beautician", "Beautician"), ("dermatologist", "Dermatologist")]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLES, default="beautician")
    bio = HTMLField(blank=True, null=True)
    image = models.ImageField(upload_to="staff/")
    services = models.ManyToManyField(Service, related_name="staff")

    def __str__(self):
        return self.name


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="appointments",
        null=True,
        blank=True,
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="appointments"
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        related_name="appointments",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} - {self.service.name} - {self.date} - {self.time}"
