from datetime import datetime

from pydantic import BaseModel
from x_model.types import New, Upd

from xync_schema.enums import AdStatus, OrderStatus, PmType
from xync_schema import models


class UnitEx(BaseModel):
    exid: int | str
    ticker: str
    scale: int


class CoinEx(UnitEx):
    p2p: bool = None
    minimum: float | None = None


class CurEx(UnitEx):
    rounding_scale: int | None = None
    minimum: int | None = None


class PmexBank(BaseModel):
    id: int | None = None
    exid: str
    name: str


class PmIn(New):
    norm: str
    acronym: str | None = None
    alias: str | None = None
    extra: str | None = None
    bank: bool | None = None
    country_id: int | None = None
    type_: PmType | None = None
    logo: str | None = None


class PmOut(PmIn, Upd):
    banks: list[PmexBank] | None = None


# class Pmcur(BaseModel):
#     id: int | None = None
#     pm_id: int
#     cur_id: int


class CredIn(BaseModel):
    id: int | None = None
    exid: int
    pmcur: models.Pmcur
    actor: models.Actor
    detail: str = ""
    name: str = ""
    banks: list[str] | None = None

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "exid", "ch", "pmcur"
        df: tuple[str, ...] = "detail", "name"
        d = self.model_dump()
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class FiatIn(BaseModel):
    # unq
    id: int = None
    cred: models.Cred
    # df
    amount: float
    target: float | None = None

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "cred"
        df: tuple[str, ...] = "amount", "target"
        d = self.model_dump()
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class BaseAd(BaseModel):
    id: int | None = None
    price: float


class BaseAdIn(BaseAd):
    exid: int
    min_fiat: float
    max_fiat: float | None = None
    detail: str | None = None
    auto_msg: str | None = None
    status: AdStatus = AdStatus.active
    maker: models.Actor = None
    direction: models.Direction

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "exid", "maker", "direction"
        df: tuple[str, ...] = "price", "price", "min_fiat", "max_fiat", "detail", "auto_msg", "status"
        d = self.model_dump(exclude_none=True)
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class AdBuyIn(BaseAdIn):
    pms_: list[models.Pm]


class AdSaleIn(BaseAdIn):
    creds_: list[models.Cred]


class BaseOrder(BaseModel):
    id: int | None = None


class Order(BaseModel):
    id: int
    amount: float
    status: str
    actions: dict | None = {}
    cred: models.Cred.out_type()
    is_sell: bool
    actor: int | None = None
    created_at: datetime
    payed_at: datetime | None = None
    appealed_at: datetime | None = None
    confirmed_at: datetime | None = None
    msgs: int = 0
    topic: int


class OrderIn(BaseModel):
    id: int = None
    exid: int
    amount: float
    maker_topic: int | None = None
    taker_topic: int | None = None
    status: OrderStatus = OrderStatus.created
    created_at: datetime
    payed_at: datetime | None = None
    confirmed_at: datetime | None = None
    appealed_at: datetime | None = None
    ad: models.Ad
    cred: models.Cred
    taker: models.Actor

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "exid", "amount", "maker_topic", "taker_topic", "ad", "cred", "taker"
        df: tuple[str, ...] = "status", "created_at", "payed_at", "confirmed_at", "appealed_at"
        d = self.model_dump(exclude_none=True)
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class UreadMsgs(BaseModel):
    order_id: int
    unread_cnt: int
