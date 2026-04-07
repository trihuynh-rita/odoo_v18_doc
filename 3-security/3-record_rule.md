# Advanced Record Rule in Odoo

## 1. Record Rule là gì? (What is a Record Rule?)
- Trong hệ thống Odoo, **Record Rule** (`ir.rule`) là một cơ chế phân quyền điều khiển truy cập nâng cao (row-level security).
- Khác với Security Access Rights (`ir.model.access.csv`) quyết định xem một người dùng có quyền (đọc, ghi, tạo, xóa) trên CẢ MỘT MODEL (Bảng) hay không, thì Record Rule quyết định người dùng đó chỉ có quyền tác động vào NHỮNG BẢN GHI NÀO cụ thể bên trong model đó.

## 2. Kiến trúc, Cú pháp và Các Attributes (Architecture & Attributes)
Record rule được khai báo dưới dạng dữ liệu trong file XML. Các file này thường được đặt trong thư mục `security/`.

### 2.1 Cấu trúc cơ bản 
Dựa vào đoạn code mẫu trong file `cinema_manager_record_rule.xml`:

```xml
<odoo>
    <record id="present_movie_showing_rules" model="ir.rule">
        <!-- Tên của Record Rule -->
        <field name="name">Present Movie Showing</field>
        
        <!-- Chỉ định Model bị áp dụng luật -->
        <field name="model_id" ref="model_movie_showing"/>
        
        <!-- Luật (Record Rule Condition) -->
        <field name="domain_force">[('is_past', '=', False)]</field>
        
        <!-- Áp dụng cho từng nhóm người dùng (nếu không định nghĩa thì là Global Rule) -->
        <!-- <field name="groups" eval="[(4, ref('base.group_user'))]"/> -->
        
        <!-- Các thao tác bị kiểm soát bởi luật này -->
        <field name="perm_write" eval="True"/>
        <field name="perm_read" eval="False"/>
        <field name="perm_create" eval="False"/>
        <field name="perm_unlink" eval="False"/>
    </record>
</odoo>
```

### 2.2 Giải thích các thuộc tính (Attributes)
- `id`: Định danh ID duy nhất của record rule trên hệ thống.
- `model`: Luôn là `ir.rule` (để báo cho Odoo biết đây là dữ liệu cho bảng luật lệ của hệ thống).
- `name`: Tên của record rule, giúp nhận biết chức năng của luật trên giao diện người dùng hệ thống.
- `model_id`: Bắt buộc tham chiếu (reference) tới Model sẽ bị áp dụng luật, sử dụng tiền tố `model_` cộng với tên module định dạng các dấu chấm (`.`) chuyển thành dấu gạch ngang dưới (`_`). VD: `ref="model_movie_showing"` là áp dụng cho model `movie.showing`.
- `domain_force`: Là một *Domain (biểu thức lọc)* chứa các tuple điều kiện. Hệ thống sẽ so khớp, nếu bản ghi thỏa mãn domain này thì thao tác (Operation) tiếp theo mới được đồng ý. 
  - VD: `[('is_past', '=', False)]`: Chỉ xử lý các lịch chiếu phim (`movie.showing`) có thuộc tính `is_past` bằng `False` (tức là chưa diễn ra).
- Các định nghĩa về Thao tác (Permissions - Quyền lực): Xác định luật Record Rule sẽ KÍCH HOẠT ở thao tác nào.
  - Về giá trị: Cờ `eval="True"` (sẽ kích hoạt luật cho hành động đó) và `eval="False"` (bỏ qua filter của Record Rule, chỉ dựa vào `ir.model.access`).
  - `perm_read`: Áp dụng luật cho thao tác Đọc / Xem (`Read`).
  - `perm_write`: Áp dụng luật cho thao tác Viết / Cập nhật (`Write`). VD: Cho giới hạn chỉ được cập nhật các lịch phim chưa chiếu.
  - `perm_create`: Áp dụng luật cho thao tác Tạo mới (`Create`).
  - `perm_unlink`: Áp dụng luật cho thao tác Xóa (`Unlink`).

*Lưu ý: Nếu một luật định nghĩa thuộc tính `groups` bằng lệnh `eval="[(4, ref('Tên_nhóm'))]"`, nó sẽ chỉ tác động tới nhóm quyền đó. Nếu không có `groups`, nó sẽ là hệ thống Global áp dụng cho MỌI TÀI KHOẢN.*

## 3. Các bước thực hiện 
1. **Tạo file XML**: Tạo một file có đuôi `.xml` (tên thường đặt chứa từ record rules cho dễ nhớ, vd: `cinema_manager_record_rule.xml`) bên trong thư mục `security/` của module.
2. **Khai báo luật ghi chú Xml**: Viết thẻ `<record>` với các trường như `name`, `model_id`, `domain_force` và các thuộc tính phân quyền (`perm_write`, `perm_read`, `perm_create`, `perm_unlink`) như phần trên.
3. **Khai báo Data vào `__manifest__.py`**:
   - Mở file cấu hình module.
   - Trỏ đường dẫn tương đối của file XML đã tạo vào bên trong list `data`. 
   - VD: `'data': ['security/ir.model.access.csv', 'security/cinema_manager_record_rule.xml', ...]`
4. **Cập nhật (Upgrade) Module**: Khởi động lại service Odoo (restart), vào danh sách Apps để thực hiện Upgrade cho module đã thay đổi code để file XML được load vào Database.
5. **Đăng nhập Kiểm tra**: Chuyển đổi qua lại người dùng tương ứng với logic để test xem khi read/write/unlink bản ghi có nhận được thông báo giới hạn Access Rules từ hệ thống hay không.