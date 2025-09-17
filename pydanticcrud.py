import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app4 = FastAPI(title="Patient Management API")


class Patient(BaseModel):
    patient_id: str = Field(..., example="P1001", pattern="^P[0-9]{4}$")
    name: str = Field(..., example="Ramesh Kumar", min_length=3)
    age: int = Field(..., example=40, ge=0, le=120)
    gender: str = Field(..., example="Male")
    phone: str = Field(..., example="+91-9876543210")
    condition: Optional[str] = Field(None, example="Diabetes Type 2")

# Load patient data from JSON
patients_db: List[Patient] = []

try:
    with open("patient.json", "r") as file:
        data = json.load(file)
        for item in data.get("patients", []):
            patients_db.append(Patient(**item))
except FileNotFoundError:
    print("patient.json file not found. Starting with empty database.")
except Exception as e:
    print(f"Error loading JSON data: {e}")

# CRUD Endpoints

# Create a patient
@app4.post("/patients", response_model=Patient)
def create_patient(patient: Patient):
    for p in patients_db:
        if p.patient_id == patient.patient_id:
            raise HTTPException(status_code=400, detail="Patient ID already exists")
    patients_db.append(patient)
    return patient

# Read all patients with optional sorting
@app4.get("/patients", response_model=List[Patient])
def get_patients(
    sort_by: Optional[str] = Query("name", pattern="^(name|age|patient_id)$"),
    order: str = Query("asc", pattern="^(asc|desc)$")
):
    sorted_patients = sorted(
        patients_db,
        key=lambda x: getattr(x, sort_by),
        reverse=(order == "desc")
    )
    return sorted_patients

# Read single patient by ID
@app4.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: str):
    for patient in patients_db:
        if patient.patient_id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

# Update a patient by ID
@app4.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: str, updated_patient: Patient):
    for index, patient in enumerate(patients_db):
        if patient.patient_id == patient_id:
            patients_db[index] = updated_patient
            return updated_patient
    raise HTTPException(status_code=404, detail="Patient not found")

# Delete a patient by ID
@app4.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    for index, patient in enumerate(patients_db):
        if patient.patient_id == patient_id:
            del patients_db[index]
            return {"detail": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")
