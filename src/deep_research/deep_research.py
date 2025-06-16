"""
Deep Research System

This module implements an automated research workflow using multiple AI agents
to conduct comprehensive research on a given topic.
"""

import os
import asyncio
from typing import Optional

from tavily import AsyncTavilyClient
from llama_index.llms.ollama import Ollama
from config import config
from llama_index.core.workflow import (
    Context,
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)
from llama_index.core.agent.workflow import FunctionAgent

# Initialize core components
llm = Ollama(model=config.DEFAULT_MODEL,
                          timeout=300,
                          temperature=0.7,
                          context_window=4096,
                          num_ctx=4096)
tavily_api_key = os.environ.get("TAVILY_API_KEY")


# Event definitions
class GenerateEvent(Event):
    """Event for initiating research on a topic."""

    research_topic: str


class QuestionEvent(Event):
    """Event containing a research question."""

    question: str


class AnswerEvent(Event):
    """Event containing a question and its answer."""

    question: str
    answer: str


class ProgressEvent(Event):
    """Event for reporting workflow progress."""

    msg: str


class FeedbackEvent(Event):
    """Event containing feedback for improving research."""

    feedback: str


class ReviewEvent(Event):
    """Event containing a research report for review."""

    report: str


# Utility functions
async def search_web(query: str) -> str:
    """Search the web for information using Tavily API."""
    client = AsyncTavilyClient(api_key=tavily_api_key)
    return str(await client.search(query))


async def record_notes(ctx: Context, notes: str, notes_title: str) -> str:
    """Record research notes in the workflow context."""
    current_state = await ctx.get("state")
    if "research_notes" not in current_state:
        current_state["research_notes"] = {}
    current_state["research_notes"][notes_title] = notes
    await ctx.set("state", current_state)
    return "Notes recorded."


async def write_report(ctx: Context, report_content: str) -> str:
    """Write a research report to the workflow context."""
    current_state = await ctx.get("state")
    current_state["report_content"] = report_content
    await ctx.set("state", current_state)
    return "Report written."


async def review_report(ctx: Context, review: str) -> str:
    """Record a report review in the workflow context."""
    current_state = await ctx.get("state")
    current_state["review"] = review
    await ctx.set("state", current_state)
    return "Report reviewed."


# Agent definitions
question_agent = FunctionAgent(
    tools=[],
    llm=llm,
    verbose=False,
    system_prompt="""You are part of a deep research system.
    Given a research topic, generate a list of questions that will help create
    a comprehensive report. Provide one question per line without markdown or preamble.""",
)

answer_agent = FunctionAgent(
    tools=[search_web],
    llm=llm,
    verbose=False,
    system_prompt="""You are part of a deep research system.
    Given a specific question, provide a detailed answer using web search
    capabilities. Return only the answer without preamble or markdown.""",
)

report_agent = FunctionAgent(
    tools=[],
    llm=llm,
    verbose=False,
    system_prompt="""You are part of a deep research system.
    Given a set of question-answer pairs, synthesize them into a comprehensive report.""",
)

review_agent = FunctionAgent(
    tools=[],
    llm=llm,
    verbose=False,
    system_prompt="""You are part of a deep research system.
    Review a research report and either approve it as comprehensive or suggest
    additional questions for improvement.""",
)


class DeepResearchWithReflectionWorkflow(Workflow):
    """Workflow for conducting deep research with iterative improvement."""

    @step
    async def setup(self, ctx: Context, ev: StartEvent) -> GenerateEvent:
        """Initialize workflow components and start research."""
        self.question_agent = ev.question_agent
        self.answer_agent = ev.answer_agent
        self.report_agent = ev.report_agent
        self.review_agent = ev.review_agent
        self.review_cycles = 0

        ctx.write_event_to_stream(ProgressEvent(msg="Starting research"))
        return GenerateEvent(research_topic=ev.research_topic)

    @step
    async def generate_questions(
        self, ctx: Context, ev: GenerateEvent | FeedbackEvent
    ) -> QuestionEvent:
        """Generate research questions based on topic and feedback."""
        await ctx.set("research_topic", ev.research_topic)
        ctx.write_event_to_stream(
            ProgressEvent(msg=f"Research topic: {ev.research_topic}")
        )

        prompt = f"Generate questions on the topic: {ev.research_topic}"

        if isinstance(ev, FeedbackEvent):
            ctx.write_event_to_stream(
                ProgressEvent(msg=f"Processing feedback: {ev.feedback}")
            )
            prompt += (
                f"\nConsider previous feedback for additional questions: {ev.feedback}"
            )

        result = await self.question_agent.run(user_msg=prompt)
        questions = [line.strip() for line in str(result).split("\n") if line.strip()]

        await ctx.set("total_questions", len(questions))
        for question in questions:
            ctx.send_event(QuestionEvent(question=question))

    @step
    async def answer_question(self, ctx: Context, ev: QuestionEvent) -> AnswerEvent:
        """Generate an answer for a specific research question."""
        result = await self.answer_agent.run(
            user_msg=f"Research and answer: {ev.question}"
        )

        ctx.write_event_to_stream(
            ProgressEvent(
                msg=f"Answered question: {ev.question}\nAnswer: {str(result)}"
            )
        )

        return AnswerEvent(question=ev.question, answer=str(result))

    @step
    async def write_report(
        self, ctx: Context, ev: AnswerEvent
    ) -> Optional[ReviewEvent]:
        """Compile answers into a comprehensive report."""
        research = ctx.collect_events(
            ev, [AnswerEvent] * await ctx.get("total_questions")
        )
        if research is None:
            ctx.write_event_to_stream(ProgressEvent(msg="Collecting answers..."))
            return None

        ctx.write_event_to_stream(ProgressEvent(msg="Generating report..."))

        all_answers = "\n\n".join(
            f"Question: {qa.question}\nAnswer: {qa.answer}" for qa in research
        )

        result = await self.report_agent.run(
            user_msg=f"""Topic: {await ctx.get("research_topic")}
            Compile a comprehensive report from these Q&A pairs:
            {all_answers}"""
        )

        return ReviewEvent(report=str(result))

    @step
    async def review(self, ctx: Context, ev: ReviewEvent) -> StopEvent | FeedbackEvent:
        """Review the report and decide if more research is needed."""
        result = await self.review_agent.run(
            user_msg=f"""Review this report on {await ctx.get("research_topic")}:
            {ev.report}
            Respond with "ACCEPTABLE" if comprehensive, or suggest additional questions."""
        )

        self.review_cycles += 1
        if str(result) == "ACCEPTABLE" or self.review_cycles >= 3:
            return StopEvent(result=ev.report)

        ctx.write_event_to_stream(ProgressEvent(msg="Requesting additional research"))
        return FeedbackEvent(
            research_topic=await ctx.get("research_topic"), feedback=str(result)
        )


async def main():
    """Run the deep research workflow."""
    workflow = DeepResearchWithReflectionWorkflow(timeout=300)
    handler = workflow.run(
        research_topic="Comparison of AgenticAI frameworks: LangGraph, CrewAI, "
        "Google's Agent Development Kit, and LlamaIndex. "
        "Analyze key differences, strengths, and weaknesses.",
        question_agent=question_agent,
        answer_agent=answer_agent,
        report_agent=report_agent,
        review_agent=review_agent,
    )

    async for ev in handler.stream_events():
        if isinstance(ev, ProgressEvent):
            print(ev.msg)

    final_result = await handler
    print("==== Final Report ====")
    with open("./REPORT.md", "w") as f:
        f.write(final_result)


if __name__ == "__main__":
    asyncio.run(main())
