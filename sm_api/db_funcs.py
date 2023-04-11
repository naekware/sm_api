import sqlite3
import sm_api.config as config
import os


def init_db() -> None:
    """Initializes the database with all the required tables."""
    if os.path.exists(config.DB_PATH):
        return None
    con = sqlite3.connect(config.DB_PATH)
    cur = con.cursor()
    query = [
        "CREATE TABLE user(username PRIMARY KEY, password)",
        "CREATE TABLE item(item_id INTEGER PRIMARY KEY, username, game_id, name, price, FOREIGN KEY(username) REFERENCES user(username))",  # noqa: E501
    ]
    for q in query:
        cur.execute(q)
    con.commit()


def user_exists(username: str) -> bool:
    """Checks if a user exists.

    Args:
        username (str): The username of the user to be checked.

    Returns:
        bool: True if the user exists, False if not.
    """
    con = sqlite3.connect(config.DB_PATH)
    cur = con.cursor()
    query = "SELECT username FROM user WHERE username = ?"
    cur.execute(query, (username,))
    return any(cur.fetchall())


def create_user(username: str, password: str) -> bool:
    """Creates a new user in the database.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the user was created, False if the user already exists.
    """
    if user_exists(username):
        return False
    con = sqlite3.connect(config.DB_PATH)
    cur = con.cursor()
    query = "INSERT INTO user(username, password) VALUES(?, ?)"
    cur.execute(query, (username, password))
    con.commit()
    return True


def add_item(username: str, game_id: int, name: str, price: float) -> None:
    """Add an item to be tracked to a users account

    Args:
        username (str): The username of the user.
        game_id (int): The game id associated with the item. i.e. CS:GO is 730
        name (str): The name of the item.
        price (float): The price of the item.
    """
    con = sqlite3.connect(config.DB_PATH)
    cur = con.cursor()
    query = "INSERT INTO item(username, game_id, name, price) VALUES(?, ?, ?, ?)"
    cur.execute(query, (username, game_id, name, price))
    con.commit()


def remove_item(item_id: int):
    """Removes an item from a user's tracked items.

    Args:
        item_id (int): The id of the item.
    """
    con = sqlite3.connect(config.DB_PATH)
    cur = con.cursor()
    query = "DELETE FROM item WHERE item_id = ?"
    cur.execute(query, (item_id,))
    con.commit()


def get_user_items(username: str):
    con = sqlite3.connect(config.DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    query = (
        "SELECT item_id, username, game_id, name, price FROM item WHERE username = ?"
    )
    cur.execute(query, (username,))
    return [dict(row) for row in cur.fetchall()]
