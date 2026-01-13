from fastapi import FastAPI, Path,  HTTPException, Query
import json

app = FastAPI() # Create an instance of the FastAPI application

# function to load data from the json file
def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data
    
@app.get("/") # Define a route for the root URL
def hello():
    return{"message":"A patient management system"} # Return a JSON response with a greeting message

@app.get("/about") # Define a route for the /about URL
def about():
    return{"message":"Simple FastAPI application to manage patient records"} # Return a JSON response with information about the application

@app.get("/view-all-patients") # route to view all patients
def view_all_patients():
    data = load_data()
    return data

@app.get("/view-patient/{patient_id}") # route to view a specific patient by ID
def view_patient(patient_id: str = Path(..., description="ID of patient", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found") # Raise a 404 error if the patient ID is not found

@app.get("/sort") # route to sort patients
def sort_patients(sort_by:str = Query(..., description="sort on the basis of height, weight, age or bmi"), 
                  order_by:str = Query("asc", description="sort in ascending or descending order")):

    valid_fields = ["height", "weight", "age", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. select from {valid_fields}")

    if order_by not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid Order. It must be 'asc' or 'desc'")
    
    data = load_data()
    sorted_order = True if order_by == "desc" else False # Determine the sorting order
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sorted_order) # Sort the data based on the specified field and order
    return sorted_data
