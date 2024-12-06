import streamlit as st
import requests
from collections import defaultdict
from datetime import datetime
import helper

edit_user_container=st.container()
current_user_data={}

if not st.session_state.logged_in:
    st.write("Please Log in First")
else:
    with edit_user_container:
        st.title("Edit User")
        try:
            # Define the API endpoint
            api_url = f"http://localhost:8000/api/v1/users/{st.session_state.user_data["userId"]}" 
            response = requests.get(api_url)
            if response.status_code == 200:
                current_user_data=response.json()
        except Exception as e:
            st.error(f"Error: {e}")

        with st.form("user_edit_form"):
            st.subheader("Basic Information")
            first_name = st.text_input("First Name", value=current_user_data["firstName"])
            last_name = st.text_input("Last Name", value=current_user_data["lastName"])
            preferred_name = st.text_input("Preferred Name", value=current_user_data["preferredName"])
            nric = st.text_input("NRIC", value=current_user_data["nric"])
            address = st.text_area("Address", value=current_user_data["address"])
            date_of_birth = st.date_input(
                "Date of Birth",
                value=datetime.fromisoformat(current_user_data["dateOfBirth"].replace("Z", ""))
            )
            gender = st.selectbox(
                "Gender",
                options=["Male", "Female"],
                index=["M", "F"].index(current_user_data["gender"])
            )
            contact_no = st.text_input("Contact Number", value=current_user_data["contactNo"])
            allow_notification = st.selectbox(
                "Allow Notification",
                options=["Yes", "No"],
                index=0 if current_user_data["allowNotification"] == "T" else 1
            )

            st.subheader("Account Information")
            user_name = st.text_input("Username", value=current_user_data["userName"])
            email = st.text_input("Email", value=current_user_data["email"])
            phone_number = st.text_input("Phone Number", value=current_user_data["phoneNumber"])

            # Submit button
            submitted = st.form_submit_button("Save Changes")

        if submitted:
            current_user_data["firstName"]= first_name
            current_user_data["lastName"]= last_name
            current_user_data["preferredName"]= preferred_name
            current_user_data["nric"]= nric
            current_user_data["address"]= address
            current_user_data["dateOfBirth"]= date_of_birth.isoformat()+"T23:39:04.804Z"
            current_user_data["gender"]= "M" if gender=="Male" else "F"
            current_user_data["contactNo"]= contact_no
            current_user_data["allowNotification"]= "Y" if allow_notification=="Yes" else "N"
            current_user_data["userName"]= user_name
            current_user_data["email"]= email
            current_user_data["phoneNumber"]= phone_number
            st.write(current_user_data)
            helper.edit_user(api_url=api_url,userdata=current_user_data)