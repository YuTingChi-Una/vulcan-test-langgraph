"""LangGraph agent, tool, skill, and MCP definitions."""
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import TypedDict, Annotated
import operator

# ===== AI MODELS =====
gpt4o = ChatOpenAI(model="gpt-4o", temperature=0)
gpt4o_mini = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# ===== MCP SERVERS =====
mcp_client = MultiServerMCPClient({
    "knowledge_base": {
            "url": "http://localhost:8010/mcp",
                    "transport": "streamable_http",
                        },
                            "filesystem": {
                                    "command": "npx",
                                            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
                                                    "transport": "stdio",
                                                        },
                                                        })

                                                        # ===== TOOLS =====
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

                                                                                # ===== AGENTS (graph nodes) =====
                                                                                class AgentState(TypedDict):
                                                                                    messages: Annotated[list, operator.add]
                                                                                        next: str

                                                                                        def research_agent(state: AgentState) -> AgentState:
                                                                                            """Agent: Gathers information on the given topic using web search."""
                                                                                                return {"messages": [{"role": "assistant", "content": "Research complete"}], "next": "writer"}

                                                                                                def writer_agent(state: AgentState) -> AgentState:
                                                                                                    """Agent: Writes content based on research findings."""
                                                                                                        return {"messages": [{"role": "assistant", "content": "Writing complete"}], "next": "reviewer"}
                                                                                                        
                                                                                                        def reviewer_agent(state: AgentState) -> AgentState:
                                                                                                            """Agent: Reviews and improves written content for quality."""
                                                                                                                return {"messages": [{"role": "assistant", "content": "Review complete"}], "next": END}
                                                                                                                
                                                                                                                # ===== SKILLS (compiled graphs) =====
                                                                                                                def build_research_pipeline() -> StateGraph:
                                                                                                                    """Skill: Multi-agent research, writing, and review pipeline."""
                                                                                                                        graph = StateGraph(AgentState)
                                                                                                                            graph.add_node("researcher", research_agent)
                                                                                                                                graph.add_node("writer", writer_agent)
                                                                                                                                    graph.add_node("reviewer", reviewer_agent)
                                                                                                                                        graph.set_entry_point("researcher")
                                                                                                                                            graph.add_conditional_edges("researcher", lambda s: s["next"], {"writer": "writer"})
                                                                                                                                                graph.add_conditional_edges("writer", lambda s: s["next"], {"reviewer": "reviewer"})
                                                                                                                                                    graph.add_edge("reviewer", END)
                                                                                                                                                        return graph.compile()
                                                                                                                                                        
                                                                                                                                                        def build_quick_summary() -> StateGraph:
                                                                                                                                                            """Skill: Single-agent quick research and summarization."""
                                                                                                                                                                graph = StateGraph(AgentState)
                                                                                                                                                                    graph.add_node("researcher", research_agent)
                                                                                                                                                                        graph.set_entry_point("researcher")
                                                                                                                                                                            graph.add_edge("researcher", END)
                                                                                                                                                                                return graph.compile()
                                                                                                                                                                                
