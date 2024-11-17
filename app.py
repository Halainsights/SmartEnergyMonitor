import streamlit as st
import pandas as pd
import joblib

# Load the saved models
final_model_y1 = joblib.load('final_model_y1.pkl')
final_model_y2 = joblib.load('final_model_y2.pkl')

# Prediction functions
def predict_heating_load(features):
    return final_model_y1.predict(features)

def predict_cooling_load(features):
    return final_model_y2.predict(features)

# Configure Streamlit page
st.set_page_config(
    page_title="Building Energy Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for white labels and visible dropdown boxes
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 1rem !important; padding-bottom: 0rem !important;}
        .stApp {background: linear-gradient(135deg, #1e2433 0%, #16213e 100%);}
        .main-header {background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 2rem; margin-bottom: 3rem; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);}
        .main-header h1 {color: #ffffff; font-size: 2.5rem; font-weight: 600; text-align: center; margin-bottom: 0.5rem;}
        .main-header p {color: rgba(255, 255, 255, 0.8); text-align: center; font-size: 1.2rem; margin: 0;}
        .custom-card {background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);}
        .results-container {background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); margin-top: 2rem;}
        .results-text {text-align: center; margin: 0.5rem 0;}
        label {color: white !important;}  /* Make all labels white */
        .stSelectbox > div {height: auto !important; padding: 5px 8px !important; background-color: white !important; color: black !important; border-radius: 8px !important;}
        .stSelectbox > div > div {overflow: visible !important; padding: 0 10px !important; font-size: 16px !important; line-height: 1.6 !important;}
        .stNumberInput > div > div > input {color: black !important; background-color: white !important; border-radius: 8px !important; padding: 5px !important;}
        .stButton > button {width: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6) !important; color: white !important; border: none !important; padding: 0.75rem 2rem !important; border-radius: 8px !important; font-weight: 500 !important; transition: all 0.3s ease !important; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important; margin-top: 1rem !important;}
        .stButton > button:hover {transform: translateY(-2px); box-shadow: 0 6px 16px rgba(99, 102, 241, 0.3) !important;}
        /* Center logo container */
        .logo-container {
            display: flex;
            justify-content: center;
            margin: 2rem auto;
            padding: 1rem;
        }
        .logo-container img {
            margin: 0 auto;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='main-header'>
        <h1>Building Energy Efficiency Predictor</h1>
        <p>Optimize Your Building's Energy Performance</p>
    </div>
""", unsafe_allow_html=True)

# Input columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='custom-card'><h3 style='color: white;'>Building Parameters</h3>", unsafe_allow_html=True)
    X1 = st.number_input("Relative Compactness (X1)", 0.0, 1.0, 0.5, 0.01)
    X2 = st.number_input("Surface Area (X2)", 0.0, 400.0, 10.0)
    X3 = st.number_input("Wall Area (X3)", 0.0, 200.0, 10.0)
    X4 = st.number_input("Roof Area (X4)", 0.0, 100.0, 10.0)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='custom-card'><h3 style='color: white;'>Additional Features</h3>", unsafe_allow_html=True)
    X5 = st.number_input("Overall Height (X5)", 0.0, 50.0, 3.0)
    X6 = st.selectbox("Orientation (X6)", [1, 2, 3, 4])
    X7 = st.number_input("Glazing Area (X7)", 0.0, 1.0, 0.25, 0.01)
    X8 = st.selectbox("Glazing Area Distribution (X8)", [0, 1, 2, 3, 4, 5])
    st.markdown("</div>", unsafe_allow_html=True)

# Predict button
predict_button = st.button("Predict Energy Loads")

# Results container
results_container = st.container()

if predict_button:
    features = pd.DataFrame({'X1': [X1], 'X2': [X2], 'X3': [X3], 'X4': [X4], 'X5': [X5], 'X6': [X6], 'X7': [X7], 'X8': [X8]})
    heating_pred = predict_heating_load(features)
    cooling_pred = predict_cooling_load(features)
    
    heating_color = "red" if heating_pred[0] < 0 else "green"
    cooling_color = "red" if cooling_pred[0] < 0 else "green"

    with results_container:
        st.markdown(f"""
            <div class='results-container'>
                <div style='display: flex; justify-content: space-around;'>
                    <h3 style='color: {heating_color};'>Heating Load: {heating_pred[0]:.2f} kWh/m²</h3>
                    <h3 style='color: {cooling_color};'>Cooling Load: {cooling_pred[0]:.2f} kWh/m²</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)



# centered and larger logo
try:
    from PIL import Image
    logo = Image.open('logo_0bg.png')
    # Create three columns with the middle one for the logo - adjusted ratios for better centering
    left_spacer, logo_col, right_spacer = st.columns([2, 1, 2])
    with logo_col:
        # Center the image within its column
        st.markdown("""
            <div style="display: flex; justify-content: center; width: 100%;">
        """, unsafe_allow_html=True)
        st.image(logo, width=450)
        st.markdown("</div>", unsafe_allow_html=True)
except Exception as e:
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: rgba(255,255,255,0.6);">
            Logo not found. Please ensure 'logo_0bg.png' is in the same directory as the script.
        </div>
    """, unsafe_allow_html=True)