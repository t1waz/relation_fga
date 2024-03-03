from pydantic import BaseModel, StrictStr, field_validator


class CreateStoreSchemaIn(BaseModel):
    name: StrictStr

    @field_validator("name")
    @classmethod
    def name_should_be_at_least_5_chars(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("name too short")

        return v
