import streamlit as st
import pandas as pd
import requests
import json

# Define the URL of your FastAPI backend
API_URL = "http://146.190.78.32:8080"  # Replace with your actual Render URL

def predict_heart_disease():
    # Collect user inputs
    inputs = {}

    st.sidebar.header('User Input Features')

    # Numerical inputs (sliders)
    inputs['HeightInMeters'] = st.sidebar.slider('Height (meters)', 0.91, 2.41, 1.75)
    inputs['WeightInKilograms'] = st.sidebar.slider('Weight (kg)', 30.39, 263.08, 70.5)
    inputs['BMI'] = st.sidebar.slider('BMI', 12.11, 97.65, 23.0)
    inputs['PhysicalHealthDays'] = st.sidebar.slider('Physical Health Days', 0, 30, 2)
    inputs['MentalHealthDays'] = st.sidebar.slider('Mental Health Days', 0, 30, 1)
    inputs['SleepHours'] = st.sidebar.slider('Sleep Hours', 1, 24, 7.5)

    # Categorical inputs (dropdowns)
    inputs['AgeCategory'] = st.sidebar.selectbox('Age Category', [
        'Age 80 or older', 'Age 75 to 79', 'Age 70 to 74', 
        'Age 65 to 69', 'Age 60 to 64', 'Age 55 to 59', 
        'Age 50 to 54', 'Age 45 to 49', 'Age 40 to 44',
        'Age 35 to 39', 'Age 30 to 34', 'Age 25 to 29',
        'Age 18 to 24'
    ], index=9)  # Default to 'Age 30 to 34'
    
    inputs['Sex'] = st.sidebar.selectbox('Sex', ['Male', 'Female'])
    inputs['RaceEthnicityCategory'] = st.sidebar.selectbox('Race/Ethnicity', [
        'White only, Non-Hispanic', 'Hispanic', 
        'Black only, Non-Hispanic', 'Other race only, Non-Hispanic'
    ])
    inputs['GeneralHealth'] = st.sidebar.selectbox('General Health', ['Good', 'Very good', 'Fair', 'Excellent', 'Poor'], index=1)
    
    inputs['LastCheckupTime'] = st.sidebar.selectbox('Last Checkup Time', [
        'Within past year (anytime less than 12 months ago)', 
        'Within past 2 years (1 year but less than 2 years ago)',
        'Within past 5 years (2 years but less than 5 years ago)',
        '5 or more years ago'
    ])
    inputs['BMI_category'] = st.sidebar.selectbox('BMI_category', ['Underweight', 'Normal', 'Overweight', 'Obese'], index=1)
    inputs['SmokerStatus'] = st.sidebar.selectbox('Smoker Status', [
        'Never smoked',
        'Former smoker',
        'Current smoker - now smokes every day',
        'Current smoker - now smokes some days'
    ])
    
    inputs['ECigaretteUsage'] = st.sidebar.selectbox('E-Cigarette Usage', [
        'Never used e-cigarettes in my entire life',
        'Not at all (right now)',
        'Use them some days',
        'Use them every day'
    ])
    
    # Boolean inputs (radio buttons)
    boolean_vars = ['PhysicalActivities', 'AlcoholDrinkers', 
                    'HadAsthma', 'HadSkinCancer', 
                    'HadCOPD', 'HadDepressiveDisorder',
                    'HadKidneyDisease', 'HadArthritis',
                    'HadDiabetes', 'DeafOrHardOfHearing',
                    'BlindOrVisionDifficulty', 'DifficultyConcentrating',
                    'DifficultyWalking', 'DifficultyDressingBathing',
                    'DifficultyErrands', 'ChestScan',
                    'HIVTesting', 'FluVaxLast12',
                    'PneumoVaxEver', 'HighRiskLastYear',
                    'CovidPos']

    for var in boolean_vars:
        inputs[var] = st.sidebar.radio(var, ['True', 'False']) == 'True'

    # Predict button
    if st.sidebar.button('Predict Heart Disease'):
        # Prepare the input data for prediction
        input_data = json.dumps(inputs)
        
        # Make prediction request to FastAPI backend
        try:
            response = requests.post(f"{API_URL}/predict", json=inputs)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            prediction_message = response.json()['Prediction']
            st.subheader('Prediction')
            st.write(prediction_message)
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
        except json.JSONDecodeError:
            st.error("Error decoding the API response")
        except KeyError:
            st.error("Unexpected response format from the API")

# Run the app
if __name__ == '__main__':
    st.title('Heart Disease Prediction App')
    predict_heart_disease()
