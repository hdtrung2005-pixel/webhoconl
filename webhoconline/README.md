#  Web Học Lập Trình (Django E-Learning Platform)

> Hệ thống website học trực tuyến (E-Learning) được xây dựng bằng **Django Framework**, cho phép người dùng mua khóa học, xem lộ trình và học qua video bài giảng.

##  Giới thiệu

Dự án này là một nền tảng giáo dục trực tuyến, nơi Học viên có thể tìm kiếm các khóa học lập trình, đặt mua và vào học trực tiếp. Hệ thống tích hợp trình phát Video (Youtube Embed), quản lý đơn hàng và lộ trình học tập bài bản.

Đây là đồ án thực hành nhằm áp dụng kiến thức về **Django, Bootstrap 5 và Cơ sở dữ liệu**.

---

##  Tính năng nổi bật

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
    * **Quản lý đơn hàng:** Xem trạng thái đơn, **Hủy đơn hàng** (khi chưa xử lý).

### 2.  Dành cho Quản trị viên (Admin)
* **Quản lý Khóa học:** Thêm/Sửa/Xóa khóa học.
* **Quản lý Bài giảng (Inline Admin):** Thêm video bài học (Youtube ID) ngay trong giao diện sửa Khóa học.
* **Quản lý Đơn hàng:** Duyệt đơn hàng thành công hoặc Hủy đơn.
* **Quản lý Lộ trình:** Tạo lộ trình và gán khóa học vào lộ trình.
* **Thống kê:** Quản lý người dùng, giảng viên.

---

##  Công nghệ sử dụng

* **Backend:** Python 3.x, Django 5.x.
* **Frontend:** HTML5, CSS3, **Bootstrap 5** (Responsive), Bootstrap Icons.
* **Font:** Google Fonts (Dancing Script cho Footer & Roboto).
* **Database:** SQLite (Mặc định).

---

## Cài đặt và Chạy dự án

Để chạy dự án này trên máy tính cá nhân, hãy làm theo các bước sau:

### Bước 1: Clone dự án
```bash
git clone [https://github.com/Hoangnolove/Book-store.git](https://github.com/Hoangnolove/Book-store.git)
cd Book-store