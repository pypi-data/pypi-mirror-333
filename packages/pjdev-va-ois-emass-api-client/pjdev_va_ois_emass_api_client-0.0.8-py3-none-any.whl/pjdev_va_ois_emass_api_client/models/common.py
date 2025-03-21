from pydantic import BaseModel, ConfigDict

class ModelBase(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)