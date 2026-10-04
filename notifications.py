import os
import smtplib

from email.message import EmailMessage


# -------------------------------------------------
# EMAIL CONFIGURATION
# -------------------------------------------------

def get_email_config():
    """
    Load email configuration from environment variables
    or Streamlit Secrets.
    """

    sender = os.getenv("EMAIL_SENDER")
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

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


# -------------------------------------------------
# GENERIC EMAIL FUNCTION
# -------------------------------------------------

def send_email(subject: str, body: str):
    """
    Send an email using Gmail SMTP.
    """

    sender, app_password, receiver = get_email_config()

    if not sender:
        raise ValueError("EMAIL_SENDER is missing.")

    if not app_password:
        raise ValueError("EMAIL_APP_PASSWORD is missing.")

    if not receiver:
        raise ValueError("EMAIL_RECEIVER is missing.")

    message = EmailMessage()

    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.set_content(body)

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


# -------------------------------------------------
# TEST EMAIL
# -------------------------------------------------

def send_test_email():

    subject = "NovaTech Agent - Test Notification"

    body = """
Hello,

This is a test notification from your
NovaTech Autonomous IT Operations Agent.

The email notification system is working.

NovaTech AI Operations Agent
"""

    return send_email(
        subject,
        body
    )


# -------------------------------------------------
# NEW INCIDENT EMAIL
# -------------------------------------------------

def send_incident_email(
    incident: dict,
    analysis: str
):

    incident_number = incident[
        "incident_number"
    ]

    system_name = incident[
        "system"
    ].upper()

    status = incident[
        "detected_status"
    ].upper()

    response_time = incident[
        "response_time_ms"
    ]

    detected_at = incident[
        "detected_at"
    ]

    subject = (
        f"🚨 NovaTech Incident "
        f"{incident_number} - "
        f"{system_name} {status}"
    )

    body = f"""
NOVATECH INFRASTRUCTURE ALERT

A new infrastructure incident has been
automatically detected.

Incident ID: {incident_number}
System: {system_name}
Status: {status}
Response Time: {response_time} ms
Detected At: {detected_at}

AI INCIDENT ANALYSIS
--------------------

{analysis}

The NovaTech monitoring system will continue
tracking this incident.

NovaTech AI Operations Agent
"""

    return send_email(
        subject,
        body
    )


# -------------------------------------------------
# INCIDENT RESOLUTION EMAIL
# -------------------------------------------------

def send_resolution_email(
    incident: dict
):

    incident_number = incident[
        "incident_number"
    ]

    system_name = incident[
        "system"
    ].upper()

    detected_at = incident[
        "detected_at"
    ]

    resolved_at = incident[
        "resolved_at"
    ]

    subject = (
        f"✅ NovaTech Incident "
        f"{incident_number} Resolved"
    )

    body = f"""
NOVATECH INCIDENT RESOLVED

The monitoring system has detected that
the affected service has recovered.

Incident ID: {incident_number}
System: {system_name}

Previous Status:
{incident['detected_status'].upper()}

Current Status:
HEALTHY

Detected At:
{detected_at}

Resolved At:
{resolved_at}

Incident Status:
RESOLVED

The incident has been automatically closed.

NovaTech AI Operations Agent
"""

    return send_email(
        subject,
        body
    )
