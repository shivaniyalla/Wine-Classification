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
    initial_sidebar_state="collapsed",
)

# ============================================================
# PREMIUM WINE THEME
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    * {
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 15% 20%,
                rgba(116, 20, 54, 0.30),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 75%,
                rgba(82, 12, 39, 0.28),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #090507 0%,
                #160a10 45%,
                #090507 100%
            );

        min-height: 100vh;
        color: white;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* ========================================================
       BACKGROUND GLOW
       ======================================================== */

    .wine-glow {
        position: fixed;
        width: 550px;
        height: 550px;

        background:
            radial-gradient(
                circle,
                rgba(126, 18, 58, 0.20) 0%,
                rgba(91, 9, 39, 0.10) 40%,
                transparent 72%
            );

        top: -180px;
        right: -150px;

        border-radius: 50%;
        filter: blur(10px);

        pointer-events: none;
        z-index: 0;
    }

    .wine-glow-bottom {
        position: fixed;
        width: 500px;
        height: 500px;

        background:
            radial-gradient(
                circle,
                rgba(137, 26, 67, 0.16) 0%,
                transparent 70%
            );

        bottom: -220px;
        left: -150px;

        border-radius: 50%;
        filter: blur(20px);

        pointer-events: none;
        z-index: 0;
    }

    /* ========================================================
       DECORATIVE WINE GLASS
       ======================================================== */

    .wine-scene {
        position: fixed;
        right: 4%;
        top: 10%;

        width: 360px;
        height: 620px;

        opacity: 0.14;

        pointer-events: none;
        z-index: 0;

        transform: rotate(-2deg);
    }

    .glass-bowl {
        position: absolute;

        left: 55px;
        top: 70px;

        width: 250px;
        height: 320px;

        border: 3px solid rgba(255,255,255,0.45);
        border-top: none;

        border-radius:
            0 0 125px 125px /
            0 0 170px 170px;

        background:
            linear-gradient(
                90deg,
                rgba(255,255,255,0.06),
                rgba(255,255,255,0.015),
                rgba(255,255,255,0.08)
            );

        backdrop-filter: blur(2px);
    }

    .glass-rim {
        position: absolute;

        left: 55px;
        top: 62px;

        width: 250px;
        height: 35px;

        border:
            3px solid rgba(255,255,255,0.42);

        border-radius: 50%;
    }

    .glass-stem {
        position: absolute;

        left: 176px;
        top: 388px;

        width: 5px;
        height: 145px;

        background:
            linear-gradient(
                to right,
                rgba(255,255,255,0.10),
                rgba(255,255,255,0.50),
                rgba(255,255,255,0.10)
            );
    }

    .glass-base {
        position: absolute;

        left: 105px;
        top: 525px;

        width: 145px;
        height: 12px;

        border:
            2px solid rgba(255,255,255,0.35);

        border-radius: 50%;
    }

    .wine-liquid {
        position: absolute;

        left: 68px;
        top: 245px;

        width: 224px;
        height: 130px;

        background:
            linear-gradient(
                180deg,
                #7b123c,
                #4a0925
            );

        border-radius:
            0 0 110px 110px /
            0 0 75px 75px;

        box-shadow:
            inset 0 15px 25px rgba(255,255,255,0.05),
            0 15px 50px rgba(102, 10, 45, 0.45);

        animation:
            wineRise 4s ease-in-out infinite;
    }

    .wine-surface {
        position: absolute;

        left: 68px;
        top: 237px;

        width: 224px;
        height: 30px;

        border-radius: 50%;

        background:
            radial-gradient(
                ellipse,
                #8f1a49,
                #5a0a2d 70%
            );

        animation:
            wineWave 3s ease-in-out infinite;
    }

    .wine-stream {
        position: absolute;

        left: 173px;
        top: -5px;

        width: 15px;
        height: 255px;

        background:
            linear-gradient(
                90deg,
                #5d0a2e,
                #8e1748,
                #5d0a2e
            );

        border-radius: 20px;

        transform-origin: bottom;

        animation:
            pourWine 2.2s ease-in-out infinite;
    }

    .wine-bottle {
        position: absolute;

        left: 120px;
        top: -45px;

        width: 105px;
        height: 150px;

        border-radius:
            20px 20px 30px 30px;

        background:
            linear-gradient(
                90deg,
                rgba(255,255,255,0.04),
                rgba(72,5,28,0.85),
                rgba(255,255,255,0.05)
            );

        transform: rotate(22deg);
    }

    .wine-bottle-neck {
        position: absolute;

        left: 32px;
        top: -60px;

        width: 40px;
        height: 75px;

        background:
            linear-gradient(
                90deg,
                #3c071d,
                #671031,
                #360619
            );

        border-radius:
            12px 12px 5px 5px;
    }

    @keyframes pourWine {

        0%, 100% {
            transform: scaleY(0.80);
            opacity: 0.65;
        }

        50% {
            transform: scaleY(1.05);
            opacity: 1;
        }
    }

    @keyframes wineRise {

        0%, 100% {
            height: 125px;
        }

        50% {
            height: 135px;
        }
    }

    @keyframes wineWave {

        0%, 100% {
            transform: scaleX(1);
        }

        50% {
            transform: scaleX(0.97);
        }
    }

    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .main-container {
        position: relative;

        z-index: 2;

        max-width: 1100px;

        margin: 0 auto;

        padding:
            42px
            24px
            60px
            24px;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        text-align: center;

        margin-bottom: 38px;
    }

    .hero-badge {
        display: inline-block;

        padding:
            8px 17px;

        border:
            1px solid rgba(255,255,255,0.14);

        border-radius: 50px;

        background:
            rgba(255,255,255,0.06);

        backdrop-filter:
            blur(15px);

        color:
            #e7b6c8;

        font-size:
            13px;

        font-weight:
            600;

        letter-spacing:
            1.4px;

        text-transform:
            uppercase;

        margin-bottom:
            18px;
    }

    .hero-title {
        font-family:
            'Playfair Display',
            serif;

        font-size:
            clamp(42px, 6vw, 70px);

        line-height:
            1.05;

        margin:
            0;

        background:
            linear-gradient(
                120deg,
                #ffffff,
                #e9bacd,
                #a83b69
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;
    }

    .hero-subtitle {
        margin:
            18px auto 0 auto;

        color:
            rgba(255,255,255,0.65);

        font-size:
            16px;

        max-width:
            650px;

        line-height:
            1.7;
    }

    /* ========================================================
       STREAMLIT CARD
       ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.095),
                rgba(255,255,255,0.035)
            ) !important;

        border:
            1px solid rgba(255,255,255,0.13) !important;

        border-radius:
            28px !important;

        backdrop-filter:
            blur(24px) saturate(120%);

        -webkit-backdrop-filter:
            blur(24px) saturate(120%);

        box-shadow:
            0 30px 80px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.08);

        padding:
            8px !important;

        margin-bottom:
            22px;
    }

    .section-title {
        font-family:
            'Playfair Display',
            serif;

        font-size:
            25px;

        color:
            white;

        margin:
            5px 0 5px 0;
    }

    .section-description {
        color:
            rgba(255,255,255,0.52);

        font-size:
            14px;

        margin-bottom:
            20px;

        line-height:
            1.6;
    }

    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-testid="stNumberInput"] label {

        color:
            rgba(255,255,255,0.75) !important;

        font-size:
            13px !important;

        font-weight:
            500 !important;
    }

    div[data-testid="stNumberInput"] input {

        background:
            rgba(255,255,255,0.065) !important;

        color:
            white !important;

        border:
            1px solid rgba(255,255,255,0.12) !important;

        border-radius:
            12px !important;

        height:
            45px !important;
    }

    div[data-testid="stNumberInput"] input:focus {

        border-color:
            rgba(176,57,105,0.8) !important;

        box-shadow:
            0 0 0 2px rgba(176,57,105,0.15) !important;
    }

    /* ========================================================
       BUTTON
       ======================================================== */

    div.stButton > button {

        width:
            100%;

        min-height:
            54px;

        border:
            none;

        border-radius:
            15px;

        background:
            linear-gradient(
                135deg,
                #8d1746,
                #b4386a
            );

        color:
            white;

        font-size:
            15px;

        font-weight:
            700;

        letter-spacing:
            0.3px;

        box-shadow:
            0 12px 30px rgba(128,18,63,0.30);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div.stButton > button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 18px 40px rgba(128,18,63,0.45);

        color:
            white;
    }

    /* ========================================================
       RESULT CARD
       ======================================================== */

    .result-card {

        margin-top:
            8px;

        padding:
            30px;

        border-radius:
            22px;

        background:
            linear-gradient(
                135deg,
                rgba(137,25,70,0.24),
                rgba(255,255,255,0.045)
            );

        border:
            1px solid rgba(190,67,117,0.28);

        text-align:
            center;

        backdrop-filter:
            blur(20px);

        box-shadow:
            0 20px 60px rgba(80,5,35,0.25);
    }

    .result-label {

        color:
            rgba(255,255,255,0.55);

        font-size:
            12px;

        text-transform:
            uppercase;

        letter-spacing:
            2px;

        margin-bottom:
            8px;
    }

    .result-value {

        font-family:
            'Playfair Display',
            serif;

        font-size:
            52px;

        font-weight:
            700;

        color:
            #f0c6d7;

        line-height:
            1;
    }

    .result-icon {

        font-size:
            35px;

        margin-bottom:
            10px;
    }

    /* ========================================================
       INFO CARDS
       ======================================================== */

    .info-card {

        padding:
            22px 16px;

        border-radius:
            20px;

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.08);

        text-align:
            center;

        min-height:
            145px;
    }

    .info-icon {

        font-size:
            25px;

        margin-bottom:
            8px;
    }

    .info-title {

        font-weight:
            700;

        color:
            white;

        font-size:
            14px;
    }

    .info-text {

        color:
            rgba(255,255,255,0.45);

        font-size:
            12px;

        margin-top:
            6px;

        line-height:
            1.5;
    }

    .footer {

        text-align:
            center;

        color:
            rgba(255,255,255,0.32);

        font-size:
            12px;

        margin-top:
            18px;

        letter-spacing:
            0.3px;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .main-container {

            padding:
                28px 12px 45px 12px;
        }

        .wine-scene {

            right:
                -120px;

            top:
                10%;

            opacity:
                0.07;

            transform:
                scale(0.75);
        }

        [data-testid="stVerticalBlockBorderWrapper"] {

            border-radius:
                22px !important;
        }

        .hero-title {

            font-size:
                42px;
        }
    }

    </style>

    <div class="wine-glow"></div>
    <div class="wine-glow-bottom"></div>

    <div class="wine-scene">

        <div class="wine-bottle">
            <div class="wine-bottle-neck"></div>
        </div>

        <div class="wine-stream"></div>

        <div class="glass-rim"></div>

        <div class="glass-bowl"></div>

        <div class="wine-surface"></div>

        <div class="wine-liquid"></div>

        <div class="glass-stem"></div>

        <div class="glass-base"></div>

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="main-container">

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

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# LOAD MODEL AND SCALER
# ============================================================

@st.cache_resource
def load_artifacts():

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model_candidates = [
        "New_RFmodel.pkl",
        "New_RFModel.pkl",
    ]

    # --------------------------------------------------------
    # SCALER
    # Supports both New_Scalar.pkl and New_scalar.pkl
    # --------------------------------------------------------

    scaler_candidates = [
        "New_Scalar.pkl",
        "New_scalar.pkl",
        "New_Scaler.pkl",
        "New_scaler.pkl",
    ]

    model_path = next(
        (
            os.path.join(base_dir, filename)
            for filename in model_candidates
            if os.path.isfile(
                os.path.join(base_dir, filename)
            )
        ),
        None,
    )

    scaler_path = next(
        (
            os.path.join(base_dir, filename)
            for filename in scaler_candidates
            if os.path.isfile(
                os.path.join(base_dir, filename)
            )
        ),
        None,
    )

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if model_path is None:

        raise FileNotFoundError(
            "Model file not found.\n\n"
            f"Expected one of:\n"
            f"{', '.join(model_candidates)}\n\n"
            f"App folder:\n{base_dir}\n\n"
            f"Files found:\n{os.listdir(base_dir)}"
        )

    # --------------------------------------------------------
    # CHECK SCALER
    # --------------------------------------------------------

    if scaler_path is None:

        raise FileNotFoundError(
            "Scaler file not found.\n\n"
            f"Expected one of:\n"
            f"{', '.join(scaler_candidates)}\n\n"
            f"App folder:\n{base_dir}\n\n"
            f"Files found:\n{os.listdir(base_dir)}"
        )

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    with open(
        model_path,
        "rb"
    ) as file:

        model = pickle.load(file)

    # --------------------------------------------------------
    # LOAD SCALER
    # --------------------------------------------------------

    with open(
        scaler_path,
        "rb"
    ) as file:

        scaler = pickle.load(file)

    return model, scaler


# ============================================================
# LOAD ARTIFACTS SAFELY
# ============================================================

try:

    model, scaler = load_artifacts()

except FileNotFoundError as error:

    st.error(
        "❌ Required model/scaler file is missing."
    )

    st.code(
        str(error)
    )

    st.info(
        "Make sure app.py, the model .pkl file, "
        "and the scaler .pkl file are in the "
        "same GitHub folder."
    )

    st.stop()

except Exception as error:

    st.error(
        "❌ Unable to load the machine-learning model."
    )

    st.code(
        str(error)
    )

    st.stop()


# ============================================================
# WINE CHARACTERISTICS
# ============================================================

with st.container(border=True):

    st.markdown(
        """
        <div class="section-title">
            🍇 Wine Characteristics
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Enter the chemical properties of the wine below.
            The AI model will analyze these values and predict
            the wine quality.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    # --------------------------------------------------------
    # LEFT COLUMN
    # --------------------------------------------------------

    with col1:

        fixed_acidity = st.number_input(
            "Fixed Acidity",
            min_value=0.0,
            value=7.4,
            step=0.1,
        )

        volatile_acidity = st.number_input(
            "Volatile Acidity",
            min_value=0.0,
            value=0.70,
            step=0.01,
        )

        citric_acid = st.number_input(
            "Citric Acid",
            min_value=0.0,
            value=0.00,
            step=0.01,
        )

        residual_sugar = st.number_input(
            "Residual Sugar",
            min_value=0.0,
            value=1.9,
            step=0.1,
        )

        chlorides = st.number_input(
            "Chlorides",
            min_value=0.0,
            value=0.076,
            step=0.001,
            format="%.3f",
        )

        free_sulfur_dioxide = st.number_input(
            "Free Sulfur Dioxide",
            min_value=0.0,
            value=11.0,
            step=1.0,
        )

    # --------------------------------------------------------
    # RIGHT COLUMN
    # --------------------------------------------------------

    with col2:

        total_sulfur_dioxide = st.number_input(
            "Total Sulfur Dioxide",
            min_value=0.0,
            value=34.0,
            step=1.0,
        )

        density = st.number_input(
            "Density",
            min_value=0.0,
            value=0.9978,
            step=0.0001,
            format="%.4f",
        )

        pH = st.number_input(
            "pH",
            min_value=0.0,
            value=3.51,
            step=0.01,
        )

        sulphates = st.number_input(
            "Sulphates",
            min_value=0.0,
            value=0.56,
            step=0.01,
        )

        alcohol = st.number_input(
            "Alcohol",
            min_value=0.0,
            value=9.4,
            step=0.1,
        )


# ============================================================
# PREDICTION SECTION
# ============================================================

with st.container(border=True):

    st.markdown(
        """
        <div class="section-title">
            🔮 Analyze Wine
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Ready to discover the predicted quality?
            Click the button below.
        </div>
        """,
        unsafe_allow_html=True,
    )

    predict_button = st.button(
        "🍷 Predict Wine Quality",
        use_container_width=True,
    )

    # ========================================================
    # PREDICTION
    # ========================================================

    if predict_button:

        try:

            # IMPORTANT:
            # Keep EXACTLY the same order used
            # during model training.

            input_values = [

                fixed_acidity,

                volatile_acidity,

                citric_acid,

                residual_sugar,

                chlorides,

                free_sulfur_dioxide,

                total_sulfur_dioxide,

                density,

                pH,

                sulphates,

                alcohol,
            ]

            # ------------------------------------------------
            # NUMPY ARRAY
            # ------------------------------------------------

            input_array = np.array(
                input_values,
                dtype=float
            ).reshape(
                1,
                -1
            )

            # ------------------------------------------------
            # SCALE
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
            # RESULT CARD
            # ------------------------------------------------

            st.markdown(
                f"""
                <div class="result-card">

                    <div class="result-icon">
                        🍷
                    </div>

                    <div class="result-label">
                        Predicted Wine Quality
                    </div>

                    <div class="result-value">
                        {predicted_quality}
                    </div>

                    <div style="
                        margin-top:12px;
                        color:rgba(255,255,255,0.55);
                        font-size:13px;
                    ">
                        AI-generated prediction based on
                        chemical properties
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception as error:

            st.error(
                "❌ Prediction error"
            )

            st.code(
                str(error)
            )


# ============================================================
# INFO CARDS
# ============================================================

st.markdown(
    """
    <div class="main-container"
         style="padding-top:10px;">
    """,
    unsafe_allow_html=True,
)

info_col1, info_col2, info_col3 = st.columns(
    3,
    gap="medium"
)

# ------------------------------------------------------------
# CARD 1
# ------------------------------------------------------------

with info_col1:

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# CARD 2
# ------------------------------------------------------------

with info_col2:

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# CARD 3
# ------------------------------------------------------------

with info_col3:

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
        <div class="footer">
            🍷 Wine Quality AI · Powered by Machine Learning
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
