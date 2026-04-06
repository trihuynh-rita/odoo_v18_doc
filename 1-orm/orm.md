### 1. Định nghĩa Class Python kế thừa từ `models.Model`
Trong Odoo, mọi bảng dữ liệu (Table) trong PostgreSQL đều được đại diện bằng một Class Python. Việc kế thừa từ lớp `models.Model` là cách  "đăng ký" class này với bộ máy ORM của Odoo.

* **Bản chất:** Khi server Odoo khởi động, ORM sẽ quét tất cả các class kế thừa từ `models.Model` và tự động chuyển đổi (dịch) chúng thành các câu lệnh SQL để thao tác với database.
* **Các thuộc tính bắt buộc:**
    * `_name`: Tên định danh duy nhất của model trên toàn hệ thống (ví dụ: `'hospital.patient'`).
    * `_description`: Mô tả ngắn gọn về model dành cho developer.

```python
from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hồ sơ bệnh nhân'
    # Các fields sẽ được định nghĩa ở đây
```

### 2. Phân biệt các loại Fields (Trường dữ liệu)
Odoo chia fields thành 3 nhóm chính, tương đương với các cách lưu trữ dữ liệu khác nhau.

#### A. Basic Fields (Trường cơ bản)
Đây là các trường lưu trữ giá trị vật lý trực tiếp trong một cột của bảng dữ liệu.
* `Char`: Chuỗi ký tự ngắn (Tương đương `VARCHAR` trong SQL).
* `Integer`: Số nguyên (Tương đương `INT`).
* `Boolean`: Đúng/Sai (Tương đương `BOOL`).
* *(Ngoài ra còn có: `Float`, `Text`, `Date`, `Datetime`, `Selection`).*

#### B. Relational Fields (Trường quan hệ)
Dùng để liên kết dữ liệu giữa các bảng với nhau (Tương đương Foreign Key trong CSDL quan hệ).

* **`Many2one` (Nhiều - Một):** Ví dụ: Nhiều bệnh nhân do 1 bác sĩ khám. Trường này thực chất sẽ lưu ID của bác sĩ (`doctor_id`) vào bảng bệnh nhân (tạo Foreign Key thực sự trong DB).
* **`One2many` (Một - Nhiều):** Là trường **ảo**, chiều ngược lại của `Many2one`. Bác sĩ muốn xem d sách bệnh nhân của mình. Nó không tạo cột mới trong DB mà ORM sẽ tự động truy vấn ngược.
* **`Many2many` (Nhiều - Nhiều):** Ví dụ: Một bệnh nhân có thể mắc nhiều bệnh, một bệnh có thể xuất hiện trên nhiều bệnh nhân. ORM sẽ **tự động tạo ra một bảng trung gian (Junction table)** trong PostgreSQL để lưu các cặp ID mà  không cần tự viết SQL.

#### C. Functional Fields (Trường chức năng)
Đây là các trường có giá trị được tính toán động (dynamic) bằng code Python, thay vì người dùng tự nhập.
* **`Compute`:** Trường tính toán. Ví dụ: Có trường `Năm sinh`,  dùng `Compute` để tự động tính ra `Tuổi` bằng hàm Python. Mặc định nó tính on-the-fly (không lưu xuống DB) trừ khi  thêm thuộc tính `store=True`.
* **`Related`:** Trường liên đới. Một dạng viết tắt để lấy dữ liệu qua cầu nối quan hệ. Ví dụ: Từ đơn hàng,  muốn lấy thẳng "Số điện thoại của khách hàng",  dùng `related='partner_id.phone'`.

### 3. Ánh xạ Model xuống PostgreSQL
Khi  cài đặt hoặc nâng cấp (upgrade) module, Odoo ORM sẽ thực thi phép ánh xạ như sau:

1.  **Tạo bảng:** `_name = 'hospital.patient'` sẽ được biến thành bảng `hospital_patient` (dấu chấm biến thành dấu gạch dưới).
2.  **Tạo cột:** Các Basic Fields và Many2one fields sẽ được tạo thành các cột tương ứng trong bảng đó.
3.  **Magic Columns (Cột tự động):** Dù  không định nghĩa, Odoo tự động chèn thêm 5 cột vào mọi bảng `models.Model` để theo dõi lịch sử:
    * `id`: Khóa chính (Primary Key).
    * `create_uid`: ID người tạo bản ghi.
    * `create_date`: Ngày giờ tạo.
    * `write_uid`: ID người sửa cuối cùng.
    * `write_date`: Ngày giờ sửa cuối cùng.

### 4. Các phương thức CRUD cơ bản
Đây là 5 hàm nền tảng nhất để thao tác với dữ liệu thông qua code Python (thường dùng trong Backend Logic hoặc API).

| Phương thức ORM | Tương đương SQL | Chức năng chi tiết |
| :--- | :--- | :--- |
| **`create(vals_list)`** | `INSERT INTO` | Tạo một hoặc nhiều bản ghi mới. Nhận vào một list các dictionary (key là tên field, value là giá trị). Trả về Recordset chứa các bản ghi vừa tạo. |
| **`search(domain)`** | `SELECT ... WHERE` | Tìm kiếm các bản ghi dựa trên điều kiện (Domain). Ví dụ: `.search([('age', '>=', 18)])`. Trả về một Recordset chứa các bản ghi thỏa mãn. |
| **`browse(ids)`** | `SELECT ... WHERE id IN (...)` | Lấy dữ liệu khi  **đã biết trước ID**. Ví dụ: `.browse([1, 4, 5])`. Trả về Recordset của 3 ID đó. Truy vấn này rất nh. |
| **`write(vals)`** | `UPDATE ... SET` | Cập nhật dữ liệu cho các bản ghi đang có trong Recordset hiện tại. Nhận vào một dictionary các giá trị mới. |
| **`unlink()`** | `DELETE FROM` | Xóa (vĩnh viễn) các bản ghi có trong Recordset hiện tại khỏi CSDL. |
