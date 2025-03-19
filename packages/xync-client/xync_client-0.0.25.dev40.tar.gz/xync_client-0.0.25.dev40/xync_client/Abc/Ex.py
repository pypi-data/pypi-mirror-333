import logging
import re
from abc import abstractmethod

import msgspec
from msgspec import Struct
from tortoise.exceptions import MultipleObjectsReturned, IntegrityError
from x_model.models import PydIn
from xync_schema import types
from xync_schema import models

from xync_client.Abc.Base import BaseClient, MapOfIdsList


class PmUni(PydIn):
    _unq: list[str] = ["norm", "country"]

    norm: str
    acronym: str = None
    country: str = None
    alias: str = None
    extra: str = None
    bank: bool = None


class PmUnifier:
    pms: dict[str, PmUni] = {}  # {origin: normalized}

    pm_map: dict[str, str] = {
        "Юmoney": "YooMoney",
        # "Local Bank (R-Green)": "Sberbank",
        # "Local Bank (S-Green)": "Sberbank",
        # "Local Card (Red)": "Alfa-Bank",
        # "Local Card (Yellow)": "Tinkoff",
        # "Local Card M-redTS": "MTS-bank",
        # "Local Card-Green": "Sberbank",
        # "Local Card-Yellow": "Tinkoff",
        # "GTB Bank (Guarantee Trust Bank)": "GTBank",
    }
    re_bank = [
        r"^bank (?!of )| bank$",
        r" banka$",
        r" bankas$",
        r" bankası$",
        r" banca$",
        r"^banco(?! de | del )| banco$",
    ]
    re_extra = [
        r"\(card\)$|\bpay$|\bmoney$|\bwallet$|\bcash$",
        r"b\.s\.c\.|k\.s\.c|s\.a$| sv$| gt$",
    ]
    re_glut = [
        r"\.io$|\.com$",
        r"l'|d’|d'",
    ]
    i18n_map = {
        # "  ": " ",
        "nationale": "national",
        "а": "a",
        "á": "a",
        "â": "a",
        "о": "o",
        "ó": "o",
        "ō": "o",
        "ú": "u",
        "ü": "u",
        "ų": "u",
        "с": "c",
        "č": "c",
        "ç": "c",
        "é": "e",
        "è": "e",
        "ş": "s",
        "š": "s",
        "ř": "r",
        "í": "i",
    }
    rms = " -:`'’′"

    def __init__(self, countries: list[str]):
        self.cts = countries

    def countries(self, name: str):
        cmap = {
            "kazakstan": "kazakhstan",
        }
        for ct in self.cts:
            # Если имя кончается на "Название_страны" в скобках
            if (
                ct
                and self.pms[name].norm.endswith((ct + ")", cmap.get(ct, ct)))
                and not self.pms[name].norm.endswith((" of " + ct, " of the " + ct, " and " + ct, " de " + ct))
            ):
                self.pms[name].norm = self.pms[name].norm.replace(ct, "")
                self.pms[name].country = ct
                self.clear(name)
                return

    def extra(self, name: str):
        for r in self.re_extra:
            if match := re.search(r, self.pms[name].norm):
                self.pms[name].norm = self.pms[name].norm.replace(match.group(), "")
                self.pms[name].extra = match.group()
                self.clear(name)
                return

    def alias(self, name: str):
        if match := re.search(r"\(.+\)$", self.pms[name].norm):
            self.pms[name].norm = self.pms[name].norm.replace(match.group(), "")
            self.pms[name].alias = match.group()[1:-1]
            self.clear(name)
            return

    def bank(self, name: str):
        for r in self.re_bank:
            if match := re.search(r, self.pms[name].norm):
                self.pms[name].norm = self.pms[name].norm.replace(match.group(), "")
                self.pms[name].bank = True
                self.clear(name)
                return

    def acro(self, name: str):
        acr = "".join(
            wrd[0]
            for wrd in self.pms[name].norm.split(" ")
            if not wrd.isupper()
            and not wrd.startswith(("(", "the"))
            and len(wrd) > 2
            or (len(wrd) > 1 and wrd.istitle())
        ).upper()
        if len(acr) >= 2 and (
            f"({acr})" in self.pms[name].norm
            or self.pms[name].norm.startswith(acr + " ")
            or self.pms[name].norm.endswith(" " + acr)
        ):
            self.pms[name].norm = self.pms[name].norm.replace(acr, "", 1).replace("()", "", 1).strip()
            self.pms[name].acronym = acr
            self.clear(name)

    def slim(self, name: str):
        for rm in self.re_glut:
            self.pms[name].norm = re.sub(rm, "", self.pms[name].norm)

    def i18n(self, name: str):
        for src, trgt in self.i18n_map.items():
            self.pms[name].norm = self.pms[name].norm.replace(src, trgt)

    def clear(self, name: str):
        self.pms[name].norm = self.pms[name].norm.replace("()", "").replace("  ", " ").strip(" -")

    def __call__(self, s: str) -> PmUni:
        # если в словаре замен есть текущее назвние - меняем, иначе берем строку до запятой
        self.pms[s] = PmUni(norm=self.pm_map.get(s, s.split(",")[0]))
        # вырезаем мусорные добавки
        self.slim(s)
        # заменяем локальные символы на англ:
        self.i18n(s)
        # находим и вырезаем аббревиатуру, если есть
        self.acro(s)
        # уменьшаем все буквы
        self.pms[s].norm = self.pms[s].norm.lower()
        # находим и вырезаем страны, если есть
        self.countries(s)
        self.bank(s)
        self.extra(s)
        self.alias(s)
        self.bank(s)
        self.countries(s)
        self.extra(s)
        # вырезаем каждый символ rms
        [self.pms[s].norm.replace(rm, "") for rm in self.rms]

        return self.pms[s]


class BaseExClient(BaseClient):
    @abstractmethod
    def pm_type_map(self, type_: models.Pmex) -> str: ...

    # 19: Список поддерживаемых валют тейкера
    @abstractmethod
    async def curs(self) -> list[types.CurE]:  # {cur.exid: cur.ticker}
        ...

    # 20: Список платежных методов
    @abstractmethod
    async def pms(self, cur: models.Cur = None) -> dict[int | str, types.Pm]:  # {pm.exid: pm}
        ...

    # 21: Список платежных методов по каждой валюте
    @abstractmethod
    async def cur_pms_map(self) -> MapOfIdsList:  # {cur.exid: [pm.exid]}
        ...

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    @abstractmethod
    async def coins(self) -> list[types.CoinE]:  # {coin.exid: coin.ticker}
        ...

    # 23: Список пар валюта/монет
    @abstractmethod
    async def pairs(self) -> MapOfIdsList: ...

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    @abstractmethod
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[types.BaseAd]:  # {ad.id: ad}
        ...

    # 42: Чужая объява по id
    @abstractmethod
    async def ad(self, ad_id: int) -> types.BaseAd: ...

    # Преобразрование объекта объявления из формата биржи в формат xync
    @abstractmethod
    async def ad_epyd2pydin(self, ad: types.BaseAd) -> types.BaseAdIn: ...  # my_uid: for MyAd

    # 99: Страны
    @abstractmethod
    async def countries(self) -> list[Struct]: ...

    # Импорт Pm-ов (с Pmcur-, Pmex- и Pmcurex-ами) и валют (с Curex-ами) с биржи в бд
    async def set_pmcurexs(self):
        # Curs
        cur_pyds: list[types.CurE] = await self.curs()
        curs: dict[int | str, models.Cur] = {
            cur_pyd.exid: (
                await models.Cur.update_or_create({"rate": cur_pyd.rate}, ticker=cur_pyd.ticker, id=cur_pyd.exid)
            )[0]
            for cur_pyd in cur_pyds
        }
        curexs: list[models.Curex] = [models.Curex(**c.model_dump(), cur=curs[c.exid], ex=self.ex) for c in cur_pyds]
        # Curex
        await models.Curex.bulk_create(
            curexs, update_fields=["minimum", "rounding_scale"], on_conflict=["cur_id", "ex_id"]
        )

        countries = await self.countries()

        cur_map = {
            172: "CNY",
            8: "KRW",
            25: "MMK",
        }
        for c in countries:
            if c.cur_id not in curs:
                cur, _ = await models.Cur.get_or_create(id=c.cur_id, ticker=cur_map[c.cur_id])
                c.cur_id = cur.id
        # Country preparing
        # countries = sorted(
        #     (c for c in countries if c.code not in (999, 9999, 441624, 999999)), key=lambda x: x.name
        # )  # sort and filter
        cnts = {
            "BosniaandHerzegovina": "BA",
            "Brunei": "BN",
            "Congo": "CD",
            "Djibouti": "DJ",
            "Guinea": "GN",
            "Iraq": "IQ",
            "Kyrgyzstan": "KG",
            "ComorosIslands": "KM",
            "Liberia": "LR",
            "Libya": "LY",
            "Yemen": "YE",
            "Zimbabwe": "ZW",
            "United States of America": "US",
            "Lebanon": "LB",
            "Central African Republic": "XA",
            "Laos": "LA",
            "Tanzania": "TZ",
            "Bangladesh": "BD",
        }
        [setattr(c, "short", cnts.get(c.name, c.short)) for c in countries]  # add missed shortNames
        # Countries create
        cntrs: [models.Country] = [models.Country(**msgspec.to_builtins(c)) for c in countries]
        # ids only for HTX
        await models.Country.bulk_create(cntrs, ignore_conflicts=True)
        # todo: curexcountry

        # Pms
        pms_epyds: dict[int | str, types.Pm] = {
            k: v for k, v in sorted((await self.pms()).items(), key=lambda x: x[1].name)
        }  # sort by name
        pms: dict[int | str, models.Pm] = dict({})
        prev = 0, "", ""  # id, normd-name, orig-name
        cntrs = [c.lower() for c in await models.Country.all().values_list("name", flat=True)]
        uni = PmUnifier(cntrs)
        for k, pm in pms_epyds.items():
            pmu: PmUni = uni(pm.name)
            if prev[2] == pm.name and pmu.country == prev[3]:  # оригинальное имя не уникально на этой бирже
                logging.warning(f"Pm: '{pm.name}' duplicated with ids {prev[0]}: {k} on {self.ex.name}")
                # новый Pm не добавляем, а берем старый с этим названием
                pm_ = pms.get(prev[0], await models.Pm.get_or_none(norm=prev[1]))
                # и добавляем Pmex для него
                await models.Pmex.update_or_create({"name": pm.name}, ex=self.ex, exid=k, pm=pm_)
            elif (
                prev[1] == pmu.norm and pmu.country == prev[3]
            ):  # 2 разных оригинальных имени на этой бирже совпали при нормализации
                logging.error(
                    f"Pm: {pm.name}&{prev[2]} overnormd as {pmu.norm} with ids {prev[0]}: {k} on {self.ex.name}"
                )
                # новый Pm не добавляем, только Pmex для него
                # новый Pm не добавляем, а берем старый с этим названием
                pm_ = pms.get(prev[0], await models.Pm.get_or_none(norm=prev[1]))
                # и добавляем.обновляем Pmex для него
                await models.Pmex.update_or_create({"pm": pm_}, ex=self.ex, exid=k, name=pm.name)
            else:
                # todo: add logo and all other
                d = pmu.df_unq()
                d.update(
                    {
                        "country": await models.Country.get(name__iexact=cnt) if (cnt := d.get("country")) else None,
                        "logo": pm.logo,
                        "type_": pm.type_,
                    }
                )
                try:
                    pms[k], _ = await models.Pm.update_or_create(**d)
                except (MultipleObjectsReturned, IntegrityError) as e:
                    print(d)
                    raise e
            prev = k, pmu.norm, pm.name, pmu.country
        # Pmexs
        pmexs = [models.Pmex(exid=k, ex=self.ex, pm=pm, name=pms_epyds[k].name) for k, pm in pms.items()]
        await models.Pmex.bulk_create(pmexs, on_conflict=["ex_id", "exid"], update_fields=["pm_id", "name", "name_"])
        # Pmex banks
        for k, pm in pms_epyds.items():
            if banks := pm.banks:
                pmex = await models.Pmex.get(ex=self.ex, exid=k)  # pm=pms[k],
                for b in banks:
                    await models.PmexBank.update_or_create({"name": b.name}, exid=b.exid, pmex=pmex)

        cur2pms = await self.cur_pms_map()
        # # Link PayMethods with currencies
        pmcurs = set()
        for cur_id, exids in cur2pms.items():
            for exid in exids:
                pmcurs.add(
                    (
                        await models.Pmcur.update_or_create(
                            cur=curs[cur_id],
                            pm=pms.get(exid)
                            or (await models.Pmex.get(ex=self.ex, exid=exid).prefetch_related("pm")).pm,
                        )
                    )[0]
                )
        # pmcurexs = [Pmcurex(pmcur=pmcur, ex=self.ex) for pmcur in pmcurs]
        # await Pmcurex.bulk_create(pmcurexs)

    # Импорт монет (с Coinex-ами) с биржи в бд
    async def set_coinexs(self):
        coins: list[types.CoinE] = await self.coins()
        coins_db: dict[int, models.Coin] = {
            c.exid: (await models.Coin.update_or_create(ticker=c.ticker))[0] for c in coins
        }
        coinexs: list[models.Coinex] = [
            models.Coinex(coin=coins_db[c.exid], ex=self.ex, exid=c.exid, minimum=c.minimum) for c in coins
        ]
        await models.Coinex.bulk_create(coinexs, update_fields=["minimum"], on_conflict=["coin_id", "ex_id"])

    # Сохранение чужого объявления (с Pm-ами) в бд
    async def ad_pydin2db(self, ad_pydin: types.BaseAdIn) -> models.Ad:
        df, unq = ad_pydin.args()
        ad_db, _ = await models.Ad.update_or_create(df, **unq)
        if getattr(ad_pydin, "pms_", None):  # if it ListItem, not Full One # todo: remove?
            await ad_db.pms.add(*ad_pydin.pms_)
        return ad_db
