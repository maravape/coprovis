"""her_copro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path
# from django.urls import include, path

# from myapp.views import index

app_name="myapp"

urlpatterns = [
    # url(r'^$',index),
    # url(r'^', include('base.urls', namespace='base')),
    path('', include('myapp.urls', namespace='base')),
    # url(r'^admin/', include(admin.site.urls)),
    # path('admin/', include(admin.site.urls)),
    path('admin/', admin.site.urls),
    # url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    # url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
    #     name='password_reset_confirm'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
