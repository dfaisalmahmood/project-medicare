from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from .models import Patient


async def list_patients_for_user(db: AsyncSession, user_id: UUID) -> list[Patient]:
    res = await db.execute(select(Patient).where(Patient.user_id == user_id))
    return list(res.scalars().all())


async def get_patient(
    db: AsyncSession, user_id: UUID, patient_id: UUID
) -> Patient | None:
    res = await db.execute(
        select(Patient).where(Patient.id == patient_id, Patient.user_id == user_id)
    )
    return res.scalars().first()


async def create_patient(
    db: AsyncSession,
    user_id: UUID,
    *,
    name: str,
    dob=None,
    gender: str | None = None,
    blood_group: str | None = None,
    ethnicity: str | None = None,
) -> Patient:
    patient = Patient(
        user_id=user_id,
        name=name,
        dob=dob,
        gender=gender,
        blood_group=blood_group,
        ethnicity=ethnicity,
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient


async def update_patient(
    db: AsyncSession,
    user_id: UUID,
    patient_id: UUID,
    *,
    name: str | None = None,
    dob=None,
    gender: str | None = None,
    blood_group: str | None = None,
    ethnicity: str | None = None,
) -> Patient | None:
    patient = await get_patient(db, user_id, patient_id)
    if not patient:
        return None
    if name is not None:
        patient.name = name
    if dob is not None:
        patient.dob = dob
    if gender is not None:
        patient.gender = gender
    if blood_group is not None:
        patient.blood_group = blood_group
    if ethnicity is not None:
        patient.ethnicity = ethnicity
    await db.commit()
    await db.refresh(patient)
    return patient


async def delete_patient(db: AsyncSession, user_id: UUID, patient_id: UUID) -> bool:
    patient = await get_patient(db, user_id, patient_id)
    if not patient:
        return False
    await db.delete(patient)
    await db.commit()
    return True
