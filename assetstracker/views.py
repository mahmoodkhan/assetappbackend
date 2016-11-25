from django.shortcuts import render
from rest_framework import viewsets
from .models import Asset
from .serializers import AssetSerializer

# Create your views here.
def index(request):
    return render(request, 'index.html')


class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Assets to be CRUDed
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer