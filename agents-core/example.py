#!/usr/bin/env python3
"""
Example script demonstrating how to use the agents_core package.

This script shows how to import and use the DummyAgent from the agents_core package.
"""

from agents_core import DummyAgent
from agents_core.dummy_module import create_dummy_agent


def main():
    """Main function demonstrating the usage of agents_core."""
    print("=== agents_core Package Demo ===\n")
    
    # Create an agent using the class directly
    agent1 = DummyAgent("Alice", {"role": "assistant", "level": 1})
    print(f"Created agent: {agent1}")
    print(f"Agent state: {agent1.get_state()}\n")
    
    # Process some messages
    response1 = agent1.process_message("Hello, how are you?")
    print(f"Response 1: {response1}")
    
    response2 = agent1.process_message("What can you do?")
    print(f"Response 2: {response2}\n")
    
    # Check memory
    memory = agent1.get_memory()
    print("Agent Memory:")
    for i, entry in enumerate(memory, 1):
        print(f"  {i}. [{entry['type']}] {entry['content']}")
    
    print("\n" + "="*50 + "\n")
    
    # Create an agent using the factory function
    agent2 = create_dummy_agent("Bob", role="helper", level=2)
    print(f"Created agent via factory: {agent2}")
    
    response3 = agent2.process_message("I need help with Python!")
    print(f"Response 3: {response3}")
    
    print(f"\nAgent 2 memory entries: {len(agent2.get_memory())}")
    
    # Clear memory
    agent2.clear_memory()
    print(f"After clearing memory: {len(agent2.get_memory())} entries")


if __name__ == "__main__":
    main()
