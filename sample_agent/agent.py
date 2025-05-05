"""
Main entry point for the agent using LangGraph and CopilotKit.
"""

import os
from typing import Optional, Literal, TypedDict, Union, List, Dict

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent

from copilotkit import CopilotKitState
from copilotkit.langgraph import copilotkit_exit

from langchain_mcp_adapters.client import MultiServerMCPClient

# -- MCP configuration types --
class StdioConnection(TypedDict):
    command: str
    args: List[str]
    transport: Literal["stdio"]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

MCPConfig = Dict[str, Union[StdioConnection, SSEConnection]]

# -- Agent State including optional MCP config --
class AgentState(CopilotKitState):
    mcp_config: Optional[MCPConfig]

# -- Default MCP Configuration --
# -- Default MCP Configuration (DISTANT) --
DEFAULT_MCP_CONFIG: MCPConfig = {
    "math": {
        "url": "https://mcp-api.onrender.com",  # ← remplace par l’URL réelle de ton API MCP
        "transport": "sse",
    },
}

# -- Node for chat interaction using ReAct Agent --
async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["__end__"]]:
    """
    Node that invokes the ReAct agent using LangChain tools from MCP.
    """
    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)
    print(f"Using MCP config: {mcp_config}")

    async with MultiServerMCPClient(mcp_config) as mcp_client:
        mcp_tools = mcp_client.get_tools()
        model = ChatOpenAI(model="gpt-4o")
        react_agent = create_react_agent(model, mcp_tools)

        agent_input = {
            "messages": state["messages"]
        }

        agent_response = await react_agent.ainvoke(agent_input)
        updated_messages = state["messages"] + agent_response.get("messages", [])

        await copilotkit_exit(config)

        return Command(
            goto=END,
            update={"messages": updated_messages},
        )

# -- Define and compile the graph --
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.set_entry_point("chat_node")
graph = workflow.compile(MemorySaver())

# -- Entry point for testing --
if __name__ == "__main__":
    import asyncio

    initial_state = {
        "messages": [
            {"role": "user", "content": "Quelle est la racine carrée de 25 ?"},
        ]
    }

    result = asyncio.run(graph.ainvoke(initial_state))
    print("Résultat final :", result)
