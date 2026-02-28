from rest_framework import serializers
from .models import Drug, DrugBatch, StockMovement, PrescriptionItem


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'name', 'barcode', 'generic_name', 'category', 'unit', 'reorder_level',
                  'description', 'is_controlled', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DrugBatchSerializer(serializers.ModelSerializer):
    drug_name = serializers.StringRelatedField(source='drug', read_only=True)

    class Meta:
        model = DrugBatch
        fields = ['id', 'drug', 'drug_name', 'batch_number', 'expiry_date',
                  'quantity', 'purchase_price', 'selling_price', 'supplier', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockMovementSerializer(serializers.ModelSerializer):
    drug_name = serializers.StringRelatedField(source='drug', read_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'drug', 'drug_name', 'batch', 'movement_type', 'quantity',
                  'reference', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PrescriptionItemSerializer(serializers.ModelSerializer):
    drug_name = serializers.StringRelatedField(source='drug', read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'prescription', 'drug', 'drug_name', 'dose', 'frequency',
                  'duration', 'quantity', 'dispensed_quantity', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
