from django.db import models
from django.contrib.auth.models import AbstractUser
import re

# 1. Bảng User
class User(AbstractUser):
    id = models.AutoField(primary_key=True) 
    
    ROLE_CHOICES = (
        ('student', 'Học viên'),
        ('teacher', 'Giảng viên'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Vai trò")
    full_name = models.CharField(max_length=255, null=True, blank=True, db_column='full_name', verbose_name="Họ và tên")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Ảnh đại diện")

    class Meta:
        managed = True 
        db_table = 'User'
        verbose_name = "Người dùng"

# 2. Bảng Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Category'
        verbose_name = "Danh mục"
        verbose_name_plural = "Quản lý Danh mục"
    
    def __str__(self):
        return self.name

# 3. Bảng Course
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Tên khóa học")
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    instructor = models.ForeignKey(User, on_delete=models.CASCADE, 
                                   limit_choices_to={'role': 'teacher'}, 
                                   db_column='instructor_id', 
                                   null=True,
                                   verbose_name="Giảng viên")
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, 
                                 null=True, 
                                 db_column='category_id')

    class Meta:
        managed = False
        db_table = 'Course'
        verbose_name = "Khóa học"
        verbose_name_plural = "Quản lý Khóa học"

    def __str__(self):
        return self.title
    @property
    def formatted_price(self):
        # Đề phòng trường hợp khóa học miễn phí (giá = 0 hoặc rỗng)
        if not self.price:
            return "0"
        # Ép định dạng 10000 -> "10.000"
        return f"{int(self.price):,}".replace(",", ".")

# 4. Bảng Order (Đã sửa lỗi lặp field)
class Order(models.Model):
    # ĐỊNH NGHĨA CÁC TRẠNG THÁI
    STATUS_CHOICES = (
        ('Pending', 'Chờ thanh toán'),     # Mới tạo đơn, chưa trả tiền
        ('Processing', 'Đang chờ duyệt'),  # Đã bấm xác nhận chuyển khoản
        ('Completed', 'Đã hoàn thành'),
        ('Canceled', 'Đã hủy'),
    )
    
    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('banking', 'Chuyển khoản ngân hàng'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

   # is_hidden = models.BooleanField(default=False)
    # Chỉ khai báo status 1 lần duy nhất tại đây
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )  
    
    created_at = models.DateTimeField(auto_now_add=True) 
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Quản lý Đơn hàng"
   
# 5. Chi tiết đơn hàng

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.course.title}"
    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết các đơn hàng"

# 6. Giảng viên
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(verbose_name="Tiểu sử", blank=True)
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại", blank=True)
    is_approved = models.BooleanField(default=False, verbose_name="Đã được duyệt?")

    def __str__(self):
        return f"Giảng viên: {self.user.username}"
    class Meta:
        verbose_name = "Giảng viên"
        verbose_name_plural = "Danh sách Giảng viên"

# 7. Lộ trình
class Roadmap(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên lộ trình")
    description = models.TextField(verbose_name="Mô tả", blank=True)
    image = models.ImageField(upload_to='roadmaps/', verbose_name="Ảnh đại diện", blank=True, null=True)
    courses = models.ManyToManyField(Course, verbose_name="Các khóa học trong lộ trình", related_name='roadmaps')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Lộ trình"
        verbose_name_plural = "Quản lý Lộ trình"

# 8. Bài học (QUAN TRỌNG: Đã sửa hàm get_embed_url)
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200, verbose_name="Tiêu đề bài học")
    
    # Vẫn giữ nguyên trường cũ là video_id để không phải sửa Database
    video_id = models.CharField(max_length=100, verbose_name="Youtube Video Link/ID") 
    
    duration = models.FloatField(default=0.0, verbose_name="Thời lượng (phút)")
    order = models.IntegerField(default=0, verbose_name="Thứ tự")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order}. {self.title}"

    # 👇 Hàm này đã được sửa để lấy dữ liệu từ video_id
    @property
    def get_embed_url(self):
        # Lấy nội dung từ trường video_id (dù bạn paste link hay ID vào đây cũng được)
        content = self.video_id 
        
        if not content:
            return ""
        content = content.strip()
        # Logic: 
        # 1. Thử tìm xem có phải là Link dài không (như youtube.com/watch?v=ABC)
        regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(regex, content)
        
        if match:
            # Nếu tìm thấy ID trong link -> Trả về link embed chuẩn
            return f"https://www.youtube.com/embed/{match.group(1)}"
        
        # 2. Nếu không tìm thấy dạng link, giả sử người dùng chỉ paste mỗi ID (ví dụ: dQw4w9WgXcQ)
        return f"https://www.youtube.com/embed/{content}"

    class Meta:
        ordering = ['order']
        verbose_name = "Bài học"
        verbose_name_plural = "Danh sách Bài học"

# 9. Đánh giá bài học
class LessonReview(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(verbose_name="Nội dung bình luận")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
