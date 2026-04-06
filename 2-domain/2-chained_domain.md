# Chained Domain

## 1. Chained Domains là gì?
Trong Odoo ORM, **Chained Domain** (hay còn gọi là Dot Notation Domain) là một cú pháp cho phép bạn tìm kiếm dữ liệu dựa trên giá trị của các trường nằm ở một Model khác có quan hệ với Model hiện tại (qua các trường `Many2one`, `One2many` hoặc `Many2many`).

Thay vì phải viết code rườm rà: Lấy tất cả bản ghi -> Dùng hàm `mapped()` để trích xuất danh sách Model liên kết -> Dùng hàm `filtered()` để lọc. Chained Domain cho phép bạn đi xuyên qua các trường liên kết trực tiếp ngay trong mệnh đề `search()`. Cú pháp sử dụng là dấu chấm (`.`).

**Ví dụ trong bài giảng:**
Bài toán đặt ra là: Cập nhật giá vé (Ticket Price) cho các suất chiếu phim (Movie Showings). Nếu phim thuộc thể loại Khoa học viễn tưởng (Sci-fi) thì giá 12$, còn lại là 8$.

Cấu trúc quan hệ: `Movie Showing` chứa trường `movie_id` -> `Movie` chứa trường `category`.

* **Cách viết Chained Domain:**
    ```python
    sci_fi_showings = self.env['movie.showing'].search([
        ('movie_id.category', '=', 'sci_fi')
    ])
    ```
    Odoo sẽ tự động biên dịch cú pháp `movie_id.category` thành lệnh `JOIN` trong cơ sở dữ liệu để tìm ra các suất chiếu thỏa mãn điều kiện.

* **Cách viết gọn (Compact Write):**
    Odoo cho phép gọi hàm `write()` trực tiếp trên tập kết quả (Recordset) trả về từ hàm `search()` mà không cần gán vào biến trung gian:
    ```python
    self.env['movie.showing'].search([('movie_id.category', '=', 'sci_fi')]).write({'ticket_price': 12})
    ```

## 2. Thuộc tính `noupdate="1"` trong XML
Mỗi lần nâng cấp (upgrade) hoặc tải lại module, Odoo sẽ nạp lại file XML chứa cấu hình Scheduled Action. Điều này làm ghi đè trạng thái `active="False"` khiến Action bị tắt, dù trước đó người dùng đã bật lên bằng tay trên giao diện.

**Giải pháp:** Bọc thẻ `<record>` trong cặp thẻ `<data noupdate="1">`.
Thuộc tính này báo cho Odoo biết: Chỉ tạo mới bản ghi này vào database trong lần cài đặt (install) module đầu tiên. Trong các lần cập nhật (upgrade) module sau này, Odoo sẽ bỏ qua bản ghi này, giúp bảo toàn các thay đổi (như bật/tắt Action, sửa giờ chạy) mà người dùng đã thiết lập trên giao diện.

```xml
<odoo>
    <data noupdate="1">
        <record id="action_update_showing_price" model="ir.cron">
            </record>
    </data>
</odoo>
```

## 3. Cảnh báo về hiệu năng (Performance Best Practices)
Mặc dù Chained Domain viết rất ngắn gọn và tiện lợi, nhấn mạnh các quy tắc giới hạn để tránh làm hệ thống chậm đi (slow down):

1.  **Không đi quá sâu (Don't go beyond 2nd level):**
    Chỉ nên chấm tối đa 1 hoặc 2 mức (Ví dụ: `A.B.C` là mức 2). Không nên viết những domain quá dài như `('movie_id.theater_id.manager_id.name', '=', 'John')`. Mỗi dấu chấm sẽ tạo ra một phép `JOIN` trong database. Truy vấn SQL có quá nhiều `JOIN` sẽ tốn rất nhiều thời gian thực thi.
2.  **Giới hạn số lần thực hiện `search()`:**
    Nếu bài toán yêu cầu cập nhật giá cho quá nhiều thể loại khác nhau (Sci-fi giá 12, Comedy giá 10, Action giá 15, v.v.), việc dùng `search().write()` liên tục 3-4 lần cho cùng một model là không tốt (mỗi lần search là một lần chọc xuống database).

**Giải pháp thay thế khi logic phức tạp:**
Khi vượt qua các giới hạn trên, thay vì dùng Chained Domain, bạn nên quay lại phương pháp sử dụng hàm `mapped()`, vòng lặp `for` kết hợp `filtered()` trên bộ nhớ RAM của Python. Cách này gọi database 1 lần lấy toàn bộ dữ liệu lên, xử lý logic bằng Python, tuy tốn RAM nhưng sẽ tránh được tình trạng database bị quá tải do phải thực thi các truy vấn SQL phức tạp liên tục.