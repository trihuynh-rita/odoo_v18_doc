# Quyền Truy cập trong Odoo (Access Rights - ACL)

Quyền truy cập (Access Rights) trong Odoo được dùng để cấp quyền thao tác trên toàn bộ một Model cụ thể cho một Nhóm người dùng (Group). Nếu một người dùng không có bản ghi quyền truy cập nào khớp với thao tác họ đang thực hiện trên Model đó (thông qua các nhóm mà họ tham gia), họ sẽ bị từ chối truy cập.

---

## 1. Đặc tính của Quyền truy cập

*   **Tính cộng dồn (Additive):** Quyền truy cập của một người dùng là tổng hợp của tất cả các quyền từ các nhóm mà người dùng đó tham gia. 
    *   *Ví dụ:* Nếu Nhóm A cấp quyền **Đọc (Read)** và **Tạo (Create)**, còn Nhóm B cấp quyền **Sửa (Write)**, thì người dùng thuộc cả hai nhóm này sẽ có đủ các quyền: Tạo, Đọc và Sửa.
*   **Phạm vi Model:** ACL tác động lên toàn bộ dữ liệu của một Model. Để lọc quyền trên từng dòng dữ liệu cụ thể, Odoo sử dụng một cơ chế khác gọi là **Record Rules**.

---

## 2. Cấu trúc của Model `ir.model.access.csv`

Mọi cài đặt quyền truy cập đều được lưu trữ trong model hệ thống `ir.model.access.csv`. Các trường dữ liệu quan trọng bao gồm:

| Trường (Field) | Ý nghĩa |
| :--- | :--- |
| **Name (`name`)** | Tên gợi nhớ cho quyền truy cập hoặc mô tả vai trò. |
| **Model** (`model_i:id`) | Model mà quyền truy cập này sẽ kiểm soát. |
| **Group** (`group_id:id`) | Nhóm người dùng (`res.groups`) được cấp quyền. Nếu để trống, quyền này sẽ được cấp cho **tất cả người dùng** (bao gồm cả người dùng Portal và Public). |

---

## 3. Các quyền thao tác (CRUD Operations)

Khi khai báo, bạn cần thiết lập giá trị cho 4 thuộc tính tương ứng với các thao tác cơ bản (mặc định là 0 - không có quyền):

*   **`perm_read` (Đọc):** Cho phép xem các bản ghi của model.
*   **`perm_create` (Tạo):** Cho phép tạo mới bản ghi.
*   **`perm_write` (Sửa):** Cho phép cập nhật thông tin các bản ghi hiện có.
*   **`perm_unlink` (Xóa):** Cho phép xóa bản ghi khỏi hệ thống.

---

## 4. Cách khai báo trong file `ir.model.access.csv`

Thông thường, quyền truy cập được định nghĩa trong file CSV theo định dạng sau:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_create,perm_write,perm_unlink
access_movie_showing_user,access.movie.showing.user,model_movie_showing,group_movie_user,1,1,1,0
```

> [!IMPORTANT]
> **Lưu ý quan trọng:**
> 1.  `id`: Phải là duy nhất trong module.
> 2.  `model_id:id`: Có dạng `model_<tên_model_bỏ_dấu_chấm>` (Ví dụ: `model_crm_lead`).
> 3.  Nếu không khai báo ACL cho một model mới tạo, ngay cả người quản trị (Admin) cũng có thể không thấy hoặc không thao tác được với model đó (trừ khi bật chế độ Debug).

---
**Tài liệu tham khảo:**
*   Odoo Official Documentation: Security - Access Rights.
*   Odoo Framework: `ir.model.access` technical reference.
