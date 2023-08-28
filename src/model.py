# coding=UTF-8

from peewee import SqliteDatabase
from peewee import IntegerField, TextField, Model

db = SqliteDatabase('./evedata.db')


class Item(Model):
    typeID = IntegerField(primary_key=True)
    物品名称 = TextField()

    class Meta:
        database = db
        db_table = "evedata"

    @staticmethod
    def translate(typeID: str) -> str | None:
        return Item.get_or_none(Item.typeID == typeID).物品名称


class KillMail:
    victim_name: str = ""
    victim_corp: str = ""
    victim_alli: str = ""

    perpetrator_name: str = ""
    perpetrator_corp: str = ""
    perpetrator_alli: str = ""

    drop: str = ""
    total: str = ""

    ship: str = ""
    equipment: list = []

    location: list = []
    time: str = ""
