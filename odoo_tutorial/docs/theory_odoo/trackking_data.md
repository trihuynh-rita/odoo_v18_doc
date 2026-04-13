# Tracking data

## Chatter trong model

### 1. Khái niệm Chatter trong Odoo
Chatter là một khu vực giao diện thường nằm ở bên phải hoặc bên dưới form nhập liệu trong Odoo. Nó hoạt động như một hệ thống nhật ký (log) và giao tiếp, cho phép ghi lại:
* Ai đã thay đổi dữ liệu?
* Thay đổi vào lúc nào?
* Giá trị cũ và giá trị mới là gì?


*Về mặt lý thuyết phần mềm, đây là ứng dụng thực tế của cơ chế **Audit Trail** (Dấu vết kiểm toán) nhằm đảm bảo tính toàn vẹn, bảo mật và khả năng truy xuất nguồn gốc dữ liệu (tham khảo: Information security audit trail concepts).*

### 2. Các bước tích hợp Chatter vào một Model mới
Để bật tính năng này cho một model tự tạo (từ đầu, không phải kế thừa model có sẵn của Odoo), cần thực hiện 3 bước:

**Bước 1: Kế thừa các mixin model trong Python**
*Lưu ý: Đoạn transcript bị lỗi nhận diện giọng nói (speech-to-text) hiển thị là "male" và "male activity mixing". Từ chính xác trong mã nguồn Odoo là `mail`.*
Trong file Python khai báo model, bắt buộc phải kế thừa (inherit) hai class sau:
* `mail.thread`: Kích hoạt tính năng theo dõi thông báo và gửi email.
* `mail.activity.mixin`: Kích hoạt tính năng lên lịch hoạt động (to-do, gọi điện, họp...).
```python
_inherit = ['mail.thread', 'mail.activity.mixin']
```

**Bước 2: Cập nhật giao diện (XML View)**
Khai báo thẻ chatter bên trong Form View của model (thường đặt sau thẻ `</sheet>`) để giao diện hiển thị khu vực log.
```xml
<div class="oe_chatter">
    <field name="message_follower_ids"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>
```

**Bước 3: Chỉ định trường cần theo dõi (Tracking)**
Mặc định, Odoo không theo dõi toàn bộ các trường để tránh làm phình cơ sở dữ liệu và rác giao diện. Để theo dõi một trường cụ thể, cần thêm tham số `tracking=True` vào khai báo trường đó trong Python.
```python
name = fields.Char(string='Theater Name', tracking=True)
```

### 3. Hạn chế kỹ thuật và cách khắc phục
Bài giảng có nhấn mạnh một hạn chế quan trọng của tham số `tracking=True`:
* **Hỗ trợ:** Các trường dữ liệu cơ bản (Char, Integer, Boolean...) và trường quan hệ `Many2one`.
* **Không hỗ trợ:** Các trường quan hệ phức tạp như `One2many` hoặc `Many2many`. Việc tính toán sự thay đổi giữa các tập hợp danh sách dữ liệu này tốn nhiều tài nguyên.

**Cách khắc phục (Workaround):** Để ghi log khi có sự thay đổi ở trường `One2many` hoặc `Many2many`, lập trình viên phải can thiệp thủ công bằng cách ghi đè (override) hàm `write()` (hàm cập nhật dữ liệu) của model. Trong hàm này, bạn kiểm tra xem trường đó có bị thay đổi không, nếu có thì gọi hàm tạo log (ví dụ: `message_post()`) để ghi nhận vào Chatter.

## Hạn chế và cách khắc phục

### 1. Cập nhật về khả năng Tracking (Theo dõi) dữ liệu
Đầu tiên, giảng viên đính chính một thông tin quan trọng: Ở các phiên bản Odoo hiện đại, hệ thống **đã hỗ trợ** việc theo dõi sự thay đổi trên các trường quan hệ phức tạp như `Many2many` (ví dụ: thêm/bớt danh sách phòng chiếu). 
Bạn chỉ cần thêm thuộc tính `tracking=True` khi khai báo trường trong class Python, hệ thống sẽ tự động ghi nhận lại các thao tác thay đổi dữ liệu của trường đó vào Chatter.

### 2. Vấn đề: Khi nào `tracking=True` là chưa đủ?
Việc bật `tracking=True` rất hữu ích để lưu lại lịch sử giá trị (ví dụ: giá vé đổi từ 50.000đ sang 60.000đ). Tuy nhiên, nó không cung cấp **ngữ cảnh (context)** của sự thay đổi đó.

Trong bài giảng, giảng viên đưa ra tình huống: Hệ thống có một *Scheduled Action* (tác vụ tự động chạy ngầm theo lịch) để tự động cập nhật giá vé. Nếu chỉ dùng tracking mặc định, người quản trị sẽ không biết sự thay đổi này do người dùng sửa bằng tay hay do hệ thống tự chạy ngầm.

### 3. Giải pháp: Ghi log tùy chỉnh bằng hàm `message_post()`
Để chèn một thông báo cụ thể vào Chatter giải thích cho một hành động nghiệp vụ, Odoo cung cấp hàm `message_post()`. 

**Quá trình triển khai logic:**
* **Gộp các Recordset (Tập bản ghi):** Giảng viên có 2 tập hợp các suất chiếu cần cập nhật (`showings` và `other_showings`). Để tối ưu code thay vì viết 2 vòng lặp riêng biệt, Odoo hỗ trợ gộp các tập bản ghi lại với nhau bằng toán tử `|` (Phép hợp / Union trong lý thuyết tập hợp).
    ```python
    # Gộp 2 recordsets lại thành 1
    all_showings = showings | other_showings
    ```
* **Ghi log bằng vòng lặp:** Sau khi thực hiện logic cập nhật giá vé (dùng hàm `write()`), ta duyệt qua tập bản ghi đã gộp và gọi hàm chèn thông báo.
    ```python
    for showing in all_showings:
        showing.message_post(body="Tác vụ tự động cập nhật giá vé đã được thực thi.")
    ```



**Lưu ý về lỗi (Error) trong bài giảng:**
Ban đầu, giảng viên cố gắng truyền thêm tham số định dạng `type="comment"` vào hàm `message_post()` nhưng bị hệ thống báo lỗi. Thực tế, khi bạn chỉ truyền tham số `body` (nội dung text hoặc HTML), Odoo sẽ tự động hiểu và gán loại message đó là thông báo (notification/comment) tiêu chuẩn hiển thị trực tiếp trên luồng sự kiện của Chatter, nên việc ép kiểu tham số `type` trong trường hợp này là không cần thiết.

---
Bạn có muốn tôi viết lại một đoạn code Python hoàn chỉnh mô phỏng file logic của tác vụ *Scheduled Action* này (bao gồm cả hàm `search`, `write`, và `message_post`) để bạn dễ hình dung cấu trúc thực tế không?