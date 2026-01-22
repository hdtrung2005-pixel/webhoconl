from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ProfileForm, ReviewForm 

# --- CÁC HÀM VIEW ---

@login_required 
def home(request):
    courses = Course.objects.all()
    return render(request, 'app/home.html', {'courses': courses})

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user_has_course = False
    
    # Kiểm tra user đã mua khóa học chưa
    if request.user.is_authenticated:
        # Kiểm tra trong bảng OrderItem xem user đã mua course này chưa
        has_bought = OrderItem.objects.filter(order__user=request.user, course=course).exists()
        if has_bought:
            user_has_course = True

    return render(request, 'app/detail.html', {
        'course': course,
        'user_has_course': user_has_course 
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserCreationForm()
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
        total_price=0 
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
        form = ProfileForm(request.POST, instance=request.user)
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
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lessons = course.lessons.all()

    # Lấy danh sách đánh giá cũ
    reviews = lesson.reviews.all().order_by('-created_at')

    # Xử lý Form đánh giá
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.lesson = lesson
            review.save()
            messages.success(request, "Cảm ơn bạn đã gửi đánh giá!")
            return redirect('watch_lesson', course_id=course_id, lesson_id=lesson_id)
    else:
        form = ReviewForm()

    return render(request, 'app/watch_lesson.html', {
        'course': course,
        'current_lesson': lesson, 
        'lessons': lessons,
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
        messages.error(request, "Đơn hàng này không thể hủy.")
    
    return redirect('order_history')