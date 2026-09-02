# from pydantic import BaseModel


# class LabelCreate(BaseModel):
#     name: str


# class LabelResponse(BaseModel):
#     id: int
#     name: str
#     verified: bool

#     class Config:
#         from_attributes = True


from pydantic import BaseModel
from typing import List


class PackBasicResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class LabelCreate(BaseModel):
    name: str
    verified: bool = False


class LabelResponse(BaseModel):
    id: int
    name: str
    verified: bool

    class Config:
        from_attributes = True


class LabelWithPacks(BaseModel):
    id: int
    name: str
    verified: bool
    packs: List[PackBasicResponse] = []

    class Config:
        from_attributes = True