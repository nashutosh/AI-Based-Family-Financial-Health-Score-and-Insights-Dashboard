
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Financial Health Dashboard")

income = st.number_input("Income ($)", min_value=0, value=5000)
savings = st.number_input("Savings ($)", min_value=0, value=1000)
loan_payments = st.number_input("Loan Payments ($)", min_value=0, value=500)
credit_card_spending = st.number_input("Credit Card Spending ($)", min_value=0, value=300)
dependents = st.number_input("Dependents", min_value=0, value=2)
financial_goals_met = st.slider("Financial Goals Met (%)", 0, 100, 60)

if st.button("Calculate"):
    savings_ratio = savings / income
    expenses_ratio = (loan_payments + credit_card_spending) / income
    health_score = (
        savings_ratio * 40 +
        (1 - expenses_ratio) * 30 +
        financial_goals_met * 10
    ).clip(0, 100)

    st.write(f"### Financial Health Score: **{health_score:.2f}**")

    recommendations = []
    if savings_ratio < 0.2:
        recommendations.append("Increase savings to at least 20% of income.")
    if expenses_ratio > 0.7:
        recommendations.append("Reduce expenses below 70% of income.")
    if financial_goals_met < 50:
        recommendations.append("Aim to meet more financial goals.")

    st.write("### Recommendations")
    for rec in recommendations:
        st.write(f"- {rec}")
