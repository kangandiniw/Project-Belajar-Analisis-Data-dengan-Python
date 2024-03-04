# Nama          : Kang, Andini Wulandari
# Email         : kangandiniw@gmail.com
# Id Dicoding   : kangandiniw

# Import Library
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# ==============================
# LOAD DATA
# ==============================


@st.cache_resource
def load_data():
    data = pd.read_csv("hour.csv")
    return data

data = load_data()


# ==============================
# TITLE DASHBOARD
# ==============================
# Set page title
st.title("Bike Sharing Dashboard :sparkles:")

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("Informasi:")
st.sidebar.markdown("**• Nama : Kang, Andini Wulandari**")
st.sidebar.markdown("**• Email : kangandiniw@gmail.com**")
st.sidebar.markdown("**• ID Dicoding : kangandiniw**")


st.sidebar.title("Dataset Bike Sharing")
# Show the dataset
if st.sidebar.checkbox("Show Dataset"):
    st.subheader("Raw Data")
    st.write(data)

# Display summary statistics
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(data.describe())

# Show dataset source
st.sidebar.markdown("[Download Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view?usp=sharing)")


# create a layout with two columns
col1, col2 = st.columns(2)

with col1:
    # Season-wise bike share count
    # st.subheader("Season-wise Bike Share Count")

    # Mapping dari angka ke label musim
    season_mapping = {1: "spring", 2: "summer", 3: "fall", 4: "winter"}
    data["season_label"] = data["season"].map(season_mapping)

    season_count = data.groupby("season_label")["cnt"].sum().reset_index()
    fig_season_count = px.bar(season_count, x="season_label",
                              y="cnt", title="Season-wise Bike Share Count")
    st.plotly_chart(fig_season_count, use_container_width=True,
                    height=400, width=600)

with col2:
    # Weather situation-wise bike share count
    # st.subheader("Weather Situation-wise Bike Share Count")

    weather_count = data.groupby("weathersit")["cnt"].sum().reset_index()
    fig_weather_count = px.bar(weather_count, x="weathersit",
                               y="cnt", title="Weather Situation-wise Bike Share Count")
    # Mengatur tinggi dan lebar gambar
    st.plotly_chart(fig_weather_count, use_container_width=True,height=400, width=800)


# Hourly bike share count
# st.subheader("Hourly Bike Share Count")
hourly_count = data.groupby("hr")["cnt"].sum().reset_index()
fig_hourly_count = px.line(
    hourly_count, x="hr", y="cnt", title="Hourly Bike Share Count")
st.plotly_chart(fig_hourly_count, use_container_width=True,
                height=400, width=600)


# create a layout with two columns
col1, col2 = st.columns(2)

with col1:
    # Humidity-wise bike share count
    # st.subheader("Humidity vs. Bike Share Count")
   
    # Humidity vs. Bike Share Count
    fig_humidity_chart = px.scatter(
        data, x="hum", y="cnt", title="Humidity vs. Bike Share Count")
    st.plotly_chart(fig_humidity_chart)


with col2:
    # Temperature-wise bike share count
    # st.subheader("Temperature vs. Bike Share Count")
    fig_temp_chart = px.scatter(data, x="weathersit", y="cnt",
                                title="Weathersit vs. Bike Share Count")
    st.plotly_chart(fig_temp_chart, use_container_width=True,
                    height=400, width=800)


# Fungsi untuk memfilter data berdasarkan pertanyaan
def filter_data(question, df):
    if question == "Distribusi jumlah sewa sepeda berdasarkan hari kerja dan hari libur selama bulan November - Desember tahun 2012":
        # Filter data untuk bulan November - Desember tahun 2012
        nov_dec_data = df[(df['dteday'].str.startswith('2012-11')) | (df['dteday'].str.startswith('2012-12'))]

        # Pisahkan data menjadi hari kerja dan hari libur
        weekday_data = nov_dec_data[nov_dec_data['workingday'] == 1]
        holiday_data = nov_dec_data[nov_dec_data['workingday'] == 0]

        # Hitung jumlah sewa sepeda untuk setiap hari
        weekday_cnt = weekday_data['cnt'].sum()
        holiday_cnt = holiday_data['cnt'].sum()
        
        return weekday_cnt, holiday_cnt
    elif question == "Bagaimana tingkat kelembaban mempengaruhi jumlah sewa sepeda selama musim dingin?":
        # Filter data untuk musim dingin
        winter_data = df[df['season'] == 4]
        return winter_data
    elif question == "Apa hubungan cuaca dengan jumlah pengguna yang terdaftar?":
        # Filter data berdasarkan cuaca
        weather_data = df.groupby('weathersit')['registered'].sum().reset_index()
        return weather_data
    elif question == "Berapa jumlah total sewa sepeda untuk tahun 2012 selama musim gugur dan dingin?":
        # Filter data untuk tahun 2012 selama musim gugur (season 3) dan musim dingin (season 4)
        autumn_winter_data = df[(df['yr'] == 1) & ((df['season'] == 3) | (df['season'] == 4))]
        
        autumn_total_data = autumn_winter_data[autumn_winter_data['season'] == 3]
        winter_total_data = autumn_winter_data[autumn_winter_data['season'] == 4]
        
        # Hitung jumlah total sewa sepeda untuk musim gugur dan dingin
        autumn_total_cnt = autumn_total_data['cnt'].sum()
        winter_total_cnt = winter_total_data['cnt'].sum()

        return autumn_total_cnt, winter_total_cnt


# Menyiapkan aplikasi Streamlit
st.title('Dashboard Analisis Sewa Sepeda')
question = st.sidebar.selectbox(
    'Pilih Pertanyaan:',
    ("Distribusi jumlah sewa sepeda berdasarkan hari kerja dan hari libur selama bulan November - Desember tahun 2012",
     "Bagaimana tingkat kelembaban mempengaruhi jumlah sewa sepeda selama musim dingin?",
     "Apa hubungan cuaca dengan jumlah pengguna yang terdaftar?",
     "Berapa jumlah total sewa sepeda untuk tahun 2012 selama musim gugur dan dingin?")
)

# Memfilter data berdasarkan pertanyaan
filtered_data = filter_data(question, data)

# Membuat visualisasi
if question == "Distribusi jumlah sewa sepeda berdasarkan hari kerja dan hari libur selama bulan November - Desember tahun 2012":
    # Visualisasi distribusi jumlah sewa sepeda
    weekday_cnt, holiday_cnt = filtered_data  # Mendapatkan nilai weekday_cnt dan holiday_cnt dari hasil filter_data
    labels = ['Hari Kerja', 'Hari Libur']
    counts = [weekday_cnt, holiday_cnt]

    plt.bar(labels, counts, color=['blue', 'green'])
    plt.title('Distribusi Jumlah Sewa Sepeda Selama Bulan November - Desember 2012 Berdasarkan Hari Kerja dan Hari Libur')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Sewa Sepeda (cnt)')
    st.pyplot(plt)  # Menampilkan plot menggunakan st.pyplot()

elif question == "Bagaimana tingkat kelembaban mempengaruhi jumlah sewa sepeda selama musim dingin?":
    # Visualisasi hubungan antara tingkat kelembaban dan jumlah sewa sepeda
    fig, ax = plt.subplots()
    ax.scatter(filtered_data['hum'], filtered_data['cnt'])
    ax.set_title('Hubungan antara Tingkat Kelembaban dan Jumlah Sewa Sepeda selama Musim Dingin')
    ax.set_xlabel('Tingkat Kelembaban')
    ax.set_ylabel('Jumlah Sewa Sepeda (cnt)')
    st.pyplot(fig)

elif question == "Apa hubungan cuaca dengan jumlah pengguna yang terdaftar?":
    # Scatter plot untuk memvisualisasikan hubungan cuaca dengan jumlah pengguna terdaftar
    fig = px.scatter(filtered_data, x="weathersit", y="registered", title="Hubungan Cuaca dengan Jumlah Pengguna yang Terdaftar")
    fig.update_xaxes(title="Cuaca (weathersit)")
    fig.update_yaxes(title="Jumlah Pengguna Terdaftar")
    st.plotly_chart(fig)

elif question == "Berapa jumlah total sewa sepeda untuk tahun 2012 selama musim gugur dan dingin?":
    # Buat visualisasi
    autumn_total_cnt, winter_total_cnt = filtered_data
    labels = ['Musim Gugur', 'Musim Dingin']
    counts = [autumn_total_cnt, winter_total_cnt]
    
    plt.bar(labels, counts, color=['yellow', 'red'])
    plt.title('Jumlah total sewa sepeda untuk tahun 2012 selama musim gugur dan dingin')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Sewa Sepeda (cnt)')
    st.pyplot(plt)  # Menampilkan plot menggunakan st.pyplot()

    # Analisis penjelasan
    st.write("Jumlah total sewa sepeda untuk tahun 2012 selama musim gugur dan dingin adalah:", filtered_data)
