import streamlit as st
import pandas as pd
import joblib

model = joblib.load("svm_pipeline.pkl")

st.markdown(
    """
    <style>

    /* Banner styling */
    .banner {
        position: relative;
        width: 100%;
        height: 300px;
        background-image: url('https://images.pexels.com/photos/1128678/pexels-photo-1128678.jpeg');
        background-size: cover;
        background-position: center;
        border-radius: 10px;
        margin-bottom: 30px;
    }

    /* Dark overlay */
    .banner::before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.45);
        border-radius: 10px;
    }

    /* Banner text content */
    .banner-content {
        position: relative;
        z-index: 2;
        text-align: center;
        color: white;
        padding-top: 60px;
    }

    .company-name {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .title {
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .subtitle {
        font-size: 17px;
        width: 70%;
        margin: auto;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Banner content
st.markdown(
    """
    <div class="banner">
        <div class="banner-content">
            <div class="company-name">COMP Healthcare</div>
            <div class="title">Obesity Prediction System</div>
            <div class="subtitle">
                Welcome to COMP's AI-powered prediction tool.  
                Fill in your details below to check your obesity level and  
                receive instant personalized insights.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.write("Fill in your details below to predict your obesity level:")

# Collect raw user inputs (no mapping needed now!)
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.slider("Age", 10, 80, 25)
height = st.number_input("Height (meters)", 1.0, 2.5, 1.7)
weight = st.number_input("Weight (kg)", 30.0, 200.0, 65.0,step = 0.05)
family_history = st.selectbox("Family History of Overweight", ["Yes", "No"])
favc = st.selectbox("Frequent Consumption of High-Calorie Food", ["Yes", "No"])
fcvc = st.slider("Vegetable Consumption (1=Low, 3=High)", 1, 3, 2)
ncp = st.slider("Number of Main Meals", 1, 5, 3)
caec = st.selectbox("Eating Between Meals", ["No", "Sometimes", "Frequently", "Always"])
smoke = st.selectbox("Do You Smoke?", ["Yes", "No"])
ch2o = st.slider("Daily Water Intake (Liters)", 1.0, 5.0, 2.0)
scc = st.selectbox("Calories Monitoring", ["Yes", "No"])
faf = st.slider("Physical Activity Frequency (hrs/week)", 0.0, 10.0, 3.0)
tue_input = st.slider("Technology Usage (hrs/day)", 0.0, 10.0, 2.0)
tue = (tue_input / 10) * 2  # Scale to dataset range
calc = st.selectbox("Alcohol Consumption", ["No", "Sometimes", "Frequently", "Always"])
mtrans = st.selectbox("Main Transport Mode", ["Walking", "Bike", "Motorbike", "Public_Transportation", "Automobile"])

# Prepare raw DataFrame for prediction
user_data = pd.DataFrame({
    "Gender": [1 if gender == "Male" else 0],
    "Age": [age],
    "Height": [height],
    "Weight": [weight],
    "family_history_with_overweight": [1 if family_history == "Yes" else 0],
    "FAVC": [1 if favc == "Yes" else 0],
    "FCVC": [fcvc],
    "NCP": [ncp],
    "CAEC": [ {"No": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[caec] ],
    "SMOKE": [1 if smoke == "Yes" else 0],
    "CH2O": [ch2o],
    "SCC": [1 if scc == "Yes" else 0],
    "FAF": [faf],
    "TUE": [tue],
    "CALC": [ {"No": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[calc] ],
    "MTRANS": [mtrans]
})

if st.button("Predict"):
    prediction = model.predict(user_data)
    st.success(f"Predicted Obesity Level: **{prediction[0]}**")