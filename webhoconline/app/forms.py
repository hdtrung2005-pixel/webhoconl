from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LessonReview 

# 1. Form Đăng ký tài khoản 
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

# 2. Form Chỉnh sửa hồ sơ
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Họ đệm',
            'last_name': 'Tên',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# 3. Form Đánh giá bài học 
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