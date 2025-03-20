"""
econagents: A Python library for setting up and running economic experiments with LLMs or human subjects.
"""

from econagents.core.agent_role import AgentRole
from econagents.core.game_runner import GameRunner, HybridGameRunnerConfig, TurnBasedGameRunnerConfig
from econagents.core.manager import AgentManager
from econagents.core.manager.phase import PhaseManager, HybridPhaseManager, TurnBasedPhaseManager
from econagents.core.state.fields import EventField
from econagents.core.state.game import GameState, MetaInformation, PrivateInformation, PublicInformation
from econagents.llm.openai import ChatOpenAI

# Don't manually change, let poetry-dynamic-versioning handle it.
__version__ = "0.0.1"

__all__: list[str] = [
    "AgentRole",
    "AgentManager",
    "ChatOpenAI",
    "PhaseManager",
    "TurnBasedPhaseManager",
    "HybridPhaseManager",
    "GameState",
    "MetaInformation",
    "PrivateInformation",
    "PublicInformation",
    "GameRunner",
    "TurnBasedGameRunnerConfig",
    "HybridGameRunnerConfig",
    "EventField",
]
