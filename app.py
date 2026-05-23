import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Menampilkan judul utama (yang sudah kamu buat)
st.title("📊 Dashboard ChemInsight")
st.markdown("---")

# --- NAVIGASI SIDEBAR ---
st.sidebar.title("🧪 Menu Navigasi")
menu = st.sidebar.radio("Pilih Fitur:", ["Home", "Kalkulator Parameter Kimia", "Analisis Data Lab"])

# --- MENU 1: HOME ---
if menu == "Home":
    st.subheader("Selamat Datang di ChemInsight")
    st.markdown("""
    Aplikasi web ini siap membantu Anda untuk:
    1. **Menghitung parameter kimia** (Molaritas & Massa Zat) secara instan.
    2. **Menganalisis data laboratorium** melalui statistik dasar dan grafik regresi linier.
    """)

# --- MENU 2: KALKULATOR PARAMETER KIMIA ---
elif menu == "Kalkulator Parameter Kimia":
    st.subheader("🧮 Kalkulator Molaritas & Massa")
    mode = st.selectbox("Komponen yang ingin dicari:", ["Molaritas (M)", "Massa Zat (gram)"])
    
    col1, col2 = st.columns(2)
    if mode == "Molaritas (M)":
        with col1:
            massa = st.number_input("Massa Zat (gram):", min_value=0.0, value=1.0, step=0.1)
            mr = st.number_input("Massa Molar / Mr (g/mol):", min_value=0.1, value=40.0, step=0.1)
        with col2:
            volume = st.number_input("Volume Larutan (mL):", min_value=0.1, value=100.0, step=1.0)
        
        if st.button("Hitung Molaritas"):
            molaritas = (massa / mr) * (1000 / volume)
            st.success(f"Hasil: Molaritas Larutan = {molaritas:.4f} M")
            
    elif mode == "Massa Zat (gram)":
        with col1:
            molaritas_target = st.number_input("Molaritas yang Diinginkan (M):", min_value=0.0, value=0.1, step=0.01)
            mr = st.number_input("Massa Molar / Mr (g/mol):", min_value=0.1, value=40.0, step=0.1)
        with col2:
            volume = st.number_input("Volume Larutan (mL):", min_value=0.1, value=100.0, step=1.0)
            
        if st.button("Hitung Massa"):
            massa_hasil = (molaritas_target * mr * volume) / 1000
            st.success(f"Hasil: Massa zat yang harus ditimbang = {massa_hasil:.4f} gram")

# --- MENU 3: ANALISIS DATA LAB ---
elif menu == "Analisis Data Lab":
    st.subheader("📊 Analisis & Visualisasi Data Laboratorium")
    uploaded_file = st.file_uploader("Unggah file CSV hasil lab Anda", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### 📋 Tabel Data", df)
        
        st.write("### 📈 Ringkasan Statistik", df.describe())
        
        # Fitur unduh statistik
        @st.cache_data
        def convert_df(dataframe):
            return dataframe.describe().to_csv().encode('utf-8')
        
        st.download_button("💾 Unduh Laporan Statistik (.CSV)", data=convert_df(df), file_name='laporan_statistik.csv', mime='text/csv')
        
        # Membuat Grafik
        kolom_numerik = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(kolom_numerik) >= 2:
            st.write("### 🖼️ Visualisasi Grafik")
            sumbu_x = st.selectbox("Sumbu X (misal: Konsentrasi):", kolom_numerik)
            sumbu_y = st.selectbox("Sumbu Y (misal: Absorbansi):", kolom_numerik)
            
            fig, ax = plt.subplots()
            sns.regplot(data=df, x=sumbu_x, y=sumbu_y, ax=ax, marker="o", color="teal")
            ax.grid(True)
            st.pyplot(fig)
    else:
        st.info("💡 Silakan unggah file CSV. Contoh format data yang benar:")
        st.table({'Konsentrasi_ppm': [1, 2, 3], 'Absorbansi': [0.15, 0.31, 0.46]})
