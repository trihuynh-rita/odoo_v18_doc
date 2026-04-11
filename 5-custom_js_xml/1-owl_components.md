# OWL Components - Hướng Dẫn Chi Tiết

## 📌 OWL Basics

### Cấu Trúc Component Cơ Bản
```javascript
/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class MyComponent extends Component {
    static template = "module.my_component_template";
    static props = ["*"];  // Accept all props
    
    setup() {
        // Initialize state, services, hooks
    }
}
```

### Static Properties
```javascript
static template = "module.template_name";      // Template ID (t-name)
static components = { ... };                   // Child components
static props = ["prop1", "prop2"];            // Props validation
static defaultProps = { ... };                // Default values
```

---

## 🔧 Setup & Lifecycle

### setup() Method
- **Mục đích**: Khởi tạo component (chỉ gọi 1 lần)
- **Thực hiện**: Initialize state, services, event listeners

```javascript
setup() {
    // 1. Khởi tạo services
    const orm = useService("orm");
    const action = useService("action");
    
    // 2. Khởi tạo state reactive
    this.state = useState({
        isOpen: false,
        items: [],
        selectedId: null,
    });
    
    // 3. Khởi tạo lifecycle hooks
    onWillStart(async () => {
        // Chạy trước khi component được render lần đầu
        const data = await orm.search('model');
        this.state.items = data;
    });
    
    onMounted(() => {
        // Sau khi component được mount
        console.log("Component is mounted");
    });
}
```

### Lifecycle Hooks
```javascript
onWillStart()      // Trước render lần đầu
onMounted()        // Sau khi DOM được thêm
onWillUpdate()     // Trước khi update
onUpdated()        // Sau khi update
onWillUnmount()    // Trước khi remove
onWillPatch()      // Trước khi patch dữ liệu
```

---

## 📦 State Management

### useState - Reactive State
```javascript
import { useState } from "@odoo/owl";

const state = useState({
    count: 0,
    isOpen: false,
    items: [],
    selectedItem: null,
});

// Update state (triggers re-render)
state.count++;
state.isOpen = !state.isOpen;
state.items.push(newItem);
```

### Computed Properties
```javascript
get totalItems() {
    return this.state.items.length;
}

get selectedItemName() {
    return this.state.selectedItem?.name || "None";
}
```

### Update Methods
```javascript
updateState(newValue) {
    // Method 1: Direct update (không reactive nếu nested)
    this.state.value = newValue;
    
    // Method 2: Reassign object (reactive)
    this.state.selectedItem = { ...this.state.selectedItem, name: newValue };
    
    // Method 3: Array methods (reactive)
    this.state.items = [...this.state.items, newItem];
}
```

---

## 🎁 Props & Data Binding

### Props Validation
```javascript
static props = {
    record: { type: Object, optional: true },
    items: { type: Array },
    onSelect: { type: Function },
    label: { type: String },
};
```

### Props Types
```javascript
// Required
{ type: String }            // Error if not provided
{ type: Number }
{ type: Boolean }
{ type: Array }
{ type: Object }
{ type: Function }

// Optional
{ type: String, optional: true }

// Default value
{ type: Number, default: 0 }

// Wildcard (*) - Accept anything
static props = ["*"];
```

### Accessing Props
```javascript
onSelectItem() {
    if (this.props.onSelect) {
        this.props.onSelect(this.state.selectedId);
    }
}
```

---

## 🔐 Services Usage

### Common Services Pattern
```javascript
setup() {
    const orm = useService("orm");
    const action = useService("action");
    const notification = useService("notification");
    const dialog = useService("dialog");
    
    // Store as instance properties
    this.orm = orm;
    this.action = action;
    this.notification = notification;
    this.dialog = dialog;
}

// Use in methods
async onDeleteItem(itemId) {
    try {
        await this.orm.unlink("item.model", [itemId]);
        this.notification.add("Deleted!", { type: "success" });
    } catch (error) {
        this.notification.add("Error!", { type: "danger" });
    }
}
```

### ORM Service Methods
```javascript
// Search
const ids = await orm.search('model_name', [domain], { limit: 10 });

// Read
const records = await orm.read('model_name', ids, ['field1', 'field2']);

// Create
const newId = await orm.create('model_name', [{ name: 'New' }]);

// Write
await orm.write('model_name', [id], { name: 'Updated' });

// Unlink (Delete)
await orm.unlink('model_name', [id1, id2]);

// Call method
const result = await orm.call('model_name', 'method_name', [args]);
```

### Action Service Methods
```javascript
// Open window action
this.action.doAction({
    type: "ir.actions.act_window",
    res_model: "model_name",
    res_id: recordId,
    views: [[false, "form"], [false, "list"]],
    target: "current",  // or "new"
    domain: [["field", "=", value]],
    context: { ...context },
});

// Open URL
this.action.doAction({
    type: "ir.actions.act_url",
    url: "https://example.com",
    target: "new",
});

// Execute server action
this.action.doAction({
    type: "ir.actions.server",
    id: server_action_id,
});
```

---

## 🎨 Rendering & Binding

### Event Handling
```javascript
// In setup
onWillStart(async () => { ... })
onMounted(() => { ... })

// In methods
onClick() { ... }
onSubmit(ev) { ... }
async onDelete() { ... }

// Arrow functions (nên dùng để giữ `this`)
updateValue = (value) => {
    this.state.value = value;
}
```

### Passing Data to Templates
```javascript
// Template accesses:
// - this.props
// - this.state
// - this methods
// - computed getters

get formattedDate() {
    return new Date(this.state.date).toLocaleDateString();
}

// Template: <t t-esc="formattedDate" />
```

---

## 📐 Component Composition

### Child Components
```javascript
import { MyChild } from "./my_child";

export class MyParent extends Component {
    static components = { MyChild };
    static template = "module.parent_template";
    
    setup() {
        this.state = useState({ selectedId: null });
    }
    
    onChildSelect(id) {
        this.state.selectedId = id;
    }
}
```

### Template
```xml
<t t-name="module.parent_template" owl="1">
    <div>
        <MyChild
            items="state.items"
            onSelect="(id) => this.onChildSelect(id)"
        />
        <div t-if="state.selectedId">
            Selected: <t t-esc="state.selectedId" />
        </div>
    </div>
</t>
```

---

## 🚀 Advanced Patterns

### Async Operations
```javascript
async loadData() {
    try {
        const data = await this.orm.search('model', [domain]);
        this.state.items = data;
    } catch (error) {
        console.error("Failed to load", error);
        this.notification.add("Error loading", { type: "danger" });
    }
}
```

### Conditional Rendering
```javascript
get hasItems() {
    return this.state.items.length > 0;
}

get isEmpty() {
    return this.state.items.length === 0;
}

// In template: t-if="hasItems", t-else, t-elif
```

### List Rendering
```javascript
// State
this.state = useState({
    items: [
        { id: 1, name: "Item 1" },
        { id: 2, name: "Item 2" },
    ]
});

// Template
<t t-foreach="state.items" t-as="item" t-key="item.id">
    <div t-esc="item.name" />
</t>
```

### Two-way Binding (Controlled)
```javascript
// State
this.state = useState({ value: "" });

// Method
onInputChange(ev) {
    this.state.value = ev.target.value;
}

// Template
<input
    type="text"
    t-att-value="state.value"
    t-on-input="onInputChange"
/>
```

---

## 🎯 Complete Example: Simple Component

```javascript
/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ProductFilter extends Component {
    static template = "proid.ProductFilter";
    static props = ["*"];
    
    setup() {
        const orm = useService("orm");
        const action = useService("action");
        
        this.orm = orm;
        this.action = action;
        this.state = useState({
            categories: [],
            selectedCategory: null,
            isLoading: true,
        });
        
        onWillStart(async () => {
            try {
                const categories = await orm.search('product.category');
                this.state.categories = categories;
                this.state.isLoading = false;
            } catch (error) {
                console.error("Load failed", error);
                this.state.isLoading = false;
            }
        });
    }
    
    async onSelectCategory(categoryId) {
        this.state.selectedCategory = categoryId;
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "product.product",
            domain: [["category_id", "=", categoryId]],
            views: [[false, "list"]],
        });
    }
}
```

---

## Tiếp Theo
- [3-templates.md](3-templates.md) - Template XML matching
- [4-patching.md](4-patching.md) - Patching techniques
