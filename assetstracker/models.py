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
from django.utils.functional import curry

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


@python_2_unicode_compatible
class Country(Country):
    class Meta:
        proxy = True

    def __str__(self):
        return '%s' % self.name

    class JSONAPIMeta:
        resource_name = 'countries'


@python_2_unicode_compatible
class Office(Office):
    class Meta:
        proxy = True

    def __str__(self):
        return '%s' % self.name

    class JSONAPIMeta:
        resource_name = 'offices'


@python_2_unicode_compatible
class Custodian(UserProfile):
    class Meta:
        proxy = True

    def __str__(self):
        return '%s' % self.name

    class JSONAPIMeta:
        resource_name = 'custodians'

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
    assettype = models.ForeignKey(AssetType, related_name='items')
    category = models.ForeignKey(Category, related_name='items')
    subcategory = models.ForeignKey(Subcategory, related_name='items')
    status = models.ForeignKey(Status, related_name='items')
    donor = models.ForeignKey(Donor, related_name='items')
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    sno1 = models.CharField(max_length=50, null=True, blank=True)
    sno2 = models.CharField(max_length=50, null=True, blank=True)
    accessories = models.CharField(max_length=254, null=True, blank=True)
    prnumber = models.CharField(max_length=12, blank=True, null=True)
    ponumber = models.CharField(max_length=12, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s-%s %s' % (self.country.iso_two_letters_code, self.no, self.description)

    def save(self, *args, **kwargs):
        if not self.id:
            num_assets = Asset.objects.filter(country=self.country.pk).aggregate(Max('no'))['no__max']
            num_assets = 1 if num_assets == None else num_assets + 1
            self.no = num_assets
        super(Asset, self).save(*args, **kwargs)

    class JSONAPIMeta:
        resource_name = 'assets'

    def __init__(self, *args, **kwargs):
        # Call the superclass first; it'll create all of the field objects.
        super(Asset, self).__init__(*args, **kwargs)

        # Again, iterate over all of our field objects.
        for field in self._meta.fields:
            # Create a string, get_FIELDNAME_help text
            method_name = "get_{0}_help_text".format(field.name)

            # We can use curry to create the method with a pre-defined argument
            curried_method = curry(self._get_help_text, field_name=field.name)

            # And we add this method to the instance of the class.
            setattr(self, method_name, curried_method)

            # You can then use it in template like this:
            # <span>{{ asset.get_assettype_help_text }}</span>


    def _get_help_text(self, field_name):
        """Given a field name, return it's help text."""
        for field in self._meta.fields:
            if field.name == field_name:
                return field.help_text


@python_2_unicode_compatible
class AssetIssuanceHistory(CommonBaseAbstractModel):
    asset = models.ForeignKey(Asset, related_name='asset_history')
    custodian = models.ForeignKey(Custodian, related_name='custodian_history')
    notes = models.TextField(null=True, blank=True)
    issuedby = models.ForeignKey(Custodian, null=True, blank=True, related_name='issuedby_history')
    issuedate = models.DateTimeField(editable=False, blank=True, null=True)
    returndate = models.DateTimeField(editable=False, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.asset.description, self.custodian.name)

    class JSONAPIMeta:
        resource_name = 'assetissuancehistories'



