# Web Research System Architecture

```mermaid
graph TD
    subgraph "Web Research System"
        User[User Input] --> |Research Topic| Planner[Research Planner]
        
        subgraph "Research Planning Phase"
            Planner --> |Analyzes Topic| Subtopics[Identifies Subtopics]
            Planner --> |Generates| Queries[Search Queries]
            Planner --> |Creates| Outline[Report Outline]
        end
        
        subgraph "Research Execution Phase"
            Queries --> |Uses| Tavily[Tavily API]
            Tavily --> |Gathers| Researcher[Web Researcher]
            Researcher --> |Organizes| Notes[Research Notes]
        end
        
        subgraph "Report Generation Phase"
            Notes --> |Structures| Writer[Report Writer]
            Writer --> |Formats| Report[Markdown Report]
        end
        
        subgraph "Quality Assurance Phase"
            Report --> |Reviews| Reviewer[Quality Reviewer]
            Reviewer --> |Provides| Feedback[Improvement Feedback]
            Feedback --> |Updates| Report
        end
        
        Report --> |Final Output| User
    end
    
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Planner fill:#bbf,stroke:#333,stroke-width:2px
    style Researcher fill:#bfb,stroke:#333,stroke-width:2px
    style Writer fill:#fbb,stroke:#333,stroke-width:2px
    style Reviewer fill:#fbf,stroke:#333,stroke-width:2px
```

## System Components

1. **Research Planner**
   - Input: Research topic from user
   - Output: Structured research plan
   - Responsibilities:
     - Topic analysis
     - Subtopics identification
     - Search query generation
     - Report outline creation

2. **Web Researcher**
   - Input: Search queries from planner
   - Output: Organized research notes
   - Responsibilities:
     - Web search execution via Tavily API
     - Information gathering
     - Research note organization

3. **Report Writer**
   - Input: Research notes
   - Output: Structured markdown report
   - Responsibilities:
     - Content structuring
     - Markdown formatting
     - Logical flow management

4. **Quality Reviewer**
   - Input: Draft report
   - Output: Reviewed and improved report
   - Responsibilities:
     - Content review
     - Feedback generation
     - Accuracy verification

## Data Flow

1. User provides research topic
2. Research Planner creates structured plan
3. Web Researcher gathers information
4. Report Writer creates initial report
5. Quality Reviewer improves report
6. Final report delivered to user

## External Dependencies

- **Ollama**: Local LLM service running Qwen2.5 model
- **Tavily API**: Web search service for research 