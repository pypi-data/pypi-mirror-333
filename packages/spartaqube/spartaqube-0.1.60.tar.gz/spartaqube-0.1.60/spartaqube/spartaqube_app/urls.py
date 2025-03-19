from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_8cba795938.sparta_64d974bce2.qube_68f0baf933.sparta_dcaf881f0a'
handler500='project.sparta_8cba795938.sparta_64d974bce2.qube_68f0baf933.sparta_b8e06c4697'
handler403='project.sparta_8cba795938.sparta_64d974bce2.qube_68f0baf933.sparta_0d1225b919'
handler400='project.sparta_8cba795938.sparta_64d974bce2.qube_68f0baf933.sparta_340a23d592'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]