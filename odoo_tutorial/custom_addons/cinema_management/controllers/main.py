# controllers/ollama_controller.py

import json
import requests
import logging
import re
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gpt-oss:20b-cloud"  # hoặc "mistral", "phi3", v.v.


class OllamaBotController(http.Controller):

    @http.route('/ollama/chat', type='json', auth='public', methods=['POST'])
    def chat_with_ollama(self, message, channel_id=None, **kwargs):
        """
        Endpoint nhận tin nhắn từ OdooBot và trả lời bằng Ollama.
        """
        if not message:
            return {'error': 'Tin nhắn không được để trống.'}

        try:
            # Lấy lịch sử hội thoại nếu có channel_id
            history = self._get_chat_history(channel_id) if channel_id else []

            # Gửi đến Ollama
            response_text = self._call_ollama(message, history)

            # Lưu tin nhắn vào channel nếu có
            if channel_id:
                self._post_odoobot_reply(channel_id, response_text)

            return {'response': response_text}

        except Exception as e:
            _logger.error("Lỗi khi gọi Ollama: %s", str(e))
            return {'error': str(e)}

    def _call_ollama(self, user_message, history=None):
        """Gọi Ollama API và trả về nội dung phản hồi."""
        messages = [
            {
                "role": "system",
                "content": (
                    "Bạn là OdooBot, trợ lý ảo thông minh trong hệ thống ERP Odoo. "
                    "QUY TẮC BẮT BUỘC: Bạn PHẢI trả lời 100% bằng định dạng HTML thuần túy. "
                    "Sử dụng các thẻ HTML như <b> để in đậm, <br> để xuống dòng, <ul><li> để tạo danh sách."
                )
            }
        ]

        # Thêm lịch sử hội thoại
        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,  # Tắt streaming để dễ xử lý
        }

        resp = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()

        data = resp.json()
        content = data["message"]["content"]

        # Xử lý: Nếu model vẫn lỳ lợm trả về Markdown, ta chủ động convert một số thẻ cơ bản sang HTML
        # In đậm
        content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
        # In nghiêng
        content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
        # Xuống dòng
        content = content.replace('\n', '<br/>')

        return content

    def _get_chat_history(self, channel_id, limit=10):
        """Lấy lịch sử tin nhắn từ mail.channel để duy trì ngữ cảnh."""
        channel = request.env['mail.channel'].browse(int(channel_id))
        messages = channel.message_ids.sorted('date')[-limit:]

        history = []
        for msg in messages:
            if msg.author_id == request.env.ref('base.partner_root'):
                # Tin nhắn của bot (OdooBot)
                history.append({"role": "assistant", "content": msg.body or ""})
            else:
                history.append({"role": "user", "content": msg.body or ""})
        return history

    def _post_odoobot_reply(self, channel_id, message_text):
        """Đăng phản hồi vào channel dưới danh nghĩa OdooBot."""
        channel = request.env['mail.channel'].browse(int(channel_id))
        odoobot = request.env.ref('base.partner_root')

        channel.sudo().with_context(mail_create_nosubscribe=True).message_post(
            body=message_text,
            author_id=odoobot.id,
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )