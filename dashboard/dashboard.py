import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
day_df = pd.read_csv("./dashboard/day_fix.csv")
hour_df = pd.read_csv("./dashboard/hour_fix.csv")

# Konversi kolom dteday ke datetime64[ns]
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Menentukan rentang tanggal
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

st.title("Dashboard Bike Sharing")

# Menampilkan Statistik Utama
total_penyewaan = day_df['cnt'].sum()
total_casual = day_df['casual'].sum()
total_registered = day_df['registered'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{total_penyewaan:,}")
col2.metric("Total Casual", f"{total_casual:,}")
col3.metric("Total Registered", f"{total_registered:,}")

st.markdown("""
Dashboard ini menampilkan analisis penggunaan sepeda berdasarkan pengguna **casual** dan **registered**, 
serta pola penggunaan berdasarkan jam dan hari dalam seminggu.
""")

# Sidebar
with st.sidebar:
    st.image("bikerentalid.png")
    st.header(" Filter Data")
    
    # Filter berdasarkan Rentang Waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    
    # Filter berdasarkan Tahun
    year_option = st.selectbox("Pilih Tahun", sorted(day_df['yr'].unique()), format_func=lambda x: f"{2011 + x}")
    
    # Filtering Data
    filtered_day_df = day_df[(day_df['yr'] == year_option) & (day_df['dteday'].between(start_date, end_date))]
    filtered_hour_df = hour_df[(hour_df['yr'] == year_option) & (hour_df['dteday'].between(start_date, end_date))]
    
    # Filter berdasarkan Musim
    season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
    season_option = st.multiselect("Pilih Musim", sorted(day_df['season'].unique()), format_func=lambda x: season_mapping.get(x, f"Musim {x}"))
    if season_option:
        filtered_day_df = filtered_day_df[filtered_day_df['season'].isin(season_option)]
        filtered_hour_df = filtered_hour_df[filtered_hour_df['season'].isin(season_option)]
    
    # Filter berdasarkan Hari Kerja vs Akhir Pekan
    workingday_option = st.radio("Hari Kerja atau Akhir Pekan?", ["Semua", "Hari Kerja", "Akhir Pekan"])
    if workingday_option == "Hari Kerja":
        filtered_day_df = filtered_day_df[filtered_day_df['workingday'] == 1]
        filtered_hour_df = filtered_hour_df[filtered_hour_df['workingday'] == 1]
    elif workingday_option == "Akhir Pekan":
        filtered_day_df = filtered_day_df[filtered_day_df['workingday'] == 0]
        filtered_hour_df = filtered_hour_df[filtered_hour_df['workingday'] == 0]

# Membuat Line Chart untuk tren penggunaan casual vs registered
st.subheader("Tren Penggunaan Sepeda: Casual vs Registered")
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=filtered_day_df['dteday'], y=filtered_day_df['casual'], mode='lines', name='Casual', line=dict(color='blue')))
fig_line.add_trace(go.Scatter(x=filtered_day_df['dteday'], y=filtered_day_df['registered'], mode='lines', name='Registered', line=dict(color='red')))
fig_line.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Penyewa', template='plotly_white')
st.plotly_chart(fig_line)

# Insight
st.markdown("""
**Insight:**
* Pengguna **registered** memiliki pola penggunaan yang lebih stabil dengan jumlah yang lebih tinggi.
* Pengguna **casual** cenderung mengalami lonjakan pada waktu tertentu, kemungkinan besar pada akhir pekan atau musim tertentu.
""")

# Membuat Heatmap penggunaan sepeda berdasarkan jam dan hari
st.subheader("Heatmap Penggunaan Sepeda per Jam dan Hari")

# Pastikan kolom hr dan weekday bertipe numerik
filtered_hour_df['hr'] = pd.to_numeric(filtered_hour_df['hr'])
filtered_hour_df['weekday'] = pd.to_numeric(filtered_hour_df['weekday'])

heatmap_data = filtered_hour_df.pivot_table(values='cnt', index='weekday', columns='hr', aggfunc='mean')
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='coolwarm', ax=ax, cbar=True, linewidths=0.5)
st.pyplot(fig)

# Insight
st.markdown("""
**Insight:**
* Penggunaan sepeda meningkat pada jam sibuk, yaitu sekitar **07:00 - 09:00 pagi** dan **17:00 - 19:00 sore**, kemungkinan besar berhubungan dengan aktivitas kerja.
* Pada akhir pekan, pola penggunaan lebih merata sepanjang hari tanpa lonjakan signifikan seperti pada hari kerja.
* Aktivitas tertinggi cenderung terjadi pada hari kerja saat jam berangkat dan pulang kantor.
""")

# Penggunaan casual vs registered berdasarkan hari dalam seminggu
fig, ax = plt.subplots(figsize=(12, 6))
day_df.groupby('weekday')[['casual', 'registered']].mean().plot(kind='bar', ax=ax)
plt.title('Rata-rata Pengguna Casual vs Registered per Hari')
plt.ylabel('Jumlah Pengguna')
plt.xlabel('Hari dalam Seminggu')
plt.legend(['Casual', 'Registered'])
st.pyplot(fig)


# Conclusions
st.header(" Kesimpulan")

st.subheader("1. Perbedaan Pola Penggunaan antara Pelanggan Terdaftar (Registered) dan Pengguna Kasual (Casual)")
st.write("Pengguna registered memiliki pola penggunaan yang stabil dan konsisten sepanjang waktu. Rata-rata jumlah pengguna registered per hari berkisar antara 2.500 - 7.500 penyewaan, dengan puncak tertinggi sekitar 8.500 penyewaan pada hari kerja. Hal ini menunjukkan bahwa pengguna registered lebih banyak menggunakan sepeda sebagai bagian dari rutinitas harian, seperti untuk perjalanan ke tempat kerja atau sekolah.")
st.write("Pengguna casual lebih fluktuatif dan cenderung meningkat pada akhir pekan dan musim panas. Rata-rata jumlah pengguna casual per hari berkisar antara 500 - 4.000 penyewaan, dengan lonjakan tertinggi mencapai 5.500 penyewaan pada akhir pekan. Hal ini menegaskan bahwa pengguna casual lebih banyak menggunakan sepeda untuk rekreasi dibandingkan dengan komuter harian.")

st.subheader("2. Waktu Puncak Penggunaan Sepeda dalam Sehari dan di Hari Apa")
st.write("Dari heatmap penggunaan sepeda, terlihat bahwa waktu puncak penggunaan terjadi pada 07:00 - 09:00 pagi dan 17:00 - 19:00 sore di hari kerja, dengan rata-rata penggunaan mencapai 4.000 - 6.500 penyewaan per jam selama periode tersebut. Ini mencerminkan bahwa sepeda banyak digunakan untuk perjalanan komuter.")
st.write("Di akhir pekan, pola penggunaan lebih merata sepanjang hari, dengan peningkatan dari 10:00 pagi hingga 17:00 sore, dengan jumlah penyewaan rata-rata 2.000 - 4.500 per jam. Ini menunjukkan bahwa penggunaan akhir pekan lebih bersifat rekreasi dibandingkan dengan hari kerja yang lebih berorientasi pada mobilitas komuter.")