from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
 
app = FastAPI(title="Employee Attrition Prediction API")
 
# Load the trained pipeline once, when the API starts.
# Loading it inside the endpoint function would reload the model from disk on every single request, which is slow and unnecessary.
model = joblib.load("attrition_model.joblib")

@app.get("/")
def home():
    """Simple health-check endpoint."""
    return {"message": "Employee Attrition Prediction API"} 

class EmployeeInput(BaseModel):
    Age: int
    BusinessTravel: str
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int
 
 
@app.post("/predict")
def predict(employee: EmployeeInput):
    # Convert the validated request body into a single-row
    # DataFrame. Column names must match those used during training, since the saved pipeline looks them up by name.
    row = pd.DataFrame([employee.dict()])
 
    # The pipeline applies the same one-hot encoding used in training automatically, so raw text fields like OverTime or Department can be passed in directly.
    prediction = model.predict(row)[0]
    probability = model.predict_proba(row)[0][1]
 
    result = "Employee Likely to Leave" if prediction == 1 else "Employee Likely to Stay"
 
    return {
        "prediction": result,
        "attrition_probability": round(float(probability), 2),
    }
