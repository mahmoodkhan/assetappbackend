"""assetsmgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from assetstracker import views, api

router = routers.DefaultRouter(trailing_slash=False)
router.register("users", api.UserViewSet, base_name="users")
router.register("groups", api.GroupViewSet, base_name="groups")
router.register("assets", api.AssetViewSet, base_name='assets')
router.register("assettypes", api.AssetTypeViewSet)
router.register("categories", api.CategoryViewSet)
router.register("donors", api.DonorViewSet)
router.register("countries", api.CountryViewSet, base_name='countries')
router.register("offices", api.OfficeViewSet, base_name='offices')
router.register("custodians", api.CustodianViewSet, base_name='custodians')
router.register("assetissuancehistories", api.AssetIssuanceHistoryViewSet, base_name='assetissuancehistories')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth-basic/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api/', include(router.urls)),
    url(r'^api/docs/', views.schema_view),

    url(r'^$', views.HomeView.as_view(), name='index'),

    url(r'^.*$', views.HomeView.as_view(), name='ember'),
]
