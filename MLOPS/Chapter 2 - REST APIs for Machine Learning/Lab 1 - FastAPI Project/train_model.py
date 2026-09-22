import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
 
# 1. Load the dataset
data = pd.read_excel("employee_attrition.xlsx")
 
# 2. Separate features (X) and target (y)
# Use every column except the target instead of a hand-picked subset, so the model can learn from all available signals.
X = data.drop(columns=["Attrition"])
 
# The target is text ("Yes"/"No"); map it to 1/0 so it is unambiguous and consistent with the API's prediction output.
y = data["Attrition"].map({"Yes": 1, "No": 0})
 
# 3. Identify categorical vs. numerical columns
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numerical_cols = X.select_dtypes(exclude=["object"]).columns.tolist()
 
# 4. Build a preprocessing step
# Numeric columns pass through unchanged. Categorical columns (e.g. OverTime, Department, JobRole) are one-hot encoded so the model receives only numeric input, as scikit-learn requires. handle_unknown="ignore" prevents the API from crashing later if it ever sees a category value not present during training.
preprocessor = ColumnTransformer(transformers=[
    ("num", "passthrough", numerical_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
])
 
# 5. Combine preprocessing and model into a single pipeline
# Bundling both steps means the exact same preprocessing is always applied at prediction time - nothing has to be re-implemented inside app.py.
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
])
 
# 6. Split into training and test sets
# stratify=y keeps the Yes/No ratio consistent between the training and test sets, which matters because attrition datasets are usually imbalanced.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
 
# 7. Train the model
model.fit(X_train, y_train)
 
# 8. Evaluate on the held-out test set
accuracy = model.score(X_test, y_test)
print(f"Model Training Completed. Test Accuracy: {accuracy:.2f}")

# 9. Persist the trained pipeline to disk
# Saving the full Pipeline (not just the classifier) ensures the one-hot encoding logic is saved alongside the model, so app.py does not need to duplicate any preprocessing code.
joblib.dump(model, "attrition_model.joblib")
print("Model Saved Successfully")