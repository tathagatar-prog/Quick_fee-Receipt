import streamlit as st
from datetime import date
from pathlib import Path
import io
import streamlit.components.v1 as components

from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Quick Fee Receipt", page_icon="🧾", layout="centered")

ROOT = Path(__file__).parent
LOGO = ROOT / "logo.png"
SIGNATURE = ROOT / "signature.png"

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

def make_receipt_pdf(data):
    """Create a compact, shareable A5 PDF receipt with the supplied centre logo."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A5,
        rightMargin=14*mm, leftMargin=14*mm,
        topMargin=12*mm, bottomMargin=12*mm,
        title=f"Fee Receipt - {data['student']}",
        author=CENTRE
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CentreTitle", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, leading=16, textColor=colors.HexColor("#173b68"), spaceAfter=3
    )
    small_style = ParagraphStyle(
        "SmallCentre", parent=styles["Normal"], fontName="Helvetica",
        fontSize=7.5, leading=10, textColor=colors.HexColor("#475569")
    )
    receipt_title = ParagraphStyle(
        "ReceiptTitle", parent=styles["Heading2"], alignment=TA_CENTER,
        fontSize=13, leading=16, textColor=colors.HexColor("#173b68"),
        spaceBefore=8, spaceAfter=10
    )
    label_style = ParagraphStyle(
        "Label", parent=styles["Normal"], fontSize=9, leading=13,
        textColor=colors.HexColor("#526174")
    )
    value_style = ParagraphStyle(
        "Value", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=9, leading=13, textColor=colors.HexColor("#172033")
    )
    amount_style = ParagraphStyle(
        "Amount", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=17, leading=20, textColor=colors.HexColor("#12653b"),
        alignment=TA_RIGHT
    )
    paid_style = ParagraphStyle(
        "Paid", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, textColor=colors.HexColor("#12653b"),
        alignment=TA_CENTER
    )
    story = []

    header_left = []
    if LOGO.exists():
        try:
            logo = RLImage(str(LOGO), width=27*mm, height=24*mm, kind="proportional")
            header_left.append(logo)
        except Exception:
            header_left.append(Paragraph(" ", small_style))
    else:
        header_left.append(Paragraph(" ", small_style))

    header_right = [
        Paragraph(CENTRE, title_style),
        Paragraph(ADDRESS, small_style),
        Paragraph(f"Phone: {PHONE}", small_style),
    ]
    header = Table([[header_left, header_right]], colWidths=[31*mm, 111*mm])
    header.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LINEBELOW", (0,0), (-1,-1), 0.8, colors.HexColor("#9aa9bc")),
    ]))
    story.append(header)
    story.append(Paragraph("FEE PAYMENT RECEIPT", receipt_title))

    rows = [
        [Paragraph("Payment date", label_style), Paragraph(data["payment_date"], value_style)],
        [Paragraph("Student name", label_style), Paragraph(data["student"], value_style)],
        [Paragraph("Branch / Course", label_style), Paragraph(data["branch"], value_style)],
        [Paragraph("Fee paid for", label_style), Paragraph(data["month"], value_style)],
        [Paragraph("Payment mode", label_style), Paragraph(data["mode"], value_style)],
        [Paragraph("Amount received", label_style), Paragraph(f"INR {int(data['amount']):,}", amount_style)],
    ]
    details = Table(rows, colWidths=[47*mm, 95*mm])
    details.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (1,0), (1,-1), "RIGHT"),
        ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (0,0), (-1,-1), 3),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LINEBELOW", (0,0), (-1,-1), 0.45, colors.HexColor("#cbd5e1")),
    ]))
    story.append(details)
    story.append(Spacer(1, 9*mm))
    paid_box = Table([[Paragraph("PAYMENT RECEIVED", paid_style)]], colWidths=[142*mm])
    paid_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#e7f6ed")),
        ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#b6dfc5")),
        ("ROUNDEDCORNERS", [8,8,8,8]),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(paid_box)
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        f"Thank you for choosing {CENTRE}.", 
        ParagraphStyle("Thanks", parent=small_style, alignment=TA_CENTER, fontSize=8)
    ))
    story.append(Spacer(1, 12*mm))
    # Use the user's uploaded handwritten signature on every generated receipt.
    signature_content = []
    if SIGNATURE.exists():
        try:
            signature_img = RLImage(str(SIGNATURE), width=43*mm, height=25*mm, kind="proportional")
            signature_img.hAlign = "CENTER"
            signature_content.append(signature_img)
        except Exception:
            signature_content.append(Paragraph(" ", small_style))
    else:
        signature_content.append(Paragraph(" ", small_style))
    signature_content.append(Paragraph(
        "Authorised Signature",
        ParagraphStyle("SignatureLabel", parent=small_style, alignment=TA_CENTER, fontSize=8)
    ))
    signature_cell = Table([[signature_content]], colWidths=[67*mm])
    signature_cell.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    signature_table = Table([["", signature_cell]], colWidths=[75*mm, 67*mm])
    signature_table.setStyle(TableStyle([
        ("ALIGN", (1,0), (1,0), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(signature_table)

    doc.build(story)
    return buffer.getvalue()

st.title("🧾 Quick Fee Receipt")
st.caption("Enter the payment details, generate a PDF and share it directly. No student database required.")

with st.form("receipt_form"):
    student = st.text_input("Student name *", placeholder="Enter student name")
    branch = st.selectbox("Branch / Course", [
        "BCA", "MCA", "B.Tech", "B.Sc", "ITI", "CST", "XI", "XII", "Other"
    ])
    month = st.selectbox("Fee paid for month", [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ], index=date.today().month-1)
    years = list(range(date.today().year-2, date.today().year+3))
    year = st.selectbox("Year", years, index=2)
    amount = st.number_input("Fees paid (₹) *", min_value=1, step=100, value=1000)
    payment_date = st.date_input("Payment date", value=date.today())
    payment_mode = st.selectbox("Payment mode", ["Cash", "UPI", "Bank Transfer", "Other"])
    submitted = st.form_submit_button("Generate PDF receipt", type="primary", use_container_width=True)

if submitted:
    if not student.strip():
        st.error("Please enter the student's name.")
    else:
        st.session_state["receipt_data"] = {
            "student": student.strip(),
            "branch": branch,
            "month": f"{month} {year}",
            "amount": amount,
            "payment_date": payment_date.strftime("%d-%m-%Y"),
            "mode": payment_mode
        }

if "receipt_data" in st.session_state:
    d = st.session_state["receipt_data"]
    pdf_bytes = make_receipt_pdf(d)
    st.success("Your PDF receipt is ready.")
    st.download_button(
        "⬇️ Download / Share PDF Receipt",
        data=pdf_bytes,
        file_name=f"Fee_Receipt_{d['student'].replace(' ','_')}_{d['month'].replace(' ','_')}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
    st.caption("The downloaded PDF can be shared through WhatsApp, email or any other app, and printed whenever needed.")
    with st.expander("Receipt details"):
        st.write(f"**Student:** {d['student']}")
        st.write(f"**Branch:** {d['branch']}")
        st.write(f"**Month:** {d['month']}")
        st.write(f"**Amount:** ₹{int(d['amount']):,}")
        st.write(f"**Payment date:** {d['payment_date']}")
        st.write(f"**Mode:** {d['mode']}")
    st.info("This quick receipt app does not save student records or payment history. Download the PDF after generating each receipt.")
