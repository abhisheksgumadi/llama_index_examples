from llama_index.core.agent.workflow import FunctionAgent

def create_research_planner() -> FunctionAgent:
    return FunctionAgent(
        name="ResearchPlanner",
        description="Creates search strategies and report outlines",
        system_prompt="""You are an expert research planner for any given topic. You understand the topic and:
        1. Identify key subtopics (political, personal, economic)
        2. Generate 5 search queries per subtopic
        3. Create report outline with sections. You then hand off the control to the WebResearcher to search the web for information on the topic.""",
        tools=[],
        can_handoff_to=["WebResearcher"]
    ) 