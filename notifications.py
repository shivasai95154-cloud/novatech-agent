import os
import smtplib

from email.message import EmailMessage


def get_email_config():
    """
    Load email configuration from environment variables
    or Streamlit Secrets.
    """

    sender = os.getenv("EMAIL_SENDER")
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    # If environment variables are unavailable,
    # try Streamlit Secrets.
    try:
        import streamlit as st

        if not sender and "EMAIL_SENDER" in st.secrets:
            sender = st.secrets["EMAIL_SENDER"]

        if not app_password and "EMAIL_APP_PASSWORD" in st.secrets:
            app_password = st.secrets["EMAIL_APP_PASSWORD"]

        if not receiver and "EMAIL_RECEIVER" in st.secrets:
            receiver = st.secrets["EMAIL_RECEIVER"]

    except Exception:
        pass

    return sender, app_password, receiver


def send_email(subject: str, body: str):
    """
    Send an email notification using Gmail SMTP.
    """

    sender, app_password, receiver = get_email_config()

    if not sender:
        raise ValueError(
            "EMAIL_SENDER is missing."
        )

    if not app_password:
        raise ValueError(
            "EMAIL_APP_PASSWORD is missing."
        )

    if not receiver:
        raise ValueError(
            "EMAIL_RECEIVER is missing."
        )

    message = EmailMessage()

    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.set_content(body)

    # Connect securely to Gmail SMTP.
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender,
            app_password
        )

        smtp.send_message(
            message
        )

    return True


def send_test_email():
    """
    Send a simple test notification.
    """

    subject = (
        "NovaTech Agent - Test Notification"
    )

    body = """
Hello,

This is a test notification from your
NovaTech Autonomous IT Operations Agent.

If you received this email, the email
notification system is working correctly.

NovaTech AI Operations Agent
"""

    return send_email(
        subject,
        body
    )
