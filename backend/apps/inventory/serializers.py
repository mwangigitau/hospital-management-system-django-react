from rest_framework import serializers
from .models import Category, Item, Store, StoreItem, StockTransfer, StockTransferItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'category_name', 'unit', 'reorder_level',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'store_type', 'location', 'branch', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StoreItemSerializer(serializers.ModelSerializer):
    item_name = serializers.StringRelatedField(source='item', read_only=True)
    store_name = serializers.StringRelatedField(source='store', read_only=True)

    class Meta:
        model = StoreItem
        fields = ['id', 'store', 'store_name', 'item', 'item_name', 'quantity', 'unit_cost',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockTransferItemSerializer(serializers.ModelSerializer):
    item_name = serializers.StringRelatedField(source='item', read_only=True)

    class Meta:
        model = StockTransferItem
        fields = ['id', 'item', 'item_name', 'quantity']


class StockTransferSerializer(serializers.ModelSerializer):
    transfer_items = StockTransferItemSerializer(many=True, read_only=True)
    from_store_name = serializers.StringRelatedField(source='from_store', read_only=True)
    to_store_name = serializers.StringRelatedField(source='to_store', read_only=True)

    class Meta:
        model = StockTransfer
        fields = ['id', 'from_store', 'from_store_name', 'to_store', 'to_store_name',
                  'transfer_items', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
