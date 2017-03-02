from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import exceptions
import rest_framework.parsers
import rest_framework.renderers
from rest_framework_json_api.utils import format_drf_errors
import rest_framework_json_api.metadata
import rest_framework_json_api.parsers
import rest_framework_json_api.renderers

from .models import *
from .serializers import *
from .util import get_filters


HTTP_422_UNPROCESSABLE_ENTITY = 422

class JsonApiViewSet(viewsets.ModelViewSet):
    """
    Configuring DRF-jsonapi from within a class so that it can be used alongside
    vanilla DRF API views.
    """
    parser_classes = [
        rest_framework_json_api.parsers.JSONParser,
        rest_framework.parsers.FormParser,
        rest_framework.parsers.MultiPartParser,
    ]
    renderer_classes = [
        rest_framework_json_api.renderers.JSONRenderer,
        rest_framework.renderers.BrowsableAPIRenderer,
    ]
    metadata_class = rest_framework_json_api.metadata.JSONAPIMetadata

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.ValidationError):
            # some require that validation errors return 422 status
            # for example ember-data (isInvalid method on adapter)
            exc.status_code = HTTP_422_UNPROCESSABLE_ENTITY
        # exception handler can't be set on class so you have to
        # override the error response in this method
        response = super(JsonApiViewSet, self).handle_exception(exc)
        context = self.get_exception_handler_context()
        return format_drf_errors(response, context, exc)


class CountryViewSet(JsonApiViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class OfficeViewSet(JsonApiViewSet):
    def get_queryset(self):
        offices = Office.objects.all()
        if hasattr(self.request, 'query_params'):
            args, kwargs = get_filters(dict(self.request.query_params))
            offices = offices.filter(*args, **kwargs)
        return offices

    serializer_class = OfficeSerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class UserViewSet(JsonApiViewSet):
    def get_queryset(self):
        users = User.objects.all()
        if hasattr(self.request, 'query_params'):
            args, kwargs = get_filters(dict(self.request.query_params))
            users = users.filter(*args, **kwargs)
        return users
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class AssetViewSet(JsonApiViewSet):
    """
    API endpoint that allows Assets to be CRUDed
    """
    def get_queryset(self):
        user = self.request.user
        return Asset.objects.filter(country=user.userprofile.country)

    serializer_class = AssetSerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class AssetTypeViewSet(JsonApiViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class CategoryViewSet(JsonApiViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #authentication_classes = (JSONWebTokenAuthentication, )
    #authentication_classes = (TokenAuthentication,)
    permission_classes = []#(IsAuthenticated,)


class SubcategoryViewSet(JsonApiViewSet):
    def get_queryset(self):
        subcategories = Subcategory.objects.all()
        if hasattr(self.request, 'query_params'):
            args, kwargs = get_filters(dict(self.request.query_params))
            subcategories = subcategories.filter(*args, **kwargs)
        return subcategories

    serializer_class = SubcategorySerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class DonorViewSet(JsonApiViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class StatusViewSet(JsonApiViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
