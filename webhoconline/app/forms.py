from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LessonReview 
from django.core.exceptions import ValidationError
import re

# Biểu thức Regex: Chỉ cho phép chữ cái (kể cả tiếng Việt có dấu) và khoảng trắng
NAME_REGEX = r'^[a-zA-ZÀ-ỹ\s]+$'

# ===========================================================
# 1. Form Đăng ký tài khoản 
# ===========================================================
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'full_name')
        labels = {
            'role': 'Bạn đăng ký với tư cách là:',
            'full_name': 'Họ và tên',
            'email': 'Địa chỉ Email'
        }
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # Bắt lỗi nhập sai tên ngay từ lúc Đăng ký
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '')
        if full_name and not re.match(NAME_REGEX, full_name):
            raise ValidationError("Họ và tên chỉ được chứa chữ cái, không được chứa số hoặc kí tự đặc biệt!")
        
        # Tiện tay dọn dẹp: Xóa khoảng trắng thừa và Viết Hoa Chữ Cái Đầu
        return ' '.join(full_name.split()).title()


# ===========================================================
# 2. Form Chỉnh sửa hồ sơ 
# ===========================================================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'avatar'] # Dùng đúng trường full_name
        labels = {
            'full_name': 'Họ và tên',
            'email': 'Email',
            'avatar': 'Ảnh đại diện',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    # Bắt lỗi nhập sai tên lúc Cập nhật hồ sơ
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '')
        if full_name and not re.match(NAME_REGEX, full_name):
            raise ValidationError("Họ và tên chỉ được chứa chữ cái, không được chứa số hoặc kí tự đặc biệt!")
            
        return ' '.join(full_name.split()).title()


# ===========================================================
# 3. Form Đánh giá bài học 
# ===========================================================
class ReviewForm(forms.ModelForm):
    class Meta:
        model = LessonReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Bài học này thế nào? Hãy chia sẻ cảm nghĩ của bạn...'
            }),
        }
        labels = {
            'rating': 'Đánh giá (Sao)',
            'comment': 'Bình luận'
        }