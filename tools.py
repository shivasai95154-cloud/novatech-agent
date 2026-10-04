import json
from pathlib import Path

from langchain_core.tools import tool


STATE_FILE = Path(__file__).parent / "system_state.json"


def load_system_state():
    """Load the current simulated NovaTech infrastructure state."""

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@tool
def check_system_health(system_name: str) -> str:
    """
    Check the current health of a NovaTech system.

    Valid systems are:
    vpn, website, database, email.
    """

    system_name = system_name.lower().strip()

    system_status = load_system_state()

    if system_name not in system_status:
        return (
            f"Unknown system: {system_name}. "
            "Valid systems are vpn, website, database, email."
        )

    system = system_status[system_name]

    return (
        f"System: {system_name}\n"
        f"Status: {system['status']}\n"
        f"Response time: {system['response_time_ms']} ms"
    )
