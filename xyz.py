# # import sqlite3
# import streamlit as st
# st.title("Hello streamlit !!!")

# #importing the required libraries 
# import requests
# import pandas as pd
# import uuid
# from datetime import datetime

# #Using get to call API:
# url = "https://randomuser.me/api/?results=100"
# response = requests.get(url)
# data = response.json()

# #extracting the list of 100 users from response
# users100 = data['results']
# user_list = []
# for user in users100:
#     user_info = {
#         'uid': user['login']['uuid'],
#         'email': user['email'],
#         'first name': user['name']['first'],
#         'last name': user['name']['last'],
#         'gender': user['gender'],
#         'latitude': user['location']['coordinates']['latitude'],
#         'longitude': user['location']['coordinates']['longitude']
#     }
# user_list.append(user_info)

# df100 = pd.DataFrame(user_list)

# # creating a class object:
# class User:
#     def __init__(self, user_data):
#         self.user_data = user_data
    
#     def flatten_dict(self, d=None, parent_key='', sep='_'):
#         if d is None:
#             d = self.user_data
#         items = []
#         for k, v in d.items():
#             new_key = f"{parent_key}{sep}{k}" if parent_key else k
#             if isinstance(v, dict):
#                 items.extend(self.flatten_dict(v, new_key, sep=sep).items())
#             else:
#                 items.append((new_key, v))
#         return dict(items)
    
#     def to_dict(self):
#         return self.flatten_dict()
    

import streamlit as st
import pandas as pd

if 'user_data' not in st.session_state:
    st.session_state.user_data = pd.DataFrame()

st.write("Test complete")