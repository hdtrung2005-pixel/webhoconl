from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Thêm thư viện này để Django tự động tìm ảnh tĩnh (Zalo, MoMo...) cực chuẩn
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 

# Cấu hình text cho Admin
admin.site.site_header = "HỆ THỐNG QUẢN TRỊ KHÓA HỌC"
admin.site.site_title = "Admin Web Học Online"
admin.site.index_title = "Chào mừng quản trị viên"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Giao hết 100% quyền định tuyến cho app
    path('', include('app.urls')),
]

if settings.DEBUG:
    # 1. Load ảnh user tải lên (Media)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # 2. Load ảnh giao diện (Static - Zalo, MoMo, CSS...)
    urlpatterns += staticfiles_urlpatterns()