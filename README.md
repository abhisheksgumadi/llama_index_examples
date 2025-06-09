# LlamaIndex Agents

A collection of advanced AI agent systems built with LlamaIndex, demonstrating the power of multi-agent workflows for complex tasks. This repository contains implementations of sophisticated agent systems for web research and RAG (Retrieval-Augmented Generation) applications. All implementations are based on the examples and patterns found across different pages in the LlamaIndex documentation.

## Projects

### 1. Web Research Agent System
A multi-agent system that performs automated web research and report generation. The system employs four specialized agents working in sequence to produce comprehensive, well-researched reports on any given topic.

Key features:
- Automated web research using Tavily API
- Multi-agent collaboration
- Structured report generation
- Quality review process

[View Web Research Documentation](src/web_research/README.md)

### 2. Agentic RAG System
An advanced RAG implementation that combines the power of LlamaIndex with agent-based workflows for enhanced information retrieval and generation.

Key features:
- Custom RAG pipeline
- Agent-based query processing
- Enhanced context retrieval
- Flexible document handling

[View Agentic RAG Documentation](src/agentic_rag/README.md)

## Prerequisites

- Python 3.8+
- Ollama running locally
- Required API keys (Tavily, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llamaindex_agents.git
cd llamaindex_agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export TAVILY_API_KEY="your-tavily-api-key"
# Add other required API keys
```

## Project Structure

```
llamaindex_agents/
├── src/
│   ├── web_research/
│   │   ├── agents/
│   │   ├── agentic_workflow.py
│   │   ├── config.py
│   │   └── README.md
│   └── agentic_rag/
│       ├── llm_config.py
│       ├── config.py
│       └── README.md
├── requirements.txt
└── README.md
```

## Getting Started

Each project in this repository is self-contained and can be run independently. Please refer to the individual project READMEs for specific setup and usage instructions:

- [Web Research System Setup](src/web_research/README.md)
- [Agentic RAG System Setup](src/agentic_rag/README.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LlamaIndex](https://github.com/run-llama/llama_index) for the excellent framework
- [Ollama](https://github.com/ollama/ollama) for local LLM support
- [Tavily](https://tavily.com/) for web search capabilities
