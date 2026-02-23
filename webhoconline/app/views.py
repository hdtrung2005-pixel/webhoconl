from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# 1. Import chuẩn xác các model
from .models import Course, Category, Order, OrderItem, User, Lesson, Roadmap, LessonReview
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ProfileForm, ReviewForm, CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
import random

# --- 1. HÀM PHÂN QUYỀN (DECORATOR) ---
def teacher_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, "Bạn không có quyền truy cập trang này!")
            return redirect('home') 
    return wrap

# --- CÁC HÀM VIEW ---

@login_required 
def home(request):
    courses = Course.objects.all()
    return render(request, 'app/home.html', {'courses': courses})

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user_has_course = False
    
    # 1. Kiểm tra user đã mua khóa học chưa
    if request.user.is_authenticated:
        has_bought = OrderItem.objects.filter(
            order__user=request.user, 
            course=course,
            order__status='Completed' 
        ).exists()
        
        if has_bought:
            user_has_course = True

    # 2. LẤY DANH SÁCH ĐÁNH GIÁ (Dùng LessonReview)
    reviews = LessonReview.objects.filter(lesson__course=course).order_by('-created_at')
    
    review_count = reviews.count()
    average_rating = 0
    if review_count > 0:
        total_rating = sum(r.rating for r in reviews)
        average_rating = total_rating / review_count

    return render(request, 'app/detail.html', {
        'course': course,
        'user_has_course': user_has_course,
        'reviews': reviews,           
        'average_rating': round(average_rating, 1),
        'review_count': review_count
    })

def register(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def add_to_cart(request, course_id):
    cart = request.session.get('cart', {})
    course_id_str = str(course_id)
    
    if course_id_str in cart:
        cart[course_id_str] += 1
    else:
        cart[course_id_str] = 1
        
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for course_id, quantity in cart.items():
        course = get_object_or_404(Course, pk=course_id)
        subtotal = course.price * quantity
        cart_items.append({
            'course': course,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total_price += subtotal
        
    return render(request, 'app/cart.html', {
        'cart_items': cart_items, 
        'total_price': total_price
    })

def remove_from_cart(request, course_id):
    cart = request.session.get('cart', {})
    course_id_str = str(course_id)
    
    if course_id_str in cart:
        del cart[course_id_str]
        
    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, "Giỏ hàng của bạn đang trống!")
        return redirect('cart_detail')
    
    order = Order.objects.create(
        user=request.user, 
        total_price=0,
        status='Pending'
    )
    
    total_price = 0
    
    for course_id, quantity in cart.items():
        try:
            course = Course.objects.get(id=course_id)
            OrderItem.objects.create(
                order=order,
                course=course,
                price=course.price,
                quantity=quantity
            )
            total_price += course.price * quantity
            
        except Course.DoesNotExist:
            continue
        
    order.total_price = total_price
    order.save()
    
    request.session['cart'] = {} 
    messages.success(request, "Đặt hàng thành công! Cảm ơn bạn.")
    return redirect('home')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/order_history.html', {'orders': orders})

def search(request):
    query = request.GET.get('q', '') 
    courses = []

    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    return render(request, 'app/search.html', {'courses': courses, 'query': query})

def all_courses(request):
    courses_list = Course.objects.all().order_by('-id') 
    categories = Category.objects.all() 

    cate_id = request.GET.get('category')
    if cate_id:
        courses_list = courses_list.filter(category_id=cate_id)

    paginator = Paginator(courses_list, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/all_courses.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_cate': cate_id
    })

def roadmap_list(request):
    roadmaps = Roadmap.objects.all()
    return render(request, 'app/roadmap.html', {'roadmaps': roadmaps})

def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    return render(request, 'app/roadmap_detail.html', {'roadmap': roadmap})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'app/profile.html', {'form': form})
@login_required
def watch_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # 1. Chặn người chưa mua hoặc chưa thanh toán xong
    has_bought = OrderItem.objects.filter(
        order__user=request.user, 
        course=course, 
        order__status='Completed'
    ).exists()
    
    if not has_bought and request.user.role != 'teacher' and not request.user.is_superuser:
        messages.warning(request, "Bạn cần thanh toán hoàn tất để xem bài giảng này!")
        return redirect('detail', course_id=course_id)
    
    # 2. Xử lý bài học và đánh giá
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    
    # Lấy đánh giá của bài học này (dùng LessonReview)
    reviews = LessonReview.objects.filter(lesson=lesson).order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.lesson = lesson
            review.save() # Lưu vào bảng LessonReview
            messages.success(request, "Cảm ơn bạn đã gửi đánh giá!")
            return redirect('watch_lesson', course_id=course_id, lesson_id=lesson_id)
    else:
        form = ReviewForm()

    return render(request, 'app/watch_lesson.html', {
        'course': course,
        'current_lesson': lesson, 
        'lessons': course.lessons.all(),
        'reviews': reviews,        
        'form': form,             
    })

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if order.status == 'Pending':
        order.status = 'Canceled'
        order.save()
        messages.success(request, "Đã hủy đơn hàng thành công!")
    else:
        messages.error(request, "Đơn hàng này không thể hủy (Đã hoàn thành hoặc đã hủy).")
    
    return redirect('order_history')
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Kiểm tra xem email có tồn tại trong hệ thống không
        user = User.objects.filter(email=email).first()
        
        if user:
            # 1. Tạo mã OTP 6 số
            otp = str(random.randint(100000, 999999))
            
            # 2. Lưu OTP và Email vào Session (bộ nhớ tạm) để lát nữa kiểm tra
            request.session['otp'] = otp
            request.session['reset_email'] = email
            
            # 3. Gửi email
            subject = 'Mã xác nhận lấy lại mật khẩu'
            message = f'Chào bạn, mã OTP để lấy lại mật khẩu của bạn là: {otp}. Vui lòng không chia sẻ cho ai!'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            
            messages.success(request, 'Mã OTP đã được gửi đến email của bạn!')
            return redirect('verify_otp')
        else:
            messages.error(request, 'Email này chưa được đăng ký trong hệ thống!')
            
    return render(request, 'app/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        real_otp = request.session.get('otp')
        
        if user_otp == real_otp:
            messages.success(request, 'Xác thực thành công! Mời bạn nhập mật khẩu mới.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Mã OTP không chính xác hoặc đã hết hạn!')
            
    return render(request, 'app/verify_otp.html')

def reset_password(request):
    # Đảm bảo người dùng đã qua bước nhập email
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user = User.objects.get(email=email)
            user.set_password(new_password) # Mã hóa mật khẩu mới
            user.save()
            
            # Xóa session sau khi đổi thành công
            del request.session['otp']
            del request.session['reset_email']
            
            messages.success(request, 'Đổi mật khẩu thành công! Bạn có thể đăng nhập ngay.')
            return redirect('login')
        else:
            messages.error(request, 'Mật khẩu nhập lại không khớp!')
            
    return render(request, 'app/reset_password.html')