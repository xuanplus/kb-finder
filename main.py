# coding=UTF-8

from src.get_info import get_character_id, get_km_info, get_character_km_id
from src.generate_km import gen_km
from typing import Literal


def run(character_name: str, mode: Literal['kills', 'losses']) -> None:
    character_id = get_character_id(character_name)
    if character_id:
        print(f'查询到角色，id为{character_id}')
        km_id = get_character_km_id(character_id, mode)
        if km_id:
            gen_km(get_km_info(km_id), mode)
        else:
            print('该角色无击杀记录')


if __name__ == '__main__':
    run('yunnnnn', mode='losses')
