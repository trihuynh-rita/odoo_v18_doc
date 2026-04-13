### 1. Phân trang ở tầng ORM (Backend / API)
Dùng khi bạn cần viết hàm lấy dữ liệu trả về cho API hoặc xử lý logic nội bộ trong model.

```python
from odoo import models, api

class MyModel(models.Model):
    _name = 'my.model'

    @api.model
    def get_paginated_data(self, page=1, items_per_page=10):
        """
        Lấy dữ liệu có phân trang bằng ORM.
        """
        # Tính toán số lượng bản ghi cần bỏ qua
        offset_value = (page - 1) * items_per_page
        
        domain = [] # Điều kiện lọc dữ liệu (nếu có)
        
        # Tính tổng số bản ghi để tính tổng số trang
        total_records = self.search_count(domain)
        
        # Dùng search_read (hoặc search) kết hợp limit và offset
        records = self.search_read(
            domain=domain,
            fields=['name', 'description'], # Chỉ định các trường cần lấy để tối ưu
            limit=items_per_page,
            offset=offset_value,
            order='id desc'
        )
        
        return {
            'total_records': total_records,
            'total_pages': (total_records + items_per_page - 1) // items_per_page,
            'current_page': page,
            'data': records
        }
```

### 2. Phân trang ở tầng Controller (Website / Portal)
Dùng khi bạn tạo trang web tùy chỉnh (QWeb) và cần hiển thị thanh chuyển trang (Pager) trên giao diện người dùng.

**Trong file Controller:**
Odoo cung cấp sẵn hàm `request.website.pager` để tự động sinh ra cấu trúc dữ liệu cho thanh phân trang.

```python
from odoo import http
from odoo.http import request

class MyController(http.Controller):

    # Khai báo route nhận tham số <int:page> trên URL
    @http.route(['/my-data', '/my-data/page/<int:page>'], type='http', auth="public", website=True)
    def list_my_data(self, page=1, **kwargs):
        items_per_page = 12
        MyModel = request.env['my.model']
        domain = []

        # 1. Đếm tổng số lượng bản ghi
        total_count = MyModel.search_count(domain)

        # 2. Khởi tạo đối tượng Pager của Odoo
        pager = request.website.pager(
            url='/my-data',
            total=total_count,
            page=page,
            step=items_per_page,
            url_args=kwargs # Giữ nguyên các tham số query (ví dụ: ?search=abc) trên URL
        )

        # 3. Kéo dữ liệu dựa trên limit và offset được tính toán tự động từ pager
        records = MyModel.search(domain, limit=items_per_page, offset=pager['offset'])

        # 4. Truyền dữ liệu và biến pager ra view QWeb
        return request.render("my_module.my_data_template", {
            'records': records,
            'pager': pager,
        })
```

**Trong file View QWeb (XML):**
Để hiển thị thanh phân trang (nút 1, 2, 3, Trang sau, Trang trước), bạn chỉ cần gọi template `website.pager` mặc định.

```xml
<template id="my_data_template" name="My Data List">
    <t t-call="website.layout">
        <div class="container">
            
            <t t-foreach="records" t-as="record">
                <div class="row">
                    <span t-esc="record.name"/>
                </div>
            </t>
            
            <div class="d-flex justify-content-center mt-3">
                <t t-call="website.pager"/>
            </div>
            
        </div>
    </t>
</template>
```