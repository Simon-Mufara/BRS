"""
Email utility for BuildRight Solutions document automation agent.
Handles sending generated PDFs via email.
"""

from __future__ import annotations

import smtplib
import ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
from typing import List, Optional

import brs_agent.config as C


def send_email(
    to_email: str,
    subject: str,
    body: str,
    attachments: List[str] | None = None,
    from_email: str | None = None,
    smtp_server: str | None = None,
    smtp_port: int | None = None,
    username: str | None = None,
    password: str | None = None,
    use_tls: bool = True,
) -> bool:
    """
    Send an email with optional attachments.

    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (plain text)
        attachments: List of file paths to attach
        from_email: Sender email (defaults to company email)
        smtp_server: SMTP server hostname
        smtp_port: SMTP server port
        username: SMTP username
        password: SMTP password
        use_tls: Whether to use TLS encryption

    Returns:
        True if email sent successfully, False otherwise
    """
    # Use defaults from config if not provided
    if from_email is None:
        from_email = C.EMAIL

    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add body
    msg.attach(MIMEText(body, 'plain'))

    # Add attachments
    if attachments:
        for file_path in attachments:
            if Path(file_path).exists():
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {Path(file_path).name}',
                )
                msg.attach(part)

    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server or "localhost", smtp_port or 587) as server:
            if use_tls:
                server.starttls(context=context)
            if username and password:
                server.login(username, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_document_email(
    to_email: str,
    document_path: str,
    document_type: str,
    client_name: str = "",
    additional_message: str = "",
    **email_kwargs
) -> bool:
    """
    Convenience function to send a generated document via email.

    Args:
        to_email: Recipient email address
        document_path: Path to the generated PDF document
        document_type: Type of document (quotation, invoice, etc.)
        client_name: Name of the client (for personalization)
        additional_message: Additional message to include in email
        **email_kwargs: Additional arguments passed to send_email()

    Returns:
        True if email sent successfully, False otherwise
    """
    # Default email content
    subject = f"{C.COMPANY_NAME} - {document_type.title()} for {client_name or 'Client'}"

    body = f"""
Dear {client_name or 'Valued Client'},

Please find attached your {document_type.lower()} from {C.COMPANY_NAME}.

{additional_message}

{C.TAGLINE}

---
{C.COMPANY_NAME}
Reg. No: {C.REG_NUMBER}
{C.ADDRESS_LINE1}
Email: {C.EMAIL}
    """.strip()

    return send_email(
        to_email=to_email,
        subject=subject,
        body=body,
        attachments=[document_path],
        **email_kwargs
    )