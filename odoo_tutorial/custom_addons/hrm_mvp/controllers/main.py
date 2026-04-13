# -*- coding: utf-8 -*-
"""
Rita Chatbot API: returns raw Markdown for the frontend to render.
"""

import logging
import re

import requests
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class RitaChatbotController(http.Controller):
    @http.route('/api/chatbot/ask', type='jsonrpc', auth='user')
    def ask_chatbot(self, message):
        message = (message or "").strip()
        if not message:
            return {"markdown_text": "Vui lòng nhập câu hỏi."}

        context_text, match_info = self._get_employee_context(message)

        system_prompt = (
            "You are Rita, an HRM assistant in Odoo. "
            "Use the provided employee data when relevant. "
            "If the user asks about salary or employee info and no data is available, ask for the employee name. "
            "Reply in Vietnamese, concise, and format the answer in Markdown."
        )

        user_prompt = message
        if context_text:
            user_prompt = f"{message}\n\n{context_text}"
        if match_info:
            user_prompt = f"{user_prompt}\n\n{match_info}"

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "gemini-3-flash-preview:cloud",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "stream": False,
                },
                timeout=30,
            )
            response.raise_for_status()
            return {"markdown_text": response.json()["message"]["content"]}
        except Exception as exc:
            _logger.warning("Rita chatbot error: %s", exc)
            return {"markdown_text": "Xin lỗi, Rita đang bận. Vui lòng thử lại sau."}

    # Vietnamese stop-words that signal the name portion has ended.
    _STOP_WORDS = re.compile(
        r"\s+(?:đang|là|làm|có|không|gì|sao|vậy|thế|nào|ở|tại|của|và|với|cho|"
        r"được|bị|sẽ|đã|hay|hoặc|mà|nhưng|nếu|thì|vì|do|bởi)\b",
        re.IGNORECASE | re.UNICODE,
    )

    def _extract_employee_name(self, message):
        """
        Extract an employee name from a natural-language Vietnamese message.

        Strategy:
          1. Try structured keyword patterns to locate the name segment.
          2. Truncate the captured segment at the first Vietnamese stop-word
             so phrases like "Trí đang làm gì" yield only "Trí".

        Args:
            message (str): Raw user message text.

        Returns:
            str | None: Extracted name candidate, or None if not found.
        """
        patterns = [
            # Salary questions: "lương của Trí", "lương Trí"
            r"lương\s+(?:của\s+)?(.+)",
            r"salary\s+(?:of\s+)?(.+)",
            # Job / role questions: "nhân viên Trí đang làm gì"
            r"(?:nhân\s+viên|employee)\s+(.+)",
            # What does X do: "công việc của Trí", "Trí làm gì"
            r"(?:công\s+việc|vai\s+trò|vị\s+trí)\s+(?:của\s+)?(.+)",
            # Profile questions
            r"thông\s+tin\s+(?:của\s+)?(.+)",
            r"profile\s+(?:of\s+)?(.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, message, flags=re.IGNORECASE | re.UNICODE)
            if match:
                raw = match.group(1).strip()
                # Cut off at the first stop-word (e.g. "đang", "là", "làm"…)
                stop = self._STOP_WORDS.search(raw)
                name = raw[: stop.start()].strip() if stop else raw
                if name:
                    return name
        return None

    def _get_employee_context(self, message):
        name = self._extract_employee_name(message)
        if not name:
            return "", ""

        employees = request.env['hrm.employee'].search([('name', 'ilike', name)], limit=3)
        if not employees:
            return "", f"No employee found matching name: {name}."

        lines = ["Employee data (from HRM):"]
        for emp in employees:
            salary_display = f"{emp.salary} {emp.currency_id.name}" if emp.currency_id else str(emp.salary)
            lines.append(
                "- "
                f"Name: {emp.name}; "
                f"Code: {emp.employee_code or 'N/A'}; "
                f"Major: {emp.major or 'N/A'}; "
                f"Department: {emp.department or 'N/A'}; "
                f"Job Title: {emp.job_title or 'N/A'}; "
                f"Salary: {salary_display}"
            )
        return "\n".join(lines), ""
