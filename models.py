from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ENUM-----------------------------------------------------------------------------------
class SeasonType(str, Enum):
    REGULAR = "regular"
    ALL_STARS = "all_stars"
    VS_THE_WORLD = "vs_the_world"
    GLOBAL = "global"
    ROYAL = "royal"
    OTHER = "other"


class LipSyncType(str, Enum):
    LIPSYNC_FOR_YOUR_LIFE = "lipsync_for_your_life"
    LIPSYNC_FOR_THE_WIN = "lipsync_for_the_win"


class LipSyncOutcome(str, Enum):
    WIN = "win"
    LOSS = "loss"


class ArtistType(str, Enum):
    PRIMARY = "primary"
    FEATURING = "featuring"


class CastRole(str, Enum):
    CONTESTANT = "contestant"
    ASSASSIN = "assassin"


# Songs and Artists -----------------------------------------------------------------------------------
class SongArtistModel(
    BaseModel
):  # An artist can be the primary artist or a featured artist of a song
    name: str
    artist_type: ArtistType = ArtistType.PRIMARY


class SongModel(BaseModel):  # A song may have multiple artists
    title: str
    artists: list[SongArtistModel]


# Contestants -----------------------------------------------------------------------------------
class ContestantModel(BaseModel):
    # A contestant may go by a different name when they show up in a different season
    drag_name: str
    aliases: list[str] = Field(default_factory=list)


# Lipsyncs  -----------------------------------------------------------------------------------
class LipSyncParticipantModel(BaseModel):
    contestant_name: str
    outcome: LipSyncOutcome
    role: CastRole = CastRole.CONTESTANT


class LipSyncModel(BaseModel):
    lipsync_type: LipSyncType
    song: Optional[SongModel] = None
    participants: list[LipSyncParticipantModel]


# Episodes -----------------------------------------------------------------------------------
class EpisodeModel(BaseModel):
    episode_number: int
    title: Optional[str] = None
    air_date: Optional[str] = None
    lip_syncs: list[LipSyncModel] = Field(default_factory=list)


# Seasons -----------------------------------------------------------------------------------
class SeasonModel(BaseModel):
    franchise_short_code: str
    season_type: SeasonType
    season_number: int
    title: Optional[str] = None
    episode_count: Optional[int] = None
    premiere_date: Optional[str] = None
    contestants: list[ContestantModel]
    episodes: list[EpisodeModel]
