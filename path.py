import json
import re
from fastapi import FastAPI , Path, HTTPException
with open("patient.json","r") as file:
    data = json.load(file)
#print(data)
patients = data['patients']
app2 = FastAPI()

@app2.get('/view')
async def viewpatients():
    return data

@app2.get('/view/{patientid}')
async def viewPatient(patientid:str = Path(...,example="P1001")):
    for patient in patients:
        if patient["patient_id"]==patientid:
            return patient
    else:
       raise HTTPException(status_code=404,detail="patient not found")

@app2.get('/viewbycorrectpatientid/{patientid}')
async def viewPatient(patientid:str = Path(...,example="P1001")):
    if not re.match(r"^P[0-9]{4}$",patientid):
        raise HTTPException(status_code=400,detail="invalid patient id format")
    for patient in patients:
        if patient["patient_id"]==patientid:
            return patient
    else:
        raise HTTPException(status_code=404,detail="patient with the id not found")
