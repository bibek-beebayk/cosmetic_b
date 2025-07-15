from rest_framework import serializers

from .models import Service, Staff


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        exclude = ["services"]


class ServiceSerializer(serializers.ModelSerializer):
    staffs = StaffSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = "__all__"
