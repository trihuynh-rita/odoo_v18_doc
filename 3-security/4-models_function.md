# Tổng hợp Kiến thức về Model Function & Quản lý Truy cập trong Odoo

Tài liệu này tổng hợp các kiến thức quan trọng về việc ghi đè (override) các hàm cơ bản của Odoo (ORM functions), cách kiểm tra quyền (security checks) và cơ chế phân quyền trong Python.

---

## 1. Ghi đè hàm `write()` (Override Model Function)

Hàm `write()` được gọi khi một hoặc nhiều bản ghi hiện có được cập nhật. Chúng ta thường ghi đè hàm này để thực hiện xác thực (validation) hoặc kiểm tra quyền trước khi dữ liệu được lưu vào cơ sở dữ liệu.

### Cấu trúc cơ bản:
```python
def write(self, vals):
    # 'vals' là một dictionary chứa các trường đang được cập nhật
    # Ví dụ: {'status': 'ended'}
    
    if 'status' in vals:
        # Thực hiện logic kiểm tra tại đây...
        pass
        
    # LUÔN LUÔN phải gọi super() để thực hiện việc ghi thực sự
    res = super().write(vals)
    return res
```

---

## 2. Kiểm tra Quyền trong Python (`has_group`)

Để kiểm tra xem một người dùng có thuộc một nhóm bảo mật nào đó hay không, chúng ta sử dụng phương thức `has_group()` trên đối tượng User.

### Cú pháp Quan trọng:
*   **Tham số**: Phải là một chuỗi chứa **Full XML ID** theo định dạng: `module_name.xml_id_of_group`.
*   **Vị trí**: `self.env.user.has_group('module.group_id')`.

> [!WARNING]
> Nếu bạn chỉ điền `xml_id` mà thiếu `module_name.`, Odoo sẽ tìm kiếm trong module `base` và thường sẽ trả về kết quả sai (`False`), dẫn đến việc logic của bạn không hoạt động.

---

## 3. Cơ chế Nhóm Kế thừa (Implied Groups)

Đây là cơ chế quan trọng cần hiểu khi thiết kế logic bảo mật.

### Cách thức hoạt động:
*   Nếu nhóm **Manager** có `implied_ids` là nhóm **User**, thì bất kỳ ai là Manager **cũng mặc nhiên là User**.
*   Khi đó, `has_group('module.user_group')` sẽ trả về `True` cho cả User và Manager.

### Giải pháp check quyền chính xác:
Để chặn User thường nhưng cho phép Manager, bạn nên dùng logic: **"Nếu KHÔNG phải Manager thì chặn"**.
```python
if not self.env.user.has_group('my_module.group_manager'):
    raise ValidationError("Chỉ quản lý mới được làm việc này!")
```

---

## 4. Tổng kết Logic Bảo mật 3 Lớp (Odoo 18/19)

Trong các phiên bản mới, phân quyền được tổ chức như sau:

1.  **`ir.model.access.csv`**: Quyền cơ bản ở mức model (Đọc, Ghi, Tạo, Xóa). Nếu file này set `0,0,0,0` cho một nhóm, user thuộc nhóm đó thậm chí không thể mở menu ứng dụng.
2.  **`ir.rule`**: Lọc dữ liệu theo điều kiện (ví dụ: Nhân viên chỉ thấy Phim của mình, Quản lý thấy tất cả).
3.  **Model Function (`write`, `create`, `unlink`)**: Cấp độ bảo mật cao nhất và linh hoạt nhất. Cho phép chặn cập nhật vào **từng trường cụ thể** (như trường `status`) dựa trên logic nghiệp vụ phức tạp.

---

> [!TIP]
> **Thực tiễn tốt nhất**: Sau khi thay đổi bất kỳ logic bảo mật nào trong file XML hoặc CSV, hãy nâng cấp module (`-u my_module`) để cập nhật Database. Nếu thay đổi trong Python, chỉ cần restart server.
