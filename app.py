import streamlit as st
from datetime import date
from pathlib import Path
import base64
import html
import streamlit.components.v1 as components

st.set_page_config(page_title="Quick Fee Receipt", page_icon="🧾", layout="centered")

ROOT = Path(__file__).parent
LOGO = ROOT / "logo.png"

CENTRE = "Tutoring Computer Science & Application"
ADDRESS = "496/2, Amarabati Rd, Choto Bazar, Nabapally, Barasat, Kolkata, West Bengal 700126"
PHONE = "070035 85265"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.block-container{max-width:760px;padding-top:1.4rem;padding-bottom:2rem}
[data-testid="stForm"]{border:1px solid #e5eaf2;border-radius:16px;padding:20px}
div.stButton>button,div.stFormSubmitButton>button{border-radius:10px;min-height:2.8rem;font-weight:650}
</style>
""", unsafe_allow_html=True)

st.title("🧾 Quick Fee Receipt")
st.caption("Enter four details, generate a receipt and print it. No student database required.")

with st.form("receipt_form"):
    student = st.text_input("Student name *", placeholder="Enter student name")
    branch = st.selectbox("Branch / Course", [
        "BCA", "MCA", "B.Tech", "B.Sc", "ITI", "CST", "XI", "XII", "Other"
    ])
    month = st.selectbox("Fee paid for month", [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])
    year = st.selectbox("Year", list(range(date.today().year-2, date.today().year+3)),
                        index=2)
    amount = st.number_input("Fees paid (₹) *", min_value=1, step=100, value=1000)
    payment_date = st.date_input("Payment date", value=date.today())
    payment_mode = st.selectbox("Payment mode", ["Cash", "UPI", "Bank Transfer", "Other"])
    submitted = st.form_submit_button("Generate receipt", type="primary", use_container_width=True)

if submitted:
    if not student.strip():
        st.error("Please enter the student's name.")
    else:
        st.session_state["receipt_data"] = {
            "student": student.strip(), "branch": branch,
            "month": f"{month} {year}", "amount": amount,
            "payment_date": payment_date.strftime("%d-%m-%Y"),
            "mode": payment_mode
        }

if "receipt_data" in st.session_state:
    d = st.session_state["receipt_data"]
    logo_uri = ""
    if LOGO.exists():
        logo_uri = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode("ascii")

    # HTML-escape all user-entered values before inserting into the printable receipt.
    safe = {k: html.escape(str(v)) for k, v in d.items()}
    receipt_html = f"""
    <!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      @page {{ size: A5 portrait; margin: 8mm; }}
      * {{ box-sizing:border-box; }}
      body {{ margin:0; background:#fff; color:#172033; font-family:Arial,sans-serif; }}
      .receipt {{ width:100%; max-width:620px; margin:0 auto; border:1.5px solid #24476f;
                  padding:18px 20px; background:#fff; }}
      .head {{ display:flex; align-items:center; gap:13px; border-bottom:1px solid #aab8c8; padding-bottom:12px; }}
      .logo {{ width:82px; height:72px; object-fit:contain; }}
      h2 {{ margin:0 0 5px; color:#173b68; font-size:17px; line-height:1.25; }}
      .address {{ color:#475569; font-size:10px; line-height:1.5; }}
      h3 {{ text-align:center; color:#173b68; font-size:15px; letter-spacing:1.2px; margin:15px 0 12px; }}
      .row {{ display:flex; justify-content:space-between; gap:12px; padding:9px 2px;
              border-bottom:1px dashed #cbd5e1; font-size:12px; }}
      .row span:first-child {{ color:#526174; }}
      .amount {{ color:#12653b; font-size:22px; font-weight:700; }}
      .paid {{ display:inline-block; margin:14px auto 0; padding:6px 15px; border-radius:30px;
               background:#e7f6ed; color:#12653b; font-weight:bold; font-size:10px; }}
      .center {{ text-align:center; }}
      .thanks {{ margin-top:16px; text-align:center; font-size:10px; color:#526174; }}
      .sign {{ margin-top:27px; text-align:right; font-size:10px; color:#334155; }}
      @media print {{ body {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }} }}
    </style></head><body>
      <div class="receipt">
        <div class="head">
          {f'<img class="logo" src="{logo_uri}" alt="Centre logo">' if logo_uri else ''}
          <div><h2>{CENTRE}</h2><div class="address">{ADDRESS}<br>Phone: {PHONE}</div></div>
        </div>
        <h3>FEE PAYMENT RECEIPT</h3>
        <div class="row"><span>Payment date</span><b>{safe['payment_date']}</b></div>
        <div class="row"><span>Student name</span><b>{safe['student']}</b></div>
        <div class="row"><span>Branch / Course</span><b>{safe['branch']}</b></div>
        <div class="row"><span>Fee paid for</span><b>{safe['month']}</b></div>
        <div class="row"><span>Payment mode</span><b>{safe['mode']}</b></div>
        <div class="row"><span>Amount received</span><strong class="amount">₹{int(d['amount']):,}</strong></div>
        <div class="center"><span class="paid">PAYMENT RECEIVED</span></div>
        <div class="thanks">Thank you for choosing {CENTRE}.</div>
        <div class="sign">Authorised Signature<br><br>________________________</div>
      </div>
    </body></html>
    """
    st.markdown("### Receipt preview")
    components.html(receipt_html, height=470, scrolling=True)
    st.download_button(
        "Download printable receipt (HTML)",
        data=receipt_html.encode("utf-8"),
        file_name=f"fee_receipt_{d['student'].replace(' ','_')}_{d['month'].replace(' ','_')}.html",
        mime="text/html",
        use_container_width=True
    )
    st.info("To print: open the downloaded HTML receipt in Chrome and press Ctrl + P. Choose A5 or scale to fit your paper.")
    st.caption("This quick tool does not save student records or payment history. Generate and print each receipt as needed.")
