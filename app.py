"""Interactive personal-expense analytics dashboard."""

from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st


DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "expense_data.csv"

@st.cache_data
def load_expenses(uploaded_file=None) -> pd.DataFrame:
    """Read the original Excel layout or the SQL-ready CSV extract."""
    if uploaded_file is None:
        data = pd.read_csv(DEFAULT_DATA_PATH)
    else:
        raw = uploaded_file.getvalue()
        if uploaded_file.name.lower().endswith(".csv"):
            data = pd.read_csv(BytesIO(raw))
        else:
            data = pd.read_excel(BytesIO(raw), sheet_name="data")
    # Supports both the original Excel headers (DATE, DAY_TYPE, ...) and
    # the repository CSV headers (expense_date, day_type, ...).
    data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    data = data.rename(columns={"date": "expense_date", "day": "day_name"})
    data["expense_date"] = pd.to_datetime(data["expense_date"])
    required = {"expense_date", "day_name", "day_type", "category", "description", "amount", "payment_mode"}
    missing = required.difference(data.columns)
    if missing or (data["amount"] <= 0).any():
        raise ValueError(f"Invalid dataset. Missing columns: {sorted(missing)}")
    return data


def money(value: float) -> str:
    return f"₹{value:,.0f}"


st.set_page_config(page_title="Expense Analytics", page_icon="💳", layout="wide")
st.title("Personal Expense Analytics")
st.caption("Interactive portfolio project | December 2025 transaction data | Amounts in INR")

uploaded_file = st.sidebar.file_uploader("Upload expense data", type=["xlsx", "csv"], help="Upload the original expense.xlsx file or an exported CSV.")
expenses = load_expenses(uploaded_file)
with st.sidebar:
    st.header("Filters")
    selected_dates = st.date_input(
        "Date range",
        value=(expenses.expense_date.min().date(), expenses.expense_date.max().date()),
        min_value=expenses.expense_date.min().date(),
        max_value=expenses.expense_date.max().date(),
    )
    categories = st.multiselect("Categories", sorted(expenses.category.unique()), default=sorted(expenses.category.unique()))
    payment_modes = st.multiselect("Payment modes", sorted(expenses.payment_mode.unique()), default=sorted(expenses.payment_mode.unique()))
    day_types = st.multiselect("Day type", sorted(expenses.day_type.unique()), default=sorted(expenses.day_type.unique()))

if len(selected_dates) != 2:
    st.warning("Select both a start and end date.")
    st.stop()

start_date, end_date = map(pd.Timestamp, selected_dates)
filtered = expenses.loc[
    expenses.expense_date.between(start_date, end_date)
    & expenses.category.isin(categories)
    & expenses.payment_mode.isin(payment_modes)
    & expenses.day_type.isin(day_types)
].copy()
if filtered.empty:
    st.info("No transactions match the selected filters. Adjust the filters to continue.")
    st.stop()

daily = filtered.groupby("expense_date", as_index=False).amount.sum().rename(columns={"amount": "daily_spend"})
category = filtered.groupby("category", as_index=False).amount.sum().sort_values("amount", ascending=False)
payment = filtered.groupby("payment_mode", as_index=False).amount.sum().sort_values("amount", ascending=False)
day_type = filtered.groupby("day_type", as_index=False).agg(total_spend=("amount", "sum"), active_days=("expense_date", "nunique"))
day_type["average_per_day"] = day_type.total_spend / day_type.active_days

top_category = category.iloc[0]
highest_day = daily.loc[daily.daily_spend.idxmax()]
metrics = st.columns(4)
metrics[0].metric("Total spend", money(filtered["amount"].sum()))
metrics[1].metric("Average daily spend", money(daily["daily_spend"].mean()))
metrics[2].metric("Top category", top_category["category"], money(top_category["amount"]))
metrics[3].metric("Highest-spend day", highest_day["expense_date"].strftime("%d %b %Y"), money(highest_day["daily_spend"]))

st.divider()
left, right = st.columns((1.3, 1))
with left:
    st.subheader("Daily spending trend")
    st.line_chart(daily, x="expense_date", y="daily_spend", color="#4F6DF5", height=310)
with right:
    st.subheader("Category spending")
    st.bar_chart(category, x="category", y="amount", color="#6C82E8", horizontal=True, height=310)

left, right = st.columns(2)
with left:
    st.subheader("Weekday vs. weekend")
    st.bar_chart(day_type, x="day_type", y="total_spend", color="#87A7FF", height=270)
with right:
    st.subheader("Payment mode")
    st.bar_chart(payment, x="payment_mode", y="amount", color="#A48FE8", height=270)

st.subheader("Spending insights")
top_share = 100 * top_category["amount"] / filtered["amount"].sum()
threshold = daily["daily_spend"].mean() + daily["daily_spend"].std(ddof=0)
outliers = int((daily["daily_spend"] > threshold).sum())
st.write(f"**{top_category['category']}** makes up **{top_share:.1f}%** of spending in the current view. There are **{outliers}** daily spending spikes above one standard deviation from the average.")

with st.expander("View filtered transactions"):
    display = filtered.sort_values(["expense_date", "amount"], ascending=[False, False]).copy()
    display["expense_date"] = display["expense_date"].dt.strftime("%d %b %Y")
    display["amount"] = display["amount"].map(money)
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.download_button("Download filtered transactions (CSV)", filtered.to_csv(index=False).encode("utf-8"), "filtered_expenses.csv", "text/csv")
