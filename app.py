import streamlit as st
import numpy as np
import pickle
import os

# ----------------------------------
# Page config
# ----------------------------------
st.set_page_config(
    page_title="Wine Quality Prediction",
    page_icon="🍷",
    layout="centered"
)

st.title("🍷 Wine Quality Prediction")
st.write("Enter the wine chemical properties to predict quality.")


# ----------------------------------
# Load model and scaler
# ----------------------------------
@st.cache_resource
def load_artifacts():

    # Get the folder where app.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # File paths
    model_path = os.path.join(base_dir, "New_RFmodel.pkl")
    scaler_path = os.path.join(base_dir, "New_Scalar.pkl")

    # ----------------------------------
    # Check model file
    # ----------------------------------
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    # ----------------------------------
    # Check scaler file
    # ----------------------------------
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(
            f"Scaler file not found: {scaler_path}"
        )

    # ----------------------------------
    # Load model
    # ----------------------------------
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # ----------------------------------
    # Load scaler
    # ----------------------------------
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    return model, scaler


# ----------------------------------
# Load artifacts safely
# ----------------------------------
try:

    model, scaler = load_artifacts()

except FileNotFoundError as e:

    st.error("❌ Required model file is missing.")
    st.code(str(e))

    st.info(
        "Make sure New_RFmodel.pkl and New_Scalar.pkl "
        "are uploaded to the same GitHub folder as app.py."
    )

    st.stop()

except Exception as e:

    st.error("❌ Error loading model or scaler.")
    st.code(str(e))

    st.stop()


# ----------------------------------
# Feature inputs
# ----------------------------------
feature_inputs = {

    "fixed acidity": st.number_input(
        "Fixed Acidity",
        min_value=0.0,
        value=7.4
    ),

    "volatile acidity": st.number_input(
        "Volatile Acidity",
        min_value=0.0,
        value=0.7
    ),

    "citric acid": st.number_input(
        "Citric Acid",
        min_value=0.0,
        value=0.0
    ),

    "residual sugar": st.number_input(
        "Residual Sugar",
        min_value=0.0,
        value=1.9
    ),

    "chlorides": st.number_input(
        "Chlorides",
        min_value=0.0,
        value=0.076
    ),

    "free sulfur dioxide": st.number_input(
        "Free Sulfur Dioxide",
        min_value=0.0,
        value=11.0
    ),

    "total sulfur dioxide": st.number_input(
        "Total Sulfur Dioxide",
        min_value=0.0,
        value=34.0
    ),

    "density": st.number_input(
        "Density",
        min_value=0.0,
        value=0.9978
    ),

    "pH": st.number_input(
        "pH",
        min_value=0.0,
        value=3.51
    ),

    "sulphates": st.number_input(
        "Sulphates",
        min_value=0.0,
        value=0.56
    ),

    "alcohol": st.number_input(
        "Alcohol",
        min_value=0.0,
        value=9.4
    )
}


# ----------------------------------
# Maintain correct feature order
# ----------------------------------
input_values = list(feature_inputs.values())


# ----------------------------------
# Prediction
# ----------------------------------
if st.button("🍷 Predict Wine Quality"):

    try:

        # Convert inputs into NumPy array
        input_array = np.array(
            input_values,
            dtype=float
        ).reshape(1, -1)

        # ----------------------------------
        # Scale input
        # ----------------------------------
        scaled_input = scaler.transform(input_array)

        # ----------------------------------
        # Make prediction
        # ----------------------------------
        prediction = model.predict(scaled_input)

        # ----------------------------------
        # Display result
        # ----------------------------------
        st.success(
            f"🍷 Predicted Wine Quality: **{int(prediction[0])}**"
        )

    except Exception as e:

        st.error("❌ Prediction error:")
        st.code(str(e))
