"""
Mock NASA Exoplanet Tool — returns hardcoded sample exoplanet data.
Will be replaced with real NASA Exoplanet Archive API calls later.
"""

from crewai.tools import tool


@tool("NASA Exoplanet Database")
def nasa_exoplanet_tool(query: str) -> str:
    """Fetches exoplanet data from NASA's Exoplanet Archive.
    Input should be the name of an exoplanet or a search query.
    Returns planetary characteristics, host star data, and habitability info."""
    return (
        "=== NASA Exoplanet Archive Results ===\n"
        f"Query: {query}\n\n"
        "Target: Kepler-452b\n"
        "  Discovery Year : 2015\n"
        "  Discovery Method : Transit\n"
        "  Distance : 1,402 light-years (430 pc)\n"
        "  Orbital Period : 384.843 days\n"
        "  Semi-major Axis : 1.046 AU\n"
        "  Planet Radius : 1.63 Earth radii\n"
        "  Equilibrium Temp : ~265 K (-8°C)\n"
        "  Insolation Flux : 1.10 Earth flux\n\n"
        "Host Star: Kepler-452\n"
        "  Spectral Type : G2V (Sun-like)\n"
        "  Age : ~6 billion years\n"
        "  Temperature : 5,757 K\n"
        "  Radius : 1.11 Solar radii\n"
        "  Luminosity : 1.2 Solar luminosities\n\n"
        "Habitability Assessment:\n"
        "  Habitable Zone : YES — within the conservative HZ\n"
        "  Earth Similarity Index : 0.83\n"
        "  Note : Often called 'Earth's older cousin'; rocky composition likely"
    )
