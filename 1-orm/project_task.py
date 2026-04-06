from odoo import fields, models

class ProjectTask(models.Model):
    _name = 'project.task'
    _description = 'Dự án'

    # Json: lưu dict/list tự do, không cần thêm cột DB mới
    extra_data = fields.Json(
        string='Dữ liệu bổ sung',
        default=dict,
        copy=False,
    )

    # Properties: dynamic fields — user tự định nghĩa thêm field trên UI
    task_properties = fields.Properties(
        definition='task_properties_definition',
        copy=True,
    )

    # PropertiesDefinition lưu schema của Properties bên trên
    task_properties_definition = fields.PropertiesDefinition(
        string='Cấu hình thuộc tính task',
    )

    # groups: chỉ manager mới thấy field này
    internal_note = fields.Text(
        string='Ghi chú nội bộ',
        groups='project.group_project_manager',
    )

    # index='trigram': full-text search nhanh với LIKE/ilike
    description = fields.Char(
        string='Mô tả',
        index='trigram',  # cần pg_trgm extension trong PostgreSQL
    )

    # Hạn chót
    deadline = fields.Date(string='Hạn chót')

    # deprecated: cảnh báo field lỗi thời, vẫn giữ để backward compat
    legacy_code = fields.Char(
        deprecated='Dùng reference_code thay thế từ v18',
    )
    reference_code = fields.Char(string='Mã tham chiếu')

    # Serialized: nhiều field nhỏ gộp vào 1 cột JSON (tiết kiệm cột DB)
    config_data = fields.Serialized(
        string='Cấu hình',
        default=dict,
    )