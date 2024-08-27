import streamlit as st


import pandas as pd
import requests
import folium
from streamlit_folium import folium_static
from math import sqrt

# Your existing function to calculate Euclidean distance
def euclidean_distance(lat1, lon1, lat2, lon2):
    return sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

# Your existing code to fetch random users from the API
def fetch_random_users(n=100):
    url = f"https://randomuser.me/api/?results={n}"
    response = requests.get(url)
    data = response.json()
    users = data['results']
    
    user_list = []
    for user in users:
        user_info = {
            'uid': user['login']['uuid'],
            'email': user['email'],
            'first_name': user['name']['first'],
            'last_name': user['name']['last'],
            'latitude': float(user['location']['coordinates']['latitude']),
            'longitude': float(user['location']['coordinates']['longitude']),
        }
        user_list.append(user_info)
    return pd.DataFrame(user_list)

# Your existing function to find the nearest users
def find_nearest_users(df, email, n=5):
    user = df[df['email'] == email]
    if user.empty:
        return pd.DataFrame()  # Return empty DataFrame if email not found
    
    user_lat = user['latitude'].values[0]
    user_lon = user['longitude'].values[0]

    df['distance'] = df.apply(lambda row: euclidean_distance(user_lat, user_lon, row['latitude'], row['longitude']), axis=1)

    nearest_users = df[df['email'] != email].sort_values(by='distance').head(n)
    return nearest_users

# Initialize or load data into session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = pd.DataFrame()

# Streamlit App
st.title("Meet Up App")

# Button to fetch random users
if st.button("Fetch Random Users"):
    new_users = fetch_random_users(5)
    st.session_state.user_data = pd.concat([st.session_state.user_data, new_users]).drop_duplicates(subset='uid')
    st.success(f"Fetched {len(new_users)} new users!")

# Display the number of users stored
st.write(f"Total users stored: {len(st.session_state.user_data)}")

# Dropdown to select a user by email
selected_email = st.selectbox("Select a User by Email", st.session_state.user_data['email'].unique() if not st.session_state.user_data.empty else [])

if selected_email:
    # Find and display nearest users
    nearest_users = find_nearest_users(st.session_state.user_data, selected_email, n=100)
    st.write(f"Showing nearest 100 users to {selected_email}")
    
    # Display on map using Folium
    selected_user = st.session_state.user_data[st.session_state.user_data['email'] == selected_email].iloc[0]
    m = folium.Map(location=[selected_user['latitude'], selected_user['longitude']], zoom_start=5)
    
    folium.Marker(
        location=[selected_user['latitude'], selected_user['longitude']],
        popup=f"{selected_user['first_name']} {selected_user['last_name']} (Selected User)",
        icon=folium.Icon(color="red")
    ).add_to(m)
    
    for _, user in nearest_users.iterrows():
        folium.Marker(
            location=[user['latitude'], user['longitude']],
            popup=f"{user['first_name']} {user['last_name']}",
        ).add_to(m)
    
    folium_static(m)

