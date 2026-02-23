from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from .models import Course, Category, Order, OrderItem, User, Lesson, Roadmap

# ===========================================================
# 1. CẤU HÌNH USER (GIỮ NGUYÊN NHƯ CŨ - AN TOÀN)
# ===========================================================
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('full_name', 'email', 'role')}),
        ('Trạng thái', {'fields': ('is_active', 'is_staff')}), 
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.role == 'teacher':
            obj.is_staff = True
            obj.save()
            # Cấp quyền cho Giảng viên (Chỉ Course, Lesson, Category, Roadmap)
            allowed_models = ['course', 'lesson', 'category', 'roadmap']
            permissions = Permission.objects.filter(
                content_type__app_label='app',
                content_type__model__in=allowed_models
            )
            obj.user_permissions.set(permissions)
        elif obj.role == 'student':
            obj.is_staff = False
            obj.save()
            obj.user_permissions.clear()

# ===========================================================
# 2. CẤU HÌNH ĐƠN HÀNG (TÍNH NĂNG MỚI: DUYỆT ĐƠN)
# ===========================================================

# Giúp xem chi tiết món hàng (OrderItem) ngay trong đơn hàng lớn
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('course', 'price', 'quantity') # Chỉ xem, không cho sửa giá lung tung
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at') # Bộ lọc bên phải
    search_fields = ('user__username',)    # Tìm theo tên người mua
    inlines = [OrderItemInline]            # Nhúng bảng chi tiết vào
    actions = ['approve_orders']           # Thêm nút hành động

    # --- HÀM XỬ LÝ DUYỆT ĐƠN (TIÊU CHÍ 4 & 5) ---
    def approve_orders(self, request, queryset):
        # Cập nhật tất cả đơn hàng được chọn thành 'Completed'
        count = queryset.update(status='Completed')
        self.message_user(request, f"✅ Đã duyệt thành công {count} đơn hàng!")
    
    approve_orders.short_description = "Duyệt đơn hàng (Đã nhận tiền)"

# ===========================================================
# 3. CẤU HÌNH KHÓA HỌC (GIỮ NGUYÊN)
# ===========================================================
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at')
    inlines = [LessonInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs
        return qs.filter(instructor=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk: obj.instructor = request.user
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser and 'instructor' in fields:
            fields.remove('instructor')
        return fields

# ===========================================================
# 4. ĐĂNG KÝ MODEL
# ===========================================================
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Order, OrderAdmin) # <-- Đăng ký OrderAdmin mới
admin.site.register(Category)
admin.site.register(Roadmap)
# Không cần register OrderItem lẻ tẻ nữa vì đã nhúng vào Order rồi