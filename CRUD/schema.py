from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional


class PatientSchema(BaseModel):

    id: Annotated[
        str, Field(..., description="Unique identifier for the patient", example="P001")
    ]
    name: Annotated[
        str,
        Field(
            ...,
            description="Full name of the patient",
            example="John Doe",
            min_length=3,
            max_length=50,
        ),
    ]
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(..., description="Gender of the patient", example="male"),
    ]
    age: Annotated[
        int,
        Field(..., description="Age of the patient in years", example=30, ge=0, le=120),
    ]
    city: Annotated[
        str,
        Field(..., description="City where the patient resides", example="New York"),
    ]
    height: Annotated[
        float,
        Field(..., description="Height of the patient in meters", example=1.755, gt=0),
    ]
    weight: Annotated[
        float,
        Field(
            ..., description="Weight of the patient in kilograms", example=70.0, gt=0
        ),
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate and return the Body Mass Index (BMI) of the patient."""
        return round(self.weight / (self.height**2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """Determine the health verdict based on the BMI value."""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"


class PatientUpdateSchema(BaseModel):

    name: Annotated[
        Optional[str],
        Field(
            None,
            description="Full name of the patient",
            example="John Doe",
            min_length=3,
            max_length=50,
        ),
    ]
    gender: Annotated[
        Optional[Literal["male", "female", "other"]],
        Field(None, description="Gender of the patient", example="male"),
    ]
    age: Annotated[
        Optional[int],
        Field(
            None, description="Age of the patient in years", example=30, ge=0, le=120
        ),
    ]
    city: Annotated[
        Optional[str],
        Field(None, description="City where the patient resides", example="New York"),
    ]
    height: Annotated[
        Optional[float],
        Field(None, description="Height of the patient in meters", example=1.755, gt=0),
    ]
    weight: Annotated[
        Optional[float],
        Field(
            None, description="Weight of the patient in kilograms", example=70.0, gt=0
        ),
    ]
