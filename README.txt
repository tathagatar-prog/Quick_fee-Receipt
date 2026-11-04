QUICK FEE RECEIPT APP
=====================

A very simple standalone Streamlit app for generating one-off fee receipts.

Fields:
- Student name
- Branch / course
- Month and year paid for
- Amount paid
- Payment date
- Payment mode

Uses your supplied tuition centre logo and centre details. No database and no student records are stored.

WINDOWS SETUP
1. Extract this ZIP.
2. Open Command Prompt in the extracted folder.
3. Run:
   py -m pip install -r requirements.txt
   py -m streamlit run app.py

PRINTING
Generate the receipt, download the HTML receipt, open it in Chrome and press Ctrl+P.
Choose A5 portrait for a compact receipt, or adjust scaling to fit your printer paper.

MOBILE
Run:
   py -m streamlit run app.py --server.address 0.0.0.0
Find your computer's local IP using ipconfig. On a phone on the same Wi-Fi, open:
   http://YOUR-COMPUTER-IP:8501

The app is local-first. Public internet hosting requires secure deployment.
