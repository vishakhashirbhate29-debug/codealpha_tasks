import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("☁️ Data Redundancy Removal System")
st.write("Check new data before adding it to the cloud database.")

name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone")

if st.button("Check & Add Data"):

    if not name or not email or not phone:
        st.warning("Please fill all fields.")
    else:
        result = supabase.table("records").select("*").eq(
            "email", email
        ).execute()

        existing = result.data

        if existing:
            same_record = any(
                row["phone"] == phone for row in existing
            )

            if same_record:
                st.error("❌ Redundant data detected! Record already exists.")
            else:
                st.warning(
                    "⚠️ Email exists, but the phone number is different."
                )
        else:
            supabase.table("records").insert({
                "name": name,
                "email": email,
                "phone": phone,
                "status": "verified"
            }).execute()

            st.success("✅ Unique data added successfully!")