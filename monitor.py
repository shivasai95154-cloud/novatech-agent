from tools import load_system_state
from agent import analyze_incident

from incident_db import (
    create_incident,
    get_open_incident,
    resolve_incident
)


def check_infrastructure():
    """
    Check all NovaTech systems and return unhealthy systems.
    """

    system_state = load_system_state()

    incidents = []

    for system_name, details in system_state.items():

        status = details.get(
            "status",
            "unknown"
        )

        response_time = details.get(
            "response_time_ms",
            0
        )

        if status.lower() != "healthy":

            incidents.append(
                {
                    "system": system_name,
                    "status": status,
                    "response_time_ms": response_time
                }
            )

    return incidents


def analyze_detected_incident(incident):
    """
    Send a detected incident to the AI
    for automatic analysis.
    """

    return analyze_incident(
        incident
    )


def process_incidents():
    """
    Compare current infrastructure state against
    existing incidents in the database.

    Creates incidents for newly unhealthy systems.

    Resolves incidents when systems recover.
    """

    system_state = load_system_state()

    new_incidents = []
    existing_incidents = []
    resolved_incidents = []


    for system_name, details in system_state.items():

        status = details.get(
            "status",
            "unknown"
        )

        response_time = details.get(
            "response_time_ms",
            0
        )


        # -----------------------------------------
        # SYSTEM IS UNHEALTHY
        # -----------------------------------------

        if status.lower() != "healthy":

            incident_data = {
                "system": system_name,
                "status": status,
                "response_time_ms": response_time
            }


            incident_record, created = (
                create_incident(
                    incident_data
                )
            )


            if created:

                new_incidents.append(
                    incident_record
                )

            else:

                existing_incidents.append(
                    incident_record
                )


        # -----------------------------------------
        # SYSTEM IS HEALTHY
        # -----------------------------------------

        else:

            open_incident = (
                get_open_incident(
                    system_name
                )
            )


            if open_incident:

                resolved_record, resolved = (
                    resolve_incident(
                        system_name
                    )
                )


                if resolved:

                    resolved_incidents.append(
                        resolved_record
                    )


    return {
        "new": new_incidents,
        "existing": existing_incidents,
        "resolved": resolved_incidents
    }


def run_monitor():
    """
    Run one complete monitoring cycle.
    """

    print(
        "NovaTech Infrastructure Monitor"
    )

    print(
        "--------------------------------"
    )


    results = process_incidents()


    # ---------------------------------------------
    # NEW INCIDENTS
    # ---------------------------------------------

    for incident in results["new"]:

        print()

        print(
            f"NEW INCIDENT: "
            f"{incident['incident_number']}"
        )

        print(
            f"System: "
            f"{incident['system']}"
        )

        print(
            f"Status: "
            f"{incident['detected_status']}"
        )


        ai_incident = {
            "system": incident["system"],
            "status": incident[
                "detected_status"
            ],
            "response_time_ms": incident[
                "response_time_ms"
            ]
        }


        analysis = analyze_incident(
            ai_incident
        )


        print()

        print(
            "AI INCIDENT ANALYSIS"
        )

        print(
            "--------------------"
        )

        print(
            analysis
        )


    # ---------------------------------------------
    # EXISTING INCIDENTS
    # ---------------------------------------------

    for incident in results["existing"]:

        print()

        print(
            f"Incident "
            f"{incident['incident_number']} "
            f"is still OPEN."
        )


    # ---------------------------------------------
    # RESOLVED INCIDENTS
    # ---------------------------------------------

    for incident in results["resolved"]:

        print()

        print(
            f"RESOLVED: "
            f"{incident['incident_number']}"
        )

        print(
            f"System: "
            f"{incident['system']}"
        )


    # ---------------------------------------------
    # NOTHING HAPPENING
    # ---------------------------------------------

    if (
        not results["new"]
        and not results["existing"]
        and not results["resolved"]
    ):

        print(
            "All NovaTech systems are healthy."
        )


if __name__ == "__main__":

    run_monitor()
