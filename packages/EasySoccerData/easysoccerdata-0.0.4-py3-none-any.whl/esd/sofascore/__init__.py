"""
Sofascore types module necessary for the client.
"""

from .client import SofascoreClient
from .types import (
    EntityType,
    Event,
    Team,
    Player,
    MatchStats,
    PlayerLineup,
    TeamLineup,
    Lineups,
    TeamColor,
    Category,
    Tournament,
    Season,
    Bracket,
)

__all__ = [
    "SofascoreClient",
    "EntityType",
    "Event",
    "Team",
    "Player",
    "MatchStats",
    "PlayerLineup",
    "TeamLineup",
    "Lineups",
    "TeamColor",
    "Category",
    "Tournament",
    "Season",
    "Bracket",
]
