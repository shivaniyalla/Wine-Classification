import streamlit as st
import numpy as np
import pickle
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Wine Quality AI",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(120, 35, 55, 0.18), transparent 30%),
        radial-gradient(circle at 90% 80%, rgba(90, 20, 40, 0.15), transparent 30%),
        #0d080b;
    color: #f5eeee;
}

/* Main content */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hero */
.hero {
    text-align: center;
    padding: 45px 20px 35px 20px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 30px;
    background: rgba(130, 35, 60, 0.18);
    border: 1px solid rgba(180, 70, 95, 0.35);
    color: #e9a7b8;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 58px;
    line-height: 1.05;
    margin: 0;
    font-weight: 800;
    letter-spacing: -2px;
}

.hero-subtitle {
    max-width: 650px;
    margin: 20px auto 0 auto;
    color: #b9aeb2;
    font-size: 17px;
    line-height: 1.6;
}

/* Section headings */
.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #a99ca1;
    margin-bottom: 20px;
}

/* Streamlit cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(35, 17, 23, 0.65);
    border: 1px solid rgba(170, 70, 95, 0.22);
    border-radius: 18px;
    padding: 10px;
}

/* Inputs */
.stNumberInput label {
    color: #d8cdd1 !important;
    font-weight: 600;
}

.stNumberInput input {
    background: #171014 !important;
    color: #ffffff !important;
    border: 1px solid #39232b !important;
    border-radius: 10px !important;
}

/* Predict button */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg, #741f39, #a73455);
    color: white;
    font-size: 17px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(150, 40, 75, 0.3);
}

/* Result */
.result-card {
    margin-top: 25px;
    padding: 30px;
    text-align: center;
    border-radius: 20px;
    background: linear-gradient(
        145deg,
        rgba(94, 25, 44, 0.55),
        rgba(35, 14, 22, 0.75)
    );
    border: 1px solid rgba(190, 75, 105, 0.35);
}

.result-label {
    color: #bcaeb3;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-number {
    font-size: 65px;
    font-weight: 800;
    margin: 8px 0;
}

.result-message {
    color: #dfb2c0;
    font-size: 18px;
}

/* Mobile */
@media (max-width: 768px) {
    .hero-title {
        font-size: 42px;
    }

    .hero {
        padding-top: 25px;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================

st.write("")

st.caption("✦ AI POWERED WINE ANALYSIS")

st.markdown(
    "# 🍷 Wine Quality Prediction"
)

st.markdown(
    "Discover the predicted quality of your wine using "
    "machine learning and its chemical properties."
)

st.write("")

# ============================================================
# LOAD MODEL AND SCALER
# ============================================================

@st.cache_resource
def load_artifacts():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    model_candidates = [
        "New_RFmodel.pkl",
        "New_RFModel.pkl",
        "new_RFmodel.pkl",
        "new_RFModel.pkl"
    ]

    scaler_candidates = [
        "New_Scalar.pkl",
        "New_scalar.pkl",
        "New_Scaler.pkl",
        "New_scaler.pkl"
    ]

    model_path = None
    scaler_path = None

    for filename in model_candidates:
        path = os.path.join(base_dir, filename)

        if os.path.exists(path):
            model_path = path
            break

    for filename in scaler_candidates:
        path = os.path.join(base_dir, filename)

        if os.path.exists(path):
            scaler_path = path
            break

    if model_path is None:
        raise FileNotFoundError(
            "Model file not found. Expected one of: "
            + ", ".join(model_candidates)
        )

    if scaler_path is None:
        raise FileNotFoundError(
            "Scaler file not found. Expected one of: "
            + ", ".join(scaler_candidates)
        )

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    with open(scaler_path, "rb") as file:
        scaler = pickle.load(file)

    return model, scaler


# ============================================================
# LOAD ARTIFACTS
# ============================================================

try:
    model, scaler = load_artifacts()

except Exception as e:

    st.error("⚠️ Unable to load model/scaler.")

    st.code(str(e))

    st.info(
        "Make sure New_RFmodel.pkl and New_Scalar.pkl "
        "are present in the same folder as app.py."
    )

    st.stop()


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🧪 Wine Chemical Properties</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Enter the chemical characteristics of the wine.'
    '</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Row 1
# ------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):

        fixed_acidity = st.number_input(
            "Fixed Acidity",
            min_value=0.0,
            value=7.4,
            step=0.1
        )

        volatile_acidity = st.number_input(
            "Volatile Acidity",
            min_value=0.0,
            value=0.70,
            step=0.01
        )

        citric_acid = st.number_input(
            "Citric Acid",
            min_value=0.0,
            value=0.00,
            step=0.01
        )


with col2:
    with st.container(border=True):

        residual_sugar = st.number_input(
            "Residual Sugar",
            min_value=0.0,
            value=1.9,
            step=0.1
        )

        chlorides = st.number_input(
            "Chlorides",
            min_value=0.0,
            value=0.076,
            step=0.001,
            format="%.3f"
        )

        free_sulfur_dioxide = st.number_input(
            "Free Sulfur Dioxide",
            min_value=0.0,
            value=11.0,
            step=1.0
        )


with col3:
    with st.container(border=True):

        total_sulfur_dioxide = st.number_input(
            "Total Sulfur Dioxide",
            min_value=0.0,
            value=34.0,
            step=1.0
        )

        density = st.number_input(
            "Density",
            min_value=0.0,
            value=0.9978,
            step=0.0001,
            format="%.4f"
        )

        ph = st.number_input(
            "pH",
            min_value=0.0,
            value=3.51,
            step=0.01
        )


# ------------------------------------------------------------
# Row 2
# ------------------------------------------------------------

col4, col5, col6 = st.columns(3)

with col4:
    with st.container(border=True):

        sulphates = st.number_input(
            "Sulphates",
            min_value=0.0,
            value=0.56,
            step=0.01
        )


with col5:
    with st.container(border=True):

        alcohol = st.number_input(
            "Alcohol",
            min_value=0.0,
            value=9.4,
            step=0.1
        )


with col6:
    with st.container(border=True):

        st.markdown("### 🍷")
        st.markdown("**11 Features**")
        st.caption("Chemical properties used by the model.")


# ============================================================
# PREDICTION
# ============================================================

st.write("")
st.write("")

predict = st.button("🍷 Predict Wine Quality")


if predict:

    input_values = [
        fixed_acidity,
        volatile_acidity,
        citric_acid,
        residual_sugar,
        chlorides,
        free_sulfur_dioxide,
        total_sulfur_dioxide,
        density,
        ph,
        sulphates,
        alcohol
    ]

    try:

        input_array = np.array(
            input_values,
            dtype=float
        ).reshape(1, -1)

        scaled_input = scaler.transform(input_array)

        prediction = model.predict(scaled_input)

        predicted_quality = int(prediction[0])

        # Quality message
        if predicted_quality >= 8:
            message = "Excellent quality wine 🍷"
        elif predicted_quality >= 7:
            message = "Very good quality wine ✨"
        elif predicted_quality >= 6:
            message = "Good quality wine 👍"
        elif predicted_quality >= 5:
            message = "Average quality wine"
        else:
            message = "Below-average quality wine"

        # Result card
        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    Predicted Wine Quality
                </div>

                <div class="result-number">
                    {predicted_quality}
                </div>

                <div class="result-message">
                    {message}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error("⚠️ Prediction failed.")

        st.code(str(e))


# ============================================================
# INFORMATION CARDS
# ============================================================

st.write("")
st.write("")
st.write("")

st.markdown(
    '<div class="section-title">✨ About the Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'How this wine quality prediction system works.'
    '</div>',
    unsafe_allow_html=True
)

info1, info2, info3 = st.columns(3)

with info1:

    with st.container(border=True):

        st.markdown(
            "<div style='font-size:34px;'>🧪</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3>Chemical Analysis</h3>",
            unsafe_allow_html=True
        )

        st.caption(
            "11 wine characteristics are analyzed "
            "to estimate wine quality."
        )


with info2:

    with st.container(border=True):

        st.markdown(
            "<div style='font-size:34px;'>🤖</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3>Machine Learning</h3>",
            unsafe_allow_html=True
        )

        st.caption(
            "A Random Forest machine learning model "
            "predicts the wine quality score."
        )


with info3:

    with st.container(border=True):

        st.markdown(
            "<div style='font-size:34px;'>⚡</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3>Instant Results</h3>",
            unsafe_allow_html=True
        )

        st.caption(
            "Enter the values and get the predicted "
            "quality within seconds."
        )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.write("")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#786c71;
        font-size:13px;
        padding:30px 0 10px 0;
    ">
        🍷 Wine Quality AI &nbsp;·&nbsp;
        Powered by Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
