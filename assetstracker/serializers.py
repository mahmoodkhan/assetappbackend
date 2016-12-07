from rest_framework import serializers
from .models import *

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        exclude = ("created_by", "updated_by", "created", "updated")


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        exclude = ("created_by", "updated_by", "created", "updated")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("created_by", "updated_by", "created", "updated")


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        exclude = ("created_by", "updated_by", "created", "updated")


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        exclude = ("created_by", "updated_by", "created", "updated")


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        exclude = ("created_by", "updated_by", "created", "updated")