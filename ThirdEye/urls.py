"""ThirdEye URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('login',views.login,name='login'),
    path('register/', views.register, name='register'),
    path('index', views.index, name='index'),
    path('searchreport', views.searchreport, name='searchreport'),
    path('report', views.report, name='report'),
    path('create', views.create, name='create'),
    path('decode', views.decode, name='decode'),
    path('decode1', views.decode1, name='decode1'),
    path('history', views.history, name='history'),
    path('index1', views.index1, name='index1'),
    path('doc_login', views.doc_login, name='doc_login'),
    path('report1', views.report1, name='report1'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                        document_root=settings.MEDIA_ROOT)