from rest_framework import viewsets
from rest_framework_json_api.views import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_json_api.parsers import JSONParser
from rest_framework_json_api.renderers import JSONRenderer

from .models import *
from .serializers import *
from .util import get_filters


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)


class OfficeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        offices = Office.objects.all()
        if hasattr(self.request, 'query_params'):
            args, kwargs = get_filters(dict(self.request.query_params))
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
