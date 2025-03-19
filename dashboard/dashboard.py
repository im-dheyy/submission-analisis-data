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
<<<<<<< HEAD
    st.header("📊 Rentang Waktu")
=======
    st.header(" Filter Data")
>>>>>>> 0ac4895716512fe8a9f67217e474a81864c77e13
    
    # Filter berdasarkan Rentang Waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    
    # Filtering Data
    filtered_day_df = day_df[day_df['dteday'].between(start_date, end_date)]
    filtered_hour_df = hour_df[hour_df['dteday'].between(start_date, end_date)]

# Membuat Line Chart untuk tren penggunaan casual vs registered
st.subheader("Tren Penggunaan Sepeda: Casual vs Registered")
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=filtered_day_df['dteday'], y=filtered_day_df['casual'], mode='lines', name='Casual', line=dict(color='blue')))
fig_line.add_trace(go.Scatter(x=filtered_day_df['dteday'], y=filtered_day_df['registered'], mode='lines', name='Registered', line=dict(color='red')))
fig_line.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Penyewa', template='plotly_white')
st.plotly_chart(fig_line)

<<<<<<< HEAD
=======
# Insight
st.markdown("""
**Insight:**
* Pengguna **registered** memiliki pola penggunaan yang lebih stabil dengan jumlah yang lebih tinggi.
* Pengguna **casual** cenderung mengalami lonjakan pada waktu tertentu, kemungkinan besar pada akhir pekan atau musim tertentu.
""")

>>>>>>> 0ac4895716512fe8a9f67217e474a81864c77e13
# Membuat Heatmap penggunaan sepeda berdasarkan jam dan hari
st.subheader("Heatmap Penggunaan Sepeda per Jam dan Hari")
filtered_hour_df['hr'] = pd.to_numeric(filtered_hour_df['hr'])
filtered_hour_df['weekday'] = pd.to_numeric(filtered_hour_df['weekday'])
heatmap_data = filtered_hour_df.pivot_table(values='cnt', index='weekday', columns='hr', aggfunc='mean')
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='coolwarm', ax=ax, cbar=True, linewidths=0.5)
st.pyplot(fig)

<<<<<<< HEAD
# Membuat Bar Chart untuk jumlah penggunaan sepeda berdasarkan musim
st.subheader("Jumlah Penggunaan Sepeda berdasarkan Musim")
fig_bar = px.bar(filtered_day_df, x='season', y='cnt', color='season', title='Jumlah Penggunaan Sepeda berdasarkan Musim')
fig_bar.update_layout(xaxis_title='Musim', yaxis_title='Jumlah Penyewa', template='plotly_white')
st.plotly_chart(fig_bar)
=======
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

>>>>>>> 0ac4895716512fe8a9f67217e474a81864c77e13

# Conclusions
st.header(" Kesimpulan")

<<<<<<< HEAD
st.subheader("1. Perbedaan Penggunaan Casual vs Registered")
st.write("- Pengguna registered memiliki pola penggunaan yang lebih stabil dan konsisten, mengindikasikan bahwa mereka menggunakan sepeda sebagai bagian dari rutinitas harian seperti berangkat kerja.")
st.write("- Pengguna casual lebih fluktuatif dengan lonjakan pada akhir pekan atau musim tertentu, menunjukkan bahwa mereka lebih cenderung menggunakan sepeda untuk rekreasi atau aktivitas santai.")

st.subheader("2. Waktu dan Faktor yang Mempengaruhi Penggunaan Sepeda")
st.write("- Heatmap menunjukkan bahwa penggunaan sepeda memuncak pada jam sibuk pagi (07:00 - 09:00) dan sore (17:00 - 19:00), terutama di hari kerja, mencerminkan pola komuter.")
st.write("- Pada akhir pekan, pola penggunaan lebih merata sepanjang hari, dengan peningkatan di siang hingga sore hari, menunjukkan lebih banyak penggunaan rekreasi.")
st.write("- Faktor musim juga berpengaruh: penggunaan sepeda tertinggi terjadi pada musim panas, sedangkan musim dingin memiliki penyewaan terendah, kemungkinan karena kondisi cuaca yang kurang nyaman.")
=======
st.subheader("1. Perbedaan Pola Penggunaan antara Pelanggan Terdaftar (Registered) dan Pengguna Kasual (Casual)")
st.write("Pengguna registered memiliki pola penggunaan yang stabil dan konsisten sepanjang waktu. Rata-rata jumlah pengguna registered per hari berkisar antara 2.500 - 7.500 penyewaan, dengan puncak tertinggi sekitar 8.500 penyewaan pada hari kerja. Hal ini menunjukkan bahwa pengguna registered lebih banyak menggunakan sepeda sebagai bagian dari rutinitas harian, seperti untuk perjalanan ke tempat kerja atau sekolah.")
st.write("Pengguna casual lebih fluktuatif dan cenderung meningkat pada akhir pekan dan musim panas. Rata-rata jumlah pengguna casual per hari berkisar antara 500 - 4.000 penyewaan, dengan lonjakan tertinggi mencapai 5.500 penyewaan pada akhir pekan. Hal ini menegaskan bahwa pengguna casual lebih banyak menggunakan sepeda untuk rekreasi dibandingkan dengan komuter harian.")

st.subheader("2. Waktu Puncak Penggunaan Sepeda dalam Sehari dan di Hari Apa")
st.write("Dari heatmap penggunaan sepeda, terlihat bahwa waktu puncak penggunaan terjadi pada 07:00 - 09:00 pagi dan 17:00 - 19:00 sore di hari kerja, dengan rata-rata penggunaan mencapai 4.000 - 6.500 penyewaan per jam selama periode tersebut. Ini mencerminkan bahwa sepeda banyak digunakan untuk perjalanan komuter.")
st.write("Di akhir pekan, pola penggunaan lebih merata sepanjang hari, dengan peningkatan dari 10:00 pagi hingga 17:00 sore, dengan jumlah penyewaan rata-rata 2.000 - 4.500 per jam. Ini menunjukkan bahwa penggunaan akhir pekan lebih bersifat rekreasi dibandingkan dengan hari kerja yang lebih berorientasi pada mobilitas komuter.")
>>>>>>> 0ac4895716512fe8a9f67217e474a81864c77e13
