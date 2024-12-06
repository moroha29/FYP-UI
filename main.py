import streamlit as st
import requests
import helper
from collections import defaultdict

# Initialize session state for token and logged-in status
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_data" not in st.session_state:
    st.session_state.user_data = defaultdict(str)

# Login and welcome containers
login_container = st.container()
welcome_container = st.container()

# Check if user is logged in
if st.session_state.logged_in and st.session_state.access_token:
    # Welcome Page
    with welcome_container:
        # Verify the token
        user_data = helper.verify_token(st.session_state.access_token)
        if user_data:
            st.title("Welcome Page")
            st.success(f"Welcome, {user_data.get('sub', 'User')}!")
            st.write("You are successfully logged in.")
            st.write("Token Data:", user_data)
            st.write("Token:", st.session_state.access_token)
            st.session_state.user_data=user_data

            # Logout button
            if st.button("Logout"):
                st.session_state.access_token = None
                st.session_state.logged_in = False
                st.rerun()
        else:
            st.session_state.access_token = None
            st.session_state.logged_in = False
            st.warning("Session expired. Please log in again.")
            st.rerun()
else:
    # Login Page
    with login_container:
        st.title("Login Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                try:
                    # Define the API endpoint
                    api_url = "http://localhost:8000/api/v1/login" 
                    response = requests.post(api_url, data={"username": username, "password": password})

                    if response.status_code == 200:
                        token = response.json().get("access_token")
                        if token:
                            st.session_state.access_token = token
                            st.session_state.logged_in = True
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Failed to retrieve token.")
                    elif response.status_code == 401:
                        st.error("Invalid credentials. Please try again.")
                    else:
                        st.error("An error occurred during login.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter both username and password.")
