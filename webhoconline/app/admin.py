from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission, Group # Đã gọi lại Permission của bạn
from .models import Course, Category, Order, OrderItem, User, Lesson, Roadmap

# ===========================================================
# 1. CẤU HÌNH USER (TỰ ĐỘNG PHÂN QUYỀN - CODE GỐC CỦA BẠN)
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
        
        # LOGIC TỰ ĐỘNG CẤP QUYỀN XỊN XÒ CỦA BẠN:
        if obj.role == 'teacher':
            obj.is_staff = True
            obj.save()
            # Cấp quyền cho Giảng viên (Chỉ Course, Lesson, Category, Roadmap)
            allowed_models = ['course', 'lesson', 'category', 'roadmap']
            permissions = Permission.objects.filter(
                content_type__app_label='app', # Thay 'app' bằng tên app của bạn nếu khác
                content_type__model__in=allowed_models
            )
            obj.user_permissions.set(permissions)
            
        elif obj.role == 'student':
            obj.is_staff = False
            obj.save()
            obj.user_permissions.clear()

# ===========================================================
# 2. CẤU HÌNH ĐƠN HÀNG
# ===========================================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('course', 'price', 'quantity')
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)    
    inlines = [OrderItemInline]            
    actions = ['approve_orders']           
    list_editable = ['status']

    def approve_orders(self, request, queryset):
        count = queryset.update(status='Completed')
        self.message_user(request, f"✅ Đã duyệt thành công {count} đơn hàng!")
    
    approve_orders.short_description = "Duyệt đơn hàng (Đã nhận tiền)"

# ===========================================================
# 3. CẤU HÌNH KHÓA HỌC
# ===========================================================
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Cột hiển thị ở ngoài danh sách
    list_display = ('title', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)
    
    # CHIÊU CHIA KHỐI GIAO DIỆN FORM BÊN TRONG
    fieldsets = (
        ('📝 Thông tin chung', {
            'fields': ('title', 'category', 'instructor', 'description'), 
            'classes': ('wide',)
        }),
        ('💰 Chi phí & Hình ảnh', {
            'fields': ('price', 'image'),
            'classes': ('collapse',) # Có thể thu gọn/mở rộng khối này
        }),
    )
    inlines = [LessonInline]
# ===========================================================
# 4. ĐĂNG KÝ MODEL
# ===========================================================
admin.site.register(User, CustomUserAdmin)
#admin.site.register(Course, CourseAdmin)
admin.site.register(Order, OrderAdmin) 
admin.site.register(Category)
admin.site.register(Roadmap)

# CHỈ CẦN DÒNG NÀY ĐỂ XÓA GIAO DIỆN "CÁC NHÓM" THỪA THÃI BÊN NGOÀI
admin.site.unregister(Group)