# Cách để xử lý Backend API của Odoo

Mặc định, backend API của Odoo **không hỗ trợ** cơ chế bất đồng bộ `async/await` gốc của Python (như cách mà FastAPI, Sanic hay Node.js đang làm). Odoo là một framework hoàn toàn **đồng bộ (Synchronous)**.

### 1. Tại sao Odoo không có `async/await`?
* **Kiến trúc WSGI thay vì ASGI:** Odoo được xây dựng từ hơn chục năm trước dựa trên thư viện Werkzeug và chuẩn giao tiếp WSGI. WSGI bản chất là thiết kế đồng bộ (chặn luồng - blocking). Khi một request HTTP gửi tới API, tiến trình xử lý đó sẽ bị khóa (block) lại chờ database (ORM) chạy xong mới nhả kết quả ra.
* **ORM không Thread-safe / Async-safe:** Bộ ORM khổng lồ của Odoo quản lý các Transaction và Database Cursor (psycopg2) một cách chặt chẽ theo từng luồng (thread/process). Việc nhét `async def` vào một Controller của Odoo sẽ làm hỏng ngữ cảnh (context) của cơ sở dữ liệu và gây văng lỗi ngay lập tức.

### 2. Vậy Odoo xử lý hàng ngàn request cùng lúc bằng cách nào?
Vì không có `async/await` để tận dụng I/O không chặn (Non-blocking I/O), Odoo xử lý tải nặng bằng cơ chế **Đa tiến trình (Multi-processing)**:
* Khi chạy ở môi trường thực tế (Production), bạn không chạy Odoo bằng 1 luồng đơn, mà phải cấu hình tham số `--workers` (ví dụ: `--workers=9`).
* Lúc này, Odoo sẽ dùng cơ chế *Pre-fork* tạo ra 9 tiến trình (process) độc lập trên hệ điều hành. Mỗi tiến trình sẽ hứng và xử lý các request song song với nhau. Tiến trình nào bận thì hệ thống đẩy request sang tiến trình đang rảnh.

*(Lưu ý: Odoo có dùng một thư viện tên là `gevent` tạo ra các luồng ảo (greenlets) để làm chức năng Realtime như Chat/Long-polling, nhưng nó hoàn toàn tách biệt và bạn không thể dùng nó để viết API `async` thông thường).*

### 3. Cách "Lách luật" để làm API bất đồng bộ trong Odoo
Trong thực tế, nếu bạn gọi một API từ app mobile lên Odoo để xuất báo cáo hoặc gửi 100 cái email, bạn không thể để app mobile "treo" chờ Odoo chạy xong được. Lập trình viên Odoo thường dùng 2 cách sau:

**Cách 1: Sử dụng Background Jobs (Khuyên dùng)**
Sử dụng một module cực kỳ nổi tiếng của cộng đồng OCA là **`queue_job`**.
* **Luồng chạy:** API nhận request -> Ném task xử lý nặng vào một hàng đợi (Queue) -> Trả về ngay lập tức mã `200 OK` (hoặc ID của Job) cho app mobile -> Một worker ngầm (Background Worker) của Odoo sẽ từ từ lôi task đó ra chạy ở phía sau.

**Cách 2: Đẩy vào Cron Job (Scheduled Actions)**
Thay vì xử lý ngay, API chỉ ghi nhận một "Cờ lệnh" (Status = 'pending') xuống database rồi trả kết quả về luôn. Odoo sẽ có một Cron Job chạy định kỳ (ví dụ 1 phút 1 lần) quét các cờ lệnh đó để xử lý từ từ.

Odoo sinh ra để làm ERP (chú trọng tính toàn vẹn dữ liệu và logic phức tạp) chứ không sinh ra để làm các API Microservices siêu tốc. 
