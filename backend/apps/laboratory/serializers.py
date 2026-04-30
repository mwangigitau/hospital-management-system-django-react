from rest_framework import serializers
from .models import TestCatalog, LabRequest, LabRequestItem, Sample, TestResult


class TestCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCatalog
        fields = ['id', 'name', 'code', 'category', 'normal_range', 'unit', 'price',
                  'turnaround_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TestResultSerializer(serializers.ModelSerializer):
    entered_by_name = serializers.StringRelatedField(source='entered_by', read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'lab_request_item', 'value', 'unit', 'normal_range',
                  'is_critical', 'notes', 'entered_by', 'entered_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SampleSerializer(serializers.ModelSerializer):
    collected_by_name = serializers.StringRelatedField(source='collected_by', read_only=True)

    class Meta:
        model = Sample
        fields = ['id', 'lab_request_item', 'sample_type', 'collected_at',
                  'collected_by', 'collected_by_name', 'barcode', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LabRequestItemSerializer(serializers.ModelSerializer):
    test_name = serializers.StringRelatedField(source='test', read_only=True)
    result = TestResultSerializer(read_only=True)

    class Meta:
        model = LabRequestItem
        fields = ['id', 'lab_request', 'test', 'test_name', 'status', 'result', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LabRequestSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    requested_by_name = serializers.StringRelatedField(source='requested_by', read_only=True)
    items = LabRequestItemSerializer(many=True, read_only=True)

    class Meta:
        model = LabRequest
        fields = ['id', 'patient', 'patient_name', 'requested_by', 'requested_by_name',
                  'status', 'priority', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
