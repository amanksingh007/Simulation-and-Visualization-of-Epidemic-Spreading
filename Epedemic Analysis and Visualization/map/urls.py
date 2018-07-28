from django.conf.urls import url
from map import views

app_name = 'map'

urlpatterns = [


    url(r'^register/',views.register,name='register' ),
    url(r'^index/',views.index,name='index' ),
    url(r'^user_login/',views.user_login,name='user_login' ),
    url(r'^eav/',views.eav,name = "eav"),
    url(r'^parameters/',views.para_view,name = "para_view"),




]
