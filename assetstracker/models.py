from __future__ import unicode_literals

from django.db import models

import datetime, time, logging
from decimal import Decimal

from django.core.urlresolvers import reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from django.db.models import Q, Sum, Max, Min, Count

from django.utils import timezone
from django.utils.timezone import utc
from django.utils.encoding import python_2_unicode_compatible

from djangocosign.models import UserProfile, Region, Country, Office

class CommonBaseAbstractModel(models.Model):
    created_by = models.ForeignKey(UserProfile, blank=True, null=True, related_name="%(app_label)s_%(class)s_created")
    updated_by = models.ForeignKey(UserProfile, blank=True, null=True, related_name="%(app_label)s_%(class)s_updated")
    created = models.DateTimeField(editable=False, blank=True, null=True)
    updated = models.DateTimeField(editable=False, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now_utc = datetime.datetime.utcnow().replace(tzinfo=utc)
        if self.id:
            self.updated = now_utc
        else:
            self.created = now_utc
        super(CommonBaseAbstractModel, self).save(*args, **kwargs)


class Country(Country):
    class Meta:
        proxy = True

    class JSONAPIMeta:
        resource_name = 'countries'

class Office(Office):
    class Meta:
        proxy = True

    class JSONAPIMeta:
        resource_name = 'offices'

@python_2_unicode_compatible
class AssetType(CommonBaseAbstractModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '%s' % self.name

    class JSONAPIMeta:
        resource_name = 'assettypes'


@python_2_unicode_compatible
class Category(CommonBaseAbstractModel):
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '%s' % self.category

    class JSONAPIMeta:
        resource_name = 'categories'


@python_2_unicode_compatible
class Subcategory(CommonBaseAbstractModel):
    category = models.ForeignKey(Category, related_name='subcategories')
    subcategory = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '%s' % self.subcategory

    class JSONAPIMeta:
        resource_name = 'subcategories'


@python_2_unicode_compatible
class Donor(CommonBaseAbstractModel):
    donor = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % self.donor

    class JSONAPIMeta:
        resource_name = 'donors'


@python_2_unicode_compatible
class Status(CommonBaseAbstractModel):
    status = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '%s' % self.status

    class JSONAPIMeta:
        resource_name = 'statuses'


@python_2_unicode_compatible
class Asset(CommonBaseAbstractModel):
    country = models.ForeignKey(Country, related_name='items', null=False, blank=False, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, related_name='items', null=True, blank=True, on_delete=models.DO_NOTHING)
    no = models.PositiveIntegerField(verbose_name='No', default=1, null=True, blank=True)
    assettype = models.ForeignKey(AssetType)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(Subcategory)
    status = models.ForeignKey(Status)
    donor = models.ForeignKey(Donor)
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    sno1 = models.CharField(max_length=50, blank=True)
    sno2 = models.CharField(max_length=50, blank=True)
    accessories = models.CharField(max_length=254, null=True, blank=True)
    prnumber = models.CharField(max_length=12, blank=True, null=True)
    ponumber = models.CharField(max_length=12, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s-%s-%s' % (self.country.name, self.office.name, self.no)

    def save(self, *args, **kwargs):
        if not self.id:
            num_assets = Asset.objects.filter(office=self.office.pk).aggregate(Max('no'))['no__max']
            num_assets = 1 if num_assets == None else num_assets + 1
            self.no = num_assets
        super(Asset, self).save(*args, **kwargs)

    class JSONAPIMeta:
        resource_name = 'assets'


