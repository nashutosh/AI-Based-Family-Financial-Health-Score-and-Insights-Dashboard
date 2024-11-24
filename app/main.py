
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load model
try:
    model = joblib.load('financial_expenses_model.pkl')
except FileNotFoundError:
    model = None

class FinancialData(BaseModel):
    Income: float
    Savings: float
    Loan_Payments: float
    Credit_Card_Spending: float
    Dependents: float
    Financial_Goals_Met: float

@app.post("/predict")
async def predict_score(data: FinancialData):
    try:
        savings_ratio = data.Savings / data.Income
        expenses_ratio = (data.Loan_Payments + data.Credit_Card_Spending) / data.Income
        health_score = (
            savings_ratio * 40 +
            (1 - expenses_ratio) * 30 +
            data.Financial_Goals_Met * 10
        ).clip(0, 100)

        recommendations = []
        if savings_ratio < 0.2:
            recommendations.append("Increase savings to at least 20% of income.")
        if expenses_ratio > 0.7:
            recommendations.append("Reduce expenses below 70% of income.")
        if data.Financial_Goals_Met < 50:
            recommendations.append("Focus on achieving more financial goals.")

        return {
            "Financial Health Score": health_score,
            "Recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
