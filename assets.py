from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
      messages: Annotated[list, operator.add]
      next: str

# ===== AGENT =====
def research_agent(state: AgentState):
      """Agent: Gathers information on the given topic."""
      return {"messages": [{"role": "assistant", "content": "Research complete"}], "next": "writer"}

def writer_agent(state: AgentState):
      """Agent: Writes content based on research findings."""
      return {"messages": [{"role": "assistant", "content": "Writing complete"}], "next": "reviewer"}

def reviewer_agent(state: AgentState):
      """Agent: Reviews and improves the written content."""
      return {"messages": [{"role": "assistant", "content": "Review complete"}], "next": END}

# ===== TOOL =====
@tool
def web_search(query: str) -> str:
      """Search the web for information on the given query."""
      return f"Search results for: {query}"

@tool
def read_file(filepath: str) -> str:
      """Read content from a local file."""
      return f"Contents of: {filepath}"

@tool
def execute_code(code: str) -> str:
      """Execute Python code and return the output."""
      return f"Executed: {code[:100]}"

# ===== SKILL =====
def build_research_pipeline():
      """Skill: Multi-agent research and writing pipeline."""
      graph = StateGraph(AgentState)
      graph.add_node("researcher", research_agent)
      graph.add_node("writer", writer_agent)
      graph.add_node("reviewer", reviewer_agent)
      graph.set_entry_point("researcher")
      graph.add_conditional_edges("researcher", lambda s: s["next"], {"writer": "writer"})
      graph.add_conditional_edges("writer", lambda s: s["next"], {"reviewer": "reviewer"})
      graph.add_edge("reviewer", END)
      return graph.compile()

def build_quick_summary_pipeline():
      """Skill: Single-agent quick summarization."""
      graph = StateGraph(AgentState)
      graph.add_node("researcher", research_agent)
      graph.set_entry_point("researcher")
      graph.add_edge("researcher", END)
      return graph.compile()

# ===== MCP SERVER =====
MCP_SERVER_CONFIG = {
      "name": "LangGraph MCP Server",
      "version": "1.0.0",
      "transport": "stdio",
      "tools": [
                {"name": "web_search", "description": "Search the web"},
                {"name": "read_file", "description": "Read files"},
                {"name": "execute_code", "description": "Run Python code"},
      ],
}

# ===== AI MODEL =====
gpt4o = ChatOpenAI(model="gpt-4o", temperature=0)
gpt4o_mini = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
claude_sonnet = ChatOpenAI(model="claude-3-5-sonnet-20241022", temperature=0.5)

# ===== OTHER =====
class WorkflowVisualizer:
      """Utility to inspect and visualize LangGraph workflows."""

    def list_nodes(self, app) -> list:
              return list(app.nodes.keys())

    def to_mermaid(self, nodes: list) -> str:
              lines = ["graph TD"]
              for i in range(len(nodes) - 1):
                            lines.append(f"  {nodes[i]} --> {nodes[i+1]}")
                        return "\n".join(lines)
