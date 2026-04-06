# Các hàm thao tác Recordset (mapped, filtered, sorted)

Trong Odoo ORM, bộ ba hàm `mapped`, `filtered` và `sorted` là những công cụ mạnh mẽ nhất để thao tác dữ liệu trực tiếp trên RAM (in-memory) mà không cần truy vấn lại Database.

---

## 1. Phương thức `mapped()`

Hàm `mapped()` dùng để duyệt qua một Recordset và trả về một danh sách các giá trị hoặc một Recordset mới dựa trên trường hoặc hàm được truyền vào.

### 1.1. Cách hoạt động và Kiểu dữ liệu trả về
Kết quả trả về của `mapped()` thay đổi phụ thuộc vào loại dữ liệu của trường (field) được gọi:
* **Trường cơ bản (Char, Integer, Float, Date...):** Trả về một danh sách chuẩn của Python (`list`) chứa các giá trị.
* **Trường quan hệ (Many2one, One2many, Many2many):** Trả về một **Recordset mới**. Đặc tính quan trọng nhất ở đây là Odoo sẽ **tự động loại bỏ các bản ghi trùng lặp** (duplicate records) trong Recordset kết quả, giúp dữ liệu luôn là duy nhất (unique).

### 1.2. So sánh tối ưu hóa Code
Việc sử dụng `mapped()` giúp mã nguồn ngắn gọn, dễ đọc và tối ưu hiệu suất truy vấn hơn so với việc tự viết vòng lặp `for` truyền thống.

**Cách dùng vòng lặp `for` (Cồng kềnh):**
```python
partners = self.env['res.partner']
for order in sale_orders:
    # Toán tử |= dùng để gộp các bản ghi vào Recordset và tự lọc trùng
    partners |= order.partner_id 
```

**Cách dùng `mapped()` (Tối ưu):**
```python
partners = sale_orders.mapped('partner_id')
```

### 1.3. Kỹ thuật duyệt sâu bằng Dot Notation (Dấu chấm)
Sức mạnh lớn nhất của `mapped()` là khả năng truy xuất chéo qua nhiều bảng dữ liệu có quan hệ với nhau chỉ bằng dấu chấm `.`. Odoo ORM sẽ tự động xử lý các luồng truy vấn ngầm một cách an toàn.

*Ví dụ: Từ danh sách đơn hàng (`sale_orders`), lấy danh sách "Tên quốc gia" của tất cả các khách hàng đã mua hàng:*
```python
country_names = sale_orders.mapped('partner_id.country_id.name')
# Kết quả trả về là một list: ['Việt Nam', 'Hoa Kỳ', 'Nhật Bản']
```

### 1.4. Truyền hàm tính toán (Callable)
Thay vì truyền tên trường dưới dạng chuỗi (string), có thể truyền một hàm Python để thực hiện logic tính toán động trên từng bản ghi.

*Ví dụ: Tính giá trị chiết khấu 10% cho từng đơn hàng:*
```python
discounts = sale_orders.mapped(lambda record: record.amount_total * 0.1)
```

---

## 2. Phương thức `filtered()`

Hàm `filtered()` dùng để lọc các bản ghi trong một Recordset dựa trên một điều kiện nhất định.

### 2.1. Bản chất hoạt động
* **Xử lý in-memory:** `filtered()` duyệt qua từng bản ghi trong Recordset hiện tại. Nếu bản ghi đó thỏa mãn điều kiện (trả về `True`), nó sẽ được giữ lại.
* **Tính bất biến (Immutable):** Nó không làm thay đổi Recordset gốc mà sẽ trả về một **Recordset mới** chứa các bản ghi đã vượt qua bộ lọc.

### 2.2. Hai cách sử dụng chính

**Cách 1: Truyền một hàm tùy chỉnh (Dùng Lambda - Phổ biến nhất)**
Đây là cách linh hoạt nhất. Anh truyền vào một hàm Python (thường là `lambda`), hàm này nhận đầu vào là một bản ghi (record) và phải trả về `True` hoặc `False`.

```python
# Từ danh sách hóa đơn đang có, lọc ra những hóa đơn có trạng thái là 'đã thanh toán' (paid)
paid_invoices = invoices.filtered(lambda r: r.state == 'paid')

# Lọc với điều kiện phức tạp: Đơn hàng lớn hơn 1 triệu VÀ của khách VIP
vip_big_orders = sale_orders.filtered(lambda r: r.amount_total > 1000000 and r.partner_id.is_vip)
```

**Cách 2: Truyền trực tiếp tên trường (Dạng String - Ngắn gọn)**
Nếu anh chỉ muốn lọc các bản ghi mà một trường cụ thể có giá trị là `True` (đối với trường Boolean) hoặc có chứa dữ liệu (đối với các trường khác, không bị rỗng/False), anh chỉ cần truyền tên trường đó dưới dạng chuỗi.

```python
# Giả sử partner.is_company là trường Boolean (Đánh dấu là công ty)
# Thay vì viết: partners.filtered(lambda r: r.is_company == True)
# Cách tối ưu với Odoo:
companies = partners.filtered('is_company')

# Lọc ra những khách hàng ĐÃ CÓ nhập số điện thoại (trường phone không bị rỗng)
has_phone_partners = partners.filtered('phone')
```

### 2.3. Khi nào NÊN và KHÔNG NÊN dùng? (Tối ưu hiệu năng)
Để hệ thống chạy mượt mà, không bị tràn RAM, việc phân định ranh giới giữa `search()` và `filtered()` là cực kỳ quan trọng:

* **NÊN DÙNG `filtered()`:** Khi anh làm việc với các trường quan hệ như `One2many` hoặc `Many2many` của một bản ghi đã được load lên.
    * *Ví dụ:* Đang xem thông tin 1 Khách hàng, muốn lọc ra các địa chỉ giao hàng của họ (nằm trong trường `child_ids`).
* **KHÔNG NÊN DÙNG `filtered()`:** Khi muốn tìm kiếm dữ liệu trên toàn hệ thống từ Database.
    * *Sai (Load toàn bộ bảng vào RAM rồi mới lọc):*
      `self.env['sale.order'].search([]).filtered(lambda r: r.state == 'draft')`
    * *Đúng (Đẩy việc lọc xuống tầng Database xử lý bằng SQL thông qua Domain):*
      `self.env['sale.order'].search([('state', '=', 'draft')])`

---

## 3. Phương thức `sorted()`

Hàm `sorted()` dùng để sắp xếp các bản ghi trong một Recordset.

### 3.1. Bản chất hoạt động
* **Xử lý trên RAM (In-memory):** `sorted()` không tạo ra câu lệnh truy vấn SQL xuống PostgreSQL. Nó lấy Recordset hiện tại đang có trên RAM và sắp xếp nó bằng Python.
* **Tính bất biến (Immutable):** Giống như `mapped()` hay `filtered()`, hàm này không làm thay đổi Recordset gốc mà sẽ **trả về một Recordset mới** đã được sắp xếp theo đúng thứ tự anh muốn.

### 3.2. Bốn cách sử dụng `sorted()` phổ biến

**Cách 1: Sắp xếp mặc định (Không truyền tham số)**
Nếu gọi `records.sorted()`, Odoo sẽ tự động sắp xếp Recordset dựa trên thuộc tính `_order` mà anh đã định nghĩa trong Class.
```python
# Tự động sắp xếp theo cấu hình _order của model
sorted_records = sale_orders.sorted()
```

**Cách 2: Sắp xếp theo một trường cụ thể (Dạng String)**
Anh có thể truyền trực tiếp tên trường (field) vào tham số `key` để yêu cầu Odoo sắp xếp theo trường đó.
```python
# Sắp xếp các đơn hàng theo tổng tiền (tăng dần)
sorted_by_amount = sale_orders.sorted('amount_total')
```

**Cách 3: Sắp xếp đảo chiều (Giảm dần)**
Sử dụng tham số `reverse=True`.
```python
# Sắp xếp đơn hàng theo ngày tạo mới nhất lên đầu
latest_orders = sale_orders.sorted('create_date', reverse=True)
```

**Cách 4: Sắp xếp bằng hàm tùy chỉnh (Dùng Lambda)**
```python
# Sắp xếp đơn hàng dựa trên lợi nhuận (Doanh thu - Chi phí)
sorted_by_profit = sale_orders.sorted(key=lambda r: r.amount_total - r.cost_price, reverse=True)
```

### 3.3. Lưu ý "sống còn" về Hiệu năng (Performance)
* **NÊN DÙNG:** Khi anh đã có sẵn một Recordset (ví dụ: từ trường `One2many` hoặc sau khi dùng `.filtered()`).
* **KHÔNG NÊN DÙNG:** Nếu anh đang gọi dữ liệu từ Database lên *chỉ để sắp xếp*. Hãy dùng tham số `order` của hàm `search()`. 
    * **Sai:** `self.env['sale.order'].search([]).sorted('create_date')`
    * **Đúng:** `self.env['sale.order'].search([], order='create_date asc')`

---

**Tài liệu tham khảo:**
* *Odoo Official Documentation: ORM API - Recordsets.*
* *Odoo Source Code: `odoo/models.py` (BaseModel).*
