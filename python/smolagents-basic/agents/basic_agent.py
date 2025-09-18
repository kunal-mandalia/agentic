from smolagents import CodeAgent
from smolagents.models import LiteLLMModel
from dotenv import load_dotenv
from tools import calculator, tell_joke

load_dotenv()

def create_basic_agent(model_id: str = "gpt-5-nano") -> CodeAgent:
    """
    Create a basic smolagents agent with math and entertainment tools.

    Args:
        model_id: The model to use for the agent

    Returns:
        Configured CodeAgent instance
    """
    model = LiteLLMModel(model_id=model_id)
    agent = CodeAgent(tools=[calculator, tell_joke], model=model)
    return agent