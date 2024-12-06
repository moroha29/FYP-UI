import streamlit as st
import requests
import helper

get_all_user_container=st.container()
get_user_container=st.container()
delete_user_container=st.container()
data=None

if not st.session_state.logged_in:
    st.write("Please Log in First")
else:
    with get_all_user_container:
        st.title("Get All User")
        if st.button("Get All Users"):
            try:
                # Define the API endpoint
                api_url = "http://localhost:8000/api/v1/users/"
                response = requests.get(api_url)
                if response.status_code == 200:
                    data=response.json()
            except Exception as e:
                st.error(f"Error: {e}")
        if st.session_state.user_data["role"]!="Administrator" and data:
            for i in data:
                i["nric"]=helper.nricMasker(i["nric"])
        if data: st.dataframe(data)
                
    with get_user_container:
        st.title("Get User")
        userId = st.text_input("User ID to be found")
        if st.button("Get User"):
            try:
                # Define the API endpoint
                api_url = f"http://localhost:8000/api/v1/users/{userId}"
                response = requests.get(api_url)
                if response.status_code == 200:
                    data=response.json()
                    if st.session_state.user_data["role"]!="Administrator":
                        data["nric"]=helper.nricMasker(data["nric"])
                    st.write(data)
            except Exception as e:
                st.error(f"Error: {e}")
    
    if st.session_state.user_data["role"]=="Administrator":
        with delete_user_container:
            st.title("Delete User")
            userId = st.text_input("User ID to be deleted")
            if st.button("Delete User"):
                try:
                    # Define the API endpoint
                    api_url = f"http://localhost:8000/api/v1/users/{userId}"
                    response = requests.delete(api_url)
                    if response.status_code == 200:
                        st.success("User has successfully been deleted")
                except Exception as e:
                    st.error(f"Error: {e}")
    