from odoo import api, fields, models 

class SaleOrderLine(models.Model): 
    _name = 'sale.order.line' 
    
    product_id = fields.Many2one('product.template') 
    qty = fields.Float(string='Số lượng', default=1.0) 
    price_unit = fields.Float(string='Đơn giá') 

    '''
    store=True → lưu DB, tìm kiếm & group by được, 
    tốn storage # store=False (mặc định) → tính real-time, không lưu DB 
    '''
    price_subtotal = fields.Monetary( 
        string='Thành tiền',
        compute='_compute_price_subtotal', 
        store=True, 
        currency_field='currency_id', 
        aggregator='sum', # Odoo 17+: tự động sum khi group by 
        precompute=True, # tính ngay khi INSERT, không chờ flush 
    ) 
    
    @api.depends('qty', 'price_unit') 
    def _compute_price_subtotal(self): 
        for line in self: 
            line.price_subtotal = line.qty * line.price_unit 
            # inverse: cho phép user nhập vào computed field
    
    display_name = fields.Char( 
        compute='_compute_display_name', 
        inverse='_inverse_display_name', 
        store=False, 
    ) 
    
    @api.depends('product_id.name', 'qty') 
    def _compute_display_name(self): 
        for line in self: 
            line.display_name = f"{line.product_id.name} x {line.qty}" 
            
    def _inverse_display_name(self): 
        pass # parse ngược nếu cần 
        
    # related: shortcut lấy field từ model liên quan 
    partner_id = fields.Many2one( 
        related='order_id.partner_id', 
        store=True, # store=True để search/filter được 
        readonly=True, 
    ) 
    
    currency_id = fields.Many2one( 
        related='order_id.currency_id', 
        store=True, 
    )