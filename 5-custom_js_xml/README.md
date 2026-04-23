# Custom JavaScript & XML for Odoo v18

Comprehensive documentation on customizing Odoo v18 using the OWL Framework, JavaScript, and XML templates.

## 📚 Document Structure

### 1. **[0-overview.md](0-overview.md)**
   - Odoo v18 customization overview
   - Basic architecture
   - Development workflow
   - Best practices

### 2. **[1-owl_components.md](1-owl_components.md)**
   - OWL Component basics
   - Setup & lifecycle hooks
   - State management
   - Services usage
   - Props & data binding

### 3. **[2-templates.md](2-templates.md)**
   - Template syntax and output
   - Conditionals & loops (foreach)
   - Attribute binding
   - Event handling
   - Component composition
   - Template inheritance (t-inherit)

### 4. **[3-patching_system.md](3-patching_system.md)**
   - Patch() function usage
   - Patching patterns
   - Common Odoo components
   - Practical examples
   - Best practices

### 5. **[4-registry_system.md](4-registry_system.md)**
   - Registry overview
   - Registering components, fields, views
   - Common categories
   - Practical examples

### 6. **[5-examples.md](5-examples.md)**
   - Real-world examples from proid
   - Advanced filter mega menu
   - Row actions dropdown
   - Custom pagination
   - Complete working code

### 7. **[6-ui_blocking_navigation.md](6-ui_blocking_navigation.md)**
   - Handling UI Blocking errors during navigation
   - Race conditions between Auto-save and Custom Navigation
   - Patching FormController to force unblock UI

---

## 🚀 Quick Start

### File Structure
```
custom_addons/my_module/
├── static/src/
│   ├── js/
│   │   ├── components.js
│   │   └── patches.js
│   ├── xml/
│   │   ├── templates.xml
│   │   └── patches.xml
│   └── scss/styles.scss
└── __manifest__.py
```

### Minimal Setup
```python
# __manifest__.py
{
    'name': 'My Module',
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/js/**/*.js',
            'my_module/static/src/xml/**/*.xml',
        ],
    },
}
```

### Component Template
```javascript
/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class MyComponent extends Component {
    static template = "module.my_template";
    
    setup() {
        this.orm = useService("orm");
    }
}

registry.category("components").add("MyComponent", MyComponent);
```

---

## 📖 Common Tasks

### Create a New Component
1. Create `.js` file → Create `.xml` file → Register with registry
2. See [1-owl_components.md](1-owl_components.md)

### Modify an Existing Component
1. Use `patch()` to extend the component
2. See [3-patching_system.md](3-patching_system.md)

### Add a Custom Field Widget
1. Create Component + Template
2. Register with `fields` category in registry
3. See [5-examples.md](5-examples.md#example-2-row-actions-field-widget)

### Add a Custom View
1. Extend ListRenderer/FormRenderer
2. Create custom template
3. Register with `views` category in registry
4. See [5-examples.md](5-examples.md#example-3-custom-list-renderer)

### Modify a Template (Inherit)
1. Use `<t t-inherit>` in `.xml`
2. Use `<xpath>` to target elements
3. See [2-templates.md](2-templates.md#🔗-template-inheritance-t-inherit)

---

## 🔑 Key Concepts

### OWL (Object Web Library)
- Lightweight, reactive framework
- Component-based architecture
- Automatic re-rendering on state change

### State Management
- `useState()` - Reactive state
- Mutable - Direct assignment triggers update
- No Redux/Vuex needed

### Services
- `orm` - Database operations
- `action` - Navigation
- `notification` - Toast messages
- `dialog` - Modal dialogs

### Registry
- Central registration system
- Categories: components, fields, views, actions
- Enables plugin-like architecture

---

## 💡 Tips & Tricks

### Performance
```javascript
// ✅ Good: Use getters for computed values
get itemCount() {
    return this.state.items.length;
}

// ❌ Bad: Compute in template
{{ this.state.items.length }}
```

### Error Handling
```javascript
// ✅ Good: Try-catch with user feedback
try {
    await this.orm.unlink('model', [id]);
    this.notification.add("Deleted!", { type: "success" });
} catch (error) {
    this.notification.add("Error: " + error, { type: "danger" });
}
```

### Event Handling
```xml
<!-- ✅ Good: Explicit handler -->
<button t-on-click="onDelete">Delete</button>

<!-- ❌ Bad: Inline logic -->
<button t-on-click="() => this.orm.unlink(...)">Delete</button>
```

---

## 🧪 Testing

### Browser Console
```javascript
// Check if component is registered
odoo.web.registry.category("components").contains("MyComponent");

// Get component
odoo.web.registry.category("components").get("MyComponent");
```

### Manual Testing Steps
1. Clear browser cache (Ctrl+Shift+Del)
2. Refresh page (Ctrl+Shift+R)
3. Open DevTools (F12)
4. Test functionality
5. Check console for errors

---

## 🔗 References

### Official Documentation
- [Odoo 18 Framework](https://www.odoo.com/documentation/18.0/)
- [OWL Framework](https://github.com/odoo/owl)

### Related Files in Workspace
- `/rita-prodid/custom_addons/proid/` - Complete example
- `/odoo_v18_doc/` - Additional documentation

---

## 📝 Document Details

- **Created**: 2024
- **Version**: Odoo v18
- **Framework**: OWL (Object Web Library)
- **Status**: Complete with real examples

---

## 🆘 Troubleshooting

### Component not showing
- Check if registered ✓
- Check template name ✓
- Check `@odoo-module` comment ✓
- Clear cache and refresh ✓

### Template error
- Check XML syntax ✓
- Ensure `owl="1"` attribute ✓
- Validate XPath selectors ✓
- Check t-name uniqueness ✓

### ORM call failing
- Check model name exact spelling ✓
- Verify method exists on model ✓
- Add error handling with try-catch ✓

### Service not available
- Import with `useService()` ✓
- Store as instance property ✓
- Check service name spelling ✓

---

**Happy Customizing! 🚀**
