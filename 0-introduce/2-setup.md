# Hướng dẫn Cài đặt và Thiết lập (Setup Guide)

Tài liệu này tóm tắt các bước thiết lập môi trường phát triển Odoo v18 từ mã nguồn, các tham số dòng lệnh và công cụ hỗ trợ debug.

## 1. Cài đặt từ mã nguồn

### 1.1. Hình thức cài đặt
Đối với các lập trình viên, phương pháp ưu tiên là **Cài đặt từ mã nguồn (Source Install)**. Điều này cho phép bạn can thiệp trực tiếp vào code và quản lý các tùy chỉnh dễ dàng hơn.
*   **Repositories:** Thông thường bạn sẽ làm việc với 3 kho lưu trữ chính:
    *   `odoo/odoo`: Mã nguồn lõi (Community).
    *   `odoo/enterprise`: Các phân hệ bản quyền (Enterprise).
    *   `odoo/tutorials`: Thư mục chứa các module học tập hoặc tùy chỉnh riêng.

### 1.2. Khởi chạy Server Odoo
Sau khi cài đặt đủ các dependency (thư viện Python), bạn khởi động server bằng file `odoo-bin`.

**Lệnh khởi chạy mẫu:**
```bash
cd $HOME/src/odoo/
./odoo-bin --addons-path="addons/,../enterprise/,../tutorials" -d rd-demo
```

**Các tham số dòng lệnh (CLI Arguments) quan trọng:**
*   `-d <database>`: Chỉ định cơ sở dữ liệu sẽ sử dụng.
*   `--addons-path <directories>`: Danh sách các thư mục chứa module (cách nhau bởi dấu phẩy). Các thư mục này sẽ được quét để nạp module.
*   `-i <modules>`: Cài đặt mới các module (danh sách cách nhau bằng dấu phẩy).
*   `-u <modules>`: Cập nhật (Upgrade) các module đã cài đặt.
*   `--limit-time-cpu` & `--limit-time-real`: Giới hạn thời gian thực thi. Nên tăng giá trị này khi đang debug để tránh server tự ngắt kết nối.

### 1.3. Truy cập và Quản trị
*   **Địa chỉ mặc định:** `http://localhost:8069/`
*   **Thông tin đăng nhập mặc định:**
    *   Email/User: `admin`
    *   Password: `admin`
*   **Developer Mode:** Luôn kích hoạt chế độ nhà phát triển (Debug mode) để sử dụng các công cụ nâng cao trong giao diện Odoo.

### 1.4. Công cụ hỗ trợ và Quy chuẩn Code
*   **Git:** Luôn đảm bảo nhánh (branch) ở các repository Core và Enterprise đồng bộ với nhau (ví dụ: cùng ở nhánh `18.0`).
*   **Trình soạn thảo (Editor):** Khuyên dùng VSCode, PyCharm hoặc Sublime Text.
*   **Quy chuẩn Linter (Linting):**
    *   **Python:** Tuân thủ PEP8 (thường bỏ qua các lỗi E501, E301, E302).
    *   **JavaScript:** Sử dụng ESLint.
*   **PostgreSQL:** Có thể quản lý DB qua dòng lệnh hoặc GUI (pgAdmin, DBeaver). Nên kết nối qua Unix socket `/var/run/postgresql`.

### 1.5. Debug Python với `ipdb`
Sử dụng `ipdb` để kiểm tra logic code khi gặp lỗi hoặc muốn hiểu luồng dữ liệu.

*   **Cài đặt:** `pip install ipdb`
*   **Đặt điểm dừng (Breakpoint):** Thêm dòng sau vào vị trí code muốn dừng:
    ```python
    import ipdb; ipdb.set_trace()
    ```
*   **Các lệnh điều khiển khi debug:**
    *   `n (next)`: Chạy dòng tiếp theo trong hàm hiện tại.
    *   `s (step)`: Đi sâu vào bên trong hàm được gọi.
    *   `c (continue)`: Tiếp tục chạy cho đến khi gặp điểm dừng tiếp theo.
    *   `pp <expression>`: In giá trị biến một cách rõ ràng (pretty-print).
    *   `w (where)`: Hiển thị stack trace để biết code đang chạy ở đâu.
    *   `q (quit)`: Thoát khỏi chế độ debug và dừng chương trình.

## 2. Thiết lập với Docker (Docker Setup)
Sử dụng Docker là phương pháp khuyên dùng để đồng bộ hóa môi trường phát triển giữa các thành viên trong đội ngũ và đơn giản hóa việc quản lý các thư viện phụ thuộc.

#### 2.1. Các thành phần chính
Hệ thống Docker của dự án HRM được cấu trúc bởi 3 thành phần cốt lõi:
- **Dockerfile**: Xây dựng image tùy chỉnh dựa trên Odoo 18.0, tự động cài đặt các thư viện Python bổ trợ như `xlsxwriter` (xuất Excel) và `pandas` (xử lý dữ liệu).
- **docker-compose.yml**: Điều phối dịch vụ `web` (Odoo server) và `db` (Postgres 17).
- **Cơ chế Secret**: Sử dụng `Docker Secrets` để đọc mật khẩu từ tệp `.secrets/postgresql_password`, giúp bảo mật thông tin nhạy cảm.

#### 2.2. Các bước triển khai nhanh (Sử dụng Makefile)
Dự án cung cấp sẵn `Makefile` để tối ưu hóa các lệnh Docker phức tạp:
- `make init`: Khởi tạo môi trường, tạo tệp mật khẩu, build image và khởi tạo DB (chỉ chạy lần đầu).
- `make run`: Khởi chạy các container ở chế độ nền.
- `make dev`: Chạy Odoo với chế độ **Hot-reload** (tự động nhận thay đổi code Python/XML).
- `make logs`: Theo dõi log thời gian thực của hệ thống.

#### 2.3. Triển khai thủ công (Manual Commands)
Nếu không sử dụng Makefile, bạn có thể thực hiện theo quy trình sau:
1.  **Thiết lập môi trường**:
    - Tạo tệp biến môi trường: `cp .env.example .env`
    - Tạo mật khẩu PostgreSQL: `mkdir -p .secrets && echo "your_password" > .secrets/postgresql_password`
2.  **Khởi chạy dịch vụ**:
    ```bash
    docker compose up -d --build
    ```
3.  **Khởi tạo Database (Lần đầu)**:
    ```bash
    docker compose run --rm web odoo -d odoo -i base,proid --without-demo=all --stop-after-init
    ```

#### 2.4. Quản lý mã nguồn và Dữ liệu
- **Ánh xạ Addons (Volumes)**: 
    - `./custom_addons` ánh xạ vào `/mnt/custom-addons`: Nơi chứa code HRM tự phát triển.
    - `./community_addons` ánh xạ vào `/mnt/community-addons`: Nơi chứa module từ cộng đồng.
- **Hot-reload**: Khi chạy với tham số `--dev=all`, Odoo sẽ tự động phát hiện các thay đổi trong file `.py` và khởi động lại server bên trong container, giúp tăng tốc độ phát triển.
## 3. So sánh: Clone Git vs Docker

Để chọn đúng phương pháp cho từng mục đích, hãy xem bảng so sánh nhanh dưới đây:

| Tiêu chí | Docker (Khuyên dùng 📦) | Clone Git (Chuyên sâu 🛠️) |
| :--- | :--- | :--- |
| **Thời gian Setup** | Cực nhanh (~5 phút) | Phức tạp, dễ lỗi môi trường |
| **Tính Nhất quán** | Tuyệt đối (Container hóa) | Phụ thuộc thư viện máy host |
| **Khả năng Debug** | Debug Addons dễ, Core khó | Debug mọi nơi, đọc code Core dễ |
| **Deployment** | Rất dễ, đồng bộ CI/CD | Phức tạp, khó bảo trì |
| **Sạch máy host** | Không cài thêm gì bản | Cài nhiều Python lib, DB... |

---

### Khi nào nên chọn gì?

*   **Dùng DOCKER khi:**
    *   Phát triển các module chức năng (ví dụ: `hrm_core`, `prodid`).
    *   Triển khai cho doanh nghiệp hoặc khách hàng thực tế.
    *   Muốn môi trường ổn định, dễ dàng chia sẻ cho team.

*   **Dùng CLONE GIT khi:**
    *   Bạn đang nghiên cứu sâu về kiến trúc Framework/ORM của Odoo.
    *   Cần viết bản vá (Patch) trực tiếp vào mã nguồn lõi của Odoo.
    *   Muốn đóng góp (Contribute) mã nguồn cho Odoo Community.

---

### Gợi ý thực tế (Quick Choice)

| Tình huống cụ thể | Lựa chọn tối ưu |
| :--- | :--- |
| **Lập trình module HRM hàng ngày** | **Docker + Mount Addons** |
| **Triển khai ứng dụng lên Server** | **Docker** |
| **Học Odoo cơ bản (ORM, Data, View)** | **Docker** |
| **Nghiên cứu sâu mã nguồn Odoo Core** | **Clone Git** |
| **Thiết lập CI/CD, Auto-deploy** | **Docker** |