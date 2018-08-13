from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('', include('evacuation.urls')),
    path('survey/', include('survey.urls')),
    path('admin/', admin.site.urls),
    re_path('^webpush/', include('webpush.urls'))
]
