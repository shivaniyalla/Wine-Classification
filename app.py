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

/* ============================================================
   MAIN BACKGROUND
   ============================================================ */

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(128, 20, 55, 0.22), transparent 30%),
        radial-gradient(circle at 85% 75%, rgba(90, 15, 45, 0.20), transparent 30%),
        linear-gradient(135deg, #070309 0%, #10050b 45%, #070309 100%);
    color: #ffffff;
}


/* Remove Streamlit top spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}


/* ============================================================
   BACKGROUND GLOW
   ============================================================ */

.wine-glow {
    position: fixed;
    width: 450px;
    height: 450px;
    border-radius: 50%;
    background: rgba(128, 20, 55, 0.12);
    filter: blur(100px);
    top: 5%;
    left: -180px;
    pointer-events: none;
    z-index: 0;
}

.wine-glow-bottom {
    position: fixed;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: rgba(90, 15, 45, 0.12);
    filter: blur(100px);
    bottom: -150px;
    right: -150px;
    pointer-events: none;
    z-index: 0;
}


/* ============================================================
   WINE GLASS DECORATION
   ============================================================ */

.wine-scene {
    position: fixed;
    right: 4%;
    top: 80px;
    width: 150px;
    height: 230px;
    opacity: 0.18;
    pointer-events: none;
    z-index: 0;
}

.wine-glass {
    position: relative;
    width: 100px;
    height: 150px;
    margin: auto;
}

.glass-bowl {
    position: absolute;
    top: 0;
    left: 10px;
    width: 80px;
    height: 110px;
    border: 2px solid rgba(255,255,255,0.4);
    border-top-left-radius: 45px;
    border-top-right-radius: 45px;
    border-bottom-left-radius: 35px;
    border-bottom-right-radius: 35px;
    overflow: hidden;
}

.wine-liquid {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60%;
    background: linear-gradient(
        to top,
        rgba(80, 0, 25, 0.9),
        rgba(150, 20, 60, 0.7)
    );
    border-radius: 0 0 30px 30px;
}

.wine-surface {
    position: absolute;
    top: 42px;
    left: 8px;
    width: 64px;
    height: 12px;
    background: rgba(150, 20, 60, 0.5);
    border-radius: 50%;
}

.glass-stem {
    position: absolute;
    top: 108px;
    left: 49px;
    width: 2px;
    height: 70px;
    background: rgba(255,255,255,0.4);
}

.glass-base {
    position: absolute;
    top: 175px;
    left: 20px;
    width: 60px;
    height: 4px;
    border-radius: 50%;
    background: rgba(255,255,255,0.4);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 35px 20px 45px 20px;
}

.hero-badge {
    display: inline-block;
    padding: 9px 18px;
    border-radius: 30px;
    border: 1px solid rgba(180, 50, 90, 0.45);
    background: rgba(100, 10, 40, 0.20);
    color: #e7a4bd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 20px;
}

.hero-title {
    margin: 0;
    font-size: clamp(45px, 7vw, 82px);
    line-height: 0.98;
    font-weight: 800;
    letter-spacing: -3px;

    background: linear-gradient(
        135deg,
        #ffffff 15%,
        #f0b3c9 55%,
        #a72d59 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 700px;
    margin: 25px auto 0 auto;
    color: rgba(255,255,255,0.68);
    font-size: 17px;
    line-height: 1.7;
}


/* ============================================================
   STREAMLIT CONTAINER CARDS
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(80, 12, 38, 0.45),
            rgba(25, 7, 15, 0.72)
        ) !important;

    border: 1px solid rgba(200, 70, 110, 0.28) !important;

    border-radius: 24px !important;

    box-shadow:
        0 20px 60px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.04) !important;

    padding: 10px !important;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #ffffff;
    margin-bottom: 5px;
}

.section-description {
    color: rgba(255,255,255,0.55);
    font-size: 14px;
    margin-bottom: 20px;
}


/* ============================================================
   INPUT LABELS
   ============================================================ */

label {
    color: rgba(255,255,255,0.82) !important;
    font-weight: 600 !important;
}


/* ============================================================
   NUMBER INPUT
   ============================================================ */

div[data-testid="stNumberInput"] input {
    background: rgba(0,0,0,0.28) !important;
    color: white !important;

    border: 1px solid rgba(255,255,255,0.12) !important;

    border-radius: 12px !important;
}

div[data-testid="stNumberInput"] input:focus {
    border: 1px solid rgba(190, 55, 100, 0.8) !important;

    box-shadow:
        0 0 0 2px rgba(150, 30, 70, 0.15) !important;
}


/* ============================================================
   PREDICT BUTTON
   ============================================================ */

.stButton > button {
    width: 100%;

    border: none !important;
    border-radius: 14px !important;

    padding: 15px 20px !important;

    background:
        linear-gradient(
            135deg,
            #9d174d,
            #6b1238
        ) !important;

    color: white !important;

    font-size: 16px !important;
    font-weight: 750 !important;

    box-shadow:
        0 10px 30px rgba(120, 15, 60, 0.35) !important;

    transition: all 0.25s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 15px 35px rgba(150, 20, 70, 0.45) !important;
}


/* ============================================================
   RESULT CARD
   ============================================================ */

.result-card {
    margin-top: 25px;

    padding: 30px;

    border-radius: 22px;

    text-align: center;

    background:
        radial-gradient(
            circle at top,
            rgba(160, 30, 75, 0.30),
            rgba(30, 5, 15, 0.75)
        );

    border: 1px solid rgba(210, 70, 120, 0.35);

    box-shadow:
        0 15px 50px rgba(0,0,0,0.30);
}

.result-label {
    color: rgba(255,255,255,0.55);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-score {
    font-size: 65px;
    font-weight: 800;

    margin: 8px 0;

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #e49bb5
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.result-message {
    color: rgba(255,255,255,0.72);
    font-size: 16px;
}


# ============================================================
# INFORMATION CARDS
# ============================================================

st.write("")
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):

        st.markdown(
            "<div style='font-size:32px;'>🧪</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='margin:5px 0;'>Chemical Analysis</h3>",
            unsafe_allow_html=True
        )

        st.caption("11 wine characteristics")


with col2:
    with st.container(border=True):

        st.markdown(
            "<div style='font-size:32px;'>🤖</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='margin:5px 0;'>Machine Learning</h3>",
            unsafe_allow_html=True
        )

        st.caption("Random Forest prediction")


with col3:
    with st.container(border=True):

        st.markdown(
            "<div style='font-size:32px;'>⚡</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='margin:5px 0;'>Instant Results</h3>",
            unsafe_allow_html=True
        )

        st.caption("Prediction in seconds")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    🍷 Wine Quality AI &nbsp;·&nbsp; Powered by Machine Learning
</div>
""", unsafe_allow_html=True)


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .wine-scene {
        display: none;
    }

    .hero {
        padding-top: 20px;
    }

    .hero-title {
        font-size: 48px;
        letter-spacing: -2px;
    }

    .hero-subtitle {
        font-size: 15px;
    }

    .info-card {
        margin-bottom: 15px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DECORATIVE BACKGROUND
# ============================================================

st.markdown("""
<div class="wine-glow"></div>
<div class="wine-glow-bottom"></div>

<div class="wine-scene">
    <div class="wine-glass">

        <div class="glass-bowl">
            <div class="wine-liquid"></div>
            <div class="wine-surface"></div>
        </div>

        <div class="glass-stem"></div>
        <div class="glass-base"></div>

    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        ✦ AI POWERED WINE ANALYSIS
    </div>

    <h1 class="hero-title">
        Wine Quality<br>Prediction
    </h1>

    <p class="hero-subtitle">
        Discover the predicted quality of your wine using
        machine learning and its chemical properties.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL AND SCALER
# ============================================================

@st.cache_resource
def load_artifacts():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Possible model filenames
    model_candidates = [
        "New_RFmodel.pkl",
        "New_RFModel.pkl",
        "new_RFmodel.pkl",
        "new_RFModel.pkl"
    ]

    # Possible scaler filenames
    scaler_candidates = [
        "New_Scalar.pkl",
        "New_scalar.pkl",
        "New_Scaler.pkl",
        "New_scaler.pkl"
    ]

    model_path = None
    scaler_path = None

    # Find model
    for filename in model_candidates:
        path = os.path.join(base_dir, filename)

        if os.path.isfile(path):
            model_path = path
            break

    # Find scaler
    for filename in scaler_candidates:
        path = os.path.join(base_dir, filename)

        if os.path.isfile(path):
            scaler_path = path
            break

    # Model not found
    if model_path is None:

        available_files = os.listdir(base_dir)

        raise FileNotFoundError(
            "Random Forest model file not found.\n\n"
            f"Expected one of: {model_candidates}\n\n"
            f"Files found: {available_files}"
        )

    # Scaler not found
    if scaler_path is None:

        available_files = os.listdir(base_dir)

        raise FileNotFoundError(
            "Scaler file not found.\n\n"
            f"Expected one of: {scaler_candidates}\n\n"
            f"Files found: {available_files}"
        )

    # Load model
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)

    # Load scaler
    with open(scaler_path, "rb") as scaler_file:
        scaler = pickle.load(scaler_file)

    return model, scaler


# ============================================================
# LOAD ARTIFACTS
# ============================================================

try:

    model, scaler = load_artifacts()

    artifacts_loaded = True

except Exception as e:

    artifacts_loaded = False

    st.error(
        f"⚠️ Unable to load model/scaler:\n\n{e}"
    )


# ============================================================
# WINE INPUT SECTION
# ============================================================

with st.container(border=True):

    st.markdown("""
    <div class="section-title">
        🍷 Wine Chemical Properties
    </div>

    <div class="section-description">
        Enter the chemical characteristics of the wine to predict
        its quality using our trained Random Forest model.
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # ROW 1
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        fixed_acidity = st.number_input(
            "Fixed Acidity",
            min_value=0.0,
            max_value=20.0,
            value=7.4,
            step=0.1
        )

    with col2:

        volatile_acidity = st.number_input(
            "Volatile Acidity",
            min_value=0.0,
            max_value=5.0,
            value=0.70,
            step=0.01
        )

    with col3:

        citric_acid = st.number_input(
            "Citric Acid",
            min_value=0.0,
            max_value=2.0,
            value=0.00,
            step=0.01
        )

    # --------------------------------------------------------
    # ROW 2
    # --------------------------------------------------------

    col4, col5, col6 = st.columns(3)

    with col4:

        residual_sugar = st.number_input(
            "Residual Sugar",
            min_value=0.0,
            max_value=30.0,
            value=1.9,
            step=0.1
        )

    with col5:

        chlorides = st.number_input(
            "Chlorides",
            min_value=0.0,
            max_value=1.0,
            value=0.076,
            step=0.001,
            format="%.3f"
        )

    with col6:

        free_sulfur_dioxide = st.number_input(
            "Free Sulfur Dioxide",
            min_value=0.0,
            max_value=100.0,
            value=11.0,
            step=1.0
        )

    # --------------------------------------------------------
    # ROW 3
    # --------------------------------------------------------

    col7, col8, col9 = st.columns(3)

    with col7:

        total_sulfur_dioxide = st.number_input(
            "Total Sulfur Dioxide",
            min_value=0.0,
            max_value=300.0,
            value=34.0,
            step=1.0
        )

    with col8:

        density = st.number_input(
            "Density",
            min_value=0.8,
            max_value=1.2,
            value=0.9978,
            step=0.0001,
            format="%.4f"
        )

    with col9:

        ph = st.number_input(
            "pH",
            min_value=0.0,
            max_value=14.0,
            value=3.51,
            step=0.01
        )

    # --------------------------------------------------------
    # ROW 4
    # --------------------------------------------------------

    col10, col11, empty = st.columns(3)

    with col10:

        sulphates = st.number_input(
            "Sulphates",
            min_value=0.0,
            max_value=5.0,
            value=0.56,
            step=0.01
        )

    with col11:

        alcohol = st.number_input(
            "Alcohol (%)",
            min_value=0.0,
            max_value=25.0,
            value=9.4,
            step=0.1
        )


# ============================================================
# PREDICTION SECTION
# ============================================================

st.write("")


with st.container(border=True):

    st.markdown("""
    <div class="section-title">
        🤖 AI Quality Prediction
    </div>

    <div class="section-description">
        Our Random Forest machine learning model analyzes the
        chemical properties and predicts the wine quality score.
    </div>
    """, unsafe_allow_html=True)

    predict_button = st.button(
        "🍷 Predict Wine Quality",
        use_container_width=True
    )

    if predict_button:

        if not artifacts_loaded:

            st.error(
                "Model and scaler could not be loaded. "
                "Please check your .pkl files."
            )

        else:

            try:

                # ------------------------------------------------
                # CREATE INPUT ARRAY
                # ------------------------------------------------

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

                input_array = np.array(
                    input_values,
                    dtype=float
                ).reshape(1, -1)

                # ------------------------------------------------
                # SCALE INPUT
                # ------------------------------------------------

                scaled_input = scaler.transform(
                    input_array
                )

                # ------------------------------------------------
                # PREDICT
                # ------------------------------------------------

                prediction = model.predict(
                    scaled_input
                )

                predicted_quality = int(
                    prediction[0]
                )

                # ------------------------------------------------
                # QUALITY MESSAGE
                # ------------------------------------------------

                if predicted_quality >= 8:

                    quality_message = (
                        "Excellent wine quality 🍷✨"
                    )

                elif predicted_quality >= 7:

                    quality_message = (
                        "Very good wine quality 🍷"
                    )

                elif predicted_quality >= 6:

                    quality_message = (
                        "Good wine quality 👍"
                    )

                elif predicted_quality >= 5:

                    quality_message = (
                        "Average wine quality"
                    )

                else:

                    quality_message = (
                        "Below-average wine quality"
                    )

                # ------------------------------------------------
                # RESULT CARD
                # ------------------------------------------------

                st.markdown(f"""
                <div class="result-card">

                    <div class="result-label">
                        Predicted Wine Quality
                    </div>

                    <div class="result-score">
                        {predicted_quality}
                    </div>

                    <div class="result-message">
                        {quality_message}
                    </div>

                </div>
                """, unsafe_allow_html=True)

            except Exception as e:

                st.error(
                    f"Prediction failed: {e}"
                )


# ============================================================
# INFORMATION CARDS
# ============================================================

st.write("")
st.write("")


col1, col2, col3 = st.columns(3)


# ============================================================
# CARD 1
# ============================================================

with col1:

    st.markdown("""
    <div class="info-card">

        <div class="info-icon">
            🧪
        </div>

        <div class="info-title">
            Chemical Analysis
        </div>

        <div class="info-text">
            11 wine characteristics
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CARD 2
# ============================================================

with col2:

    st.markdown("""
    <div class="info-card">

        <div class="info-icon">
            🤖
        </div>

        <div class="info-title">
            Machine Learning
        </div>

        <div class="info-text">
            Random Forest prediction
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CARD 3
# ============================================================

with col3:

    st.markdown("""
    <div class="info-card">

        <div class="info-icon">
            ⚡
        </div>

        <div class="info-title">
            Instant Results
        </div>

        <div class="info-text">
            Prediction in seconds
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    🍷 Wine Quality AI &nbsp;·&nbsp; Powered by Machine Learning
</div>
""", unsafe_allow_html=True)
