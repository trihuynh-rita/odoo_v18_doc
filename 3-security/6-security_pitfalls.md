# Các lỗ hổng bảo mật

## 1. Bảo mật ở tầng Cơ sở dữ liệu (Database Layer)
* **Không lạm dụng SQL thuần (Bypassing the ORM):** * Luôn ưu tiên dùng các hàm ORM có sẵn (như `search()`, `write()`).
    * *Lý do:* Nếu gọi thẳng lệnh SQL (`self.env.cr.execute`), bạn sẽ vô tình vượt rào qua toàn bộ cơ chế bảo mật của Odoo (Access Rights, Record Rules), làm mất tự động dịch ngôn ngữ và mất cơ chế vô hiệu hóa cache.
* **Ngăn chặn SQL Injection:**
    * Nếu bắt buộc phải viết câu lệnh SQL thủ công, **tuyệt đối không** dùng phép cộng chuỗi (`+`) hoặc định dạng chuỗi (`%s` trong Python string) để nối biến do người dùng nhập vào câu SQL.
    * *Giải pháp:* Hãy truyền biến dưới dạng một `tuple` vào tham số thứ hai của hàm `execute()`. Thư viện `psycopg2` (trình điều khiển PostgreSQL) sẽ tự động xử lý định dạng và làm sạch chuỗi (escape) một cách an toàn.
* **Example:**
``` python
# the following is very bad:
#   - it's a SQL injection vulnerability
#   - it's unreadable
#   - it's not your job to format the list of ids
self.env.cr.execute('SELECT distinct child_id FROM account_account_consol_rel ' +
           'WHERE parent_id IN ('+','.join(map(str, ids))+')') 
           # the hacker can add the "(1) OR 1=1; DROP TABLE account_account_consol_rel; --)" to delete our database

# better
self.env.cr.execute('SELECT DISTINCT child_id '\
           'FROM account_account_consol_rel '\
           'WHERE parent_id IN %s',
           (tuple(ids),))
```

## 2. Bảo mật ở tầng Giao diện & Hiển thị (XSS - Cross-Site Scripting)

Đây là phần giải thích cách ngăn chặn việc thực thi các đoạn mã độc hại (như JavaScript) khi hiển thị dữ liệu người dùng nhập lên giao diện (QWeb/XML).

* **Tuyệt đối tránh dùng `t-raw`:** Luôn ưu tiên dùng `t-esc` để Odoo tự động chuyển đổi các ký tự đặc biệt thành văn bản an toàn.
* **Hiểu rõ: Escaping (Làm sạch ký tự) vs. Sanitizing (Khử trùng HTML):**
    * **Escaping (Bắt buộc):** Chuyển đổi dữ liệu Text thành dạng an toàn (ví dụ: `<` thành `&lt;`). Dùng khi bạn chắc chắn dữ liệu đó chỉ là văn bản.
    * **Sanitizing (Khử trùng):** Dùng khi dữ liệu đầu vào chứa các thẻ HTML (như bài viết Rich Text từ người dùng). Sanitizing sẽ lọc và giữ lại các thẻ an toàn (như `<p>`, `<b>`), nhưng xóa bỏ các mã độc (như `<script>`).
* **Sử dụng đối tượng `Markup`:** Odoo cung cấp class `Markup` để phân tách rõ ràng phần nào là cấu trúc HTML cố định, phần nào là dữ liệu động cần được Escape. Không bao giờ dùng `f-string` kết hợp với `Markup`.

## 3. Bảo mật ở tầng Logic Nghiệp vụ (Python Execution)
* **Tuyệt đối không dùng hàm `eval()`:**
    * `eval()` sẽ biên dịch và chạy bất kỳ đoạn mã Python nào do người dùng truyền vào, dẫn đến nguy cơ bị chiếm quyền điều khiển server.
    * *Giải pháp:* Để parse chuỗi thành kiểu dữ liệu (như Dictionary hay List), hãy dùng `ast.literal_eval()` hoặc `json.loads()`. Hàm `safe_eval` của Odoo an toàn hơn một chút nhưng cũng chỉ nên dùng cho nội bộ quản trị viên.
* **Không dùng `getattr()` và `setattr()` để lấy trường dữ liệu động:**
    * Việc gọi `getattr(record, user_input)` là cực kỳ nguy hiểm vì người dùng có thể đoán tên và gọi ra các biến/hàm private của hệ thống (những hàm bắt đầu bằng dấu `_`).
    * *Giải pháp:* Để lấy giá trị động của một field, hãy dùng cơ chế dictionary tích hợp sẵn của recordset: `record[user_input]`.

## 4. Quản lý quyền truy cập Phương thức (Public vs Private Methods)
* **Public Methods (Hàm công khai):** Những hàm không có dấu gạch dưới `_` ở đầu (ví dụ: `def action_done(self):`) có thể bị gọi từ bên ngoài thông qua giao thức RPC. Bạn không thể tin tưởng 100% vào các tham số truyền vào hàm này.
* **Private Methods (Hàm nội bộ):** Những hàm bắt đầu bằng `_` (ví dụ: `def _set_state(self):`) không thể bị gọi qua nút bấm trên giao diện hay từ API bên ngoài. Dùng nó để đóng gói các logic nhảy cảm hoặc khi dùng `sudo()`.

---

Bạn có đang sử dụng hàm `self.env.cr.execute` hay `eval()` ở đâu trong mã nguồn của module Sản phẩm mà chúng ta đang xây dựng (Task-01 đến Task-08) không? Nếu có, bạn có muốn gửi đoạn code đó lên đây để tôi hướng dẫn cách tái cấu trúc lại cho an toàn không?