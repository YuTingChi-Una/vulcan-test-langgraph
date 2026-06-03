---
name: research-pipeline
license: MIT
description: >
  LangGraph skill for multi-agent research, writing, and review pipeline.
    Composes researcher, writer, and reviewer nodes in a StateGraph.
    tools:
      - name: web_search
          description: Search the web for information on any topic
            - name: read_file
                description: Read content from a local file
                  - name: execute_code
                      description: Execute Python code and return output
                      ---

                      # Research Pipeline Skill

                      Multi-agent LangGraph workflow: research a topic, write content, and review.

                      ## Nodes (Agents)
                      - **researcher**: Gathers information using web search.
                      - **writer**: Produces structured content from research.
                      - **reviewer**: Edits and validates the final output.

                      ## MCP Servers
                      - **Knowledge Base**: Streamable HTTP MCP (port 8010).
                      - **Filesystem**: stdio MCP for local file access.
                      
