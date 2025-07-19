"""Base agent class using Google's agent protocol."""

import json
from abc import ABC, abstractmethod
from typing import Any

import google.generativeai as genai
import structlog

from agents_core.config import config

logger = structlog.get_logger(__name__)


class BaseAgent(ABC):
    """Base class for all agents using Google's agent protocol."""

    def __init__(self, name: str, model_name: str | None = None):
        """Initialize the base agent.

        Args:
            name: Name of the agent
            model_name: Gemini model to use (defaults to config)
        """
        self.name = name
        self.model_name = model_name or config.gemini.gemini_model

        # Configure Gemini
        if config.gemini.gemini_api_key:
            genai.configure(api_key=config.gemini.gemini_api_key)

        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=genai.types.GenerationConfig(
                temperature=config.gemini.gemini_temperature,
                max_output_tokens=config.gemini.gemini_max_tokens,
            ),
        )

        self.conversation_history: list[dict[str, str]] = []

    @abstractmethod
    async def get_system_prompt(self) -> str:
        """Get the system prompt for this agent.

        Returns:
            System prompt string
        """
        pass

    @abstractmethod
    async def get_available_tools(self) -> list[dict[str, Any]]:
        """Get list of tools available to this agent.

        Returns:
            List of tool definitions
        """
        pass

    async def process_message(self, message: str, context: dict[str, Any] | None = None) -> str:
        """Process a user message and return a response.

        Args:
            message: User message
            context: Optional context information

        Returns:
            Agent response
        """
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": message})

            # Get system prompt
            system_prompt = await self.get_system_prompt()

            # Prepare the conversation for Gemini
            conversation_text = self._format_conversation_for_gemini(system_prompt)

            # Generate response
            response = await self._generate_response(conversation_text, context)

            # Add agent response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})

            logger.info("Message processed", agent=self.name, message_length=len(message))
            return response

        except Exception as e:
            logger.error("Failed to process message", agent=self.name, error=str(e))
            raise

    def _format_conversation_for_gemini(self, system_prompt: str) -> str:
        """Format conversation history for Gemini.

        Args:
            system_prompt: System prompt to include

        Returns:
            Formatted conversation string
        """
        formatted = f"System: {system_prompt}\n\n"

        for message in self.conversation_history:
            role = "Human" if message["role"] == "user" else "Assistant"
            formatted += f"{role}: {message['content']}\n\n"

        return formatted

    async def _generate_response(
        self, conversation_text: str, context: dict[str, Any] | None = None
    ) -> str:
        """Generate response using Gemini.

        Args:
            conversation_text: Formatted conversation
            context: Optional context information

        Returns:
            Generated response
        """
        try:
            # Add context if provided
            if context:
                conversation_text += f"\nContext: {json.dumps(context, indent=2)}\n\n"

            # Generate response

            response = await self.model.generate_content_async(conversation_text)

            return response.text

        except Exception as e:
            logger.error("Failed to generate response", error=str(e))
            raise

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        logger.info("Conversation history cleared", agent=self.name)

    def get_conversation_summary(self) -> dict[str, Any]:
        """Get a summary of the current conversation.

        Returns:
            Conversation summary
        """
        return {
            "agent_name": self.name,
            "model": self.model_name,
            "message_count": len(self.conversation_history),
            "conversation_length": sum(len(msg["content"]) for msg in self.conversation_history),
        }
