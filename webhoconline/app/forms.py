from django import forms
from django.contrib.auth.models import User
from .models import LessonReview  


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] # Cho phép sửa Họ, Tên, Email
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

# --- chức năng Đánh giá ---
class ReviewForm(forms.ModelForm):
    class Meta:
        model = LessonReview
        fields = ['rating', 'comment']
        
        # Cấu hình giao diện cho form
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Bài học này thế nào? Hãy chia sẻ cảm nghĩ của bạn...'
            }),
        }
        
        # Nhãn hiển thị
        labels = {
            'rating': 'Đánh giá (Sao)',
            'comment': 'Bình luận'
        }