from typing import List

from pydantic import BaseModel

from .graph import PatternGraphBase


class TeamNode(BaseModel):
    """multi-agent node, as team node"""

    name: str

    role: str

    description: str

    node: PatternGraphBase


class FlatTeam:
    """flat team"""

    teams: List[TeamNode]


class NTreeTeam:
    """n-ary tree struct team"""
    parent: TeamNode

    sub_nodes: List[TeamNode]
