from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Course, Category, Order, OrderItem, Instructor, User
from .models import Roadmap
from .models import Lesson

# Tạo class quản lý User riêng (Custom)
class MyUserAdmin(BaseUserAdmin):
    # Chỉnh sửa giao diện trang chi tiết User (Bỏ phần Groups/Permissions bị lỗi đi)
    fieldsets = (
        (None, {'fields': ('username', 'password')}), # Phần tài khoản
        ('Thông tin cá nhân', {'fields': ('full_name', 'email', 'role')}), # Thêm role và full_name vào đây
        ('Quyền hạn', {'fields': ('is_active', 'is_staff', 'is_superuser')}), # Quyền truy cập Admin
        # LƯU Ý: Tuyệt đối không thêm 'groups' và 'user_permissions' vào đây
    )

    # 2. Các cột hiển thị ở danh sách danh sách User bên ngoài
    list_display = ('username', 'email', 'full_name', 'role', 'is_staff')
    
    # 3. Cho phép tìm kiếm theo tên, email
    search_fields = ('username', 'full_name', 'email')
    
    # 4. Bộ lọc bên phải (Bỏ groups đi)
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    
    # 5. Tắt tính năng chọn nhiều (vì không có bảng phụ)
    filter_horizontal = () 
    # CẤU HÌNH QUẢN LÝ INSTRUCTOR (Giảng viên)
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
     list_display = ('get_username', 'phone', 'is_approved')
     list_filter = ('is_approved',)
     actions = ['approve_instructors', 'revoke_instructors']

     def get_username(self, obj):
        return obj.user.username
     get_username.short_description = 'Tài khoản'

     def approve_instructors(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "✅ Đã duyệt các giảng viên được chọn!")
     approve_instructors.short_description = "Duyệt giảng viên"

     def revoke_instructors(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "❌ Đã hủy quyền giảng viên!")
     revoke_instructors.short_description = "Hủy quyền giảng viên"
@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    filter_horizontal = ('courses',)
#Tạo giao diện nhập Bài học nằm ngang (TabularInline)
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1 # Mặc định hiện sẵn 1 dòng trống để nhập
# Cập nhật lại CourseAdmin cũ (hoặc tạo mới nếu chưa custom)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'created_at')
    inlines = [LessonInline] # <-- Nhúng bảng nhập bài học vào đâ
# Đăng ký các bảng

admin.site.register(Category)
admin.site.register(User, MyUserAdmin) #
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Course, CourseAdmin)