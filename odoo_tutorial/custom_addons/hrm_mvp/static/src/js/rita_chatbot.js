/** @odoo-module **/

import { Component, markup, onMounted, onPatched, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

class RitaChatbot extends Component {
    setup() {
        this.state = useState({
            messages: [],
            inputText: "",
            loading: false,
        });
        this.scrollRef = useRef("scrollRef");
        this._msgId = 0;

        onMounted(() => this._scrollToBottom());
        onPatched(() => this._scrollToBottom());
    }

    _scrollToBottom() {
        const el = this.scrollRef.el;
        if (el) {
            el.scrollTop = el.scrollHeight;
        }
    }

    _escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
    }

    _fallbackMarkdown(raw) {
        const escaped = this._escapeHtml(raw);
        const bold = escaped.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
        const italic = bold.replace(/\*(.+?)\*/g, "<em>$1</em>");
        const code = italic.replace(/`([^`]+)`/g, "<code>$1</code>");
        const withBreaks = code.replace(/\n/g, "<br />");
        return `<p>${withBreaks}</p>`;
    }

    _parseMarkdown(raw) {
        let html = "";
        if (window.marked && typeof window.marked.parse === "function") {
            html = window.marked.parse(raw, { mangle: false, headerIds: false });
        } else {
            html = this._fallbackMarkdown(raw);
        }
        if (window.DOMPurify) {
            return window.DOMPurify.sanitize(html);
        }
        return html;
    }

    /**
     * Handles keyup event on the input field.
     * Triggers sendMessage only when the Enter key is pressed.
     * NOTE: OWL 2 does not support the `.enter` event modifier,
     *       so key checking must be done manually in the handler.
     *
     * @param {KeyboardEvent} ev
     */
    onKeyup(ev) {
        if (ev.key === "Enter") {
            this.sendMessage();
        }
    }

    async sendMessage() {
        const text = (this.state.inputText || "").trim();
        if (!text || this.state.loading) {
            return;
        }

        this.state.messages.push({
            id: ++this._msgId,
            role: "user",
            content: text,
        });
        this.state.inputText = "";
        this.state.loading = true;

        try {
            const result = await rpc("/api/chatbot/ask", { message: text });
            const rawMarkdown = (result && result.markdown_text) || "";
            const parsedHTML = this._parseMarkdown(rawMarkdown);
            this.state.messages.push({
                id: ++this._msgId,
                role: "bot",
                content: markup(parsedHTML),
            });
        } catch (err) {
            this.state.messages.push({
                id: ++this._msgId,
                role: "bot",
                content: markup("<em>Xin lỗi, Rita đang bận. Vui lòng thử lại sau.</em>"),
            });
        } finally {
            this.state.loading = false;
        }
    }
}

RitaChatbot.template = "hrm_mvp.RitaChatbot";

registry.category("actions").add("hrm_mvp.rita_chatbot", RitaChatbot);

export default RitaChatbot;
