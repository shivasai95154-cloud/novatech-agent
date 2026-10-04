from tools import load_system_state
from agent import analyze_incident


def check_infrastructure():
    """
    Check all NovaTech systems and return unhealthy systems.
    """

    system_state = load_system_state()

    incidents = []

    for system_name, details in system_state.items():

        status = details.get("status", "unknown")
        response_time = details.get("response_time_ms", 0)

        if status.lower() != "healthy":

            incident = {
                "system": system_name,
                "status": status,
                "response_time_ms": response_time
            }

            incidents.append(incident)

    return incidents


def analyze_detected_incident(incident):
    """
    Send a detected infrastructure incident
    to the NovaTech AI Agent for analysis.
    """

    return analyze_incident(incident)


def run_monitor():

    print("NovaTech Infrastructure Monitor")
    print("--------------------------------")

    incidents = check_infrastructure()

    if not incidents:

        print("All NovaTech systems are healthy.")
        return

    print(
        f"Detected {len(incidents)} incident(s)."
    )

    for incident in incidents:

        print()
        print("INCIDENT DETECTED")
        print(
            f"System: {incident['system']}"
        )
        print(
            f"Status: {incident['status']}"
        )
        print(
            f"Response time: "
            f"{incident['response_time_ms']} ms"
        )

        print()
        print("AI INCIDENT ANALYSIS")
        print("--------------------")

        analysis = analyze_detected_incident(
            incident
        )

        print(analysis)


if __name__ == "__main__":
    run_monitor()
