## Tổng quan về kiến trúc Hexagonal
Kiến trúc Hexagonal trong dự án này được chia thành 4 lớp chính:

1. Lớp Domain (Miền):

* Chứa các thực thể nghiệp vụ cốt lõi (models) và logic nghiệp vụ
* Định nghĩa các giao diện (ports) cho repositories và services
* Độc lập với công nghệ và framework bên ngoài


2. Lớp Application (Ứng dụng):

* Triển khai các tình huống sử dụng bằng cách điều phối các đối tượng miền
* Sử dụng giao diện miền (ports) để truy cập repositories
* Chuyển đổi giữa domain models và DTOs


3. Lớp Infrastructure (Hạ tầng):

* Triển khai các giao diện repository đã định nghĩa trong lớp domain
* Xử lý kết nối cơ sở dữ liệu và ORM models
* Chứa cấu hình hệ thống


4. Lớp Interface (Giao diện):

* Chứa các endpoint API (REST controllers)
* Xử lý HTTP requests và responses
* Ánh xạ giữa API schemas và application DTOs



## Các tính năng chính

* Xác thực JWT: Hệ thống đăng nhập và xác thực người dùng
* REST API đầy đủ: CRUD cho sản phẩm và người dùng
* Xử lý lỗi: Hệ thống xử lý lỗi toàn diện
* Kết nối MySQL không đồng bộ: Sử dụng aiomysql và SQLAlchemy
* API Documentation: Tự động tạo bằng Swagger UI của FastAPI

## Để chạy dự án

1. Cài đặt MySQL và tạo cơ sở dữ liệu hexagonal_demo
2. Cập nhật file .env với thông tin kết nối MySQL của bạn
3. Cài đặt các phụ thuộc: pip install -r requirements.txt
4. Chạy ứng dụng: python main.py
5. Truy cập API Documentation: http://localhost:8000/docs

Dự án này được thiết kế để dễ dàng mở rộng thêm tính năng mới hoặc thay đổi công nghệ cơ sở dữ liệu mà không ảnh hưởng đến logic nghiệp vụ cốt lõi.