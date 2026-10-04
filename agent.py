def analyze_incident(incident: dict) -> str:
    """
    Automatically analyze an infrastructure incident.
    This function is called by the monitor, not by the user.
    """

    llm = create_llm()

    system_name = incident["system"]
    status = incident["status"]
    response_time = incident["response_time_ms"]

    prompt = f"""
You are NovaTech's autonomous IT Operations Incident Analyst.

An infrastructure monitoring system has automatically detected
the following incident:

System: {system_name}
Status: {status}
Response Time: {response_time} ms

Analyze this incident.

Return a concise incident report containing exactly these sections:

Severity:
Business Impact:
Likely Cause:
Recommended Action:

Severity must be one of:
LOW
MEDIUM
HIGH
CRITICAL

Do not claim that you performed actions that you have not actually performed.
"""

    response = llm.invoke(prompt)

    return response.content
