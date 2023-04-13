from datetime import datetime
from dataclasses import dataclass
import urllib.request
import urllib.parse
import re


@dataclass
class SteamMarketPrice:
    price: float
    date: datetime


class SteamMarketItem:
    game_id: int
    name: str
    steam_market_url: str
    prices: list[SteamMarketPrice]

    def __init__(self, game_id: int, name: str) -> None:
        """Constructor for SteamMarketItem.

        Args:
            game_id (int): The game id, it can be found in the steam market URL.
            name (str): The name of the item, it can also be found in the steam market URL.
        """  # noqa: E501
        self.game_id = game_id
        self.name = name
        self.steam_market_url = f"https://steamcommunity.com/market/listings/{game_id}/{urllib.parse.quote(name)}"
        self.prices = self._load_market_prices()

    def _load_market_prices(self) -> list[SteamMarketPrice]:
        prices = []
        page_content = (
            urllib.request.urlopen(self.steam_market_url).read().decode("utf-8")
        )
        matches = re.findall(r'\["([A-Za-z\s\d:+]+)".([\d\.]+),"(\d+)"\]', page_content)

        for match in matches:
            price = match[1]
            date = datetime.strptime(" ".join(match[0].split(" ")[:-1]), "%b %d %Y %H:")
            prices.append(SteamMarketPrice(price, date))

        return prices
