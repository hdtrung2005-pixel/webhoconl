🎓 Web Học Lập Trình (Django E-Learning Platform)
 
>> Hệ thống E-Learning hiện đại được xây dựng bằng Django 5, tích hợp trí tuệ nhân tạo (AI) trợ giảng và hệ thống thanh toán thông minh.

📝 Giới thiệu dự án
>>Dự án là nền tảng giáo dục trực tuyến toàn diện, giúp học viên tiếp cận tri thức lập trình thông qua lộ trình bài bản. Hệ thống không chỉ dừng lại ở việc xem video mà còn tương tác trực tiếp với AI Tutor để giải đáp thắc mắc ngay trong bài học.

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
<img width="716" height="898" alt="image" src="https://github.com/user-attachments/assets/f24933cb-fcab-4283-a740-981efdfa8911" />

2. Đăng nhập 
<img width="1721" height="868" alt="image" src="https://github.com/user-attachments/assets/bd156f6d-3c43-49bd-b5b5-2a886df18ac3" />

3.Trang chủ
<img width="1903" height="915" alt="image" src="https://github.com/user-attachments/assets/54f39f62-cfc9-4465-808c-46a881d3dab9" />

4.Môn học
<img width="1905" height="915" alt="image" src="https://github.com/user-attachments/assets/db0f1e0c-8a1c-47b8-993c-5ddc2fbca89f" />

5.Danh mục, tất cả khóa học
<img width="1902" height="920" alt="image" src="https://github.com/user-attachments/assets/7ff39f05-585d-40ba-8e91-4ee6f526a094" />

6.lộ trình
 <img width="1894" height="909" alt="image" src="https://github.com/user-attachments/assets/f74f8ae5-73ce-4da7-bbb3-74a49f476c62" />

7.tìm kiếm
<img width="1919" height="911" alt="image" src="https://github.com/user-attachments/assets/a652c751-7245-43e7-bdc8-a073ae280830" />

8.giỏ hàng
<img width="1899" height="901" alt="image" src="https://github.com/user-attachments/assets/e424970d-d648-40b6-96c3-544dfcb4fda4" />

9.hồ sơ cá nhân
<img width="1919" height="916" alt="image" src="https://github.com/user-attachments/assets/39c67a46-552e-4d9f-866d-964da6f75101" />

10.lịch sử mua hàng
<img width="1919" height="911" alt="image" src="https://github.com/user-attachments/assets/4b905ae4-254f-4f1e-a1e3-00ceadd8887f" />

11.chi tiết lộ trình
<img width="1900" height="908" alt="image" src="https://github.com/user-attachments/assets/d3eb9b7c-49a7-4d33-84cd-dfff73a9234c" />









