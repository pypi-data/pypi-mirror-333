from typing import Annotated, Optional
from pydantic import Field

from .common import ModelBase


class FismaInventoryItemBase(ModelBase):
    system_id: Annotated[int, Field(alias='System ID')]
    vasi_id: Annotated[int, Field(alias="VASI ID")]
    system_name: Annotated[str, Field(alias="System Name")]
    system_acronym: Annotated[str, Field(alias="System Acronym")]
    system_description: Annotated[str, Field(alias="System Description")]
    group_tagging: Annotated[Optional[str], Field(alias="Group Tagging")] = None
