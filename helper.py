import streamlit as st
import requests

# Function to verify the token
def verify_token(token):
    api_url = "http://localhost:8000/api/v1/current_user"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Token is valid, return user data
        else:
            return None  # Token is invalid or expired
    except Exception as e:
        st.error(f"Error connecting to API for token verification: {e}")
        return None
    

def edit_user(api_url,userdata):
    try:
        response = requests.put(api_url, json=userdata)
        if response.status_code == 200:
            st.success("User has been updated") 
        else:
            return None 
    except Exception as e:
        st.error(f"Error connecting to API for token verification: {e}")
        return None

def create_user(user_data,role):
    api_url = "http://localhost:8000/api/v1/users"
    try:
        response = requests.post(api_url, json=user_data)
        if response.status_code == 200:
            data=response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error creating new User: {e}")
        return None
    
    api_url = "http://localhost:8000/api/v1/user_roles"
    roleId=2 if role=="Administrator" else 1

    try:
        roleData={
        "userId": data["id"],
        "roleId": roleId
        }
        response = requests.post(api_url, json=roleData)
        if response.status_code == 200:
            st.success(f"User has been created with role {role}") 
        else:
            return None 
    except Exception as e:
        st.error(f"Error creating new User Role: {e}")
        return None
    
def nricMasker(nric):
    return nric[0] + '*' * (len(nric) - 2) + nric[-1]