from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
# Đổi text trên giao diện Admin
admin.site.site_header = "Hệ Thống Quản Trị Khóa Học"
admin.site.site_title = "Admin Web Khóa Học"
admin.site.index_title = "Chào mừng bạn đến với Bảng Điều Khiển"
urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('add-to-cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('history/', views.order_history, name='order_history'),
    path('courses/', views.all_courses, name='all_courses'),
    path('roadmaps/', views.roadmap_list, name='roadmap_list'),
    path('roadmap/<int:pk>/', views.roadmap_detail, name='roadmap_detail'),
    path('roadmap/<int:pk>/buy-combo/', views.buy_roadmap_combo, name='buy_roadmap_combo'), # Thêm dòng này
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment_qr, name='payment_qr'),
    # Cổng giả lập MoMo
    path('payment/momo/<int:order_id>/', views.momo_mock, name='momo_mock'),
    path('payment/momo-success/<int:order_id>/', views.momo_success, name='momo_success'),
    # Xác nhận đã quét mã QR thành công
    path('payment/qr-confirm/<int:order_id>/', views.confirm_qr_payment, name='confirm_qr_payment'),
    # Xóa vĩnh viễn đơn hàng khỏi lịch sử
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    # Xóa nhiều đơn hàng cùng lúc bằng checkbox
    path('order/bulk-delete/', views.bulk_delete_orders, name='bulk_delete_orders'),
    # Đổi phương thức thanh toán
    path('payment/switch/<int:order_id>/<str:method>/', views.switch_payment, name='switch_payment'),

]