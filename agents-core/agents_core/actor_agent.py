"""Actor agent that interacts with tools to accomplish a task."""

from agents_core.base_agent import BaseAgent


class ActorAgent(BaseAgent):
    """Actor agent that interacts with tools to accomplish a task."""

    def __init__(self, name: str = "Actor", model_name: str | None = None):
        super().__init__(name, model_name)

    async def get_system_prompt(self) -> str:
        return "You are an actor agent. Your goal is to accomplish the given task by using the available tools."

    async def get_available_tools(self) -> list[dict[str, any]]:
        return []
