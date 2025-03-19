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
    st.header("📊 Rentang Waktu")
    
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

# Membuat Heatmap penggunaan sepeda berdasarkan jam dan hari
st.subheader("Heatmap Penggunaan Sepeda per Jam dan Hari")
filtered_hour_df['hr'] = pd.to_numeric(filtered_hour_df['hr'])
filtered_hour_df['weekday'] = pd.to_numeric(filtered_hour_df['weekday'])
heatmap_data = filtered_hour_df.pivot_table(values='cnt', index='weekday', columns='hr', aggfunc='mean')
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='coolwarm', ax=ax, cbar=True, linewidths=0.5)
st.pyplot(fig)

# Membuat Bar Chart untuk jumlah penggunaan sepeda berdasarkan musim
st.subheader("Jumlah Penggunaan Sepeda berdasarkan Musim")
fig_bar = px.bar(filtered_day_df, x='season', y='cnt', color='season', title='Jumlah Penggunaan Sepeda berdasarkan Musim')
fig_bar.update_layout(xaxis_title='Musim', yaxis_title='Jumlah Penyewa', template='plotly_white')
st.plotly_chart(fig_bar)

# Conclusions
st.header("📌 Kesimpulan")

st.subheader("1. Perbedaan Penggunaan Casual vs Registered")
st.write("- Pengguna registered memiliki pola penggunaan yang lebih stabil dan konsisten, mengindikasikan bahwa mereka menggunakan sepeda sebagai bagian dari rutinitas harian seperti berangkat kerja.")
st.write("- Pengguna casual lebih fluktuatif dengan lonjakan pada akhir pekan atau musim tertentu, menunjukkan bahwa mereka lebih cenderung menggunakan sepeda untuk rekreasi atau aktivitas santai.")

st.subheader("2. Waktu dan Faktor yang Mempengaruhi Penggunaan Sepeda")
st.write("- Heatmap menunjukkan bahwa penggunaan sepeda memuncak pada jam sibuk pagi (07:00 - 09:00) dan sore (17:00 - 19:00), terutama di hari kerja, mencerminkan pola komuter.")
st.write("- Pada akhir pekan, pola penggunaan lebih merata sepanjang hari, dengan peningkatan di siang hingga sore hari, menunjukkan lebih banyak penggunaan rekreasi.")
st.write("- Faktor musim juga berpengaruh: penggunaan sepeda tertinggi terjadi pada musim panas, sedangkan musim dingin memiliki penyewaan terendah, kemungkinan karena kondisi cuaca yang kurang nyaman.")
