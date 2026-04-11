# XML Templates - OWL Syntax & Inheritance

## 📌 Template Basics

### Template Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <!-- OWL Template -->
    <t t-name="module.template_name" owl="1">
        <div class="my-container">
            <!-- Content here -->
        </div>
    </t>

    <!-- Template Inheritance -->
    <t t-inherit="web.SomeTemplate" t-inherit-mode="extension" owl="1">
        <xpath expr="//selector" position="inside">
            <!-- New content -->
        </xpath>
    </t>
</templates>
```

### Key Attributes
- `t-name="module.name"` - Template identifier
- `owl="1"` - Enable OWL syntax (required!)
- `t-inherit="base.template"` - Inherit from another template
- `t-inherit-mode` - How to inherit (extension, primary)

---

## 🔤 Expression & Output

### Basic Output
```xml
<!-- Escape text (safe for XSS) -->
<t t-esc="value" />              <!-- "value" -->
<t t-esc="item.name" />          <!-- item.name -->

<!-- Raw HTML (dangerous!) -->
<t t-raw="html_string" />        <!-- Don't use unless necessary -->

<!-- Format string -->
<t t-attf-string="Hello #{name}" />
```

### Object/List Access
```xml
<!-- Object properties -->
<div><t t-esc="person.name" /></div>
<div><t t-esc="person.address.city" /></div>

<!-- Array access -->
<div><t t-esc="items[0].name" /></div>

<!-- Method calls -->
<div><t t-esc="getFormatted(value)" /></div>
```

### Conditionals
```xml
<!-- If -->
<div t-if="condition">Content</div>

<!-- If-Else -->
<div t-if="condition1">First</div>
<t t-elif="condition2">Second</t>
<t t-else="">Third</t>

<!-- Shorthand -->
<div t-if="item.active" class="active" />
<div t-else="" class="inactive" />
```

---

## 🔄 Loops (Foreach)

### Basic Foreach
```xml
<!-- Simple list -->
<t t-foreach="items" t-as="item">
    <div><t t-esc="item.name" /></div>
</t>

<!-- With index -->
<t t-foreach="items" t-as="item" t-key="item_index">
    <div><t t-esc="item_index" />: <t t-esc="item.name" /></div>
</t>

<!-- With unique key (better performance) -->
<t t-foreach="items" t-as="item" t-key="item.id">
    <div><t t-esc="item.name" /></div>
</t>
```

### Loop Variables
```xml
<t t-foreach="items" t-as="item">
    <!-- item_index      - 0-based index -->
    <!-- item_first      - true if first iteration -->
    <!-- item_last       - true if last iteration -->
    <!-- item_parity     - "even" or "odd" -->
    <!-- item_length     - total items count -->
    
    <div t-if="item_first" class="header">First: <t t-esc="item.name" /></div>
    <div t-elif="item_last" class="footer">Last: <t t-esc="item.name" /></div>
    <div t-else="">Other: <t t-esc="item.name" /> (<t t-esc="item_parity" />)</div>
</t>
```

---

## 🎨 Attribute Binding

### Static Attributes
```xml
<div class="container" id="main" data-value="test">Content</div>
```

### Dynamic Attributes
```xml
<!-- t-att-name="expression" -->
<div t-att-class="item.status">Class: <t t-esc="item.status" /></div>

<!-- t-att="object" -->
<div t-att="{ class: item.status, id: 'item_' + item.id }">
    Dynamic attributes
</div>

<!-- t-attf-name="format string" -->
<div t-attf-class="item-#{item.status} #{ item.active ? 'active' : '' }">
    Formatted class
</div>
```

### Common Patterns
```xml
<!-- Class based on condition -->
<div t-att-class="{ 'active': item.active, 'disabled': !item.enabled }">
    <t t-esc="item.name" />
</div>

<!-- Style binding -->
<div t-att-style="'color: ' + item.color + '; font-size: ' + item.fontSize + 'px'">
    Styled text
</div>

<!-- Conditional attributes -->
<input
    type="checkbox"
    t-att-checked="item.selected ? 'checked' : undefined"
    t-att-disabled="item.disabled ? 'disabled' : undefined"
/>
```

---

## ⚡ Event Handling

### Basic Events
```xml
<!-- Click events -->
<button t-on-click="onDeleteItem">Delete</button>
<button t-on-click="() => this.onSelectItem(item.id)">Select</button>

<!-- Input events -->
<input t-on-input="onSearchChange" />
<select t-on-change="onCategoryChange">...</select>

<!-- Form events -->
<form t-on-submit="onSubmitForm">...</form>
```

### Event Modifiers
```xml
<!-- .stop = preventDefault + stopPropagation -->
<button t-on-click.stop="onAction">Stop event</button>

<!-- .prevent = preventDefault -->
<a href="/" t-on-click.prevent="onCustomClick">Custom link</a>

<!-- Combine -->
<button t-on-click.stop.prevent="onAction">Fully stopped</button>
```

### Passing Data with Events
```xml
<!-- Pass item data -->
<button t-on-click="() => this.onEdit(item.id, item.name)">Edit</button>

<!-- Pass event data -->
<input t-on-input="(ev) => this.searchItems(ev.target.value)" />

<!-- With condition -->
<button
    t-on-click="item.editable ? () => this.onEdit(item.id) : undefined"
>
    Edit
</button>
```

---

## 🧩 Component Composition

### Include Component
```xml
<!-- Use component -->
<MyChildComponent
    items="state.items"
    selectedId="state.selectedId"
    onSelect="(id) => this.onSelectItem(id)"
/>

<!-- With dynamic props -->
<MyComponent
    t-props="{
        label: item.name,
        value: item.value,
        onChange: (v) => this.update(v),
    }"
/>
```

### Slots (t-set-slot)
```xml
<!-- Parent -->
<MyComponent>
    <t t-set-slot="header">
        <h1>Custom Header</h1>
    </t>
    <t t-set-slot="content">
        <p>Custom Content</p>
    </t>
</MyComponent>

<!-- Child template receives slots -->
<div>
    <div class="header"><t t-slot="header" /></div>
    <div class="content"><t t-slot="content" /></div>
</div>
```

---

## 🔗 Template Inheritance (t-inherit)

### Inheritance Mode: extension
```xml
<!-- Add/modify to existing template -->
<t t-inherit="web.NavBar" t-inherit-mode="extension" owl="1">
    <!-- Use xpath to target elements -->
    <xpath expr="//nav" position="inside">
        <div class="my-addon">New content</div>
    </xpath>
</t>
```

### Inheritance Mode: primary
```xml
<!-- Replace entire template -->
<t t-inherit="web.NavBar" t-inherit-mode="primary" owl="1">
    <!-- Complete new template content -->
    <nav class="custom-navbar">...</nav>
</t>
```

### XPath Positions
```xml
<!-- before - Insert before matched element -->
<xpath expr="//button[@id='save']" position="before">
    <button>Backup</button>
</xpath>

<!-- after - Insert after matched element -->
<xpath expr="//button[@id='save']" position="after">
    <button>Undo</button>
</xpath>

<!-- inside - Add inside matched element -->
<xpath expr="//div[@class='footer']" position="inside">
    <p>New footer content</p>
</xpath>

<!-- replace - Replace matched element -->
<xpath expr="//button[@id='old']" position="replace">
    <button id="new">New Button</button>
</xpath>

<!-- attributes - Modify attributes -->
<xpath expr="//div[@class='container']" position="attributes">
    <attribute name="class">new-class</attribute>
    <attribute name="data-id">123</attribute>
</xpath>

<!-- move - Move element before another -->
<xpath expr="//element1" position="move">before //element2</xpath>
```

### XPath Selectors
```xml
<!-- By tag -->
<xpath expr="//div" position="..." />

<!-- By class -->
<xpath expr="//div[hasclass('my-class')]" position="..." />

<!-- By id -->
<xpath expr="//div[@id='myid']" position="..." />

<!-- By attribute -->
<xpath expr="//button[@type='submit']" position="..." />

<!-- Combined -->
<xpath expr="//div[hasclass('my-class') and @id='myid']" position="..." />

<!-- Nth child -->
<xpath expr="//div[1]" position="..." />

<!-- Text content -->
<xpath expr="//button[text()='Save']" position="..." />
```

---

## 🧮 Utilities & Helpers

### t-call - Include template
```xml
<!-- Call another template -->
<t t-call="module.helper_template" />

<!-- With variables -->
<t t-call="module.item_template">
    <t t-set="item" t-value="current_item" />
    <t t-set="editable" t-value="true" />
</t>
```

### t-set - Define variable
```xml
<!-- Simple set -->
<t t-set="count" t-value="items.length" />

<!-- Use in template -->
<div>Total: <t t-esc="count" /></div>

<!-- Object set -->
<t t-set="data" t-value="{ name: item.name, id: item.id }" />
```

### Comments
```xml
<!-- This is visible in HTML -->
<!-- Use for documentation -->

<!-- Conditional comment (template directive) -->
<t t-if="debug">Debug info: <t t-esc="debugData" /></t>
```

---

## 💡 Complete Template Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">

    <!-- Main component template -->
    <t t-name="proid.ProductListTemplate" owl="1">
        <div class="o_product_container">
            <!-- Header -->
            <div class="o_header">
                <h1>Products</h1>
                <input
                    type="search"
                    placeholder="Search..."
                    t-on-input="(ev) => this.onSearch(ev.target.value)"
                    t-att-value="state.searchQuery"
                />
            </div>

            <!-- Loading state -->
            <t t-if="state.isLoading">
                <div class="text-muted p-5 text-center">
                    <i class="fa fa-spinner fa-spin" /> Loading...
                </div>
            </t>

            <!-- Empty state -->
            <t t-elif="state.products.length === 0">
                <div class="alert alert-info">
                    No products found.
                </div>
            </t>

            <!-- Products list -->
            <t t-else="">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Price</th>
                            <th>Category</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <t t-foreach="state.products" t-as="product" t-key="product.id">
                            <tr t-att-class="{ 'table-success': product.active, 'table-danger': !product.active }">
                                <td>
                                    <t t-esc="product.name" />
                                </td>
                                <td>
                                    <t t-esc="product.list_price" />
                                </td>
                                <td>
                                    <span class="badge bg-info">
                                        <t t-esc="product.category_id[1]" />
                                    </span>
                                </td>
                                <td>
                                    <button
                                        class="btn btn-sm btn-primary"
                                        t-on-click="() => this.onEdit(product.id)"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        class="btn btn-sm btn-danger"
                                        t-on-click.stop="() => this.onDelete(product.id)"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        </t>
                    </tbody>
                </table>
            </t>
        </div>
    </t>

    <!-- Child component template -->
    <t t-name="proid.ProductItemTemplate" owl="1">
        <div class="product-item" t-att-class="{ 'selected': isSelected }">
            <h4 t-esc="props.product.name" />
            <p class="text-muted">
                <t t-esc="props.product.description" />
            </p>
        </div>
    </t>

</templates>
```

---

## Tiếp Theo
- [4-patching.md](4-patching.md) - Advanced patching
- [5-registry.md](5-registry.md) - Registry system
