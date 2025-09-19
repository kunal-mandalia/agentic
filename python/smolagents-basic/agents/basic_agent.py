from smolagents import CodeAgent
from smolagents.models import LiteLLMModel
from dotenv import load_dotenv
from tools import all_tools

load_dotenv()

def create_basic_agent(model_id: str = "gpt-5-nano") -> CodeAgent:
    """
    Create a basic smolagents agent with all available tools.
    Includes math, entertainment, and Gmail tools (if dependencies installed).

    Args:
        model_id: The model to use for the agent

    Returns:
        Configured CodeAgent instance
    """
    model = LiteLLMModel(model_id=model_id)
    agent = CodeAgent(tools=all_tools, model=model)
    return agent

def create_minimal_agent(model_id: str = "gpt-5-nano") -> CodeAgent:
    """
    Create a minimal smolagents agent with only basic tools.
    Excludes Gmail tools for faster loading.

    Args:
        model_id: The model to use for the agent

    Returns:
        Configured CodeAgent instance with minimal tools
    """
    from tools import calculator, tell_joke

    model = LiteLLMModel(model_id=model_id)
    agent = CodeAgent(tools=[calculator, tell_joke], model=model)
    return agent