from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context

async def review_report(ctx: Context, review: str) -> str:
    """Useful for reviewing a report and providing feedback."""
    current_state = await ctx.get("state")
    current_state["review"] = review
    await ctx.set("state", current_state)
    return "Report reviewed."

def create_quality_reviewer() -> FunctionAgent:
    return FunctionAgent(
        name="QualityReviewer",
        description="Useful for reviewing a report and providing feedback.",
        system_prompt=(
            "You are the ReviewAgent that can review a report and provide feedback."       
            "Your feedback should either approve the current report or request changes for the WriteAgent to implement."
        ),
        tools=[review_report],
        can_handoff_to=["WriteAgent"],
    ) 