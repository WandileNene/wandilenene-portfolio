"""
Email service for sending contact form messages.
Supports SMTP email sending with fallback to logging if email is not configured.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP"""
    
    @staticmethod
    def send_contact_email(
        name: str,
        email: str,
        message: str,
        subject: Optional[str] = None
    ) -> bool:
        """
        Send a contact form email.
        
        Args:
            name: Name of the person sending the message
            email: Email address of the sender
            message: The message content
            subject: Optional subject line
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not settings.mail_enabled:
            logger.warning(
                f"Email sending is disabled. Contact form message from {name} ({email}): {message}"
            )
            return True  # Return True so form submission succeeds
        
        if not settings.mail_to:
            logger.error("MAIL_TO is not configured. Cannot send contact email.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{settings.mail_from_name} <{settings.mail_from}>"
            msg['To'] = settings.mail_to
            msg['Subject'] = subject or f"Portfolio Contact: Message from {name}"
            msg['Reply-To'] = email
            
            # Create HTML and plain text versions
            text_content = f"""
New Contact Form Message

From: {name}
Email: {email}
Subject: {subject or 'No subject'}

Message:
{message}

---
This message was sent via your portfolio contact form.
Reply to this email to respond directly to {email}.
            """.strip()
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #e0e0e0; border-radius: 0 0 8px 8px; }}
        .field {{ margin-bottom: 15px; }}
        .label {{ font-weight: bold; color: #6366F1; }}
        .value {{ margin-top: 5px; }}
        .message-box {{ background: white; padding: 15px; border-left: 4px solid #10B981; margin: 15px 0; }}
        .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="margin: 0;">📬 New Portfolio Contact Message</h2>
        </div>
        <div class="content">
            <div class="field">
                <div class="label">From:</div>
                <div class="value">{name}</div>
            </div>
            <div class="field">
                <div class="label">Email:</div>
                <div class="value"><a href="mailto:{email}">{email}</a></div>
            </div>
            <div class="field">
                <div class="label">Subject:</div>
                <div class="value">{subject or 'No subject'}</div>
            </div>
            <div class="field">
                <div class="label">Message:</div>
                <div class="message-box">{message.replace(chr(10), '<br>')}</div>
            </div>
        </div>
        <div class="footer">
            <p>This message was sent via your portfolio contact form.</p>
            <p>Reply to this email to respond directly to {email}.</p>
        </div>
    </div>
</body>
</html>
            """.strip()
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            if settings.smtp_ssl:
                server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
            else:
                server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
                if settings.smtp_tls:
                    server.starttls()
            
            if settings.smtp_username and settings.smtp_password:
                server.login(settings.smtp_username, settings.smtp_password)
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Contact email sent successfully from {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send contact email: {str(e)}")
            return False


email_service = EmailService()
