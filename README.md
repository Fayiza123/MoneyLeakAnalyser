   MONEY LEAK ANALYSER

A Money Leak Analyzer analyzes hidden micro-spending patterns and identifies financial leakages from PDF bank statements.

Problem Statement:

Many individuals track large expenses but ignore frequent small-value transactions (₹20–₹50). These micro-transactions accumulate over time and silently reduce savings.
This project detects and analyzes these "money leaks" automatically from uploaded bank statements.

Solution:
- Extracts transaction data from bank statement PDFs
- Classifies transactions into meaningful categories
- Identifies micro-spending (transactions below ₹50)
- Calculates leak percentage
- Generates risk assessment alerts

Tech Stack
- Python 3.11
- Streamlit
- Pandas
- pdfplumber
- Regex (re)
-  GitHub

Features
-  Upload Bank Statement (PDF)
-  Automatic Transaction Extraction
-  Smart Expense Classification (Food, E-Commerce, Transport, etc.)
-  Debit-Only Expense View
-  Micro-Spending Detection (< ₹50)
-  Separate Micro Transaction Table
-  Leak Percentage Calculation
-  Risk Assessment (Safe / Warning)

 How It Works
1. User uploads bank statement PDF.
2. System extracts transaction rows using text parsing.
3. Transactions are structured into:
   - Date
   - Description
   - Withdrawal
   - Deposit
   - Balance
   - Type
   - Category
4. Debit transactions are filtered.
5. Micro-transactions (< ₹50) are detected.
6. Leak percentage is calculated:
   Leak % = (Micro Spending / Total Spending) × 100
7. Risk assessment message is generated.

 🏗 Architecture 

 PDF Upload --> Text Extraction (pdfplumber) --> Transaction Parsing (Regex) --> DataFrame Structuring (Pandas) --> Classification Engine --> Micro-Spending Analysis --> Risk Evaluation --> Streamlit Dashboard Output 
<img width="1024" height="1536" alt="architecture" src="https://github.com/user-attachments/assets/a3916406-c6d1-46cf-9d20-9bef50bffc12" />
 

[Uploading [microspending transactions.csv](https://github.com/user-attachments/files/25309986/microspending.transactions.csv)
[transactions with categories.csv](https://github.com/user-attachments/files/25309988/transactions.with.categories.csv)
[Transactions(debit only).csv](https://github.com/user-attachments/files/25309987/Transactions.debit.only.csv)
[extracted transaction row.csv](https://github.com/user-attachments/files/25310008/extracted.transaction.row.csv)
<img width="1050" height="485" alt="final outcome" src="https://github.com/user-attachments/assets/a131b20f-4c3b-4e5b-9ba5-33be1bc92e61" />

short vedio:
https://github.com/user-attachments/assets/fedcedda-a187-4cc0-80d9-aaf633154ba2




