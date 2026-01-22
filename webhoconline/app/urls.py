from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('roadmaps/<int:pk>/', views.roadmap_detail, name='roadmap_detail'),
]