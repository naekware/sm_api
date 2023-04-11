from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class SteamMarketItemDB(BaseModel):
    username: str
    game_id: int
    name: str
    price: float
