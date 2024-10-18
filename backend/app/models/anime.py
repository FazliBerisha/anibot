from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class AnimeBase(BaseModel):
    title: str
    genres: List[str]
    release_date: datetime
    episodes: int
    synopsis: str

class AnimeCreate(AnimeBase):
    pass

class AnimeUpdate(BaseModel):
    title: Optional[str] = None
    genres: Optional[List[str]] = None
    release_date: Optional[datetime] = None
    episodes: Optional[int] = None
    synopsis: Optional[str] = None

class Anime(AnimeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
