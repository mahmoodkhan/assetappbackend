from django.contrib.auth.models import User
#from rest_framework import serializers
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from .models import *


class CountrySerializer(serializers.ModelSerializer):
    iso2 = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ('id', 'name', 'iso2')

    def get_iso2(self, obj):
        return obj.iso_two_letters_code

class OfficeSerializer(serializers.ModelSerializer):

    longname = serializers.SerializerMethodField()

    class Meta:
        model = Office
        fields = ('id', 'country', 'longname', 'name')

    def get_longname(self, obj):
        return obj.long_name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

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