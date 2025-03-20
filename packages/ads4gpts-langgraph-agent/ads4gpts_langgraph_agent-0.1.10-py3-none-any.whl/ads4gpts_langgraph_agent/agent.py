from typing_extensions import Literal, Annotated
from typing import Dict, Optional
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.types import Command
from langgraph.prebuilt import ToolNode
from langchain_core.runnables.config import RunnableConfig

from ads4gpts_langchain.utils import get_from_dict_or_env
from ads4gpts_langchain import Ads4gptsToolkit

from ads4gpts_langgraph_agent.state import ADS4GPTsState, ADS4GPTsConfig
from ads4gpts_langgraph_agent.tools import make_handoff_tool
from ads4gpts_langgraph_agent.llms import (
    create_integration_agent,
    create_advertiser_agent,
)


def make_ads4gpts_langgraph_agent(
    agent_name: Optional[str],
    **kwargs,
):
    ads4gpts_api_key = get_from_dict_or_env(
        kwargs, "ADS4GPTS_API_KEY", "ADS4GPTS_API_KEY"
    )
    ads4gpts_base_url = get_from_dict_or_env(
        kwargs, "ADS4GPTS_BASE_URL", "ADS4GPTS_BASE_URL"
    )
    ads4gpts_ads_endpoint = get_from_dict_or_env(
        kwargs, "ADS4GPTS_ADS_ENDPOINT", "ADS4GPTS_ADS_ENDPOINT"
    )
    ads4gpts_toolkit = Ads4gptsToolkit(
        base_url=ads4gpts_base_url,
        ads_endpoint=ads4gpts_ads_endpoint,
        ads4gpts_api_key=ads4gpts_api_key,
    ).get_tools()
    provider = get_from_dict_or_env(kwargs, "PROVIDER", "PROVIDER")
    api_key = get_from_dict_or_env(
        kwargs,
        f"{provider.upper()}_API_KEY",
        f"{provider
        .upper()}_API_KEY",
    )
    integration_agent = create_integration_agent(
        provider, api_key, ads4gpts_api_key, ads4gpts_base_url, ads4gpts_ads_endpoint
    )
    advertiser_agent = create_advertiser_agent(provider, api_key)

    async def integration_agent_node(state: ADS4GPTsState, config: RunnableConfig):
        session_id = config["configurable"].get("session_id", "")
        integration_agent_response = await integration_agent.ainvoke(
            {
                "messages": state["messages"],
                "ad_prompt": "Get one Inline Ad based on the context provided.",
                "session_id": session_id,
            }
        )
        return {"messages": [integration_agent_response]}

    async def advertiser_agent_node(state: ADS4GPTsState, config: RunnableConfig):
        advertiser_agent_response = await advertiser_agent.ainvoke(
            {"ads": state["messages"][-1].content, "messages": state["messages"][:-2]}
        )
        return {"messages": [advertiser_agent_response]}

    rtb_node = ToolNode(ads4gpts_toolkit)

    graph = StateGraph(ADS4GPTsState, ADS4GPTsConfig)
    graph.add_node("integration_agent_node", integration_agent_node)
    graph.add_node("rtb_node", rtb_node)
    graph.add_node("advertiser_agent_node", advertiser_agent_node)
    graph.add_edge(START, "integration_agent_node")
    graph.add_edge("integration_agent_node", "rtb_node")
    graph.add_edge("rtb_node", "advertiser_agent_node")
    graph.add_edge("advertiser_agent_node", END)

    return graph.compile()
