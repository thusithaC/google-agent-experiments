"""Critic agent that evaluates the work of other agents."""

from agents_core.base_agent import BaseAgent


class CriticAgent(BaseAgent):
    """Critic agent that evaluates the work of other agents."""

    def __init__(self, name: str = "Critic", model_name: str | None = None):
        super().__init__(name, model_name)

    async def get_system_prompt(self) -> str:
        return "You are a critic agent. Your goal is to evaluate the work of other agents and provide constructive feedback."

    async def get_available_tools(self) -> list[dict[str, any]]:
        return []
