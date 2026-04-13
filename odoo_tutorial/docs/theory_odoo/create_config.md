# Creating Configuration Settings in Odoo

This document explains how to implement a configuration settings page in Odoo (v17/18/19), allowing users to define global parameters that can be used across the module.

## 1. Model Implementation

To create settings, you must inherit from `res.config.settings`. This is a `TransientModel`, meaning data is NOT stored in the model's table but rather in the system parameters (`ir.config_parameter`).

### Example: `res_config_setting.py`
```python
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # The config_parameter attribute automatically saves/loads the value to ir.config_parameter
    ticket_price = fields.Integer(
        string="Ticket Price", 
        config_parameter="cinema_management.ticket_price"
    )
```

## 2. View Implementation

The UI for settings must inherit from the base Odoo settings view.

### Example: `res_config_setting.xml`
```xml
<record id="res_config_settings_view_form" model="ir.ui.view">
    <field name="name">res.config.settings.view.form.inherit.cinema</field>
    <field name="model">res.config.settings</field>
    <field name="priority" eval="90"/>
    <field name="inherit_id" ref="base.res_config_settings_view_form"/>
    <field name="arch" type="xml">
        <xpath expr="//form" position="inside">
            <app data-string="Cinema Manager" string="Cinema Manager" name="cinema_management">
                <block title="Movie Showings">
                    <setting id="ticket_price" string="Ticket price" help="Sets the default price for every movie showing">
                        <field name="ticket_price"/>
                    </setting>
                </block>
            </app>
        </xpath>
    </field>
</record>
```

## 3. Action and Menu Item

To make the settings accessible from the module menu, you need a Window Action and a Menu Item.

### Window Action
```xml
<record id="action_cinema_configuration" model="ir.actions.act_window">
    <field name="name">Configuration</field>
    <field name="res_model">res.config.settings</field>
    <field name="view_mode">form</field>
    <field name="target">current</field>
    <field name="context">{'module': 'cinema_management'}</field>
</record>
```

### Menu Item
```xml
<menuitem id="menu_configuration" 
          name="Configuration" 
          parent="menu_movie_root" 
          action="action_cinema_configuration" 
          sequence="100"/>
```

## 4. Consuming Values in Other Models

Once the value is saved in the system parameters, you can fetch it using the `ir.config_parameter` model.

### Accessing the Value
To get a value from Python code:
```python
value = self.env['ir.config_parameter'].sudo().get_param('prefix.parameter_name', default_value)
```

### Setting a Dynamic Default Value
In your target model, you can use a lambda function to always pull the latest configuration value when a new record is created.

```python
class MovieShowing(models.Model):
    _name = 'movie.showing'

    price = fields.Integer(
        string="Price", 
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
            'cinema_management.ticket_price', default=0
        )
    )
```

> [!TIP]
> Always use `.sudo()` when calling `get_param` if the current user might not have access to the configuration settings model.
