from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema import UserInputSchema
import pickle
import pandas as pd

# Load the pre-trained machine learning model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI()


@app.post("/predict")
def predict(input_data: UserInputSchema):

    # Convert input data to DataFrame
    input_model_data = pd.DataFrame(
        [
            {
                "bmi": input_data.bmi,
                "age_group": input_data.age_group,
                "city_tier": input_data.city_tier,
                "occupation": input_data.occupation,
                "income_lakhs": input_data.income_lakhs,
                "lifestyle_risk": input_data.lifestyle_risk,
            }
        ]
    )

    # Make prediction
    prediction = model.predict(input_model_data)[0]

    # Return the prediction result
    return JSONResponse(status_code=200, content={"predicted_category": prediction})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
