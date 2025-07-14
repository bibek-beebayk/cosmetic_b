from django.contrib import admin
from .models import Service, Staff, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    search_fields = ("name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "date", "time", "service", "staff")
    search_fields = ("name", "email", "phone")
    list_filter = ("date", "service", "staff")
