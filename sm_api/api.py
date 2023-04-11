from fastapi import FastAPI
from sm_api.SteamMarketItem import SteamMarketItem
import sm_api.api_models.models as models
import sm_api.db_funcs as db_funcs
from pydantic import BaseModel


class ItemProfit(BaseModel):
    item_id: int
    game_id: int
    name: str
    paid_price: float
    curr_price: float


def get_item_current_prices(username: str):
    profits = []
    user_items = db_funcs.get_user_items(username)

    for item in user_items:
        smi = SteamMarketItem(item.get("game_id"), item.get("name"))
        profits.append(
            ItemProfit(
                item_id=item.get("item_id"),
                game_id=item.get("game_id"),
                name=item.get("name"),
                curr_price=smi.prices[-1].price,
                paid_price=item.get("price"),
            )
        )
    return profits


db_funcs.init_db()
app = FastAPI()


@app.put("/user")
async def put_create_user(user: models.User):
    ret = db_funcs.create_user(user.username, user.password)
    return {"success": ret}


@app.put("/item")
async def put_add_item(item: models.SteamMarketItemDB):
    db_funcs.add_item(item.username, item.game_id, item.name, item.price)
    return {"success": True}


@app.delete("/item")
async def delete_remove_item(item_id: int):
    db_funcs.remove_item(item_id)
    return {"success": True}


@app.get("/item")
async def get_item_user(username: str):
    return {"items": db_funcs.get_user_items(username)}


@app.get("/prices")
async def get_item_prices(username: str):
    return {"profits": get_item_current_prices(username)}
