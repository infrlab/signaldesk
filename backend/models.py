"""Input validation and API response types for outreach records."""
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator

Status = Literal['planned', 'sent', 'replied', 'confirmed', 'closed']
Channel = Literal['radio', 'press', 'playlist', 'venue', 'other']


class ContactCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    outlet: str = Field(min_length=2, max_length=120)
    channel: Channel
    status: Status = 'planned'
    due_date: date | None = None
    notes: str = Field(default='', max_length=1000)

    @field_validator('outlet')
    @classmethod
    def clean_outlet(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError('Outlet name must contain at least two non-space characters')
        return value


class ContactPatch(BaseModel):
    model_config = ConfigDict(extra='forbid')
    outlet: str | None = Field(default=None, min_length=2, max_length=120)
    channel: Channel | None = None
    status: Status | None = None
    due_date: date | None = None
    notes: str | None = Field(default=None, max_length=1000)

    @field_validator('outlet')
    @classmethod
    def clean_outlet(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if len(value) < 2:
            raise ValueError('Outlet name must contain at least two non-space characters')
        return value
