from rest_framework import serializers
from .models import Banner, NavItem


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'image', 'link']


class NavItemSerializer(serializers.ModelSerializer):

    submenu = serializers.SerializerMethodField()

    def get_submenu(self, obj):
        submenu = NavItemSerializer(obj.get_children(), many=True).data
        return submenu
    
    class Meta:
        model = NavItem
        fields = ['title', 'link', 'submenu']

