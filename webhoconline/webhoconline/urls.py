"""
URL configuration for webhoconline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from app import views  # Import views từ ứng dụng 'app'
from django.contrib.auth import views as auth_views # Import LoginView có sẵn
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = "HỆ THỐNG QUẢN TRỊ KHÓA HỌC"
admin.site.site_title = "Admin Web Học Online"
admin.site.index_title = "Chào mừng quản trị viên"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.watch_lesson, name='watch_lesson'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)