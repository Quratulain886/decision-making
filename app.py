import streamlist as st
# 1. Main Title and Subtitle (Same Interface)
st.title("Calorie Predictor")
st.write("Estimate the calories in your Starbucks drink.")

# 2. Number Inputs with +/- buttons (Exact design as image)
total_fat = st.number_input(
    "Total Fat (g)", 
    min_value=0.0, 
    value=5.00, 
    step=0.5, 
    format="%.2f"
)

sugars = st.number_input(
    "Sugars (g)", 
    min_value=0.0, 
    value=20.00, 
    step=0.5, 
    format="%.2f"
)

protein = st.number_input(
    "Protein (g)", 
    min_value=0.0, 
    value=5.00, 
    step=0.5, 
    format="%.2f"
)

caffeine = st.number_input(
    "Caffeine (mg)", 
    min_value=0.0, 
    value=100.00, 
    step=5.0, 
    format="%.2f"
)

# 3. Dynamic Calculation Logic
# Fat = 9 kcal/g, Sugar = 4 kcal/g, Protein = 4 kcal/g
calculated_calories = (total_fat * 9) + (sugars * 4) + (protein * 4)

# 4. Predict Calories Button & Dynamic Result Display
if st.button("Predict Calories"):
    st.success(f"*Estimated Calories:* {calculated_calories:.2f} kcal")
else:
    # Buttons dabaane ke bina bhi live update niche show hota rahega
    st.info(f"*Estimated Calories:* {calculated_calories:.2f} kcal")
