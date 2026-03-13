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
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash # Hàm xịn chống văng đăng xuất
from django.db.models import Sum, Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
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
    # 1. LẤY TẤT CẢ KHÓA HỌC (Dành cho phần "Khám phá khóa học")
    # Sắp xếp theo khóa mới nhất đưa lên đầu
    courses = Course.objects.all().order_by('-created_at')

    # 2. KHÓA HỌC CỦA TÔI (Chỉ lấy khi khách đã đăng nhập và mua thành công)
    my_courses = []
    if request.user.is_authenticated:
        my_courses = Course.objects.filter(
            orderitem__order__user=request.user,
            orderitem__order__status='Completed'
        ).distinct()

    # 3. KHÓA HỌC NỔI BẬT (Đếm lượng mua thành công và xếp Top 4)
    featured_courses = Course.objects.annotate(
        num_students=Count('orderitem', filter=Q(orderitem__order__status='Completed'))
    ).order_by('-num_students')[:4]

    # 4. TRUYỀN TẤT CẢ DỮ LIỆU RA GIAO DIỆN
    context = {
        'courses': courses,                   # Nhớ phải có dòng này thì Khám phá mới có hàng
        'my_courses': my_courses,             # Dòng này cho Khóa học của tôi
        'featured_courses': featured_courses, # Dòng này cho Khóa học nổi bật
    }
    
    return render(request, 'app/home.html', context)
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
        if has_bought or request.user.role == 'teacher' or request.user.is_superuser:
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
        # Đã sửa: Dùng đúng CustomUserCreationForm để xử lý dữ liệu POST
        # Không dùng instance=request.user vì đây là tài khoản mới tạo, chưa tồn tại
        form = CustomUserCreationForm(request.POST) 
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Đăng ký tài khoản thành công!")
            return redirect('home')
        else:
            messages.error(request, "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.")
    else:
        # Form lúc mới vào trang (GET)
        form = CustomUserCreationForm()
        
    return render(request, 'app/register.html', {'form': form})
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    cart = request.session.get('cart', {})
    course_id_str = str(course_id)
    
    if course_id_str in cart:
        # Nếu đã có trong giỏ -> Chỉ báo Info, KHÔNG cộng dồn số lượng
        messages.info(request, f"💡 Khóa học '{course.title}' đã nằm trong giỏ hàng của bạn rồi!")
    else:
        # Nếu chưa có -> Thêm mới với số lượng mặc định là 1
        cart[course_id_str] = 1
        messages.success(request, f"🛒 Đã thêm '{course.title}' vào giỏ hàng!")
        
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'home'))
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

@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        # 1. Lấy giỏ hàng hiện tại
        cart = request.session.get('cart', {})
        if not cart:
            messages.warning(request, "Giỏ hàng của bạn đang trống!")
            return redirect('cart_detail')

        # 2. Lấy phương thức thanh toán khách vừa chọn (banking hoặc momo)
        payment_method = request.POST.get('payment_method', 'banking')

        # 3. Tính tổng tiền
        total_price = 0
        for course_id, quantity in cart.items():
            course = get_object_or_404(Course, id=course_id)
            total_price += course.price * quantity

        # 4. Tạo Đơn hàng (Order) vào Database
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_method=payment_method,
            status='Pending' # Mới đặt, chưa thanh toán
        )

        # 5. Đưa từng khóa học vào Chi tiết đơn hàng (OrderItem)
        for course_id, quantity in cart.items():
            course = get_object_or_404(Course, id=course_id)
            OrderItem.objects.create(
                order=order,
                course=course,
                price=course.price
            )

        # 6. XÓA SẠCH GIỎ HÀNG (Vì đã chốt đơn xong)
        request.session['cart'] = {}

        # 7. Chuyển hướng sang trang Hiện Mã QR Thanh toán
        messages.success(request, "🎉 Đã chốt đơn thành công! Vui lòng thanh toán để vào học.")
        return redirect('payment_qr', order_id=order.id)
        
    return redirect('cart_detail')
@login_required
def order_history(request):
    hidden_orders = request.session.get('hidden_orders', [])
    orders = Order.objects.filter(user=request.user).exclude(id__in=hidden_orders).order_by('-created_at')
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
    courses = roadmap.courses.all()
    
    # Tính tổng tiền gốc của tất cả khóa học
    original_price = sum([c.price for c in courses])
    # Tự động giảm giá 20% khi mua Combo lộ trình
    combo_price = float(original_price) * 0.8 if original_price > 0 else 0

    context = {
        'roadmap': roadmap,
        'courses': courses,
        'original_price': original_price,
        'combo_price': combo_price,
    }
    return render(request, 'app/roadmap_detail.html', context)

@login_required(login_url='login')
def buy_roadmap_combo(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    courses = roadmap.courses.all()

    # TẠO THẲNG 1 ĐƠN HÀNG MỚI (MUA NGAY KHÔNG QUA GIỎ HÀNG)
    order = Order.objects.create(user=request.user, total_price=0, status='Pending')
    
    total_combo_price = 0
    added_count = 0
    
    for course in courses:
        # Kiểm tra xem khách đã mua thành công khóa này chưa
        already_owned = OrderItem.objects.filter(
            order__user=request.user, 
            order__status='Completed', 
            course=course
        ).exists()
        
        if not already_owned:
            # Thêm vào đơn hàng với giá đã GIẢM 20%
            discounted_price = float(course.price) * 0.8
            OrderItem.objects.create(
                order=order, 
                course=course, 
                price=discounted_price, 
                quantity=1
            )
            total_combo_price += discounted_price
            added_count += 1
            
    if added_count > 0:
        # Cập nhật tổng tiền và lưu đơn
        order.total_price = total_combo_price
        order.save()
        messages.success(request, f"🎉 Đã chốt đơn Combo Lộ trình ({added_count} khóa). Vui lòng quét mã thanh toán!")
        return redirect('payment_qr', order_id=order.id) # Bắn thẳng ra trang QR
    else:
        # Nếu khách đã mua hết các khóa này rồi thì hủy cái đơn rỗng vừa tạo đi
        order.delete()
        messages.info(request, "💡 Bạn đã sở hữu toàn bộ khóa học trong lộ trình này rồi, không cần mua nữa nhé!")
        return redirect('roadmap_detail', pk=pk)


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        # Lấy biến action để biết người dùng đang submit form nào
        action = request.POST.get('action')

        # ==========================================
        # FORM 1: XỬ LÝ CẬP NHẬT THÔNG TIN
        # ==========================================
        if action == 'update_info':
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            avatar = request.FILES.get('avatar') # Nhận file ảnh

            user = request.user
            user.full_name = full_name
            user.email = email
            if avatar:
                user.avatar = avatar
            user.save()
            messages.success(request, "🎉 Cập nhật thông tin hồ sơ thành công!")
            return redirect('profile')

        # ==========================================
        # FORM 2: XỬ LÝ ĐỔI MẬT KHẨU
        # ==========================================
        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user = request.user

            # Kiểm tra 3 lớp bảo mật
            if not user.check_password(old_password):
                messages.error(request, "❌ Mật khẩu hiện tại không chính xác!")
            elif new_password != confirm_password:
                messages.error(request, "❌ Mật khẩu mới và xác nhận không khớp!")
            elif len(new_password) < 6:
                messages.error(request, "❌ Mật khẩu mới phải có ít nhất 6 ký tự!")
            else:
                # Nếu qua hết bài test -> Đổi mật khẩu
                user.set_password(new_password)
                user.save()
                # Quan trọng: Cập nhật lại session để người dùng KHÔNG bị văng ra ngoài
                update_session_auth_hash(request, user) 
                messages.success(request, "🔒 Đổi mật khẩu thành công! Tài khoản của bạn đã an toàn.")
            
            return redirect('profile')

    return render(request, 'app/profile.html')
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
@login_required
def momo_mock(request, order_id):
    # Lấy đơn hàng ra để hiển thị trên trang giả lập MoMo
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'app/momo_mock.html', {'order': order})

@login_required
def momo_success(request, order_id):
    # Hàm này đóng vai trò như hệ thống MoMo báo thanh toán thành công
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    # Tự động chuyển trạng thái đơn hàng thành "Completed" (Đã thanh toán)
    if order.status == 'Pending':
        order.status = 'Completed'
        order.save()
        
    messages.success(request, "Thanh toán qua MoMo thành công! Khóa học đã được mở.")
    return redirect('order_history')
@login_required
def confirm_qr_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    # Nếu đơn đang chờ xử lý thì đổi thành Hoàn thành
    if order.status == 'Pending':
        order.status = 'Completed'
        order.save()
        messages.success(request, "Hệ thống đã ghi nhận thanh toán! Khóa học của bạn đã được mở.")
    
    return redirect('order_history')
@login_required
def delete_order(request, order_id):
    # Tìm đơn hàng của đúng user đang đăng nhập
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    hidden_orders = request.session.get('hidden_orders', [])
    if order_id not in hidden_orders:
        hidden_orders.append(order_id)
        request.session['hidden_orders'] = hidden_orders
        request.session.modified = True  # Lệnh này báo cho Django biết Session đã thay đổi
        
    messages.success(request, "Đã xóa đơn hàng khỏi lịch sử!")
    return redirect('order_history')
@login_required
def bulk_delete_orders(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('order_ids')
        
        if order_ids:
            hidden_orders = request.session.get('hidden_orders', [])
            
            # Nhét tất cả các ID vừa được tích Checkbox vào danh sách đen
            for oid in order_ids:
                if int(oid) not in hidden_orders:
                    hidden_orders.append(int(oid))
                    
            request.session['hidden_orders'] = hidden_orders
            request.session.modified = True
            
            messages.success(request, f"Đã dọn dẹp {len(order_ids)} đơn hàng khỏi màn hình!")
        else:
            messages.warning(request, "Bạn chưa tích chọn đơn hàng nào để xóa.")
            
    return redirect('order_history')
# ==========================================
# TRANG HIỂN THỊ MÃ QUÉT QR THANH TOÁN
# ==========================================
@login_required(login_url='login')
def payment_qr(request, order_id):
    # Lấy đúng đơn hàng của user này (chống hack xem trộm đơn người khác)
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Lấy thông tin ngân hàng từ settings.py
    bank_code = settings.BANK_CODE
    account_no = settings.BANK_ACCOUNT_NUMBER
    account_name = settings.BANK_ACCOUNT_NAME
    
    # Ép kiểu số tiền về số nguyên và tạo nội dung chuyển khoản
    amount = int(order.total_price)
    add_info = f"Thanh toan don hang {order.id}"
    
    # Format lại tên để ghép vào URL (thay dấu cách bằng %20)
    account_name_url = account_name.replace(' ', '%20')
    add_info_url = add_info.replace(' ', '%20')
    
    # Link gọi API tạo ảnh QR động của VietQR
    qr_url = f"https://img.vietqr.io/image/{bank_code}-{account_no}-compact2.png?amount={amount}&addInfo={add_info_url}&accountName={account_name_url}"
    
    context = {
        'order': order,
        'qr_url': qr_url,
        'bank_code': bank_code,
        'account_no': account_no,
        'account_name': account_name,
        'amount': amount,
        'add_info': add_info,
    }
    return render(request, 'app/payment_qr.html', context)
@login_required
def switch_payment(request, order_id, method):
    # 1. Tìm đúng đơn hàng của khách
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    # 2. Chỉ cho phép đổi khi đơn hàng chưa thanh toán (Pending)
    if order.status == 'Pending':
        order.payment_method = method
        order.save()
        messages.info(request, "🔄 Đã đổi phương thức thanh toán thành công!")
        
        # 3. Chuyển hướng theo phương thức mới
        if method == 'momo':
            return redirect('momo_mock', order_id=order.id)
        elif method == 'banking':
            return redirect('payment_qr', order_id=order.id)
            
    return redirect('order_history')
# ==========================================
# TRANG THỐNG KÊ DOANH THU (CHỈ DÀNH CHO ADMIN)
# ==========================================
@user_passes_test(lambda u: u.is_superuser, login_url='login') # Chặn người lạ, chỉ Admin mới vào được
def revenue_stats(request):
    # 1. Tính TỔNG DOANH THU từ trước đến nay (Chỉ tính đơn đã Completed)
    total_revenue = Order.objects.filter(status='Completed').aggregate(Sum('total_price'))['total_price__sum'] or 0

    # 2. Tính doanh thu và số lượt mua theo TỪNG KHÓA HỌC
    course_stats = OrderItem.objects.filter(order__status='Completed') \
        .values('course__title') \
        .annotate(total_earned=Sum('price'), total_sold=Count('id')) \
        .order_by('-total_earned') # Sắp xếp khóa nào kiếm nhiều tiền nhất lên đầu

    # 3. Chuẩn bị dữ liệu để vẽ Biểu đồ (Tách tên khóa học và tiền ra 2 danh sách)
    labels = [item['course__title'] for item in course_stats]
    data = [float(item['total_earned']) for item in course_stats]

    context = {
        'total_revenue': total_revenue,
        'course_stats': course_stats,
        'chart_labels': labels,
        'chart_data': data,
    }
    return render(request, 'app/stats.html', context)