from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator,
    model_validator,
    computed_field,
)
from typing import List, Dict, Optional, Annotated


# nested models can also be created by defining another Pydantic model and using it as a type for a field in the parent model.


class Address(BaseModel):

    city: str
    state: str
    zip_code: str


class PatientSchema(
    BaseModel
):  # Step 1: Define a Pydantic model for patient data validation

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            title="name of the patient",
            description="name must be between 3 and 50 characters",
            examples=["John Doe", "Jane Smith"],
        ),
    ]
    email: EmailStr
    instaHandle: AnyUrl
    age: int = Field(gt=0, lt=200)  # age must be between 0 and 200
    height: Annotated[
        float, Field(gt=0, strict=True)
    ]  # height must be a positive float and strict type
    weight: Annotated[
        float, Field(gt=0, strict=True)
    ]  # weight must be a positive float and strict type
    married: Optional[bool] = None
    gender: str = "Male"
    allergies: Optional[List[str]] = Field(
        default=None, max_length=5
    )  # by default all defined fields are required unless specified as Optional
    contact_details: Dict[str, str]
    address: Address = Field(
        title="Address of the patient",
        description="Address must include city, state, and zip code",
    )

    # field validators = decorators that validate individual fields
    # field_validator("field_name", mode="before" or "after" (default is "after"))
    # mode specifies whether to run the validator before or after other validations like type checking, conversions, etc.
    @field_validator(
        "email", mode="before"
    )  # Step 4: Custom validator for email field.
    @classmethod
    def email_validatior(cls, value):
        if value.split("@")[-1] != "heaptrace.com":
            raise ValueError("Email domain must be heaptrace.com")
        return value

    # model validators = decorators that validate the entire model after all fields have been validated
    # model_validator("after" or "before" (default is "after"))
    @model_validator(
        mode="after"
    )  # Step 5: Custom model-level validator to ensure age is realistic.
    @classmethod
    def emergency_contact_validator(cls, model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError(
                "Emergency contact details are required for patients over 60 years old."
            )
        return model

    # computed fields = fields that are derived from other fields in the model
    @computed_field  # Step 6: Computed field to categorize patients based on age
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi


def insert_into_DB(patient: PatientSchema):  # Simulate inserting into a database
    print(patient.name)
    print(patient.email)
    print(patient.instaHandle)
    print(patient.age)
    print(patient.height)
    print(patient.weight)
    print(patient.bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.address.city)
    print(patient.address.state)
    print(patient.address.zip_code)
    print("Inserted into DB")


patient_info = {"name": "John Doe", "age": 30}
patient_info = {
    "name": "John Doe",
    "age": "thirty",
}  # give an invalid age to see validation in action
patient_info = {"name": "John Doe", "age": "30"}  # automatically converts string to int
patient_info = {
    "name": "John Doe",
    "age": 305,
    "weight": 70.5,
    "married": False,
    "allergies": ["pollen", "dust"],
    "contact_details": {"phone": "965456441", "email": "abc@example.com"},
}


address_info = {"city": "Pune", "state": "Maharashtra", "zip_code": "411057"}

address = Address(**address_info)

# with optional fields missing (need defaults value to set optional fields)
patient_info = {
    "name": "John Doe",
    "email": "abc@heaptrace.com",
    "age": 105,
    "height": 1.75,
    "weight": 70.5,
    "married": False,
    "instaHandle": "https://www.instagram.com/johndoe",
    "contact_details": {"emergency": "987654321"},
    "address": address,
}


patient1 = PatientSchema(
    **patient_info
)  # Step 2: Create an instance of the Patient model using sample data

insert_into_DB(
    patient1
)  # Step 3: Call the function to insert the patient data into the database

print()
# Exporting Pydantic Models with Nested Structures = serialization.
print(
    patient1.model_dump(
        exclude={
            "address": {"state"},
            "married": True,
            "allergies": True,
            "name": True,
        },
        exclude_unset=True,
    ),
    type(patient1.model_dump()),
)  # Serialize the model format to a dictionary
print()
print(
    patient1.model_dump_json(include={"name": True, "address": {"city"}, "bmi": True}),
    type(patient1.model_dump_json()),
)  # Serialize the model format to a JSON string

print()
print(patient1)  # Print the model instance to see the formatted output
