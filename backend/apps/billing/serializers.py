from rest_framework import serializers
from .models import ServiceCharge, Invoice, InvoiceItem, Payment, Receipt


class ServiceChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCharge
        fields = ['id', 'name', 'category', 'price', 'department', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvoiceItemSerializer(serializers.ModelSerializer):
    service_name = serializers.StringRelatedField(source='service', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'service', 'service_name', 'description',
                  'quantity', 'unit_price', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'payment', 'receipt_number', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'receipt_number', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    received_by_name = serializers.StringRelatedField(source='received_by', read_only=True)
    receipt = ReceiptSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'payment_date', 'amount', 'payment_method',
                  'reference', 'received_by', 'received_by_name', 'receipt', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvoiceSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'patient', 'patient_name', 'admission', 'invoice_date', 'due_date',
            'status', 'subtotal', 'discount', 'tax', 'total', 'notes',
            'items', 'payments', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvoiceListSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'patient', 'patient_name', 'invoice_date', 'due_date',
                  'status', 'total']
