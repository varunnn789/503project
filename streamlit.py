import streamlit as st
import pandas as pd
import requests
import json

# Define the URL of your FastAPI backend
API_URL = "https://fastapi-app-latest-nj93.onrender.com"  # Replace with your actual Render URL

def predict_heart_disease():
    # Collect user inputs
    inputs = {}

    st.sidebar.header('User Input Features')

    # Numerical inputs (sliders)
    inputs['HeightInMeters'] = st.sidebar.slider('Height (meters)', 0.91, 2.41, 1.7)
    inputs['WeightInKilograms'] = st.sidebar.slider('Weight (kg)', 30.39, 263.08, 84.46)
    inputs['BMI'] = st.sidebar.slider('BMI', 12.11, 97.65, 28.93)
    inputs['PhysicalHealthDays'] = st.sidebar.slider('Physical Health Days', 0, 30, 6)
    inputs['MentalHealthDays'] = st.sidebar.slider('Mental Health Days', 0, 30, 5)
    inputs['SleepHours'] = st.sidebar.slider('Sleep Hours', 1, 24, 7)

    # Categorical inputs (dropdowns)
    inputs['AgeCategory'] = st.sidebar.selectbox('Age Category', ['Age 80 or older', 'Age 75 to 79', 'Age 70 to 74', 'Age 65 to 69', 'Age 60 to 64', 'Age 55 to 59', 'Age 40 to 44'
                                                ,'Age 75 to 79', 'Age 70 to 74', 'Age 65 to 69', 'Age 60 to 64', 'Age 50 to 54', 'Age 45 to 49', 'Age 35 to 39', 'Age 25 to 29', 'Age 30 to 34', 'Age 18 to 24'])
    inputs['Sex'] = st.sidebar.selectbox('Sex', ['Male', 'Female'])
    inputs['RaceEthnicityCategory'] = st.sidebar.selectbox('Race/Ethnicity', ['White only, Non-Hispanic', 'Hispanic', 'Black only, Non-Hispanic', 'Other race only, Non-Hispanic', 'Other'])
    inputs['GeneralHealth'] = st.sidebar.selectbox('General Health', ['Good', 'Very good', 'Fair', 'Excellent', 'Poor'])
    inputs['LastCheckupTime'] = st.sidebar.selectbox('Last Checkup Time', ['Within past year', 'Within past 2 years', 'Within past 5 years', '5 or more years ago', 'Other'])
    inputs['SmokerStatus'] = st.sidebar.selectbox('Smoker Status', ['Never smoked', 'Former smoker', 'Current smoker - now smokes every day', 'Current smoker - now smokes some days'])
    inputs['ECigaretteUsage'] = st.sidebar.selectbox('E-Cigarette Usage', ['Never used e-cigarettes in my entire life', 'Not at all (right now)', 'Use them some days', 'Use them every day', 'Other'])
    inputs['ChestScan'] = st.sidebar.selectbox('Chest Scan', ['Yes', 'No', 'Other'])
    inputs['HIVTesting'] = st.sidebar.selectbox('HIV Testing', ['No', 'Yes', 'Other'])
    inputs['TetanusLast10Tdap'] = st.sidebar.selectbox('Tetanus Last 10 Years (Tdap)', ['No, did not receive any tetanus shot in the past 10 years', 'Yes, received tetanus shot but not sure what type', 'Yes, received Tdap', 'Other', 'Yes, received tetanus shot, but not Tdap'])

    # Boolean inputs (radio buttons)
    boolean_vars = ['PhysicalActivities', 'AlcoholDrinkers', 'HadAsthma', 'HadSkinCancer', 'HadCOPD', 
                    'HadDepressiveDisorder', 'HadKidneyDisease', 'HadArthritis', 'HadDiabetes', 
                    'DeafOrHardOfHearing', 'BlindOrVisionDifficulty', 'DifficultyConcentrating', 
                    'DifficultyWalking', 'DifficultyDressingBathing', 'DifficultyErrands', 'FluVaxLast12', 
                    'PneumoVaxEver', 'HighRiskLastYear', 'CovidPos']

    for var in boolean_vars:
        inputs[var] = st.sidebar.radio(var, ['True', 'False']) == 'True'

    # Predict button
    if st.sidebar.button('Predict Heart Disease'):
        # Prepare the input data for prediction
        input_data = json.dumps(inputs)
        
        # Make prediction request to FastAPI backend
        try:
            response = requests.post(API_URL, data=input_data, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                prediction = response.json()['prediction']
                
                # Display the prediction
                st.subheader('Prediction')
                if prediction == 1:
                    st.write('The model predicts that the person is likely to have heart disease.')
                else:
                    st.write('The model predicts that the person is not likely to have heart disease.')
            else:
                st.error(f"Error: Received status code {response.status_code} from API")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")

# Run the app
if __name__ == '__main__':
    st.title('Heart Disease Prediction App')
    predict_heart_disease()
