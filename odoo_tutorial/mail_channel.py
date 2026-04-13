# name: mail_channel.py
# description: Customizations to OdooBot behavior, overriding default responses with a connected LLM agent.

from odoo import models, api
import requests
import logging

_logger = logging.getLogger(__name__)



class MailBot(models.AbstractModel):
    """
    name: Mail Bot
    description: Inherits the mail.bot model in Odoo >= 17 to customize OdooBot's response behavior using an LLM API.
    """
    _inherit = 'mail.bot'

    def _get_answer(self, channel, body, values, command=False):
        """
        Overrides the default OdooBot response to call a local LLM via HTTP request.
        
        Args:
            channel (record): The discuss.channel where the message was posted.
            body (str): The body content of the user's message.
            values (dict): Message values.
            command (str, optional): The command executed, if any. Defaults to False.
        
        Returns:
            str or list: The generated answer from the LLM, or the default fallback response.
        """
        odoobot = self.env.ref("base.partner_root")
        
        # Only intervene if the user is chatting directly with OdooBot
        if channel.channel_type == "chat" and odoobot in channel.channel_member_ids.partner_id:
            try:
                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "gemini-3-flash-preview:cloud",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are OdooBot, a smart virtual assistant in Odoo. Please reply concisely and helpfully."
                            },
                            {"role": "user", "content": body}
                        ],
                        "stream": False,
                    },
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()["message"]["content"]
    
            except Exception as e:
                _logger.warning("LLM agent did not respond, using fallback: %s", e)
                
        # Fallback to the default OdooBot behavior
        return super()._get_answer(channel, body, values, command)