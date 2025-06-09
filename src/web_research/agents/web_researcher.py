from llama_index.core.agent.workflow import FunctionAgent
from llama_index.tools.tavily_research.base import TavilyToolSpec
from llama_index.core.workflow import Context
import os

async def record_notes(ctx: Context, notes: str, notes_title: str) -> str:
    """Useful for recording notes on a given topic."""
    current_state = await ctx.get("state")
    if "research_notes" not in current_state:
        current_state["research_notes"] = {}
    current_state["research_notes"][notes_title] = notes
    await ctx.set("state", current_state)
    return "Notes recorded."

def create_web_researcher() -> FunctionAgent:
    return FunctionAgent(
        name="WebResearcher",
        description="Useful for searching the web for information on a given topic and recording notes on the topic.",
        system_prompt="""You are the ResearchAgent that can search the web for information on a given topic and record notes on the topic.
        Once notes are recorded and you are satisfied, you should hand off control to the ReportWriter to write a report on the topic.""",
        tools=[TavilyToolSpec(api_key=os.environ.get("TAVILY_API_KEY")).to_tool_list()[0], record_notes],
        can_handoff_to=["ReportWriter"]
    ) 