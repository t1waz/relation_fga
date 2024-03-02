from pydantic import BaseModel, EmailStr


class ObtainTokenSchemaIn(BaseModel):
    password: str
    email: EmailStr


class RefreshTokenSchemaIn(BaseModel):
    refresh: str
