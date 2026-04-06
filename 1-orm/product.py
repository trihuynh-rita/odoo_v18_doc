from odoo import fields, models

class ProductTemplate(models.Model):
    _name = 'product.template'
    _description = 'Sản phẩm'

    # Char: size giới hạn độ dài, required bắt buộc, index tăng tốc search
    name = fields.Char(
        string='Tên sản phẩm',
        size=256,
        required=True,
        index='btree',
        translate=True,
    )

    # Float: digits=(tổng chữ số, số thập phân)
    weight = fields.Float(
        string='Trọng lượng (kg)',
        digits=(10, 3),
        default=0.0,
        help='Trọng lượng tịnh của sản phẩm',
    )

    # Monetary: phải khai báo currency_field tương ứng
    list_price = fields.Monetary(
        string='Giá bán',
        currency_field='currency_id',
        required=True,
        default=0.0,
    )
    currency_id = fields.Many2one('res.currency')

    # Selection: danh sách cố định, default chỉ định giá trị ban đầu
    state = fields.Selection(
        selection=[
            ('draft', 'Nháp'),
            ('active', 'Đang bán'),
            ('archived', 'Ngưng bán'),
        ],
        string='Trạng thái',
        default='draft',
        required=True,
    )

    # Boolean: active=True là convention để archive record
    active = fields.Boolean(default=True)
    is_featured = fields.Boolean(
        string='Sản phẩm nổi bật',
        copy=False,  # không copy khi duplicate
    )

    # Image: max_width/max_height tự động resize khi upload
    image_1920 = fields.Image(max_width=1920, max_height=1920)
    image_128 = fields.Image(
        related='image_1920',
        max_width=128,
        max_height=128,
        store=True,
    )