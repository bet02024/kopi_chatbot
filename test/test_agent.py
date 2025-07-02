import pytest
import sys
import os
# Add the parent directory (my_project) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.agent import DebateAgent


def test_agent_for():
    agent_for = DebateAgent("UFOs & Aliens", stance="For the topic")
    print("\n--- Turn 1 (FOR) ---")
    argument = agent_for.generate_argument()
    print(f"Agent FOR: {argument}")
    print(f"Agent Conversation ID: {agent_for.conversation_id}")
    assert isinstance(argument, str)
    assert len(argument) > 0


def test_agent_against():
    agent_for = DebateAgent("UFOs & Aliens", stance="Against the topic")
    print("\n--- Turn 1 (AGAINST) ---")
    argument = agent_for.generate_argument()
    print(f"Agent AGAINST: {argument}")
    print(f"Agent Conversation ID: {agent_for.conversation_id}")
    assert isinstance(argument, str)
    assert len(argument) > 0
