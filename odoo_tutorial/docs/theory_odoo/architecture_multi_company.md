# Kiến thức về Cơ chế Multi-company trong Odoo

## 1. Bản chất của Multi-company
Multi-company là cơ chế kiến trúc cho phép một database duy nhất phục vụ nhiều thực thể doanh nghiệp (ví dụ: công ty con, chi nhánh tại nhiều quốc gia). Dữ liệu được cô lập logic ở cấp độ **Model** và **Record Rule** để đảm bảo tính riêng tư giữa các công ty.

## 2. Ba bước bắt buộc để thiết lập Multi-company
Để một Model custom có thể phân tách dữ liệu theo công ty, lập trình viên phải thực hiện đủ 3 bước sau:

### Bước 1: Khai báo trường liên kết công ty (Cấp độ Model)
Bạn phải thêm trường `company_id` trỏ tới model `res.company`.
```python
company_id = fields.Many2one(
    'res.company', 
    string='Công ty',
    required=True,
    default=lambda self: self.env.company
)
```
- **Giải thích:** `lambda self: self.env.company` giúp gán công ty hiện tại mà user đang làm việc (`env.company`) làm giá trị mặc định khi tạo bản ghi mới.

### Bước 2: Hiển thị trường trên View
Đưa trường `company_id` vào **Form View** hoặc **Tree View** để user có thể kiểm tra và quản lý bản ghi thuộc về công ty nào.

### Bước 3: Cấu hình Record Rule (Lớp bảo mật cốt lõi)
Nếu không có Record Rule, hệ thống sẽ không tự động lọc dữ liệu dù đã có trường `company_id`.
```xml
<record id="movie_theater_multi_company_rule" model="ir.rule">
    <field name="name">Movie Theater: Multi-Company Rule</field>
    <field name="model_id" ref="model_movie_theater"/>
    <field name="domain_force">[('company_id', 'in', company_ids)]</field>
</record>
```
- **Giải thích:** `company_ids` (số nhiều) là biến môi trường chứa danh sách ID của các công ty mà user hiện tại đang được phép truy cập.

## 3. Vượt quyền bằng `.sudo()`
Trong các bài toán cần tính toán số liệu tổng hợp (ví dụ: Doanh thu toàn cầu của chuỗi rạp), chúng ta cần truy cập dữ liệu của TẤT CẢ công ty.

- **Vấn đề:** Các câu lệnh `search()` thông thường sẽ bị Record Rule ở Bước 3 lọc bỏ các công ty khác.
- **Giải pháp:** Sử dụng phương thức `.sudo()` (Superuser Do).
```python
# Lấy TOÀN BỘ rạp chiếu phim bất chấp phân quyền Multi-company
all_theaters = self.env['movie.theater'].sudo().search([])
```
`.sudo()` giúp bỏ qua toàn bộ kiểm tra quyền (Access Rights) và Record Rules để truy cập trực tiếp vào toàn bộ dữ liệu thô trong database.

---
*Tài liệu này được biên soạn dựa trên các nghiên cứu về kiến trúc Odoo cho mục đích ôn tập.*
