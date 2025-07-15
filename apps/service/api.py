from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin
from .models import Service, Staff
from .serializers import ServiceSerializer, StaffSerializer


class ServiceViewSet(ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = None