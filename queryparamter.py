import json
from fastapi import FastAPI, Query, HTTPException
from typing import Optional

app3 = FastAPI()

# Load patient data
with open("patient.json", "r") as file:
    data = json.load(file)

patients = data["patients"]

@app3.get("/sort")
def sorteddata(
    sortby: Optional[str] = Query("name", regex="^(name|age|patient_id)$", example="age"),
    order: str = Query("asc", regex="^(asc|desc)$", example="desc")
):
    try:
        sorted_patients = sorted(
            patients,
            key=lambda x: x[sortby],
            reverse=(order == "desc")
        )
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    return sorted_patients
