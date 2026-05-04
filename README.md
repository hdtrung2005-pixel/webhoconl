**#  Web Học Lập Trình (Django E-Learning Platform)

> Hệ thống website học trực tuyến (E-Learning) được xây dựng bằng **Django Framework**, cho phép người dùng mua khóa học, xem lộ trình và học qua video bài giảng.

📝 Giới thiệu dự án
Dự án là nền tảng giáo dục trực tuyến toàn diện, giúp học viên tiếp cận tri thức lập trình thông qua lộ trình bài bản. Hệ thống không chỉ dừng lại ở việc xem video mà còn tương tác trực tiếp với AI Tutor để giải đáp thắc mắc ngay trong bài học.

---

✨ Tính năng nổi bật
1. Trí tuệ nhân tạo (AI Integration) 🤖
AI Tutor: Giải đáp thắc mắc về nội dung bài giảng ngay tại trang xem video sử dụng Gemini 2.5 Flash.

AI Consultant: Tư vấn lộ trình và khóa học phù hợp dựa trên nhu cầu học viên.

2. Nghiệp vụ học tập & Thanh toán
Học tập: Trình phát Video Youtube Embed tối ưu, danh sách bài học trực quan, hệ thống đánh giá (Review).

Lộ trình (Roadmap): Đăng ký mua khóa học theo gói combo lộ trình để nhận ưu đãi giảm giá.

Thanh toán thông minh: Tích hợp VietQR tự động tạo mã QR kèm nội dung chuyển khoản chính xác.

Quản lý đơn hàng: Cho phép người dùng theo dõi lịch sử mua hàng và hủy đơn khi đang ở trạng thái chờ duyệt.

3. Bảo mật & Quản trị
Validation: Chặn số và ký tự đặc biệt trong tên người dùng tại trang Hồ sơ cá nhân.

Giao diện Jazzmin: Hệ thống quản trị Admin được tùy chỉnh chuyên nghiệp, hiện đại với đầy đủ các Dashboard thống kê.

🛠 Công nghệ sử dụng
Framework: Django 5.2.10.

Cơ sở dữ liệu: Microsoft SQL Server (MSSQL).

Frontend: HTML5, CSS3, Bootstrap 5, JavaScript.

Thư viện hỗ trợ: django-jazzmin, pillow, python-dotenv, google-generativeai.

🚀 Hướng dẫn cài đặt & Chạy dự án
Bước 1: Chuẩn bị môi trường

```Bash
# Tạo và kích hoạt môi trường ảo
python -m venv venv
venv\Scripts\activate  # Windows
```
Bước 2: Cài đặt thư viện

```Bash
pip install -r requirements.txt
```
Bước 3: Cấu hình biến môi trường (.env)
Tạo file .env tại thư mục gốc và khai báo (Dựa theo cấu hình trong settings.py):
```
GEMINI_API_KEY: API Key trợ giảng.

SECRET_KEY: Khóa bí mật của dự án.

EMAIL_HOST_USER / PASSWORD: Cấu hình gửi mã OTP.

BANK_CODE, BANK_ACCOUNT_NUMBER: Thông tin nhận thanh toán VietQR.
```
Bước 4: Cấu hình Cơ sở dữ liệu
Đảm bảo SQL Server đang chạy và thông tin kết nối trong settings.py đã chính xác:
```
Engine: mssql

Host: DESKTOP-CU99I1G\SQLEXPRESS

Database: WebHocTap_Moi
```
Bước 5: Khởi tạo và chạy Server

```Bash
python manage.py collectstatic  # Gom file tĩnh vào thư mục staticfiles
python manage.py migrate
python manage.py runserver 8888  # Chạy tại cổng 8888
```
##Hình ảnh Demo
1.Đăng ký
<img width="1919" height="958" alt="image" src="https://github.com/user-attachments/assets/748f7b06-ba76-444d-8397-d0b59ebf2ff4" />
2. Đăng nhập 
<img width="1919" height="963" alt="image" src="https://github.com/user-attachments/assets/e2fd6435-c9a9-412f-ba5e-67e241289ece" />
3.Trang chủ
<img width="1899" height="917" alt="image" src="https://github.com/user-attachments/assets/ff4dba1a-cc6d-44da-8b83-89b6b2df317c" />
Môn học
<img width="1919" height="911" alt="image" src="https://github.com/user-attachments/assets/79d9ab55-8720-42f0-a15c-53d0aa21996d" />
Danh mục, tất cả khóa học
<img width="1919" height="900" alt="image" src="https://github.com/user-attachments/assets/635e3747-7dde-44aa-9a42-a44b869cb194" />
lộ trình
<img width="1909" height="880" alt="image" src="https://github.com/user-attachments/assets/9b363092-a024-4bbe-8ef0-02a99d855f5a" />
tìm kiếm
<img width="1919" height="902" alt="image" src="https://github.com/user-attachments/assets/7b4e8f18-32b3-45c7-ac15-8d5d09926bcb" />
giỏ hàng
<img width="1917" height="921" alt="image" src="https://github.com/user-attachments/assets/5122605f-dd85-4027-942a-d1986d9e1233" />
hồ sơ cá nhân
<img width="1918" height="908" alt="image" src="https://github.com/user-attachments/assets/1a401f1c-3273-40e1-ad25-7072732345a7" />
lịch sử mua hàng
<img width="1919" height="889" alt="image" src="https://github.com/user-attachments/assets/2d686820-36de-492f-8a11-20ab6ede2e78" />
đăng xuất, xem hồ sơ
<img width="678" height="899" alt="image" src="https://github.com/user-attachments/assets/70d5e6d4-49c7-4709-b7d6-69d66a172dca" />









