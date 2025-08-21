from pydantic import BaseModel, Field as PField
from sqlmodel import SQLModel, Field, Column, ARRAY, String
from datetime import datetime, timezone
from typing import Any


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    content: str
    category: str
    tags: list[str] = Field(min_items=1, sa_column=Column(ARRAY(String)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PostCreate(BaseModel):
    title: str = PField(max_length=100)
    content: str
    category: str
    tags: list[str] = PField(min_length=1)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "title": "First Post",
                "content": "This is my first blog post",
                "category": "Programming",
                "tags": ["Technology", "IT"]
            }
        }


class PostUpdate(BaseModel):
    title: str | None = PField(default=None, max_length=100)
    content: str | None = PField(default=None)
    category: str | None = PField(default=None)
    tags: list[str] | None = PField(default=None)

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "title": "First Post",
                "content": "This is my first blog post",
                "category": "Programming",
                "tags": ["Technology", "IT"]
            }
        }


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
