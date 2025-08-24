from typing import TypedDict


class CardData(TypedDict):
    id: int
    rank: str
    imgUrl: str


class RewardsResult(TypedDict):
    card: CardData | None
    coins: int


class Chapter(TypedDict):
    id: int
    chapter: int
    is_paid: bool
    is_bought: bool
    viewed: bool