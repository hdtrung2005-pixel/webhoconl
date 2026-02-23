from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LessonReview 
from django.core.exceptions import ValidationError

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
        fields = ['first_name', 'last_name', 'email', 'avatar']
        labels = {
            'first_name': 'Họ đệm',
            'last_name': 'Tên',
            'email': 'Email',
            'avatar': 'Ảnh đại diện',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        # Kiểm tra xem trong chuỗi có chữ số nào không
        if any(char.isdigit() for char in first_name):
            raise ValidationError("Họ đệm không được chứa chữ số!")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        # Kiểm tra xem trong chuỗi có chữ số nào không
        if any(char.isdigit() for char in last_name):
            raise ValidationError("Tên không được chứa chữ số!")
        return last_name
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