import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Judul aplikasi
st.title("Prediksi Harga Properti")

# Input form
st.header("Masukkan Data Properti Anda")

# Input fields untuk berbagai fitur
bedrooms = st.number_input('Jumlah Kamar Tidur (Bedrooms)', min_value=0, max_value=10, value=1)
bathrooms = st.number_input('Jumlah Kamar Mandi (Bathrooms)', min_value=0, max_value=10, value=1)
beds = st.number_input('Jumlah Tempat Tidur (Beds)', min_value=0, max_value=10, value=1)
minimum_nights = st.number_input('Minimum Malam Menginap (Minimum Nights)', min_value=1, max_value=30, value=1)
maximum_nights = st.number_input('Maksimum Malam Menginap (Maximum Nights)', min_value=1, max_value=365, value=30)
availability_365 = st.number_input('Tersedia dalam 365 Hari (Availability 365)', min_value=0, max_value=365, value=365)
review_scores_rating = st.number_input('Skor Rating Ulasan (Review Scores Rating)', min_value=0, max_value=10, value=5)
reviews_per_month = st.number_input('Jumlah Ulasan per Bulan (Reviews per Month)', min_value=0.0, max_value=100.0, value=1.0)
room_type = st.selectbox('Tipe Kamar (Room Type)', ['Entire home/apt', 'Private room', 'Shared room'])
host_is_superhost = st.selectbox('Apakah Host Superhost?', ['Yes', 'No'])
neighbourhood = st.text_input('Lingkungan (Neighbourhood)', 'Unknown')
latitude = st.number_input('Lintang (Latitude)', min_value=-90.0, max_value=90.0, value=0.0)
longitude = st.number_input('Bujur (Longitude)', min_value=-180.0, max_value=180.0, value=0.0)
property_type = st.selectbox('Tipe Properti (Property Type)', ['House', 'Apartment', 'Condo', 'Loft', 'Villa'])

# Load model prediksi harga (misalnya model yang sudah dilatih disimpan dalam file .pkl)
model = joblib.load('random_search.joblib')  # Ganti dengan nama model Anda

# Fungsi untuk memproses input
def process_input():
    data = {
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'beds': beds,
        'minimum_nights': minimum_nights,
        'maximum_nights': maximum_nights,
        'availability_365': availability_365,
        'review_scores_rating': review_scores_rating,
        'reviews_per_month': reviews_per_month,
        'room_type': room_type,
        'host_is_superhost': 1 if host_is_superhost == 'Yes' else 0,
        'neighbourhood': neighbourhood,
        'latitude': latitude,
        'longitude': longitude,
        'property_type': property_type
    }
    input_df = pd.DataFrame([data])
    
    # Identifying numerical and categorical columns
    numerical_columns = input_df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = input_df.select_dtypes(include=['object']).columns
    
    # Handle missing values for numerical columns with median
    input_df[numerical_columns] = input_df[numerical_columns].fillna(input_df[numerical_columns].median())
    
    # Handle missing values for categorical columns with mode
    for col in categorical_columns:
        input_df[col] = input_df[col].fillna(input_df[col].mode()[0])
    
    # Apply one-hot encoding to categorical columns
    input_df = pd.get_dummies(input_df, columns=['room_type', 'neighbourhood', 'property_type'], drop_first=True)

    return input_df

 # Tombol untuk prediksi
    if st.button("Predict Price"):
        if model is not None:
            # Prediksi harga
            prediction = model.predict(input_data)
            st.write(f"🏡 **Predicted Price: ${prediction[0]:,.2f}**")
        else:
            st.error("⚠️ Model is not loaded. Please check the file and try again.")

