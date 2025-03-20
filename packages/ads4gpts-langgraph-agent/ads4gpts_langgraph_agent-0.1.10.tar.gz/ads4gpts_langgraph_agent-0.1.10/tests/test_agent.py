from unittest.mock import MagicMock, patch
from ads4gpts_langgraph_agent.agent import make_ads4gpts_langgraph_agent
from langgraph.graph.state import CompiledStateGraph
import pytest
from dotenv import load_dotenv
import os

load_dotenv()


@patch("ads4gpts_langgraph_agent.agent.get_from_dict_or_env")
@patch("ads4gpts_langgraph_agent.agent.Ads4gptsToolkit")
@patch("ads4gpts_langgraph_agent.agent.create_integration_agent")
@patch("ads4gpts_langgraph_agent.agent.create_advertiser_agent")
def test_make_ads4gpts_langgraph_agent(
    mock_create_advertiser_agent,
    mock_create_integration_agent,
    mock_Ads4gptsToolkit,
    mock_get_from_dict_or_env,
):
    # Setup mock for get_from_dict_or_env to return appropriate values
    mock_get_from_dict_or_env.side_effect = lambda d, key, env_key: {
        "ADS4GPTS_API_KEY": "test_ads4gpts_api_key",
        "ADS4GPTS_BASE_URL": "http://localhost:8000",
        "ADS4GPTS_ADS_ENDPOINT": "test_endpoint",
        "PROVIDER": "openai",
        "OPENAI_API_KEY": "test_openai_api_key",
    }.get(key)

    # Mock Ads4gptsToolkit instance and its get_tools method
    mock_toolkit_instance = MagicMock()
    mock_Ads4gptsToolkit.return_value.get_tools.return_value = mock_toolkit_instance

    # Mock integration and advertiser agents
    mock_integration_agent = MagicMock()
    mock_create_integration_agent.return_value = mock_integration_agent
    mock_advertiser_agent = MagicMock()
    mock_create_advertiser_agent.return_value = mock_advertiser_agent

    # Call the function with test arguments
    agent_name = "test_agent"
    kwargs = {
        "ADS4GPTS_API_KEY": "test_ads4gpts_api_key",
        "PROVIDER": "openai",
        "OPENAI_API_KEY": "test_openai_api_key",
    }
    graph = make_ads4gpts_langgraph_agent(agent_name, **kwargs)

    # Assertions
    mock_Ads4gptsToolkit.assert_called_once_with(
        base_url="http://localhost:8000",
        ads_endpoint="test_endpoint",
        ads4gpts_api_key="test_ads4gpts_api_key",
    )
    mock_create_integration_agent.assert_called_once_with(
        "openai",
        "test_openai_api_key",
        "test_ads4gpts_api_key",
        "http://localhost:8000",
        "test_endpoint",
    )
    mock_create_advertiser_agent.assert_called_once_with(
        "openai", "test_openai_api_key"
    )

    assert graph is not None
    assert isinstance(graph, CompiledStateGraph)


@patch("ads4gpts_langgraph_agent.agent.get_from_dict_or_env")
@patch("ads4gpts_langgraph_agent.agent.Ads4gptsToolkit")
@patch("ads4gpts_langgraph_agent.agent.create_integration_agent")
@patch("ads4gpts_langgraph_agent.agent.create_advertiser_agent")
def test_make_ads4gpts_langgraph_agent_missing_api_key(
    mock_create_advertiser_agent,
    mock_create_integration_agent,
    mock_Ads4gptsToolkit,
    mock_get_from_dict_or_env,
):
    # Setup mock for get_from_dict_or_env to raise KeyError for ADS4GPTS_API_KEY
    def side_effect(d, key, env_key):
        if key == "ADS4GPTS_API_KEY":
            raise KeyError(f"Missing {key}")
        return {
            "PROVIDER": "openai",
            "OPENAI_API_KEY": "test_openai_api_key",
        }.get(key)

    mock_get_from_dict_or_env.side_effect = side_effect

    # Mock Ads4gptsToolkit instance and its get_tools method
    mock_toolkit_instance = MagicMock()
    mock_Ads4gptsToolkit.return_value.get_tools.return_value = mock_toolkit_instance

    # Mock integration and advertiser agents
    mock_integration_agent = MagicMock()
    mock_create_integration_agent.return_value = mock_integration_agent
    mock_advertiser_agent = MagicMock()
    mock_create_advertiser_agent.return_value = mock_advertiser_agent

    # Call the function with missing API key
    agent_name = "test_agent"
    kwargs = {
        "PROVIDER": "openai",
        "OPENAI_API_KEY": "test_openai_api_key",
    }

    with pytest.raises(KeyError):
        make_ads4gpts_langgraph_agent(agent_name, **kwargs)


@patch("ads4gpts_langgraph_agent.agent.get_from_dict_or_env")
@patch("ads4gpts_langgraph_agent.agent.Ads4gptsToolkit")
@patch("ads4gpts_langgraph_agent.agent.create_integration_agent")
@patch("ads4gpts_langgraph_agent.agent.create_advertiser_agent")
def test_make_ads4gpts_langgraph_agent_invalid_provider(
    mock_create_advertiser_agent,
    mock_create_integration_agent,
    mock_Ads4gptsToolkit,
    mock_get_from_dict_or_env,
):
    # Setup mock for get_from_dict_or_env
    def side_effect(d, key, env_key):
        if key == "INVALID_PROVIDER_API_KEY":
            raise KeyError(f"Missing API key for {key}")
        return {
            "ADS4GPTS_API_KEY": "test_ads4gpts_api_key",
            "PROVIDER": "invalid_provider",
            "ADS4GPTS_BASE_URL": "http://localhost:8000",
            "ADS4GPTS_ADS_ENDPOINT": "test_endpoint",
        }.get(key)

    mock_get_from_dict_or_env.side_effect = side_effect

    # Mock Ads4gptsToolkit instance and its get_tools method
    mock_toolkit_instance = MagicMock()
    mock_Ads4gptsToolkit.return_value.get_tools.return_value = mock_toolkit_instance

    # Mock integration and advertiser agents
    mock_integration_agent = MagicMock()
    mock_create_integration_agent.return_value = mock_integration_agent
    mock_advertiser_agent = MagicMock()
    mock_create_advertiser_agent.return_value = mock_advertiser_agent

    # Call the function with an invalid provider
    agent_name = "test_agent"
    kwargs = {
        "ADS4GPTS_API_KEY": "test_ads4gpts_api_key",
        "PROVIDER": "invalid_provider",
        "INVALID_PROVIDER_API_KEY": "test_invalid_provider_api_key",
    }

    with pytest.raises(KeyError):
        make_ads4gpts_langgraph_agent(agent_name, **kwargs)


# from unittest.mock import MagicMock, patch
# from ads4gpts_langgraph_agent.agent import make_ads4gpts_langgraph_agent
# from langgraph.graph import StateGraph
# import pytest
# from dotenv import load_dotenv
# import os

# load_dotenv()


# @patch("ads4gpts_langgraph_agent.agent.Ads4gptsToolkit")
# @patch("ads4gpts_langgraph_agent.agent.create_integration_agent")
# @patch("ads4gpts_langgraph_agent.agent.create_advertiser_agent")
# def test_make_ads4gpts_langgraph_agent(
#     mock_create_advertiser_agent,
#     mock_create_integration_agent,
#     mock_Ads4gptsToolkit,
# ):
#     # Mock Ads4gptsToolkit instance and its get_tools method
#     mock_toolkit_instance = MagicMock()
#     mock_Ads4gptsToolkit.return_value.get_tools.return_value = mock_toolkit_instance

#     # Mock integration and advertiser agents
#     mock_integration_agent = MagicMock()
#     mock_create_integration_agent.return_value = mock_integration_agent
#     mock_advertiser_agent = MagicMock()
#     mock_create_advertiser_agent.return_value = mock_advertiser_agent

#     # Call the function with test arguments
#     agent_name = "test_agent"
#     kwargs = {
#         "ADS4GPTS_API_KEY": "test_ads4gpts_api_key",
#         "PROVIDER": "openai",
#         "OPENAI_API_KEY": "test_openai_api_key",
#     }
#     graph = make_ads4gpts_langgraph_agent(agent_name, **kwargs)

#     # Assertions
#     mock_Ads4gptsToolkit.assert_called_once_with(
#         ads4gpts_api_key="test_ads4gpts_api_key"
#     )
#     mock_create_integration_agent.assert_called_once_with(
#         "openai", "test_openai_api_key", "test_ads4gpts_api_key"
#     )
#     mock_create_advertiser_agent.assert_called_once_with(
#         "openai", "test_openai_api_key", "test_ads4gpts_api_key"
#     )

#     assert graph is not None
#     assert isinstance(graph, StateGraph)


# @patch("ads4gpts_langgraph_agent.agent.Ads4gptsToolkit")
# @patch("ads4gpts_langgraph_agent.agent.create_integration_agent")
# @patch("ads4gpts_langgraph_agent.agent.create_advertiser_agent")
# def test_make_ads4gpts_langgraph_agent_missing_api_key(
#     mock_create_advertiser_agent,
#     mock_create_integration_agent,
#     mock_Ads4gptsToolkit,
# ):
#     # Mock Ads4gptsToolkit instance and its get_tools method
#     mock_toolkit_instance = MagicMock()
#     mock_Ads4gptsToolkit.return_value.get_tools.return_value = mock_toolkit_instance

#     # Mock integration and advertiser agents
#     mock_integration_agent = MagicMock()
#     mock_create_integration_agent.return_value = mock_integration_agent
#     mock_advertiser_agent = MagicMock()
#     mock_create_advertiser_agent.return_value = mock_advertiser_agent

#     # Call the function with missing API key
#     agent_name = "test_agent"
#     kwargs = {
#         "PROVIDER": "openai",
#         "OPENAI_API_KEY": "test_openai_api_key",
#     }

#     with pytest.raises(KeyError):
#         make_ads4gpts_langgraph_agent(agent_name, **kwargs)


# @patch("ads4gpts_langgraph_agent.agent.Ads4gptsToolkit")
# @patch("ads4gpts_langgraph_agent.agent.create_integration_agent")
# @patch("ads4gpts_langgraph_agent.agent.create_advertiser_agent")
# def test_make_ads4gpts_langgraph_agent_invalid_provider(
#     mock_create_advertiser_agent,
#     mock_create_integration_agent,
#     mock_Ads4gptsToolkit,
# ):
#     # Mock Ads4gptsToolkit instance and its get_tools method
#     mock_toolkit_instance = MagicMock()
#     mock_Ads4gptsToolkit.return_value.get_tools.return_value = mock_toolkit_instance

#     # Mock integration and advertiser agents
#     mock_integration_agent = MagicMock()
#     mock_create_integration_agent.return_value = mock_integration_agent
#     mock_advertiser_agent = MagicMock()
#     mock_create_advertiser_agent.return_value = mock_advertiser_agent

#     # Call the function with an invalid provider
#     agent_name = "test_agent"
#     kwargs = {
#         "ADS4GPTS_API_KEY": "test_ads4gpts_api_key",
#         "PROVIDER": "invalid_provider",
#         "INVALID_PROVIDER_API_KEY": "test_invalid_provider_api_key",
#     }

#     with pytest.raises(KeyError):
#         make_ads4gpts_langgraph_agent(agent_name, **kwargs)
#     mock_get_from_dict_or_env.assert_any_call(
#         kwargs, "OPENAI_API_KEY", "OPENAI_API_KEY"
#     )
#     mock_Ads4gptsToolkit.assert_called_once_with(
#         ads4gpts_api_key="test_ads4gpts_api_key"
#     )
#     mock_create_integration_agent.assert_called_once_with(
#         "openai", "test_openai_api_key", "test_ads4gpts_api_key"
#     )
#     mock_create_advertiser_agent.assert_called_once_with(
#         "openai", "test_openai_api_key", "test_ads4gpts_api_key"
#     )

#     assert graph is not None
#     assert isinstance(graph, StateGraph)
