odoo-addons/                    ← git repo
├── hrm_mvp/
│   ├── __manifest__.py
│   ├── __init__.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mixins/
│   │   │   ├── __init__.py
│   │   │   └── timestamp_mixin.py
│   │   ├── res_partner_ext.py
│   │   └── sale_order_ext.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── serializers.py
│   │
│   ├── services/              ← business logic thuần Python, không kế thừa models
│   │   ├── __init__.py
│   │   ├── order_service.py
│   │   └── notification_service.py
│   │
│   ├── wizards/
│   │   ├── __init__.py
│   │   ├── import_wizard.py
│   │   └── import_wizard_view.xml
│   │
│   ├── views/
│   │   ├── form_views.xml
│   │   ├── list_views.xml
│   │   ├── menu_items.xml
│   │   └── report_templates.xml
│   │
│   ├── security/
│   │   ├── ir.model.access.csv
│   │   ├── groups.xml
│   │   └── rules.xml
│   │
│   ├── data/
│   │   ├── default_data.xml
│   │   ├── sequences.xml
│   │   └── mail_templates.xml
│   │
│   ├── static/
│   │   └── src/
│   │       ├── js/
│   │       └── scss/
│   │
│   ├── migrations/
│   │   └── 16.0.1.1.0/
│   │       ├── pre-migrate.py
│   │       └── post-migrate.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── common.py
│       ├── test_models.py
│       └── test_controllers.py
│
├── shared/                    ← code dùng chung giữa các addon
│   ├── __init__.py
│   └── base_utils.py
│
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml             ← ruff, isort config
├── Makefile
├── .pre-commit-config.yaml
└── .github/
    └── workflows/
        └── ci.yml