import streamlit as st
import pandas as pd
from modules.db import init_db, add_expense, load_expenses
from modules.auth import login, signup
from modules.ml_model import predict_category
from modules.analytics import category_summary, monthly_summary
import plotly.express as px

# --- INIT ---
init_db()

# --- LOAD CSS ---
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SESSION ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- LOGIN / SIGNUP ---
if not st.session_state.user:
    st.title("🔐 Login / Signup")

    choice = st.radio("Select", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if signup(username, password):
                st.success("Account created!")
            else:
                st.error("User already exists")

    else:
        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.success("Logged in!")
            else:
                st.error("Invalid credentials")

    st.stop()

# --- SIDEBAR ---
menu = st.sidebar.selectbox("📂 Menu", ["Dashboard", "Add Expense", "Analytics"])

# --- LOAD DATA ---
df = load_expenses(st.session_state.user)

# ================= DASHBOARD =================
if menu == "Dashboard":
    st.title("💰 Smart Expense Dashboard")

    if not df.empty:
        total = df["amount"].sum()
        avg = df["amount"].mean()
        max_spend = df["amount"].max()

        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Total Spent", f"₹{total:.2f}")
        col2.metric("📊 Avg Expense", f"₹{avg:.2f}")
        col3.metric("🔥 Highest", f"₹{max_spend:.2f}")

        st.markdown("### 📋 Recent Expenses")
        st.dataframe(df.tail(5), use_container_width=True)

    else:
        st.info("No expenses yet. Add some!")

# ================= ADD EXPENSE =================
elif menu == "Add Expense":
    st.title("➕ Add Expense")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    date = st.date_input("Date")
    amount = st.number_input("Amount", min_value=0.0)
    desc = st.text_input("Description")

    if st.button("Add Expense"):
        category = predict_category(desc)
        add_expense(st.session_state.user, date, amount, category, desc)
        st.success(f"Added under category: {category}")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= ANALYTICS =================
elif menu == "Analytics":
    st.title("📊 Analytics")

    if not df.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Category Distribution")
            cat = category_summary(df)
            fig = px.pie(values=cat.values, names=cat.index)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Monthly Spending")
            month = monthly_summary(df)
            fig2 = px.line(
                x=month.index.astype(str),
                y=month.values,
                markers=True
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("No data to analyze yet.")