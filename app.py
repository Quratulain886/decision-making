import io
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(page_title="Starbucks Data Analysis", page_icon="☕", layout="wide")
st.title("☕ Starbucks Data Analysis & Decision Tree")
st.write("Upload your Starbucks CSV to explore beverage categories, view a pie chart, and train a Decision Tree model.")

uploaded = st.file_uploader("Upload Starbucks CSV file", type=["csv"])
if uploaded is None:
    st.info("Upload your Starbucks CSV file to start.")
    st.caption("The app looks for Beverage_category by default when that column exists.")
    st.stop()

try:
    df = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"Could not read CSV: {exc}")
    st.stop()

df.columns = df.columns.astype(str).str.strip()
before = len(df)
df = df.drop_duplicates().dropna(how="all")
st.subheader("Dataset overview")
a, b, c = st.columns(3)
a.metric("Rows", f"{len(df):,}")
b.metric("Columns", len(df.columns))
c.metric("Duplicate rows removed", before - len(df))
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Category distribution — Pie chart")
candidates = [x for x in df.columns if any(k in x.lower() for k in ("category", "beverage", "type"))]
default_col = "Beverage_category" if "Beverage_category" in df.columns else (candidates[0] if candidates else df.columns[0])
category_col = st.selectbox("Choose category column", list(df.columns), index=list(df.columns).index(default_col))
counts = df[category_col].fillna("Missing").astype(str).value_counts()
shown = counts.copy()
if len(shown) > 12:
    shown = shown.head(11)
    shown.loc["Other"] = counts.iloc[11:].sum()

left, right = st.columns([3, 2])
with left:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(shown.values, labels=shown.index, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"Distribution by {category_col}")
    ax.axis("equal")
    st.pyplot(fig)
    plt.close(fig)
with right:
    count_table = counts.rename_axis(category_col).reset_index(name="Count")
    st.dataframe(count_table, use_container_width=True, height=350)
    st.download_button("Download category counts CSV", count_table.to_csv(index=False).encode("utf-8"),
                       file_name="starbucks_category_counts.csv", mime="text/csv")

st.subheader("Decision Tree classification")
target_default = "Beverage_category" if "Beverage_category" in df.columns else category_col
target = st.selectbox("Select target column to predict", list(df.columns),
                      index=list(df.columns).index(target_default))
if st.button("Train Decision Tree", type="primary"):
    work = df.dropna(subset=[target]).copy()
    if len(work) < 5:
        st.error("Please upload at least 5 usable rows.")
        st.stop()
    y = work[target].astype(str)
    X = work.drop(columns=[target])
    X = X.drop(columns=[col for col in X.columns if col.lower() in {"id", "unnamed: 0"}], errors="ignore")
    X = X.dropna(axis=1, how="all")
    if X.shape[1] == 0 or y.nunique() < 2:
        st.error("Need at least one feature column and two target classes.")
        st.stop()
    X = pd.get_dummies(X, dummy_na=True)
    X = X.replace([float("inf"), float("-inf")], float("nan")).fillna(0)
    test_n = min(max(1, round(len(work) * 0.2)), len(work) - 1)
    class_counts = y.value_counts()
    stratify = y if class_counts.min() >= 2 and test_n >= y.nunique() and len(work)-test_n >= y.nunique() else None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_n, random_state=42, stratify=stratify)
    model = DecisionTreeClassifier(criterion="gini", max_depth=5, min_samples_leaf=2,
                                   class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    st.success("Model trained successfully.")
    st.metric("Accuracy", f"{accuracy_score(y_test, pred):.2%}")
    st.dataframe(pd.DataFrame(classification_report(y_test, pred, output_dict=True, zero_division=0)).transpose(),
                 use_container_width=True)
    bundle = {"model": model, "feature_columns": X.columns.tolist(), "target_column": target}
    buffer = io.BytesIO()
    joblib.dump(bundle, buffer)
    st.download_button("Download trained model (.pkl)", buffer.getvalue(),
                       file_name="starbucks_decision_tree_model.pkl", mime="application/octet-stream")

st.caption("The app uses the CSV you upload; it does not rely on a fixed Kaggle path.")
