from rest_framework import serializers
from .models import Downloads

class DownloadDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downloads
        fields = '__all__'
