import streamlit as st

st.title("Calorie Predictor")
st.write("Estimate the calories in your Starbucks drink.")

fat = st.number_input("Total Fat (g)", value=5.0)
sugars = st.number_input("Sugars (g)", value=20.0)
protein = st.number_input("Protein (g)", value=5.0)
caffeine = st.number_input("Caffeine (mg)", value=150.0)

# Formula/Model Prediction Logic
predicted_calories = (fat * 9) + (sugars * 4) + (protein * 4)

st.subheader(f"Estimated Calories: {predicted_calories:.2f} kcal")
