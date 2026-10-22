# %%
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Dataset
X = [
    [1, 40], [2, 50], [2, 60], [3, 65],
    [4, 70], [5, 80], [6, 85], [7, 90],
    [1, 30], [6, 95], [3, 75], [5, 85],
    [8, 95], [9, 90], [4, 60], [7, 80]
]

y = [0, 0, 0, 0, 1, 1, 1, 1,
     0, 1, 1, 1, 1, 1, 0, 1]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Create model
model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=4,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

# Predict new data: [study_hours, attendance]
print("Prediction:", model.predict([[5, 80]])[0])

# Save trained model
joblib.dump(model, "decision_tree_model.pkl")

print("Model trained and saved successfully!")

# %%
# ==========================================
# DECISION TREE MODEL - KAGGLE
# Complete Training Code
# ==========================================

import os
import glob
import warnings
import pandas as pd
import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

warnings.filterwarnings("ignore")

# 1. Find the dataset
csv_files = glob.glob("/kaggle/input/**/*.csv", recursive=True)

# Find Starbucks dataset
starbucks_files = [
    f for f in csv_files
    if os.path.basename(f).lower() == "starbucks.csv"
]

if starbucks_files:
    file_path = starbucks_files[0]
else:
    # Use an available CSV if Starbucks file is not found
    if not csv_files:
        raise FileNotFoundError(
            "No CSV dataset found. Add a dataset using "
            "Kaggle Notebook > Add Input."
        )

    print("starbucks.csv not found. Available CSV files:")
    for f in csv_files[:20]:
        print(f)

    raise FileNotFoundError(
        "Please add the correct Starbucks dataset in Kaggle Input."
    )

# 2. Load dataset
df = pd.read_csv(file_path)

# 3. Clean dataset
df.columns = df.columns.str.strip()
df = df.drop_duplicates()
df = df.dropna(how="all")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# 4. Choose target column
# Change this if you want to predict another column
target_column = "Beverage_category"

if target_column not in df.columns:
    raise ValueError(
        f"Target column '{target_column}' not found. "
        f"Available columns: {df.columns.tolist()}"
    )

# 5. Prepare features and target
df = df.dropna(subset=[target_column])

X = df.drop(columns=[target_column])
y = df[target_column]

# Remove columns with no useful values
X = X.dropna(axis=1, how="all")

# Remove ID-like columns when present
id_columns = [
    c for c in X.columns
    if c.lower() in ["id", "unnamed: 0"]
]
X = X.drop(columns=id_columns, errors="ignore")

# Convert categorical columns into numeric columns
X = pd.get_dummies(X, dummy_na=True)
X = X.replace([float("inf"), float("-inf")], float("nan"))
X = X.fillna(0)

# Check data before training
if len(X) < 2:
    raise ValueError("Dataset must contain at least two rows.")

if y.nunique() < 2:
    raise ValueError("Target must contain at least two classes.")

# 6. Split dataset
test_count = max(1, int(round(len(df) * 0.2)))
test_count = min(test_count, len(df) - 1)

# Stratify only when each class has enough samples
stratify_y = (
    y if y.value_counts().min() >= 2
    and test_count >= y.nunique()
    and len(df) - test_count >= y.nunique()
    else None
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_count,
    random_state=42,
    stratify=stratify_y
)

# 7. Create Decision Tree model
model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)

# 8. Train model
model.fit(X_train, y_train)

print("\nModel trained successfully!")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# 9. Evaluate model
y_pred = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# 10. Save trained model
model_data = {
    "model": model,
    "feature_columns": X.columns.tolist(),
    "target_column": target_column
}

joblib.dump(model_data, "/kaggle/working/decision_tree_model.pkl")

print("\nModel saved successfully!")
print("Path: /kaggle/working/decision_tree_model.pkl")

# 11. Display sample predictions
results = pd.DataFrame({
    "Actual": y_test.reset_index(drop=True),
    "Predicted": pd.Series(y_pred)
})

print("\nSample predictions:")
print(results.head(10))

# %%
import os
import joblib
from IPython.display import FileLink, display

# Folder to save the model
save_path = "/kaggle/working/decision_tree_model.pkl"

# Check whether the model is trained
if "model" not in globals():
    raise ValueError(
        "Model not found. Pehle Decision Tree training wala code run karein."
    )

# Save the trained model
joblib.dump(model, save_path)

print("Model saved successfully!")
print("File location:", save_path)
print("File size:", round(os.path.getsize(save_path) / 1024, 2), "KB")

# Display download link
display(FileLink(save_path))
