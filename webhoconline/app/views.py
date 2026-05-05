import os
import json
import random
from dotenv import load_dotenv
import google.generativeai as genai

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction

from .models import Course, Category, Order, OrderItem, User, Lesson, Roadmap, LessonReview
from .forms import ProfileForm, ReviewForm, CustomUserCreationForm

# --- BẢO MẬT: LẤY API KEY TỪ FILE .env ---
load_dotenv()
# Sửa lại dòng cấu hình API ở đầu file views.py
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY, transport='rest')
# --- HÀM PHÂN QUYỀN ---
def teacher_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return function(request, *args, **kwargs)
        messages.warning(request, "Bạn không có quyền truy cập trang này!")
        return redirect('home')
    return wrap

# --- CÁC HÀM VIEW TRANG CHỦ & TÌM KIẾM ---
def home(request):
    # Đã gỡ bỏ filter status để khớp với Database của bác
    courses = Course.objects.all().order_by('-created_at')
    my_courses = []
    
    if request.user.is_authenticated:
        my_courses = Course.objects.filter(
            orderitem__order__user=request.user,
            orderitem__order__status='Completed'
        ).distinct()

    featured_courses = Course.objects.annotate(
        num_students=Count('orderitem', filter=Q(orderitem__order__status='Completed'))
    ).order_by('-num_students')[:4]

    return render(request, 'app/home.html', {
        'courses': courses, 'my_courses': my_courses, 'featured_courses': featured_courses,
    })

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user_has_course = False

    if request.user.is_authenticated:
        has_bought = OrderItem.objects.filter(
            order__user=request.user, course=course, order__status='Completed'
        ).exists()
        if has_bought or request.user.role == 'teacher' or request.user.is_superuser:
            user_has_course = True

    reviews = LessonReview.objects.filter(lesson__course=course).order_by('-created_at')
    review_count = reviews.count()
    average_rating = sum(r.rating for r in reviews) / review_count if review_count > 0 else 0

    price_formatted = f"{int(course.price):,}".replace(",", ".")
    
    return render(request, 'app/detail.html', {
        'course': course, 
        'user_has_course': user_has_course,
        'reviews': reviews, 
        'average_rating': round(average_rating, 1), 
        'review_count': review_count,
        'price_formatted': price_formatted  # THÊM DÒNG NÀY VÀO LÀ ĂN TIỀN
    })

def search(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else []
    return render(request, 'app/search.html', {'courses': courses, 'query': query})

def all_courses(request):
    courses_list = Course.objects.all().order_by('-id')
    cate_id = request.GET.get('category')
    if cate_id:
        courses_list = courses_list.filter(category_id=cate_id)

    paginator = Paginator(courses_list, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'app/all_courses.html', {
        'page_obj': page_obj, 'categories': Category.objects.all(), 'current_cate': cate_id
    })

# --- XÁC THỰC TÀI KHOẢN (AUTH) ---
def register(request):
    if request.method == 'POST':
        # 1. Khai báo form với dữ liệu người dùng gửi lên
        form = CustomUserCreationForm(request.POST)
        
        # 2. Lấy email từ dữ liệu form để kiểm tra
        email = request.POST.get('email')

        # 3. Kiểm tra email trùng
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email này đã được đăng ký. Vui lòng sử dụng email khác!')
            return redirect('register') 
        
        # 4. Nếu email chưa ai dùng, tiếp tục kiểm tra form có hợp lệ không
        if form.is_valid():
            user = form.save()
            login(request, user) # Đăng nhập luôn sau khi tạo tài khoản
            messages.success(request, "Đăng ký thành công!")
            return redirect('home')
        else:
            # Nếu form không hợp lệ (ví dụ: mật khẩu quá ngắn, không khớp...)
            messages.error(request, "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.")
    else:
        # Nếu là phương thức GET (vào trang đăng ký)
        form = CustomUserCreationForm()
        
    return render(request, 'app/register.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    # 1. Khởi tạo form với dữ liệu hiện tại của user để hiển thị lên giao diện
    form = ProfileForm(instance=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.user
        
        if action == 'update_info':
            # 2. Dùng ProfileForm để hứng dữ liệu (Phải có cái này thì nó mới chạy hàm check chặn số)
            form = ProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Cập nhật hồ sơ thành công!")
                return redirect('profile')
            else:
                messages.error(request, "Cập nhật thất bại. Vui lòng kiểm tra lỗi bên dưới!")
                
        elif action == 'change_password':
            old_pwd = request.POST.get('old_password')
            new_pwd = request.POST.get('new_password')
            if not user.check_password(old_pwd): 
                messages.error(request, "Mật khẩu cũ sai!")
            elif new_pwd != request.POST.get('confirm_password'): 
                messages.error(request, "Xác nhận không khớp!")
            elif len(new_pwd) < 6: 
                messages.error(request, "Mật khẩu > 6 ký tự!")
            else:
                user.set_password(new_pwd)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Đổi mật khẩu thành công!")
            return redirect('profile')

    return render(request, 'app/profile.html', {'form': form})
# --- GIỎ HÀNG VÀ THANH TOÁN ---
@login_required(login_url='login')
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    already_processing = OrderItem.objects.filter(
        order__user=request.user, course=course, order__status__in=['Completed', 'Pending']
    ).exists()
    
    if already_processing:
        messages.warning(request, f"Khóa học '{course.title}' đã mua hoặc đang có đơn chờ thanh toán!")
        return redirect('detail', course_id=course.id)

    cart = request.session.get('cart', {})
    if str(course_id) in cart:
        messages.info(request, "Khóa học đã có trong giỏ hàng!")
    else:
        cart[str(course_id)] = 1
        messages.success(request, f"Đã thêm '{course.title}' vào giỏ!")
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for course_id, quantity in cart.items():
        course = get_object_or_404(Course, pk=course_id)
        subtotal = course.price * quantity
        cart_items.append({'course': course, 'quantity': quantity, 'subtotal': subtotal})
        total_price += subtotal
        
    formatted_total = f"{int(total_price):,}".replace(",", ".")


    return render(request, 'app/cart.html', {
        'cart_items': cart_items, 
        'total_price': total_price,
        'formatted_total': formatted_total 
    })
def remove_from_cart(request, course_id):
    cart = request.session.get('cart', {})
    cart.pop(str(course_id), None)
    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.warning(request, "Giỏ hàng trống!")
            return redirect('cart_detail')

        with transaction.atomic():
            total_price = sum(get_object_or_404(Course, id=cid).price * qty for cid, qty in cart.items())
            order = Order.objects.create(
                user=request.user, total_price=total_price,
                payment_method=request.POST.get('payment_method', 'banking'), status='Pending'
            )
            for course_id, qty in cart.items():
                course = get_object_or_404(Course, id=course_id)
                OrderItem.objects.create(order=order, course=course, price=course.price, quantity=qty)

        request.session['cart'] = {}
        messages.success(request, "Chốt đơn thành công! Vui lòng thanh toán.")
        return redirect('payment_qr', order_id=order.id)
    return redirect('cart_detail')

# --- LỘ TRÌNH HỌC (ROADMAP) ---
def roadmap_list(request):
    return render(request, 'app/roadmap.html', {'roadmaps': Roadmap.objects.all()})

def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    courses = roadmap.courses.all()
    
    # Tính giá gốc và giá combo
    original_price = sum(c.price for c in courses)
    combo_price = int(float(original_price) * 0.8) if original_price > 0 else 0
    
    # --- ĐOẠN MỚI THÊM: ÉP ĐỊNH DẠNG TIỀN VNĐ ---
    original_price_formatted = f"{int(original_price):,}".replace(",", ".")
    combo_price_formatted = f"{int(combo_price):,}".replace(",", ".")

    # Truyền thêm 2 biến mới ra HTML
    return render(request, 'app/roadmap_detail.html', {
        'roadmap': roadmap, 
        'courses': courses, 
        'original_price': original_price, 
        'combo_price': combo_price,
        'original_price_formatted': original_price_formatted, # Gửi giá gốc đã phẩy
        'combo_price_formatted': combo_price_formatted        # Gửi giá combo đã phẩy
    })
@login_required(login_url='login')
def buy_roadmap_combo(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    courses = roadmap.courses.all()
    
    courses_to_buy = []
    total_combo_price = 0
    
    for course in courses:
        if not OrderItem.objects.filter(order__user=request.user, order__status__in=['Completed', 'Pending'], course=course).exists():
            courses_to_buy.append(course)
            total_combo_price += int(float(course.price) * 0.8)

    if not courses_to_buy:
        messages.info(request, "Bạn đã sở hữu (hoặc đang chờ duyệt) toàn bộ khóa học trong lộ trình này!")
        return redirect('roadmap_detail', pk=pk)

    with transaction.atomic():
        order = Order.objects.create(user=request.user, total_price=total_combo_price, status='Pending')
        for course in courses_to_buy:
            OrderItem.objects.create(order=order, course=course, price=int(float(course.price) * 0.8), quantity=1)

    messages.success(request, f"Đã chốt đơn Combo {len(courses_to_buy)} khóa học!")
    return redirect('payment_qr', order_id=order.id)

# --- XEM VIDEO VÀ ĐÁNH GIÁ ---
@login_required
def watch_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if not (OrderItem.objects.filter(order__user=request.user, course=course, order__status='Completed').exists() 
            or request.user.role == 'teacher' or request.user.is_superuser):
        messages.warning(request, "Bạn cần thanh toán để xem bài giảng!")
        return redirect('detail', course_id=course_id)

    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
    reviews = LessonReview.objects.filter(lesson=lesson).order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.lesson = lesson
            review.save()
            messages.success(request, "Đã gửi đánh giá!")
            return redirect('watch_lesson', course_id=course_id, lesson_id=lesson_id)
    else:
        form = ReviewForm()

    return render(request, 'app/watch_lesson.html', {
        'course': course, 'current_lesson': lesson, 'lessons': course.lessons.all().order_by('order'), 
        'reviews': reviews, 'form': form
    })

# --- QUẢN LÝ ĐƠN HÀNG VÀ THANH TOÁN CÁC LOẠI ---
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/order_history.html', {'orders': orders})

@login_required
def payment_qr(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    bank_code = getattr(settings, 'BANK_CODE', 'MB')
    account_no = getattr(settings, 'BANK_ACCOUNT_NUMBER', '0916536176')
    account_name = getattr(settings, 'BANK_ACCOUNT_NAME', 'HA DUC TRUNG')
    
    amount = int(order.total_price)
    add_info = f"Thanh toan don hang {order.id}"
    
    # ÉP ĐỊNH DẠNG TIỀN BẰNG PYTHON (10000 -> "10.000")
    amount_formatted = f"{amount:,}".replace(",", ".")
    
    qr_url = f"https://img.vietqr.io/image/{bank_code}-{account_no}-compact2.png?amount={amount}&addInfo={add_info.replace(' ', '%20')}&accountName={account_name.replace(' ', '%20')}"
    
    context = {
        'order': order,
        'qr_url': qr_url,
        'bank_code': bank_code,
        'account_no': account_no,
        'account_name': account_name,
        'amount_formatted': amount_formatted, # Gửi số tiền ĐÃ PHẨY ra ngoài
        'add_info': add_info,                 # Gửi nội dung chuyển khoản ra ngoài
    }
    return render(request, 'app/payment_qr.html', context)
@login_required
def confirm_qr_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # KHI KHÁCH BẤM ĐÃ CHUYỂN KHOẢN -> KHÓA ĐƠN LẠI THÀNH CHỜ DUYỆT
    order.status = 'Processing'
    order.save()
    
    messages.success(request, "Đã ghi nhận thanh toán, vui lòng chờ Admin duyệt!")
    return redirect('order_history')
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status == 'Pending':
        order.status = 'Canceled'
        order.save()
        messages.success(request, "Đã hủy đơn hàng thành công!")
    else:
        messages.error(request, "Không thể hủy đơn hàng này!")
    return redirect('order_history')

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status in ['Pending', 'Canceled']:
        order.delete()
        messages.success(request, "Đã xóa đơn hàng khỏi hệ thống!")
    else:
        messages.error(request, "Không thể xóa đơn hàng đã hoàn thành!")
    return redirect('order_history')

@login_required
def momo_mock(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # 1. Ép định dạng tiền (Ví dụ: 10000 -> "10.000")
    total_price = int(order.total_price)
    price_formatted = f"{total_price:,}".replace(",", ".")
    
    # 2. Tạo nội dung chuyển khoản
    add_info = f"Thanh toan don hang {order.id}"
    
    context = {
        'order': order,
        'price_formatted': price_formatted, # Biến tiền đã phẩy
        'add_info': add_info,               # Biến nội dung
    }
    return render(request, 'app/momo_mock.html', context)
@login_required
def momo_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = 'Processing'
    order.save()
    
    messages.success(request, "Đã ghi nhận thanh toán MoMo, vui lòng chờ Admin duyệt!")
    return redirect('order_history')
@login_required
def switch_payment(request, order_id, method):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status == 'Pending':
        order.payment_method = method
        order.save()
        messages.info(request, "Đã đổi phương thức thanh toán!")
        if method == 'momo':
            return redirect('momo_mock', order_id=order.id)
        elif method == 'banking':
            return redirect('payment_qr', order_id=order.id)
    return redirect('order_history')

@login_required
def bulk_delete_orders(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('order_ids')
        if order_ids:
            Order.objects.filter(
                id__in=order_ids, user=request.user, status__in=['Pending', 'Canceled']
            ).delete()
            messages.success(request, f"Đã xóa thành công {len(order_ids)} đơn hàng!")
    return redirect('order_history')

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def revenue_stats(request):
    total_rev_raw = Order.objects.filter(status='Completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Định dạng tổng doanh thu (Ví dụ: 2910000 -> "2.910.000")
    total_revenue_formatted = f"{int(total_rev_raw):,}".replace(",", ".")
    
    course_stats_raw = OrderItem.objects.filter(order__status='Completed')\
        .values('course__title')\
        .annotate(total_earned=Sum('price'), total_sold=Count('id'))\
        .order_by('-total_earned')


    # Định dạng lại giá cho từng khóa học trong danh sách
    for item in course_stats_raw:
        item['earned_formatted'] = f"{int(item['total_earned']):,}".replace(",", ".")

    labels = [item['course__title'] for item in course_stats_raw]
    data = [float(item['total_earned']) for item in course_stats_raw]

    return render(request, 'app/stats.html', {
        'total_revenue': total_revenue_formatted, # Gửi số đã định dạng
        'course_stats': course_stats_raw,
        'chart_labels': labels,
        'chart_data': data,
    })
# --- TÍNH NĂNG AI TRỢ GIẢNG & TƯ VẤN ---
@login_required
def ask_ai_tutor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            if not question:
                return JsonResponse({'status': 'error', 'message': 'Câu hỏi trống!'})

            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"Bạn là trợ giảng IT của CEO HỌC LẬP TRÌNH. Giải đáp bài học '{data.get('lesson_title')}'. Câu hỏi: {question}"
            response = model.generate_content(prompt)
            return JsonResponse({'status': 'success', 'answer': response.text})
        except Exception as e:
         error_msg = str(e)
    if "429" in error_msg or "Quota" in error_msg:
        return JsonResponse({'status': 'error', 'message': 'AI đang bận trả lời nhiều học viên cùng lúc, bác đợi khoảng 30 giây rồi hỏi lại nhé!'})
    return JsonResponse({'status': 'error', 'message': 'Lỗi kết nối AI, vui lòng thử lại sau!'})
@login_required
def ai_consultant(request):
    if request.method == 'POST':
        try:
            question = json.loads(request.body).get('question', '').strip()
            course_list = "\n".join([f"- {c.title}: {c.price}đ" for c in Course.objects.all()])
            
            # Dùng chuẩn bản 2.5 mới nhất
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"Bạn là tư vấn viên tuyển sinh HỌC LẬP TRÌNH. Khóa học có sẵn:\n{course_list}\nKhách hỏi: {question}"
            
            response = model.generate_content(prompt)
            return JsonResponse({'status': 'success', 'answer': response.text})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

        # --- OTP RESET PASSWORD ---
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['reset_email'] = email
            request.session['otp_verified'] = False 
            send_mail('Mã OTP lấy lại mật khẩu', f'Mã của bạn là: {otp}', settings.EMAIL_HOST_USER, [email])
            messages.success(request, 'Đã gửi mã OTP!')
            return redirect('verify_otp')
        messages.error(request, 'Email chưa đăng ký!')
    return render(request, 'app/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        if session_otp and user_otp == session_otp:
            request.session['otp_verified'] = True 
            return redirect('reset_password')
        messages.error(request, 'Mã OTP sai hoặc đã hết hạn!')
    return render(request, 'app/verify_otp.html')




def reset_password(request):
    email = request.session.get('reset_email')
    is_verified = request.session.get('otp_verified')
    
    if not email or not is_verified: 
        messages.error(request, 'Yêu cầu xác thực OTP trước!')
        return redirect('forgot_password')
        
    if request.method == 'POST':
        if request.POST.get('new_password') == request.POST.get('confirm_password'):
            user = User.objects.get(email=email)
            user.set_password(request.POST.get('new_password'))
            user.save()
            
            del request.session['otp']
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, 'Đổi mật khẩu thành công!')
            return redirect('login')
        messages.error(request, 'Mật khẩu không khớp!')
    return render(request, 'app/reset_password.html')