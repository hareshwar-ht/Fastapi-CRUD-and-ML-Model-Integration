import streamlit as st
import requests

AI_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Prediction")

st.markdown("Enter your details below")

# Input Fields
age = st.number_input("Age", min_value=1, max_value=120, value=36)
height_cm = st.number_input("Height in cm", min_value=10, value=136)
weight_kg = st.number_input("Weight in Kg", min_value=2, value=36)
income_lakhs = st.number_input("Annual Income in lakhs", min_value=1, value=36)
smoke_status = st.selectbox("Are you smoking? ", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    options=[
        "Government",
        "IT",
        "Education",
        "Manufacturing",
        "Business",
        "Self-Employed",
        "Healthcare",
        "Other",
    ],
)

if st.button("Submit"):
    input_data = {
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "income_lakhs": income_lakhs,
        "smoke_status": smoke_status,
        "city": city,
        "occupation": occupation,
    }

    try:
        response = requests.post(AI_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(
                f"Predicted insurance premium category : **{result['predicted_category']}**"
            )
        else:
            st.error(f"API error : {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the service. Make sure it running on the proper port."
        )
