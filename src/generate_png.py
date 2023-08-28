# coding=UTF-8

import os
import imgkit
from typing import Literal
from .model import Item, KillMail


def get_template() -> str:
    with open('./template.html', mode='r', encoding='utf-8') as file:
        return file.read()


def gen_template(killmail: KillMail, mode: Literal['kills', 'losses']):
    equipments = ""
    for i in killmail.equipment:
        for j in i:
            name = Item.get_or_none(Item.typeID == j[1]).物品名称
            if j[0] == "dropped":
                equipments += f'<li class="Drops">{name if name else j[2] + "（暂无翻译）"}</li>\n'
            else:
                equipments += f'<li>{name if name else j[2] + "（暂无翻译）"}</li>\n'
        equipments += "<br/>\n"
    template = get_template()
    with open(f'./{mode}.html', mode='w', encoding='utf-8') as file:
        file.write(
            template.replace("victim_name", killmail.victim_name)
            .replace("victim_corp", killmail.victim_corp)
            .replace("victim_alli", killmail.victim_alli)
            .replace("perpetrator_name", killmail.perpetrator_name)
            .replace("perpetrator_corp", killmail.perpetrator_corp)
            .replace("perpetrator_alli", killmail.perpetrator_alli)
            .replace("total_value", killmail.total)
            .replace("drop", killmail.drop)
            .replace("ship", killmail.ship)
            .replace("time", killmail.time)
            .replace("location", killmail.location[0] + killmail.location[1])
            .replace("equipments", equipments))


def gen_png(mode: Literal['kills', 'losses']):
    imgkit.from_file(
        f"./{mode}.html",
        output_path=f"./{mode}.png",
        options={
            "width": 350,
            "enable-local-file-access": "",
            "quality": 100
        })
    os.remove(f"./{mode}.html")
