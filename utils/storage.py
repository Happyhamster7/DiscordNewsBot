import json
import os
import tempfile
from config import STORE_PATH

_EMPTY_STORE = {"guilds": {}, "users": {}, "seen_articles": {}}


def load_store() -> dict:
    if not os.path.exists(STORE_PATH):
        return {k: {} for k in _EMPTY_STORE}
    with open(STORE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for key in _EMPTY_STORE:
        data.setdefault(key, {})
    return data


def save_store(data: dict) -> None:
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    dir_name = os.path.dirname(STORE_PATH)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False,
                                     suffix=".tmp", encoding="utf-8") as tf:
        json.dump(data, tf, indent=2)
        tmp_path = tf.name
    os.replace(tmp_path, STORE_PATH)
