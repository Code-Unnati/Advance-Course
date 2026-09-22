import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
 
# 1. Load the dataset
data = pd.read_excel("loan_approval.xlsx")
 
# 2. Separate features (X) and target (y)
# Use every column except the target, instead of a small hand-picked subset, so the model can use all available signals.
X = data.drop(columns=["Loan_Status"])
 
# The target is text ("Y"/"N"); map it to 1/0 for the classifier and so the API's output is unambiguous.
y = data["Loan_Status"].map({"Y": 1, "N": 0})
 
# 3. Identify categorical vs. numerical columns
categorical_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
numerical_cols = X.select_dtypes(exclude=["object", "string"]).columns.tolist()
 
# 4. Preprocessing: one-hot encode categorical columns
# Gender, Married, Education, Self_Employed and Property_Area are text columns. Passing them straight into RandomForestClassifier, as the original script did, raises "could not convert string to float". handle_unknown="ignore" also protects the live API from crashing on a category value that was not seen during training.
preprocessor = ColumnTransformer(transformers=[
    ("num", "passthrough", numerical_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
])
 
# 5. Combine preprocessing and model into a single pipeline
# This guarantees app.py reuses the exact same encoding at prediction time, rather than re-implementing it separately.
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
])
 
# 6. Split into training and test sets, then train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model.fit(X_train, y_train)
 
# 7. Evaluate and save
accuracy = model.score(X_test, y_test)
print(f"Model Trained Successfully. Test Accuracy: {accuracy:.2f}")
joblib.dump(model, "loan_model.joblib")
print("Model Saved Successfully")
