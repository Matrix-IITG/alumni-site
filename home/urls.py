from django.conf.urls import url
from . import views
app_name = 'home'
urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^home/$',views.home,name='home'),
    url(r'^events/$', views.events, name='events'),
    url(r'^about/$', views.about_us, name='about_us'),
    url(r'^team/$', views.team, name='team'),

    #url(r'^accounts/login/$',views.register,name='register'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/edit_profile_manual/$', views.profile_edit_manual, name='profile_edit_manual'),
    url(r'^accounts/edit_profile_linkdin/$', views.profile_edit_linkdin, name='profile_edit_linkdin'),
    url(r'^accounts/update/$',views.update_user,name='update_user'),
    url(r'^parse/$',views.linkedin_companies_parser,name="linkedin_companies_parser"),
]