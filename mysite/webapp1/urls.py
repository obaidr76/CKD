from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login/$', views.login,name='login'),
    url(r'signup/$',views.signup,name='signup'),
    url(r'input/$',views.input,name='input'),
    url(r'dashboard/$',views.dashboard,name='dashboard1'),
    url(r'dashboard/(?P<id>[0-6])/$',views.dashboard,name='dashboard'),
    url(r'logout/',views.logout,name='logout'),
    url(r'profile/',views.profile,name='profile'),
    url(r'download/',views.download,name='download'),
    url(r'review/',views.review,name='review')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)