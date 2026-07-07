"""
Mock Risk Assessment Tool — returns hardcoded radiation/risk data.
Will be replaced with real risk-modelling APIs later.
"""

from crewai.tools import tool


@tool("Mission Risk Assessor")
def risk_assessment_tool(query: str) -> str:
    """Assesses mission risks including radiation exposure, micrometeorite hazards,
    communication delays, and life-support margins.
    Input should describe the mission profile and destination."""
    return (
        "=== Mission Risk Assessment ===\n"
        f"Mission Profile: {query}\n\n"
        "Radiation Environment:\n"
        "  Galactic Cosmic Rays : 0.4 Sv/year (interstellar cruise)\n"
        "  Solar Particle Events : N/A (beyond heliosphere)\n"
        "  Destination Stellar Flux : 1.1x Solar — moderate UV\n"
        "  Shielding Requirement : 20 g/cm² polyethylene equivalent\n"
        "  Crew Dose (26-yr trip) : ~10.4 Sv — EXCEEDS safe limits\n"
        "  Mitigation : Hibernation pods + active magnetic shielding\n\n"
        "Micrometeorite Hazard:\n"
        "  Interstellar Medium Density : ~1 atom/cm³\n"
        "  Impact Probability (>1mm) : 0.02% per year\n"
        "  Cumulative Risk (26 yr) : 0.5%\n"
        "  Shield : Whipple bumper (dual-wall) rated to 1 cm particles\n\n"
        "Communication:\n"
        "  One-Way Light Delay : 1,402 years\n"
        "  Practical Comms : Laser-link with relay probes every 100 ly\n"
        "  Data Rate at Destination : ~1 kbps (estimated)\n\n"
        "Life Support (crewed variant):\n"
        "  O₂ Recycling Margin : 15% above nominal\n"
        "  Water Recovery Rate : 98.5%\n"
        "  Food Production : Hydroponic bays — 2,200 kcal/person/day\n"
        "  Psychological Risk : HIGH — multi-generational isolation\n\n"
        "Overall Risk Rating: HIGH\n"
        "Recommendation: Proceed with robotic probe first; crewed mission requires "
        "breakthrough propulsion and hibernation technology."
    )
