import streamlit as st
import helper
from datetime import datetime
from collections import defaultdict

create_user_container=st.container()
user_data=defaultdict(str)

if not st.session_state.logged_in:
    st.write("Please Log in First")
elif st.session_state.user_data["role"]=="Administrator":
    with create_user_container:
        st.title("Create User")
        with st.form("user_create_form"):
            st.subheader("Account Information")
            user_name = st.text_input("Username")
            password = st.text_input("Password", type="password")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            allow_notification = st.selectbox("Allow Notification", options=["Y", "N"])
            profile_picture = st.text_input("Picture Link")

            st.subheader("Basic Information")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            preferred_name = st.text_input("Preferred Name")
            nric = st.text_input("NRIC")
            address = st.text_area("Address")
            date_of_birth = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", options=["M", "F"])
            contact_no = st.text_input("Contact Number")

            role=st.text_input("Role")

            # Submit button
            submitted = st.form_submit_button()
        if submitted:
            user_data = {
                "firstName": first_name,
                "lastName": last_name,
                "preferredName": preferred_name,
                "nric": nric,
                "address": address,
                "dateOfBirth": date_of_birth.isoformat(),
                "gender": gender,
                "contactNo": contact_no,
                "allowNotification": allow_notification,
                "profilePicture": profile_picture,
                "lockoutReason": "None",
                "loginTimeStamp": datetime.now().isoformat(),
                "lastPasswordChanged": datetime.now().isoformat(),
                "status": "Active",  # Default value
                "userName": user_name,
                "email": email,
                "emailConfirmed": "T",  # Default value
                "passwordHash": password,  # Replace with hashed password if required
                "securityStamp": "random_security_stamp",
                "concurrencyStamp": "random_concurrency_stamp",
                "phoneNumber": phone_number,
                "phoneNumberConfirmed": "T",  # Default value
                "twoFactorEnabled": "T",  # Default value
                "lockOutEnd": None,
                "lockOutEnabled": "F",  # Default value
                "accessFailedCount": 0,  # Default value
            }
            helper.create_user(user_data,role)
            st.write(user_data)
else:
    st.warning(f"Your role of {st.session_state.user_data["role"]} is not allowed to access this function!")
