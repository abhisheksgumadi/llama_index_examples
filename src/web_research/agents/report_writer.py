from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context


async def write_report(ctx: Context, report_content: str) -> str:
    """Useful for writing a report on a given topic."""
    current_state = await ctx.get("state")
    current_state["report_content"] = report_content
    await ctx.set("state", current_state)
    return "Report written."


def create_report_writer() -> FunctionAgent:
    return FunctionAgent(
        name="ReportWriter",
        description="Useful for writing a report on a given topic.",
        system_prompt=(
            "You are the WriteAgent that can write a report on a given topic. "
            "Your report should be in a markdown format. The content should be grounded in the research notes. "
            "Once the report is written, you should get feedback at least once from the QualityReviewer."
        ),
        tools=[write_report],
        can_handoff_to=["QualityReviewer", "WebResearcher"],
    )
