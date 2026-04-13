# Hướng dẫn cách tạo Controller, xây dựng API và cách gọi API trong Odoo.

### 1. Cấu trúc thư mục cho Controller

Để tạo Controller trong Odoo, bạn cần tuân thủ cấu trúc thư mục tiêu chuẩn:

1.  **Tạo thư mục `controllers`:** Thư mục này nằm ngang hàng với `models`, `views`, v.v. trong module của bạn.
2.  **Tạo file Python (ví dụ: `main.py`):** Bên trong thư mục `controllers`, tạo file để chứa code logic của Controller.
3.  **Khai báo trong `__init__.py`:**
    * Trong thư mục `controllers`, tạo file `__init__.py` và import file vừa tạo: `from . import main`
    * Trong file `__init__.py` ở thư mục gốc của module, import thư mục controllers: `from . import controllers`

### 2. Định nghĩa Controller và API Endpoint

Trong file `main.py`, bạn thực hiện các bước sau để định nghĩa một API:

**Bước 1: Import thư viện cần thiết**

```python
from odoo import http
from odoo.http import request
import json
```

**Bước 2: Khai báo class Controller**

Class này phải kế thừa từ `http.Controller`.

```python
class CinemaManagerController(http.Controller):
    # Các hàm xử lý API sẽ được định nghĩa ở đây
```

**Bước 3: Định nghĩa Route (Endpoint) bằng Decorator `@http.route`**

Sử dụng `@http.route` trước hàm xử lý để định nghĩa đường dẫn và các cấu hình cho API.

```python
    @http.route(['/cinema/showings', '/cinema/showings/<string:category>'], type='http', auth='public', methods=['GET'], csrf=False)
    def fetch_movie_showings(self, category=None, **kwargs):
        # ... logic xử lý ...
```

**Các tham số quan trọng trong `@http.route`:**
* **Đường dẫn (Path):** Có thể truyền một danh sách các đường dẫn. Ví dụ trên hỗ trợ cả `/cinema/showings` và `/cinema/showings/category_name`. Biến truyền trên URL được định nghĩa dạng `<type:variable_name>` (ví dụ: `<string:category>`).
* **`type`:** Kiểu request, thường là `'http'` (trả về HTML, chuỗi, hoặc JSON tự format) hoặc `'json'` (trả về JSON chuẩn). Video sử dụng `'http'`.
* **`auth`:** Cấp độ xác thực.
    * `'public'`: Ai cũng truy cập được, có lưu session.
    * `'user'`: Yêu cầu phải đăng nhập.
    * `'none'`: Không xác thực, không session (ít dùng).
* **`methods`:** Danh sách các HTTP method được phép (ví dụ: `['GET']`, `['POST']`). Mặc định nếu không khai báo là POST.
* **`csrf=False`:** (Quan trọng cho POST request từ bên ngoài) Tắt kiểm tra Cross-Site Request Forgery token để cho phép gọi API từ ứng dụng khác không phải Odoo.

### 3. Xử lý Logic trong Hàm Controller

Bên trong hàm xử lý, bạn truy xuất dữ liệu thông qua đối tượng `request.env` (không dùng `self.env` như trong models).

```python
    @http.route(['/cinema/showings', '/cinema/showings/<string:category>'], type='http', auth='public', methods=['GET'], csrf=False)
    def fetch_movie_showings(self, category=None, **kwargs):
        # 1. Truy vấn dữ liệu qua request.env
        # Dùng .sudo() để lấy toàn bộ dữ liệu (nếu cần bỏ qua phân quyền)
        domain = []
        if category:
            domain.append(('movie_id.category', '=', category))
            
        showings = request.env['movie.showing'].sudo().search(domain)

        # 2. Định dạng dữ liệu trả về (dạng danh sách Dictionary)
        showings_data = []
        for showing in showings:
            showings_data.append({
                'movie': showing.movie_id.name,
                # ... các trường khác ...
            })

        # 3. Chuyển đổi sang JSON string
        response_json = json.dumps(showings_data)

        # 4. Trả về Response
        return request.make_response(
            response_json,
            headers=[('Content-Type', 'application/json')] # Khuyên dùng thêm header này
        )
```

**Lưu ý quan trọng:**
* Tham số từ URL (ví dụ: `category`) phải được khai báo với giá trị mặc định (`category=None`) trong hàm để tránh lỗi thiếu tham số khi gọi endpoint cơ bản (không có tham số).
* Các tham số truyền qua Body hoặc Query String (khi gọi POST) sẽ nằm trong `**kwargs`.
* Vì trả về dữ liệu kiểu `type='http'`, bạn phải tự format dữ liệu thành chuỗi JSON bằng `json.dumps()` trước khi trả về, không được trả về list/dictionary trực tiếp. Hàm `request.make_response()` giúp thiết lập nội dung và headers cho HTTP response.

### 4. Cách Gọi API (Testing)

Bạn có thể dùng công cụ như **Postman** hoặc trình duyệt (đối với GET request) để kiểm tra API.

* **Gọi GET không tham số:**
    * URL: `http://localhost:8069/cinema/showings`
* **Gọi GET có tham số trên URL:**
    * URL: `http://localhost:8069/cinema/showings/comedy` (Trả về danh sách các suất chiếu phim hài).

### 5. Sự khác nhau của HTTP và Json
Sự khác biệt cốt lõi giữa `type='http'` và `type='json'` trong Odoo nằm ở **chuẩn giao tiếp** và **cách Odoo tự động xử lý dữ liệu** (cả đầu vào lẫn đầu ra).

### 1. Bảng so sánh tổng quan

| Tiêu chí | `type='http'` (Standard HTTP) | `type='json'` (JSON-RPC) |
| :--- | :--- | :--- |
| **Mục đích chính** | Phục vụ trang web (HTML), tải file, hoặc làm REST API tự chế. | Gọi hàm từ xa (RPC) chuyên dụng cho Web Client của Odoo. |
| **HTTP Method hỗ trợ** | Cả `GET` và `POST`. | **Chỉ hỗ trợ `POST`**. |
| **Cách truyền tham số (Input)** | Dùng Query String trên URL (GET) hoặc Form-data (POST). | Gửi cục JSON trong Body, **bắt buộc** phải bọc trong object `{"params": {...}}`. |
| **Xử lý dữ liệu trả về (Output)**| Trả về tự do. Phải tự convert sang chuỗi (dùng `json.dumps`) và dùng `request.make_response()`. | Trả về thẳng Dictionary/List của Python. Odoo tự động ép kiểu sang JSON. |
| **Cấu trúc Response** | Do bạn tự quyết định 100%. | Bị Odoo bọc lại theo chuẩn JSON-RPC: `{"jsonrpc": "2.0", "result": { ...dữ liệu của bạn... }}`. |

---

### 2. Chi tiết về `type='http'` (Như trong video bạn vừa xem)


Đây là dạng "thuần túy" nhất. Khi bạn tạo API kiểu này, Odoo cho phép bạn kiểm soát hoàn toàn request và response.
* **Khi nào nên dùng:** Khi bạn muốn tự xây dựng một hệ thống **RESTful API chuẩn** để giao tiếp với các hệ thống bên ngoài.
* **Lợi thế khi làm App:** Khi tích hợp với các ứng dụng mobile (như lúc code bằng Flutter hay React Native), dùng `type='http'` sẽ giúp bạn dễ dùng các thư viện chuẩn (như `dio` hay `http`) hơn vì bạn tự do định nghĩa body và response theo đúng ý mình.

---

### 3. Chi tiết về `type='json'` (Đặc sản của Odoo)


Odoo thiết kế `type='json'` để tuân thủ chặt chẽ giao thức **JSON-RPC 2.0**. Nó tự động hóa việc parse dữ liệu nhưng lại cực kỳ khắt khe về format.

**Cái khó chịu nhất (Input Format):**
Nếu bạn dùng Postman bắn API vào một endpoint `type='json'`, bạn không thể gửi một file JSON bình thường như vầy:
```json
{
  "category": "comedy",
  "limit": 10
}
```
**Odoo sẽ báo lỗi ngay lập tức.** Bạn **bắt buộc** phải bọc dữ liệu vào một key tên là `params`:
```json
{
  "jsonrpc": "2.0",
  "params": {
    "category": "comedy",
    "limit": 10
  }
}
```

**Sự tiện lợi (Output Format):**
Trong code Python, bạn không cần dùng `json.dumps()` hay `request.make_response()`. Chỉ cần `return {'status': 'success', 'data': showings}`.
Tuy nhiên, khi trả về app, dữ liệu sẽ tự động bị bọc lại:
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "status": "success",
    "data": [...]
  }
}
```
Lúc này, ở code frontend (Figma UI/Flutter), bạn luôn phải parse thêm một tầng `.result` thì mới lấy được data thật.

---

### 6. Cách triển khai JSON Controller và chuẩn JSON-RPC (Odoo 18/19 Standard)

Phần này hướng dẫn cách xây dựng một JSON endpoint để giao tiếp với các ứng dụng bên ngoài (như React, Flutter, hoặc Postman) thông qua giao thức JSON-RPC 2.0 của Odoo.

#### 1. Ví dụ khai báo Controller
Để tạo một JSON endpoint tìm kiếm rạp phim, bạn sử dụng cấu hình sau trong controller:

```python
from odoo import http
from odoo.http import request

class CinemaJsonController(http.Controller):

    @http.route('/cinema/movie_theaters', type='json', auth='public', methods=['POST'], csrf=False)
    def get_movie_theaters(self, is_vip=False, **kwargs):
        """
        Fetch movie theaters based on VIP status.
        :param is_vip: Boolean to filter VIP theaters
        :return: List of theater data (dictionary)
        """
        # Use .sudo() to bypass record rules and access all relevant data
        domain = []
        if is_vip:
            domain.append(('is_vip', '=', True))
            
        theaters = request.env['movie.theater'].sudo().search(domain)
        
        # Prepare response data as a list of dictionaries
        # Odoo automatically converts this to a JSON-RPC response
        result = []
        for theater in theaters:
            result.append({
                'id': theater.id,
                'name': theater.name,
                'is_vip': theater.is_vip,
                'location': theater.location_id.display_name if theater.location_id else 'N/A'
            })
            
        return result
```

#### 2. Cách gọi API bằng JSON-RPC (Postman)
Khi gọi một endpoint kiểu `type='json'` từ bên ngoài, bạn **bắt buộc** phải bọc các tham số vào một "lớp vỏ" JSON-RPC. Các request JSON thông thường sẽ bị Odoo từ chối.

**Đường dẫn API:** `http://localhost:8069/cinema/movie_theaters`
**Phương thức:** `POST`
**Headers:** `Content-Type: application/json`

**Cấu trúc Body (Raw JSON):**
```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "is_vip": true
    }
}
```

#### 3. Các lưu ý kỹ thuật quan trọng
*   **Xử lý bất đồng bộ (Background Processing):** JSON endpoint cực kỳ phù hợp cho việc cập nhật giao diện web/app mà không cần tải lại trang.
*   **Phương thức hỗ trợ:** Dù route `type='json'` cho phép khai báo method, nhưng về bản chất nó được thiết kế cho các request `POST` chứa payload JSON-RPC.
*   **Bảo vệ dữ liệu (sudo):** Việc gọi `.sudo()` trong controller thường được dùng khi endpoint cần cung cấp dữ liệu cho người dùng vãng lai hoặc hệ thống bên ngoài mà không bị giới hạn bởi Record Rules nội bộ.
*   **Tự động chuyển đổi dữ liệu:** Khác với `type='http'`, bạn không cần dùng `json.dumps()`. Odoo sẽ tự động chuyển đổi Dictionary/List từ Python sang JSON response.
*   **Cấu trúc kết quả trả về:** Dữ liệu thật sẽ nằm bên trong khóa `result` của JSON nhận được (ví dụ: `{"jsonrpc": "2.0", "result": [...]}`).


