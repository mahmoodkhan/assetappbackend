from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        print("executing the view code")
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user'] = "Me me!"
        return context