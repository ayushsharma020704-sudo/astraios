"""
ASTRAIOS Mission Planner — CrewAI Crew definition.

Assembles 4 agents (Astronomer, Mission Architect, Cosmic Historian, Risk Analyst)
into a sequential crew that produces a combined mission plan.
"""

from __future__ import annotations

import os
import time
from crewai import Agent, Crew, LLM, Process, Task
import litellm

from agents.config import AGENT_CONFIGS
from agents.tools.nasa_tool import nasa_exoplanet_tool
from agents.tools.orbital_tool import orbital_mechanics_tool
from agents.tools.historian_tool import cosmic_historian_tool
from agents.tools.risk_tool import risk_assessment_tool
from core.config import settings

# ---------------------------------------------------------------------------
# Ensure API keys are in env for litellm (used by CrewAI under the hood)
# ---------------------------------------------------------------------------
os.environ.setdefault("GROQ_API_KEY", settings.GROQ_API_KEY)
os.environ.setdefault("GEMINI_API_KEY", settings.GOOGLE_AI_STUDIO_KEY)

# ---------------------------------------------------------------------------
# LiteLLM Configuration & Patches
# ---------------------------------------------------------------------------

# Built-in litellm retries for transient rate limit hits (adds 3 retries with exponential backoff)
litellm.num_retries = 3

_original_completion = litellm.completion

def _patched_completion(*args, **kwargs):
    # Patch 1: Groq cache_breakpoint removal
    messages = kwargs.get("messages", [])
    for m in messages:
        if isinstance(m, dict) and "cache_breakpoint" in m:
            del m["cache_breakpoint"]
            
    if "cache_breakpoint" in kwargs:
        del kwargs["cache_breakpoint"]
        
    return _original_completion(*args, **kwargs)

litellm.completion = _patched_completion

# ---------------------------------------------------------------------------
# Pacing hooks
# ---------------------------------------------------------------------------

def pace_llm_execution(*args, **kwargs):
    """
    Called after every agent step to space out LLM calls and avoid RPM limits.
    Gemini free tier has 5 RPM limit, 13 seconds keeps us safe!
    """
    time.sleep(13)

# ---------------------------------------------------------------------------
# Crew builder
# ---------------------------------------------------------------------------

def build_crew(goal: str) -> Crew:
    """Build and return the 4-agent Mission Planner crew for a given goal."""

    gemini_llm = "gemini/gemini-2.0-flash"

    # ── Agents (Segregated by LLM Provider) ────────────────────────────────
    
    astronomer = Agent(
        **AGENT_CONFIGS["astronomer"],
        tools=[nasa_exoplanet_tool],
        llm=gemini_llm,
        verbose=True,
    )

    architect = Agent(
        **AGENT_CONFIGS["architect"],
        tools=[orbital_mechanics_tool],
        llm=gemini_llm,
        verbose=True,
    )

    historian = Agent(
        **AGENT_CONFIGS["historian"],
        tools=[cosmic_historian_tool],
        llm=gemini_llm,
        verbose=True,
    )

    risk_analyst = Agent(
        **AGENT_CONFIGS["risk_analyst"],
        tools=[risk_assessment_tool],
        llm=gemini_llm,
        verbose=True,
    )

    # ── Tasks ─────────────────────────────────────────────────────────────
    task_astronomer = Task(
        description=(
            f"Analyze the target for the following mission goal: '{goal}'. "
            "Use the NASA Exoplanet Database tool to gather all relevant data about "
            "the target world — distance, size, orbital parameters, host star type, "
            "and habitability assessment. Summarize your findings clearly."
        ),
        expected_output=(
            "A detailed astronomical profile of the target exoplanet including "
            "distance, radius, orbital period, host star properties, and "
            "habitability assessment."
        ),
        agent=astronomer,
    )

    task_architect = Task(
        description=(
            f"Design a mission trajectory for: '{goal}'. "
            "Use the Orbital Mechanics Calculator to determine the optimal transfer "
            "type, delta-v budget, travel time, propulsion options, and orbital "
            "insertion strategy. Build on the astronomer's target data."
        ),
        expected_output=(
            "A mission flight plan covering propulsion type, delta-v budget, "
            "travel time, launch windows, and orbital insertion strategy."
        ),
        agent=architect,
    )

    task_historian = Task(
        description=(
            f"Provide historical and scientific context for: '{goal}'. "
            "Use the Cosmic History Archive to find relevant precedents, "
            "discoveries, and historical milestones related to this mission. "
            "Connect the mission to humanity's broader journey of exploration."
        ),
        expected_output=(
            "A narrative connecting the mission to key historical milestones, "
            "past discoveries, and scientific context."
        ),
        agent=historian,
    )

    task_risk = Task(
        description=(
            f"Assess all risks for: '{goal}'. "
            "Use the Mission Risk Assessor to evaluate radiation exposure, "
            "micrometeorite hazards, communication challenges, and life-support "
            "requirements. Provide a risk rating and mitigation recommendations."
        ),
        expected_output=(
            "A comprehensive risk assessment with quantified hazard levels, "
            "cumulative risks, mitigation strategies, and an overall risk rating."
        ),
        agent=risk_analyst,
    )

    # ── Crew ──────────────────────────────────────────────────────────────
    crew = Crew(
        agents=[astronomer, architect, historian, risk_analyst],
        tasks=[task_astronomer, task_architect, task_historian, task_risk],
        process=Process.sequential,
        step_callback=pace_llm_execution, # Pauses 13s after every agent step
        verbose=True,
    )

    return crew


def run_mission_crew(goal: str) -> dict:
    """
    Build and kick off the mission planner crew (synchronous).
    Returns a dict with the final combined output.
    """
    crew = build_crew(goal)
    result = crew.kickoff()

    # Extract individual agent task outputs (sequential order guarantees alignment)
    outputs = result.tasks_output if hasattr(result, "tasks_output") else []
    
    return {
        "goal": goal,
        "status": "completed",
        "astronomer": outputs[0].raw if len(outputs) > 0 else None,
        "mission_architect": outputs[1].raw if len(outputs) > 1 else None,
        "historian": outputs[2].raw if len(outputs) > 2 else None,
        "risk_analyst": outputs[3].raw if len(outputs) > 3 else None,
        "result": str(result), # The final combined summary / final task output
        "token_usage": getattr(result, "token_usage", None),
    }


