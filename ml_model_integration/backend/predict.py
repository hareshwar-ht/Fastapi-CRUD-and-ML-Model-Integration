import pandas as pd
import pickle

# Load the pre-trained machine learning model
with open("models/model.pkl", "rb") as file:
    model = pickle.load(file)

# Extract model version from  MLFlow
MODEL_VERSION = "1.0.0"

# Get class labels from the model (IMP for matching probabilities to the class name)
category_labels = model.classes_.tolist()


def predict_premium_category(user_input: dict):

    input_df = pd.DataFrame([user_input])

    # predict the category
    predicted_category = model.predict(input_df)[0]

    # get probabilities of all the categories
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    # create mapping -> {category_name : probability}
    category_probs = dict(
        zip(category_labels, map(lambda p: round(p, 4), probabilities))
    )

    # return the output
    return {
        "predicted category": predicted_category,
        "confidence": confidence,
        "category probabilities": category_probs,
    }
