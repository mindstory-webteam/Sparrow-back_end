"""
main/emails.py
Email helpers for the Sparrow International site.

Career form submissions are always delivered to HR (Hr@sparrowgroup.in),
plus any extra addresses in settings.CAREER_NOTIFY_EMAILS. An optional
acknowledgement is sent back to the applicant.

Nothing here is allowed to raise: if SMTP fails, we log the error and the
application still stays safely in the database.
"""

import logging
import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils import timezone

logger = logging.getLogger(__name__)

# Every career application is emailed here.
HR_EMAIL = "Hr@sparrowgroup.in"


def career_recipients():
    """HR address + any extra addresses from settings.CAREER_NOTIFY_EMAILS (no duplicates)."""
    extra = getattr(settings, "CAREER_NOTIFY_EMAILS", []) or []
    if isinstance(extra, str):
        extra = [extra]
    recipients, seen = [], set()
    for addr in [HR_EMAIL, *extra]:
        addr = (addr or "").strip()
        if addr and addr.lower() not in seen:
            seen.add(addr.lower())
            recipients.append(addr)
    return recipients


# ──────────────────────────────────────────────────────────────
# Low-level sender
# ──────────────────────────────────────────────────────────────
def _deliver(subject, text_body, html_body, to_list, reply_to=None):
    """Actually open an SMTP connection and send. Never raises."""
    if not to_list:
        logger.warning("Email not sent — empty recipient list. Subject: %s", subject)
        return False
    try:
        connection = get_connection(fail_silently=False)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_list,
            reply_to=reply_to or None,
            connection=connection,
        )
        if html_body:
            msg.attach_alternative(html_body, "text/html")
        msg.send()
        logger.info("Email sent to %s | %s", ", ".join(to_list), subject)
        return True
    except Exception as exc:                      # noqa: BLE001
        logger.exception("Email FAILED to %s: %s", ", ".join(to_list), exc)
        return False


def _send(subject, text_body, html_body, to_list, reply_to=None):
    """Send synchronously or in a background thread (settings.EMAIL_SEND_ASYNC)."""
    if getattr(settings, "EMAIL_SEND_ASYNC", True):
        threading.Thread(
            target=_deliver,
            args=(subject, text_body, html_body, to_list, reply_to),
            daemon=True,
        ).start()
        return True
    return _deliver(subject, text_body, html_body, to_list, reply_to)


# ──────────────────────────────────────────────────────────────
# 1) Notification to the company
# ──────────────────────────────────────────────────────────────
def send_career_application_email(application, request=None):
    """
    `application` is a saved main.models.CareerApplication instance.
    Sends the full submitted data to settings.CAREER_NOTIFY_EMAILS.
    """
    company = getattr(settings, "COMPANY_NAME", "Sparrow International")
    applied = timezone.localtime(application.applied_date).strftime("%d %b %Y, %I:%M %p")

    admin_url = ""
    if request is not None:
        try:
            admin_url = request.build_absolute_uri(
                f"/admin/main/careerapplication/{application.pk}/change/"
            )
        except Exception:                          # noqa: BLE001
            admin_url = ""

    subject = f"New Job Application — {application.job_role} — {application.full_name}"

    text_body = f"""New career application received on the {company} website.

Name        : {application.full_name}
Email       : {application.email}
Phone       : {application.phone}
Job Role    : {application.job_role}
Applied On  : {applied}
Reference # : APP-{application.pk:05d}

Message / Cover Letter:
{application.message or '(not provided)'}

{('Open in admin: ' + admin_url) if admin_url else ''}

--
This is an automated message from the {company} website.
"""

    html_body = f"""\
<!DOCTYPE html>
<html>
<body style="margin:0;padding:24px;background:#f4f6f8;
             font-family:Arial,Helvetica,sans-serif;color:#222;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="max-width:640px;margin:0 auto;background:#ffffff;
                border-radius:10px;overflow:hidden;
                box-shadow:0 2px 10px rgba(0,0,0,.06);">
    <tr>
      <td style="background:#164476;padding:22px 28px;">
        <h2 style="margin:0;color:#ffffff;font-size:19px;">New Job Application</h2>
        <p style="margin:6px 0 0;color:#c9d8ea;font-size:12px;">{company} — Careers</p>
      </td>
    </tr>
    <tr>
      <td style="padding:24px 28px;">
        <table width="100%" cellpadding="8" cellspacing="0" style="font-size:14px;">
          <tr style="background:#f8fafc;">
            <td width="35%" style="font-weight:bold;">Full Name</td>
            <td>{application.full_name}</td>
          </tr>
          <tr>
            <td style="font-weight:bold;">Email</td>
            <td><a href="mailto:{application.email}"
                   style="color:#164476;">{application.email}</a></td>
          </tr>
          <tr style="background:#f8fafc;">
            <td style="font-weight:bold;">Phone</td>
            <td><a href="tel:{application.phone}"
                   style="color:#164476;">{application.phone}</a></td>
          </tr>
          <tr>
            <td style="font-weight:bold;">Job Role</td>
            <td>{application.job_role}</td>
          </tr>
          <tr style="background:#f8fafc;">
            <td style="font-weight:bold;">Applied On</td>
            <td>{applied}</td>
          </tr>
          <tr>
            <td style="font-weight:bold;">Reference</td>
            <td>APP-{application.pk:05d}</td>
          </tr>
        </table>

        <h4 style="margin:22px 0 8px;font-size:14px;color:#164476;">
          Message / Cover Letter
        </h4>
        <div style="background:#f8fafc;border-left:4px solid #164476;
                    padding:14px 16px;font-size:14px;line-height:1.6;
                    white-space:pre-wrap;">{application.message or '(not provided)'}</div>

        {f'<p style="margin-top:22px;"><a href="{admin_url}" style="background:#164476;color:#fff;padding:11px 20px;border-radius:6px;text-decoration:none;font-size:13px;display:inline-block;">Open in Admin Panel</a></p>' if admin_url else ''}
      </td>
    </tr>
    <tr>
      <td style="background:#f0f3f7;padding:14px 28px;font-size:11px;color:#77808c;">
        Automated notification from the {company} website. Reply directly to
        contact the applicant.
      </td>
    </tr>
  </table>
</body>
</html>"""

    return _send(
        subject=subject,
        text_body=text_body,
        html_body=html_body,
        to_list=career_recipients(),
        # Hitting "Reply" in Gmail replies to the applicant, not to the server.
        reply_to=[application.email],
    )


# ──────────────────────────────────────────────────────────────
# 2) Acknowledgement to the applicant
# ──────────────────────────────────────────────────────────────
def send_applicant_acknowledgement(application):
    if not getattr(settings, "SEND_APPLICANT_ACKNOWLEDGEMENT", False):
        return False

    company = getattr(settings, "COMPANY_NAME", "Sparrow International")
    subject = f"We received your application — {company}"

    text_body = f"""Dear {application.full_name},

Thank you for applying for the position of {application.job_role} at {company}.

We have received your application (reference APP-{application.pk:05d}) and our
team will review it shortly. If your profile matches the requirements, we will
contact you on {application.phone} or at this email address.

Warm regards,
HR Team
{company}
"""

    html_body = f"""\
<!DOCTYPE html>
<html>
<body style="margin:0;padding:24px;background:#f4f6f8;
             font-family:Arial,Helvetica,sans-serif;color:#222;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="max-width:600px;margin:0 auto;background:#fff;
                border-radius:10px;overflow:hidden;">
    <tr>
      <td style="background:#164476;padding:22px 28px;">
        <h2 style="margin:0;color:#fff;font-size:19px;">Application Received</h2>
      </td>
    </tr>
    <tr>
      <td style="padding:26px 28px;font-size:14px;line-height:1.7;">
        <p style="margin-top:0;">Dear <strong>{application.full_name}</strong>,</p>
        <p>Thank you for applying for the position of
           <strong>{application.job_role}</strong> at {company}.</p>
        <p>Your application has been received. Reference number:
           <strong>APP-{application.pk:05d}</strong>.</p>
        <p>Our team will review your profile and get in touch if it matches
           our current requirements.</p>
        <p style="margin-bottom:0;">Warm regards,<br>
           <strong>HR Team</strong><br>{company}</p>
      </td>
    </tr>
    <tr>
      <td style="background:#f0f3f7;padding:14px 28px;font-size:11px;color:#77808c;">
        This is an automated confirmation — please do not reply.
      </td>
    </tr>
  </table>
</body>
</html>"""

    return _send(subject, text_body, html_body, [application.email])