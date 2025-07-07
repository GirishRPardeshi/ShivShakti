import streamlit as st
import os
import pandas as pd

EXCEL_FILE = "bookings.xlsx"
ADMIN_PASSWORD = "Girish7871" 

    
# ------------------ Admin Panel ------------------
st.header("🔐 Admin Login")
pw = st.text_input("Enter admin password:", type="password")

# Show only if something is entered
if pw:
    if pw == ADMIN_PASSWORD:
        st.success("✅ Access granted.")
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            st.dataframe(df)

            # Delete individual booking
            st.markdown("### ❌ Delete a Booking")
            if not df.empty:
                idx = st.number_input("Row index to delete", 0, len(df)-1)
                if st.button("🗑️ Delete Booking"):
                    df.drop(index=idx, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    df.to_excel(EXCEL_FILE, index=False)
                    st.success("Booking deleted.")
                    st.rerun()

            # Delete all bookings
            st.markdown("### 🚨 Delete All Bookings")
            if st.button("🧹 Delete All Bookings"):
                os.remove(EXCEL_FILE)
                st.success("All bookings deleted.")
                st.rerun()
        else:
            st.warning("No bookings yet.")
    else:
        st.error("❌ Incorrect password.")
