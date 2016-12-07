from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Asset)
admin.site.register(AssetType)
admin.site.register(Donor)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(Subcategory)