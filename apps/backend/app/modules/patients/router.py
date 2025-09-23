from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.rbac import require_superadmin
from app.modules.users.models import User
from .dto import PatientCreate, PatientRead, PatientUpdate
from .service import (
    list_patients_for_user,
    create_patient,
    get_patient,
    update_patient,
    delete_patient,
)


router = APIRouter()


@router.get("/", response_model=List[PatientRead])
async def list_my_patients(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await list_patients_for_user(db, current_user.id)


@router.post("/", response_model=PatientRead)
async def create_my_patient(
    payload: PatientCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_patient(
        db,
        current_user.id,
        name=payload.name,
        dob=payload.dob,
        gender=payload.gender,
        blood_group=payload.blood_group,
        ethnicity=payload.ethnicity,
    )


@router.get("/{patient_id}", response_model=PatientRead)
async def get_my_patient(
    patient_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    patient = await get_patient(db, current_user.id, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=PatientRead)
async def update_my_patient(
    patient_id: UUID,
    payload: PatientUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    patient = await update_patient(
        db,
        current_user.id,
        patient_id,
        name=payload.name,
        dob=payload.dob,
        gender=payload.gender,
        blood_group=payload.blood_group,
        ethnicity=payload.ethnicity,
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.delete("/{patient_id}", status_code=204)
async def delete_my_patient(
    patient_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ok = await delete_patient(db, current_user.id, patient_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Patient not found")
    return None


# Superadmin management of patients for any user (optional)
@router.get(
    "/admin/by-user/{user_id}",
    response_model=List[PatientRead],
    dependencies=[Depends(require_superadmin)],
)
async def list_patients_admin(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await list_patients_for_user(db, user_id)
