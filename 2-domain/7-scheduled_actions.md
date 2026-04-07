### 1. Scheduled Actions (Hành động theo lịch trình) là gì?
Scheduled Actions (hay còn gọi là Cron Jobs) là một cơ chế trong Odoo cho phép hệ thống tự động thực thi một đoạn mã (code) hoặc một tác vụ (task) lặp đi lặp lại sau những khoảng thời gian nhất định (định kỳ).

**Mục đích sử dụng:**
* Chạy các quy trình ngầm mà không cần người dùng thao tác thủ công.
* Ví dụ: Tự động gửi email nhắc nhở mỗi sáng, tự động xóa dữ liệu rác hàng tuần, tự động đồng bộ tồn kho mỗi giờ, hoặc như trong video là tự động cập nhật giá vé xem phim (Ticket Price) mỗi ngày.

### 2. Cấu trúc và cách khai báo một Scheduled Action
Để tạo một Scheduled Action thông qua mã nguồn (code), bạn cần khai báo dữ liệu trong file XML (nằm trong thư mục `data` của module). Bản chất là bạn đang tạo một bản ghi mới vào model `ir.cron` của Odoo.

**Các trường (Fields) quan trọng cần thiết lập:**
* **`id`**: Định danh duy nhất cho hành động này (ví dụ: `action_update_showing_price`).
* **`model`**: Luôn luôn là `ir.cron`.
* **`name`**: Tên hiển thị của hành động (sẽ hiện trên giao diện quản trị).
* **`model_id`**: Model chứa hàm (function) mà bạn muốn thực thi. Định dạng bắt buộc là `model_tên_model` (ví dụ: `model_movie_showing`).
* **`state`**: Luôn để là `code` (chỉ định rằng tác vụ này sẽ chạy một đoạn mã Python).
* **`code`**: Đoạn mã Python sẽ được gọi. Thông thường, đoạn mã này chỉ là lệnh gọi đến một hàm đã được định nghĩa sẵn trong model. Cú pháp: `model.ten_ham()`.
* **`interval_number`**: Số lượng chu kỳ (ví dụ: `1`, `2`, `5`...).
* **`interval_type`**: Đơn vị tính của chu kỳ: `minutes` (phút), `hours` (giờ), `days` (ngày), `weeks` (tuần), `months` (tháng).
    * *Ví dụ:* `interval_number = 1`, `interval_type = days` => Chạy mỗi ngày 1 lần.
* **`active`** (hoặc Evolve theo cách gọi trong video): Xác định trạng thái ban đầu của Scheduled Action.
    * `True`: Action sẽ tự động kích hoạt và bắt đầu chạy theo lịch trình ngay sau khi cài đặt.
    * `False` (hoặc `Eval="False"`): Action được tạo ra nhưng bị vô hiệu hóa (inactive - chữ màu xám trên giao diện). Bạn phải vào kích hoạt thủ công. Giảng viên chọn `False` để tiện demo việc "kích hoạt bằng tay" trên giao diện.



### 3. Cách thức hoạt động của Logic Code
Sau khi khai báo XML, Odoo cần biết cụ thể sẽ thực thi cái gì. Bạn phải viết logic xử lý vào trong file Python của model tương ứng.

* Trong hàm xử lý (ở đây là `update_showing_price`), Odoo sử dụng ORM để thực hiện các thao tác cơ sở dữ liệu.
* Lệnh `self.env['movie.showing'].search([])` với mảng rỗng `[]` (empty domain) mang ý nghĩa **lấy toàn bộ (fetch all)** các bản ghi đang có trong model đó.
* Sau đó, dùng vòng lặp `for` để đi qua từng bản ghi và cập nhật lại trường dữ liệu (ở đây là gán cứng `ticket_price = 10`).



### 4. Cách quản lý Scheduled Actions trên giao diện
Để kiểm tra, chỉnh sửa hoặc chạy thử (trigger) các Scheduled Actions trên giao diện Odoo:
1.  Bắt buộc phải bật **Chế độ nhà phát triển (Developer Mode)**.
2.  Truy cập menu **Settings (Cài đặt)** > **Technical (Kỹ thuật)** > **Scheduled Actions (Hành động theo lịch trình)**.
3.  Tại đây, bạn có thể xem lịch sử chạy, sửa lại khoảng thời gian, xem giờ chạy dự kiến tiếp theo (Next Execution Date) hoặc nhấn nút "Run Manually" (Chạy thủ công) để test code ngay lập tức mà không cần đợi đến giờ hẹn.

### 5. Code mẫu (Example Code)

Dưới đây là ví dụ hoàn chỉnh về cách triển khai một Scheduled Action để cập nhật giá vé và ghi log vào Chatter.

#### Bước 1: Khai báo trong file XML (ví dụ: `data/ir_cron_data.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Scheduled Action definition -->
        <record id="ir_cron_update_ticket_prices" model="ir.cron">
            <field name="name">Cinema: Update Ticket Prices Daily</field>
            <field name="model_id" ref="model_movie_showing"/>
            <field name="state">code</field>
            <field name="code">model._update_showing_price_cron()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="numbercall">-1</field>
            <field name="active" eval="True"/>
        </record>
    </data>
</odoo>
```

#### Bước 2: Triển khai logic trong file Python (ví dụ: `models/movie_showing.py`)

```python
from odoo import models, fields, api

class MovieShowing(models.Model):
    _name = 'movie.showing'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Include tracking and chatter

    ticket_price = fields.Float(string="Ticket Price", tracking=True)

    @api.model
    def _update_showing_price_cron(self):
        """
        Logic for the scheduled action to update ticket prices.
        This method will be called by the Odoo Cron system.
        """
        # 1. Fetch data that needs updating
        # In this example, we fetch all records
        showings = self.search([])
        
        # 2. Perform business logic
        # We update the ticket price and log a message to the Chatter
        for showing in showings:
            # Update the price
            showing.write({'ticket_price': 10.0})
            
            # Post a message to the chatter to provide context for the automated update
            showing.message_post(
                body="Hệ thống đã tự động cập nhật giá vé thông qua tác vụ Scheduled Action hàng ngày."
            )
```

**Một số lưu ý khi viết code:**
*   **`noupdate="1"`**: Thuộc tính này giúp ngăn chặn việc Odoo ghi đè lên các thay đổi mà người dùng đã thực hiện trực tiếp trên giao diện (như thay đổi giờ chạy) mỗi khi bạn cập nhật module.
*   **`@api.model`**: Hàm được gọi từ cron nên được đánh dấu là `@api.model` vì Odoo gọi nó từ môi trường chung của model mà không truyền vào danh sách ID cụ thể (no specific recordset).
*   **`mail.thread`**: Đừng quên kế thừa `mail.thread` để có thể sử dụng hàm `message_post()`.