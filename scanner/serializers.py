from rest_framework import serializers
from .models import ScanResult, CommunityReport

class ScanResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanResult
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CommunityReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityReport
        fields = '__all__'
        read_only_fields = ['created_at']