"""Tests for the Actor and Critic agents."""

import pytest

from agents_core.actor_agent import ActorAgent
from agents_core.critic_agent import CriticAgent


@pytest.fixture
def actor_agent():
    """Fixture for ActorAgent."""
    return ActorAgent()


@pytest.fixture
def critic_agent():
    """Fixture for CriticAgent."""
    return CriticAgent()


def test_actor_agent_creation(actor_agent):
    """Test that the ActorAgent can be created."""
    assert actor_agent.name == "Actor"
    assert actor_agent.model_name is not None


def test_critic_agent_creation(critic_agent):
    """Test that the CriticAgent can be created."""
    assert critic_agent.name == "Critic"
    assert critic_agent.model_name is not None


@pytest.mark.asyncio
async def test_actor_agent_system_prompt(actor_agent):
    """Test the ActorAgent's system prompt."""
    prompt = await actor_agent.get_system_prompt()
    assert "You are an actor agent." in prompt


@pytest.mark.asyncio
async def test_critic_agent_system_prompt(critic_agent):
    """Test the CriticAgent's system prompt."""
    prompt = await critic_agent.get_system_prompt()
    assert "You are a critic agent." in prompt


@pytest.mark.asyncio
async def test_actor_agent_available_tools(actor_agent):
    """Test the ActorAgent's available tools."""
    tools = await actor_agent.get_available_tools()
    assert isinstance(tools, list)


@pytest.mark.asyncio
async def test_critic_agent_available_tools(critic_agent):
    """Test the CriticAgent's available tools."""
    tools = await critic_agent.get_available_tools()
    assert isinstance(tools, list)
