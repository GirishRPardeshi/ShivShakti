import streamlit as st
import os
import pandas as pd
import altair as alt

EXCEL_FILE = "bookings.xlsx"
CONTACT_FILE = "contact_messages.xlsx"
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

            # ------------------ Booking Analytics ------------------
            st.markdown("---")
            st.header("📊 Booking Analytics Dashboard")

            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date'])  # Drop rows where date conversion failed

            # Total bookings
            st.metric("📅 Total Bookings", len(df))

            # Most popular service
            if not df['Service'].empty:
                most_common_service = df['Service'].mode()[0]
                st.metric("🔥 Most Booked Service", most_common_service)

            # Booking trend over time
            date_counts = df['Date'].value_counts().sort_index()
            chart_data = pd.DataFrame({'Date': date_counts.index, 'Bookings': date_counts.values})
            st.subheader("📈 Daily Booking Trend")
            line_chart = alt.Chart(chart_data).mark_line(point=True).encode(
                x='Date:T',
                y='Bookings:Q'
            ).properties(width=700)
            st.altair_chart(line_chart, use_container_width=True)

            # Service-wise count
            st.subheader("🛠️ Services Distribution")
            service_counts = df['Service'].value_counts().reset_index()
            service_counts.columns = ['Service', 'Count']
            pie_chart = alt.Chart(service_counts).mark_arc().encode(
                theta="Count:Q",
                color="Service:N"
            )
            st.altair_chart(pie_chart, use_container_width=True)

            # ------------------ Delete individual booking ------------------
            st.markdown("### ❌ Delete a Booking")
            if not df.empty:
                idx = st.number_input("Row index to delete", 0, len(df)-1)
                if st.button("🗑️ Delete Booking"):
                    df.drop(index=idx, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    df.to_excel(EXCEL_FILE, index=False)
                    st.success("Booking deleted.")
                    st.rerun()

            # ------------------ Delete all bookings ------------------
            st.markdown("### 🚨 Delete All Bookings")
            if st.button("🧹 Delete All Bookings"):
                os.remove(EXCEL_FILE)
                st.success("All bookings deleted.")
                st.rerun()
                
            #-----------User Messages------------   
            st.markdown("---")
            st.subheader("📩 Contact Messages")

            if os.path.exists(CONTACT_FILE):
                df_contact = pd.read_excel(CONTACT_FILE)
                st.dataframe(df_contact)

                if not df_contact.empty:
                    st.markdown("### ✅ Mark Message as Resolved")
                    selected_index = st.number_input("Enter row index to mark as resolved", 0, len(df_contact)-1)

                    if st.button("✅ Mark as Resolved"):
                        df_contact.at[selected_index, "Status"] = "Resolved"
                        df_contact.to_excel(CONTACT_FILE, index=False)
                        st.success("Status updated to Resolved.")
                        st.rerun()

            else:
                st.info("No contact messages yet.")

        else:
            st.warning("No bookings yet.")
    else:
        st.error("❌ Incorrect password.")
