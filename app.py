import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import logging
import firebase_admin
from firebase_admin import credentials, firestore

#logging.basicConfig(level=logging.INFO)

if not firebase_admin._apps:
    cred = credentials.Certificate("crimeagainstwomenindex-firebase-adminsdk-7b0uc-1ff3e12bed.json") 
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title('Crime Against Women Index - Kolkata')

st.write('**If you have anything to report, please feel free to report**')

text = st.text_input('Enter your report here')

reports = []
if st.button('Submit'):
    if text:
        
        doc_ref = db.collection('Reports').add({
            'report': text,
            'status': 'submitted'
        })
        
        st.write('Your report has been recorded in Firestore')
    else:
        st.write('Please enter a report before submitting.')
    
df_filtered = pd.read_csv('Final.csv')

station_names = df_filtered['Police Station Name'].tolist()
selected_station = st.selectbox("Select a Police Station", station_names)

selected_row = df_filtered[df_filtered['Police Station Name'] == selected_station].iloc[0]

st.write(f"**Crime Against Women Index for {selected_station}:** {selected_row['Crime Against Women Index']}")

nm = folium.Map(location=[selected_row['Latitude'],selected_row['Longitude']],zoom_start=13)
folium.Marker(
    location=[selected_row['Latitude'],selected_row['Longitude']],
    popup=selected_row['Police Station Name'],
    icon=folium.Icon(color=selected_row['Crime Against Women Index'].lower())
).add_to(nm)

st_folium(nm, width=700, height=500)
    

st.image('output.png')

# Create a folium map
m = folium.Map(location=[22.526493, 88.332369], zoom_start=13)

# Add markers to the map
for index, row in df_filtered.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Police Station Name'],
        icon=folium.Icon(color=row['Crime Against Women Index'].lower())
    ).add_to(m)

# Display the map in Streamlit

st.write("**Interactive Map Showing Crime Index**")

st_folium(m, width=700, height=500)

