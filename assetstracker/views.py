from django.views.generic import TemplateView

from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Assets API')
    return response.Response(generator.get_schema(request=request))


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        print("executing the view code")
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user'] = "Me me!"
        return context