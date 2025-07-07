import streamlit as st
import re
import datetime
import os
import pandas as pd
from fpdf import FPDF

EXCEL_FILE = "bookings.xlsx"


# ----------------- Save to Excel -----------------
def save_booking(data_dict):
    df_new = pd.DataFrame([data_dict])
    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_excel(EXCEL_FILE, index=False)

# ----------------- PDF Invoice Generator -----------------
def generate_invoice(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Mobile Repair Invoice", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        clean_key = key.encode("ascii", "ignore").decode()
        clean_value = str(value).encode("ascii", "ignore").decode()
        pdf.cell(200, 10, f"{clean_key}: {clean_value}", ln=True)

    invoice_name = f"Invoice_{data['Name'].replace(' ', '_')}_{data['Timestamp'].replace(':', '-').replace(' ', '_')}.pdf"
    pdf.output(invoice_name)
    return invoice_name


# ----------------- Page Config -----------------
st.set_page_config(page_title="ShivShakti Mobile Repairing - Jalgaon", layout="centered", page_icon="📱")

# ----------------- Styling -----------------
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        h1, h2, h3 {color: #2E8B57;}
        .section {padding: 20px 0;}
        .footer {text-align: center; font-size: 14px; color: gray; margin-top: 50px;}
        hr {border: 1px solid #ccc;}
        @media only screen and (max-width: 768px) {
            h1 { font-size: 32px !important; }
        }
        .whatsapp-float {
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 25px;
            right: 25px;
            background-color: #25D366;
            color: white;
            border-radius: 50px;
            text-align: center;
            font-size: 30px;
            box-shadow: 2px 2px 3px #999;
            z-index: 100;
        }
        .whatsapp-icon {
            margin-top: 13px;
        }
    </style>
    <a href="https://wa.me/917030663155" class="whatsapp-float" target="_blank">
        <div class="whatsapp-icon">💬</div>
    </a>
""", unsafe_allow_html=True)

# ----------------- Header -----------------
st.markdown("<h1 style='text-align:center;'>📱 ShivShakti Mobile Repairing, Jalgaon</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Your One-Stop Solution for All Mobile Issues</h4>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- Home Section -----------------
st.markdown("## 🏠 Welcome")
with open("images/demo.mp4", "rb") as video_file:
    video_bytes = video_file.read()
    st.video(video_bytes)

#st.image("Designer.png", width=500)
st.success("We fix all brands – Apple, Samsung, Vivo, Oppo, Xiaomi, and more. Reliable service with warranty.")

# ----------------- Services Section -----------------
st.markdown("---")
st.markdown("## 🛠️ Our Services")
services = [
    {"name": "📱 Screen Replacement", "price": "₹150"},
    {"name": "🔋 Battery Replacement", "price": "₹200"},
    {"name": "💧 Water Damage Repair", "price": "₹1,200"},
    {"name": "⚡ Charging Port Repair", "price": "₹100"},
    {"name": "🔄 Software Update", "price": "₹400"},
    {"name": "🔓 Unlocking Services", "price": "₹250"},
    {"name": "🧼 Internal Cleaning", "price": "₹150"},
    {"name": "📈 Data Recovery", "price": "₹500"},
    {"name": "🛠️ Others", "price": "₹200"}
]
for s in services:
    st.write(f"**{s['name']}** – {s['price']}")

# ----------------- Booking Section -----------------
st.markdown("---")
st.markdown("## 📅 Book a Service")

import os

invoice_path = None  # initialize before form
downloaded_invoice = False  # track download

with st.form("booking_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Mobile Number")
    selected_service = st.selectbox("Select Service", [s["name"] for s in services])
    preferred_date = st.date_input("Preferred Date", datetime.date.today())
    preferred_time = st.time_input("Preferred Time(Open: 11:00 AM to 8:00 PM)", value=datetime.time(11, 0))
    submit_booking = st.form_submit_button("Book Now")

    if submit_booking:
        if datetime.time(11, 0) <= preferred_time <= datetime.time(20, 0):
            if not name.strip():
                st.warning("Please enter your name.")
            elif not re.fullmatch(r"[6-9]\d{9}", phone.strip()):
                st.warning("Please enter a valid 10-digit mobile number.")
            else:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                booking_data = {
                    "Name": name,
                    "Phone": phone,
                    "Service": selected_service,
                    "Date": str(preferred_date),
                    "Time": preferred_time.strftime("%I:%M %p"),
                    "Timestamp": timestamp
                }
                save_booking(booking_data)
                invoice_path = generate_invoice(booking_data)
                st.success(f"✅ Booking confirmed for **{selected_service}** on **{preferred_date} at {preferred_time.strftime('%I:%M %p')}**. Thank you, {name}!")
        else:
            st.error("❌ Please choose a time between 11:00 AM and 8:00 PM.")

# ✅ Show download button and delete invoice after
if invoice_path:
    with open(invoice_path, "rb") as f:
        st.download_button(
            label="📄 Download Invoice (PDF)",
            data=f,
            file_name=invoice_path,
            mime="application/pdf"
        )

# ----------------- Testimonials -----------------
st.markdown("---")
st.markdown("## 📢 What Our Customers Say")
st.info("“Phone got repaired in 2 hours. Very professional and affordable!” – Priya J.")
st.info("“Great experience! Honest pricing and support.” – Akshay M.")
st.info("“They fixed my water-damaged iPhone. Highly recommended!” – Rahul T.")

# ----------------- FAQ -----------------
st.markdown("---")
st.markdown("## ❓ Frequently Asked Questions")
st.write("**Q: How long does a typical repair take?**")
st.write("A: Most repairs are completed in 1–2 hours.")
st.write("**Q: Do you offer warranty?**")
st.write("A: Yes, up to 3 months depending on the service.")
st.write("**Q: Do you have pickup/drop?**")
st.write("A: Yes, within Jalgaon city limits.")

# ----------------- About Us -----------------
st.markdown("---")
st.markdown("## ℹ️ About Us")
#st.image("ironman.jpg", width=400)
st.markdown("""
We are a trusted mobile repair shop operating in Jalgaon for over **15 years**. Our expert technicians provide both software and hardware solutions. We have served **10,000+ happy customers**.
""")

# ----------------- Contact Us -----------------
st.markdown("---")
st.markdown("## 📞 Contact Us")
with st.form("contact_form"):
    c_name = st.text_input("Your Name")
    c_email = st.text_input("Email")
    c_phone = st.text_input("Mobile Number")
    c_message = st.text_area("Message")
    submit_contact = st.form_submit_button("Submit")

    if submit_contact:
        if not c_name.strip():
            st.warning("Please enter your name.")
        elif not re.fullmatch(r"[6-9]\d{9}", c_phone.strip()):
            st.warning("Please enter a valid phone number.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", c_email.strip()):
            st.warning("Please enter a valid email address.")
        elif not c_message.strip():
            st.warning("Message cannot be empty.")
    else:
        st.success("Thank you! We have received your message and will get back to you soon.")

    st.markdown("📍 **Address:** Shop No 140 Third Floor Golani Market, Jalgaon – 425001")
    st.markdown("📞 **Phone:** +91-7030663155")
    st.markdown("✉️ **Email:** support@ShivShaktimobilejalgaon.com")

# ----------------- Footer -----------------
st.markdown("---")
st.markdown('<div class="footer">© 2025 Girish Pardeshi. All rights reserved.</div>', unsafe_allow_html=True)
