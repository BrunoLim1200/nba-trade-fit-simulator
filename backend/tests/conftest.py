import pytest
from typing import List
from src.schemas.analysis import (
    PlayerAdvancedStats,
    PlayerAnalysis,
    PlayerArchetype,
    TeamStats,
    TeamNeeds,
    TeamNeed,
    RosterFrictionResult,
    RosterConflict,
    FitLabel
)


@pytest.fixture
def sniper_stats() -> PlayerAdvancedStats:
    return PlayerAdvancedStats(
        player_id=1,
        player_name="Klay Thompson",
        pts=20.0,
        fg3a=8.0,
        fg3_pct=0.42,
        ast=2.0,
        reb=3.5,
        blk=0.3,
        stl=0.8,
        min=32.0,
        position="SG"
    )


@pytest.fixture
def ball_dominant_stats() -> PlayerAdvancedStats:
    return PlayerAdvancedStats(
        player_id=2,
        player_name="Luka Doncic",
        pts=28.5,
        fg3a=7.0,
        fg3_pct=0.35,
        ast=9.0,
        reb=8.5,
        blk=0.4,
        stl=1.2,
        usg_pct=0.35,
        ast_pct=0.40,
        min=36.0,
        position="PG"
    )


@pytest.fixture
def rim_protector_stats() -> PlayerAdvancedStats:
    return PlayerAdvancedStats(
        player_id=3,
        player_name="Rudy Gobert",
        pts=12.0,
        fg3a=0.1,
        fg3_pct=0.0,
        ast=1.2,
        reb=12.5,
        oreb=3.5,
        blk=2.3,
        stl=0.6,
        min=30.0,
        position="C"
    )


@pytest.fixture
def three_and_d_stats() -> PlayerAdvancedStats:
    return PlayerAdvancedStats(
        player_id=4,
        player_name="Mikal Bridges",
        pts=14.0,
        fg3a=5.0,
        fg3_pct=0.38,
        ast=2.5,
        reb=4.0,
        blk=0.9,
        stl=1.1,
        min=34.0,
        position="SF"
    )


@pytest.fixture
def stretch_big_stats() -> PlayerAdvancedStats:
    return PlayerAdvancedStats(
        player_id=5,
        player_name="Karl-Anthony Towns",
        pts=22.0,
        fg3a=4.5,
        fg3_pct=0.41,
        ast=3.0,
        reb=10.0,
        oreb=2.0,
        blk=1.0,
        stl=0.7,
        min=33.0,
        position="C"
    )


@pytest.fixture
def playmaker_stats() -> PlayerAdvancedStats:
    return PlayerAdvancedStats(
        player_id=6,
        player_name="Chris Paul",
        pts=12.0,
        fg3a=3.0,
        fg3_pct=0.37,
        ast=10.5,
        ast_pct=0.35,
        reb=4.0,
        blk=0.1,
        stl=1.5,
        usg_pct=0.22,
        min=30.0,
        position="PG"
    )


@pytest.fixture
def hustle_player_stats() -> PlayerAdvancedStats:
    return PlayerAdvancedStats(
        player_id=7,
        player_name="Steven Adams",
        pts=8.0,
        fg3a=0.0,
        fg3_pct=0.0,
        ast=2.0,
        reb=11.0,
        oreb=4.5,
        blk=0.8,
        stl=0.6,
        min=28.0,
        position="C"
    )


@pytest.fixture
def team_needs_shooting() -> TeamStats:
    return TeamStats(
        team_id=100,
        team_name="Shooting Needed FC",
        fg3_pct_rank=25,
        reb_rank=10,
        ast_rank=12,
        pace_rank=15,
        def_rating_rank=8,
        off_rating_rank=18,
        fg3_pct=0.32,
        ball_dominant_count=1
    )


@pytest.fixture
def team_needs_defense() -> TeamStats:
    return TeamStats(
        team_id=101,
        team_name="Defense Needed FC",
        fg3_pct_rank=5,
        reb_rank=10,
        ast_rank=12,
        pace_rank=15,
        def_rating_rank=28,
        off_rating_rank=6,
        fg3_pct=0.40,
        ball_dominant_count=0
    )


@pytest.fixture
def team_with_multiple_stars() -> TeamStats:
    return TeamStats(
        team_id=102,
        team_name="Star Heavy FC",
        fg3_pct_rank=8,
        reb_rank=10,
        ast_rank=6,
        pace_rank=15,
        def_rating_rank=12,
        off_rating_rank=4,
        fg3_pct=0.38,
        ball_dominant_count=2
    )


@pytest.fixture
def fast_paced_team() -> TeamStats:
    return TeamStats(
        team_id=103,
        team_name="Run and Gun FC",
        fg3_pct_rank=10,
        reb_rank=20,
        ast_rank=8,
        pace_rank=3,
        def_rating_rank=15,
        off_rating_rank=5,
        fg3_pct=0.36,
        ball_dominant_count=1
    )


@pytest.fixture
def balanced_team() -> TeamStats:
    return TeamStats(
        team_id=104,
        team_name="Balanced FC",
        fg3_pct_rank=12,
        reb_rank=10,
        ast_rank=11,
        pace_rank=15,
        def_rating_rank=10,
        off_rating_rank=9,
        fg3_pct=0.37,
        ball_dominant_count=1
    )