from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login,name='login'),
    url(r'^doc_login/$', views.doc_login,name='doc_login'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^doc_signup/$',views.doc_signup,name='doc_signup'),
    url(r'^input/$',views.input,name='input'),
    url(r'^dashboard/$',views.dashboard,name='dashboard1'),
    url(r'^dashboard/(?P<id>[0-8])/$',views.dashboard,name='dashboard'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^download/$',views.download,name='download'),
    url(r'^review/$',views.review,name='review'),
    url(r'^address/$',views.address,name='address'),
    url(r'^medical1/$',views.medical1,name='medical1'),
    url(r'^home/$',views.home,name='home'),
    url(r'^home/(?P<id>[a-zA-Z]+)/$',views.home,name='home'),    
    url(r'^console/$',views.console,name='console'),
    url(r'^console/(?P<id>[a-z_A-Z]+)/$',views.console,name='console'),
    url(r'^doc_profile/$',views.doc_profile,name='doc_profile'),
    url(r'^doc_address/$',views.doc_address,name='doc_address'),
    url(r'^report_sent/$',views.report_sent,name='report_sent'),
    url(r'^consultation/$',views.consultation,name='consultation'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)