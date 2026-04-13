# Hướng dẫn Cấu hình Nhóm Truy cập (Access Groups) & Quy tắc Bảo mật Odoo

Tài liệu này cung cấp hướng dẫn toàn diện về cách triển khai các nhóm truy cập và quy tắc bảo mật trong các phiên bản Odoo hiện đại (Odoo 18/19). Tài liệu bao gồm kiến trúc phân cấp và cú pháp cho các trường quan hệ trong dữ liệu XML.

## 1. Kiến trúc Bảo mật (Odoo 18/19)

Các phiên bản Odoo hiện đại sử dụng phân loại 3 lớp cho quyền truy cập để cải thiện khả năng mở rộng và tổ chức giao diện người dùng (UI) trong menu Cài đặt:

1.  **`ir.module.category`**: Cấp cao nhất. Nó định nghĩa khu vực "Ứng dụng" (ví dụ: Cinema Management hoặc Project).
2.  **`res.groups.privilege`**: Một lớp trung gian đại diện cho một khả năng chức năng cụ thể. Nó liên kết với một danh mục (category) và có trường `sequence` để điều khiển vị trí trong danh sách chọn (dropdown).
3.  **`res.groups`**: Bản ghi nhóm thực tế nắm giữ các quyền kỹ thuật. Nó liên kết với một **Đặc quyền (Privilege)**, không liên kết trực tiếp với Danh mục.

### Ví dụ về Triển khai Phân cấp:
```xml
<!-- 1. Định nghĩa Danh mục (Category) -->
<record id="cinema_management_group_category" model="ir.module.category">
    <field name="name">Cinema Management</field>
</record>

<!-- 2. Định nghĩa Đặc quyền (Privilege) -->
<record id="cinema_management_privilege" model="res.groups.privilege">
    <field name="name">Cinema Management</field>
    <field name="category_id" ref="cinema_management_group_category"/>
</record>

<!-- 3. Định nghĩa Nhóm (Group) -->
<record id="cinema_user_group" model="res.groups">
    <field name="name">User</field>
    <field name="privilege_id" ref="cinema_management_privilege"/>
</record>
```

---

## 2. Hướng dẫn Cú pháp Trường Quan hệ (Relational Field)

Viết định nghĩa các trường một cách chính xác là điều cần thiết để ngăn chặn lỗi phân tích cú pháp (parsing) và lỗi đồng bộ hóa.

### `name`: Trường Mục tiêu
Thuộc tính `name` trong thẻ `<field>` chỉ định trường nào trên model mà bạn đang điền dữ liệu.
*   **Đối với `res.groups`**: Sử dụng `privilege_id` (không dùng `category_id`).
*   **Đối với `ir.rule`**: Sử dụng `groups` (không dùng `group_id`).

### `eval`: Thực thi Python
Thuộc tính `eval` được sử dụng khi một trường yêu cầu thực thi mã thay vì văn bản thuần túy.
*   **Lệnh Quan hệ (Relational Commands)**: Cực kỳ quan trọng cho các trường Many2many hoặc One2many.
*   **Cú pháp Lệnh (Command Syntax)**: `[(4, ID)]`
    *   `4` = Liên kết (Link) tới bản ghi đã tồn tại.
    *   `6` = Thay thế (Replace) tất cả các liên kết bằng các bản ghi này: `[(6, 0, [ID1, ID2])]`.

### `ref`: Giải quyết ID bên ngoài (External ID Resolution)
Hàm `ref()` được sử dụng bên trong `eval` để chuyển đổi một XML ID thân thiện với nhà phát triển (như `cinema_user_group`) thành một Integer ID cụ thể trong cơ sở dữ liệu.

| **Cú pháp** | **Cách dùng** | **Kết quả** |
| :--- | :--- | :--- |
| `ref="id_name"` | Thuộc tính trên thẻ `<field>` | Tham chiếu Many2one đơn giản. |
| `ref('id_name')` | Hàm bên trong `eval` | Trả về Integer ID (ví dụ: 15). |

---

## 3. Các thực tiễn tốt nhất cho Quy tắc Bản ghi (`ir.rule`)

Quy tắc bản ghi lọc những bản ghi mà một nhóm cụ thể có thể tương tác bằng cách sử dụng một Domain.

### Các thành phần cú pháp chính:
```xml
<record id="example_rule" model="ir.rule">
    <field name="name">Mô tả Quy tắc</field>
    <field name="model_id" ref="model_ten_model_cua_ban"/>
    <!-- Bộ lọc Domain -->
    <field name="domain_force">[('is_active', '=', True)]</field>
    <!-- Quyền CRUD -->
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="False"/>
    <!-- Liên kết quan hệ tới Nhóm -->
    <field name="groups" eval="[(4, ref('group_xml_id'))]"/>
</record>

## 4. Sử dụng Trường `sequence` để Sắp xếp Giao diện (UI)

Trường `sequence` là một công cụ mạnh mẽ để kiểm soát cách các ứng dụng và đặc quyền của bạn hiển thị trong form người dùng Odoo (Settings > Users).

### Sắp xếp Thứ tự Ứng dụng (Category)
Khi bạn định nghĩa một `ir.module.category`, trường `sequence` quyết định vị trí của ứng dụng đó trong danh sách dài các ứng dụng của Odoo.
*   **Giá trị**: Số nguyên (mặc định là 100).
*   **Nguyên tắc**: Số càng nhỏ, ứng dụng càng hiện lên phía trên cùng của danh sách.

### Sắp xếp Thứ tự Đặc quyền (Privilege)
Khi một ứng dụng có nhiều menu dropdown khác nhau, `sequence` trong `res.groups.privilege` quyết định dropdown nào hiển thị trước dropdown nào.

### Ví dụ Code:
```xml
<!-- Đưa ứng dụng Cinema lên vị trí ưu tiên cao trong danh sách App -->
<record id="cinema_management_group_category" model="ir.module.category">
    <field name="name">Cinema Management</field>
    <field name="sequence">10</field> 
</record>

<!-- Đưa quyền quản lý Cinema lên trên các quyền khác của cùng Category -->
<record id="cinema_management_privilege" model="res.groups.privilege">
    <field name="name">Cinema Management</field>
    <field name="category_id" ref="cinema_management_group_category"/>
    <field name="sequence">5</field>
</record>
```

---

> [!IMPORTANT]
> **Luôn luôn** kiểm tra xem trường mục tiêu của model là số ít (`_id`) hay số nhiều (Many2many). Nếu là Many2many, bạn **bắt buộc** phải sử dụng cú pháp danh sách `eval="[(4, ref('...'))]"`.

> [!TIP]
> Sử dụng trường `sequence` một cách thông minh sẽ giúp giao diện quản lý người dùng trở nên chuyên nghiệp và dễ tìm kiếm hơn cho quản trị viên hệ thống.