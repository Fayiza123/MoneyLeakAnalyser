import streamlit as st
import pdfplumber
import re
import pandas as pd

st.title("Money Leak Analyzer")

uploaded_file = st.file_uploader("Upload your bank statement (PDF)", type=["pdf"])

def classify_transaction(description):
    desc = description.lower()

    if "amazon" in desc or "flipkart" in desc:
        return "E-Commerce"

    elif "swiggy" in desc or "zomato" in desc:
        return "Food"

    elif "uber" in desc or "ola" in desc:
        return "Transport"

    elif "playstore" in desc or "netflix" in desc:
        return "Subscription"

    elif "upi" in desc or "@ok" in desc or "@axis" in desc or "@ybl" in desc:
        return "Transfer"

    else:
        return "Miscellaneous"

if uploaded_file:
    text_data = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_data += text + "\n"

    lines = text_data.split("\n")

    transaction_rows = []
    current_transaction = ""

    date_pattern = r"^\d{1,2}-[A-Z0-9]{3}-\d{4}"

    for line in lines:
        line = line.strip()

        # Ignore unwanted footer/header lines
        if "Abbreviations Used" in line or "GRAND TOTAL" in line:
            continue

        if re.match(date_pattern, line):
            # Save previous transaction
            if current_transaction:
                transaction_rows.append(current_transaction.strip())

            # Start new transaction
            current_transaction = line

        else:
            if current_transaction:
                current_transaction += " " + line

    # Add last transaction
    if current_transaction:
        transaction_rows.append(current_transaction.strip())

    df = pd.DataFrame(transaction_rows, columns=["Transaction Line"])

    st.subheader("Extracted Transaction Rows")
    st.write(df)

    

    structured_data = []
    previous_balance = None

    for row in transaction_rows:
        parts = row.split()

        decimals = re.findall(r"\d+[.,]\d+", row)

        if len(decimals) >= 2:
            balance = float(decimals[-1].replace(",", "."))
            amount = float(decimals[-2].replace(",", "."))

            date = parts[0]
            description = row.replace(date, "").strip()

            # Determine transaction type using balance movement
            if previous_balance is not None:
                if balance < previous_balance:
                    type = "Debit"
                    withdrawal = amount
                    deposit = 0.0
                else:
                    type = "Credit"
                    withdrawal = 0.0
                    deposit = amount
            else:
                type = "Unknown"
                withdrawal = 0.0
                deposit = 0.0

            structured_data.append([
                date,
                description,
                withdrawal,
                deposit,
                balance,
                type
            ])

            previous_balance = balance

    structured_df = pd.DataFrame(
        structured_data,
        columns=["Date", "Description", "Withdrawal", "Deposit", "Balance", "Type"]
    )

    structured_df["Category"] = structured_df["Description"].apply(classify_transaction)

    st.subheader("Transactions with Categories")
    st.write(structured_df)

    debit_df = structured_df[structured_df["Withdrawal"] > 0]


    st.subheader("Expense Transactions (Debit Only)")
    st.write(debit_df)

    MICRO_THRESHOLD = 50

    micro_df = debit_df[debit_df["Withdrawal"] < MICRO_THRESHOLD]
    total_spent = debit_df["Withdrawal"].sum()
    
    micro_total = micro_df["Withdrawal"].sum()

    leak_percent = (micro_total / total_spent) * 100 if total_spent > 0 else 0

    st.subheader("Micro Spending Transactions (< ₹50)")
    st.write(micro_df)

    st.subheader("Money Leak Summary")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Spending", f"₹{total_spent:.2f}")
    col2.metric("Micro Spending (<50)", f"₹{micro_total:.2f}")
    col3.metric("Leak Percentage", f"{leak_percent:.2f}%")

    st.subheader("Final Risk Assessment")

    if micro_total > 50:
        st.error("⚠ Warning: Your total micro spending exceeds ₹50. Small expenses are accumulating.")
        st.write("Suggestion: Track frequent small transactions carefully.")
    else:
        st.success("✅ Safe: Your micro spending is under control.")
        st.write("Great job! Your small expenses are well managed.")

