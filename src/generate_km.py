import re
from lxml import etree
from typing import Literal
from .model import Item, KillMail
from .generate_png import gen_template, gen_png


def gen_km(kb_html: str, mode: Literal['kills', 'losses']) -> None:
    html = etree.HTML(kb_html, etree.HTMLParser())

    victim = html.xpath('//table[contains(@class,"table table-condensed") and @style="width: 100%; margin: '
                        '0px;"]/tr/td[3]/a/text()')[0:3]

    perpetrator: list = html.xpath('//td[@class="pilotinfo"]/div[@class="hidden-sm hidden-md hidden-xs"]/a/text()')
    killer = html.xpath('//a[@class="info_final_blow"]/text()')

    try:
        for i in perpetrator:
            n = perpetrator.index(i)
            if killer[0] == i:
                perpetrator = perpetrator[n: n + 3]
                break
    except IndexError:
        pass

    kb_info = html.xpath(
        '//table[contains(@class,"table table-condensed table-striped table-hover") and @style="width: 100%; padding: '
        '0px; margin: 0px;"]'
    )[0]

    killmail = KillMail()

    killmail.victim_name = victim[0]
    killmail.victim_corp = victim[1]
    killmail.victim_alli = victim[2] if len(victim) > 2 else '无'

    killmail.perpetrator_name = perpetrator[0]
    killmail.perpetrator_corp = perpetrator[1]
    killmail.perpetrator_alli = perpetrator[2] if len(perpetrator) > 2 else '无'

    killmail.drop = re.findall(r'<td class="item_dropped">(.*?)</td>', etree.tostring(kb_info).decode("utf-8"))[0]

    killmail.total = re.findall(
        r'<td><strong class="item_dropped">(.*?)</strong></td>',
        etree.tostring(kb_info).decode("utf-8"),
    )[0]

    ship = re.findall(
        r'<td style="width: 100%"> <a href="/ship/(.*?)/">(.*?)</a>',
        etree.tostring(kb_info).decode("utf-8"),
    )[0]

    killmail.ship = Item.translate(ship[0])

    killmail.time = re.findall(r'<td class="info_kill_dttm">(.*?)</td>', etree.tostring(kb_info).decode("utf-8"))[0]

    killmail.location = re.findall(
        r'<td><a href="/location/.*?/">(.*?)</a> (.*?)</td>',
        etree.tostring(kb_info).decode("utf-8"),
    )[0]

    equipment_ = html.xpath('//table[@class="table table-condensed item_list item-table"]')[0]

    for i in re.split('<th colspan="4"><h5>.*?</h5></th>', etree.tostring(equipment_).decode("utf-8")):
        if s := re.findall(r'<td class="item_(.*?)"><a href="/item/(.*?)/">(.*?)</a>', i):
            killmail.equipment.append(s)

    gen_template(killmail, mode)
    gen_png(mode)
