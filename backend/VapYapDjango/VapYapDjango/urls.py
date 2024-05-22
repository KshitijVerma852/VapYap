import os

from django.contrib import admin
from django.shortcuts import render
from django.urls import path, re_path
from .parsing import returnJSONObject
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

class FrontendAppView(TemplateView):
    template_name = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'index.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: Figure out how to configure the react proxy
        return context

urlpatterns = [
    path("dev/", returnJSONObject),
    path('admin/', admin.site.urls),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [re_path(r'^.*', FrontendAppView.as_view())]
