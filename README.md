**#  Web Học Lập Trình (Django E-Learning Platform)

> Hệ thống website học trực tuyến (E-Learning) được xây dựng bằng **Django Framework**, cho phép người dùng mua khóa học, xem lộ trình và học qua video bài giảng.

##  Giới thiệu

Dự án này là một nền tảng giáo dục trực tuyến, nơi Học viên có thể tìm kiếm các khóa học lập trình, đặt mua và vào học trực tiếp. Hệ thống tích hợp trình phát Video (Youtube Embed), quản lý đơn hàng và lộ trình học tập bài bản.

Đây là đồ án thực hành nhằm áp dụng kiến thức về **Django, Bootstrap 5 và Cơ sở dữ liệu**.

---

## Tính năng nổi bật

### 1.  Dành cho Học viên (User)
* **Hệ thống tài khoản:** Đăng ký, Đăng nhập, Quản lý hồ sơ cá nhân (Profile).
* **Khóa học (Courses):**
    * Tìm kiếm khóa học theo tên.
    * Xem chi tiết khóa học, giá tiền và nội dung.
* **Học tập (Learning):**
    * **Xem Video bài giảng:** Tích hợp trình phát video Youtube ngay trên web (Bảo mật link, không cần tải video nặng).
    * Danh sách bài học hiển thị rõ ràng bên cạnh video.
* **Lộ trình (Roadmaps):** Xem các lộ trình gợi ý (VD: Backend Python, Frontend Basic...).
* **Mua sắm & Thanh toán:**
    * Thêm khóa học vào giỏ hàng.
    * Thanh toán (COD / Chuyển khoản).
    * **Quản lý đơn hàng:** Xem trạng thái đơn, **Hủy đơn hàng** (khi trạng thái đang chờ xử lý).

### 2.  Dành cho Quản trị viên (Admin)
* **Quản lý Khóa học:** Thêm/Sửa/Xóa khóa học.
* **Quản lý Bài giảng (Inline Admin):** Thêm video bài học (Youtube ID) ngay trong giao diện sửa Khóa học.
* **Quản lý Đơn hàng:** Duyệt đơn hàng thành công hoặc Hủy đơn.
* **Quản lý Lộ trình:** Tạo lộ trình và gán khóa học vào lộ trình.
* **Thống kê:** Quản lý người dùng, giảng viên.

---

## Công nghệ sử dụng

* **Backend:** Python 3.x, Django 5.x.
* **Frontend:** HTML5, CSS3, **Bootstrap 5** (Responsive), Bootstrap Icons.
* **Font:** Google Fonts (Dancing Script cho Footer & Roboto).
* **Database:** SQLite (Mặc định).

---

## Cài đặt và Chạy dự án

Để chạy dự án này trên máy tính cá nhân, hãy làm theo các bước sau:

### Bước 1: Clone dự án
```bash
git clone [https://github.com/TEN-CUA-BAN/TEN-REPO.git](https://github.com/TEN-CUA-BAN/TEN-REPO.git)
cd TEN-REPO**
```
Bước 2: Tạo môi trường ảo (Khuyên dùng)
```Bash

python -m venv venv
# Windows:
venv\Scripts\activate
# MacOS/Linux:
source venv/bin/activate
```
Bước 3: Cài đặt thư viện
```Bash

pip install django pillow
```
Bước 4: Khởi tạo Database
```Bash

python manage.py makemigrations
python manage.py migrate
```
Bước 5: Tạo tài khoản Admin
```Bash

python manage.py createsuperuser
# Nhập username, email và password...
```
Bước 6: Chạy Server
```Bash

python manage.py runserver
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









