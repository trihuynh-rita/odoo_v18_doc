from odoo import models, fields

class SaleOrder(models.Model):
    _name = 'sale.order'
    _description = 'Đơn bán hàng'

    # Many2one: ondelete='restrict' ngăn xóa partner nếu còn đơn hàng
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Khách hàng',
        required=True,
        ondelete='restrict',  # ondelete quan trọng: 'restrict' bảo vệ dữ liệu, 'cascade' cho child records, 'set null'
        index='btree_not_null',
        check_company=True,
        domain=[('customer_rank', '>', 0)],  # chỉ hiện khách hàng
    )

    # Many2one với context: truyền giá trị mặc định khi tạo mới từ field
    pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Bảng giá',
        context={'active_test': False},
    )

    # One2many: inverse_name phải là tên M2o trỏ ngược về model này
    order_line = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string='Chi tiết đơn hàng',
        copy=True,
    )

    # Many2many: tự tạo bảng trung gian, hoặc khai báo tường minh
    tag_ids = fields.Many2many(
        comodel_name='crm.tag',
        relation='sale_order_tag_rel',  # tên bảng trung gian
        column1='order_id',
        column2='tag_id',
        string='Nhãn',
    )


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _description = 'Chi tiết đơn hàng'

    # Many2one trỏ ngược lên đơn hàng: cascade = tự xóa line khi xóa order
    order_id = fields.Many2one(
        'sale.order',
        ondelete='cascade',
        required=True,
        index=True,
    )
    product_id = fields.Many2one('product.product')
    qty = fields.Float(string='Số lượng', default=1.0)
    price_unit = fields.Float(string='Đơn giá')