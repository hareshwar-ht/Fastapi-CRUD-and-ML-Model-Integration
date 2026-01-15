from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from schema import PatientSchema, PatientUpdateSchema

app = FastAPI()  # Create an instance of the FastAPI application


# function to load data from the json file
def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data


# function to save data in json file (json format)
def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)


@app.get("/")  # Define a route for the root URL
def hello():
    return {
        "message": "A patient management system"
    }  # Return a JSON response with a greeting message


@app.get("/about")  # Define a route for the /about URL
def about():
    return {
        "message": "Simple FastAPI application to manage patient records"
    }  # Return a JSON response with information about the application


@app.get("/view-all-patients")  # route to view all patients
def view_all_patients():
    data = load_data()
    return data


@app.get("/view-patient/{patient_id}")  # route to view a specific patient by ID
def view_patient(patient_id: str = Path(..., description="ID of patient")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(
        status_code=404, detail="Patient not found"
    )  # Raise a 404 error if the patient ID is not found


@app.get("/sort")  # route to sort patients
def sort_patients(
    sort_by: str = Query(
        ..., description="sort on the basis of height, weight, age or bmi"
    ),
    order_by: str = Query("asc", description="sort in ascending or descending order"),
):

    valid_fields = ["height", "weight", "age", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid field. select from {valid_fields}"
        )

    if order_by not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid Order. It must be 'asc' or 'desc'"
        )

    data = load_data()
    sorted_order = True if order_by == "desc" else False  # Determine the sorting order
    sorted_data = sorted(
        data.values(), key=lambda x: x[sort_by], reverse=sorted_order
    )  # Sort the data based on the specified field and order
    return sorted_data


@app.post("/add-patient")  # route to add a new patient
def add_patient(patient: PatientSchema):
    # Load existing data
    data = load_data()

    # check if patient with the same id already exists then raise error
    if patient.id in data:
        raise HTTPException(
            status_code=400, detail="Patient with this ID already exists"
        )

    # Add the new patient
    data[patient.id] = patient.model_dump(exclude=["id"])

    # save the updated data back to the file in json format
    save_data(data)

    # Return a success response
    return JSONResponse(
        status_code=201,
        content={"message": "Patient added successfully", "patient_id": patient.id},
    )


@app.put("/update-patient/{patient_id}")  # route to update an existing patient
def update_patient(
    patient_id: str = Path(..., description="ID of patient to update"),
    patient_update: PatientUpdateSchema = ...,
):
    # Load existing data
    data = load_data()

    # Check if the patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update the patient details
    existing_patient_data = data[patient_id]

    updated_patient_data = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_data.items():
        existing_patient_data[key] = value  # Update only the provided fields

    # To recalculate BMI and verdict after update
    existing_patient_data["id"] = patient_id
    patient_pydantic_obj = PatientSchema(**existing_patient_data)

    existing_patient_data_with_recalculated_fields = patient_pydantic_obj.model_dump(
        exclude=["id"]
    )

    # add dictionary back to data
    data[patient_id] = existing_patient_data_with_recalculated_fields

    # Save the updated data back to the file in json format
    save_data(data)

    # Return a success response
    return JSONResponse(
        status_code=200,
        content={"message": "Patient updated successfully", "patient_id": patient_id},
    )


@app.delete("/delete-patient/{patient_id}")  # route to delete a patient
def delete_patient(patient_id: str = Path(..., description="ID of patient to delete")):

    # Load existing data
    data = load_data()

    # Check if the patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Delete the patient
    del data[patient_id]

    # Save the updated data back to the file in json format
    save_data(data)

    # Return a success response
    return JSONResponse(
        status_code=200,
        content={"message": "Patient deleted successfully", "patient_id": patient_id},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
