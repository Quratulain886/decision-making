import streamlit as st

# Light theme configuration
st.set_page_config(page_title="Calorie Predictor", layout="centered")

st.title("Calorie Predictor")
st.write("Estimate the calories in your Starbucks drink.")

# Input fields
total_fat = st.number_input("Total Fat (g)", value=5.00, step=1.0)
sugars = st.number_input("Sugars (g)", value=20.00, step=1.0)
protein = st.number_input("Protein (g)", value=5.00, step=1.0)
caffeine = st.number_input("Caffeine (mg)", value=100.00, step=1.0)

# Predict button
if st.button("Predict Calories"):
    # Aapka prediction logic yahan aayega
    estimated_calories = 145.00  
    st.write(f"Estimated Calories: {estimated_calories:.2f} kcal")
