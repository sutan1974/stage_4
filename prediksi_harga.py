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
    
    # Lakukan one-hot encoding pada kolom kategori
    input_df = pd.get_dummies(input_df, columns=['room_type', 'neighbourhood', 'property_type'], drop_first=True)

    # Memastikan kolom pada input sesuai dengan kolom yang digunakan saat pelatihan model
    model_columns = input_df.columns
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0  # Jika ada kolom yang hilang, tambahkan dengan nilai 0
    
    # Memastikan tidak ada missing values
    input_df = input_df.fillna(0)

    return input_df

# Tombol prediksi harga
if st.button('Prediksi Harga'):
    # Proses input
    input_data = process_input()

    # Prediksi harga menggunakan model yang sudah dilatih
    prediction = model.predict(input_data)
    
    # Menampilkan hasil prediksi
    st.subheader(f"Prediksi Harga: ${prediction[0]:,.2f}")

