from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import (
    AgentWorkflow,
    AgentOutput,
    ToolCall,
    ToolCallResult,
)
from llama_index.tools.tavily_research.base import TavilyToolSpec
from llama_index.core.workflow import Context
import asyncio
from config import config
from agents.research_planner import create_research_planner
from agents.web_researcher import create_web_researcher
from agents.report_writer import create_report_writer
from agents.quality_reviewer import create_quality_reviewer
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer


async def main():
    Settings.llm = Ollama(
        model=config.DEFAULT_MODEL,
        timeout=300,
        temperature=0.7,
        context_window=4096,
        num_ctx=4096,
    )

    # Create agents
    research_planner = create_research_planner()
    web_researcher = create_web_researcher()
    report_writer = create_report_writer()
    quality_reviewer = create_quality_reviewer()

    # Create workflow
    workflow = AgentWorkflow(
        agents=[research_planner, web_researcher, report_writer, quality_reviewer],
        root_agent=research_planner.name,
        initial_state={
            "research_notes": {},
            "report_content": "Not written yet.",
            "review": "Review required.",
        },
    )

    # Run workflow
    handler = workflow.run(
        user_msg="Create comprehensive report on relationship between Donald Trump and Vladmir Putin."
    )

    # Stream progress
    current_agent = None
    async for event in handler.stream_events():
        if (
            hasattr(event, "current_agent_name")
            and event.current_agent_name != current_agent
        ):
            current_agent = event.current_agent_name
            print(f"\n{'='*50}")
            print(f"Agent: {current_agent}")
            print(f"{'='*50}\n")
        elif isinstance(event, AgentOutput):
            if event.response.content:
                print("Output:", event.response.content)
            if event.tool_calls:
                print(
                    "Planning to use tools:",
                    [call.tool_name for call in event.tool_calls],
                )
        elif isinstance(event, ToolCallResult):
            print(f"Tool Result ({event.tool_name}):")
            print(f"  Arguments: {event.tool_kwargs}")
            print(f"  Output: {event.tool_output}")
        elif isinstance(event, ToolCall):
            print(f"Calling Tool: {event.tool_name}")
            print(f"  With arguments: {event.tool_kwargs}")

    print(workflow.initial_state)


if __name__ == "__main__":
    asyncio.run(main())
