# Registry System - Registering Custom Components

## 🎯 Registry Overview

Registry(rivet) giúp đăng ký các components, fields, views, actions tùy chỉnh vào Odoo.

### Registry Categories
```javascript
// Main categories
"components"              // UI Components
"fields"                  // Field widgets
"views"                   // View types (list, form, kanban)
"actions"                 // Action handlers
"services"                // Services
"dialogs"                 // Dialog components
```

---

## 📝 Basic Registration

### Register Component
```javascript
import { registry } from "@web/core/registry";
import { MyComponent } from "./my_component";

registry.category("components").add("my_component_id", MyComponent);
```

### Register Field Widget
```javascript
export const myFieldConfig = {
    component: MyFieldComponent,
    supportedTypes: ["integer", "text"],
    supportedOptions: ["size", "style"],
};

registry.category("fields").add("my_field_type", myFieldConfig);
```

### Register View
```javascript
import { listView } from "@web/views/list/list_view";

export const customListView = {
    ...listView,
    Renderer: CustomRenderer,
};

registry.category("views").add("custom_list", customListView);
```

---

## 🔧 Common Registry Categories

### 1. Field Widgets
```javascript
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class MyCustomField extends Component {
    static template = "module.my_field_template";
    static props = ["value", "onChange", ...];
}

const myFieldConfig = {
    component: MyCustomField,
    supportedTypes: ["integer", "text", "selection"],
    supportedOptions: ["required", "readonly"],
    extractProps({ attrs, field }) {
        return {
            value: field.value,
            required: attrs.required,
            readonly: attrs.readonly,
        };
    },
};

registry.category("fields").add("my_custom_field", myFieldConfig);
```

### 2. View Types
```javascript
import { listView } from "@web/views/list/list_view";

class CustomListRenderer extends ListRenderer {
    setup() {
        super.setup();
        // Custom setup
    }
}

const customListView = {
    ...listView,
    Renderer: CustomListRenderer,
    Controller: CustomListController,
};

registry.category("views").add("alternative_list", customListView);
```

### 3. Components
```javascript
registry.category("components").add("MyDropdown", MyDropdown);
```

### 4. Action Types
```javascript
registry.category("actions").add("custom_action", CustomActionHandler);
```

---

## 💾 Practical Examples

### Example 1: Register Advanced Filter Component
```javascript
/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class ProidAdvanceFilter extends Component {
    static template = "proid.proid_advance_filter_template";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            isDropdownOpen: false,
            groups: [],
            selectedGroups: [],
        });

        onWillStart(async () => {
            try {
                const data = await this.orm.call(
                    "proid.product.group",
                    "get_group_hierarchy",
                    []
                );
                this.state.groups = data || [];
            } catch (e) {
                console.error("Failed to fetch", e);
            }
        });
    }
}

// Register as component
registry.category("components").add("ProidAdvanceFilter", ProidAdvanceFilter);
```

### Example 2: Register Custom Field Widget
```javascript
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ProIdAttributeTable extends Component {
    static template = "proid.AttributeTable";
    static props = {
        ...standardFieldProps,
        value: { type: Object },
    };
}

const proIdAttributeTableConfig = {
    component: ProIdAttributeTable,
    supportedTypes: ["one2many"],
    supportedOptions: [],
    extractProps: ({ attrs, field }) => ({
        value: field.value,
    }),
};

registry.category("fields").add("proid_attribute_table", proIdAttributeTableConfig);
```

### Example 3: Register Row Action Field
```javascript
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ProidListRowActions extends Component {
    static template = "proid.ListRowActions";
    static components = { Dropdown, DropdownItem };

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.dialog = useService("dialog");
    }

    onEdit() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "proid.product",
            res_id: this.props.record.resId,
            views: [[false, "form"]],
        });
    }

    onDelete() {
        // Delete logic with confirmation
    }
}

export const proidListRowActions = {
    component: ProidListRowActions,
    supportedTypes: ["integer", "many2one"],
};

registry.category("fields").add("proid_row_actions", proidListRowActions);
```

### Example 4: Register Custom List View
```javascript
/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

export class PaginationRenderer extends ListRenderer {
    // Custom rendering logic
}

PaginationRenderer.template = "proid.ListRenderer";

export const proidListView = {
    ...listView,
    Renderer: PaginationRenderer,
};

registry.category("views").add("pagination_render", proidListView);
```

---

## 🔗 Using Registered Items

### In XML Templates
```xml
<!-- Use registered component -->
<t t-name="module.parent" owl="1">
    <ProidAdvanceFilter />
</t>

<!-- Use registered field widget in form view -->
<field name="attributes" widget="proid_attribute_table" />

<!-- Use registered view -->
<!-- Defined in action: views: [[false, "pagination_render"]] -->
```

### Programmatically
```javascript
// Access registry
const registry = useService("registry");
const components = registry.category("components");
const MyComponent = components.get("MyComponent");

// Create instance
const instance = new MyComponent(...);
```

---

## 📊 Registry Priority & Ordering

### Loading Order
```
1. Core Odoo registrations
2. Community addons (alphabetical)
3. Custom addons (alphabetical)
4. Late patches
```

### Overriding
```javascript
// You can override existing registry items
registry.category("fields").add("integer", MyCustomIntegerField);

// Later registrations override earlier ones
registry.category("components").add("NavBar", CustomNavBar);
```

---

## 🎯 Best Practices

### ✅ DO's
- ✅ Register in component file (same file)
- ✅ Export both Component and Config
- ✅ Use descriptive registry IDs
- ✅ Document supported types
- ✅ Handle errors in initialization

### ❌ DON'Ts
- ❌ Don't register in random files
- ❌ Don't forget to import registry
- ❌ Don't use conflicting IDs
- ❌ Don't skip component validation
- ❌ Don't register in __init__.py

---

## 🧪 Testing Registry

### Check if Registered
```javascript
import { registry } from "@web/core/registry";

const components = registry.category("components");
const exists = components.contains("my_component");
console.log(exists); // true/false

// Get component
const Component = components.get("my_component");
```

### In QUnit Tests
```javascript
QUnit.test("Component registered", function(assert) {
    const registry = await loadModules("web");
    const components = registry.category("components");
    assert.ok(components.contains("MyComponent"));
});
```

---

## 📋 Complete Registration Example

```javascript
/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Dropdown, DropdownItem } from "@web/core/dropdown/dropdown";

/**
 * Advanced Filter Component
 * Displays hierarchical product groups with mega menu
 */
export class ProidAdvanceFilter extends Component {
    static template = "proid.proid_advance_filter_template";
    static props = ["*"];
    static components = { Dropdown, DropdownItem };

    setup() {
        const orm = useService("orm");
        const action = useService("action");

        this.orm = orm;
        this.action = action;

        this.state = useState({
            isDropdownOpen: false,
            activeGroup: null,
            groups: [],
            selectedGroups: [],
        });

        onWillStart(async () => {
            try {
                const data = await orm.call(
                    "proid.product.group",
                    "get_group_hierarchy",
                    []
                );
                this.state.groups = data || [];
                if (this.state.groups.length > 0) {
                    this.state.activeGroup = this.state.groups[0];
                }
            } catch (error) {
                console.error("Failed to fetch product groups", error);
            }
        });
    }

    toggleDropdown() {
        this.state.isDropdownOpen = !this.state.isDropdownOpen;
    }

    async onSelectGroup(group) {
        this.state.selectedGroups = [group];
        await this._applyFilter();
        this.state.isDropdownOpen = false;
    }

    _applyFilter() {
        const groupIds = this.state.selectedGroups.map(g => g.id);
        const domain = groupIds.length > 0 ? [["group_ids", "in", groupIds]] : [];

        return this.action.doAction({
            type: "ir.actions.act_window",
            name: "Sản phẩm",
            res_model: "proid.product",
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain,
        });
    }
}

// Register as component
registry
    .category("components")
    .add("ProidAdvanceFilter", ProidAdvanceFilter);
```

---

## Tiếp Theo
- [5-fields_widgets.md](5-fields_widgets.md) - Custom field widgets
- [6-examples.md](6-examples.md) - Real-world examples
