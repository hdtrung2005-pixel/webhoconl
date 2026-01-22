from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from .models import Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ProfileForm
from .models import Lesson

# Gắn ổ khóa vào đây
@login_required 
def home(request):
    courses = Course.objects.all()
    return render(request, 'app/home.html', {'courses': courses})
def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'app/detail.html', {'course': course})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Đăng ký xong tự đăng nhập luôn
            return redirect('home')  # Quay về trang chủ
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})
def add_to_cart(request, course_id):
    # Lấy giỏ hàng hiện tại từ session (nếu chưa có thì tạo dict rỗng)
    cart = request.session.get('cart', {})
    
    # Chuyển ID sang chuỗi để làm key lưu trữ
    course_id_str = str(course_id)
    
    # Logic: Nếu có rồi thì +1, chưa có thì gán = 1
    if course_id_str in cart:
        cart[course_id_str] += 1
    else:
        cart[course_id_str] = 1
        
    # Lưu ngược lại vào session
    request.session['cart'] = cart
    
    # Chuyển hướng đến trang xem giỏ hàng
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    # Duyệt qua các ID trong giỏ để lấy thông tin chi tiết khóa học từ Database
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
    
    # Chuyển ID sang chuỗi (vì key trong session là chuỗi)
    course_id_str = str(course_id)
    
    # Kiểm tra xem sản phẩm có trong giỏ không, có thì xóa
    if course_id_str in cart:
        del cart[course_id_str]
        
    # Lưu lại session mới (QUAN TRỌNG: Quên dòng này là không xóa được)
    request.session['cart'] = cart
    
    # Xóa xong thì load lại trang giỏ hàng
    return redirect('cart_detail')
@login_required  # Nhớ dòng này để bắt buộc đăng nhập mới được thanh toán
def checkout(request):
    cart = request.session.get('cart', {})
    
    # 1. Nếu giỏ hàng trống
    if not cart:
        messages.warning(request, "Giỏ hàng của bạn đang trống!")
        return redirect('cart_detail')
    
    # 2. Tạo đơn hàng chính
    order = Order.objects.create(
        user=request.user, 
        total_price=0 
    )
    
    total_price = 0
    
    # 3. Duyệt qua giỏ hàng (Lưu ý: item ở đây chính là số lượng)
    for course_id, quantity in cart.items():
        try:
            course = Course.objects.get(id=course_id)
            
            # Tạo chi tiết đơn hàng
            OrderItem.objects.create(
                order=order,
                course=course,
                price=course.price, # <--- LẤY GIÁ TỪ DATABASE (Đúng)
                quantity=quantity   # <--- LẤY SỐ LƯỢNG TỪ GIỎ (Đúng)
            )
            
            # Cộng dồn tổng tiền
            total_price += course.price * quantity
            
        except Course.DoesNotExist:
            continue
        
    # 4. Cập nhật tổng tiền và xóa giỏ hàng
    order.total_price = total_price
    order.save()
    
    request.session['cart'] = {} # Xóa sạch giỏ hàng
    messages.success(request, "Đặt hàng thành công! Cảm ơn bạn.")
    return redirect('home')
@login_required
def order_history(request):
    # Lấy danh sách đơn hàng của user, xếp theo ngày mới nhất
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/order_history.html', {'orders': orders})
def search(request):
    query = request.GET.get('q', '') # Lấy từ khóa người dùng nhập (nếu không có thì để rỗng)
    courses = []

    if query:
        # Tìm các khóa học có Tiêu đề HOẶC Mô tả chứa từ khóa (icontains = không phân biệt hoa thường)
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    return render(request, 'app/search.html', {'courses': courses, 'query': query})
#chức năng tìm kiếm 
def all_courses(request):
    courses_list = Course.objects.all().order_by('-id') # Lấy tất cả, mới nhất lên đầu
    categories = Category.objects.all() # Lấy danh mục để làm bộ lọc

    # 1. Xử lý lọc theo danh mục (nếu user bấm vào sidebar)
    cate_id = request.GET.get('category')
    if cate_id:
        courses_list = courses_list.filter(category_id=cate_id)

    # 2. Phân trang (Mỗi trang hiện 6 khóa học)
    paginator = Paginator(courses_list, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/all_courses.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_cate': cate_id
    })
#lộ trình 
def roadmap_list(request):
    roadmaps = Roadmap.objects.all()
    return render(request, 'app/roadmap.html', {'roadmaps': roadmaps})

def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    return render(request, 'app/roadmap_detail.html', {'roadmap': roadmap})
#hồ sơ cá nhân
@login_required
def profile(request):
    # Xử lý khi người dùng bấm nút "Lưu thay đổi"
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công!")
            return redirect('profile')
    else:
        # Nếu mới vào trang thì hiện thông tin cũ
        form = ProfileForm(instance=request.user)

    return render(request, 'app/profile.html', {'form': form})
#video bài gỉang
@login_required
def watch_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Lấy bài học hiện tại
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    
    # Lấy danh sách tất cả bài học để hiển thị bên sidebar
    lessons = course.lessons.all()

    return render(request, 'app/watch_lesson.html', {
        'course': course,
        'current_lesson': lesson,
        'lessons': lessons
    })

@login_required
def cancel_order(request, order_id):
    # 1. Tìm đơn hàng theo ID và phải đúng là của người dùng đó (để tránh hủy đơn người khác)
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    # 2. Kiểm tra: Chỉ cho hủy nếu đơn đang ở trạng thái "Chờ xử lý"
    if order.status == 'Pending':
        order.status = 'Canceled' # Chuyển trạng thái thành Đã hủy
        order.save()
        messages.success(request, "Đã hủy đơn hàng thành công!")
    else:
        messages.error(request, "Đơn hàng này không thể hủy (Do đã hoàn thành hoặc đã hủy trước đó).")
    
    # 3. Quay lại trang lịch sử
    return redirect('order_history')