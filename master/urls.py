from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^resources/', include('resources.urls', namespace='resources')),
    url(r'^analysis/', include('analysis.urls', namespace='analysis')),
]
