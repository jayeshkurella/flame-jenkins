# serializers.py
from rest_framework import serializers
from searchbar.models import data

class SourceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = data
        fields = '__all__'
