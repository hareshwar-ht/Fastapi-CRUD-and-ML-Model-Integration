from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated, Dict
from config import tier_1_Cities, tier_2_Cities


class UserInputSchema(BaseModel):

    age: Annotated[
        int,
        Field(
            ...,
            gt=0,
            lt=120,
            description="Age must be a greater than 0 and less than 120",
        ),
    ]
    height_cm: Annotated[float, Field(..., gt=0, description="Height in centimeters")]
    weight_kg: Annotated[float, Field(..., gt=0, description="Weight in kilograms")]
    income_lakhs: Annotated[float, Field(..., gt=0, description="Income in lakhs")]
    smoke_status: Annotated[
        bool, Field(..., description="Whether the user smokes or not")
    ]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[
        Literal[
            "Government",
            "IT",
            "Education",
            "Manufacturing",
            "Business",
            "Self-Employed",
            "Healthcare",
        ],
        Field(..., description="Occupation of the user"),
    ]

    @field_validator("city", mode="after")
    @classmethod
    def city_titleCase(cls, value: str) -> str:
        value = value.strip().title()
        return value

    @computed_field
    @property
    def bmi(self) -> float:
        """Compute Body Mass Index (BMI)"""
        height_m = self.height_cm / 100
        return self.weight_kg / (height_m**2)

    @computed_field
    @property
    def age_group(self) -> str:
        """Compute age group"""
        if self.age > 0 and self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle age"
        else:
            return "senior"

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        """Compute lifestyle risk based on smoking status and BMI"""
        if self.smoke_status and self.bmi > 30:
            return "high"
        elif self.smoke_status and self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def city_tier(self) -> int:
        """Compute city tier based on city name"""
        if self.city in tier_1_Cities:
            return 1
        elif self.city in tier_2_Cities:
            return 2
        else:
            return 3


class ModelOutputSchema(BaseModel):

    predicted_category: str = Field(
        ..., description="The predicted insurance premium category"
    )
    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted category (range 0 to 1)",
    )
    class_probs: Dict[str, float] = Field(
        ..., description="Probability distribution of all categories"
    )
