"""production_kaju URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from kaju import views
from django.urls import path

app_name = "kaju"

urlpatterns = [
    # url(r'^$',views.base,name = 'base'),
    url(r'^$',views.index,name = 'index'),
    # url(r'registration/',views.register,name='register'),
    url(r'^admin/',admin.site.urls),
    url(r'login/',views.user_login,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
    # url(r'index/',views.index, name = 'index'),
    url(r'Add_static/',views.add_static, name='add_static'),
    url(r'add_country/',views.add_country,name='add_country'),
    url(r'add_region/',views.add_region,name='add_region'),
    url(r'bucket',views.bucket_vw,name='bucket'),
    url(r'dry_rcn',views.dry_rcn,name='rcn_dry'),
    url(r'processing/',views.processing,name='processing'),
    url(r'climate/', views.day_parameters,name='day_parameters'),
    url(r'cooking/',views.cooking,name = 'cooking'),
    url(r'RCN_avail',views.rcn_avail,name='rcn_avail'),
    url(r'cutting/',views.cutting,name='cutting'),
    url(r'bormah/',views.bormah,name='bormah'),
    url(r'peeling/',views.peeling, name='peeling'),
    url(r'add_grade/',views.add_grade,name ='add_grade'),
    url(r'grading/',views.grading,name='grading'),

]
