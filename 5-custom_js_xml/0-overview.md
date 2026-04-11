# Custom JavaScript & XML cho Odoo v18 - Hướng Dẫn Toàn Diện

## 📋 Mục Lục
1. [Khái Quát](#khái-quát)
2. [Kiến Trúc](#kiến-trúc)
3. [Công Cụ & Dependencies](#công-cụ--dependencies)
4. [Quy Trình Phát Triển](#quy-trình-phát-triển)
5. [Best Practices](#best-practices)

---

## Khái Quát

Odoo v18 sử dụng **OWL Framework** (Object Web Library) để xây dựng giao diện người dùng. Để custom Odoo v18, bạn cần hiểu:

### Hai Thành Phần Chính:
1. **JavaScript (OWL Components)** - Logic và tương tác
2. **XML Templates (OWL Syntax)** - Cấu trúc HTML với templating

### Các Loại Customization:
```
┌─────────────────────────────────────────┐
│     Odoo v18 Customization Layers       │
├─────────────────────────────────────────┤
│ 1. Custom Components (new)              │
│    - Hoàn toàn mới từ OWL Component    │
│                                          │
│ 2. Custom Fields (new)                  │
│    - Field widgets cho specific types   │
│                                          │
│ 3. Custom Views (new)                   │
│    - List, Form, Kanban, Graph, etc    │
│                                          │
│ 4. Patching Existing Components         │
│    - Patch Core Odoo components         │
│                                          │
│ 5. Template Inheritance                 │
│    - t-inherit trên existing templates  │
└─────────────────────────────────────────┘
```

---

## Kiến Trúc

### File Structure
```
custom_addons/your_module/
├── static/
│   └── src/
│       ├── js/
│       │   ├── component1.js
│       │   ├── component2.js
│       │   └── patches.js
│       ├── xml/
│       │   ├── template1.xml
│       │   ├── template2.xml
│       │   └── patches.xml
│       └── scss/ (optional)
├── __manifest__.py
└── __init__.py
```

### Module Manifest Registration
```python
# __manifest__.py
{
    'name': 'My Module',
    'version': '18.0.1.0.0',
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/js/**/*.js',
            'my_module/static/src/xml/**/*.xml',
            'my_module/static/src/scss/**/*.scss',
        ],
    },
}
```

---

## Công Cụ & Dependencies

### Core Imports
```javascript
// Framework & Components
import { Component, useState, onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";

// Services
import { useService } from "@web/core/utils/hooks";

// UI Components
import { Dropdown, DropdownItem } from "@web/core/dropdown/dropdown";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

// Views
import { ListRenderer } from "@web/views/list/list_renderer";
import { listView } from "@web/views/list/list_view";
```

### Services Chính
```javascript
// ORM - Database operations
const orm = useService("orm");
await orm.call('model_name', 'method_name', []);
await orm.search(...);
await orm.read(...);
await orm.unlink(...);

// Action - Navigation & Actions
const action = useService("action");
action.doAction({...});

// Notification - Toast messages
const notification = useService("notification");
notification.add("Message", { type: "success" });

// Dialog - Modal dialogs
const dialog = useService("dialog");
dialog.add(ConfirmationDialog, {...});
```

---

## Quy Trình Phát Triển

### 1. Tạo Component Mới
```
Bước 1: Tạo file .js (OWL Component)
  ↓
Bước 2: Tạo file .xml (Template)
  ↓
Bước 3: Đăng ký với registry
  ↓
Bước 4: Khai báo trong __manifest__.py
  ↓
Bước 5: Test
```

### 2. Patch Existing Components
```
Bước 1: Import component cần patch
  ↓
Bước 2: Dùng patch() để modify
  ↓
Bước 3: Đảm bảo super.setup() được gọi
  ↓
Bước 4: Test
```

### 3. Template Inheritance
```
Bước 1: Tạo template kế thừa từ template khác
  ↓
Bước 2: Dùng <t t-inherit> với xpath
  ↓
Bước 3: Chọn position (before/after/replace/attributes/inside)
  ↓
Bước 4: Test thay đổi
```

---

## Best Practices

### ✅ DO's
- ✅ Luôn gọi `super.setup()` khi patch component
- ✅ Dùng `useState()` cho state reactive
- ✅ Sử dụng services thay vì global state
- ✅ Validate dữ liệu trước khi gửi lên server
- ✅ Thêm error handling cho ORM calls
- ✅ Dùng `t-on-click.stop` để prevent event bubbling
- ✅ Organize code theo responsibility (getters, update methods, actions)

### ❌ DON'Ts
- ❌ Không modify core Odoo components trực tiếp
- ❌ Không dùng global variables cho state
- ❌ Không gọi render() trực tiếp
- ❌ Không quên `@odoo-module` comment ở đầu file
- ❌ Không để async operations không có error handling

### Performance Tips
- 🚀 Dùng `limit` trong ORM search để tránh load hết
- 🚀 Cache dữ liệu nếu không thay đổi thường xuyên
- 🚀 Lazy load components khi cần thiết
- 🚀 Minimize re-renders bằng cách tối ưu state updates

---

## Tiếp Theo
- [2-owl_components.md](2-owl_components.md) - Chi tiết về OWL Components
- [3-templates.md](3-templates.md) - XML Templates & Inheritance
- [4-patching.md](4-patching.md) - Patching Existing Components
- [5-registry.md](5-registry.md) - Registry System
- [6-examples.md](6-examples.md) - Thực tế từ code proid
