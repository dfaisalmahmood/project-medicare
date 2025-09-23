from datetime import date
from pydantic import BaseModel
from uuid import UUID


class PatientCreate(BaseModel):
    name: str
    dob: date | None = None
    gender: str | None = None
    blood_group: str | None = None
    ethnicity: str | None = None


class PatientUpdate(BaseModel):
    name: str | None = None
    dob: date | None = None
    gender: str | None = None
    blood_group: str | None = None
    ethnicity: str | None = None


class PatientRead(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    dob: date | None = None
    gender: str | None = None
    blood_group: str | None = None
    ethnicity: str | None = None

    class Config:
        from_attributes = True
