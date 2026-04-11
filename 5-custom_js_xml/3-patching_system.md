# Patching System - Modify Core Odoo Components

## 🔧 Patch Basics

### Patch() Function
```javascript
import { patch } from "@web/core/utils/patch";
import { SomeComponent } from "@web/path/to/component";

patch(SomeComponent.prototype, {
    // Add/Override methods
    methodName() {
        // Your code
    },
    
    // Override setup (must call super.setup())
    setup() {
        super.setup();
        // Your additional setup
    },
});
```

### When to Use Patch
- ✅ Modify core Odoo components behavior
- ✅ Add methods to existing components
- ✅ Extend setup logic
- ✅ Modify event handlers
- ❌ Don't use if you can use inheritance/extension

---

## 🎯 Patching Patterns

### Pattern 1: Patch ControlPanel
```javascript
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { useService } from "@web/core/utils/hooks";

patch(ControlPanel.prototype, {
    setup() {
        super.setup();
        this.actionService = useService("action");
    },

    async onCustomAction() {
        const resModel = this.env.searchModel?.resModel;
        if (!resModel) return;

        await this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: resModel,
            views: [[false, "form"]],
        });
    }
});
```

### Pattern 2: Patch ListRenderer
```javascript
import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";

patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        this.customState = useState({
            selectedRows: [],
        });
    },

    selectRow(row) {
        this.customState.selectedRows.push(row.id);
    },
});
```

### Pattern 3: Patch Static Methods
```javascript
patch(MyComponent, {
    // Patch static method
    staticMethod() {
        return "patched";
    }
});

// Or patch static components
patch(MyComponent, {
    components: {
        ...MyComponent.components,
        NewComponent,
    }
});
```

### Pattern 4: Patch with super() calls
```javascript
// Important: Always call super when overriding
patch(Component.prototype, {
    setup() {
        super.setup();  // MUST call this!
        // Your setup
    },

    onAction() {
        const result = super.onAction?.();  // Call parent if exists
        // Do additional work
        return result;
    },
});
```

---

## 📋 Common Odoo Components to Patch

### ControlPanel
```javascript
// Navigation control for list/form views
patch(ControlPanel.prototype, {
    setup() {
        super.setup();
    }
});
```

### ListRenderer
```javascript
// Renders list view rows
patch(ListRenderer.prototype, {
    setup() {
        super.setup();
    }
});
```

### FormController
```javascript
// Controls form view
patch(FormController.prototype, {
    setup() {
        super.setup();
    }
});
```

### NavBar
```javascript
// Top navigation bar
patch(NavBar.prototype, {
    setup() {
        super.setup();
    }
});
```

---

## 🔄 Practical Patching Examples

### Example 1: Add Custom Button to ControlPanel
```javascript
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { useService } from "@web/core/utils/hooks";

patch(ControlPanel.prototype, {
    setup() {
        super.setup();
        this.action = useService("action");
    },

    async onExportData() {
        const model = this.env.searchModel?.resModel;
        if (!model) return;

        // Call backend export
        const result = await this.action.doAction({
            type: "ir.actions.server",
            id: "export_action",
        });
    }
});
```

### Example 2: Intercept Delete Action
```javascript
patch(ListRenderer.prototype, {
    setup() {
        super.setup();
    },

    async deleteRecord(record) {
        const confirmed = await this.showConfirmation();
        if (!confirmed) return;

        // Custom delete logic
        const result = super.deleteRecord?.(record);
        return result;
    },

    async showConfirmation() {
        // Your confirmation logic
        return true;
    }
});
```

### Example 3: Modify Navbar
```javascript
import { NavBar } from "@web/webclient/navbar/navbar";

patch(NavBar.prototype, {
    setup() {
        super.setup();
        this.customMenu = this.getCustomMenu();
    },

    getCustomMenu() {
        return {
            id: 'custom_menu',
            name: 'My Custom Menu',
            items: []
        };
    }
});
```

### Example 4: Patch Multiple Times (Safe)
```javascript
// Can patch same component multiple times
patch(ControlPanel.prototype, {
    setup() {
        super.setup();
        this.featureA = true;
    }
});

patch(ControlPanel.prototype, {
    setup() {
        super.setup();
        this.featureB = true;
        // Both featureA and featureB available now
    }
});
```

---

## ⚠️ Gotchas & Best Practices

### ✅ DO's
- ✅ Always call `super.setup()` first
- ✅ Always call parent method before adding logic
- ✅ Store services as instance properties
- ✅ Use proper error handling
- ✅ Test on clean Odoo instance

### ❌ DON'Ts
- ❌ Don't forget `super.setup()`
- ❌ Don't directly modify component.prototype
- ❌ Don't patch in wrong order (before component imports)
- ❌ Don't create infinite loops with patches
- ❌ Don't assume parent methods exist (use `?.`)

### Performance Tips
```javascript
// ✅ Good: Cache computed values
get filterConfig() {
    if (!this._filterConfig) {
        this._filterConfig = this.computeFilter();
    }
    return this._filterConfig;
}

// ❌ Bad: Compute every time
get filter() {
    return this.computeExpensiveFilter();
}
```

---

## 🧪 Testing Patches

### Manual Testing
```javascript
// In browser console
const { patch } = owl;
const { ControlPanel } = web;

// Check if patched
console.log(ControlPanel.prototype.myMethod);

// Test
const instance = new ControlPanel();
instance.setup();
```

### Unit Testing
```javascript
import { patch } from "@web/core/utils/patch";
import { MyComponent } from "my_module";

QUnit.test("Patch works", async function(assert) {
    patch(MyComponent.prototype, {
        customMethod() {
            return "patched";
        }
    });

    const result = MyComponent.prototype.customMethod();
    assert.equal(result, "patched");
});
```

---

## 🎯 Real Example: ControlPanel Patch from proid

```javascript
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { useService } from "@web/core/utils/hooks";

export class ProidControlPanelPatch {
    static apply() {
        patch(ControlPanel.prototype, {
            setup() {
                super.setup();
                this.actionService = useService("action");
            },

            async onProidCreateNew() {
                const resModel = this.env.searchModel?.resModel;
                if (!resModel) return;

                await this.actionService.doAction({
                    type: "ir.actions.act_window",
                    res_model: resModel,
                    views: [[false, "form"]],
                    target: "current",
                });
            },

            async onProidExport() {
                const resModel = this.env.searchModel?.resModel;
                if (!resModel) return;

                await this.actionService.doAction({
                    type: "ir.actions.server",
                    id: "export_action",
                });
            }
        });
    }
}

// Apply patch when module loads
ProidControlPanelPatch.apply();
```

---

## Tiếp Theo
- [4-registry_system.md](4-registry_system.md) - Registry patterns
- [5-fields_widgets.md](5-fields_widgets.md) - Custom fields
