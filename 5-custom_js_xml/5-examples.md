# Real-World Examples from proid

## 📚 Complete Examples from Production Code

---

## Example 1: Advanced Filter Component

### Component File (advance_filter.js)
```javascript
/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { patch } from "@web/core/utils/patch";

/**
 * ProidAdvanceFilter: Mega dropdown filter for product categories
 * Displays hierarchical groups with interactive UI
 */
export class ProidAdvanceFilter extends Component {
    static template = "proid.proid_advance_filter_template";
    static props = ["*"];

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

        // Load hierarchy on component start
        onWillStart(async () => {
            try {
                const data = await this.orm.call(
                    "proid.product.group",
                    "get_group_hierarchy",
                    []
                );
                this.state.groups = data || [];
                if (this.state.groups.length > 0) {
                    this.state.activeGroup = this.state.groups[0];
                }
            } catch (e) {
                console.error("Failed to fetch product groups", e);
            }
        });
    }

    // UI Methods
    toggleDropdown() {
        this.state.isDropdownOpen = !this.state.isDropdownOpen;
    }

    onHoverGroup(group) {
        this.state.activeGroup = group;
    }

    async onSelectGroup(group) {
        if (!this.state.selectedGroups.find(g => g.id === group.id)) {
            this.state.selectedGroups = [group];
            await this._applyFilter();
        }
        this.state.isDropdownOpen = false;
    }

    // Filter logic
    _applyFilter() {
        const groupIds = this.state.selectedGroups.map(g => g.id);
        const domain = groupIds.length > 0 
            ? [["group_ids", "in", groupIds]] 
            : [];

        return this.action.doAction({
            type: "ir.actions.act_window",
            name: "Sản phẩm",
            res_model: "proid.product",
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain,
            context: {
                search_default_draft: 0,
            },
        });
    }
}

// Register component
registry.category("components").add("ProidAdvanceFilter", ProidAdvanceFilter);

// Patch ControlPanel to add custom button
patch(ControlPanel.prototype, {
    setup() {
        super.setup();
        this.actionService = useService("action");
    },

    async onProidCreateNew() {
        const resModel = this.env.searchModel?.resModel;
        if (!resModel) return;

        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: resModel,
            views: [[false, "form"]],
            target: "current",
        });
    },

    async onProidImport() {
        const resModel = this.env.searchModel?.resModel;
        if (!resModel) return;

        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "import",
            params: {
                model: resModel,
            },
        });
    },

    async onProidExport() {
        const resModel = this.env.searchModel?.resModel;
        if (!resModel) return;

        this.actionService.doAction({
            type: "ir.actions.server",
            id: "export_action",
        });
    }
});
```

### Template File (advance_filter.xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">

    <!-- Advanced Filter Mega Menu Template -->
    <t t-name="proid.proid_advance_filter_template" owl="1">
        <div class="o_proid_advance_dropdown position-relative">
            <!-- Toggle Button -->
            <button
                class="btn o_proid_dropdown_toggle d-flex align-items-center border-0 p-2 bg-white shadow-sm rounded-3 h-100"
                t-on-click="toggleDropdown"
                t-att-class="{'bg-light-subtle': state.isDropdownOpen}">
                <div
                    class="bg-danger-light text-danger p-2 rounded-2 d-flex align-items-center justify-content-center"
                    style="width: 32px; height: 32px;">
                    <i class="fa fa-th-large fs-6" />
                </div>
                <span class="fw-bold text-secondary mx-2 fs-7">Hàng hóa</span>
                <i
                    t-attf-class="fa fa-chevron-#{state.isDropdownOpen ? 'up' : 'down'} ms-auto fs-9 opacity-50" />
            </button>

            <!-- Mega Menu Dropdown -->
            <t t-if="state.isDropdownOpen">
                <div class="o_proid_mega_menu shadow-lg bg-white rounded-3 border-0 mt-3 d-flex overflow-hidden"
                    style="width: 850px; height: 480px; position: absolute; z-index: 1050; left: 0;">
                    
                    <!-- Sidebar: Group List -->
                    <div class="o_mega_menu_sidebar bg-light" style="width: 240px; overflow-y: auto;">
                        <t t-foreach="state.groups || []" t-as="group" t-key="group.id">
                            <div
                                class="o_mega_menu_item d-flex align-items-center p-3 cursor-pointer border-bottom border-transparent transition-all"
                                t-on-mouseenter="() => this.onHoverGroup(group)"
                                t-on-click="() => this.onSelectGroup(group)"
                                t-att-class="{'bg-white text-danger fw-bold shadow-sm': state.activeGroup and state.activeGroup.id == group.id, 'text-dark': !state.activeGroup or state.activeGroup.id != group.id}">
                                <t t-esc="group.name" />
                            </div>
                        </t>
                    </div>

                    <!-- Content: Subgroups -->
                    <div class="o_mega_menu_content p-4 flex-grow-1 overflow-y-auto bg-white text-start">
                        <t t-if="state.activeGroup">
                            <div class="row row-cols-2 row-cols-lg-3 g-4">
                                <t t-foreach="state.activeGroup.children || []" t-as="child" t-key="child.id">
                                    <div class="col">
                                        <a href="#"
                                            class="o_mega_menu_link px-2 py-1 rounded text-secondary fs-8 transition-all hover-bg-danger-light hover-text-danger cursor-pointer"
                                            t-on-click.prevent="() => this.onSelectGroup(child)">
                                            <t t-esc="child.name" />
                                        </a>
                                    </div>
                                </t>
                            </div>
                        </t>
                        <t t-else="">
                            <div class="text-muted">Chọn danh mục</div>
                        </t>
                    </div>
                </div>
            </t>
        </div>
    </t>

    <!-- Patch ControlPanel: Add buttons -->
    <t t-inherit="web.ControlPanel" t-inherit-mode="extension" owl="1">
        <!-- Add filter component to left -->
        <xpath expr="//div[hasclass('o_control_panel_breadcrumbs')]" position="inside">
            <div class="o_proid_cp_left d-flex align-items-center">
                <ProidAdvanceFilter
                    t-if="env.searchModel?.resModel === 'proid.product' and env.config?.viewType === 'list'" />
            </div>
        </xpath>

        <!-- Add custom buttons to right -->
        <xpath expr="//div[hasclass('o_control_panel_navigation')]" position="inside">
            <div class="o_proid_cp_right d-flex align-items-center gap-3">
                <button
                    class="btn btn-proid-action-create fw-bold px-4 py-2 rounded-2 d-flex align-items-center gap-2 shadow-sm text-white"
                    t-on-click="onProidCreateNew">
                    <i class="fa fa-plus fs-8" />
                    <span>Tạo mới</span>
                </button>

                <div class="dropdown">
                    <button class="btn btn-sm btn-light" data-bs-toggle="dropdown">
                        <i class="fa fa-ellipsis-v" />
                    </button>
                    <ul class="dropdown-menu shadow border-0 rounded-3 mt-2">
                        <li>
                            <a class="dropdown-item" href="#" t-on-click.prevent="onProidImport">
                                <i class="fa fa-upload" /> Import
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="#" t-on-click.prevent="onProidExport">
                                <i class="fa fa-download" /> Export
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </xpath>
    </t>

</templates>
```

### Key Learning Points
- ✅ Fetch data in `onWillStart` hook
- ✅ Use `useState` for reactive state
- ✅ Patch core components to extend functionality
- ✅ Use `t-att-class` for conditional styling
- ✅ Use `t-foreach` for rendering lists with keys

---

## Example 2: Row Actions Field Widget

### Component File (list_row_actions.js)
```javascript
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

/**
 * ProidListRowActions: Per-row dropdown menu for product list
 * Supports: Show detail, Edit, Delete
 */
export class ProidListRowActions extends Component {
    static components = { Dropdown, DropdownItem };
    static template = "proid.ListRowActions";

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.dialog = useService("dialog");
    }

    // View product detail (readonly mode)
    onShowDetail() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "proid.product",
            res_id: this.props.record.resId,
            views: [[false, "form"]],
            target: "current",
            context: { ...this.props.record.context },
            flags: { mode: "readonly" },
        });
    }

    // Edit product
    onEdit() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "proid.product",
            res_id: this.props.record.resId,
            views: [[false, "form"]],
            target: "current",
            flags: { mode: "edit" },
        });
    }

    // Delete with confirmation
    onDelete() {
        const name = this.props.record.data.display_name 
            || this.props.record.data.name 
            || "";
        
        this.dialog.add(ConfirmationDialog, {
            body: `Bạn có chắc chắn muốn xoá sản phẩm "${name}"?`,
            confirm: async () => {
                try {
                    await this.orm.unlink("proid.product", [this.props.record.resId]);
                    await this.props.record.model.root.load();
                    this.notification.add(
                        "Sản phẩm đã được xoá thành công.",
                        { type: "success" }
                    );
                } catch (error) {
                    this.notification.add(
                        "Không thể xoá sản phẩm này.",
                        { type: "danger" }
                    );
                }
            },
            cancel: () => { },
        });
    }
}

// Register as field widget
export const proidListRowActions = {
    component: ProidListRowActions,
    supportedTypes: ["integer", "many2one"],
};

registry.category("fields").add("proid_row_actions", proidListRowActions);
```

### Template File (list_row_actions.xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="proid.ListRowActions" owl="1">
        <div class="o_proid_row_actions d-flex align-items-center justify-content-center"
             t-on-click.stop="">
            <Dropdown menuClass="'dropdown-menu-end shadow-lg border-0 py-2'">
                <!-- Trigger Button -->
                <button class="btn btn-sm p-0 border-0 bg-transparent d-flex align-items-center justify-content-center o_proid_action_trigger">
                    <img src="/proid/static/src/icon/setting.svg"
                         style="width: 18px; height: 18px;"
                         class="mx-2"
                         title="Thao tác" />
                </button>

                <!-- Menu Items -->
                <t t-set-slot="content">
                    <!-- Show Detail -->
                    <DropdownItem
                        class="'o_proid_action_item px-3 py-2 d-flex align-items-center gap-3 fw-medium'"
                        onSelected="() => this.onShowDetail()">
                        <div class="o_proid_action_icon rounded-2 d-flex align-items-center justify-content-center bg-info-light"
                             style="width: 28px; height: 28px;">
                            <img src="/proid/static/src/icon/eye.svg" style="width: 14px; height: 14px;" />
                        </div>
                        <span class="fs-7 text-dark">Xem chi tiết sản phẩm</span>
                    </DropdownItem>

                    <div class="border-top my-1 opacity-25"></div>

                    <!-- Edit -->
                    <DropdownItem
                        class="'o_proid_action_item px-3 py-2 d-flex align-items-center gap-3 fw-medium'"
                        onSelected="() => this.onEdit()">
                        <div class="o_proid_action_icon rounded-2 d-flex align-items-center justify-content-center bg-warning-light"
                             style="width: 28px; height: 28px;">
                            <img src="/proid/static/src/icon/pen.svg" style="width: 14px; height: 14px;" />
                        </div>
                        <span class="fs-7 text-dark">Chỉnh sửa sản phẩm</span>
                    </DropdownItem>

                    <div class="border-top my-1 opacity-25"></div>

                    <!-- Delete -->
                    <DropdownItem
                        class="'o_proid_action_item px-3 py-2 d-flex align-items-center gap-3 fw-medium text-danger'"
                        onSelected="() => this.onDelete()">
                        <div class="o_proid_action_icon rounded-2 d-flex align-items-center justify-content-center bg-danger-light"
                             style="width: 28px; height: 28px;">
                            <img src="/proid/static/src/icon/forbidden_circle.svg" style="width: 14px; height: 14px;" />
                        </div>
                        <span class="fs-7">Xoá sản phẩm</span>
                    </DropdownItem>
                </t>
            </Dropdown>
        </div>
    </t>
</templates>
```

### Key Learning Points
- ✅ Use Dropdown & DropdownItem for menus
- ✅ Use ConfirmationDialog for dangerous actions
- ✅ Use `t-set-slot` for dropdown content
- ✅ Use `t-on-click.stop` to prevent event bubbling
- ✅ Refresh data after changes with `model.root.load()`

---

## Example 3: Custom List Renderer with Pagination

### Component File (pagination_render.js)
```javascript
/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";

/**
 * PaginationRenderer: Extended list renderer with custom pagination
 * Adds footer with page size selector and custom pagination controls
 */
export class PaginationRenderer extends ListRenderer {
    // Can extend with custom rendering logic
}

// Use custom template referencing pagination footer
PaginationRenderer.template = "proid.ListRenderer";

// Register as custom view
export const proidListView = {
    ...listView,
    Renderer: PaginationRenderer,
};

registry.category("views").add("pagination_render", proidListView);
```

### Template File (paginator_footer.xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <!-- Inherit and extend ListRenderer template -->
    <t t-name="proid.ListRenderer" t-inherit="web.ListRenderer" t-inherit-mode="primary" owl="1">
        <!-- Original list content -->
        <xpath expr="//div[hasclass('o_list_renderer')]" position="replace">
            <div class="d-flex flex-column h-100">
                <!-- Original renderer -->
                <div class="o_list_renderer flex-grow-1"></div>
            </div>
        </xpath>

        <!-- Add custom pagination footer -->
        <xpath expr="//div[hasclass('o_list_renderer')]" position="after">
            <div class="o_proid_list_footer d-flex justify-content-between align-items-center py-3 bg-white mt-auto w-100">
                <!-- Page size selector -->
                <div class="d-flex align-items-center ms-4">
                    <span class="me-2 fw-medium text-muted fs-7">Kết quả mỗi trang</span>
                    <select class="form-select form-select-sm fw-bold border-0 bg-light"
                        style="width: 70px;">
                        <option value="20">20</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                    </select>
                    <span class="ms-3 fw-medium text-muted fs-7">/ Tổng: 100</span>
                </div>

                <!-- Pagination controls -->
                <div class="o_proid_custom_pagination d-flex gap-2 align-items-center me-4">
                    <button class="btn btn-sm btn-white border shadow-sm text-muted px-2 py-1">
                        <i class="fa fa-angle-double-left" />
                    </button>
                    <button class="btn btn-sm btn-white border shadow-sm text-muted px-2 py-1">
                        <i class="fa fa-angle-left" />
                    </button>
                    
                    <button class="btn btn-sm btn-white border shadow-sm fw-bold text-muted px-3 py-1">01</button>
                    <button class="btn btn-sm text-white shadow-sm fw-bold px-3 py-1" style="background-color: #CC1A22;">02</button>
                    <button class="btn btn-sm btn-white text-muted px-2 py-1 border-0" disabled="">...</button>
                    <button class="btn btn-sm btn-white border shadow-sm fw-bold text-muted px-3 py-1">21</button>

                    <button class="btn btn-sm btn-white border shadow-sm text-muted px-2 py-1">
                        <i class="fa fa-angle-right" />
                    </button>
                    <button class="btn btn-sm btn-white border shadow-sm text-muted px-2 py-1">
                        <i class="fa fa-angle-double-right" />
                    </button>
                </div>
            </div>
        </xpath>
    </t>
</templates>
```

### Key Learning Points
- ✅ Extend ListRenderer for custom views
- ✅ Use `t-inherit` with mode="primary" to replace template
- ✅ Keep original functionality while adding new UI
- ✅ Register view with registry

---

## Summary: Common Patterns

| Pattern | Use Case | Key Components |
|---------|----------|-----------------|
| **Component** | Reusable UI element | `Component`, `useState`, Registry |
| **Field Widget** | Custom form field | `Component`, `supportedTypes`, Registry |
| **View** | Custom list/form layout | `Renderer`, `listView`, Registry |
| **Patch** | Extend core functionality | `patch()`, `super.setup()` |
| **Template Inherit** | Modify existing templates | `t-inherit`, `xpath`, positions |

---

## 🎯 Next Steps
- test các components trong form/list view
- Theo dõi console errors
- Dùng browser dev tools để validate HTML structure
- Test trên clean database
