from django.urls import path
from django.contrib.auth import views as auth_views # Thêm dòng này để dùng View có sẵn của Django
from . import views

urlpatterns = [
    # Trang chủ & Hiển thị khóa học
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('courses/', views.all_courses, name='all_courses'),
    path('course/<int:course_id>/', views.detail, name='detail'),
    
    # Tính năng học & Đánh giá
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.watch_lesson, name='watch_lesson'),
    
    # Lộ trình học (Combo)
    path('roadmaps/', views.roadmap_list, name='roadmap_list'),
    path('roadmap/<int:pk>/', views.roadmap_detail, name='roadmap_detail'),
    path('roadmap/<int:pk>/buy/', views.buy_roadmap_combo, name='buy_roadmap_combo'),

    # Giỏ hàng & Mua hàng
    path('add-to-cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Quản lý đơn hàng & Thanh toán
    path('order-history/', views.order_history, name='order_history'),
    path('payment-qr/<int:order_id>/', views.payment_qr, name='payment_qr'),
    path('confirm-qr-payment/<int:order_id>/', views.confirm_qr_payment, name='confirm_qr_payment'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('bulk-delete-orders/', views.bulk_delete_orders, name='bulk_delete_orders'),
    
    # MoMo
    path('payment/momo/<int:order_id>/', views.momo_mock, name='momo_mock'),
    path('payment/momo/success/<int:order_id>/', views.momo_success, name='momo_success'),
    path('switch-payment/<int:order_id>/<str:method>/', views.switch_payment, name='switch_payment'),

    # Tài khoản & Xác thực (Auth)
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # FIX LỖI: Bổ sung Login và Logout
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Quên mật khẩu OTP
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # Tính năng AI (Trợ giảng & Tư vấn)
    path('ask-ai-tutor/', views.ask_ai_tutor, name='ask_ai_tutor'),
    path('ai-consultant/', views.ai_consultant, name='ai_consultant'),

    # Thống kê doanh thu (Admin)
    path('stats/', views.revenue_stats, name='revenue_stats'),
]