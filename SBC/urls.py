"""SBC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^buscador$', views.buscador_pm_index, name="buscador"),
    url(r'^plantas_ajax/$', views.plantas_ajax, name="plantas_ajax"),

    # Extraccion de la informacion
    url(r'^anotador/$', views.extraccion_informacion, name="anotador"),
    url(r'^buscador_skos/$', views.buscador_skos, name="buscador_skos"),


    url(r'^visualizador/$', views.visualizador, name="visualizador"),
    url(r'^visualizador2/$', views.visualizador2, name="visualizador2"),
]
