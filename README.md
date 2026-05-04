🎓 Web Học Lập Trình (Django E-Learning Platform)
 
>> Hệ thống E-Learning hiện đại được xây dựng bằng Django 5, tích hợp trí tuệ nhân tạo (AI) trợ giảng và hệ thống thanh toán thông minh.

📝 Giới thiệu dự án
>>Dự án là nền tảng giáo dục trực tuyến toàn diện, giúp học viên tiếp cận tri thức lập trình thông qua lộ trình bài bản. Hệ thống không chỉ dừng lại ở việc xem video mà còn tương tác trực tiếp với AI Tutor để giải đáp thắc mắc ngay trong bài học.
##  Mục lục

* [Tính năng nổi bật](#tính-năng-nổi-bật)
* [Yêu cầu & Cài đặt](#yêu-cầu--cài-đặt)
* [Cách sử dụng](#cách-sử-dụng)
* [Công nghệ sử dụng](#công-nghệ-sử-dụng)
---

## Tính năng nổi bật


### 1. Dành cho Học viên (Student)
* **Trợ giảng AI (Gemini AI):** Giải đáp thắc mắc bài học và tư vấn lộ trình học tập ngay trên website.
* **Hệ thống lộ trình (Roadmap):** Đăng ký mua khóa học theo các combo lộ trình định sẵn để nhận ưu đãi.
* **Thanh toán VietQR:** Tự động tạo mã QR thanh toán kèm nội dung chuyển khoản chính xác cho từng đơn hàng.
* **Học tập trực quan:** Xem video bài giảng (YouTube Embed), theo dõi danh sách bài học và đánh giá khóa học.
* **Bảo mật hồ sơ:** Chặn ký tự số và đặc biệt trong tên người dùng, giao diện cập nhật hồ sơ thân thiện.

### 2. Dành cho Giảng viên (Teacher)
* **Đặc quyền truy cập:** Xem và kiểm tra toàn bộ nội dung khóa học, video bài giảng mà không cần qua bước thanh toán.
* **Phân quyền bảo mật:** Hệ thống bảo vệ các trang nghiệp vụ riêng biệt bằng Decorator `@teacher_required`, ngăn chặn học viên truy cập trái phép.

### 3. Dành cho Quản trị viên (Admin)
* **Quản trị hiện đại:** Sử dụng giao diện **Jazzmin** chuyên nghiệp, trực quan.
* **Thống kê thông minh:** Biểu đồ doanh thu và báo cáo số lượng học viên theo từng khóa học.
* **Quản lý nội dung:** CRUD (Thêm/Sửa/Xóa) Khóa học, bài giảng (Inline Admin), lộ trình và duyệt/hủy đơn hàng.
🛠 Công nghệ sử dụng
Framework: Django 5.2.10.
### 4. Trí tuệ nhân tạo (AI Integration) 🤖
AI Tutor: Giải đáp thắc mắc về nội dung bài giảng ngay tại trang xem video sử dụng Gemini 2.5 Flash.

AI Consultant: Tư vấn lộ trình và khóa học phù hợp dựa trên nhu cầu học viên.

---

## Yêu cầu & Cài đặt

### Yêu cầu hệ thống
* **Python** >= 3.11.9
* **Django** >= 5.2.10
* **SQL Server** (MSSQL)
* **Môi trường:** VS Code (khuyến nghị)

---

Hướng dẫn cài đặt & Chạy dự án
1. **Clone repository**
   ```bash
   git clone [https://github.com/trung123/webhoconline.git](https://github.com/trung123/webhoconline.git)
   cd webhoconline
2. **Tạo và kích hoạt môi trường ảo**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
3. **Cài đặt thư viện cần thiết**
    ```bash
pip install django pillow python-dotenv google-generativeai django-jazzmin mssql-django

4. **Cấu hình biến môi trường (.env)**
   ```bash
   GEMINI_API_KEY=your_api_key_here
   SECRET_KEY=your_django_secret_key
   BANK_CODE=MB
   BANK_ACCOUNT_NUMBER=0916536176
   BANK_ACCOUNT_NAME=HA DUC TRUNG

5. **Cấu hình Cơ sở dữ liệu (SQL Server)**
   ```bash
   Đảm bảo SQL Server đang chạy và database WebHocTap_Moi đã được tạo trên host
6. **Chạy Migrate và thu thập Static**
   ```bash
   python manage.py collectstatic
   python manage.py migrate
---

## Cách sử dụng
**Chạy server Django tại cổng 8888 (theo cấu hình dự án):**
  
    python manage.py runserver 8888
**Truy cập website tại:**
 
    http://127.0.0.1:8888/
    
**Trang quản trị Admin:** 

    http://127.0.0.1:8888/admin/
---
## Công nghệ sử dụng
Backend Framework: Django 5.2.10

Ngôn ngữ: Python 3.11.9

Cơ sở dữ liệu: Microsoft SQL Server (MSSQL)

Frontend: Bootstrap 5, HTML5, CSS3, JavaScript

AI Integration: Google Gemini AI API

Giao diện quản trị: Jazzmin
---
Dự án phục vụ mục đích học tập và thực hành môn Phát triển ứng dụng Python.
