# Xử lý Ngày tháng và Múi giờ trong Odoo 18 (Date & Timezone)

Tài liệu này tổng hợp các kỹ thuật xử lý dữ liệu thời gian trong Odoo 18, từ việc cấu hình bộ lọc trên giao diện (XML) đến xử lý logic múi giờ chuyên sâu trong Backend (Python).

---

## 1. Lọc dữ liệu "Hôm nay" trong Search View (XML)

Khi tạo bộ lọc (filter) cho các trường `Datetime` trong file XML, chúng ta cần xử lý hai vấn đề: kiểu dữ liệu khác nhau và quy tắc mã hóa XML.

### 1.1. Khác biệt giữa Python và XML
*   **Trong Python:** Dùng `fields.Date.today()`.
*   **Trong XML View:** Odoo không hiểu hàm Python. Bạn phải dùng hàm `context_today()`. Hàm này tự động lấy ngày hiện tại theo múi giờ (timezone) của người dùng.

### 1.2. Xử lý khoảng thời gian (Datetime Range)
Trường `Datetime` bao gồm cả giờ-phút-giây. Để lọc chính xác "Ngày hôm nay", bạn phải tạo một khoảng từ **00:00:00** đến **23:59:59**.

### 1.3. Mã hóa ký tự đặc biệt (XML Escaping)
Vì XML sử dụng `<` và `>` để đóng mở thẻ, bạn phải dùng mã hóa thực thể:
*   `>=` viết thành `&gt;=`
*   `<=` viết thành `&lt;=`

> [!TIP]
> **Cấu trúc bộ lọc chuẩn trong XML:**
> ```xml
> <filter string="Hôm nay" name="today" domain="[
>     ('date_start', '&gt;=', context_today().strftime('%Y-%m-%d 00:00:00')),
>     ('date_start', '&lt;=', context_today().strftime('%Y-%m-%d 23:59:59'))
 > ]"/>
> ```

---

## 2. Kiến trúc Múi giờ trong Odoo

Hiểu luồng dữ liệu giúp tránh các lỗi lệch giờ (thường là lệch 7 tiếng tại Việt Nam).

| Thành phần | Đặc điểm | Trạng thái |
| :--- | :--- | :--- |
| **PostgreSQL** | Luôn lưu trữ ở dạng **UTC** | `timestamp without time zone` |
| **Odoo Server** | Xử lý logic nghiệp vụ | Naive UTC (Không chứa thông tin TZ) |
| **Browser (Client)** | Hiển thị cho người dùng | Tự động chuyển đổi UTC → Timezone của User |

> [!IMPORTANT]
> **Quy tắc vàng:** ORM Python luôn làm việc với UTC. Việc chuyển đổi múi giờ chỉ nên xảy ra ở tầng hiển thị (Browser) hoặc khi cần in Report/Log.

---

## 3. Các hàm cốt lõi xử lý Timezone (Odoo 18)

| Hàm | Kết quả trả về | Trường hợp sử dụng |
| :--- | :--- | :--- |
| `fields.Date.context_today(record)` | `date` (TZ Client) | Giá trị mặc định, Domain filter |
| `fields.Datetime.context_timestamp(record, dt)` | `datetime aware` (TZ Client) | Hiển thị giờ địa phương trong Report/Log |
| `fields.Datetime.now()` | `datetime` (UTC naive) | Gán timestamp hiện tại vào DB |
| `date_utils.start_of(dt, 'day')` | `datetime` (UTC 00:00) | Lấy điểm bắt đầu của ngày/tuần/tháng |
| `date_utils.end_of(dt, 'day')` | `datetime` (UTC 23:59) | Lấy điểm kết thúc của chu kỳ |

---

## 4. Pattern xử lý đúng trong Python (Backend)

### 4.1. Lọc "Hôm nay" chuẩn Timezone User
Nếu chỉ dùng `strftime('00:00:00')` mà không tính đến múi giờ, kết quả sẽ bị lệch. Dưới đây là cách xử lý an toàn:

```python
import pytz
from datetime import datetime
from odoo import fields
from odoo.tools import date_utils

def _get_today_domain(self):
    # 1. Xác định múi giờ User hoặc mặc định UTC
    user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
    
    # 2. Lấy thời điểm hiện tại và localize sang múi giờ User
    now_utc = pytz.utc.localize(datetime.utcnow())
    now_local = now_utc.astimezone(user_tz)
    
    # 3. Tính toán biên đầu/cuối ngày tại địa phương
    start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = now_local.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # 4. Convert ngược về UTC để so sánh với Database
    start_utc = start_local.astimezone(pytz.utc).replace(tzinfo=None)
    end_utc = end_local.astimezone(pytz.utc).replace(tzinfo=None)
    
    return [('date_start', '>=', start_utc), ('date_start', '<=', end_utc)]
```

---

## 5. Xử lý trong các ngữ cảnh đặc thù

### 5.1. Scheduled Action (Cron)
Cron chạy dưới quyền `OdooBot` nên `env.user.tz` thường rỗng.
**Giải pháp:** Sử dụng múi giờ của Công ty (`self.env.company.partner_id.tz`) làm mốc tham chiếu.

### 5.2. Hiển thị giờ cục bộ trong Chatter/Log
Sử dụng `context_timestamp` để chuyển đổi từ UTC sang múi giờ người dùng trước khi định dạng chuỗi:
```python
local_dt = fields.Datetime.context_timestamp(self, self.date_start)
display_time = local_dt.strftime('%d/%m/%Y %H:%M')
```

### 5.3. API / XML-RPC bên ngoài
**Nguyên tắc:** Luôn gửi dữ liệu dạng **UTC String**. Hệ thống API không tự động chuyển đổi múi giờ cho bạn.

---

## 6. Các "Bẫy" thường gặp và Cách tránh

| Tình huống | Sai lầm | Cách làm đúng |
| :--- | :--- | :--- |
| **Default Value** | `default=datetime.now()` (Lấy giờ server) | `default=fields.Datetime.now` (Luôn là UTC) |
| **Domain XML** | Dùng `datetime.now()` | Dùng `context_today().strftime(...)` |
| **So sánh DB** | So sánh giờ Local với trường trong DB | Luôn convert giờ Local sang UTC trước khi so sánh |
| **API Integration** | Gửi giờ địa phương lên API | Convert sang UTC chuẩn ISO trước khi gọi API |

---
**Tài liệu tham khảo:**
* Odoo 18 ORM API - Date/Time handling.
* Python `pytz` and `datetime` libraries.
