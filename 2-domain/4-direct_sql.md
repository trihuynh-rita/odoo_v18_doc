# Direct SQL Query trong Odoo (Thao tác SQL trực tiếp)

Khi làm việc với các Model chứa lượng dữ liệu khổng lồ (hàng trăm nghìn đến hàng triệu bản ghi như Logs, Reviews, Ratings), Odoo ORM (Object-Relational Mapping) thường gặp vấn đề về hiệu suất nghiêm trọng. Việc sử dụng Direct SQL Query giúp tối ưu hóa tốc độ và tài nguyên bằng cách làm việc trực tiếp với PostgreSQL.

---

## 1. Tại sao và Khi nào nên dùng Direct SQL?

### Hạn chế của Odoo ORM:
* **Tốc độ cực chậm:** ORM phải khởi tạo các Object Python cho mỗi bản ghi, gây tốn bộ nhớ và thời gian xử lý.
* **Lỗi treo hệ thống (Timeout):** Truy vấn kéo dài quá thời gian cho phép sẽ gây ra `Timeout Exception`.
* **Hủy giao dịch (Rollback):** Nếu một transaction bị timeout giữa chừng, toàn bộ các thao tác trước đó đều bị rollback, dẫn đến mất dữ liệu không mong muốn.

### Giải pháp:
Bỏ qua lớp ORM và sử dụng truy vấn SQL trực tiếp cho các thao tác tìm kiếm (`SELECT`), thêm mới (`INSERT`) hoặc cập nhật (`UPDATE`) hàng loạt.

---

## 2. Truy vấn lấy dữ liệu (SELECT)

Để lấy dữ liệu hiệu quả, chúng ta sử dụng con trỏ cơ sở dữ liệu (`cursor`).

### A. Cấu trúc truy vấn (JOIN)
Sử dụng `JOIN` trong SQL giúp lấy toàn bộ dữ liệu cần thiết từ nhiều bảng chỉ trong một lần gọi database duy nhất, thay vì phải truy vấn chéo qua lại giữa các Model của Odoo.

### B. Thực thi và lấy kết quả
* **Lệnh thực thi:** `self.env.cr.execute(query)` (hoặc `self._cr.execute(query)`).
* **Lấy dữ liệu:** Sử dụng `self.env.cr.fetchall()` để kéo toàn bộ kết quả từ database lên.

### C. Xử lý kết quả từ `fetchall()`
Lệnh `fetchall()` trả về một **List chứa các Tuples**, không phải là Recordsets. Bạn buộc phải truy xuất dữ liệu qua chỉ mục số (**index**) thay vì tên trường:
* Ví dụ dòng dữ liệu: `(id, name, rating)`
* Truy cập `id`: `record[0]`, `name`: `record[1]`, `rating`: `record[2]`.

---

## 3. Truy vấn cập nhật dữ liệu (UPDATE / INSERT)

Khi cập nhật hàng loạt, Direct SQL giúp bỏ qua các bước kiểm tra rườm rà của ORM để tác động trực tiếp xuống bảng.

* **Tên bảng:** Tên technical của model với dấu chấm `.` được thay bằng dấu gạch dưới `_` (ví dụ: `movie.review` -> `movie_review`).
* **Lưu thay đổi:** Bắt buộc phải **Commit thủ công** (`self.env.cr.commit()`) để dữ liệu được lưu xuống đĩa.

---

## 4. Mã nguồn mẫu (Tổng hợp)

```python
from odoo import models, api

class CinemaMovie(models.Model):
    _inherit = 'cinema.movie'

    def action_bulk_process_reviews(self):
        """
        Ví dụ kết hợp SELECT và UPDATE bằng Direct SQL
        """
        # 1. Lấy dữ liệu (SELECT với JOIN)
        query_select = """
            SELECT r.id, r.rating, m.name 
            FROM movie_review r
            JOIN cinema_movie m ON r.movie_id = m.id
            WHERE r.movie_id = %s
        """
        self.env.cr.execute(query_select, (self.id,))
        reviews = self.env.cr.fetchall()

        for res in reviews:
            review_id = res[0]
            rating = res[1]
            
            # 2. Cập nhật dữ liệu hàng loạt (UPDATE)
            response_msg = "Cảm ơn bạn!" if rating > 6 else "Chúng tôi sẽ cải thiện."
            query_update = "UPDATE movie_review SET staff_response = %s WHERE id = %s"
            self.env.cr.execute(query_update, (response_msg, review_id))

        # 3. BẮT BUỘC: Commit và Xóa Cache
        self.env.cr.commit()
        self.env.clear()
```

---

## 5. Những lưu ý "sống còn" (Trade-offs & Risks)

### Rủi ro về kiến trúc:
* **Bỏ qua Record Rules:** SQL trực tiếp không kích hoạt phân quyền dữ liệu. Bạn phải tự kiểm soát bảo mật.
* **Không kích hoạt Computed Fields:** ORM sẽ không tự động tính lại các trường phụ thuộc. Bạn phải tự xử lý nếu cần.

### Quy tắc an toàn:
1.  **Ngăn chặn SQL Injection:** Luôn sử dụng `%s` làm placeholder và truyền tham số qua tuple trong hàm `execute()`. Tuyệt đối không dùng f-string để nối chuỗi query.
2.  **Quản lý Transaction:** Phải gọi `self.env.cr.commit()`. Nếu không, thay đổi sẽ bị rollback khi request kết thúc.
3.  **Xóa Cache ORM:** Sử dụng `self.env.clear()`. Vì bạn sửa dữ liệu ở tầng DB nên Cache của Odoo sẽ bị cũ (stale). Lệnh này buộc Odoo load lại dữ liệu mới nhất.

---
**Tài liệu tham khảo:**
* *Odoo Official Documentation: Database Cursor.*
* *Python DB-API 2.0 (psycopg2).*