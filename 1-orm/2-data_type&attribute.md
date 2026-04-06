# Data type & Attribute

## 1. Các kiểu dữ liệu cơ bản (Basic Fields)

| Nhóm | Loại dữ liệu | Mô tả | Ví dụ |
| :--- | :--- | :--- | :--- |
| **Văn bản** | `Char` | Chuỗi ký tự ngắn, có giới hạn độ dài (SQL: `VARCHAR`) | `name = fields.Char(size=128)` |
| | `Text` | Chuỗi dài, không giới hạn ký tự (textarea) | `description = fields.Text()` |
| | `Html` | Nội dung HTML, hỗ trợ bộ soạn thảo Rich Text | `body = fields.Html(sanitize=True)` |
| **Số học** | `Integer` | Số nguyên (int4 trong PostgreSQL) | `qty = fields.Integer(default=1)` |
| | `Float` | Số thực, có thể chỉ định độ chính xác | `price = fields.Float(digits=(10,2))` |
| | `Monetary` | Tiền tệ, tự động hiển thị ký hiệu dựa trên `currency_id` | `amount = fields.Monetary(currency_field='currency_id')` |
| **Logic** | `Boolean` | Giá trị Đúng hoặc Sai (`True`/`False`) | `active = fields.Boolean(default=True)` |
| **Thời gian** | `Date` | Lưu trữ ngày tháng năm (không kèm giờ) | `date_start = fields.Date()` |
| | `Datetime` | Lưu trữ cả ngày và giờ (theo chuẩn UTC trong DB) | `create_date = fields.Datetime()` |
| **Lựa chọn** | `Selection` | Danh sách các giá trị cố định để người dùng chọn | `state = fields.Selection([('draft','Nháp'),('done','Xong')])` |
| **Tệp tin** | `Binary` | Dữ liệu nhị phân, dùng cho tệp đính kèm | `file = fields.Binary(attachment=True)` |
| | `Image` | Chuyên dụng cho ảnh, hỗ trợ tự động thay đổi kích thước | `avatar = fields.Image(max_width=1920)` |

## 2. Các trường quan hệ (Relational Fields)

| Loại | Tên Field | Mô tả | Ví dụ |
| :--- | :--- | :--- | :--- |
| **N-1** | `Many2one` | Nhiều record trỏ đến 1 record khác. Tạo cột FK trong DB. | `partner_id = fields.Many2one('res.partner', ondelete='restrict')` |
| **1-N** | `One2many` | Chiều ngược lại của Many2one. Không tạo cột trong DB (virtual). | `line_ids = fields.One2many('sale.order.line', 'order_id')` |
| **N-N** | `Many2many` | Quan hệ nhiều - nhiều. Tạo bảng trung gian để lưu liên kết. | `tag_ids = fields.Many2many('res.partner.category')` |
| **Poly** | `Reference` | Liên kết tới nhiều model khác nhau (polymorphic). | `ref = fields.Reference(selection=[('res.partner','Partner')])` |
| **Poly** | `Many2oneReference` | Giống Reference nhưng lưu ID kèm theo model chỉ định. | `res_id = fields.Many2oneReference(model_field='res_model')` |

## 3. Các trường đặc biệt (Special Fields)

| Nhóm | Tên Field | Mô tả | Ví dụ |
| :--- | :--- | :--- | :--- |
| **Tự động** | `Id` | Primary key, tự tăng. Odoo tự tạo, không cần khai báo. | `id # auto-created` |
| **Tự động** | `Create_date` / `Write_date` | Thời gian tạo và cập nhật bản ghi cuối cùng. | `create_date = fields.Datetime(readonly=True)` |
| **Tự động** | `Create_uid` / `Write_uid` | User tạo và User cập nhật bản ghi cuối cùng. | `write_uid # automatic` |
| **Đặc biệt** | `Properties` | Dynamic fields (Odoo 16+), lưu cấu trúc động dạng JSON. | `properties = fields.Properties(definition='...')` |
| **Đặc biệt** | `Json` | Lưu dữ liệu JSON tùy biến cấu trúc (Odoo 17+). | `metadata = fields.Json()` |
| **Đặc biệt** | `Serialized` | Lưu dict/list dưới dạng JSON string trong một cột. | `config = fields.Serialized()` |
| **Helper** | `Command` | ORM Helper để thao tác nhanh với các trường quan hệ. | `[(0, 0, {vals}), (6, 0, [ids])]` |

## 4. Các thuộc tính của Field (Attributes)

| Thuộc tính | Kiểu | Mô tả |
| :--- | :--- | :--- |
| `string` | `str` | Label hiển thị trên giao diện người dùng (UI). |
| `help` | `str` | Tooltip/mô tả chi tiết khi di chuột vào field trên UI. |
| `required` | `bool` | Bắt buộc nhập liệu, không được để trống. |
| `readonly` | `bool` | Chỉ cho phép đọc, không cho người dùng sửa đổi. |
| `store` | `bool` | Có lưu vào Database không (mặc định `True` với non-computed). |
| `index` | `str/bool` | Tạo index DB: `True`, `'btree'`, `'btree_not_null'`, `'trigram'`. |
| `default` | `any` | Giá trị mặc định hoặc hàm (lambda) trả về giá trị mặc định. |
| `copy` | `bool` | Có sao chép giá trị của field này khi Duplicate bản ghi không. |
| `groups` | `str` | Giới hạn truy cập dựa trên XML ID của Security Group. |
| `states` | `dict` | Thay đổi thuộc tính (readonly, required...) theo `state` (Deprecated, nên dùng `invisible/readonly` trực tiếp trên view). |
| `deprecated` | `str` | Ghi chú cảnh báo field này đã lỗi thời và lý do. |
| `sanitize` | `bool` | Lọc các mã độc hoặc thẻ HTML nguy hiểm (chỉ áp dụng cho `Html` field). |
| `size` | `int` | Giới hạn độ dài tối đa của chuỗi ký tự (chỉ cho `Char` field). |
| `digits` | `tuple` | Độ chính xác cho `Float` hoặc `Monetary` (tổng chữ số, số thập phân). |
| `translate` | `bool/fn` | Hỗ trợ tính năng đa ngôn ngữ (i18n) cho trường dữ liệu. |
| `ondelete` | `str` | Hành vi khi record liên quan bị xoá: `'set null'`, `'restrict'`, `'cascade'` (Many2one). |
| `domain` | `list` | Bộ lọc điều kiện để giới hạn records hiển thị trong dropdown (relation fields). |
| `context` | `dict` | Context truyền đi khi mở form hoặc thao tác với relation field. |
| `comodel_name` | `str` | Tên Model đích của trường quan hệ. |
| `inverse_name` | `str` | Tên field ngược lại của quan hệ `One2many`. |
| `relation` | `str` | Tên bảng trung gian tùy chỉnh cho quan hệ `Many2many`. |
| `column1/column2`| `str` | Tên các cột Foreign Key trong bảng trung gian `Many2many`. |
| `auto_join` | `bool` | Dùng SQL JOIN thay vì subquery khi thực hiện tìm kiếm (tăng hiệu năng). |
| `check_company` | `bool` | Kiểm tra tính nhất quán của Company khi gán giá trị Many2one. |
| `prefetch` | `bool/str` | Kiểm soát prefetch group khi load record để tối ưu query. |
| `recursive` | `bool` | Field tính toán (computed) có phụ thuộc vào chính nó không (đệ quy). |
| `precompute` | `bool` | Tính toán giá trị trước khi INSERT vào DB (Odoo 16+). |
| `aggregator` | `str` | Hàm tổng hợp trong Group By: `'sum'`, `'avg'`, `'min'`, `'max'`, `'count'` (Odoo 17+). |
| `export_string_translation` | `bool` | Có xuất bản dịch của field dưới dạng string khi export không. |

## 5. Trường tính toán & Liên kết (Computed & Related)

| Nhóm | Từ khóa | Mô tả | Ví dụ |
| :--- | :--- | :--- | :--- |
| **Computed** | `compute` | Hàm tính toán động, dùng `@api.depends` để theo dõi thay đổi. | `total = fields.Float(compute='_compute_total', store=True)` |
| **Computed** | `inverse` | Cho phép người dùng nhập liệu ngược lại vào trường được tính toán. | `fields.Char(compute='_get', inverse='_set')` |
| **Computed** | `search` | Định nghĩa logic tìm kiếm cho các computed field không lưu (`store=False`). | `fields.Char(compute='_get', search='_search')` |
| **Related** | `related` | Truy xuất trực tiếp dữ liệu từ model liên quan (Shortcut). | `partner_name = fields.Char(related='partner_id.name', store=True)` |