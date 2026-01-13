from pydantic import BaseModel

class PatientSchema(BaseModel): # Step 1: Define a Pydantic model for patient data validation
    name : str
    age : int
    weight: float
    married : bool
    


def insert_into_DB(patient: PatientSchema):    # Simulate inserting into a database
    print(patient.name)
    print(patient.age)
    print("Inserted into DB")

patient_info = {"name": "John Doe", "age": 30}
patient_info = {"name": "John Doe", "age": 'thirty'} # give an invalid age to see validation in action
patient_info = {"name": "John Doe", "age": '30'} # automatically converts string to int


patient1 = PatientSchema(**patient_info) # Step 2: Create an instance of the Patient model using sample data

insert_into_DB(patient1) # Step 3: Call the function to insert the patient data into the database