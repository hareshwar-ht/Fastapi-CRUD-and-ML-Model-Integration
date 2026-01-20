from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schema import UserInputSchema, ModelOutputSchema
from predict import predict_premium_category, MODEL_VERSION, model
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction System"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model version": MODEL_VERSION,
        "model loaded": model is not None,
    }


@app.post("/predict", response_model=ModelOutputSchema)
def predict(input_data: UserInputSchema):

    # Convert input data to DataFrame
    input_model_data = {
        "bmi": input_data.bmi,
        "age_group": input_data.age_group,
        "city_tier": input_data.city_tier,
        "occupation": input_data.occupation,
        "income_lakhs": input_data.income_lakhs,
        "lifestyle_risk": input_data.lifestyle_risk,
    }

    try:
        # Make prediction
        prediction = predict_premium_category(input_model_data)

        # Return the prediction result aligned with ModelOutputSchema
        return {
            "predicted_category": prediction["predicted category"],
            "confidence": prediction["confidence"],
            "class_probs": prediction["category probabilities"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8005)
