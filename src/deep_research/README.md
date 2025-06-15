# Deep Research System

This is heavily inspired from excellent documentations and tutorials from LlamaIndex. A sophisticated automated research workflow system that leverages multiple AI agents to conduct comprehensive research on any given topic. The system uses LlamaIndex's workflow capabilities along with Ollama for LLM processing and Tavily for web search functionality.

## Overview

The Deep Research System is designed to automate the research process through a multi-agent workflow that:
1. Generates relevant research questions
2. Searches and answers each question
3. Compiles comprehensive reports
4. Reviews and iteratively improves the research

## System Architecture

The system consists of several key components:

### Agents
- **Question Agent**: Generates relevant research questions based on the topic
- **Answer Agent**: Searches the web and provides detailed answers to questions
- **Report Agent**: Synthesizes Q&A pairs into a comprehensive report
- **Review Agent**: Evaluates report quality and suggests improvements

### Workflow
The system implements a `DeepResearchWithReflectionWorkflow` that orchestrates the research process through these steps:
1. Setup and initialization
2. Question generation
3. Answer collection
4. Report compilation
5. Review and iteration

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Tavily API key

## Installation

1. Install the required dependencies:
```bash
pip install llama-index tavily-python
```

2. Set up your environment variables:
```bash
export TAVILY_API_KEY="your_tavily_api_key"
```

## Configuration

The system uses a configuration file (`config.py`) that specifies:
- Default LLM model (currently set to "qwen2.5:14b-instruct-q4_K_M")

## Usage

To run the deep research system:

```python
from deep_research import main

# Run the research workflow
await main()
```

The system will:
1. Accept a research topic
2. Generate relevant questions
3. Search for answers
4. Compile a comprehensive report
5. Review and iterate if necessary

## Features

- **Automated Research**: Conducts thorough research on any given topic
- **Web Search Integration**: Uses Tavily API for real-time web searches
- **Iterative Improvement**: Reviews and refines research through multiple cycles
- **Progress Tracking**: Monitors and reports workflow progress
- **Flexible Configuration**: Customizable LLM models and parameters

## Workflow Events

The system uses several event types to manage the research process:
- `GenerateEvent`: Initiates research on a topic
- `QuestionEvent`: Contains research questions
- `AnswerEvent`: Contains question-answer pairs
- `ProgressEvent`: Reports workflow progress
- `FeedbackEvent`: Contains improvement suggestions
- `ReviewEvent`: Contains research reports for review

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your license information here] 