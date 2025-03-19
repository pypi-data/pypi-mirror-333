from pydantic import BaseModel

class DayMMRStats(BaseModel):
    mmr: int
    mmr_difference: int
    wins: int
    losses: int
    wins_percentage: float