"""dx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import  url


urlpatterns = [
    url(r'^$', 'devop.views.index', name='index'),
    url(r'^all$', 'devop.views.get_all', name='api_all'),
    url(r'^(?P<sys_type>[w|a|p])/(?P<sys_name>\w{2,20})/$', 'devop.views.generate_yaml', name='t'),
    url(r'^(?P<sys_type>[w|a|p])/(?P<sys_name>\w{2,20})/(?P<data_format>\bstr\b|\bjson\b)$',
         'devop.views.query', name='search'
    ),
]
