from django.views.generic import TemplateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework_jwt.settings import api_settings
from datetime import datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Assets API')
    return response.Response(generator.get_schema(request=request))


class HomeView(TemplateView):
    template_name = 'index.html'

    def render_to_response(self, context, **response_kwargs):
        response = super(HomeView, self).render_to_response(context, **response_kwargs)
        if self.request.user.is_authenticated():
            if self.request.COOKIES.get("jwt", None) is None:
                response.set_cookie(key="jwt", value=convert_sessionid_to_jwt(self.request.user), domain="localhost")
        return response


def jwt_payload_handler(user):
    try:
        username = user.get_username()
    except AttributeError:
        username = user.username

    return {
        'user_id': user.pk,
        'email': user.email,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

def convert_sessionid_to_jwt(user):
    """convert a session_id to a jwt.

    """
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


