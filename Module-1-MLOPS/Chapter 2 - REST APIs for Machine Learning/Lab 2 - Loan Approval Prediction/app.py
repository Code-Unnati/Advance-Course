from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
 
app = FastAPI(title="Loan Approval Prediction API")
 
# Load the trained pipeline once at startup, not per request.
model = joblib.load("loan_model.joblib")
 
@app.get("/")
def home():
    """Simple health-check endpoint."""
    return {"message": "Loan Approval Prediction API Running"}

# Request schema: every feature the model was trained on.
# Using Pydantic here means FastAPI validates types and reports clear errors automatically.
class LoanApplication(BaseModel):
    Age: int
    Gender: str
    Married: str
    Dependents: int
    Education: str
    Self_Employed: str
    ApplicantIncome: int
    CoapplicantIncome: int
    LoanAmount: int
    Loan_Amount_Term: int
    Credit_History: int
    Property_Area: str
 
@app.post("/predict")
def predict(application: LoanApplication):
    # Convert the validated request body into a single-row DataFrame. Column names must match those seen in training, since the saved pipeline selects columns by name.
    row = pd.DataFrame([application.dict()])

     # The pipeline re-applies the same one-hot encoding used during training, so text fields can be passed in as-is.
    prediction = model.predict(row)[0]
    probability = model.predict_proba(row)[0][1]
 
    result = "Loan Approved" if prediction == 1 else "Loan Rejected"
    return {
        "Prediction": result,
        "approval_probability": round(float(probability), 2),
    }
