"""
main/zeptomail_backend.py

Django email backend that sends through Zoho ZeptoMail's HTTPS API
instead of SMTP. Use it on servers where SMTP ports (25/465/587) are
blocked, e.g. DigitalOcean droplets.

settings.py:
    EMAIL_BACKEND     = 'main.zeptomail_backend.ZeptoMailBackend'
    ZEPTOMAIL_TOKEN   = '...'   # Send Mail Token from ZeptoMail → Mail Agent → SMTP/API → API
    ZEPTOMAIL_API_URL = 'https://api.zeptomail.in/v1.1/email'   # India data centre
    DEFAULT_FROM_EMAIL = 'Sparrow International Website <hr@sparrowgroup.in>'

All existing code (send_mail, EmailMultiAlternatives, main/emails.py) keeps
working unchanged — only the delivery method changes.
"""

import base64
import json
import logging
import mimetypes
import urllib.error
import urllib.request
from email.utils import parseaddr

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://api.zeptomail.in/v1.1/email"


class ZeptoMailError(Exception):
    pass


class ZeptoMailBackend(BaseEmailBackend):

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        token = (getattr(settings, "ZEPTOMAIL_TOKEN", "") or "").strip()
        # Accept the token with or without the "Zoho-enczapikey " prefix
        if token.lower().startswith("zoho-enczapikey"):
            token = token.split(None, 1)[1] if " " in token else ""
        self.token = token
        self.api_url = getattr(settings, "ZEPTOMAIL_API_URL", DEFAULT_API_URL)
        self.timeout = getattr(settings, "EMAIL_TIMEOUT", None) or 20
        self.bounce_address = getattr(settings, "ZEPTOMAIL_BOUNCE_ADDRESS", "")

    # ── public API ────────────────────────────────────────────────
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        sent = 0
        for message in email_messages:
            try:
                self._send(message)
                sent += 1
            except Exception:
                logger.exception("ZeptoMail send failed: %s", getattr(message, "subject", ""))
                if not self.fail_silently:
                    raise
        return sent

    # ── helpers ───────────────────────────────────────────────────
    @staticmethod
    def _addr(value):
        name, address = parseaddr(value)
        item = {"address": address}
        if name:
            item["name"] = name
        return item

    def _recipients(self, addresses):
        return [{"email_address": self._addr(a)} for a in addresses if a]

    def _build_payload(self, message):
        from_email = message.from_email or settings.DEFAULT_FROM_EMAIL
        payload = {
            "from": self._addr(from_email),
            "to": self._recipients(message.to),
            "subject": message.subject or "",
        }
        if message.cc:
            payload["cc"] = self._recipients(message.cc)
        if message.bcc:
            payload["bcc"] = self._recipients(message.bcc)
        if message.reply_to:
            payload["reply_to"] = [self._addr(a) for a in message.reply_to]
        if self.bounce_address:
            payload["bounce_address"] = self.bounce_address

        # Body: plain text + optional HTML alternative
        html = None
        if getattr(message, "content_subtype", "plain") == "html":
            html = message.body
        else:
            if message.body:
                payload["textbody"] = message.body
        for alt in getattr(message, "alternatives", []) or []:
            content, mimetype = alt[0], alt[1]
            if mimetype == "text/html":
                html = content
        if html:
            payload["htmlbody"] = html
        if "textbody" not in payload and "htmlbody" not in payload:
            payload["textbody"] = " "

        # Attachments added with message.attach(name, content, mimetype)
        attachments = []
        for att in getattr(message, "attachments", []) or []:
            if isinstance(att, tuple) or hasattr(att, "filename"):
                name, content, mimetype = att[0], att[1], att[2] if len(att) > 2 else None
                if isinstance(content, str):
                    content = content.encode("utf-8")
                attachments.append({
                    "name": name or "attachment",
                    "mime_type": mimetype or mimetypes.guess_type(name or "")[0] or "application/octet-stream",
                    "content": base64.b64encode(content).decode("ascii"),
                })
        if attachments:
            payload["attachments"] = attachments
        return payload

    def _send(self, message):
        if not self.token:
            raise ZeptoMailError("ZEPTOMAIL_TOKEN is not set in settings.py")
        if not message.to and not message.cc and not message.bcc:
            raise ZeptoMailError("Email has no recipients")

        data = json.dumps(self._build_payload(message)).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=data,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Zoho-enczapikey {self.token}",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8", "replace")
                logger.info("ZeptoMail accepted email to %s (HTTP %s)", ", ".join(message.to), response.status)
                return body
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            raise ZeptoMailError(f"ZeptoMail HTTP {exc.code}: {detail}") from None
        except urllib.error.URLError as exc:
            raise ZeptoMailError(f"Cannot reach ZeptoMail ({self.api_url}): {exc.reason}") from None