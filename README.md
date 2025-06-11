# LlamaIndex Agents

A collection of advanced AI agent systems built with LlamaIndex, demonstrating the power of multi-agent workflows for complex tasks. This repository contains implementations of sophisticated agent systems for web research, RAG (Retrieval-Augmented Generation) applications, and Message Control Protocol (MCP) implementations. All implementations are based on the examples and patterns found across different pages in the LlamaIndex documentation.

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

### 3. Simple MCP System
A straightforward implementation of the Message Control Protocol (MCP) using FastMCP and LlamaIndex. This system demonstrates how to create a server that exposes tools and a client that can interact with these tools using an LLM agent.

Key features:
- FastMCP server implementation
- Tool exposure and management
- LLM agent integration
- Simple calculator tool demonstration

[View Simple MCP Documentation](src/simple_mcp/README.md)

## Prerequisites

- Python 3.8+
- Ollama running locally
- Required API keys (Tavily, etc.)
- FastMCP for MCP implementations
