from typing import Annotated, Optional
from pydantic import Field

from .common import ModelBase


class EmassSystemBase(ModelBase):
    system_id: Annotated[int, Field(alias='systemId')]
    name: str
    acronym: str
    description: Optional[str] = None
    is_financial_management: Annotated[Optional[bool], Field(alias="isFinancialManagement")] = None