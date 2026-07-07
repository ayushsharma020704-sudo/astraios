"""
Mock Orbital Mechanics Tool — returns hardcoded trajectory/delta-v data.
Will be replaced with real orbital computation engine later.
"""

from crewai.tools import tool


@tool("Orbital Mechanics Calculator")
def orbital_mechanics_tool(query: str) -> str:
    """Computes interstellar/interplanetary trajectory parameters.
    Input should describe the mission destination and objectives.
    Returns delta-v budget, transfer type, travel time, and fuel estimates."""
    return (
        "=== Orbital Mechanics Computation ===\n"
        f"Mission Parameters: {query}\n\n"
        "Trajectory Analysis:\n"
        "  Transfer Type : Hohmann-equivalent interstellar transfer\n"
        "  Total Delta-V : 0.1c (30,000 km/s) — theoretical light-sail\n"
        "  Cruise Velocity : 0.05c (15,000 km/s) sustained\n"
        "  Estimated Travel Time : ~28,000 years (conventional)\n"
        "  With Light-Sail : ~26 years at 0.05c\n\n"
        "Fuel & Propulsion:\n"
        "  Propulsion Type : Laser-driven light sail (Breakthrough Starshot-class)\n"
        "  Sail Area : 16 m² (4m × 4m)\n"
        "  Sail Mass : 1 gram (nanoscale)\n"
        "  Laser Array Power : 100 GW (ground-based)\n"
        "  Acceleration Phase : 10 minutes to 0.05c\n\n"
        "Orbital Insertion:\n"
        "  Braking Method : Magnetic sail / stellar photon braking\n"
        "  Capture Orbit : 1.05 AU circular orbit around Kepler-452\n"
        "  Orbital Period : ~390 days\n\n"
        "Launch Windows:\n"
        "  Optimal Window : Year-round (interstellar — no planetary alignment needed)\n"
        "  Recommended : Align with minimal solar interference"
    )
