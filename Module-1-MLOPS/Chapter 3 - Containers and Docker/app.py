from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
 
app = FastAPI(title="Customer Segmentation API")
 
# Load the trained pipeline (scaler + KMeans) once at startup.
model = joblib.load("customer_segment_model.pkl")
 
class Customer(BaseModel):
    AnnualIncome: float
    SpendingScore: float
 
@app.get("/")
def home():
    """Simple health-check endpoint."""
    return {"message": "Customer Segmentation API Running"}
 
@app.post("/predict")
def predict(customer: Customer):
    # Build a single-row DataFrame using the same column names and order seen during training, so the pipeline's scaler transforms the input consistently.
    row = pd.DataFrame(
        [[customer.AnnualIncome, customer.SpendingScore]],
        columns=["AnnualIncome", "SpendingScore"],
    )
 
    # model.predict() runs the input through the saved scaler first, then assigns it to the nearest cluster centroid.
    segment = model.predict(row)[0]
    return {"Customer Segment": int(segment)}
