import streamlit as st

# Inputs for custom values
fat = st.number_input("Total Fat (g)", value=0.0, step=0.1)
sugar = st.number_input("Sugar (g)", value=0.0, step=0.1)
protein = st.number_input("Protein (g)", value=0.0, step=0.1)

# Dynamic Calorie Calculation (Fat: 9 cal/g, Sugar/Protein: 4 cal/g)
estimated_calories = (fat * 9) + (sugar * 4) + (protein * 4)

st.write(f"*Estimated Calories:* {estimated_calories:.1f} kcal")
