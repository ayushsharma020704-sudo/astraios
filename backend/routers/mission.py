"""
Mission Planner router — POST /mission/plan
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter
from pydantic import BaseModel

from agents.crew import run_mission_crew

router = APIRouter(prefix="/mission", tags=["mission"])

_executor = ThreadPoolExecutor(max_workers=2)


class MissionPlanRequest(BaseModel):
    goal: str


@router.post("/plan")
async def plan_mission(request: MissionPlanRequest):
    """
    Run the CrewAI Mission Planner crew with the given goal.
    Runs the blocking crew.kickoff() in a thread pool to avoid
    blocking the async event loop.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        _executor, run_mission_crew, request.goal
    )
    return result
