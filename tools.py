from langchain_core.tools import tool


# Simulated NovaTech infrastructure.
# Later this will be replaced by real APIs/monitoring services.
SYSTEM_STATUS = {
    "vpn": {
        "status": "healthy",
        "response_time_ms": 45
    },
    "website": {
        "status": "healthy",
        "response_time_ms": 120
    },
    "database": {
        "status": "healthy",
        "response_time_ms": 30
    },
    "email": {
        "status": "healthy",
        "response_time_ms": 80
    }
}


@tool
def check_system_health(system_name: str) -> str:
    """
    Check the current health of a NovaTech system.

    Valid systems are:
    vpn, website, database, email.
    """

    system_name = system_name.lower().strip()

    if system_name not in SYSTEM_STATUS:
        return (
            f"Unknown system: {system_name}. "
            "Valid systems are vpn, website, database, email."
        )

    system = SYSTEM_STATUS[system_name]

    return (
        f"System: {system_name}\n"
        f"Status: {system['status']}\n"
        f"Response time: {system['response_time_ms']} ms"
    )
