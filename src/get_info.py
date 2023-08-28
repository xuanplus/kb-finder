import re
import requests
from typing import Literal


def get_character_id(character_name: str) -> str | None:
    response = requests.post(
        url="https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        data=f'["{character_name}"]',
        headers={"Content-Type": "application/json"},
    )
    result = re.findall(r'"id":(\d+),"name"', response.text)
    if result:
        return result[0]
    else:
        return None


def get_character_km_id(character_id: str, mode: Literal['kills', 'losses']) -> str | None:
    url = f"https://zkillboard.com/api/{mode}/characterID/{character_id}/"
    if mode == "kills":
        url += "finalblow-only/"
    response = requests.get(
        url=url,
        headers={
            "User-Agent": "xuanplus@outlook.com",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip",
        },
    )
    result = response.json()
    if result:
        for i in result:
            if i["zkb"]["totalValue"] == 10000 or i["zkb"]["npc"]:
                continue
            return i["killmail_id"]
        else:
            return None
    else:
        return None


def get_km_info(km_id: str) -> str:
    response = requests.get(
        url=f"https://zkillboard.com/kill/{km_id}/",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.7",
            "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"'
        },
    )
    return response.text
