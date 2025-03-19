from typing import Optional

from pydantic import BaseModel, Field

from ..valo_enums import Regions, Maps, Modes


class GetStoredMatchesFilterModel(BaseModel):
    page: Optional[int] = Field(1, ge=1)
    size: Optional[int] = Field(None, ge=1, le=25)


class GetStoredMatchesOptionsModel(BaseModel):
    region: Regions
    name: str
    tag: str
    mode: Optional[Modes] = None
    map: Optional[Maps] = None
    filter: Optional[GetStoredMatchesFilterModel] = None


class GetStoredMatchesByPUUIDResponseModel(BaseModel):
    puuid: str
    region: Regions
    mode: Optional[Modes] = None
    map: Optional[Maps] = None
    filter: Optional[GetStoredMatchesFilterModel] = None
