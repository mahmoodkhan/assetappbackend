import re
from operator import and_, or_
from django.db.models import Q

from rest_framework import viewsets
from rest_framework_json_api.views import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_json_api.parsers import JSONParser
from rest_framework_json_api.renderers import JSONRenderer

from .models import *
from .serializers import *


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class OfficeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """"
        It parses querset that is formatted as:
        /api/offices?filter[country][]=1&filter[country][]=2&filter[name][]=KBL&filter[name][]=KND&filter[long_name]=Kabul

        To test is in Ember using Chrome Console:
        console out an instance of the Ember.js store object in your Ember app
        in the cosnsole window, right click on the store class and set it as Global
        store = temp1
        offices = store.query('office', {filter: {country: ["1", "2",], name: ['KBL', 'KND',],long_name: 'Kabul' }});
        offices.forEach(function(o){console.log(o.get('name'));});
        """
        offices = Office.objects.all()
        kwargs = {}
        args = []
        if hasattr(self.request, 'query_params'):
            params = dict(self.request.query_params)
            for key, val in params.iteritems():
                # retrieves the field name from the filter query string.
                field = re.search(r"\[([A-Za-z0-9_]+)\]", key).group(1)

                # if the val is a list with > 1 values in it, then use Q objects
                if len(val) > 1:
                    args.append(reduce(or_, [Q(**{field:v}) for v in val] ) )
                else:
                    kwargs[field] = str(val[0])

            offices = offices.filter(*args, **kwargs)
        return offices

    serializer_class = OfficeSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Assets to be CRUDed
    """
    def get_queryset(self):
        user = self.request.user
        return Asset.objects.filter(country=user.userprofile.country)

    serializer_class = AssetSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class AssetTypeViewSet(viewsets.ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #authentication_classes = (JSONWebTokenAuthentication, )
    #authentication_classes = (TokenAuthentication,)
    permission_classes = []#(IsAuthenticated,)
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
