# UI Blocking & Navigation Race Conditions

## 🚨 Issue: UI Freeze during Tab/Navigation Switch

This is a common pitfall when building custom Navigation Bars or navigation `<a>` tags in Odoo without properly synchronizing them with the system's data-saving process.

### 📋 Scenario Description
1. The user is in a Form view and has modified some data (Dirty state).
2. The user clicks a link (`<a>` tag) or a tab button on your custom navigation bar.
3. **Two processes occur simultaneously:**
   - **Process A:** Your browser or custom JS tries to switch the page/tab.
   - **Process B:** Odoo triggers its automatic save mechanism (Auto-save).
4. If **Process B (Save)** fails (e.g., due to a missing required field), Odoo will:
   - Display an error notification.
   - Activate `blockUI` (shows a loading spinner and blocks all user interaction).
5. **The Problem:** When the user clicks "OK" to close the error dialog, `Process A` might still be running or have interrupted Odoo's internal event loop, causing the "Unblock UI" command to be skipped or fail to execute.
6. **Result:** The screen remains "frozen" under a gray overlay/spinner even though the error dialog is closed.

---

## 🔍 Technical Root Cause

In Odoo, the `ui` service manages the blocking state. When an `RPC` call fails and has the `blockUI: true` attribute, the system increments a `blockCount`. If your navigation process interferes with the event loop or causes a conflict in Promise management, the `unblock()` command might never be triggered.

---

## 🛠️ Solution 1: Proper Event Management

Always ensure that click events on your custom navigation bar are strictly controlled by preventing default behavior and stopping event bubbling.

```javascript
// Inside your component
onNavClick(ev) {
    ev.preventDefault();  // Prevent the <a> tag from immediately reloading the page
    ev.stopPropagation(); // Stop the event from bubbling up to Odoo's parent elements
    
    // Perform your tab switching logic safely
    this.actionService.doAction(...);
}
```

---

## 🛠️ Solution 2: Patching FormController for Forced Unblocking

This is the most robust way to ensure the UI is always unblocked when an error occurs, regardless of any parallel navigation processes.

### Code Patch (static/src/js/patches/form_controller_patch.js)

```javascript
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";

patch(FormController.prototype, {
    setup() {
        super.setup();
        this.uiService = useService("ui");
    },

    /**
     * Override the save error handler
     */
    async onSaveError(error) {
        // Call Odoo's default error handling logic
        const result = await super.onSaveError(error);
        
        // FORCED UNBLOCK: Ensure UI is always unblocked 
        // even if parallel navigation processes are running
        if (this.uiService.isBlocked) {
            this.uiService.unblock();
        }
        
        return result;
    }
});
```

---

## 💡 Key Takeaways for Developers

1. **Don't fight the framework:** Odoo has a powerful auto-save mechanism. When implementing custom navigation, always check if the record is "dirty" (modified but not saved).
2. **Async synchronization:** Always `await` commands related to data saving or navigation to ensure they execute in the correct order.
3. **UI Service is key:** If you encounter a frozen gray screen, check the `uiService` and the `blockCount` state.

---

## 🔗 Related Documentation
- [3-patching_system.md](3-patching_system.md) - How to use patches
- [1-owl_components.md](1-owl_components.md) - Event handling in OWL
